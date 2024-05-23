import csv
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Database Setup
def create_database():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def populate_database(csv_file='data.csv'):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            try:
                cursor.execute('''
                    INSERT INTO items (id, name, price, description) 
                    VALUES (?, ?, ?, ?)
                ''', row)
            except sqlite3.IntegrityError:
                pass # Skip if the ID already exists

    conn.commit()
    conn.close()

# Request Handler
@app.route('/items/<int:item_id>')
def get_item(item_id):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        item = {
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'description': row[3]
        }
        return jsonify(item)
    else:
        return jsonify({'error': 'Item not found'}), 404

# Application Startup
if __name__ == '__main__':
    create_database()
    populate_database()
    app.run(debug=True)
