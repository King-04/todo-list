from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

# File path for storing the to-do lists data
TODO_LISTS_FILE = 'todo_lists.json'

# Sample data structure to store lists and tasks
todo_lists = {}

def save_todo_lists_to_file():
    with open(TODO_LISTS_FILE, 'w') as file:
        json.dump(todo_lists, file)

def load_todo_lists_from_file():
    try:
        with open(TODO_LISTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Load existing data from file on application startup
todo_lists = load_todo_lists_from_file()

@app.route('/')
def index():
    return render_template('index.html', todo_lists=todo_lists)

@app.route('/create_list', methods=['POST'])
def create_list():
    list_title = request.form.get('list_title')
    if list_title:
        todo_lists[list_title] = []
        save_todo_lists_to_file()
    return redirect(url_for('index'))

@app.route('/todo/<list_title>', methods=['GET', 'POST'])
def todo(list_title):
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            # Modify task data structure to include a 'completed' flag
            todo_lists[list_title].append({'task': task, 'completed': False})
            save_todo_lists_to_file()

    return render_template('todo.html', list_title=list_title, tasks=todo_lists.get(list_title, []))

if __name__ == '__main__':
    app.run(debug=True)
