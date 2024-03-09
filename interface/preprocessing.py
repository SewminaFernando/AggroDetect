import librosa
import tensorflow as tf
import pickle
import numpy as np

def audio_feature_extraction(segment, sr=22050):
    with open('Models//scaler_4(pro).pickle', 'rb') as f:
        sc = pickle.load(f)

    features = []
    mfccs = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=13, n_fft=2048, hop_length=512)
    features.extend(np.mean(mfccs.T, axis=0))
    features.append(np.sum(np.abs(segment)**2))
    features.append(librosa.feature.rms(y=segment)[0].mean())
    features.append(np.max(np.abs(segment)))
    features.append(librosa.beat.beat_track(y=segment, sr=22050)[0])

    features = np.array(features)
    # Scale data
    features = sc.transform(features.reshape(1,-1))
    features = np.expand_dims(features, axis=2)

    return features