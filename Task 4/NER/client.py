import requests
import json

def main():
    # Sample sentence
    sample_sentence = input("Enter a sentence:")

    # Send the request to the Flask API
    response = requests.post('http://localhost:5000/predict', json={'sentence': sample_sentence})

    # Print the response
    print("Predicted entities:")
    for item in response.json():
        print(f"{item['entity']}: {item['label']}")

if __name__ == '__main__':
    main()