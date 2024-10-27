from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_admin_key'  # Change this for production

# Set the port to 8800
PORT = 8800

# Admin credentials
ADMIN_EMAIL = 'admin@admin.com'
ADMIN_PASSWORD = 'admin@admin123'

# Helper function to interact with SQLite
def query_db(query, args=(), one=False):
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row  # Use Row factory to access columns by name
        cur = con.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        con.commit()
        return (rv[0] if rv else None) if one else rv

# Admin Login Route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials. Please try again."
    return render_template("login.html")

# Admin Dashboard Route
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    students = query_db("SELECT id, name, email FROM students")
    return render_template("admin_dashboard.html", students=students)

# Manage Users Route
@app.route('/manage-users')
def manage_users():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    # Fetch users from the database
    users = query_db("SELECT id, username, email, role FROM users")  # Adjust table name as needed
    return render_template("manage_users.html", users=users)

# View User Route
@app.route('/admin/user/<int:user_id>')
def view_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    user = query_db("SELECT username, email, role FROM users WHERE id=?", (user_id,), one=True)
    return render_template("view_user.html", user=user)

# Edit User Route
@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']  # Get the role
        query_db("UPDATE users SET username=?, email=?, role=? WHERE id=?", (username, email, role, user_id))
        return redirect(url_for('manage_users'))
    
    user = query_db("SELECT * FROM users WHERE id=?", (user_id,), one=True)  # Ensure user is fetched as a dictionary
    return render_template("edit_user.html", user=user)

# Add User Route
@app.route('/admin/user/add', methods=['POST'])
def add_user():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    # Insert user into the database
    query_db("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", 
             (username, email, password, role))

    return redirect(url_for('manage_users'))

# Delete User Route
@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    query_db("DELETE FROM users WHERE id=?", (user_id,))
    return redirect(url_for('manage_users'))

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # Capture the role

        # Insert user into the database
        query_db("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", 
                 (username, email, password, role))
        return redirect(url_for('admin_login'))
    return render_template("signup.html")

# Admin Logout Route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(port=PORT)
