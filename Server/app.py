from flask import Flask, render_template, request, jsonify

def create_app():
    app = Flask(__name__, static_folder='../Client', template_folder='../Client')

    @app.route('/chat')
    def chat():
        return render_template('index.html')

    @app.route('/api/flightbot', methods=['POST'])
    def flightbot():
        data = request.get_json()
        message = data.get('message', '')
        response = message + " !!!"
        print(response)
        return jsonify({'response': response})

    return app
