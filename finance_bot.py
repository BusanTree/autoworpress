from google import genai
import feedparser
import urllib.parse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pyperclip
import pickle

# ==========================================
# 👇 [설정] 여기에 API 키를 넣으세요!
# ==========================================
GEMINI_API_KEY = "AIzaSyAWFMfczRNM0nKGwCxR1-edck8caG5osG4"
BLOG_NAME = "techeverything" 

# Gemini 연결
client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# 1. 금융 뉴스 수집 (RSS)
# ==========================================
def get_finance_news():
    print("🔍 오늘의 금융 뉴스를 수집합니다...")
    keywords = ["미국 증시", "FOMC", "연준 금리", "환율 전망"]
    news_data = []

    for keyword in keywords:
        encoded = urllib.parse.quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        
        # 키워드당 상위 3개 뉴스 수집 (정보량 증가)
        if feed.entries:
            for i, entry in enumerate(feed.entries[:3], 1):
                news_data.append(f"[{keyword} - 뉴스 #{i}]\n- 제목: {entry.title}\n- 링크: {entry.link}")
    
    return "\n\n".join(news_data)

# ==========================================
# 2. Gemini Pro로 SEO 최적화된 제목과 본문 작성
# ==========================================
def generate_blog_content(news_text):
    print("🧠 Gemini가 '쉽고 깊이 있는' 금융 분석 콘텐츠를 작성합니다...")
    
    # 초보자 친화적 심층 분석 프롬프트
    prompt = f"""
    당신은 **'세계 금융·경제의 모든 것'** 블로그의 전문 작가입니다.
    복잡한 금융 뉴스를 **쉽게 풀어내면서도 깊이 있게** 분석하는 것이 당신의 강점입니다.
    초보자도 이해할 수 있으면서, 전문성은 잃지 않는 분석을 작성하세요.

    [SEO 최적화 제목 작성 가이드]
    1. **검색 키워드 포함**: "미국 증시", "FOMC", "금리", "환율", "주식 전망" 등 핵심 키워드 필수
    2. **클릭 유도**: 숫자, 구체적 정보, 시급성으로 클릭률 향상
       예: "미국 증시 3% 급등! FOMC 금리 동결이 만든 5가지 투자 기회"
    3. **적절한 길이**: 30~60자
    4. **날짜 제외**: 검색 효율 향상
    5. **감정 자극**: "급등", "급락", "주목", "전망", "분석", "충격" 등 활용

    [본문 작성 - 쉽고 깊이 있는 분석]
    
    **1. HTML 태그 전략적 사용**
       - 소제목: <h3> (SEO 중요)
       - 강조 키워드: <b> (검색엔진 인식)
       - 목록: <ul>, <li>
       - 문단: <br> (2줄 간격)
       - 링크: <a href="URL" target="_blank" rel="noopener">텍스트</a>

    **2. 초보자도 이해 가능한 쉬운 설명 (매우 중요!)**
       - 전문 용어는 반드시 쉽게 풀어 설명
         예: "FOMC(연방공개시장위원회)는 미국 중앙은행이 금리를 결정하는 회의입니다"
       - 비유와 예시를 적극 활용
         예: "금리 인상은 마치 브레이크를 밟는 것과 같아요"
       - 일상 언어로 풀어쓰기
         ✅ 좋은 예: "금리가 오르면 대출 이자가 비싸져서, 사람들이 돈을 덜 빌리게 됩니다"
         ❌ 나쁜 예: "긴축 통화정책으로 유동성이 감소합니다"

    **3. 각 섹션별 최소 분량 및 깊이**
       - **각 뉴스 분석: 최소 250자 이상**
       - 반드시 포함할 내용:
         * 무슨 일이 일어났나요? (What) - 쉽게 설명
         * 왜 중요한가요? (Why) - 배경 맥락을 쉽게
         * 나에게 어떤 영향이 있나요? (Impact) - 일반인 관점
         * 전문가 시각 (Insight) - 깊이 있되 이해하기 쉽게

    **4. 구체성과 친근함**
       ✅ 좋은 예: "S&P500 지수가 전일보다 2.3% 올라 4,782포인트로 마감했어요. 
                   특히 애플, 마이크로소프트 같은 기술주가 3% 이상 올랐는데요,
                   이는 지난 7월 이후 가장 큰 상승폭이랍니다."
       
       ❌ 나쁜 예: "S&P500 지수의 상승세가 두드러졌다."

    **5. Few-Shot 예시 - 이 수준으로 작성하세요**
    
    예시 분석:
    "<h3>💰 FOMC 금리 동결, 무슨 의미일까요?</h3>
    미국 연방준비제도(연준)가 이번에 금리를 그대로 동결했어요. '금리 동결'이 뭐냐고요? 
    쉽게 말하면 <b>은행 이자율을 올리지도 내리지도 않고 그대로 유지</b>한다는 뜻이에요.<br><br>
    
    그런데 이게 단순히 '현상 유지'만은 아니에요. 연준의 파월 의장은 기자회견에서 
    '앞으로 나올 경제 지표를 보고 결정하겠다'고 했는데요, 특히 <b>2월 고용지표</b>가 
    핵심 변수가 될 것 같아요.<br><br>
    
    역사적으로 금리를 동결한 뒤 3개월 동안 미국 S&P500 지수는 평균 <b>4.2% 올랐어요</b>. 
    하지만 현재 시장은 이미 이 기대감을 절반 이상 반영한 상태라서, 
    <b>단기적으로는 약간 조정받을 수 있고, 중장기적으로는 계속 오를 가능성</b>이 있답니다.<br><br>
    
    특히 주목할 건 <b>반도체와 AI 관련 주식</b>이에요. 엔비디아, AMD 같은 회사들이 
    5% 이상 급등했는데, 금리 부담이 줄어들면서 AI 투자가 계속될 거란 기대감 때문이에요."

    **6. 글의 구조 (총 2,500자 이상 목표)**
       - **[🚀 오프닝]** (100-150자): 
         * 친근하고 흥미로운 시작
         * 예시: "🚀 오프닝<br>
                  미국 증시, FOMC, 금리, 환율… 뉴스에서 많이 들어봤지만 어렵게 느껴지시죠? 
                  '세계 금융·경제의 모든 것' 블로그가 핵심만 쉽게 정리해드릴게요!"
         * 절대 거짓 경력(예: 월스트리트 10년) 언급하지 마세요!
         
       - **[📊 3줄 요약]** (150자): 바쁜 독자용
       
       - **[📰 주요 뉴스 쉽게 풀어보기]** (1,800자): 
         * 각 뉴스별 <h3> 소제목 (이모지 포함)
         * 최소 250자 이상의 쉬운 설명
         * 전문 용어는 풀어서 설명
         * 일상 언어 사용
         
       - **[💡 투자 전략 정리]** (300자):
         * 단기/중기/장기 관점
         * 어떤 섹터가 좋을지 쉽게 설명
         * 위험 요소도 알려주기
         
       - **[📰 참고 뉴스]** (필수): 
         * 모든 뉴스 링크를 <ul><li> 목록으로
         * <a> 태그로 클릭 가능하게
         
       - **[👋 클로징]** (50자): "다음에도 쉽고 유익한 정보로 찾아올게요!"

    **7. 말투 및 스타일**
       - "해요체" 사용
       - 친근하고 대화하듯이
       - 전문성은 유지하되, 교육적이고 이해하기 쉽게
       - 독자를 존중하는 톤

    **8. 키워드 SEO 전략**
       - 핵심 키워드 5~7회 자연스럽게 반복
       - <b> 태그로 강조

    [오늘의 뉴스 데이터 - 총 12개]
    {news_text}
    
    [출력 형식]
    반드시 다음 JSON 형식으로 출력:
    {{{{
        "title": "SEO 최적화된 클릭 유도 제목 (30-60자)",
        "content": "초보자도 이해하기 쉬운 HTML 본문 (2,500자 이상)"
    }}}}
    
    **중요**: 
    1. 전문 용어는 반드시 쉽게 풀어 설명하세요!
    2. 거짓 경력(월스트리트 10년 등)을 절대 언급하지 마세요!
    3. '세계 금융·경제의 모든 것' 블로그 정체성을 반영하세요!
    """

    # Gemini 2.0 Flash 모델로 고품질 콘텐츠 생성
    # 프롬프트와 파라미터 최적화로 품질 대폭 향상
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',  # 안정적이고 빠른 모델
        contents=prompt,
        config={
            'temperature': 0.9,  # 창의성 최대화
            'max_output_tokens': 8000,  # 긴 심층 분석 가능
        }
    )
    
    return response.text

