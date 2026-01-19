# 워드프레스 자동 포스팅 시스템

## 📌 개요

이 시스템은 Gemini AI를 사용하여 금융 뉴스를 분석하고, 워드프레스 블로그에 자동으로 포스팅합니다.

### 주요 특징
- ✅ **간편한 설정**: Selenium 없이 REST API만 사용
- ✅ **안정적**: HTTP 요청 기반으로 브라우저 오류 없음
- ✅ **빠름**: 10초 내 포스팅 완료
- ✅ **안전**: 앱 비밀번호 사용으로 본 계정 보호
- ✅ **자동화**: Windows 작업 스케줄러로 완전 자동화 가능

## 🚀 빠른 시작

### 1단계: 워드프레스 애플리케이션 비밀번호 생성

1. 워드프레스 관리자 페이지 로그인
2. **사용자 → 프로필** 메뉴로 이동
3. 아래로 스크롤하여 **"애플리케이션 비밀번호"** 섹션 찾기
4. 이름 입력 (예: `AutoBlogBot`)
5. **"새 애플리케이션 비밀번호 추가"** 버튼 클릭
6. 생성된 비밀번호 복사 **(한 번만 표시됨!)**

### 2단계: 초기 설정

```bash
python setup_wordpress.py
```

대화형 프롬프트가 나타나면:
1. 워드프레스 블로그 URL 입력
2. 사용자명 입력 (기본값: SoulTree)
3. 생성한 애플리케이션 비밀번호 붙여넣기

설정이 완료되면 자동으로 연결 테스트와 카테고리 조회가 실행됩니다.

### 3단계: 자동 포스팅 실행

```bash
python wordpress_bot.py
```

또는 배치 파일 더블클릭:
```
run_wordpress_bot.bat
```

## 📂 파일 구조

```
c:\quant\
├── wordpress_bot.py          # 메인 자동 포스팅 스크립트
├── config.py                  # 설정 파일 (민감 정보 포함, Git 제외)
├── setup_wordpress.py         # 초기 설정 도우미
├── run_wordpress_bot.bat      # 실행 배치 파일
└── README_WORDPRESS.md        # 이 파일
```

## ⚙️ 고급 설정

### config.py 직접 수정

`config.py` 파일을 열어 다음 설정을 변경할 수 있습니다:

```python
# 카테고리 ID 변경
WORDPRESS_CATEGORY_ID = 5  # 원하는 카테고리 ID

# 포스트 상태 변경
POST_STATUS = 'draft'  # 임시저장으로 변경
```

### 카테고리 ID 찾기

```bash
python -c "from wordpress_bot import get_wordpress_categories; get_wordpress_categories()"
```

## 🔧 문제 해결

### 인증 오류 (401)
- 사용자명과 애플리케이션 비밀번호 확인
- 비밀번호에 공백이 포함되어 있는지 확인 (공백 포함이 정상)

### API 엔드포인트 오류 (404)
- 워드프레스 URL 확인 (https:// 포함)
- 워드프레스 REST API가 활성화되어 있는지 확인

### 본문이 비어있음
- Gemini API 키 확인
- 인터넷 연결 확인
- 뉴스 RSS 피드 접근 가능 여부 확인

## 📅 자동화 설정 (Windows 작업 스케줄러)

### 방법 1: PowerShell 스크립트 사용 (권장)

`register_wordpress_schedule.ps1` 파일 생성:

```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" `
    -Argument "c:\quant\wordpress_bot.py" `
    -WorkingDirectory "c:\quant"

$trigger = New-ScheduledTaskTrigger -Daily -At "09:00AM"

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName "WordPress Auto Poster" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "워드프레스 자동 포스팅 (매일 오전 9시)"
```

실행:
```powershell
.\register_wordpress_schedule.ps1
```

### 방법 2: 수동 설정

1. Windows 검색 → "작업 스케줄러" 실행
2. **작업 만들기** 클릭
3. **일반** 탭: 이름 입력
4. **트리거** 탭: **새로 만들기** → 매일, 원하는 시간 설정
5. **작업** 탭: 
   - 프로그램: `python.exe`
   - 인수: `c:\quant\wordpress_bot.py`
   - 시작 위치: `c:\quant`

## 🔐 보안 주의사항

1. **config.py는 절대 Git에 커밋하지 마세요!**
   - `.gitignore`에 자동 추가됨
   
2. **애플리케이션 비밀번호 보관**
   - 본 계정 비밀번호가 아님
   - 언제든지 취소 가능
   
3. **GitHub Actions 사용 시**
   - GitHub Secrets에 저장:
     - `WORDPRESS_URL`
     - `WORDPRESS_USERNAME`
     - `WORDPRESS_APP_PASSWORD`

## 🆚 Tistory vs WordPress

| 기능 | Tistory (Selenium) | WordPress (REST API) |
|------|-------------------|---------------------|
| 설정 복잡도 | 높음 (쿠키, 브라우저) | 낮음 (URL, 비밀번호) |
| 실행 속도 | 느림 (30~60초) | 빠름 (5~10초) |
| 안정성 | 낮음 (DOM 변경 시 오류) | 높음 (API 안정) |
| 의존성 | ChromeDriver, Selenium | requests만 |
| 오류 빈도 | 높음 | 낮음 |

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. `config.py` 설정 확인
2. `setup_wordpress.py` 재실행
3. 워드프레스 플러그인 충돌 확인
4. REST API 활성화 확인

## 📄 라이선스

MIT License
