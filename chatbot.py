import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {
    "Authorization": f"Bearer {os.getenv('my_api_key')}"
}

system_prompt = (
    "You are a friendly and careful medical assistant. "
    "Answer general health-related questions clearly. "
    "Do not give medical advice for serious issues. Always suggest visiting a doctor if needed."
)

unsafe_keywords = ["cure", "overdose", "suicide", "kill", "prescription", "dosage"]

def is_safe(user_input):
    return not any(word in user_input.lower() for word in unsafe_keywords)

def ask_question(user_input):
    if not is_safe(user_input):
        return " This question may require professional help. Please consult a doctor."

    prompt = f"{system_prompt}\nUser: {user_input}\nAssistant:"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150}}

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        result = response.json()
        return result[0]["generated_text"].split("Assistant:")[-1].strip()
    except Exception as e:
        print("DEBUG:", response.text)
        return " Sorry, couldn't fetch a valid response."

if __name__ == "__main__":
    print(" Ask a health question (type 'exit' to quit):\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Bot:", ask_question(user_input), "\n")
