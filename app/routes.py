from flask import render_template, redirect, url_for, session
from . import app
from app.blueprints.auth import login_required
from app.db_connect import get_db
from datetime import datetime

@app.route('/')
def index():
    # If user is logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    # Otherwise show login page
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor()

    # Get current year
    current_year = datetime.now().year

    # Get total sales for all time (with 7% tax included)
    from decimal import Decimal
    cursor.execute('''
        SELECT COALESCE(SUM(p.price * od.quantity), 0) as subtotal
        FROM `Order` o
        JOIN Order_Detail od ON o.order_id = od.order_id
        JOIN Pizza p ON od.pizza_id = p.pizza_id
    ''')
    sales_result = cursor.fetchone()
    subtotal_sales = sales_result['subtotal'] if sales_result else 0
    tax_rate = Decimal('0.07')
    total_sales = subtotal_sales * (1 + tax_rate)

    # Get total number of customers
    cursor.execute('SELECT COUNT(*) as customer_count FROM Customer')
    customer_result = cursor.fetchone()
    customer_count = customer_result['customer_count'] if customer_result else 0

    # Get most recent orders (last 10)
    cursor.execute('''
        SELECT o.order_id, o.date, c.name as customer_name,
               COUNT(od.order_detail_id) as item_count,
               SUM(p.price * od.quantity) as order_total
        FROM `Order` o
        JOIN Customer c ON o.customer_id = c.customer_id
        LEFT JOIN Order_Detail od ON o.order_id = od.order_id
        LEFT JOIN Pizza p ON od.pizza_id = p.pizza_id
        GROUP BY o.order_id, o.date, c.name
        ORDER BY o.date DESC, o.order_id DESC
        LIMIT 10
    ''')
    recent_orders = cursor.fetchall()

    return render_template('dashboard.html',
                         total_sales=total_sales,
                         customer_count=customer_count,
                         recent_orders=recent_orders,
                         current_year=current_year)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
@login_required
def profile():
    db = get_db()
    cursor = db.cursor()

    # Get logged-in employee's information
    user_id = session.get('user_id')
    cursor.execute('''
        SELECT user_id, username, first_name, last_name, created_at, updated_at
        FROM Employee
        WHERE user_id = %s
    ''', (user_id,))
    employee = cursor.fetchone()

    if not employee:
        flash('Employee profile not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Get orders processed by this employee (using created_at as proxy)
    # Since we don't have an employee_id in Order table, we'll show recent system activity
    cursor.execute('''
        SELECT COUNT(*) as total_orders
        FROM `Order`
    ''')
    stats = cursor.fetchone()

    return render_template('profile.html', employee=employee, stats=stats)
