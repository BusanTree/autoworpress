# WordPress 자동 포스팅 봇 (Auto WordPress Posting Bot)

금융 뉴스를 자동으로 수집하고 Gemini AI로 분석하여 워드프레스 블로그에 자동 포스팅하는 봇입니다.

## 기능

- 📰 구글 뉴스에서 금융 뉴스 자동 수집
- 🤖 Gemini AI로 초보자 친화적인 블로그 글 작성
- 🎨 Unsplash에서 금융 관련 이미지 자동 추가
- 📝 워드프레스에 자동 포스팅
- ⏰ GitHub Actions로 매일 자동 실행

## 설정 방법

### 1. 로컬 실행

1. **의존성 설치**
```bash
pip install -r requirements.txt
```

2. **config.py 파일 생성**
```python
# Gemini API 키
GEMINI_API_KEY = "your_gemini_api_key"

# 워드프레스 정보
WORDPRESS_URL = "https://yourblog.com"
WORDPRESS_USERNAME = "your_username"
WORDPRESS_APP_PASSWORD = "your_app_password"
WORDPRESS_CATEGORY_ID = 1

# 포스트 상태
POST_STATUS = 'publish'  # 또는 'draft'

# Unsplash API 키 (선택)
UNSPLASH_ACCESS_KEY = "your_unsplash_key"
```

3. **실행**
```bash
python wordpress_bot.py
```

### 2. GitHub Actions 자동 스케줄링

#### Secrets 설정

GitHub Repository → Settings → Secrets and variables → Actions → New repository secret

다음 Secrets를 추가하세요:

- `GEMINI_API_KEY`: Gemini API 키 ([발급 링크](https://makersuite.google.com/app/apikey))
- `WORDPRESS_URL`: 워드프레스 블로그 URL (예: `https://yourblog.com`)
- `WORDPRESS_USERNAME`: 워드프레스 사용자명
- `WORDPRESS_APP_PASSWORD`: 워드프레스 Application Password
  - WordPress 관리자 → 사용자 → 프로필 → Application Passwords에서 생성
- `WORDPRESS_CATEGORY_ID`: 카테고리 ID (예: `1`)
- `UNSPLASH_ACCESS_KEY`: Unsplash API 키 (선택) ([발급 링크](https://unsplash.com/oauth/applications))

#### 실행 스케줄

- **자동 실행**: 매일 오전 9시 (한국 시간)
- **수동 실행**: GitHub Actions 탭에서 "Run workflow" 버튼 클릭

## 워크플로우

```
뉴스 수집 → AI 분석 → 이미지 추가 → 워드프레스 포스팅
```

1. 구글 뉴스에서 금융 키워드로 뉴스 수집
2. Gemini AI가 초보자도 이해할 수 있는 블로그 글 작성
3. Unsplash에서 관련 이미지 자동 추가
4. SEO 최적화된 제목과 메타 설명 생성
5. 워드프레스에 자동 포스팅

## 파일 구조

```
.
├── wordpress_bot.py          # 메인 봇 스크립트
├── config.py                 # 설정 파일 (로컬용, .gitignore에 포함)
├── requirements.txt          # Python 의존성
├── .github/
│   └── workflows/
│       └── auto-post.yml     # GitHub Actions 워크플로우
└── README.md                 # 이 파일
```

## 주의사항

- `config.py`는 절대 Git에 커밋하지 마세요 (API 키 포함)
- GitHub Actions 사용 시 반드시 Secrets 설정 필요
- Gemini API 무료 할당량 확인 필요

## 라이선스

MIT License
