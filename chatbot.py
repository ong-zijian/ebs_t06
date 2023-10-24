from flask import Flask, request, jsonify
import openai
import os

# API-KEY
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

def custom_chatbot_response(user_input):
    print(request.json)
    if "stress" in user_input.lower():
        return "Why are you stressed? Do you need help?"
    elif "suicidal" in user_input.lower() or "suicide" in user_input.lower():
        # Future implementation: notify counselors
        return ("If you are facing a mental health crisis, please call our Mental Health Helpline at 6389 2222 or "
                "seek medical help at our 24-hour Emergency Services located in our hospital. All counselors will be notified as well.")
    else:
        return None  # Let the main function decide to use GPT-3

def get_response_from_gpt3(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/chatbot', methods=['POST'])
def chat_endpoint():
    user_input = request.json.get('user_input')
    response = custom_chatbot_response(user_input)

    if response is None:  # If custom responses didn't match, use GPT-3
        response = get_response_from_gpt3(user_input)

    print("Response to user:", response)  # Printing the response on server side

    return jsonify({'response': response})

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=5000)
