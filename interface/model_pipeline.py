import tensorflow as tf
import librosa
import numpy as np
from preprocessing import audio_feature_extraction
import speech_recognition as sr

def record_and_transcribe():
    # Create a recognizer object
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise before recording
        r.adjust_for_ambient_noise(source, duration=1)

        # Record audio
        audio = r.listen(source)

        print("Processing...")

    # Transcribe the recorded audio to text
    try:
        transcript = r.recognize_whisper_api(audio)
        return audio,transcript
    except sr.UnknownValueError:
        print("Unable to transcribe audio")
    except sr.RequestError as e:
        print(f"Error: {e}")

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
        return ['Aggressive' if prediction > threshold else 'Non-Aggressive'][0],len(predictions)
    else:
        if binary_predictions.count(1) > binary_predictions.count(0):
            prediction = "Aggressive"
        else:
            prediction = "Non-Aggressive"
        return prediction
