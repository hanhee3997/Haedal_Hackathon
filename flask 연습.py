# session, redirect, url_for 세 가지를 추가로 불러옵니다.
from flask import Flask, request, jsonify, session, redirect, url_for
import csv
import os

app = Flask(__name__)
# 🔑 로그인을 유지하기 위해 서버에 주는 비밀 암호문입니다.
app.secret_key = 'sunmyeong_secret_key_1234' 

CSV_FILE = 'reviews.csv'

# 엑셀 파일이 없으면 깨끗하게 새로 만듭니다.
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['location', 'sub_location', 'price', 'sunlight', 'review'])

@app.route('/')
def home():
    # ⭐ [로그인 체크] 로그인 안 한 사용자는 로그인 창으로 튕겨냅니다.
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # 🔗 여기에 선명 님의 진짜 구글 폼 주소를 넣어주세요!
    GOOGLE_FORM_URL = "https://docs.google.com/forms/e/1FAIpQLScVM-U57exhN6qBWZbC28CPulMTfZEmzMRpEb0BrheHHVoiMQ/viewform?usp=header"
    
    return f"""
    <div style="text-align:center; padding:40px 20px; font-family: sans-serif; max-width: 600px; margin: 0 auto;">
        <h1>🏠 우리 학교 자취방 찐 후기 모음</h1>
        <p style="color: #666;">원하는 구역을 선택해 학생들의 거주 후기를 확인하세요.</p>
        
        <div style="margin: 30px 0 20px 0;">
            <a href="{GOOGLE_FORM_URL}" target="_blank" style="text-decoration: none;">
                <button style="padding: 18px 40px; font-size: 18px; font-weight: bold; color: white; background: #007bff; border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,123,255,0.2); transition: all 0.2s;">
                    ✍️ 내 자취방 후기 작성하러 가기
                </button>
            </a>
        </div>
        
        <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;">
        
        <p style="font-weight: bold; text-align: left; margin-left: 10px; color: #333;">📍 구역별 후기 보기</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <a href="/location/쪽문" style="text-decoration:none;"><button style="width:100%; padding:15px; font-size:16px; cursor:pointer; border-radius:8px; border:1px solid #ddd; background:#f9f9f9;">🚪 쪽문 후기</button></a>
            <a href="/location/정문" style="text-decoration:none;"><button style="width:100%; padding:15px; font-size:16px; cursor:pointer; border-radius:8px; border:1px solid #ddd; background:#f9f9f9;">🏫 정문 후기</button></a>
            <a href="/location/북문" style="text-decoration:none;"><button style="width:100%; padding:15px; font-size:16px; cursor:pointer; border-radius:8px; border:1px solid #ddd; background:#f9f9f9;">🏢 북문 후기</button></a>
            <a href="/location/서문" style="text-decoration:none;"><button style="width:100%; padding:15px; font-size:16px; cursor:pointer; border-radius:8px; border:1px solid #ddd; background:#f9f9f9;">🌾 서문 후기</button></a>
        </div>
    </div>
    """
