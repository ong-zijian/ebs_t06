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

def handle_sensitive_topics(user_input):
    # Define sensitive keywords and custom responses
    sensitive_keywords = {
    ('suicide', 'suicidal', 'end my life'): "I'm truly concerned to hear that you're feeling this way and it's really important that we find you some help. You're not alone in this, and there are people who want to support you through these tough times. It's crucial that you talk to a mental health professional as soon as possible. They can offer the support and guidance you need to get through this. Please, let's find someone who can help.",

    ('depress', 'depression', 'hopeless'): "I hear that you're feeling depressed, and I want you to know that your feelings are valid. Depression can be incredibly challenging, but there are many people who have walked this path and found their way through. Talking to a mental health professional can be very helpful. They can provide support and strategies to cope with what you're feeling. Remember, you are not alone in this.",

    ('anxious', 'anxiety', 'nervous'): "It sounds like you're dealing with a lot of anxiety. It’s okay to feel this way, and it's a good step to acknowledge these feelings. Anxiety can be overwhelming, but there are ways to manage it. Consider speaking with a mental health professional who can provide you with support and techniques to help you cope. Simple practices like deep breathing or mindfulness can make a difference.",

    ('abuse', 'abused', 'violence'): "I'm very sorry to hear that you might be experiencing abuse. It's important to know that you deserve to be treated with respect and to feel safe. Please consider reaching out to a trusted friend, family member, or a professional for support. There are also organizations and helplines that can provide guidance and assistance.",

    ('grieving', 'grief', 'loss'): "I'm so sorry for your loss. Grief is a deeply personal experience, and it's okay to feel a range of emotions. It can be helpful to talk about your feelings with someone you trust, whether it's a friend, family member, or a mental health professional. Remember, grieving is a process, and it's okay to take it at your own pace.",

    ('stress', 'stressed', 'overwhelmed'): "I'm really sorry to hear that you're feeling stressed. It's completely okay to feel this way, especially with how demanding life can be. Remember, it's important to take care of yourself. Taking short breaks, engaging in activities you enjoy, and maybe even talking to someone you trust can help immensely. Your feelings are valid, and taking steps to manage your stress is a sign of strength.",

    ('panic', 'panic attack', 'panicking'): "Experiencing a panic attack can be really frightening, but remember that it will pass. Try to focus on your breathing – slow, deep breaths. It's also important to talk to a healthcare provider about these experiences. They can offer strategies to manage panic attacks and help you understand what triggers them.",

    ('self-harm', 'hurting myself', 'self injury'): "It sounds like you're going through a very difficult time and might be considering harming yourself. It's important to talk to someone who can help, like a mental health professional. You're not alone, and there are people who want to support you. Your life is valuable, and there is help available to get through this.",

    ('substance abuse', 'addiction', 'drug use'): "Dealing with substance abuse can be incredibly challenging, and I want you to know that it's okay to seek help. There are professionals who specialize in helping people through addiction, and talking to them can be a great first step. Remember, taking the step to ask for help is a sign of strength and the first step towards recovery.",

    ('lonely', 'loneliness', 'isolated'): "Feeling lonely can be really tough, and it's okay to feel this way sometimes. But remember, you're not alone in feeling lonely. Reaching out to friends, family, or community groups can help. Also, consider talking to a mental health professional who can provide support and help you navigate these feelings.",

    }


    print(f"Checking for sensitive topics in user input: {user_input}")
    # Check if any sensitive keyword is in the user input
    user_input_lower = user_input.lower()
    for keywords_tuple, response in sensitive_keywords.items():
        if any(keyword in user_input_lower for keyword in keywords_tuple):
            return response
    return None

    return None
    
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
    print(f"Received user input: {user_input}")
    sensitive_response = handle_sensitive_topics(user_input)
    
    
    if sensitive_response:
        append_to_chat_history(user_id, {"user": user_input, "bot": sensitive_response})
        return sensitive_response
    
    chat_history = get_chat_history(user_id)
    
    prompt_with_context = create_prompt_with_context(chat_history, user_input)
    
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt_with_context,
            max_tokens=150,
            temperature=0.3,
            top_p=1,
            frequency_penalty=0.3,
            presence_penalty=0.3,
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
