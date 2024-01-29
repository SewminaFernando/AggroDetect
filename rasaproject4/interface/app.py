# 3rd code
# input:user massage()
from flask import Flask, render_template, request, jsonify
import requests
import pyttsx3


app = Flask(__name__)

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"  # Adjust the URL as needed



# answer=input("bot_reply")
# text_speech.say(answer)
# text_speech.runAndWait()

old_conv = {
        "user_messagee":[],
        "resp":[]
    }

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form['user_message']
        old_conv['user_messagee'].append(user_message)
        rasa_response = send_message_to_rasa(user_message)
        old_conv['resp'].append(rasa_response[0]['text'])
        if 'error' in rasa_response:
            return "Error: " + rasa_response['error']
        else:
            bot_response = rasa_response[0]['text']
            text_speech = pyttsx3.init()

            text_speech.say(bot_response)
            text_speech.runAndWait()
            return render_template('index.html', user_message=user_message, bot_response=bot_response, old_conv=old_conv, size=len(old_conv["user_messagee"]))
    return render_template('index.html')


@app.route('/user_message', methods=['POST'])
def user_message():
    # Retrieve the user's message from the POST request
    user_input = request.form.get('user_input')

    # Send the user's message to the Rasa server
    response = requests.post(rasa_server_url, json={"message": user_input})

    # Get the response from the Rasa server
    rasa_response = response.json()
    bot_reply = rasa_response[0]['text']

    # Return the bot's reply
    return jsonify({"bot_reply": bot_reply})


def send_message_to_rasa(message):
    payload = {
        "message": message,
    }
    response = requests.post(rasa_server_url, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to send message to Rasa."}


if __name__ == '__main__':
    app.run(debug=True)

