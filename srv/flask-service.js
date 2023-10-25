const axios = require('axios');
const FLASK_ENDPOINT = "http://ebst06-api-service-test.smu-team06.svc.cluster.local:4004";

module.exports = (srv) => {

    srv.on('test', async () => {
        try {
            const response = await axios.get(`${FLASK_ENDPOINT}/test`);
            return response.data;
        } catch (error) {
            console.error("Error calling Flask service for test:", error);
            throw new Error("Failed to fetch test. Please try again later.");
        }
    });

    srv.on('mood', async (req) => {
        try {
            const response = await axios.post(`${FLASK_ENDPOINT}/mood`, {
                mood: req.data.mood
            });
            return response.data;
        } catch (error) {
            console.error("Error calling Flask service for mood:", error);
            throw new Error("Failed to analyze mood. Please try again later.");
        }
    });

    srv.on('chatbot', async (req) => {
        try {
            const response = await axios.post(`${FLASK_ENDPOINT}/chatbot`, {
                user_input: req.data.user_input
            });
            return {
                response: response.data.response
            };
        } catch (error) {
            console.error("Error calling Flask service for chatbot:", error);
            throw new Error("Failed to get chatbot response. Please try again later.");
        }
    });
};
