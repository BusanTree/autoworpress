from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException # 👈 예외 처리 추가
import time
import pyperclip

# 1. 디버깅 크롬 연결
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

# 2. 글쓰기 페이지 이동
blog_name = "techeverything" 
write_url = f"https://{blog_name}.tistory.com/manage/post"
driver.get(write_url)

# ==========================================
# 🚨 [추가된 부분] "저장된 글 불러올까요?" 알림 처리
# ==========================================
try:
    # 알림창이 뜰 때까지 아주 잠깐 기다려봅니다.
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(f"⚠️ 알림 발견: {alert.text}")
    alert.dismiss() # '취소'를 눌러서 새로 씁니다. ('확인'은 alert.accept())
    print("✅ 알림을 닫았습니다 (새 글 작성).")
except TimeoutException:
    print("✅ 알림 없음, 바로 작성 시작.")
except Exception as e:
    print(f"⚠️ 알림 처리 중 특이사항: {e}")
# ==========================================

# 3. 제목 입력 함수
def input_text(element_xpath, text):
    pyperclip.copy(text)
    driver.find_element(By.XPATH, element_xpath).click()
    driver.find_element(By.XPATH, element_xpath).send_keys(Keys.CONTROL, 'v')
    time.sleep(0.5)

try:
    # --- 제목 입력 ---
    print("📝 페이지 로딩 및 제목 대기 중...")
    title_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="post-title-inp"]'))
    )
    
    print("📝 제목 작성 중...")
    input_text('//*[@id="post-title-inp"]', "[자동 포스팅] 쉐보레 크루즈 뉴스 요약")

    # --- 본문 입력 ---
    print("📝 본문 에디터 진입 시도...")

    # 1. iframe 찾기 및 진입
    driver.switch_to.default_content() 
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "editor-tistory_ifr"))
        )
        print("✅ 에디터(iframe) 진입 성공!")
    except:
        print("⚠️ ID로 실패, 태그로 재시도...")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
        )

    # 2. 본문 영역(tinymce) 찾기
    body_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tinymce"))
    )
    body_area.click()
    time.sleep(0.5)

    # 3. 내용 입력
    content = "안녕하세요.\n\n알림창도 닫을 줄 아는 똑똑한 봇입니다.\n성공 확인!"
    pyperclip.copy(content)
    body_area.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)

    # 4. 메인으로 복귀
    driver.switch_to.default_content()

    # --- 발행 버튼 클릭 (임시저장) ---
    print("💾 임시 저장 버튼 찾는 중...")
    finish_layer_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#publish-layer-btn'))
    )
    finish_layer_btn.click()
    
    print("✅ 테스트 완료! 화면을 확인하세요.")

except Exception as e:
    print(f"❌ 오류 발생: {e}")