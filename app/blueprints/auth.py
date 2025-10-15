from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from app.db_connect import get_db
from werkzeug.security import check_password_hash
from functools import wraps

auth = Blueprint('auth', __name__)

def no_cache(f):
    """Decorator to prevent caching of pages"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return decorated_function

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    @no_cache
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Get employee by username
        cursor.execute('SELECT user_id, username, first_name, last_name, password FROM Employee WHERE username = %s', (username,))
        employee = cursor.fetchone()

        if employee and check_password_hash(employee['password'], password):
            # Login successful - store user info in session
            session['user_id'] = employee['user_id']
            session['username'] = employee['username']
            session['full_name'] = f"{employee['first_name']} {employee['last_name']}"

            flash(f'Welcome back, {employee["first_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
