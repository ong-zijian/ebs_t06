# Existing ZJ's dockerfile
# FROM python:3-slim
# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN python -m pip install --no-cache-dir -r requirements.txt
# RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
# COPY ./emotionDetection.py .
# EXPOSE 5000
# CMD ["python", "emotionDetection.py"]

# Combined dockerfile
FROM python:3-slim

WORKDIR /usr/src/app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# Download necessary NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copy both Python files to the working directory
COPY ./emotionDetection.py .
COPY ./chatbot.py .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app for chatbot.py by default
CMD ["python", "chatbot.py"]
