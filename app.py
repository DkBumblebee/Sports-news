from flask import Flask, redirect, render_template, request, session
from database import create_table, creat_user, query
from collections import namedtuple
import sqlite3

app = Flask(__name__)
app.secret_key="__my_privateKey__"

create_table()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods= ['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            user = query("SELECT username,password FROM users WHERE username = ? AND password=?", (username, password))
            print(user)
            if len(user) > 0:
                session['username'] = username
                return redirect("/tasks")
            else:
                print("Invalid username or password")
                return render_template("login.html")

        except Exception as e:
            print(f"Login error: {e}")
            return render_template("login.html", error=e)
    return render_template("login.html")

@app.route("/register", methods= ['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            print("Do not match")
            return render_template("login.html", error="Passwords do not match")
        try:
            creat_user(username, password)
            return render_template("login.html")
        except Exception as e:
            print(f"Error creating user: {e}")
        finally:
            return render_template("login.html")
    return render_template("login.html")

@app.route("/tasks")
def tasks():
    if 'username' not in session:
        return redirect("/login")
    username = session['username']
    tasks_data = query("SELECT id, description FROM tasks WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
    Task = namedtuple("Task", ["id", "description"]) #Create a namedtuple
    tasks = [Task(*row) for row in tasks_data] #Convert to namedtuples
    print(tasks)  # Print the tasks data to the console
    return render_template("tasks.html", tasks=tasks)


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session..
    return redirect('/login')


@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    task_description = request.form['task']

    if task_description: # Check if the task description is not empty
        try:
            user_data = query("SELECT id FROM users WHERE username = ?", (username,))
            if user_data and len(user_data) > 0: # Check if the user exists
                user_id = user_data[0][0] 
            query("INSERT INTO tasks (description, user_id) VALUES (?, ?)", (task_description, user_id))
        except Exception as e:
            print(f"Error adding task: {e}")
            # Handle the error appropriately (e.g., flash a message)

    return redirect('/tasks')  # Redirect back to the task page

@app.route('/edit_task', methods=['POST'])
def edit_task():
    if 'username' not in session:
        return redirect('/login')

    task_id = request.form['task_id']
    task_description = request.form['task']

    try:
        query("UPDATE tasks SET description = ? WHERE id = ?", (task_description, task_id))
    except Exception as e:
        print(f"Error editing task: {e}")

    return redirect('/tasks')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    if 'username' not in session:
        return redirect('/login')
    
    task_id = request.form['task_id']

    try:
        query("DELETE FROM tasks WHERE id = ?", (task_id,))
    except Exception as e:
        print(f"Error deleting task: {e}")
        return render_template("tasks.html", error="Error deleting task")# Return an error response

    return redirect("/tasks") # Return an empty response to indicate success