# ==========================================
# 3. 티스토리 자동 포스팅 (기존과 동일)
# ==========================================
# ==========================================
# 3. 티스토리 자동 포스팅 (수정판: 팝업 방어 + 브라우저 유지)
# ==========================================
def post_to_tistory(title, content):
    print("🚀 티스토리에 접속합니다... (브라우저 실행)")

    chrome_options = Options()
    
    # [중요] 서버 환경(GitHub Actions)인지 확인하는 로직
    # os.environ.get('GITHUB_ACTIONS')가 'true'면 Headless 모드 실행
    import os
    is_github_action = os.environ.get('GITHUB_ACTIONS') == 'true'
    
    if is_github_action:
        print("🤖 GitHub Actions 환경 감지: Headless 모드로 실행합니다.")
        chrome_options.add_argument("--headless=new") # 화면 없이 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # 봇 탐지 회피를 위한 User-Agent 설정
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    else:
        # 로컬 환경
        chrome_options.add_experimental_option("detach", True) 

    driver = webdriver.Chrome(options=chrome_options)
    
    # 1. 쿠키 심기
    print("🍪 로그인 정보(쿠키)를 심는 중...")
    driver.get("https://www.tistory.com") 
    time.sleep(3)
    
    try:
        # GitHub Actions에서는 환경 변수에서 쿠키를 읽어옴 (파일이 없으므로)
        if is_github_action:
            import base64
            cookie_b64 = os.environ.get('TISTORY_COOKIES_B64')
            if cookie_b64:
                print("📂 환경 변수에서 쿠키 로드 중...")
                cookies = pickle.loads(base64.b64decode(cookie_b64))
            else:
                raise Exception("GitHub Secrets에 'TISTORY_COOKIES_B64'가 없습니다.")
        else:
            # 로컬 파일에서 로드
            cookies = pickle.load(open("tistory_cookies.pkl", "rb"))
            
        for cookie in cookies:
            # 쿠키 도메인 호환성 처리
            if 'expiry' in cookie:
                del cookie['expiry'] # 만료 시간 삭제 (오류 방지)
            driver.add_cookie(cookie)
        print("✅ 쿠키 로드 완료!")
    except Exception as e:
        print("❌ 쿠키 로드 실패:", e)
        return

    # 2. 새로고침 (로그인 적용) 및 글쓰기 이동
    driver.refresh()
    time.sleep(3)
    
    # 글쓰기 페이지 URL (manage/post가 아니라 manage/newpost 권장)
    write_url = "https://techeverything.tistory.com/manage/newpost" 
    driver.get(write_url)
    time.sleep(5) # 로딩 대기

    # [중요] 로그인 성공 여부 확인 (URL 체크)
    current_url = driver.current_url
    print(f"📍 현재 URL: {current_url}")
    
    if "login" in current_url or "auth" in current_url:
        print("❌ 로그인 실패! (로그인 페이지로 리다이렉트됨)")
        print("💡 원인: GitHub Actions IP(해외) 차단 또는 쿠키 만료")
        print("👉 해결책: 티스토리 설정 > '해외 로그인 차단' 해제 필요")
        # 여기서 강제로 에러를 내야 Actions가 '실패'로 뜸
        import sys
        sys.exit(1)
        
    if "manage" not in current_url:
        print(f"⚠️ 경고: 예상치 못한 페이지입니다. 글쓰기가 불가능할 수 있습니다.")

    # 🚨 [핵심] 팝업창(Alert) 무조건 닫기 (강력한 방어막)
    try:
        print("🛡️ 팝업창이 있는지 확인 중...")
        # 3초 동안 팝업이 뜨는지 감시하다가, 뜨면 즉시 닫아버림
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"⚠️ 팝업 발견: {alert.text}")
        alert.dismiss() # '취소' 클릭 (새 글 쓰기)
        print("✅ 팝업 제거 완료")
    except TimeoutException:
        print("✅ 팝업 없음, 통과")
    except Exception as e:
        print(f"⚠️ 팝업 처리 중 특이사항: {e}")

    # 3. 제목 입력
    print("📝 제목 입력 중...")
    title_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="post-title-inp"]'))
    )
    title_area.click() # 클릭 먼저 하고
    time.sleep(0.5)
    pyperclip.copy(title)
    title_area.send_keys(Keys.CONTROL, 'v')

    # 4. HTML 모드로 본문 입력 (강력한 검증 및 재시도 로직)
    print("📝 본문(HTML) 입력 시도...")
    
    for attempt in range(1, 4):  # 최대 3번 시도
        try:
            driver.switch_to.default_content()
            # 에디터 iframe 찾기 (모든 가능성 열어두기)
            try:
                WebDriverWait(driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe#editor-tistory_ifr, iframe.tox-edit-area__iframe'))
                )
            except:
                # 못 찾으면 첫 번째 iframe으로 시도
                driver.switch_to.default_content()
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                if len(frames) > 0:
                    driver.switch_to.frame(frames[0])
            
            # 본문 요소 찾기
            body_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce, body"))
            )
            
            # [핵심 수정] 에디터가 변경을 감지하도록 입력 방식 개선
            print(f"⌨️ 본문 입력 중... (시도 {attempt}/3)")
            
            # 1. 포커스 주기
            driver.execute_script("arguments[0].focus();", body_element)
            time.sleep(1)
            
            # 2. 브라우저 명령어로 HTML 삽입 (이게 사람이 붙여넣기 한 것처럼 동작함)
            driver.execute_script("document.execCommand('insertHTML', false, arguments[0]);", content)
            time.sleep(1)
            
            # 3. [중요] 키보드 입력 시늉을 해서 에디터의 '변경 감지' 트리거
            body_element.send_keys(".") 
            body_element.send_keys(Keys.BACK_SPACE) # 점 찍고 지우기
            
            time.sleep(2)
            
            # [검증] 내용이 진짜 들어갔는지 확인
            current_content = body_element.get_attribute('innerHTML')
            # 태그 포함 길이가 충분한지 확인
            if len(current_content) > 200: 
                print(f"✅ 본문 입력 성공! (길이: {len(current_content)})")
                break
            else:
                print(f"⚠️ 본문 입력 실패 (내용 누락), 재시도... ({attempt}/3)")
        
        except Exception as e:
            print(f"⚠️ 본문 입력 중 에러: {e}, 재시도... ({attempt}/3)")
            time.sleep(3)
    
    driver.switch_to.default_content() # 메인으로 복귀
    time.sleep(2)

    # 5. 발행 준비 (팝업 열기)
    print("📤 발행 준비 중...")
    try:
        publish_layer_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#publish-layer-btn'))
        )
        publish_layer_btn.click()
    except:
        # 혹시 버튼이 안 눌리면 JS로 강제 클릭
        driver.execute_script("document.getElementById('publish-layer-btn').click();")
    
    time.sleep(3)  # 팝업 로딩 대기
    
    # 6. 공개 설정 및 카테고리 (가장 중요)
    try:
        print("⚙️ 발행 설정 적용 중...")
        
        # [공개 설정] "공개" 라디오 버튼 클릭
        try:
            # id="open20" 또는 라디오 버튼 value="3" (공개)
            open_radio = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="radio"][id="open20"], label[for="open20"]'))
            )
            open_radio.click()
            print("✅ '공개' 설정 완료")
        except Exception as e:
            print(f"⚠️ 공개 설정 실패 (JS 시도): {e}")
            driver.execute_script("document.getElementById('open20').click();")

        time.sleep(1)

        # [카테고리] '금융·경제 뉴스' 선택
        print("📂 카테고리 설정 중...")
        try:
            # 1. SelectBox 찾기
            category_select = driver.find_element(By.ID, "category")
            
            # 2. '금융·경제 뉴스' 옵션 찾아서 값 가져오기
            options = category_select.find_elements(By.TAG_NAME, "option")
            target_value = ""
            for option in options:
                # 텍스트에 '금융'이나 '경제'가 포함된 옵션 찾기 (공백 제거 후 비교)
                opt_text = option.text.strip()
                if "금융" in opt_text or "경제" in opt_text:
                    target_value = option.get_attribute("value")
                    print(f"👉 카테고리 찾음: {opt_text} (ID: {target_value})")
                    break
            
            if target_value:
                # 3. JS로 값 강제 변경 및 이벤트 발생 (가장 확실)
                driver.execute_script(f"""
                    var select = document.getElementById('category');
                    select.value = '{target_value}';
                    select.dispatchEvent(new Event('change'));
                """)
                print("✅ 카테고리 선택 완료 (JS 강제 적용)")
            else:
                print("⚠️ '금융' 또는 '경제' 카테고리를 찾지 못했습니다. (기본값 유지)")
                
        except Exception as e:
            print(f"⚠️ 카테고리 설정 실패: {e}")

    except Exception as e:
        print(f"⚠️ 설정 적용 중 에러: {e}")

    time.sleep(2)

    # 7. 최종 발행 버튼 클릭
    print("🚀 자동 발행 시도 중...")
    published = False
    
    # 방법 1: ID로 찾기
    try:
        final_publish_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, 'publish-btn'))
        )
        final_publish_btn.click()
        published = True
        print("✅ 포스팅 완료! (방법 1: ID)")
    except:
        pass
    
    # 방법 2: 클래스명으로 찾기
    if not published:
        try:
            final_publish_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_publish, .publish-btn, button.confirm'))
            )
            final_publish_btn.click()
            published = True
            print("✅ 포스팅 완료! (방법 2: 클래스)")
        except:
            pass
    
    # 방법 3: XPath로 텍스트 기반 찾기
    if not published:
        try:
            final_publish_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(., "발행")]'))
            )
            final_publish_btn.click()
            published = True
            print("✅ 포스팅 완료! (방법 3: XPath)")
        except:
            pass
    
    # 방법 4: CSS 선택자로 팝업 내 버튼 찾기
    if not published:
        try:
            final_publish_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#publishLayer button[type="button"].btn_confirm'))
            )
            final_publish_btn.click()
            published = True
            print("✅ 포스팅 완료! (방법 4: CSS)")
        except:
            pass
    
    if not published:
        print("⚠️ 자동 발행 실패 - 임시저장 상태입니다. 수동으로 발행해주세요.")
    
    time.sleep(5)  # 발행 완료 확인 대기

