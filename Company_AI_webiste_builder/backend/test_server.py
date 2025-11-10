from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

test_data = [
    {"id": 1, "name": "Test Service 1", "description": "This is a test service"},
    {"id": 2, "name": "Test Service 2", "description": "This is another test service"}
]

@app.route('/test')
def test():
    return jsonify({"message": "Server is working!"})

@app.route('/api/services')
def get_services():
    return jsonify(test_data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)