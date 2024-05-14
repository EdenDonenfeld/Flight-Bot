from flask import Flask, render_template

def create_app():
    app = Flask(__name__, static_folder='../client', template_folder='../client')

    @app.route('/chat')
    def chat():
        return render_template('index.html')

    @app.route('/api/flightbot/<message>', methods=['POST'])
    def flightbot(message):
        response = message + " !!!"
        return response

    return app
