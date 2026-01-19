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
        POST_STATUS as CONFIG_POST_STATUS,
        UNSPLASH_ACCESS_KEY as CONFIG_UNSPLASH_KEY
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
    CONFIG_UNSPLASH_KEY = ""

# 환경 변수가 있으면 우선 사용 (보안!)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', CONFIG_GEMINI_KEY)
WORDPRESS_URL = os.environ.get('WORDPRESS_URL', CONFIG_WP_URL)
WORDPRESS_USERNAME = os.environ.get('WORDPRESS_USERNAME', CONFIG_WP_USER)
WORDPRESS_APP_PASSWORD = os.environ.get('WORDPRESS_APP_PASSWORD', CONFIG_WP_PASS)
WORDPRESS_CATEGORY_ID = int(os.environ.get('WORDPRESS_CATEGORY_ID', CONFIG_CATEGORY_ID))
POST_STATUS = os.environ.get('POST_STATUS', CONFIG_POST_STATUS)
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY', CONFIG_UNSPLASH_KEY)

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
# 1-1. Unsplash에서 금융 관련 이미지 가져오기
# ==========================================
def get_finance_image_from_unsplash():
    """
    Unsplash API를 사용하여 금융 관련 이미지 URL을 가져옵니다.
    Returns: 이미지 URL 또는 None
    """
    if not UNSPLASH_ACCESS_KEY:
        print("⚠️ Unsplash API 키가 없습니다. 이미지 생략.")
        return None
    
    try:
        # 금융 관련 키워드 - 더 구체적으로
        import random
        keywords = [
            "stock market chart screen",  # 주식 차트 화면
            "financial trading graph",     # 금융 거래 그래프
            "money investment business",   # 투자 비즈니스
            "economy dollar currency",     # 달러 통화
            "wall street stock exchange",  # 월스트리트 증권거래소
            "cryptocurrency bitcoin chart", # 암호화폐 차트
            "forex trading chart",         # 외환 거래 차트
            "stock market bull bear"       # 주식시장 불/베어
        ]
        query = random.choice(keywords)
        
        url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            image_url = data['urls']['regular']  # 1080px 폭
            photographer = data['user']['name']
            photo_link = data['links']['html']
            
            print(f"📷 이미지 가져옴: {image_url}")
            print(f"   촬영: {photographer}")
            
            # Unsplash 이용 약관: 출처 표기 HTML
            credit_html = f'<p style="font-size:12px;color:#999;margin-top:30px;">Photo by <a href="{photo_link}?utm_source=quanroot&utm_medium=referral" target="_blank">{photographer}</a> on <a href="https://unsplash.com?utm_source=quanroot&utm_medium=referral" target="_blank">Unsplash</a></p>'
            
            return {"url": image_url, "credit": credit_html}
        else:
            print(f"⚠️ Unsplash API 오류: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"⚠️ 이미지 가져오기 실패: {e}")
        return None

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
    5. **완성도**: 반드시 모든 내용을 끝까지 완성해서 작성

    [📊 SEO 최적화 필수 요소]
    
    **제목 (Title Tag)** - 검색 유입의 핵심!
    
    ⚠️ 중요: 사람들이 **실제로 검색하는 질문/키워드**를 제목으로 사용하세요!
    
    **실제 검색 쿼리 예시:**
    - "미국 금리 언제 인하?" → "미국 금리 인하 시기 2026 전망 - FOMC 일정 정리"
    - "나스닥 왜 올랐어?" → "나스닥 급등 원인 분석 - 빅테크 실적 발표 총정리"
    - "환율 전망" → "원달러 환율 2026년 전망 - 1500원 돌파 가능성은?"
    - "금리 동결 주식 영향" → "미국 금리 동결 발표 - 한국 주식시장 영향 5가지"
    - "FOMC 뭐야?" → "FOMC 쉽게 설명 - 금리 결정 회의가 내 투자에 미치는 영향"
    
    **제목 작성 원칙:**
    1. 질문형 또는 호기심 유발 ("왜?", "언제?", "어떻게?")
    2. 구체적인 숫자/날짜 포함 ("2026년", "5가지", "3% 급등")
    3. 타겟 키워드 맨 앞 배치
    4. 30-55자 (검색 결과 표시 최적화)
    5. 클릭 유도 문구 ("총정리", "쉽게 설명", "핵심 요약")
    
    **메타 디스크립션 (Meta Description)** - 검색 결과 미리보기!
    - 120-155자 (모바일 최적화)
    - 핵심 키워드 1-2회 자연스럽게 포함
    - 클릭 유도 문구 ("지금 확인하세요", "핵심만 정리")
    - 예시: "미국 금리 인하가 한국 주식과 부동산에 미치는 영향을 초보자도 이해할 수 있게 정리했습니다. FOMC 일정과 투자 전략까지 한눈에 확인하세요."
    
    **메타 구조**
    - 첫 문단(100자)에 주요 키워드 2-3회 포함
    - H2 제목마다 키워드 변형 사용
    - 5,000자 이상 작성 (검색 순위 향상)
    
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

    [📋 필수 글 구조 - 반드시 모든 섹션 작성!]
    
    **⚠️ 중요: 아래 모든 섹션을 반드시 포함하세요. 뉴스가 적어도 각 섹션을 상세히 작성하여 최소 5,000자를 채우세요!**
    
    ```html
    <p><strong>[핵심 키워드]</strong>에 대해 궁금하신가요? 오늘의 금융 뉴스와 시장 동향을 초보자도 쉽게 이해할 수 있게 심층 분석해드립니다.</p>
    
    <h2>📊 오늘의 핵심 요약 (3줄 핵심)</h2>
    <ul>
        <li><strong>핵심 1</strong> → 쉬운 설명</li>
        <li><strong>핵심 2</strong> → 쉬운 설명</li>
        <li><strong>핵심 3</strong> → 쉬운 설명</li>
    </ul>
    
    <h2>💰 주요 뉴스 심층 분석</h2>
    
    <h3>1️⃣ [첫 번째 뉴스 제목]</h3>
    <p><strong>� 무슨 일이 일어났나요?</strong></p>
    <p>(200자 이상 상세 설명)</p>
    
    <p><strong>🤔 초보자를 위한 쉬운 설명</strong></p>
    <p>(300자 이상 비유와 예시를 들어 설명)</p>
    
    <p><strong>💡 나의 투자와 실생활에 미치는 영향</strong></p>
    <ul>
        <li><strong>주식 투자자:</strong> 구체적 영향</li>
        <li><strong>예금자:</strong> 구체적 영향</li>
        <li><strong>대출 이용자:</strong> 구체적 영향</li>
        <li><strong>환전 계획자:</strong> 구체적 영향</li>
    </ul>
    
    <h3>2️⃣ [두 번째 뉴스 제목]</h3>
    <p>(위와 동일한 구조로 작성)</p>
    
    <h3>3️⃣ [세 번째 뉴스 제목]</h3>
    <p>(위와 동일한 구조로 작성)</p>
    
    <h2>📈 시장 전망 및 투자 전략</h2>
    
    <h3>🎯 단기 전망 (1-3개월)</h3>
    <p>(200자 이상)</p>
    <ul>
        <li>예상 시나리오 1</li>
        <li>예상 시나리오 2</li>
    </ul>
    
    <h3>🎯 중장기 전망 (6-12개월)</h3>
    <p>(200자 이상)</p>
    
    <h2>💼 초보 투자자를 위한 실전 가이드</h2>
    
    <h3>✅ 이런 분께 추천합니다</h3>
    <ul>
        <li>투자 유형 1</li>
        <li>투자 유형 2</li>
        <li>투자 유형 3</li>
    </ul>
    
    <h3>⚠️ 주의해야 할 점</h3>
    <ul>
        <li>주의사항 1</li>
        <li>주의사항 2</li>
        <li>주의사항 3</li>
    </ul>
    
    <h3>� 더 공부하면 좋은 금융 용어</h3>
    <ul>
        <li><strong>용어 1:</strong> 설명</li>
        <li><strong>용어 2:</strong> 설명</li>
        <li><strong>용어 3:</strong> 설명</li>
    </ul>
    
    <h2>🔮 전문가 의견 정리</h2>
    <p>전문가들의 다양한 의견을 요약 (300자 이상)</p>
    
    <p>오늘도 유익한 금융 정보가 되셨기를 바랍니다. 투자는 신중하게, 항상 분산 투자 원칙을 지키세요! 😊</p>
    ```
    
    [⚠️ 절대 규칙 - 위반 시 재작성!]
    1. **최소 분량**: 5,000자 이상 (HTML 태그 제외, 순수 텍스트 기준) - 절대적
    2. **필수 섹션**: 위의 모든 H2, H3 섹션 반드시 포함
    3. **각 섹션 최소 길이**: 각 H3마다 최소 200자 이상 작성
    4. **뉴스가 적을 때**: 각 뉴스를 더 깊이 분석, 배경 지식, 역사적 맥락, 향후 전망 추가
    5. **완성도**: 모든 섹션을 끝까지 완성 (중간에 절대 끊기지 않음)
    6. **용어 설명**: 진짜 어려운 금융 전문 용어만 설명 (FOMC, 양적완화, S&P500 등)
    7. **중복 금지**: "환율(환율)", "달러(달러)" 같은 같은 단어 반복 절대 금지
    8. **비유와 예시**: 구체적 숫자 예시 필수 사용

    [오늘의 뉴스 데이터]
    {news_text}
    
    [출력 형식]
    {{{{
        "title": "실제 검색 쿼리 기반 SEO 제목 (30-55자, 질문형/호기심 유발)",
        "meta_description": "검색 결과 미리보기 설명 (120-155자, 클릭 유도)",
        "content": "초등학생도 이해 가능한 HTML 본문 (5,000자 이상 필수!!)"
    }}}}
    """

    # Gemini 2.5 Flash - 안정적이고 빠른 모델, 긴 출력
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,  # 더 일관된 품질
            max_output_tokens=16384,  # 글이 잘리지 않도록 충분한 토큰 수
            top_p=0.95,
        )
    )
    
    return response.text

# ==========================================
# 3. 워드프레스 REST API로 포스팅
# ==========================================
def post_to_wordpress(title, content, category_id=1, status='publish', meta_description=None, featured_image_url=None):
    """
    워드프레스에 포스트를 생성합니다.
    
    Args:
        title: 포스트 제목
        content: 포스트 본문 (HTML)
        category_id: 카테고리 ID (기본값: 1 - Uncategorized)
        status: 'publish' (공개) 또는 'draft' (임시저장)
        meta_description: SEO 메타 디스크립션 (선택)
        featured_image_url: 대표 이미지 URL (선택)
    
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
    
    # 메타 디스크립션 추가 (Yoast SEO 또는 excerpt 사용)
    if meta_description:
        post_data['excerpt'] = meta_description  # WordPress 기본 발췌
        # Yoast SEO 플러그인 사용 시 메타 필드 추가
        post_data['meta'] = {
            '_yoast_wpseo_metadesc': meta_description
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
        
        # 3. 제목/본문/메타 디스크립션 추출
        blog_title = ""
        blog_content = ""
        meta_description = ""

        try:
            # JSON 파싱 시도
            title_match = re.search(r'"title"\s*:\s*"(.*?)"', ai_response, re.DOTALL)
            content_match = re.search(r'"content"\s*:\s*"(.*?)"', ai_response, re.DOTALL)
            meta_match = re.search(r'"meta_description"\s*:\s*"(.*?)"', ai_response, re.DOTALL)
            
            if title_match and content_match:
                blog_title = title_match.group(1)
                blog_content = content_match.group(1)
                meta_description = meta_match.group(1) if meta_match else ""
                
                # 이스케이프 문자 처리
                blog_content = blog_content.replace('\\n', '<br>').replace('\\"', '"').replace('\n', '<br>')
                meta_description = meta_description.replace('\\n', ' ').replace('\\"', '"').replace('\n', ' ')
                
                print(f"\n📌 제목: {blog_title}")
                print(f"📝 본문 길이: {len(blog_content)}자")
                print(f"📋 메타 디스크립션: {meta_description[:100]}...\n")
            else:
                raise Exception("정규식 패턴 매칭 실패")
        except Exception as parse_error:
            print(f"⚠️ 제목/본문 분리 실패: {parse_error}")
            print("→ SEO 최적화 제목 자동 생성 모드")
            
            # SEO에 유리한 제목 생성 - 검색 쿼리 기반
            today_str = datetime.now().strftime("%Y년 %m월")
            
            # 실제 검색 쿼리 스타일로 제목 생성
            if "금리" in raw_news and "인하" in raw_news:
                blog_title = f"미국 금리 인하 언제? {today_str} FOMC 일정과 전망 정리"
                meta_description = f"미국 금리 인하 시기와 한국 경제 영향을 초보자도 이해할 수 있게 정리했습니다. {today_str} 최신 FOMC 전망을 확인하세요."
            elif "금리" in raw_news and "동결" in raw_news:
                blog_title = f"미국 금리 동결 발표 - 한국 주식 영향 5가지 ({today_str})"
                meta_description = f"미국 금리 동결이 국내 증시와 환율에 미치는 영향을 분석했습니다. 투자자가 알아야 할 핵심 정보를 확인하세요."
            elif "환율" in raw_news:
                blog_title = f"원달러 환율 {today_str} 전망 - 1500원 돌파 가능성은?"
                meta_description = f"원달러 환율 전망과 달러 강세 원인을 쉽게 설명합니다. 환율 변동이 내 자산에 미치는 영향까지 확인하세요."
            elif "나스닥" in raw_news or "급등" in raw_news:
                blog_title = f"나스닥 급등 원인 분석 - {today_str} 빅테크 실적 총정리"
                meta_description = f"나스닥이 급등한 이유를 초보 투자자도 이해할 수 있게 설명합니다. 빅테크 기업 실적과 투자 전략을 확인하세요."
            else:
                blog_title = f"{today_str} 글로벌 금융시장 - 주식·금리·환율 핵심 정리"
                meta_description = f"복잡한 금융 뉴스를 3분 만에 이해하세요. 오늘의 주요 경제 소식과 투자 포인트를 초보자 눈높이에 맞춰 정리했습니다."
            
            blog_content = ai_response.replace('```json', '').replace('```', '').strip()
            if '"content":' in blog_content:
                blog_content = blog_content.split('"content":')[-1].strip().strip('"}')
            
            # 이스케이프 문자 처리
            blog_content = blog_content.replace('\\n', '<br>').replace('\n', '<br>').replace('\\"', '"')

        # 4. Unsplash 이미지 가져오기
        image_data = get_finance_image_from_unsplash()
        if image_data:
            # 이미지를 본문 상단에 삽입
            image_html = f'<img src="{image_data["url"]}" alt="금융 시장 분석" style="width:100%;max-width:800px;height:auto;margin:20px 0;border-radius:8px;" />'
            blog_content = image_html + "<br>" + blog_content
            # 이미지 출처 하단에 추가
            blog_content += "<br>" + image_data["credit"]
        
        # 5. 안전장치: 본문 길이 체크 및 보강
        if len(blog_content) < 1000:
            print(f"⚠️ 경고: 본문이 너무 짧습니다 ({len(blog_content)}자)")
            print("   → 원본 뉴스를 추가합니다")
            blog_content += "<br><br><h2>📰 참고: 오늘의 주요 뉴스</h2><div style='background:#f5f5f5;padding:20px;border-radius:8px;'><pre style='white-space:pre-wrap;'>" + raw_news + "</pre></div>"
        
        # 최종 정보 출력
        print(f"\n✅ 최종 제목: {blog_title}")
        print(f"✅ 메타 설명: {meta_description[:80]}...")
        print(f"✅ 본문 길이: {len(blog_content)}자")
        print(f"✅ 이미지: {'포함' if image_data else '없음'}")

        # 6. 워드프레스에 포스팅
        post_url = post_to_wordpress(
            title=blog_title,
            content=blog_content,
            meta_description=meta_description,
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
