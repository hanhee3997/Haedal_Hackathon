from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import csv
import os

app = Flask(__name__)
app.secret_key = 'sunmyeong_secret_key_1234'
CSV_FILE = 'reviews.csv'
USER_FILE = 'users.csv'

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(['location', 'sub_location', 'price', 'sunlight', 'review'])

if not os.path.exists(USER_FILE):
    with open(USER_FILE, mode='w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(['username', 'password'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form.get('username').strip()
        user_pw = request.form.get('password').strip()
        with open(USER_FILE, mode='a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([user_id, user_pw])
        return "<h2>가입 성공! 🎉</h2><a href='/login'>로그인하러 가기</a>"
    return '''<div style="text-align:center; margin-top:100px;"><h2>📝 회원가입</h2>
    <form method="POST">
    <input name="username" placeholder="아이디" required><br><br>
    <input type="password" name="password" placeholder="비밀번호" required><br><br>
    <button>가입하기</button></form></div>'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('username').strip()
        user_pw = request.form.get('password').strip()
        with open(USER_FILE, mode='r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row and row[0] == user_id and row[1] == user_pw:
                    session['logged_in'] = True
                    return redirect(url_for('home'))
        return "<h2>아이디/비번이 틀렸습니다.</h2><a href='/login'>다시 시도</a>"
    return '''<div style="text-align:center; margin-top:100px;"><h2>🏠 로그인</h2>
    <form method="POST">
    <input name="username" placeholder="아이디" required><br><br>
    <input type="password" name="password" placeholder="비밀번호" required><br><br>
    <button>로그인</button></form><br>
    <a href="/register">회원가입 하기</a></div>'''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    loc     = data.get('location', '미정')
    sub_loc = data.get('sub_location', '미정')
    price   = data.get('price', '정보없음')
    sun     = data.get('sunlight', '정보없음')
    rev     = data.get('review', '내용없음')
    with open(CSV_FILE, mode='a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow([loc, sub_loc, price, sun, rev])
    return jsonify({"status": "success"}), 200

@app.route('/location/<name>')
def show_reviews(name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    target_name = name.strip()
    reviews = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 5 and row[0].strip() == target_name:
                    reviews.append({
                        'sub': row[1],
                        'price': row[2],
                        'sun': row[3],
                        'rev': row[4]
                    })
    return render_template('reviews.html', location=target_name, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)