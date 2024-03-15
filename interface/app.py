from flask import Flask, render_template, request
import requests
import pyttsx3
from save_report import firebase_datastore
from model_pipeline import record_and_transcribe, agg_by_voice, agg_by_text, department_by_text
import subprocess
import time

app = Flask(__name__)

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"  # Adjust the URL as needed
welcome_message_spoken = False



old_conv = {
        "user_messagee":[],
        "resp":[]
    }

def run_commands(commands):
    processes = []
    
    # Start each command in a separate process
    for cmd in commands:
        processes.append(subprocess.Popen(cmd, shell=True))

    # Wait for all processes to finish
    for process in processes:
        process.wait()

def add_welcome_message():
    global welcome_message_spoken
    message = "Thank you for calling us, How can I help you?"
    if not welcome_message_spoken:
        text_speech = pyttsx3.init()
        text_speech.say(message)
        text_speech.runAndWait()
        old_conv['user_messagee'].append("_")
        old_conv['resp'].append(message)
        welcome_message_spoken = True


# @app.route('/', methods=['GET', 'POST'])
def chat():
    add_welcome_message()
    # user_message = "hello" 
    audio, user_message = record_and_transcribe()
    agg_voice = agg_by_voice(audio)
    agg_text = agg_by_text(user_message)
    dep_text = department_by_text(user_message)
    print("User Message:",user_message,"\nEmotion audio:",agg_voice,"\nEmotion text:",agg_text,"\nDepartment:",dep_text)
    # old_conv['user_messagee'].append(user_message)
    rasa_response = send_message_to_rasa(user_message)
    # Check if the response from Rasa is not empty and contains 'text'
    if rasa_response and isinstance(rasa_response, list):
        if 'custom' in rasa_response[0]:

            bot_response = rasa_response[0]['custom']['text']

            # Text-to-speech conversion using pyttsx3
            text_speech = pyttsx3.init()
            text_speech.say(bot_response)
            text_speech.runAndWait()

            print(bot_response)

            # Append the bot's response to the conversation
            # old_conv['resp'].append(bot_response)

            # firebase_datastore('', old_conv, aggr_lvl="Not angry")
            # render_template('index.html', user_message=user_message, bot_response=bot_response,
            #                     old_conv=old_conv, size=len(old_conv["user_messagee"]))

        else:
            bot_response = rasa_response[0]['text']
            # Text-to-speech conversion using pyttsx3
            text_speech = pyttsx3.init()
            text_speech.say(bot_response)
            text_speech.runAndWait()
            # Append the bot's response to the conversation
            # old_conv['resp'].append(bot_response)
            # render_template('index.html', user_message=user_message, bot_response=bot_response,
            #                     old_conv=old_conv, size=len(old_conv["user_messagee"]))
            print(bot_response)
            chat()

        
    else:
        bot_response="sorry, I didn't get that. Can you please repeat?"
        # old_conv['resp'].append(bot_response)
        text_speech = pyttsx3.init()
        text_speech.say(bot_response)
        text_speech.runAndWait()
        # render_template('index.html', user_message=user_message, bot_response="No Response",
        #                         old_conv=old_conv, size=len(old_conv["user_messagee"]))
        print(bot_response)
        chat()
    
    
    # if request.method == 'POST':
        # user_message = record_and_transcribe()[1]
        # old_conv['user_messagee'].append(user_message)
        # rasa_response = send_message_to_rasa(user_message)
        # # Check if the response from Rasa is not empty and contains 'text'
        # if rasa_response and isinstance(rasa_response, list):
        #     if 'custom' in rasa_response[0]:

        #         bot_response = rasa_response[0]['custom']['text']

        #         # Text-to-speech conversion using pyttsx3
        #         text_speech = pyttsx3.init()
        #         text_speech.say(bot_response)
        #         text_speech.runAndWait()

        #         # Append the bot's response to the conversation
        #         old_conv['resp'].append(bot_response)

        #         firebase_datastore('', old_conv, aggr_lvl="Not angry")

        #     else:
        #         bot_response = rasa_response[0]['text']
        #         # Text-to-speech conversion using pyttsx3
        #         text_speech = pyttsx3.init()
        #         text_speech.say(bot_response)
        #         text_speech.runAndWait()

        #         # Append the bot's response to the conversation
        #         old_conv['resp'].append(bot_response)

        #     return render_template('index.html', user_message=user_message, bot_response=bot_response,
        #                            old_conv=old_conv, size=len(old_conv["user_messagee"]))
        # else:

        #     old_conv['resp'].append("No Response")

        #     return render_template('index.html', user_message=user_message, bot_response="No Response",
        #                            old_conv=old_conv, size=len(old_conv["user_messagee"]))

    # Render the chat interface template for initial load
    # return render_template('index.html')

def send_message_to_rasa(message):
    payload = {
        "message": message,
    }
    response = requests.post(rasa_server_url, json=payload)
    if response.status_code == 200:
        # predicted_intent = response.json()[0].get('metadeta', {}).get('response_name')
        return response.json()
    else:
        return {"error": "Failed to send message to Rasa."}

if __name__ == '__main__':
    # app.run(debug=True)

    # Commands to run
    # commands = ["rasa shell", "rasa run actions"]

    # Run the commands
    # run_commands(commands)
    chat()