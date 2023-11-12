from flask import Flask, request, jsonify
import openai
import os

# Set your OpenAI API key in an environment variable for security reasons
openai.api_key = os.environ.get("OPENAI_KEY")

app = Flask(__name__)

# This will store the conversation history for each user in memory
# Added a dummy user with user_id 'dummy_user' for testing
chat_histories = {
    'dummy_user': [
        {"user": "Hello, how are you?", "bot": "I'm fine, thank you for asking! How can I assist you today?"}
    ]
}

def append_to_chat_history(user_id, exchange):
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    chat_histories[user_id].append(exchange)

def get_chat_history(user_id):
    return chat_histories.get(user_id, [])

def create_prompt_with_context(chat_history, new_user_input):
    prompt = f"User: {new_user_input}\nBot:"
    for exchange in reversed(chat_history[-5:]):  # Adjust the slice to control context size
        prompt = f"User: {exchange['user']}\nBot: {exchange['bot']}\n" + prompt
    return prompt

def get_response_from_gpt3(user_id, user_input):
    chat_history = get_chat_history(user_id)
    prompt_with_context = create_prompt_with_context(chat_history, user_input)
    
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt_with_context,
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            stop=["\n"],  # Stop the response after one completion
        )
        gpt_response = response.choices[0].text.strip()

        # Post-process the response to prevent repetitive answers
        if gpt_response.lower() in ["i'm sorry to hear that.", "i'm sorry to hear that"]:
            # Provide a more helpful follow-up or ask for more information
            gpt_response = "I'm here for you. What's been on your mind lately?"

        append_to_chat_history(user_id, {"user": user_input, "bot": gpt_response})
        return gpt_response
    except Exception as e:
        print(f"Error during GPT-3 response generation: {e}")
        return "I'm not sure how to respond to that. Can you rephrase?"

@app.route('/chatbot', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    # Default to using the dummy user if no user_id is provided
    user_id = data.get('user_id', 'dummy_user')
    user_input = data.get('user_input')

    if not user_input:
        return jsonify({'response': "User input is required."}), 400

    try:
        response = get_response_from_gpt3(user_id, user_input)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'response': "I'm experiencing difficulties. Please try again later."}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=False)  # Set debug to False for production
