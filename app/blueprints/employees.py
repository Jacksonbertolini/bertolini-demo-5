from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
from app.blueprints.auth import login_required
from werkzeug.security import generate_password_hash

employees = Blueprint('employees', __name__)

@employees.route('/', methods=['GET', 'POST'])
@login_required
def show_employees():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new employee
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        # Check if username already exists
        cursor.execute('SELECT COUNT(*) as count FROM Employee WHERE username = %s', (username,))
        result = cursor.fetchone()

        if result['count'] > 0:
            flash('Username already exists! Please choose a different username.', 'danger')
            return redirect(url_for('employees.show_employees'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new employee into the database
        cursor.execute('INSERT INTO Employee (username, first_name, last_name, password) VALUES (%s, %s, %s, %s)',
                       (username, first_name, last_name, hashed_password))
        db.commit()

        flash('New employee added successfully!', 'success')
        return redirect(url_for('employees.show_employees'))

    # Handle GET request to display all employees
    cursor.execute('SELECT user_id, username, first_name, last_name, created_at, updated_at FROM Employee ORDER BY last_name, first_name')
    all_employees = cursor.fetchall()
    return render_template('employees.html', all_employees=all_employees)

@employees.route('/update_employee/<int:user_id>', methods=['POST'])
@login_required
def update_employee(user_id):
    db = get_db()
    cursor = db.cursor()

    # Update the employee's details
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form.get('password', '')

    # Check if username is taken by another user
    cursor.execute('SELECT COUNT(*) as count FROM Employee WHERE username = %s AND user_id != %s', (username, user_id))
    result = cursor.fetchone()

    if result['count'] > 0:
        flash('Username already exists! Please choose a different username.', 'danger')
        return redirect(url_for('employees.show_employees'))

    # If password is provided, hash it and update
    if password:
        hashed_password = generate_password_hash(password)
        cursor.execute('UPDATE Employee SET username = %s, first_name = %s, last_name = %s, password = %s WHERE user_id = %s',
                       (username, first_name, last_name, hashed_password, user_id))
    else:
        # Update without changing password
        cursor.execute('UPDATE Employee SET username = %s, first_name = %s, last_name = %s WHERE user_id = %s',
                       (username, first_name, last_name, user_id))

    db.commit()

    flash('Employee updated successfully!', 'success')
    return redirect(url_for('employees.show_employees'))

@employees.route('/delete_employee/<int:user_id>', methods=['POST'])
@login_required
def delete_employee(user_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the employee
    cursor.execute('DELETE FROM Employee WHERE user_id = %s', (user_id,))
    db.commit()

    flash('Employee deleted successfully!', 'danger')
    return redirect(url_for('employees.show_employees'))
