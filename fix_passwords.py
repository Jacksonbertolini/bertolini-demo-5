"""
Script to fix employee passwords in the database
This will update the admin user with the password 'password'
"""
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import pymysql
import os

# Load environment variables
load_dotenv()

def fix_passwords():
    # Connect directly to database
    db = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()

    # Create properly hashed passwords
    admin_password = generate_password_hash('password')
    jsmith_password = generate_password_hash('password123')
    mjones_password = generate_password_hash('password123')
    bwilson_password = generate_password_hash('password123')
    sgarcia_password = generate_password_hash('password123')

    # Update all employees with proper password hashes
    employees = [
        ('admin', admin_password),
        ('jsmith', jsmith_password),
        ('mjones', mjones_password),
        ('bwilson', bwilson_password),
        ('sgarcia', sgarcia_password)
    ]

    for username, password_hash in employees:
        cursor.execute(
            'UPDATE Employee SET password = %s WHERE username = %s',
            (password_hash, username)
        )
        print(f"Updated password for user: {username}")

    db.commit()
    print("\nAll passwords updated successfully!")
    print("\nYou can now log in with:")
    print("  Username: admin")
    print("  Password: password")

    cursor.close()
    db.close()

if __name__ == '__main__':
    fix_passwords()
