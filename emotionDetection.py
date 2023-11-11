import nltk
nltk.download('vader_lexicon')

from flask import Flask, render_template, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime

import string
import openai
import os

app = Flask(__name__)

# API keys
openai.api_key = os.environ.get("OPENAI_KEY")
mongo_uri = os.environ.get("MONGO_URI")

# MongoDB connection
client = MongoClient(mongo_uri)
db = client['EBS']

# List of collection
students_collection = db['student']
counsellors_collection = db['counsellor']
bookings_collection = db['booking']
emotion_collection = db['emotion']

# Sentiment analysis classes
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


########################################################################################################################
## Student Collection
@app.route('/students', methods=['GET'])
def get_all_students():
    students = list(students_collection.find({}))
    for student in students:
        student['_id'] = str(student['_id'])
    return jsonify(students)

@app.route('/student/<object_id>', methods=['GET'])
def get_student_by_id(object_id):
    try:
        student = students_collection.find_one({"_id": ObjectId(object_id)})
        if student:
            student['_id'] = str(student['_id'])
            return jsonify(student)
        else:
            return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/student', methods=['POST'])
def create_student():
    try:
        data = request.json
        student_id = students_collection.insert_one(data).inserted_id
        return jsonify({"_id": str(student_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
########################################################################################################################
## Counsellor Collection
@app.route('/counsellors', methods=['GET'])
def get_all_counsellor():
    counsellors = list(counsellors_collection.find({}))
    for counsellor in counsellors:
        counsellor['_id'] = str(counsellor['_id'])
    return jsonify(counsellors)

@app.route('/counsellor/<object_id>', methods=['GET'])
def get_counsellor_by_id(object_id):
    try:
        counsellor = counsellors_collection.find_one({"_id": ObjectId(object_id)})
        if counsellor:
            counsellor['_id'] = str(counsellor['_id'])
            return jsonify(counsellor)
        else:
            return jsonify({"error": "Counsellor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/counsellor', methods=['POST'])
def create_counsellor():
    try:
        data = request.json
        counsellor_id = counsellors_collection.insert_one(data).inserted_id
        return jsonify({"_id": str(counsellor_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

########################################################################################################################
## Booking Collection
@app.route('/bookings', methods=['GET'])
def get_all_bookings():
    bookings = list(bookings_collection.find({}))
    for booking in bookings:
        booking['_id'] = str(booking['_id'])
        booking['cid'] = str(booking['cid'])
        booking['sid'] = str(booking['sid'])
    return jsonify(bookings)

@app.route('/booking/<object_id>', methods=['GET'])
def get_booking_by_id(object_id):
    try:
        booking = bookings_collection.find_one({"cid": object_id})
        if booking:
            booking['_id'] = str(booking['_id'])
            booking['cid'] = str(booking['cid'])
            booking['sid'] = str(booking['sid'])
            return jsonify(booking)
        else:
            return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/booking', methods=['POST'])
def create_booking():
    try:
        data = request.json
        booking_id = bookings_collection.insert_one(data).inserted_id
        return jsonify({"_id": str(booking_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


########################################################################################################################
## Emotion Collection
@app.route('/emotion/<object_id>', methods=['GET'])
def get_emotion_by_id(object_id):
    try:
        emotion = emotion_collection.find_one({"sid": ObjectId(object_id)})
        if emotion:
            emotion['_id'] = str(emotion['_id'])
            emotion['sid'] = str(emotion['sid'])
            return jsonify(emotion)
        else:
            return jsonify({"error": "Emotion not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/emotion/add', methods=['POST'])
def add_emotion_journal_entry():
    try:
        request_data = request.get_json()
        object_id = request_data.get('object_id')
        title = request_data.get('title')
        description = request_data.get('description')

        # Preprocess and analyze the sentiment of the description
        preprocessed_text = preprocess_text(description)
        sentiment_scores = sid.polarity_scores(preprocessed_text)
        compound_score = sentiment_scores['compound']

        # Prepare the journal entry
        current_date = datetime.now().date().isoformat()
        score_entry = {
            "date": current_date,
            "score": compound_score
        }
        journal_entry = {
            "title": title,
            "description": description,
            "date": current_date
        }

        # Updating the MongoDB document using $push
        result = emotion_collection.update_one(
            {"sid": ObjectId(object_id)},
            {
                "$push": {
                    "journal": journal_entry,
                    "score": score_entry
                }
            }
        )

        # Checking if any document got updated
        if result.modified_count > 0:
            return jsonify({"message": "Journal entry added successfully"}), 200
        else:
            return jsonify({"error": "No matching document found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
