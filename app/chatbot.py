from flask import Blueprint, request, jsonify
# from app.models import Lesson
# from app import db
import requests

chatbot_bp = Blueprint('chatbot', __name__)


#user_states = {}

# @chatbot_bp.route('/chatbot', methods=['POST'])
# def chatbot_response():
#     user_message = request.json.get('message', '')
#     try:
#         rasa_response = requests.post(
#             'http://localhost:5005/webhooks/rest/webhook',  # Rasa API endpoint
#             json={"sender": "user", "message": user_message}
#         )
#         response_data = rasa_response.json()

#         if not response_data:
#             return jsonify({'response': "I'm sorry, I didn't understand that."})

#         bot_reply = response_data[0].get('text', "I'm sorry, I didn't understand that.")
#         custom_action = response_data[0].get('custom', {})
#         return jsonify({'response': bot_reply, **custom_action})

#     except Exception as e:
#         print(f"Error: {e}")  # Log error for debugging
#         return jsonify({'response': "Sorry, something went wrongnow."}), 500


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
        rasa_response.raise_for_status() #remove later
        response_data = rasa_response.json()
        bot_reply = response_data[0]['text'] if response_data else "Sorry, I didn't understand that."
        return jsonify({'response': bot_reply})
    except requests.exceptions.ConnectionError:  #remove later
        return jsonify({'response': 'Rasa server is not reachable. Please ensure it is running.'}), 503  #remove later
    except requests.exceptions.RequestException as e:
        return jsonify({'response': f'Error communicating with Rasa: {str(e)}'}), 500 #change later
    
# # Assign the alias
# chatbot_logic = handle_user_input

