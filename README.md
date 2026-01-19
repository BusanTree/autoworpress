# 워드프레스 자동 포스팅 시스템 🚀

금융 뉴스를 AI가 분석하여 **SEO 최적화된 블로그 포스트**를 자동으로 워드프레스에 게시하는 시스템입니다.

## ✨ 주요 기능

- 🤖 **Gemini AI 분석**: 최신 금융 뉴스를 수집하고 초보자도 이해하기 쉽게 분석
- 🎯 **SEO 최적화**: 검색엔진 최적화된 제목과 본문 자동 생성
- 📝 **워드프레스 REST API**: Selenium 없이 안정적인 포스팅
- ⏰ **완전 자동화**: GitHub Actions로 매일 오전 7시 자동 실행
- 🌐 **다양한 환경 지원**: 로컬 + GitHub Actions

## 📂 프로젝트 구조

```
c:\quant\
├── .github/
│   └── workflows/
│       └── wordpress-auto-post.yml   # GitHub Actions 워크플로우
├── wordpress_bot.py                  # 메인 스크립트
├── config.py                         # 설정 파일 (Git 제외)
├── setup_wordpress.py                # 초기 설정 도우미
├── run_wordpress_bot.bat             # Windows 실행 파일
├── register_wordpress_schedule.ps1   # Windows 작업 스케줄러 등록
├── requirements_wordpress.txt        # Python 패키지 목록
├── README.md                         # 이 파일
├── README_WORDPRESS.md               # 상세 사용 설명서
└── GITHUB_ACTIONS_GUIDE.md           # GitHub Actions 가이드
```

## 🚀 빠른 시작

### 1단계: 의존성 설치

```bash
pip install google-generativeai feedparser requests
```

또는:

```bash
pip install -r requirements_wordpress.txt
```

### 2단계: 워드프레스 설정

```bash
python setup_wordpress.py
```

대화형 프롬프트에 따라:
1. 워드프레스 블로그 URL 입력
2. 사용자명 입력
3. 애플리케이션 비밀번호 입력

**애플리케이션 비밀번호 생성 방법:**
- 워드프레스 관리자 → 사용자 → 프로필
- "애플리케이션 비밀번호" 섹션에서 생성

### 3단계: 실행

```bash
python wordpress_bot.py
```

또는 배치 파일 더블클릭:
```
run_wordpress_bot.bat
```

## 🤖 GitHub Actions 자동화

### GitHub Secrets 설정

GitHub 저장소 → Settings → Secrets and variables → Actions

다음 Secret들을 추가:

| Secret Name | Example | 설명 |
|------------|---------|------|
| `GEMINI_API_KEY` | `AIzaSyA...` | Gemini API 키 |
| `WORDPRESS_URL` | `https://yourblog.com` | 워드프레스 URL |
| `WORDPRESS_USERNAME` | `SoulTree` | 사용자명 |
| `WORDPRESS_APP_PASSWORD` | `fKyz DdgT...` | 앱 비밀번호 |
| `WORDPRESS_CATEGORY_ID` | `1` | 카테고리 ID |

### 워크플로우 푸시

```bash
git add .github/workflows/wordpress-auto-post.yml
git commit -m "Add WordPress auto-posting workflow"
git push origin main
```

### 실행 시간

- **한국 시간**: 매일 오전 7:00
- **수동 실행**: Actions 탭 → Run workflow

자세한 내용은 [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) 참고

## 📊 SEO 최적화 특징

✅ **제목 최적화**
- 핵심 키워드 최전방 배치
- 숫자와 구체적 정보 포함
- 30-55자 최적 길이

✅ **본문 최적화**
- H2/H3 제목 태그 계층 구조
- 키워드 밀도 1-2%
- 외부 링크 포함
- 목록 및 표 활용
- 3,000자 이상 심층 분석

✅ **사용자 경험**
- 초보자도 이해하기 쉬운 설명
- 비유와 예시 활용
- 실질적 투자 전략 제공

## 🛠️ 설정 파일

### config.py

```python
GEMINI_API_KEY = "your_api_key"
WORDPRESS_URL = "https://yourblog.com"
WORDPRESS_USERNAME = "SoulTree"
WORDPRESS_APP_PASSWORD = "your_app_password"
WORDPRESS_CATEGORY_ID = 1
POST_STATUS = 'publish'  # 또는 'draft'
```

> **주의**: `config.py`는 `.gitignore`에 포함되어 있습니다. Git에 커밋하지 마세요!

## 🖥️ Windows 작업 스케줄러 (로컬 자동화)

GitHub Actions 대신 Windows에서 직접 실행하려면:

```powershell
.\register_wordpress_schedule.ps1
```

관리자 권한으로 PowerShell 실행 필요

## 📝 주요 파일 설명

| 파일 | 설명 |
|------|------|
| `wordpress_bot.py` | 메인 스크립트 (뉴스 수집 → AI 분석 → 포스팅) |
| `config.py` | 설정 파일 (민감 정보 포함) |
| `setup_wordpress.py` | 초기 설정 도우미 |
| `requirements_wordpress.txt` | Python 패키지 목록 |
| `.github/workflows/wordpress-auto-post.yml` | GitHub Actions 워크플로우 |

## 🔒 보안

- ✅ config.py는 Git에 커밋되지 않음
- ✅ GitHub Secrets로 민감 정보 보호
- ✅ 애플리케이션 비밀번호 사용 (본 계정 비밀번호 아님)
- ✅ 언제든지 앱 비밀번호 취소 가능

## 🆚 기존 시스템과 비교

| 항목 | Tistory (기존) | WordPress (현재) |
|------|---------------|-----------------|
| 설정 | 복잡 (쿠키, 브라우저) | 간단 (URL, 비밀번호) |
| 속도 | 30~60초 | 5~10초 |
| 안정성 | 낮음 | 높음 |
| 의존성 | ChromeDriver, Selenium | requests만 |
| SEO | 수동 최적화 | 자동 최적화 |
| 자동화 | 어려움 | 쉬움 |

## 📚 추가 문서

- [README_WORDPRESS.md](README_WORDPRESS.md) - 상세 사용 설명서
- [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) - GitHub Actions 설정 가이드

## 🐛 문제 해결

### 인증 오류 (401)
- 앱 비밀번호 재생성
- 사용자명 확인

### 본문이 비어있음
- Gemini API 키 확인
- 인터넷 연결 확인

### GitHub Actions 실행 안 됨
- Secrets 설정 재확인
- 워크플로우 권한 확인

## 📞 지원

문제가 발생하면:
1. 실행 로그 확인
2. config.py 설정 검토
3. setup_wordpress.py 재실행

## 📄 라이선스

MIT License

---

Made with ❤️ using Gemini AI + WordPress REST API
