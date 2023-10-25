service FlaskService {
    function test() returns String;

    entity SentimentResult {
        processed_text: String;
        compound: Double;
        neg: Double;
        neu: Double;
        pos: Double;
        overall_sentiment: String;
    }

    entity ChatbotResult {
        response: String;
    }

    function mood(mood: String) returns SentimentResult;
    function chatbot(user_input: String) returns ChatbotResult;
}
