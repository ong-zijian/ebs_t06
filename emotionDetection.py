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
import json

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
        # Find all bookings with the given cid
        booking_cursor = bookings_collection.find({"cid": object_id})
        bookings_list = list(booking_cursor)

        if bookings_list:
            # Convert ObjectId and datetime to strings
            for booking in bookings_list:
                booking['_id'] = str(booking['_id'])
                booking['cid'] = str(booking['cid'])
                booking['sid'] = str(booking['sid'])
                # Convert datetime to ISO format string
                booking['sDateTime'] = booking['sDateTime'].isoformat()
                booking['eDateTime'] = booking['eDateTime'].isoformat()
            
            # Return the list of bookings
            return jsonify(bookings_list)
        else:
            return jsonify({"error": "No bookings found with that ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/bookingStudent/<object_id>', methods=['GET'])
def get_booking_by_sid(object_id):
    try:
        # Find all bookings with the given cid
        booking_cursor = bookings_collection.find({"sid": object_id})
        bookings_list = list(booking_cursor)

        if bookings_list:
            # Convert ObjectId and datetime to strings
            for booking in bookings_list:
                booking['_id'] = str(booking['_id'])
                booking['cid'] = str(booking['cid'])
                booking['sid'] = str(booking['sid'])
                # Convert datetime to ISO format string
                booking['sDateTime'] = booking['sDateTime'].isoformat()
                booking['eDateTime'] = booking['eDateTime'].isoformat()
            
            # Return the list of bookings
            return jsonify(bookings_list)
        else:
            return jsonify({"error": "No bookings found with that ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/booking', methods=['POST'])
def create_booking():
    try:
        data = request.json
        
        data['cid'] = str(data['cid'])
        data['sid'] = str(data['sid'])
        
        # Parse the ISO date strings to datetime objects
        data['sDateTime'] = datetime.fromisoformat(data['sDateTime'].rstrip('Z'))
        data['eDateTime'] = datetime.fromisoformat(data['eDateTime'].rstrip('Z'))

        # Insert
        booking_id = bookings_collection.insert_one(data).inserted_id

        return jsonify({"_id": str(booking_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/booking/<booking_id>', methods=['PUT'])
def update_booking(booking_id):
    try:
        data = request.json
        result = bookings_collection.update_one(
            {"_id": ObjectId(booking_id)}, 
            {"$set": data}
        )

        if result.matched_count:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Booking not found"}), 404
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
            return jsonify({})
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
