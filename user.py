import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    # Database initialization logic if required
    pass

def start_app():
    app.run(port=5050)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        user = c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if user:
            session['username'] = user[1]  # Username
            session['role'] = user[4]  # Role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please sign up.')
            return redirect(url_for('signup'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)', (username, email, password, 'student'))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email or username already exists.')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin/user/<int:user_id>')
def view_user(user_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    user = c.execute("SELECT username, email, role FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()

    if user is None:
        return "User not found", 404  # Return 404 if user not found
    
    return render_template("view_user.html", user=user)

@app.route('/tasks')
def tasks():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('task_overview.html')  # Render your existing task_overview.html

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    start_app()
