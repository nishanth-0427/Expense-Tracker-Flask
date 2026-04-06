import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# This function creates our database table if it doesn't exist
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Change your CREATE TABLE line to include 'category'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT 'General'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 1. Fetch all expenses
    cursor.execute('SELECT * FROM expenses')
    all_expenses = cursor.fetchall()
    
    # 2. Calculate the total amount
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()[0]
    if total is None:
        total = 0 # If the list is empty, set total to 0
        
    conn.close()
    return render_template('index.html', expenses=all_expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    item = request.form.get('item')
    amount = request.form.get('amount')
    category = request.form.get('category') # NEW LINE
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Update the query to include category
    cursor.execute('INSERT INTO expenses (item, amount, category) VALUES (?, ?, ?)', (item, amount, category))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db() # Run the database setup
    app.run(debug=True)