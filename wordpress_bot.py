import google.generativeai as genai
import feedparser
import urllib.parse
from datetime import datetime
import requests
import json
import base64
import os

# config.py 또는 환경 변수에서 설정 불러오기
# 우선순위: 환경 변수 > config.py > 기본값
try:
    from config import (
        GEMINI_API_KEY as CONFIG_GEMINI_KEY,
        WORDPRESS_URL as CONFIG_WP_URL,
        WORDPRESS_USERNAME as CONFIG_WP_USER,
        WORDPRESS_APP_PASSWORD as CONFIG_WP_PASS,
        WORDPRESS_CATEGORY_ID as CONFIG_CATEGORY_ID,
        POST_STATUS as CONFIG_POST_STATUS
    )
except ImportError:
    # config.py가 없으면 환경 변수만 사용 (GitHub Actions용)
    print("⚠️ config.py 없음 - 환경 변수 사용")
    CONFIG_GEMINI_KEY = ""
    CONFIG_WP_URL = ""
    CONFIG_WP_USER = ""
    CONFIG_WP_PASS = ""
    CONFIG_CATEGORY_ID = 1
    CONFIG_POST_STATUS = 'publish'

# 환경 변수가 있으면 우선 사용 (보안!)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', CONFIG_GEMINI_KEY)
WORDPRESS_URL = os.environ.get('WORDPRESS_URL', CONFIG_WP_URL)
WORDPRESS_USERNAME = os.environ.get('WORDPRESS_USERNAME', CONFIG_WP_USER)
WORDPRESS_APP_PASSWORD = os.environ.get('WORDPRESS_APP_PASSWORD', CONFIG_WP_PASS)
WORDPRESS_CATEGORY_ID = int(os.environ.get('WORDPRESS_CATEGORY_ID', CONFIG_CATEGORY_ID))
POST_STATUS = os.environ.get('POST_STATUS', CONFIG_POST_STATUS)

# 설정 검증
if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY가 설정되지 않았습니다!")
if not WORDPRESS_URL or not WORDPRESS_USERNAME or not WORDPRESS_APP_PASSWORD:
    print("⚠️ 워드프레스 설정이 완료되지 않았습니다!")
    print("   로컬: config.py 파일 확인")
    print("   GitHub Actions: Secrets 설정 확인")

# Gemini 연결
genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# 1. 금융 뉴스 수집 (기존과 동일)
# ==========================================
def get_finance_news():
    print("🔍 오늘의 금융 뉴스를 수집합니다...")
    keywords = ["미국 증시", "FOMC", "연준 금리", "환율 전망"]
    news_data = []

    for keyword in keywords:
        encoded = urllib.parse.quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        
        if feed.entries:
            for i, entry in enumerate(feed.entries[:3], 1):
                news_data.append(f"[{keyword} - 뉴스 #{i}]\n- 제목: {entry.title}\n- 링크: {entry.link}")
    
    return "\n\n".join(news_data)

