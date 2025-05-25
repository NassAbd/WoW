# backend/app.py
from flask import Flask, request, jsonify
from inheritance_parser import generate_mermaid_diagram
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/diagram", methods=["POST"])
def generate():
    data = request.get_json()
    module_name = data.get("module")
    diagrams = generate_mermaid_diagram(module_name)
    if diagrams is None:
        return jsonify({"error": "Module not found or no classes"})
    return jsonify(diagrams)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
