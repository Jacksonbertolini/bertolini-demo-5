from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
from app.blueprints.auth import login_required

customers = Blueprint('customers', __name__)

@customers.route('/', methods=['GET', 'POST'])
@login_required
def show_customers():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new customer
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        # Insert the new customer into the database
        cursor.execute('INSERT INTO Customer (name, phone, email) VALUES (%s, %s, %s)',
                       (name, phone, email))
        db.commit()

        flash('New customer added successfully!', 'success')
        return redirect(url_for('customers.show_customers'))

    # Handle GET request to display all customers
    cursor.execute('SELECT * FROM Customer ORDER BY name')
    all_customers = cursor.fetchall()
    return render_template('customers.html', all_customers=all_customers)

@customers.route('/update_customer/<int:customer_id>', methods=['POST'])
@login_required
def update_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    # Update the customer's details
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']

    cursor.execute('UPDATE Customer SET name = %s, phone = %s, email = %s WHERE customer_id = %s',
                   (name, phone, email, customer_id))
    db.commit()

    flash('Customer updated successfully!', 'success')
    return redirect(url_for('customers.show_customers'))

@customers.route('/delete_customer/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    # Check if customer has orders
    cursor.execute('SELECT COUNT(*) as order_count FROM `Order` WHERE customer_id = %s', (customer_id,))
    result = cursor.fetchone()

    if result['order_count'] > 0:
        flash(f'Cannot delete customer! They have {result["order_count"]} order(s). Delete their orders first.', 'danger')
        return redirect(url_for('customers.show_customers'))

    # Delete the customer
    cursor.execute('DELETE FROM Customer WHERE customer_id = %s', (customer_id,))
    db.commit()

    flash('Customer deleted successfully!', 'danger')
    return redirect(url_for('customers.show_customers'))

@customers.route('/view/<int:customer_id>')
@login_required
def view_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    # Get customer information
    cursor.execute('SELECT * FROM Customer WHERE customer_id = %s', (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        flash('Customer not found!', 'danger')
        return redirect(url_for('customers.show_customers'))

    # Get customer's orders
    cursor.execute('''
        SELECT o.order_id, o.date, COUNT(od.order_detail_id) as item_count,
               SUM(p.price * od.quantity) as total_amount
        FROM `Order` o
        LEFT JOIN Order_Detail od ON o.order_id = od.order_id
        LEFT JOIN Pizza p ON od.pizza_id = p.pizza_id
        WHERE o.customer_id = %s
        GROUP BY o.order_id, o.date
        ORDER BY o.date DESC
    ''', (customer_id,))
    orders = cursor.fetchall()

    # Calculate total spent
    total_spent = sum(order['total_amount'] or 0 for order in orders)

    return render_template('customer_details.html', customer=customer, orders=orders, total_spent=total_spent)
