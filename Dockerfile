FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
COPY ./emotionDetection.py .
EXPOSE 5000
CMD ["python", "emotionDetection.py"]
