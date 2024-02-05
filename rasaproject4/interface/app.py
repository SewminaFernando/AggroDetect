# 3rd code
# input:user massage()
from flask import Flask, render_template, request, jsonify
import requests
import pyttsx3


app = Flask(__name__)

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"  # Adjust the URL as needed
welcome_message_spoken = False

old_conv = {
        "user_messagee":[],
        "resp":[]
    }
def add_welcome_message():
    global welcome_message_spoken
    if not welcome_message_spoken:
        text_speech = pyttsx3.init()
        text_speech.say("Thank you for calling us, How can I help you?")
        text_speech.runAndWait()
        old_conv['user_messagee'].append("_")
        old_conv['resp'].append("Thank you for calling us, How can I help you?")
        welcome_message_spoken = True
        return "Thank you for calling us, How can I help you?"


@app.route('/', methods=['GET', 'POST'])
def chat():
    add_welcome_message()
    if request.method == 'POST':
        user_message = request.form['user_message']
        old_conv['user_messagee'].append(user_message)
        rasa_response = send_message_to_rasa(user_message)

        # Check if the response from Rasa is not empty and contains 'text'
        if rasa_response and isinstance(rasa_response, list) and rasa_response[0].get('text'):
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
        # Handle the case when the response is empty or does not contain 'text'
        return render_template('index.html', user_message=user_message,
                               bot_response="Error: Invalid response from Rasa", old_conv=old_conv,
                               size=len(old_conv["user_messagee"]))

    # Render the chat interface template for initial load
    return render_template('index.html')
def send_message_to_rasa(message):
    payload = {
        "message": message,
    }
    response = requests.post(rasa_server_url, json=payload)
    print('wada')
    if response.status_code == 200:
        print('wada')
        return response.json()
    else:
        return {"error": "Failed to send message to Rasa."}


if __name__ == '__main__':
    app.run(debug=True)

