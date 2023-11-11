from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello from Flask!"

@app.route('/CreateJournal')
def next_page():
    # You can serve a SPA HTML or a template here
    return "Hello from Flask!"

# app.py

from flask import Flask, jsonify, abort

app = Flask(__name__)

counselors = [
    {
        'id': 1,
        'name': 'Ada Johnson',
        'photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwVRR689h-rJJsTMJbY7w4zLP30xxYflNRy6HM164ZjtcJHhgL8su7kCJgBLqdJOx_2D4&usqp=CAU',
        'description': 'Specializing in youth and family counseling, Ada brings over 20 years of compassionate experience to her practice.',
        'rating': 4.5
    },
    {
        'id': 2,
        'name': 'Steven Miller',
        'photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwQQTS4NPqnCGbJPd4x7O_YJNOJ5gH6KkejH3nhVfIhxwwJPHEotjPs0VCpGg-UcybvxM&usqp=CAU',
        'description': 'With a focus on community well-being, Steven aids diverse groups in overcoming a myriad of challenges.',
        'rating': 4.7
    },
    {
        'id': 3,
        'name': 'Jenny Smith',
        'photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfbspSuAlbAFC2RqZweFBTjOF4cWY9gizRbQKEzzLE0QdxIKrV5E-iZipiZxcdYyB7aTU&usqp=CAU',
        'description': 'Jenny has dedicated more than a decade to social services, empowering her clients to reach personal milestones.',
        'rating': 5
    },
    # ... other counselors ...
]

# Convert the list to a dictionary for easier access by ID
counselors_dict = {counselor['id']: counselor for counselor in counselors}

@app.route('/api/counselors', methods=['GET'])
@cross_origin()
def get_counselors():
    # Return the list of counselors
    return jsonify(counselors)

@app.route('/api/counselor/<int:counselor_id>', methods=['GET'])
@cross_origin()
def get_counselor(counselor_id):
    # Access the counselor by ID from the dictionary
    counselor = counselors_dict.get(counselor_id)
    if counselor:
        return jsonify(counselor)
    else:
        abort(404, description="Resource not found")

if __name__ == '__main__':
    app.run(debug=True)