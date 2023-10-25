import nltk
nltk.download('vader_lexicon')

from flask import Flask, render_template, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_KEY")

sid = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    processed_tokens = [ps.stem(token) for token in tokens if token not in stop_words and token not in string.punctuation]
    processed_text = ' '.join(processed_tokens)
    return processed_text

def custom_chatbot_response(user_input):
    print(request.json)
    if "stress" in user_input.lower():
        return "Why are you stressed? Do you need help?"
    elif "suicidal" in user_input.lower() or "suicide" in user_input.lower():
        # Future implementation: notify counselors
        return ("If you are facing a mental health crisis, please call our Mental Health Helpline at 6389 2222 or "
                "seek medical help at our 24-hour Emergency Services located in our hospital. All counselors will be notified as well.")
    else:
        return None 
    
def get_response_from_gpt3(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/test', methods=['GET'])
def test():
    return "Hello World!"

@app.route('/mood', methods=['POST'])
def analyze_mood():
    if request.method == 'POST':
        request_data = request.get_json()
        user_text = request_data.get('mood', '')

        preprocessed_text = preprocess_text(user_text)
        sentiment_scores = sid.polarity_scores(preprocessed_text)

        overall_sentiment = ""
        if sentiment_scores['compound'] >= 0.05:
            overall_sentiment = "Positive"
        elif sentiment_scores['compound'] <= -0.1:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"

        response = {
            'processed_text': preprocessed_text,
            'sentiment_scores': sentiment_scores,
            'overall_sentiment': overall_sentiment
        }
        return jsonify(response)
    
@app.route('/chatbot', methods=['POST'])
def chat_endpoint():
    user_input = request.json.get('user_input')
    response = custom_chatbot_response(user_input)
    template_res = "The input is of a person dealing with some mental issues. Please respond in an appropriate manner:"

    if response is None:  # If custom responses didn't match, use GPT-3
        response = get_response_from_gpt3(template_res + user_input)

    print("Response to user:", response)  # Printing the response on server side

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
