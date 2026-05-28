import csv
import os
import random
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'prod_secure_knu_party_session_key_#99201@v!'

CSV_FILE = 'reviews.csv'
USER_FILE = 'users.csv'

PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]).{8,20}$'
)

RAW_EMAIL = "본인의_실제_구글계정@gmail.com"  
RAW_PASSWORD = "xxxx xxxx xxxx xxxx"     

MY_EMAIL = RAW_EMAIL.strip().encode('utf-8').decode('ascii', 'ignore')
MY_PASSWORD = RAW_PASSWORD.replace(" ", "").strip().encode('utf-8').decode('ascii', 'ignore')

verification_store = {}

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(['location', 'name', 'address', 'price', 'sunlight', 'pros_cons', 'recommend', 'honey_tip'])

if not os.path.exists(USER_FILE):
    with open(USER_FILE, mode='w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(['name', 'username', 'password', 'email'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        user_id = request.form.get('username', '').strip()
        student_email = request.form.get('email', '').strip()
        user_pw = request.form.get('password', '').strip()
        user_pw_confirm = request.form.get('password_confirm', '').strip()


        if not name or not user_id or not student_email or not user_pw or not user_pw_confirm:
            error = '모든 항목을 입력해주세요.'
            return render_template('register.html', error=error)

  
        if not student_email.endswith("@knu.ac.kr"):
            error = '경북대 이메일(@knu.ac.kr)로만 가입할 수 있습니다.'
            return render_template('register.html', error=error)

  
        if user_pw != user_pw_confirm:
            error = '비밀번호 확인이 일치하지 않습니다.'
            return render_template('register.html', error=error)

   
        with open(USER_FILE, mode='a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([name, user_id, user_pw, student_email])

        flash('회원가입이 완료되었습니다. 로그인해주세요!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', error=error)

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
                for idx, row in enumerate(reader):
                    if len(row) >= 3 and row[1] == user_id and row[2] == user_pw:
                        if len(row) >= 3 and row[1] == user_id and row[2] == user_pw:
                            session['logged_in'] = True
                            session['user_id'] = user_id  
                            session['name'] = row[0]      
                            return redirect(url_for('home'))
        error = '아이디/비번이 틀렸습니다.'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login'))


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    my_review_count = 0
    if os.path.exists('reviews.csv'):
        with open('reviews.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                my_review_count += 1

    return render_template('index.html', review_count=my_review_count)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    
    row_data = [
        data.get('location', '정보없음'),
        data.get('name', '정보없음'),
        data.get('address', '정보없음'),
        data.get('price', '정보없음'),
        data.get('sunlight', '정보없음'),
        data.get('pros_cons', '정보없음'),
        data.get('recommend', '정보없음'),
        data.get('honey_tip', '정보없음')
    ]
    
    
    with open('reviews.csv', mode='a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(row_data)
        
    return jsonify({"status": "success"}), 200
        
    


@app.route('/location/<name>')
def show_reviews(name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    target_name = name.strip()
    reviews = []
    count=1
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None) # 헤더 건너뜀
            for row in reader:
                # 💡 인덱스를 8개 항목에 맞게 수정!
                if len(row) >= 8 and row[0].strip() == target_name:
                    reviews.append({
                        'id': count,
                        'name': row[1],        # 자취방 이름
                        'address': row[2],     # 주소
                        'price': row[3],       # 가격
                        'sun': row[4],         # 채광
                        'pros_cons': row[5],   # 장단점
                        'recommend': row[6],   # 추천여부
                        'honey': row[7]        # 꿀팁
                    })
                    count+=1
    return render_template('reviews.html', location=target_name, reviews=reviews)

@app.route("/mypage")
def mypage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_name = session.get('name', '사용자')
    user_id = session.get('user_id', '알수없음')
    
    review_count = 0
    if os.path.exists('reviews.csv'):
        with open('reviews.csv', mode='r', encoding='utf-8') as f:
            review_count = len(list(csv.reader(f))) - 1 
    
    return render_template("mypage.html", 
                           name=user_name, 
                           id=user_id, 
                           review_count=review_count)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
