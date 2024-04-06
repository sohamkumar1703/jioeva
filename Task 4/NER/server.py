from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import spacy
import warnings

# Suppress the warning message
warnings.filterwarnings("ignore", category=UserWarning)


app = Flask(__name__)

# Load the pre-trained NER model
ner = spacy.load('/home/soham/Downloads/NER/file/content/model-best')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input sentence from the client
    sample_sentence = request.json['sentence']

    # Process the input sentence using the NER model
    doc = ner(sample_sentence)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Prepare the response
    response = []
    for entity, label in entities:
        response.append({'entity': entity, 'label': label})

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)