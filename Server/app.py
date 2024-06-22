import sys
import os
import json
# # Add the Server directory to sys.path
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# server_dir = os.path.join(parent_dir, 'Server')
# sys.path.append(parent_dir)

import mimetypes
from flask import Flask, render_template, request, jsonify, send_file
from Server.flow.flow_functions import analyze_class
from Server.flow.extract_functions import extract_entities, format_date
from Server.flow.check_for_missing_entities import check_for_missing
from Server.flow.launchDBFunc import launch_functions, get_flights, action_by_intent
from Server.database.functions import init

def create_app():
    app = Flask(__name__, static_folder='../Client', template_folder='../Client')

    mimetypes.init()
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')
    print(mimetypes.guess_type('auth.js'))
    init()

    def get_mimetype(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(root_dir, '..', 'Client', filename)
        if os.path.isfile(file_path):
            mimetype = get_mimetype(filename)
            return send_file(file_path, mimetype=mimetype)
        else:
            return 'File not found', 404

    @app.route('/')
    def chat():
        return render_template('index.html')
    
    @app.route('/signUp')
    def signUp():
        return render_template('/src/pages/signUp.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('/src/pages/dashboard.html')

    @app.route('/api/flightbot', methods=['POST'])
    def flightbot():
        data = request.get_json()
        message = data.get('message', '')
        
        user = data.get('user', '')
        # print("UserID:", user["uid"])
        # uid = user["uid"]

        # TODO:
        # Data needed to be extracted from the user's authentication firebase db - UID
        # Data from message - flight number, new date, new destination, new seats, ticket id

        print("Received message:", message)
        predicted_label, text = analyze_class(message)
        # Convert predicted_label to a regular Python integer
        predicted_label = int(predicted_label)
        # validate predicated label

        entities = extract_entities(message, predicted_label)
        print("Entities:", entities)

        #check for missing entities
        check_for_missing(entities, predicted_label)

        #validate entities


        #return text and entities
        response_data = text 
        response_message = f"{text} {str(entities)}"
        response_entities = json.dumps(entities)

        # lanch_functions(predicted_label, uid)
        # return jsonify({'response': response_message, 'predicted_label': predicted_label, 'response_data': response_data, entities: response_entities})
        return jsonify({'response': response_message, 'predicted_label': predicted_label, 'response_data': response_data, 'entities': response_entities})

    @app.route('/api/valflightbot', methods=['POST'])
    def vallightbotv():
        data = request.get_json()
        entities = data.get('entities', '')
        entities = json.loads(entities)
        try:
            entities["Date"] = format_date(entities["Date"])
        except:
            pass

        label = data.get('label', '')
        user = data.get('user', '')

        response = action_by_intent(label, entities, user["uid"])
        print("Response: ", response)
        return jsonify({'response': response})
    return app
