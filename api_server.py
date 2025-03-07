from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']  # Database name
collection = db['properties']  # Collection name

# CREATE - Add new item (updated to support bulk)
@app.route('/properties', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if isinstance(data, list):  # Handle bulk create
            result = collection.insert_many(data)
            return jsonify({'ids': [str(id) for id in result.inserted_ids]}), 201
        else:  # Single create
            result = collection.insert_one(data)
            return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get all properties
@app.route('/properties', methods=['GET'])
def get_properties():
    try:
        properties = list(collection.find())
        for item in properties:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string
        return jsonify(properties), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get single item
@app.route('/properties/<id>', methods=['GET'])
def get_item(id):
    try:
        item = collection.find_one({'_id': ObjectId(id)})
        if item:
            item['_id'] = str(item['_id'])
            return jsonify(item), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get properties by query
@app.route('/properties/query', methods=['GET'])
def get_properties_by_query():
    try:
        query = request.get_json() or {}
        properties = list(collection.find(query))
        for item in properties:
            item['_id'] = str(item['_id'])
        return jsonify(properties), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE - Update item
@app.route('/properties/<id>', methods=['PUT'])
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

# UPDATE - Update multiple properties by query
@app.route('/properties/bulk-update', methods=['PUT'])
def bulk_update_properties():
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
@app.route('/properties/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({'message': 'Item deleted'}), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Delete multiple properties by query
@app.route('/properties/bulk-delete', methods=['DELETE'])
def bulk_delete_properties():
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