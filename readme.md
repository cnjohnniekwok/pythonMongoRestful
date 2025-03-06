# MongoDB CRUD with Python API Server and Client UI

This project consists of a Flask-based RESTful API server connected to MongoDB and a Tkinter-based GUI client for performing CRUD (Create, Read, Update, Delete) operations on a housing survey dataset. The API supports single and bulk operations, and the UI provides an intuitive interface to interact with the data.

## Installation Steps
### Install MongoDB
1. Download and Install MongoDB [https://www.mongodb.com/try/download/community]
2. Set up the data directory for example in window:
```shell
mkdir C:\data\db
```

### Install Python
1. Download and Install Python [https://www.python.org/downloads/release/python-3132/]
2. Install the required packages:
```shell
python --version
pip upgrade
pip install flask pymongo requests
```

## Start MongoDB
1. change directory into mongod executable file location
```shell
cd "<PATH TO MONGODB>\MongoDB\Server\8.0\bin"
mongod.exe --dbpath "C:\data\db"
```
2. MongoDB will run on http://localhost:27017. Keep this terminal open.
3. You can also install MongoDB Compass to help visualise the database, the uri for this connection is `mongodb://localhost:27017/`.

## Start API Server
1. Clone this repository into your machine
```shell
git clone 
```
2. Run python command to start the server:
```shell
python ./api_server.py
```
The API server will run on http://localhost:5000, Keep this terminal open.

## Start the Client UI
1. If you haven't done so in the previos step, clone this repository into your machine
```shell
git clone 
```
2. Run python command to launch the UI:
```shell
python ./api_client.py
```

# Test JSON Prompts
Below are example JSON inputs for testing the API and UI, Paste these into the UI’s "JSON Input" text box and click the corresponding button:

### Create (`POST /items`)
Create a new record.

```json
{
  "address": "123 Maple St",
  "rooms": 3,
  "price": 250000,
  "condition": "good"
}
```
Response Example: `{"id": "some_object_id"}`


### Read All (`GET /items`)
Retrieve all entries.
No input needed, just return everything from the database.

Response Example:
```json
[
  {"_id": "660f8e2b...", "address": "123 Maple St", "rooms": 3, "price": 250000, "condition": "good"},
  {"_id": "660f8e2c...", "address": "456 Oak Ave", "rooms": 4, "price": 300000, "condition": "excellent"}
]
```

### Query (`GET /items/query`)
Filter entry by a condition.
Below input is a query on properties that consists of 3 rooms.
```json
{
  "rooms": 3
}
```

Response Example:
```json
[
  {"_id": "660f8e2b...", "address": "123 Maple St", "rooms": 3, "price": 250000, "condition": "good"}
]
```

### Update (`PUT /items/<id>`)
Update a specific entry by ID.
Note: Replace _id with an actual ID from "Read All" or "Query".

```json
{
  "_id": "660f8e2b...",
  "price": 260000,
  "condition": "renovated"
}
```
Response Example: `{"message": "Item updated"}`

### Delete (`DELETE /items/<id>`)
Delete a specific entry by ID.
Note: Replace _id with an actual ID from "Read All" or "Query".

```json
{
  "_id": "660f8e2b..."
}
```
Response Example: `{"message": "Item deleted"}`

### Bulk Update (`PUT /items/bulk-update`)
Update all entry with a specific query condition.

```json
{
  "query": {"rooms": 3},
  "update": {"price": 270000, "condition": "updated"}
}
```

### Bulk Delete (`DELETE /items/bulk-delete`)
Delete all entry matching a query.


```json
{
  "query": {"condition": "good"}
}
```

Response example: Response: `{"deleted_count": N}` (where `N` is the number of deleted items)