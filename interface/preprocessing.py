import librosa
import tensorflow as tf
import pickle
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('punkt')
nltk.download('stopwords')
import warnings
warnings.filterwarnings("ignore")

def audio_feature_extraction(segment, sr=22050):
    with open('..//Models//scaler_4(pro).pickle', 'rb') as f:
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

def dep_preprocess_text(text):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    text = re.sub(r'\d{10}', '', text)  # Remove contact numbers
    tokens = nltk.word_tokenize(text)  # Use NLTK tokenizer for better tokenization
    tokens = [word for word in tokens if len(word) > 2]  # Remove short words (length <= 2)
    tokens = [word.lower() for word in tokens if word.isalnum()]  # Tokenization, lowercase
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]  # Stemming, remove stopwords

    return ' '.join(tokens)

def agg_preprocess_text(text):
    stop_words = set(stopwords.words('english'))

    text = re.sub(r'\d{10}', '', text)  # Remove contact numbers
    text = re.sub(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', '', text)  # Remove dates
    tokens = text.split()
    tokens = [word for word in tokens if len(word) > 2]  # Remove short words (length <= 2)
    tokens = [word.lower() for word in tokens if word.isalnum()]  # Tokenization, lowercase
    tokens = [word for word in tokens if word not in stop_words] #removing stopwords

    return ' '.join(tokens)
