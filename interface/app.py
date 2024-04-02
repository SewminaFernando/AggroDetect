from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

from interface.save_report import firebase_datastore, read_users_data_from_firebase, convert_to_conversation_dict
from model_pipeline import agg_by_voice, agg_by_text, department_by_text, text_to_speech, transcribe_audio, chat, \
    send_message_to_rasa
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

first_time = True

# Create a list to store the conversation
old_conv = []
department = ""

def overall_sentiment():
    global old_conv
    text_agg_count = 0
    voice_agg_count = 0
    for conv in old_conv:
        if conv['agg_text'] == 'Aggressive':
            text_agg_count += 1
        elif conv['agg_text'] == 'Aggressive':
            voice_agg_count += 1

    if text_agg_count > voice_agg_count:
        return 'Aggressive'
    elif voice_agg_count > text_agg_count:
        return 'Aggressive'
    else:
        return 'Neutral'
    
def agent_name():
    # Get the agent name from the database
    pass

def set_firebase_dictionary():
    global old_conv

    new_conv = {
    "user_message": ["-"],
    "resp": ["Thank you for calling us. How can I help you?"]
    }
    for i in range(len(old_conv)):
        new_conv["user_message"].append(f"{old_conv[i]['user_messagee']} (Aggressiveness by text: {old_conv[i]['agg_text']}) (Aggressiveness by voice: {old_conv[i]['agg_voice']})")
        new_conv["resp"].append(old_conv[i]["resp"])

    return new_conv


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/sign-out')
def sign_out():
    return redirect(url_for('login_page'))

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('Database/Agents.db')
    c = conn.cursor()
    c.execute('SELECT * FROM agentLogIn WHERE userName = ? AND password = ?', (username, password))
    result = c.fetchone()
    conn.close()
    
    if result:
        return redirect(url_for('dashboard'))
    else:
        return 'Login failed. Please check your username and password.'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/end-conversation' , methods=['POST'])
def end_conversation():
    # clear all files in the uploads folder
    for file in os.listdir('uploads'):
        os.remove(os.path.join('uploads', file))
    agent_name = "Agent 1"
    overall_sentiment = "Neutral"
    # Save the conversation to the database
    # Clear the conversation list
    old_conv.clear()
    return jsonify({'agent_name': agent_name, 'overall_sentiment': overall_sentiment})
    
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)

@app.route('/record', methods=['POST','GET'])
def receive_audio():
    global first_time
    global old_conv
    global department
    if 'audio' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # if uploads folder does not exist, create it
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        audio_file.save('uploads/recorded_audio.webm')
    except Exception as e:
        return jsonify({'error': f'Error saving audio: {str(e)}'}), 500
    
    transcript = transcribe_audio("uploads/recorded_audio.webm")
    voice_agg = agg_by_voice("uploads/n_audio.wav")
    text_agg = agg_by_text(transcript)
    if first_time:
        dep_text = department_by_text(transcript)
        department = dep_text
        first_time = False
    response, end_converastion = chat(transcript)

    audio_path="../"+text_to_speech(response)

    # create a dictionary to store the conversation
    dictionary = {
        "user_messagee": transcript,
        "agg_voice": voice_agg,
        "agg_text": text_agg,
        "resp": response
    }
    
    # append the dictionary to the list
    old_conv.append(dictionary)

    if end_conversation:
        firebase_datastore('', set_firebase_dictionary(), department=department)

    return jsonify({'transcript': old_conv, 'audio_path': audio_path, "dep":department})

@app.route('/chat_history')
def index():
    # Read data from Firebase
    users_data, _ = read_users_data_from_firebase()
    print(users_data)
    # Convert data to conversation format
    conversation_dict = convert_to_conversation_dict(users_data)
    print(conversation_dict)
    # Pass conversation_dict to the HTML template
    return render_template('interface.html', conversation_dict = (conversation_dict))

if __name__ == '__main__':
    app.run(debug=True)
