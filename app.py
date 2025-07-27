from flask import Flask, render_template, request, redirect, session, jsonify
from db_config import get_connection

app = Flask(__name__)
app.secret_key = 'secret123'

ADMIN_USER = "ganesh@123"
ADMIN_PASS = "Pass@8010"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user')
def user_panel():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('user.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit_answer():
    correct = request.form['correct']
    selected = request.form['selected']
    return jsonify({'result': 'correct' if correct == selected else 'incorrect'})

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'POST':
        q = request.form['question']
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        d = request.form['d']
        correct = request.form['correct']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option) VALUES (%s, %s, %s, %s, %s, %s)",
            (q, a, b, c, d, correct)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin')
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if email == ADMIN_USER and password == ADMIN_PASS:
        session['logged_in'] = True
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail'})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')