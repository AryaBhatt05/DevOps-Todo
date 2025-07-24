from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

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
    from bson.objectid import ObjectId
    collection.delete_one({'_id': ObjectId(task_id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
