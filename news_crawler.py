import feedparser
import urllib.parse
from datetime import datetime

# ==========================================
# 🎯 [설정] 금융 블로그를 위한 핵심 키워드
# ==========================================
# 매일 돌아가면서 이 주제들을 검색합니다.
KEYWORDS = ["미국 증시", "FOMC", "미국 기준금리", "나스닥 전망", "환율 전망"]

def get_finance_news():
    print(f"💰 금융 뉴스 수집을 시작합니다... ({datetime.now().strftime('%Y-%m-%d')})")
    
    all_news = []
    
    for keyword in KEYWORDS:
        # 검색어 URL 인코딩
        encoded_keyword = urllib.parse.quote(keyword)
        # 구글 뉴스 RSS (정확도 순 정렬)
        rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
        
        feed = feedparser.parse(rss_url)
        
        # 키워드별로 최신 기사 2개씩만 뽑음 (너무 많으면 블로그 글이 지저분해짐)
        print(f"\n🔍 '{keyword}' 관련 주요 뉴스:")
        
        count = 0
        for entry in feed.entries:
            if count >= 2: break # 2개만 수집
            
            title = entry.title
            link = entry.link
            date = entry.published
            
            # 뉴스 정보 저장
            news_item = {
                "keyword": keyword,
                "title": title,
                "link": link,
                "date": date
            }
            all_news.append(news_item)
            
            print(f"- {title}")
            count += 1
            
    return all_news

if __name__ == "__main__":
    news_data = get_finance_news()
    print(f"\n✅ 총 {len(news_data)}개의 금융 뉴스를 수집했습니다.")