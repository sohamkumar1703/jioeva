import requests

def detect_singular_plural(sentence):
    url = "http://127.0.0.1:5000/detect_singular_plural"
    headers = {"Content-Type": "application/json"}
    data = {"sentence": sentence}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        singular_words = result.get("singular", [])
        plural_words = result.get("plural", [])

        print(f"Singular Words: {singular_words}")
        print(f"Plural Words: {plural_words}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    user_sentence = input("Enter a sentence: ")
    detect_singular_plural(user_sentence)