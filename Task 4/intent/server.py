import logging
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Dropout, Embedding, GRU, Bidirectional, LSTM
from tensorflow.keras import Sequential
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Define a Pydantic model for the input data
class InputData:
    def __init__(self, sentence: str):
        self.sentence = sentence

# Load the model and other required resources
stem = PorterStemmer()
lem = WordNetLemmatizer()
stop = stopwords.words('english')
data1 = pd.read_csv('/home/soham/Downloads/intent/preprocessed_train_data2.csv')
data2 = pd.read_csv('/home/soham/Downloads/intent/preprocessed_test_data2.csv')
X_1 = data1["comment_text"]
X_2 = data2["comment_text"]
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_1)
tokenizer.fit_on_texts(X_2)

#Define the model
MAX_FEATURES = max(tokenizer.word_index.values())
model = Sequential()
model.add(Embedding(MAX_FEATURES + 1, 50, input_shape = (100, )))
model.add(Bidirectional(LSTM(50, dropout=0.1)))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(6, activation = 'sigmoid'))
model.load_weights('/home/soham/Downloads/intent/intent_model_weights3.h5')

# Define a function to preprocess the input sentence
def preprocess_sentence(text):
    def stem_lem(text):
        lemmatized = []
        for word in text:
            if len(word) < 990:
                stem.stem(word)
                lemmatized.append(lem.lemmatize(word))
        return lemmatized

    text = text.lower()
    text = word_tokenize(text)
    text = [word for word in text if word not in stop]
    text = stem_lem(text)
    return text

# Define the API endpoint
@app.route('/predict', methods=['POST'])
def predict():
    input_data = InputData(request.get_json()['sentence'])
    preprocessed_sentence = preprocess_sentence(input_data.sentence)
    sequence = tokenizer.texts_to_sequences([preprocessed_sentence])
    padded_sequence = pad_sequences(sequence, maxlen=100)
    prediction = model.predict(padded_sequence)
    logits = prediction[0].tolist()
    toxic, severe_toxic, obscene, threat, insult, identity_hate = logits
    output = {
        'toxic': toxic,
        'severe_toxic': severe_toxic,
        'obscene': obscene,
        'threat': threat,
        'insult': insult,
        'identity_hate': identity_hate
    }
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)