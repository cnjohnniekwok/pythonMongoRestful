from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']  # Database name
collection = db['items']  # Collection name

# Helper function to convert ObjectId to string
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# CREATE - Add new item
@app.route('/items', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = collection.insert_one(data)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get all items
@app.route('/items', methods=['GET'])
def get_items():
    try:
        items = list(collection.find())
        return JSONEncoder().encode(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get single item
@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    try:
        item = collection.find_one({'_id': ObjectId(id)})
        if item:
            return JSONEncoder().encode(item), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get items by query
@app.route('/items/query', methods=['GET'])
def get_items_by_query():
    try:
        # Get query from JSON body (optional, can be empty)
        query = request.get_json() or {}
        items = list(collection.find(query))
        return JSONEncoder().encode(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE - Update item
@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )
        
        if result.matched_count:
            return jsonify({'message': 'Item updated'}), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE - Update multiple items by query
@app.route('/items/bulk-update', methods=['PUT'])
def bulk_update_items():
    try:
        data = request.get_json()
        if not data or 'query' not in data or 'update' not in data:
            return jsonify({'error': 'Must provide "query" and "update" fields'}), 400
        
        query = data['query']
        update_data = data['update']
        
        result = collection.update_many(query, {'$set': update_data})
        
        return jsonify({
            'matched_count': result.matched_count,
            'modified_count': result.modified_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Delete item
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({'message': 'Item deleted'}), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Delete multiple items by query
@app.route('/items/bulk-delete', methods=['DELETE'])
def bulk_delete_items():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Must provide "query" field'}), 400
        
        query = data['query']
        
        result = collection.delete_many(query)
        
        return jsonify({
            'deleted_count': result.deleted_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)