from flask import Blueprint, render_template, request, redirect, url_for
from database import init_db
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        title = request.form['title']
        pdf = request.form['pdf']
        user_id = 1  # Placeholder for actual user ID
        conn = sqlite3.connect('class_management.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (user_id, title, pdf) VALUES (?, ?, ?)', (user_id, title, pdf))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    
    # Display tasks for the user
    conn = sqlite3.connect('class_management.db')
    c = conn.cursor()
    tasks = c.execute('SELECT * FROM tasks WHERE user_id = ?', (1,)).fetchall()  # Placeholder for actual user ID
    conn.close()
    return render_template('task_overview.html', tasks=tasks)
