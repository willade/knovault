from flask import Blueprint, request, jsonify
import requests

chatbot_bp = Blueprint('chatbot', __name__)



@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Message cannot be empty.'}), 400

    try:
         # Send the message to Rasa's REST API
        rasa_response = requests.post(
            'http://localhost:5005/webhooks/rest/webhook',
            json={"sender": "user", "message": user_message}
        )
        rasa_response.raise_for_status() 
        response_data = rasa_response.json()
        
        bot_reply = response_data[0].get("custom") or  {"text": response_data[0].get("text") or "Sorry, I didn't understand that."}
        print({'response': bot_reply})
        return jsonify({'response': bot_reply})
    except requests.exceptions.ConnectionError:  
        return jsonify({'response': 'Rasa server is not reachable. Please ensure it is running.'}), 503  
    except requests.exceptions.RequestException as e:
        return jsonify({'response': f'Error communicating with Rasa: {str(e)}'}), 500 
    


