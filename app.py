from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# 🔗 Connect to MongoDB (local)
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["tasks"]

@app.route('/')
def index():
    tasks = collection.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form['task']
    if task_content:
        collection.insert_one({'task': task_content})
    return redirect('/')

@app.route('/delete/<task_id>')
def delete(task_id):
    collection.delete_one({'_id': ObjectId(task_id)})
    return redirect('/')

# NEW: JSON API Route for Git Branch Task
@app.route('/api', methods=['GET'])
def get_data():
    return jsonify([
        {"name": "Arya Task 1", "desc": "Flask API testing"},
        {"name": "Arya Task 2", "desc": "Modified by arya_new branch"}
    ])
    
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_desc = request.form.get('itemDescription')

    if item_name and item_desc:
        collection.insert_one({'item_name': item_name, 'item_description': item_desc})

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
