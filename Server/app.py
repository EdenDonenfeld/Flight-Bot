import sys
import os

# Add the Server directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
server_dir = os.path.join(parent_dir, 'Server')
sys.path.append(server_dir)

from flask import Flask, render_template, request, jsonify
from nlpAnalyze import analyze_class

def create_app():
    app = Flask(__name__, static_folder='../Client', template_folder='../Client')

    @app.route('/chat')
    def chat():
        return render_template('index.html')

    @app.route('/api/flightbot', methods=['POST'])
    def flightbot():
        data = request.get_json()
        message = data.get('message', '')
        print("Received message:", message)
        predicted_label, text = analyze_class(message)
        return jsonify({'response': text})

    return app
