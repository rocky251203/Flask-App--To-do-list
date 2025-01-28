import webbrowser
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()

# Initialize database before running the app
with app.app_context():
    init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task, status) VALUES (?, ?)', (task, 'Pending'))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ('Completed', task_id))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")  # Opens the app in the browser automatically
    app.run(debug=True)
