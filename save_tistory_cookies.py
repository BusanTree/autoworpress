from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time

"""
티스토리 쿠키 저장 스크립트
--------------------------
사용 방법:
1. 이 스크립트를 실행하세요: python save_tistory_cookies.py
2. 브라우저가 열리면 티스토리에 직접 로그인하세요
3. 로그인 완료 후 60초 동안 대기합니다
4. 쿠키가 자동으로 저장됩니다
"""

print("=" * 60)
print("🍪 티스토리 쿠키 저장 스크립트")
print("=" * 60)

# Chrome 브라우저 실행
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# 티스토리 메인 페이지로 이동
print("\n1️⃣ 티스토리 페이지를 엽니다...")
driver.get("https://www.tistory.com")
time.sleep(2)

# 사용자가 수동으로 로그인할 수 있도록 대기
print("\n2️⃣ 이제 브라우저에서 티스토리에 로그인하세요!")
print("   - 카카오, 구글 등 원하는 방법으로 로그인하세요")
print("   - 로그인이 완료되면 60초 후 자동으로 쿠키를 저장합니다\n")

# 60초 카운트다운
for i in range(60, 0, -10):
    print(f"⏱️  {i}초 후에 쿠키를 저장합니다... (로그인을 완료해주세요)")
    time.sleep(10)

# 쿠키 저장
print("\n3️⃣ 쿠키를 저장하는 중...")
cookies = driver.get_cookies()
pickle.dump(cookies, open("tistory_cookies.pkl", "wb"))
print("✅ 쿠키 저장 완료! (파일: tistory_cookies.pkl)")

print("\n" + "=" * 60)
print("🎉 성공! 이제 finance_bot.py를 실행하면 자동 로그인이 됩니다.")
print("=" * 60)

# 브라우저는 닫지 않음 (사용자가 확인할 수 있도록)
print("\n⚠️  브라우저를 직접 닫아주세요.")
