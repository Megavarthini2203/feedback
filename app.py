from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

# Initialize DB if it doesn't exist
DB_PATH = "feedback.db"
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE feedback (name TEXT, email TEXT, comment TEXT)')
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    comment = request.form['comment']

    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO feedback (name, email, comment) VALUES (?, ?, ?)', (name, email, comment))
    conn.commit()
    conn.close()

    return "Thanks for your feedback!"

@app.route('/feedbacks')
def feedbacks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute('SELECT name, email, comment FROM feedback')
    data = cursor.fetchall()
    conn.close()
    return {'feedbacks': data}

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

