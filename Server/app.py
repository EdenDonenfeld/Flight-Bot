import sys
import os
from flask import Flask, render_template, request, jsonify
from database.functions import order_ticket, refund_ticket, change_date, change_dest, check_status
from flow.flow_functions import analyze_class
from flow.extract_functions import extract_places, extract_dates
# from nlpAnalyze import analyze_class

# Add the Server directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
server_dir = os.path.join(parent_dir, 'Server')
sys.path.append(server_dir)

def lanch_functions(predicted_label, uid,):
    if predicted_label == 0:
        # order ticket(uid, flight_num, seats)
        order_ticket()
    elif predicted_label == 1:
        # refund ticket(uid, ticket_id)
        refund_ticket()
    elif predicted_label == 2:
        # check status(uid, ticket_id)
        check_status()
    elif predicted_label == 3:
        # change date(uid, ticket_id, new_date, new_seats)
        change_date()
    elif predicted_label == 4:
        # change dest(uid, ticket_id, new_dest, new_seats)
        change_dest()
    elif predicted_label == 5:
        # weather
        pass
    else:
        # what's allowed
        pass



def create_app():
    app = Flask(__name__, static_folder='../Client', template_folder='../Client')

    @app.route('/chat')
    def chat():
        return render_template('index.html')

    @app.route('/api/flightbot', methods=['POST'])
    def flightbot():
        data = request.get_json()
        message = data.get('message', '')

        # TODO:
        # Data needed to be extracted from the user's authentication firebase db - UID
        # Data from message - flight number, new date, new destination, new seats, ticket id

        print("Received message:", message)
        predicted_label, text = analyze_class(message)
        
        # lanch_functions(predicted_label, uid)
        return jsonify({'response': text})

    return app
