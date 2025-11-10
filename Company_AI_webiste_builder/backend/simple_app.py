from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Sample data
SERVICES = [
    {"id": 1, "name": "Web Development", "description": "Building modern web applications with React, Angular, and Vue.js"},
    {"id": 2, "name": "Mobile Development", "description": "Creating native and cross-platform mobile apps"},
    {"id": 3, "name": "Cloud Services", "description": "AWS, Azure, and Google Cloud solutions"},
    {"id": 4, "name": "UI/UX Design", "description": "Creating beautiful and intuitive user interfaces"}
]

PROJECTS = [
    {
        "id": 1,
        "title": "E-Commerce Platform",
        "description": "A full-featured online shopping platform",
        "image": "https://picsum.photos/800/600?random=1",
        "tags": ["React", "Node.js", "MongoDB"]
    },
    {
        "id": 2,
        "title": "Healthcare App",
        "description": "Patient management system",
        "image": "https://picsum.photos/800/600?random=2",
        "tags": ["Angular", "Python", "PostgreSQL"]
    }
]

@app.route("/")
def home():
    return jsonify({"message": "API is running"})

@app.route("/api/services")
def get_services():
    return jsonify(SERVICES)

@app.route("/api/projects")
def get_projects():
    return jsonify(PROJECTS)

if __name__ == "__main__":
    app.run(debug=True, port=5000)