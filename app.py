import csv
import os
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'prod_secure_knu_party_session_key_#99201@v!'

PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]).{8,20}$'
)

RAW_EMAIL = "본인의_실제_구글계정@gmail.com"  
RAW_PASSWORD = "xxxx xxxx xxxx xxxx"    

MY_EMAIL = RAW_EMAIL.strip().encode('utf-8').decode('ascii', 'ignore')
MY_PASSWORD = RAW_PASSWORD.replace(" ", "").strip().encode('utf-8').decode('ascii', 'ignore')

verification_store = {}

CSV_FILE = '/home/ubuntu/Haedal_Hackathon/reviews.csv'
USER_FILE = '/home/ubuntu/Haedal_Hackathon/users.csv'
REPORT_FILE = '/home/ubuntu/Haedal_Hackathon/reports.csv'
WISH_FILE = '/home/ubuntu/Haedal_Hackathon/wish.csv'
REVIEW_CLICK_FILE = '/home/ubuntu/Haedal_Hackathon/review_click.csv'

def ensure_file(file_path, header):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow(header)

def append_row(file_path, row):
    with open(file_path, mode='a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(row)

def count_rows_by_user(file_path, user_id):
    count = 0
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) > 0 and row[0] == user_id:
                    count += 1
    return count
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow([
            'writer', 'location', 'name', 'address', 'price', 
            'sunlight', 'pros_cons', 'recommend', 'honey_tip'
        ])

ensure_file(CSV_FILE, ['writer', 'location', 'name', 'address', 'price', 'sunlight', 'pros_cons', 'recommend', 'honey_tip'])
ensure_file(USER_FILE, ['name', 'username', 'password', 'email'])
ensure_file(REPORT_FILE, ['user_id', 'reported_writer', 'review_id', 'reason', 'created_at'])
ensure_file(WISH_FILE, ['user_id', 'review_id', 'created_at'])
ensure_file(REVIEW_CLICK_FILE, ['user_id', 'location', 'created_at'])

# --- 라우트 기능 구현 ---

