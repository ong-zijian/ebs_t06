import nltk
nltk.download('vader_lexicon')

from flask import Flask, render_template, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

app = Flask(__name__)

sid = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    processed_tokens = [ps.stem(token) for token in tokens if token not in stop_words and token not in string.punctuation]
    processed_text = ' '.join(processed_tokens)
    return processed_text

@app.route('/', methods=['GET'])
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
