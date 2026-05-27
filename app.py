import csv
import os
import random
import re
import smtplib
from email.mime.text import MIMEText
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'prod_secure_knu_party_session_key_#99201@v!'

CSV_FILE = 'reviews.csv'
USER_FILE = 'users.csv'

PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]).{8,20}$'
)

MY_EMAIL = "자취파티공식계정@gmail.com"  
MY_PASSWORD = "발급받은앱비밀번호"       

verification_store = {}

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
        user_code = request.form.get('code', '').strip()

        if not name or not user_id or not user_pw or not user_pw_confirm or not user_code:
            error = '모든 항목을 입력해주세요.'
            return render_template('register.html', error=error)

        if user_pw != user_pw_confirm:
            error = '비밀번호 확인이 일치하지 않습니다.'
            return render_template('register.html', error=error)

        if not PASSWORD_REGEX.match(user_pw):
            error = '비밀번호는 영문, 숫자, 특수문자를 포함해 8~20자로 입력해주세요.'
            return render_template('register.html', error=error)

        correct_code = verification_store.get(user_id)
        if not correct_code or user_code != correct_code:
            error = '인증코드가 올바르지 않거나 만료되었습니다.'
            return render_template('register.html', error=error)
        
        if user_id in verification_store:
            del verification_store[user_id]

        with open(USER_FILE, mode='a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([name, user_id, user_pw])

        flash('회원가입이 완료되었습니다. 로그인해주세요!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', error=error)


@app.route('/send-code', methods=['POST'])
def send_code():
    student_email = request.form.get('email', '').strip()

    if not student_email.endswith("@knu.ac.kr"):
        return "❌ 경북대 이메일(@knu.ac.kr)만 입력 가능합니다."

    try:
        code = str(random.randint(100000, 999999))
        verification_store[student_email] = code
        
        msg = MIMEText(f"Auth Code: {code}", 'plain', 'us-ascii')
        msg['Subject'] = "KNU Party Verification"
        msg['From'] = MY_EMAIL
        msg['To'] = student_email

        smtp = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        smtp.starttls()
        smtp.login(MY_EMAIL, MY_PASSWORD)
        smtp.sendmail(MY_EMAIL, student_email, msg.as_string())
        smtp.quit()

        return "📩 인증코드를 발송했습니다. 메일함을 확인하세요!"
    except Exception as e:
        return f"❌ 메일 발송 실패 (설정 확인 필요): {str(e)}"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form.get('username', '').strip()
        user_pw = request.form.get('password', '').strip()

        if os.path.exists(USER_FILE):
            with open(USER_FILE, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 3 and row[1] == user_id and row[2] == user_pw:
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
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "로그인이 필요한 서비스입니다."}), 401

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
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("mypage.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)