@app.route('/wish/<review_id>', methods=['POST'])
def wish(review_id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    user_id = session.get('user_id')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(WISH_FILE):
        with open(WISH_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[0] == user_id and row[1] == str(review_id):
                    return "<script>alert('이미 찜한 방입니다.'); history.back();</script>"
    append_row(WISH_FILE, [user_id, review_id, now])
    return "<script>alert('찜한 방에 추가되었습니다.'); history.back();</script>"

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
        elif not student_email.endswith("@knu.ac.kr"):
            error = '경북대 이메일(@knu.ac.kr)로만 가입할 수 있습니다.'
        elif user_pw != user_pw_confirm:
            error = '비밀번호 확인이 일치하지 않습니다.'
        else:
            append_row(USER_FILE, [name, user_id, user_pw, student_email])
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
                for row in reader:
                    if len(row) >= 4 and row[1] == user_id and row[2] == user_pw:
                        session['logged_in'] = True
                        session['user_id'] = user_id
                        session['name'] = row[0]
                        session['email'] = row[3]
                        return redirect(url_for('home'))
        error = '아이디/비번이 틀렸습니다.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def home():
    if not session.get('logged_in'): return redirect(url_for('login'))
    reviews = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            reviews = list(reader)
    user_id = session.get('user_id', '알수없음')
    return render_template('index.html', reviews=reviews,
        wish_count=count_rows_by_user(WISH_FILE, user_id),
        report_count=count_rows_by_user(REPORT_FILE, user_id),
        review_count=count_rows_by_user(REVIEW_CLICK_FILE, user_id))
def write():
    if request.method == 'POST':
        user_email = session.get('email', 'anonymous')
        user_hash = hashlib.sha256(user_email.encode()).hexdigest()[:8]

        row_data = [
            user_hash,
            request.form.get('location', '정보없음'),
            request.form.get('name', '익명'),
            request.form.get('address', '정보없음'),
            request.form.get('price', '정보없음'),
            request.form.get('sunlight', '정보없음'),
            request.form.get('pros_cons', '없음'),
            request.form.get('recommend', '정보없음'),
            request.form.get('honey_tip', '없음')
        ]

        with open('/home/ubuntu/Haedal_Hackathon/reviews.csv', 'a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow(row_data)

        return redirect('/')
    return render_template('write.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json or {}
        if not data:
            return jsonify({"status": "error", "message": "No data"}), 400
        writer_id = session.get('user_id', 'webhook')
        row_data = [writer_id, data.get('location', '정보없음'), data.get('name', '정보없음'), data.get('address', '정보없음'), data.get('price', '정보없음'), data.get('sunlight', '정보없음'), data.get('pros_cons', '정보없음'), data.get('recommend', '정보없음'), data.get('honey_tip', '정보없음')]
        with open('reviews.csv', mode='a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow(row_data) 
        file_path = '/home/ubuntu/Haedal_Hackathon/reviews.csv'
        with open(file_path, mode='a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow(row_data)      
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/location/<name>')
def show_reviews(name):
    if not session.get('logged_in'): return redirect(url_for('login'))
    target_name = name.strip()
    reviews, count = [], 1
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 9 and row[1].strip() == target_name:
                    reviews.append({'id': f"{target_name}_{count}", 'writer': row[0], 'name': row[2], 'address': row[3], 'price': row[4], 'sun': row[5], 'pros_cons': row[6], 'recommend': row[7], 'honey': row[8]})
                    count += 1
    return render_template('reviews.html', location=target_name, reviews=reviews)

@app.route('/report/<review_id>', methods=['POST'])
def report(review_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    try:
        report_file = '/home/ubuntu/Haedal_Hackathon/reports.csv'
        user_id = session.get('user_id', 'anonymous')
        reason = request.form.get('reason', '기타')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. 이미 신고한 게시물인지 중복 확인 로직 (원본의 핵심 기능)
        if os.path.exists(report_file):
            with open(report_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 3 and row[0] == user_id and row[2] == review_id:
                        return "<script>alert('이미 신고한 게시물입니다.'); history.back();</script>"
        reported_writer = "알수없음"
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                count = 1
                for row in reader:
                    if len(row) >= 9:
                        if f"{row[1].strip()}_{count}" == review_id:
                            reported_writer = row[0]
                            break
                        count += 1
        append_row(report_file, [user_id, reported_writer, review_id, reason, now])
        
        return "<script>alert('신고가 접수되었습니다.'); history.back();</script>"
        
    except Exception as e:
        return f"신고 처리 중 오류가 발생했습니다: {str(e)}"

@app.route("/mypage")
def mypage():
    if not session.get('logged_in'): return redirect(url_for('login'))
    user_id = session.get('user_id', '알수없음')
    
    # 1. 리뷰 데이터 가져오기
    all_reviews_dict = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            count = 1
            for row in reader:
                if len(row) >= 9:
                    rev_id = f"{row[1].strip()}_{count}"
                    all_reviews_dict[rev_id] = row
                    count += 1
    
    # 2. 찜 데이터 가져오기
    my_wishes = []
    if os.path.exists(WISH_FILE):
        with open(WISH_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[0] == user_id:
                    rev_info = all_reviews_dict.get(row[1])
                    if rev_info:
                        my_wishes.append({'id': row[1], 'name': rev_info[2]})
                        
    return render_template("mypage.html", my_wishes=my_wishes)

@app.route('/go-review')
def go_review():
    if not session.get('logged_in'): return redirect(url_for('login'))
    user_id = session.get('user_id')
    location = request.args.get('location', 'main').strip()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_row(REVIEW_CLICK_FILE, [session.get('user_id'), request.args.get('location', 'main').strip(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLScVM-U57exhN6qBWZbC28CPulMTfZEmzMRpEb0BrheHHVoiMQ/viewform?usp=header"
    return redirect(google_form_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
