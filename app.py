from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
import csv
import os
import re

app = Flask(__name__)
app.secret_key = 'sunmyeong_secret_key_1234'
CSV_FILE = 'reviews.csv'
USER_FILE = 'users.csv'
PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]).{8,20}$'
)

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(['location', 'sub_location', 'price', 'sunlight', 'review'])

if not os.path.exists(USER_FILE):
    with open(USER_FILE, mode='w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(['name', 'username', 'password'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        user_id = request.form.get('username', '').strip()
        user_pw = request.form.get('password', '').strip()
        user_pw_confirm = request.form.get('password_confirm', '').strip()

        if not name or not user_id or not user_pw or not user_pw_confirm:
            error = '모든 항목을 입력해주세요.'
            return render_template('register.html', error=error)

        if user_pw != user_pw_confirm:
            error = '비밀번호 확인이 일치하지 않습니다.'
            return render_template('register.html', error=error)

        if not PASSWORD_REGEX.match(user_pw):
            error = '비밀번호는 영문, 숫자, 특수문자를 포함해 8~20자로 입력해주세요.'
            return render_template('register.html', error=error)

        with open(USER_FILE, mode='a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([name, user_id, user_pw])

        flash('회원가입이 완료되었습니다. 로그인해주세요!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        user_id = request.form.get('username').strip()
        user_pw = request.form.get('password').strip()

        with open(USER_FILE, mode='r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row and row[1] == user_id and row[2] == user_pw:
                    session['logged_in'] = True
                    return redirect(url_for('home'))

        error = '아이디/비번이 틀렸습니다.'

    return render_template('login.html', error=error)

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

@app.route("/mypage")
def mypage():
    return render_template("mypage.html")

if __name__ == '__main__':
    app.run(debug=True)