# ==========================================
# 2. Gemini Pro로 SEO 최적화된 제목과 본문 작성
# ==========================================
def generate_blog_content(news_text):
    print("🧠 Gemini가 '쉽고 깊이 있는' 금융 분석 콘텐츠를 작성합니다...")
    
    prompt = f"""
    당신은 **SEO 전문가이자 금융 블로그 작가**입니다.
    금융을 전혀 모르는 초보자도 쉽게 이해하면서도, 검색엔진 상위 노출이 가능한 고품질 콘텐츠를 작성합니다.

    [🎯 핵심 목표]
    1. **SEO 최적화**: 검색엔진 상위 노출
    2. **초보자 친화**: 중학생도 이해 가능
    3. **가독성**: 정갈하고 읽기 편한 구조
    4. **신뢰성**: 정확한 정보와 실용적 조언

    [📊 SEO 최적화 필수 요소]
    
    **제목 (Title Tag)**
    - 핵심 키워드를 앞쪽 배치
    - 30-55자 (검색 결과 잘림 방지)
    - 숫자 포함 (CTR 200% 향상)
    - 예: "미국 증시 3% 급등! 금리 동결이 주는 5가지 투자 기회"
    
    **메타 구조**
    - 첫 문단(100자)에 주요 키워드 2-3회 포함
    - H2 제목마다 키워드 변형 사용
    - 3,500자 이상 작성 (검색 순위 향상)
    
    **1. 초보자도 이해 가능한 쉬운 설명** 
    주식 시장이란 회사의 주식(회사 조각)을 사고파는 곳이에요.
    3% 올랐다는 건, 100만원을 투자했다면 103만원이 되었다는 뜻이죠.
    왜 올랐냐고요? 미국 중앙은행(연준)이 '금리를 올리지 않겠다'고 발표했거든요.
    금리란 돈을 빌릴 때 내는 이자예요. 금리가 안 오르면 회사들이 돈을 싸게 빌릴 수 있어서 좋아합니다."
    
    ❌ 나쁜 예시:
    "S&P500 지수가 3% 상승했다. FOMC의 금리 동결 결정으로 시장의 유동성이 증가할 것으로 예상되기 때문이다."
    
    **2. 진짜 어려운 금융 전문 용어만 설명 (중요!)**
    
    ✅ **설명이 필요한 용어** (금융 전문 용어):
    - "FOMC(미국 중앙은행 금리 결정 회의)"
    - "양적완화(QE, 중앙은행이 돈을 찍어내는 것)"
    - "S&P500(미국 대표 500개 기업 주가 지수)"
    - "금리(돈을 빌릴 때 내는 이자 비율)"
    - "환율(외국 돈과 우리나라 돈을 바꾸는 비율)"
    - "나스닥(미국 기술주 중심 주식 시장)"
    
    ❌ **설명 불필요한 용어** (일반적으로 알려진 단어):
    - "금융", "경제", "투자", "전문가", "은행", "회사"
    - "미국", "한국", "시장", "가격", "비용"
    - "주식", "돈", "이자", "대출" (문맥상 이해 가능)
    
    ⚠️ **절대 금지**:
    - "환율(환율)" ← 같은 단어 반복 금지!
    - "달러(달러)" ← 이미 알려진 단어는 괄호 불필요!
    - 쉬운 단어를 억지로 설명하지 말 것!
    
    **규칙**: 중학생이 모를 만한 금융 전문 용어만 처음 등장 시 1회 설명!
    
    **3. 숫자는 쉬운 비유로 설명**
    
    - "3% 상승" → "100만원이 103만원이 됨"
    - "5.25%의 금리" → "100만원을 빌리면 1년에 5만 2500원의 이자를 내야 함"
    - "1,400원대 환율" → "1달러를 사려면 1,400원이 필요함"

    **4. 각 뉴스는 이렇게 구성** (필수 형식!)
    
    ```
    <h3>🔹 [쉬운 한 줄 요약]</h3>
    <p><strong>📰 뉴스 요약:</strong> 무슨 일이 일어났는지 한 문장으로</p>
    
    <p><strong>🤔 쉽게 풀어보면:</strong></p>
    <p>
    (여기서 초등학생도 이해할 수 있게 설명)
    - 핵심 용어를 일상 언어로 바꾸기
    - 비유 사용하기
    - 왜 중요한지 쉽게 설명
    </p>
    
    <p><strong>💡 나에게 어떤 영향이 있나요:</strong></p>
    <p>
    (투자자 관점에서 실생활 영향 설명)
    </p>
    ```

    [🎯 SEO 최적화 제목]
    1. **주요 키워드 최전방**: "미국 증시", "금리", "환율", "주식"
    2. **숫자 포함**: "3가지", "5% 급등"
    3. **30~55자**
    4. **날짜 제외**
    
    예시: "미국 증시 3% 급등! 금리 동결이 주는 5가지 기회"

    [📋 글 구조 - SEO 최적화 + 정갈한 가독성]
    
    <p><strong>[키워드]</strong>에 대해 궁금하신가요? 오늘 중요한 금융 뉴스가 있었습니다. 초보자도 쉽게 이해할 수 있게 핵심만 정리해드릴게요.</p>
    
    <h2>📊 오늘의 핵심 요약</h2>
    <p>바쁘신 분들을 위한 3줄 요약입니다:</p>
    <ul>
        <li><strong>미국 증시 3% 상승</strong> → 100만원 투자 시 103만원으로 증가</li>
        <li><strong>금리 동결 결정</strong> → 대출 이자 부담 동결</li>
        <li><strong>투자 심리 개선</strong> → 시장 전망 긍정적</li>
    </ul>
    
    <h2>💰 주요 뉴스 상세 분석</h2>
    
    <h3>1️⃣ 미국 금리 동결 - 투자자에게 어떤 의미일까요?</h3>
    
    <p><strong>📌 핵심 내용</strong></p>
    <p>미국 중앙은행이 기준금리를 현재 수준으로 유지하기로 결정했습니다.</p>
    
    <p><strong>🔍 쉽게 이해하기</strong></p>
    <p>금리란 돈을 빌릴 때 내야 하는 이자예요. 은행에서 100만원을 빌리면 이자를 추가로 내야 하는데, 그 이자의 비율이 바로 금리입니다.</p>
    
    <p>금리가 동결된다는 건, 이자 부담이 늘어나지 않는다는 의미예요. 기업들은 이전과 같은 조건으로 돈을 빌릴 수 있어서 새로운 사업에 투자하기가 수월합니다.</p>
    
    <p><strong>💡 실생활 영향</strong></p>
    <ul>
        <li><strong>주식 투자자:</strong> 기업 실적 개선 기대로 주가 상승 가능</li>
        <li><strong>대출 이용자:</strong> 대출 이자 부담 증가 없음</li>
        <li><strong>예금자:</strong> 예금 금리도 동결 (이자 수익 변동 없음)</li>
    </ul>
    
    <h3>2️⃣ [다음 뉴스 제목]</h3>
    <p>(같은 형식으로 작성...)</p>
    
    <h2>💼 초보 투자자를 위한 실전 가이드</h2>
    
    <h3>🎯 단계별 투자 시작하기</h3>
    
    <p><strong>1단계: 기초 지식 쌓기 (1주일)</strong></p>
    <ul>
        <li>금융 용어 100개 학습</li>
        <li>경제 뉴스 매일 읽기</li>
        <li>투자 관련 유튜브 시청</li>
    </ul>
    
    <p><strong>2단계: 소액 투자 시작 (1개월)</strong></p>
    <ul>
        <li>5만원-10만원으로 시작</li>
        <li>안전한 펀드나 ETF 추천</li>
        <li>투자 일기 작성하기</li>
    </ul>
    
    <p><strong>3단계: 장기 투자 계획 (3개월 이상)</strong></p>
    <ul>
        <li>분산 투자 원칙 지키기</li>
        <li>정기적인 투자 습관</li>
        <li>전문가 조언 참고하기</li>
    </ul>
    
    <p>오늘도 쉽고 유익한 정보였길 바라요! 다음에 또 만나요 😊</p>

    [⚠️ 절대 규칙 - 반드시 지킬 것!]
    1. **SEO**: 첫 문단에 주요 키워드 포함, H2마다 키워드 변형 사용
    2. **분량**: 3,500자 이상 작성 (검색 노출 필수)
    3. **가독성**: 문단은 3-4문장, 소제목 적극 활용
    4. **용어 설명**: 진짜 어려운 금융 전문 용어만 설명 (FOMC, 양적완화, S&P500 등)
    5. **중복 금지**: "환율(환율)", "달러(달러)" 같은 같은 단어 반복 절대 금지!
    6. **쉬운 용어**: "금융", "투자", "은행", "주식" 같은 일반 단어는 설명 불필요!
    7. **구조**: 각 뉴스마다 "📌 핵심 내용" + "🔍 쉽게 이해하기" + "💡 실생활 영향"
    8. **금지**: 메타 설명, 지시사항, "참고 뉴스" 섹션 절대 출력 금지
    9. **정갈함**: 불필요한 이모지 남발 금지, 깔끔한 서술

    [⚠️ 중복 규칙 제거]
    1. **모든 금융 용어는 괄호 안에 즉시 설명!**
    2. **중학생도 이해할 수 있는 언어 사용!**
    3. **각 뉴스마다 "📰 뉴스 요약" + "🤔 쉽게 풀어보면" 필수!**
    4. **참고 뉴스 원문 링크를 모두 포함! (하나도 빠뜨리지 말 것)**
    5. **비유와 구체적 숫자 예시 필수 사용!**
    6. **"오프닝(친근하게)" 같은 메타 설명 절대 포함하지 말 것! 실제 내용만 작성!**

    [오늘의 뉴스 데이터]
    {news_text}
    
    [출력 형식]
    {{{{
        "title": "SEO 최적화 제목 (30-55자, 쉬운 언어)",
        "content": "초등학생도 이해 가능한 HTML 본문 (3,000자 이상)"
    }}}}
    """

    # Gemini 2.5 Flash - 최신 모델, 긴 출력, SEO 최적화에 유리
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,  # 더 일관된 품질
            max_output_tokens=8192,
            top_p=0.95,
        )
    )
    
    return response.text