if __name__ == "__main__":
    import json
    import re
    
    try:
        # 1. 뉴스 수집
        raw_news = get_finance_news()
        
        # 2. AI로 제목과 본문 생성
        ai_response = generate_blog_content(raw_news)
        
        # [디버깅] AI 응답 길이 확인
        print(f"🤖 AI 응답 길이: {len(ai_response)}자")
        
        # 3. 제목/본문 추출 로직 (강력하게 수정)
        blog_title = ""
        blog_content = ""

        # 1) JSON 정규식 추출 시도
        try:
            title_match = re.search(r'"title"\s*:\s*"(.*?)"', ai_response, re.DOTALL)
            content_match = re.search(r'"content"\s*:\s*"(.*?)"', ai_response, re.DOTALL)
            
            if title_match and content_match:
                blog_title = title_match.group(1)
                blog_content = content_match.group(1)
                # 이스케이프 문자 등 정리
                blog_content = blog_content.replace('\\n', '\n').replace('\\"', '"')
                print(f"\n📌 제목 추출 성공: {blog_title}\n")
            else:
                raise Exception("정규식 패턴 매칭 실패")
        except Exception:
            # 2) 실패 시 수동 생성
            print("⚠️ 제목/본문 분리 실패 → 수동 생성 모드")
            today_str = datetime.now().strftime("%m월 %d일")
            blog_title = f"[{today_str}] 오늘의 글로벌 금융 시장 심층 분석"
            
            # 본문에서 JSON 기호 제거하고 그대로 사용
            blog_content = ai_response.replace('```json', '').replace('```', '').strip()
            # 혹시나 앞부분에 title 키가 남아있으면 제거 시도
            if '"content":' in blog_content:
                blog_content = blog_content.split('"content":')[-1].strip().strip('"}')

        # [안전장치] 본문이 너무 짧으면 경고
        if len(blog_content) < 500:
            print(f"⚠️ 경고: 본문 내용이 너무 짧습니다 ({len(blog_content)}자). 뉴스 데이터가 부족하거나 AI 응답이 잘렸을 수 있습니다.")
            # 뉴스 데이터라도 붙여넣기 (비상용)
            blog_content += "<br><br><h3>📰 수집된 뉴스 데이터</h3><pre>" + raw_news + "</pre>"

        # 4. 티스토리에 포스팅
        post_to_tistory(blog_title, blog_content)
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")