# ---------------- 여기를 복사해서 @app.route('/') 바로 위에 넣으세요 ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('username')
        user_pw = request.form.get('password')
        
        # 선명 님이 지정한 아이디(admin)와 비밀번호(1234)
        if user_id == 'admin' and user_pw == '1234':
            session['logged_in'] = True
            return redirect(url_for('home'))  # 로그인 성공하면 메인 홈으로 이동
        else:
            return "<h2>비밀번호가 틀렸습니다.</h2><a href='/login'>다시 시도</a>"
            
    # 주소창에 /login을 쳐서 들어왔을 때 보여주는 로그인 화면창
    return '''
    <div style="text-align:center; margin-top:100px; font-family: sans-serif;">
        <form method="POST" style="display:inline-block; padding:40px; border:1px solid #ddd; border-radius:10px; background:#f9f9f9;">
            <h2>🏠 자취방 후기 로그인</h2>
            <input type="text" name="username" placeholder="아이디" style="padding:10px; width:200px; margin-bottom:10px;" required><br>
            <input type="password" name="password" placeholder="비밀번호" style="padding:10px; width:200px; margin-bottom:15px;" required><br>
            <button type="submit" style="padding:10px 40px; background:#007bff; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">로그인</button>
        </form>
    </div>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # 로그인 기록을 완전히 삭제
    return redirect(url_for('login'))  # 로그아웃 후 로그인창으로 이동


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    print("\n[🚨 구글 데이터 수신 원본]:", data)
    
    # 💡 키 이름 억까 방지: 구글이 보낸 순수 값만 순서대로 리스트로 뽑아냅니다.
    values = list(data.values())
    
    # 기본값 세팅
    loc, sub_loc, price, sun, rev = '미정', '미정', '정보없음', '정보없음', '내용없음'
    
    # ⭐ [핵심 수정] 구글 폼의 답변들이 엑셀의 제자리에 쏙쏙 들어가도록 순서를 완벽 고정했습니다!
    try:
        if len(values) >= 1: loc = str(values[0]).strip()     # 1번째: 구역 (쪽문, 정문, 북문 등)
        if len(values) >= 2: sub_loc = str(values[1]).strip() # 2번째: 상세 위치
        if len(values) >= 3: price = str(values[2]).strip()   # 3번째: 가격
        if len(values) >= 4: sun = str(values[3]).strip()     # 4번째: 채광
        if len(values) >= 5: rev = str(values[4]).strip()     # 5번째: 후기 내용
    except Exception as e:
        print(f"데이터 파싱 중 에러 발생: {e}")

    # 엑셀 파일에 안전하게 한 줄 저장
    with open(CSV_FILE, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([loc, sub_loc, price, sun, rev])
        
    print(f"🎯 [엑셀 저장 완벽 성공] -> 구역: {loc} | 상세위치: {sub_loc}\n")
    return jsonify({"status": "success"}), 200

@app.route('/location/<name>')
def show_reviews(name):
    target_name = name.strip()
    reviews = []
    
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # 첫 줄 제목행 패스
            for row in reader:
                if len(row) >= 5:
                    # 엑셀의 0번째 칸(구역)과 클릭한 버튼 이름이 맞으면 웹 리스트에 추가
                    if row[0].strip() == target_name:
                        reviews.append({
                            'sub_location': row[1].strip(),
                            'price': row[2].strip(),
                            'sunlight': row[3].strip(),
                            'review': row[4].strip()
                        })
                
    html = f"<div style='padding:30px; font-family: sans-serif;'><h1>📍 {target_name} 구역 후기</h1><a href='/' style='text-decoration:none; color:#007bff;'>← 메인으로 돌아가기</a><hr style='border: 0; height: 1px; background: #ccc; margin: 20px 0;'>"
    
    if not reviews:
        html += "<p style='color:#666;'>아직 등록된 후기가 없습니다. 구글 폼으로 첫 번째 후기를 남겨보세요!</p>"
        
    for r in reviews:
        html += f"""
        <div style="border:1px solid #ddd; margin-bottom:15px; padding:20px; border-radius:10px; background:#fbfbfb; max-width:600px;">
            <p style="margin:5px 0; color:#555;">📍 <b>상세 위치:</b> <span style="background:#e9ecef; padding:2px 6px; border-radius:4px;">{r['sub_location']}</span></p>
            <p style="margin:5px 0;">💰 <b>가격:</b> {r['price']}</p>
            <p style="margin:5px 0;">☀️ <b>채광:</b> {r['sunlight']}</p>
            <p style="margin:10px 0 0 0; padding-top:10px; border-top:1px dashed #eee;">💬 <b>후기:</b> {r['review']}</p>
        </div>
        """
    html += "</div>"
    return html

if __name__ == '__main__':
    app.run(debug=True)