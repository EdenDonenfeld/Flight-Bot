import mimetypes, os
from flask import Flask, render_template, request, jsonify, send_file

def create_app():
    app = Flask(__name__, static_folder='../Client', template_folder='../Client')

    mimetypes.init()
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')
    print(mimetypes.guess_type('auth.js'))

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
        response = message + " !!!"
        print(response)
        return jsonify({'response': response})

    return app
