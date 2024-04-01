import tensorflow as tf
import librosa
import numpy as np
from preprocessing import audio_feature_extraction, dep_preprocess_text, agg_preprocess_text
import speech_recognition as sr
import pickle
import os
from pydub import AudioSegment
import pyttsx3
import noisereduce as nr
import soundfile as sf
import requests
from openai import OpenAI
import warnings
warnings.filterwarnings("ignore")

count = 0
rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"

def agg_by_voice(wav_file, threshold=0.737163):
    model = tf.keras.models.load_model('..//Models//agg_cnn_model.h5')

    # Load audio file using librosa
    signal,sr = librosa.load(wav_file, offset=0.5, res_type='kaiser_fast', sr=22050)

    # Calculate the duration in samples for 3 seconds
    segment_length_samples = sr * 3

    predictions = []

    # Iterate over the audio signal with a step of 3 seconds
    for i in range(0, len(signal), segment_length_samples):
        # Slice the audio
        segment = signal[i:i + segment_length_samples]

        features = audio_feature_extraction(segment, sr=22050)

        # Predict the emotion
        predictions.append(model.predict(features)[0][0])

    binary_predictions = [1 if prediction > threshold else 0 for prediction in predictions]

    if binary_predictions.count(1) == binary_predictions.count(0):
        prediction = np.mean(predictions)
        return ['Aggressive' if prediction > threshold else 'Non-Aggressive'][0]
    else:
        if binary_predictions.count(1) > binary_predictions.count(0):
            prediction = "Aggressive"
        else:
            prediction = "Non-Aggressive"
        return prediction
    

def agg_by_text(text):
    p_text = agg_preprocess_text(text)

    # Load the model
    with open('..//Models//agg_RF_model.pickle', 'rb') as f:
        model = pickle.load(f)
    # Load the vectorizer
    with open('..//Models//agg_vectorizer.pickle', 'rb') as f:
        vectorizer = pickle.load(f)
    # Vectorize the text
    v_text = vectorizer.transform([p_text]).toarray()
    # Predict the emotion
    prediction = model.predict(v_text)
    return prediction[0]

def department_by_text(text):
    p_text = dep_preprocess_text(text)

    # Load the model
    with open('..//Models//dep_rf_model.pickle', 'rb') as f:
        model = pickle.load(f)
    # Load the vectorizer
    with open('..//Models//dep_vectorizer.pickle', 'rb') as f:
        vectorizer = pickle.load(f)
    # Vectorize the text
    v_text = vectorizer.transform([p_text]).toarray()
    # Predict the emotion
    prediction = model.predict(v_text)
    return prediction[0]

# Writting a function to noice reduction
def apply_noise_reduction(input_path, output_path):
    # Load the audio file
    audio, _ = librosa.load(input_path, sr=22050)

    # Perform noise reduction
    reduced_audio = nr.reduce_noise(audio, sr=22050)

    # Save the denoised audio
    sf.write(output_path, reduced_audio,22050)

def convert_webm_to_wav(input_file):

    audio = AudioSegment.from_file(input_file, format="webm")
    audio.export("uploads\\audio.wav", format="wav")
    # Noice reduction
    apply_noise_reduction("uploads\\audio.wav", "uploads\\n_audio.wav")


def transcribe_audio(audio_file):
    # Convert webm to wav
    convert_webm_to_wav(audio_file)
    # Initialize recognizer
    recog = sr.Recognizer()

    try:
        # Use OpenAI client if API key is working
        # Define the OpenAI client
        client = OpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY"),
                    organization=os.environ.get("WHISPER_ORG")
                )

        audio = open("uploads\\recorded_audio.webm", "rb")

        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file = audio,
            language="en",
            response_format="text")
        
    except Exception as e:
        # Load audio file
        with sr.AudioFile("uploads\\n_audio.wav") as source:
            audio = recog.record(source)
        # Use default speech recognition if API key is not working
        transcript = recog.recognize_whisper(audio)

    return transcript

def text_to_speech(text):
    global count
    engine = pyttsx3.init()
    # speed
    engine.setProperty('rate', 150)
    # set directory
    directory = 'uploads\\output'+str(count)+'.mp3'
    # save to file
    engine.save_to_file(text, directory)
    engine.runAndWait()

    if count >= 1:
        os.remove('uploads\\output'+str(count-1)+'.mp3')

    count += 1

    return directory

def chat(user_message):
    rasa_response = send_message_to_rasa(user_message)
    # Check if the response from Rasa is not empty and contains 'text'
    if rasa_response and isinstance(rasa_response, list):
        if 'custom' in rasa_response[0]:
            bot_response = rasa_response[0]['custom']['text']

            return bot_response

        else:
            bot_response = rasa_response[0]['text']

            return bot_response
        
    else:
        bot_response="sorry, I didn't get that. Can you please repeat?"

        return bot_response
    

def send_message_to_rasa(message):
    payload = {
        "message": message,
    }
    response = requests.post(rasa_server_url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to send message to Rasa."}