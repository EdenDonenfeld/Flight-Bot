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
from Server.flow.extract_functions import extract_entities
from Server.flow.check_for_missing_entities import check_for_missing
from Server.flow.launchDBFunc import launch_functions, action_by_intent
from Server.database.functions import init, add_new_user, return_available_seats, get_tickets

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
    
    @app.route('/myTickets')
    def myTickets():
        return render_template('/src/pages/myTickets.html')

    @app.route('/api/flightbot', methods=['POST'])
    def flightbot():
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', '')

        predicted_label = analyze_class(message)
        # Convert predicted_label to a regular Python integer
        predicted_label = int(predicted_label)
        # validate predicated label

        entities = extract_entities(message, predicted_label)

        #TODO: check for missing entities
        check_for_missing(entities, predicted_label)
 
        #TODO: validate entities - here the user should be asked to provide the missing entities, or correct the provided entities

        #return entities
        response_message = f"{str(entities)}"
        response_entities = json.dumps(entities)

        # lanch_functions(predicted_label, uid)
        # return jsonify({'response': response_message, 'predicted_label': predicted_label, 'response_data': response_data, entities: response_entities})
        return jsonify({'response': response_message, 'predicted_label': predicted_label, 'entities': response_entities})

    @app.route('/api/flightbot/user', methods=['POST'])
    def check_user():
        data = request.get_json()
        user_id = data.get('user_id', '')
        print("User ID: ", user_id)
        # add user_id if not exists
        try:
            add_new_user(user_id)
            return jsonify({'response': 'User added successfully'}, 200)
        except:
            return jsonify({'response': 'User already exists'}, 400)
        
    @app.route('/api/seats/<flight_id>', methods=['GET'])
    def get_seats(flight_id):
        seats = return_available_seats(flight_id)
        return jsonify({'response': seats})

    @app.route('/api/valflightbot', methods=['POST'])
    def vallightbotv():
        data = request.get_json()
        entities = data.get('entities', '')
        entities = json.loads(entities)
        print("Entities:", entities)
    
        label = data.get('label', '')
        user = data.get('user', '')

        response = action_by_intent(label, entities, user["uid"])
        print("Response: ", response)
        return jsonify({'response': response})
    
    # alpha version: buy flight ticket
    @app.route('/api/finalActions', methods=['POST'])
    def finalActions():
        data = request.get_json()
        entities = data.get('entities', '')
        entities = json.loads(entities)
        # print("Entities:", entities)

        response = launch_functions(entities["label"], entities, entities["user"]["uid"])
        # print("Response: ", response)
        return jsonify({'response': response, 'label': entities["label"]})
    
    @app.route('/api/myTickets', methods=['POST'])
    def sendUserTickets():
        data = request.get_json()
        user_id = data.get('user-id', '')
        print("User ID: ", user_id)
        # get_tickets not working
        tickets = get_tickets(user_id)
        return jsonify({'response': tickets})

    return app
