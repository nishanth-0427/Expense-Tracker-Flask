import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
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
    
    # Fetch expenses
    cursor.execute('SELECT * FROM expenses')
    all_expenses = cursor.fetchall()
    
    # Calculate total using SQL
    cursor.execute('SELECT SUM(amount) FROM expenses')
    row = cursor.fetchone()
    total = row[0] if row[0] is not None else 0
        
    conn.close()
    return render_template('index.html', expenses=all_expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    item = request.form.get('item')
    amount = request.form.get('amount')
    category = request.form.get('category')
    
    # The 'with' block automatically CLOSES the connection for you
    with sqlite3.connect('database.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (item, amount, category) VALUES (?, ?, ?)', (item, amount, category))
        conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_expense(id):
    with sqlite3.connect('database.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
        conn.commit()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)