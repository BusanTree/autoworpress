import pickle
import base64

# 쿠키 파일 읽기
try:
    with open("tistory_cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
        
    # Base64 문자열로 변환
    cookie_b64 = base64.b64encode(pickle.dumps(cookies)).decode('utf-8')
    
    print("✅ 쿠키 변환 성공! 아래 문자열 전체를 복사하세요:")
    print("-" * 50)
    print(cookie_b64)
    print("-" * 50)
    print("👉 이 값을 GitHub Repository Settings > Secrets > Actions에 'TISTORY_COOKIES_B64' 라는 이름으로 추가하세요.")
    
except FileNotFoundError:
    print("❌ 'tistory_cookies.pkl' 파일이 없습니다. 먼저 로그인을 진행해주세요.")
