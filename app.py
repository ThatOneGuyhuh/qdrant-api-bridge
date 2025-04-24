from flask import Flask, request, jsonify
from qdrant_utils import embed_and_store, search_vector

app = Flask(__name__)

@app.route('/embed', methods=['POST'])
def embed():
    data = request.get_json()
    result = embed_and_store(data)
    return jsonify(result)

@app.route('/search', methods=['POST'])
def search():
    query = request.get_json().get("query")
    result = search_vector(query)
    return jsonify(result)

@app.route('/')
def root():
    return jsonify({"message": "Qdrant API Bridge active."})
