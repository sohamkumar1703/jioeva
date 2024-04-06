import requests
import json

# Get user input
user_input = input("Enter a sentence: ")

# Define the input data
input_data = {
    'sentence': user_input
}

# Send the POST request to the Flask API
response = requests.post('http://localhost:5000/predict', json=input_data)

# Print the response
print(json.dumps(response.json(), indent=2))