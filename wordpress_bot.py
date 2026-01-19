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
    # config.py가 없으면 기본값 사용 (GitHub Actions용)
    CONFIG_GEMINI_KEY = ""
    CONFIG_WP_URL = ""
    CONFIG_WP_USER = ""
    CONFIG_WP_PASS = ""
    CONFIG_CATEGORY_ID = 1
    CONFIG_POST_STATUS = 'publish'

# 환경 변수가 있으면 우선 사용 (GitHub Actions에서 실행 시)
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
    복잡한 금융 뉴스를 **검색엔진 최적화하면서도 독자 친화적으로** 분석하는 것이 당신의 강점입니다.

    [🎯 SEO 최적화 제목 작성 - 매우 중요!]
    1. **주요 키워드 최전방 배치**: "미국 증시", "FOMC", "금리", "환율", "주식" 등을 제목 앞쪽에
       ✅ 좋은 예: "미국 증시 급등! 오늘의 투자 전략 3가지"
       ❌ 나쁜 예: "오늘의 투자 전략 3가지 - 미국 증시"
    
    2. **숫자와 구체성**: CTR 200% 향상
       예: "5가지 투자 기회", "3% 급등", "7가지 체크포인트"
    
    3. **파워 워드 사용**: 클릭 유도
       - 긍정: "급등", "기회", "전망", "주목", "분석", "완벽 정리"
       - 긴급: "오늘", "지금", "최신", "속보"
       - 실용: "방법", "전략", "가이드", "정리"
    
    4. **최적 길이**: 30~55자 (검색 결과 잘림 방지)
    5. **날짜 제외**: "2026년 1월" 같은 날짜 넣지 말 것
    
    예시 제목:
    - "미국 증시 3% 급등! FOMC 결정이 만든 5가지 투자 기회"
    - "환율 급변! 달러 강세가 한국 투자자에게 미치는 영향 완벽 정리"

    [📝 SEO 최적화 본문 작성 - 워드프레스 HTML]
    
    **1. 제목 태그 계층 구조 (매우 중요!)**
       - H1: 사용하지 말 것 (워드프레스가 자동 생성)
       - H2: 주요 섹션 (<h2>💰 오늘의 핵심 뉴스</h2>)
       - H3: 세부 항목 (<h3>S&P500 급등 분석</h3>)
       - 각 H2마다 핵심 키워드 포함 필수!

    **2. 키워드 최적화 전략**
       - 주요 키워드(미국 증시, FOMC 등) **5-8회** 자연스럽게 반복
       - 첫 문단(100자 이내)에 핵심 키워드 **반드시 포함**
       - <strong> 태그로 키워드 강조 (SEO 가중치)
       - LSI 키워드 활용: "S&P500", "나스닥", "연준", "파월 의장" 등

    **3. 내부 구조 최적화**
       - 각 문단: 2-4문장 (가독성)
       - 목록 적극 활용: <ul><li> (스니펫 노출 확률 UP)
       - 표 사용: <table> (Featured Snippet 가능성)
       
    **4. 링크 전략 (매우 중요!)**
       - 외부 링크: 뉴스 원문에 rel="noopener" 필수
         <a href="URL" target="_blank" rel="noopener">기사 제목</a>
       - 앵커 텍스트를 키워드로: 
         ✅ <a href="#">미국 증시 전망 보기</a>
         ❌ <a href="#">여기 클릭</a>

    **5. 초보자 친화적 설명 (체류 시간 증가 = SEO 향상)**
       - 전문 용어 바로 설명
         예: "FOMC(연방공개시장위원회)는 미국의 금리를 결정하는 회의예요"
       - 비유 활용: "금리 인상은 자동차 브레이크와 같아요"
       - 일상 언어: "긴축 통화정책" → "돈의 흐름을 줄이는 것"

    **6. 글 구조 (SEO 최적화, 3,000자 이상)**
    
    <p><strong>핵심 키워드가 포함된 오프닝 문장</strong> (100자)</p>
    
    <h2>📊 3줄 요약</h2>
    <ul>
        <li>요약 1 (키워드 포함)</li>
        <li>요약 2</li>
        <li>요약 3</li>
    </ul>
    
    <h2>💰 오늘의 핵심 뉴스 분석</h2>
    
    <h3>🔹 [뉴스 1 제목 - 키워드 포함]</h3>
    <p>본문 (300자 이상, 키워드 자연스럽게 2-3회)</p>
    <p><strong>투자 포인트:</strong> 핵심 요약</p>
    
    <h3>🔹 [뉴스 2 제목]</h3>
    <p>본문...</p>
    
    <h2>💡 투자자를 위한 실전 전략</h2>
    <ul>
        <li><strong>단기 전략:</strong> 구체적 조언</li>
        <li><strong>중기 전략:</strong> 구체적 조언</li>
        <li><strong>장기 전략:</strong> 구체적 조언</li>
    </ul>
    
    <h2>📰 참고 뉴스 원문</h2>
    <ul>
        <li><a href="URL" target="_blank" rel="noopener">뉴스 제목 (키워드 포함)</a></li>
    </ul>
    
    <p>마무리 문장 (CTA: Call To Action 포함)</p>

    **7. SEO 체크리스트**
    ✅ 첫 100자에 핵심 키워드 포함
    ✅ H2 태그 3개 이상, 각각 키워드 포함
    ✅ 키워드 밀도 1-2% (과도하지 않게)
    ✅ 외부 링크 3개 이상 (신뢰도)
    ✅ 목록(<ul>) 2개 이상
    ✅ <strong> 태그로 중요 키워드 강조
    ✅ 총 3,000자 이상 (검색 순위 향상)
    ✅ 독자 가치 제공 (이탈률 감소)

    [오늘의 뉴스 데이터]
    {news_text}
    
    [출력 형식]
    반드시 다음 JSON 형식으로 출력:
    {{{{
        "title": "SEO 최적화된 제목 (30-55자, 키워드 최전방)",
        "content": "SEO 최적화된 HTML 본문 (3,000자 이상)"
    }}}}
    
    **절대 규칙**:
    1. 제목에 핵심 키워드를 앞쪽에!
    2. 첫 100자에 핵심 키워드 필수!
    3. H2 태그마다 키워드 포함!
    4. 3,000자 이상 작성!
    5. 독자에게 실질적 가치 제공!
    """

    # Gemini 2.0 Flash 모델로 고품질 콘텐츠 생성
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.9,  # 창의성 최대화
            max_output_tokens=8000,  # 긴 심층 분석 가능
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
