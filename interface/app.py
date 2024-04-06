from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

from save_report import firebase_datastore, read_users_data_from_firebase, convert_to_conversation_dict
from model_pipeline import agg_by_voice, agg_by_text, department_by_text, text_to_speech, transcribe_audio, chat
import sqlite3
import os
import datetime
from calendar import month_name

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

first_time = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/sign-out')
def sign_out():
    return redirect(url_for('home'))

@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('Database/AggroDetect.db')
    cursor = conn.cursor()

    # Retrieve unique sorted months from the database
    cursor.execute("SELECT DISTINCT month AS month FROM Analytics ORDER BY month")
    months_data = cursor.fetchall()

    # Extract and sort unique months
    month_map = {month_name[i]: i for i in range(1, 13)}
    labels = sorted([row[0] for row in months_data], key=lambda x: month_map[x])

    # Prepare data for the chart
    datasets = [
        {"label": "Aggressive Customers", "fill": False, "borderColor": "red", "data": [0] * len(labels)},
        {"label": "Non-aggressive Customers", "fill": False, "borderColor": "green", "data": [0] * len(labels)},
        {"label": "Neutral Customers", "fill": False, "borderColor": "blue", "data": [0] * len(labels)}
    ]

    # Retrieve sentiment counts for each month
    cursor.execute("SELECT month AS month, SUM(CASE WHEN sentiment = 'Aggressive' THEN 1 ELSE 0 END) AS aggressive, SUM(CASE WHEN sentiment = 'Neutral' THEN 1 ELSE 0 END) AS neutral, SUM(CASE WHEN sentiment = 'Non-Aggressive' THEN 1 ELSE 0 END) AS non_aggressive FROM Analytics GROUP BY month ORDER BY month")
    data = cursor.fetchall()

    for row in data:
        month_str = row[0]
        if month_str is not None and month_str in month_map:
            month_index = month_map[month_str]
            datasets[0]["data"][labels.index(month_str)] = row[1]  # Aggressive count
            datasets[1]["data"][labels.index(month_str)] = row[3]  # Non-aggressive count
            datasets[2]["data"][labels.index(month_str)] = row[2]  # Neutral count

    chart_data = {"labels": labels, "datasets": datasets}

    conn.close()

    return render_template('analytics.html', active_page='analytics', chart_data=chart_data)


@app.route('/login', methods=['POST'])
def login():
    login_username = "admin"
    login_password = "admin234"
    username = request.form['username']
    password = request.form['password']
    
    if username == login_username and password == login_password:
        return redirect(url_for('dashboard'))
    elif username == login_username and password != login_password:
        error_message = 'Incorrect password.'
        return render_template('login.html', error_message=error_message)
    elif username != login_username:
        error_message = 'Incorrect username.'
        return render_template('login.html', error_message=error_message)
    else:
        error_message = 'Login failed.'
        return render_template('login.html', error_message=error_message)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

# Create a list to store the conversation
old_conv = []
department = ""

def overall_sentiment():
    global old_conv
    # Get the last response from the conversation
    agg_voice, agg_text = old_conv[-1]["agg_voice"], old_conv[-1]["agg_text"]
    print(agg_voice, agg_text)
    if agg_voice == "Aggressive" and agg_text == "Aggressive":
        return "Aggressive"
    elif agg_voice == "Non-Aggressive" and agg_text == "Non-aggressive":
        return "Non-Aggressive"
    else:
        return "Neutral"
    
def agent_name(sentiment,department):
    if sentiment == "Aggressive":
        skillLevel = 1
    elif sentiment == "Non-Aggressive":
        skillLevel = 3
    else:
        skillLevel = 2
    conn = sqlite3.connect('Database/AggroDetect.db')
    c = conn.cursor()
    c.execute('SELECT firstName,lastName,position FROM AgentDetails WHERE department = ? AND skillLevel = ?', (department, skillLevel))
    result = c.fetchone()
    conn.close()
    if result:
        firstName, lastName, position = result
        name = f"{firstName} {lastName}"
        print(name,position)
        return name, position
    else:
        return None, None

def save_analytics(sentiment):
    # Get date and time together
    now = datetime.datetime.now()
    # Get month only
    month = now.strftime("%B")
    # Get year only
    year = now.strftime("%Y")
    conn = sqlite3.connect('Database/AggroDetect.db')
    c = conn.cursor()
    c.execute('INSERT INTO Analytics (id, month, year, sentiment) VALUES (?,?,?,?)', (now, month, year, sentiment))
    conn.commit()
    conn.close()

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

@app.route('/end-conversation' , methods=['POST'])
def end_conversation():
    # clear all files in the uploads folder
    for file in os.listdir('uploads'):
        os.remove(os.path.join('uploads', file))
    # if old_conv is not empty return the overall sentiment, save analytics and save the conversation to the database
    if old_conv:
        # Overall sentiment of the conversation
        overall_sent = overall_sentiment()
        # Pass overall sentiment to the database
        save_analytics(overall_sent)
        # Save the conversation to the database
        firebase_datastore('', set_firebase_dictionary(), department=department)
        # Clear the conversation list
        old_conv.clear()
        return jsonify({'overall_sentiment': overall_sent})
    return jsonify({'overall_sentiment': ""})

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
    response, conversation = chat(transcript)

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

    if conversation == "end":
        first_time = True
        # Save the conversation to the database
        firebase_datastore('', set_firebase_dictionary(), department=department)
        # Overall sentiment of the conversation
        overall_sent = overall_sentiment()
        # Pass overall sentiment to the database
        save_analytics(overall_sent)
        # Save temporary conversation list
        temp_conv = old_conv.copy()
        # Clear the conversation list
        old_conv.clear()

        return jsonify({'transcript': temp_conv, 'audio_path': audio_path, 'dep':department, 'overall_sentiment': overall_sent, 'status': "end"})
    
    if conversation == "route":
        first_time = True
        # Overall sentiment of the conversation
        overall_sent = overall_sentiment()
        # Agent name
        agentName, position = agent_name(overall_sent,department)

        return jsonify({'transcript': old_conv, 'audio_path': audio_path, 'dep':department, 'overall_sentiment': overall_sent, 'agent_name':agentName, 'position':position, 'status': "route"})

    return jsonify({'transcript': old_conv, 'audio_path': audio_path, "dep":department})


@app.route('/chat_history')
def index():
    # Read data from Firebase
    users_data, _ = read_users_data_from_firebase()
    # Convert data to conversation format
    conversation_dict = convert_to_conversation_dict(users_data)
    # Pass conversation_dict to the HTML template
    return render_template('interface.html', conversation_dict = (conversation_dict),active_page='chat_history')

if __name__ == '__main__':
    app.run(debug=True)
