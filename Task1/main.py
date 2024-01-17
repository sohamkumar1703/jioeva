import spacy
from flask import Flask, request, jsonify

app = Flask(__name__)


def detect_singular_plural(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    singular_words = [token.text for token in doc if token.tag_ == "NN"]
    plural_words = [token.text for token in doc if token.tag_ == "NNS"]

    return singular_words, plural_words


    return singular_words, plural_words

@app.route('/detect_singular_plural', methods=['POST'])
def api_detect_singular_plural():
    data = request.get_json()
    sentence = data.get('sentence', '')

    singular, plural = detect_singular_plural(sentence)
    return jsonify({"singular": singular,"plural": plural})

if __name__ == '__main__':
    app.run(debug=True)
