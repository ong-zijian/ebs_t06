from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from Flask!"

@app.route('/CreateJournal')
def next_page():
    # You can serve a SPA HTML or a template here
    return "Hello from Flask!"

if __name__ == '__main__':
    app.run(debug=True)
