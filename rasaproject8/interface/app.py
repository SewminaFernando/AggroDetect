# 3rd code
# input:user massage()
from flask import Flask, render_template, request
import requests
import pyttsx3
from save_report import firebase_datastore

app = Flask(__name__)

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"  # Adjust the URL as needed
welcome_message_spoken = False

# def conversation(user_messagee,resp):


old_conv = {
        "user_messagee":[],
        "resp":[]
    }

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


@app.route('/', methods=['GET', 'POST'])
def chat():
    add_welcome_message()

    if request.method == 'POST':
        user_message = request.form['user_message']
        old_conv['user_messagee'].append(user_message)
        # print("1")
        # print(old_conv)
        rasa_response = send_message_to_rasa(user_message)
        # Check if the response from Rasa is not empty and contains 'text'
        if rasa_response and isinstance(rasa_response, list):
            if 'custom' in rasa_response[0]:

                bot_response = rasa_response[0]['custom']['text']

                # Text-to-speech conversion using pyttsx3
                text_speech = pyttsx3.init()
                text_speech.say(bot_response)
                text_speech.runAndWait()

                # Append the bot's response to the conversation
                old_conv['resp'].append(bot_response)

                firebase_datastore('', old_conv, aggr_lvl="Not angry")

            else:
                bot_response = rasa_response[0]['text']
                # Text-to-speech conversion using pyttsx3
                text_speech = pyttsx3.init()
                text_speech.say(bot_response)
                text_speech.runAndWait()

                # Append the bot's response to the conversation
                old_conv['resp'].append(bot_response)

            return render_template('index.html', user_message=user_message, bot_response=bot_response,
                                   old_conv=old_conv, size=len(old_conv["user_messagee"]))
        else:

            old_conv['resp'].append("No Response")

            return render_template('index.html', user_message=user_message, bot_response="No Response",
                                   old_conv=old_conv, size=len(old_conv["user_messagee"]))

    # Render the chat interface template for initial load
    return render_template('index.html')
def send_message_to_rasa(message):
    # print("2")
    # print(old_conv)
    payload = {
        "message": message,
    }
    response = requests.post(rasa_server_url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to send message to Rasa."}
# def dict_to_pickle():
#     with open('interface\old_conv.pkl','wb') as data:
#         pickle.dump(old_conv, data)
#         return True

if __name__ == '__main__':
    app.run(debug=True)
