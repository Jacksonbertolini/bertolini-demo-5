-- Sample data for Pizza Management System
-- Run this after creating the schema to populate with sample records

-- Insert Customers
INSERT INTO Customer (name, phone, email) VALUES
('John Smith', '555-0101', 'john.smith@email.com'),
('Jane Doe', '555-0102', 'jane.doe@email.com'),
('Michael Johnson', '555-0103', 'michael.j@email.com'),
('Sarah Williams', '555-0104', 'sarah.w@email.com'),
('David Brown', '555-0105', 'david.brown@email.com'),
('Emily Davis', '555-0106', 'emily.davis@email.com'),
('Christopher Miller', '555-0107', 'chris.miller@email.com'),
('Ashley Wilson', '555-0108', 'ashley.w@email.com'),
('Matthew Moore', '555-0109', 'matt.moore@email.com'),
('Jessica Taylor', '555-0110', 'jessica.t@email.com');

-- Insert Pizzas
INSERT INTO Pizza (name, size, price, cost) VALUES
('Margherita', 'Small', 8.99, 3.50),
('Margherita', 'Medium', 12.99, 5.00),
('Margherita', 'Large', 15.99, 6.50),
('Pepperoni', 'Small', 9.99, 4.00),
('Pepperoni', 'Medium', 13.99, 6.00),
('Pepperoni', 'Large', 16.99, 7.50),
('Hawaiian', 'Small', 10.99, 4.50),
('Hawaiian', 'Medium', 14.99, 6.50),
('Hawaiian', 'Large', 17.99, 8.00),
('Veggie Supreme', 'Small', 11.99, 5.00),
('Veggie Supreme', 'Medium', 15.99, 7.00),
('Veggie Supreme', 'Large', 18.99, 8.50),
('Meat Lovers', 'Small', 12.99, 5.50),
('Meat Lovers', 'Medium', 16.99, 7.50),
('Meat Lovers', 'Large', 19.99, 9.00),
('BBQ Chicken', 'Small', 11.99, 5.00),
('BBQ Chicken', 'Medium', 15.99, 7.00),
('BBQ Chicken', 'Large', 18.99, 8.50),
('Buffalo Chicken', 'Small', 11.99, 5.00),
('Buffalo Chicken', 'Medium', 15.99, 7.00),
('Buffalo Chicken', 'Large', 18.99, 8.50),
('Four Cheese', 'Small', 10.99, 4.50),
('Four Cheese', 'Medium', 14.99, 6.50),
('Four Cheese', 'Large', 17.99, 8.00);

-- Insert Employees
INSERT INTO Employee (username, first_name, last_name, password) VALUES
('admin', 'Admin', 'User', 'pbkdf2:sha256:600000$salt123$hash123'),
('jsmith', 'John', 'Smith', 'pbkdf2:sha256:600000$salt456$hash456'),
('mjones', 'Mary', 'Jones', 'pbkdf2:sha256:600000$salt789$hash789'),
('bwilson', 'Bob', 'Wilson', 'pbkdf2:sha256:600000$salt012$hash012'),
('sgarcia', 'Sarah', 'Garcia', 'pbkdf2:sha256:600000$salt345$hash345');

-- Insert Orders
INSERT INTO `Order` (customer_id, date) VALUES
(1, '2024-01-15'),
(2, '2024-01-15'),
(3, '2024-01-16'),
(1, '2024-01-17'),
(4, '2024-01-17'),
(5, '2024-01-18'),
(6, '2024-01-19'),
(7, '2024-01-19'),
(8, '2024-01-20'),
(9, '2024-01-21'),
(10, '2024-01-21'),
(2, '2024-01-22'),
(3, '2024-01-22'),
(4, '2024-01-23'),
(5, '2024-01-24');

-- Insert Order Details
INSERT INTO Order_Detail (order_id, pizza_id, quantity) VALUES
-- Order 1
(1, 5, 2),
(1, 8, 1),
-- Order 2
(2, 2, 1),
(2, 14, 1),
-- Order 3
(3, 6, 3),
-- Order 4
(4, 11, 1),
(4, 17, 1),
(4, 23, 1),
-- Order 5
(5, 1, 2),
-- Order 6
(6, 15, 1),
(6, 20, 2),
-- Order 7
(7, 9, 1),
-- Order 8
(8, 3, 2),
(8, 12, 1),
-- Order 9
(9, 18, 1),
(9, 24, 1),
-- Order 10
(10, 7, 2),
-- Order 11
(11, 13, 1),
(11, 19, 1),
-- Order 12
(12, 4, 3),
-- Order 13
(13, 10, 1),
(13, 16, 2),
-- Order 14
(14, 21, 1),
(14, 22, 1),
-- Order 15
(15, 14, 2),
(15, 8, 1);