# ==========================================
# 3. 워드프레스 REST API로 포스팅
# ==========================================
def post_to_wordpress(title, content, category_id=1, status='publish'):
    """
    워드프레스에 포스트를 생성합니다.
    
    Args:
        title: 포스트 제목
        content: 포스트 본문 (HTML)
        category_id: 카테고리 ID (기본값: 1 - Uncategorized)
        status: 'publish' (공개) 또는 'draft' (임시저장)
    
    Returns:
        생성된 포스트의 URL 또는 None
    """
    
    # 환경 변수에서 워드프레스 설정 읽기 (GitHub Actions용)
    wp_url = os.environ.get('WORDPRESS_URL', WORDPRESS_URL)
    wp_user = os.environ.get('WORDPRESS_USERNAME', WORDPRESS_USERNAME)
    wp_pass = os.environ.get('WORDPRESS_APP_PASSWORD', WORDPRESS_APP_PASSWORD)
    
    # 필수 정보 검증
    if not wp_url or not wp_user or not wp_pass:
        print("❌ 오류: 워드프레스 설정이 완료되지 않았습니다!")
        print("   WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD를 설정하세요.")
        return None
    
    # API 엔드포인트
    api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
    
    # Basic Authentication 인코딩
    credentials = f"{wp_user}:{wp_pass}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    
    # 헤더 설정
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
    }
    
    # 포스트 데이터
    post_data = {
        'title': title,
        'content': content,
        'status': status,  # 'publish' 또는 'draft'
        'categories': [category_id],
        'format': 'standard',
    }
    
    print(f"🚀 워드프레스에 포스팅 중... ({api_url})")
    
    try:
        # POST 요청
        response = requests.post(
            api_url,
            headers=headers,
            data=json.dumps(post_data),
            timeout=30
        )
        
        # 응답 처리
        if response.status_code == 201:  # Created
            post_info = response.json()
            post_url = post_info.get('link', '')
            post_id = post_info.get('id', '')
            
            print(f"✅ 포스팅 성공!")
            print(f"   📝 포스트 ID: {post_id}")
            print(f"   🔗 URL: {post_url}")
            
            return post_url
        else:
            print(f"❌ 포스팅 실패!")
            print(f"   상태 코드: {response.status_code}")
            print(f"   응답: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 오류: {e}")
        return None

