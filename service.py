from flask import Flask, jsonify, request

class BackendManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_endpoints()

    def setup_endpoints(self):
        self.add_cors_headers(self.app)  # Aplica os cabeçalhos CORS globalmente
        self.app.route('/api/data', methods=['GET'])(self.get_data)
        self.app.route('/api/save_questions', methods=['POST'])(self.post_data)

    @staticmethod
    def add_cors_headers(app):
        @app.after_request
        def add_cors_headers(response):
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

    def get_data(self):
        data = {'message': 'GET request successful'}
        return jsonify(data)

    def post_data(self):
        content = request.get_json()
        if content is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        message = content.get('message')
        if message is None:
            return jsonify({'error': 'Message not found in JSON'}), 400

        response_data = {'message': f'POST request successful. Received message: {message}'}
        return jsonify(response_data)

    def run(self, host='localhost', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    api = BackendManager()
    api.run()