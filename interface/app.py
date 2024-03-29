from flask import Flask, render_template, request, redirect, url_for
import requests
from save_report import firebase_datastore
from model_pipeline import record_and_transcribe, agg_by_voice, agg_by_text, department_by_text
import subprocess
import time
import sqlite3

app = Flask(__name__)

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"  # Adjust the URL as needed
welcome_message_spoken = False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/sign-out')
def sign_out():
    return redirect(url_for('login_page'))


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

# rasa_shell_process = subprocess.Popen(["rasa", "run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# # Wait for the Rasa shell to start up
# time.sleep(45)


old_conv = {
    "user_messagee": [],
    "resp": []
}


# def add_welcome_message():
#     global welcome_message_spoken
#     message = "Thank you for calling us, How can I help you?"
#     if not welcome_message_spoken:
#         text_speech = pyttsx3.init()
#         text_speech.say(message)
#         text_speech.runAndWait()
#         old_conv['user_messagee'].append("_")
#         old_conv['resp'].append(message)
#         welcome_message_spoken = True


# @app.route('/', methods=['GET', 'POST'])
# def chat():
#     add_welcome_message()
#     audio, user_message = record_and_transcribe()
#     agg_voice = agg_by_voice(audio)
#     agg_text = agg_by_text(user_message)
#     dep_text = department_by_text(user_message)
#     print("User Message:", user_message, "\nEmotion audio:", agg_voice, "\nEmotion text:", agg_text, "\nDepartment:",
#           dep_text)
#     old_conv['user_message'].append((user_message, "(aggressive level by voice: non angry)", "(aggressive level by "
#                                                                                              "text:non angry)"))
#     rasa_response = send_message_to_rasa(user_message)

#     # Check if the response from Rasa is not empty and contains 'text'
#     if rasa_response and isinstance(rasa_response, list):
#         if 'custom' in rasa_response[0]:

#             bot_response = rasa_response[0]['custom']['text']

#             # Text-to-speech conversion using pyttsx3
#             text_speech = pyttsx3.init()
#             text_speech.say(bot_response)
#             text_speech.runAndWait()
#             print(bot_response)

#             # Append the bot's response to the conversation
#             old_conv['resp'].append(bot_response)

#             firebase_datastore('unknown', old_conv, department="department")  # put here department
#             # render_template('index.html', user_message=(user_message, "(aggressive level by voice: non angry)", "(aggressive level by text:non angry)"), bot_response=bot_response,
#             #                 old_conv=old_conv, size=len(old_conv["user_messagee"]))

#         else:
#             bot_response = rasa_response[0]['text']
#             # Text-to-speech conversion using pyttsx3
#             text_speech = pyttsx3.init()
#             text_speech.say(bot_response)
#             text_speech.runAndWait()
#             # Append the bot's response to the conversation
#             old_conv['resp'].append(bot_response)
#             # render_template('index.html', user_message=(user_message, "(aggressive level by voice: non angry)", "(aggressive level by text:non angry)"), bot_response=bot_response,
#             #                 old_conv=old_conv, size=len(old_conv["user_messagee"]))
#             print(bot_response)
#             chat()


#     else:
#         bot_response="sorry, I didn't get that. Can you please repeat?"
#         old_conv['resp'].append(bot_response)
#         text_speech = pyttsx3.init()
#         text_speech.say(bot_response)
#         text_speech.runAndWait()
#         # render_template('index.html', user_message=user_message, bot_response="No Response",
#         #                         old_conv=old_conv, size=len(old_conv["user_messagee"]))
#         print(bot_response)
#         chat()


# def send_message_to_rasa(message):
#     payload = {
#         "message": message,
#     }
#     response = requests.post(rasa_server_url, json=payload)
#     if response.status_code == 200:
#         predicted_intent = response.json()[0].get('metadeta', {}).get('response_name')
#         return response.json(), predicted_intent
#     else:
#         return {"error": "Failed to send message to Rasa."}


if __name__ == '__main__':
    app.run(debug=True)