# ==========================================
# 4. 워드프레스 카테고리 목록 조회 (참고용)
# ==========================================
def get_wordpress_categories():
    """
    워드프레스 카테고리 목록을 조회합니다.
    """
    wp_url = os.environ.get('WORDPRESS_URL', WORDPRESS_URL)
    wp_user = os.environ.get('WORDPRESS_USERNAME', WORDPRESS_USERNAME)
    wp_pass = os.environ.get('WORDPRESS_APP_PASSWORD', WORDPRESS_APP_PASSWORD)
    
    if not wp_url or not wp_user or not wp_pass:
        print("❌ 워드프레스 설정이 완료되지 않았습니다!")
        return []
    
    api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/categories"
    
    credentials = f"{wp_user}:{wp_pass}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {token}',
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            categories = response.json()
            print("📂 사용 가능한 카테고리:")
            for cat in categories:
                print(f"   ID: {cat['id']} - {cat['name']}")
            return categories
        else:
            print(f"❌ 카테고리 조회 실패: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 오류: {e}")
        return []

# ==========================================
# 메인 실행
# ==========================================
if __name__ == "__main__":
    import re
    
    try:
        # 1. 뉴스 수집
        raw_news = get_finance_news()
        
        # 2. AI로 제목과 본문 생성
        ai_response = generate_blog_content(raw_news)
        
        print(f"🤖 AI 응답 길이: {len(ai_response)}자")
        
        # 3. 제목/본문 추출
        blog_title = ""
        blog_content = ""

        try:
            # JSON 파싱 시도
            title_match = re.search(r'"title"\s*:\s*"(.*?)"', ai_response, re.DOTALL)
            content_match = re.search(r'"content"\s*:\s*"(.*?)"', ai_response, re.DOTALL)
            
            if title_match and content_match:
                blog_title = title_match.group(1)
                blog_content = content_match.group(1)
                blog_content = blog_content.replace('\\n', '\n').replace('\\"', '"')
                print(f"\n📌 제목: {blog_title}\n")
            else:
                raise Exception("정규식 패턴 매칭 실패")
        except Exception:
            print("⚠️ 제목/본문 분리 실패 → 수동 생성 모드")
            today_str = datetime.now().strftime("%m월 %d일")
            blog_title = f"[{today_str}] 오늘의 글로벌 금융 시장 심층 분석"
            
            blog_content = ai_response.replace('```json', '').replace('```', '').strip()
            if '"content":' in blog_content:
                blog_content = blog_content.split('"content":')[-1].strip().strip('"}')

        # 안전장치
        if len(blog_content) < 500:
            print(f"⚠️ 경고: 본문이 너무 짧습니다 ({len(blog_content)}자)")
            blog_content += "<br><br><h3>📰 수집된 뉴스</h3><pre>" + raw_news + "</pre>"

        # 4. 워드프레스에 포스팅
        post_url = post_to_wordpress(
            title=blog_title,
            content=blog_content,
            category_id=WORDPRESS_CATEGORY_ID,
            status=POST_STATUS
        )
        
        if post_url:
            print(f"\n🎉 작업 완료! 블로그를 확인하세요: {post_url}")
        else:
            print("\n⚠️ 포스팅 실패. 설정을 확인하세요.")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
