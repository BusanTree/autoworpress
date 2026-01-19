# GitHub Actions 워드프레스 자동 포스팅 설정 가이드

## 📋 개요

이 가이드는 GitHub Actions를 사용하여 매일 오전 7시(한국 시간)에 워드프레스 블로그에 자동으로 포스팅하는 방법을 설명합니다.

## 🚀 설정 방법

### 1단계: GitHub Secrets 등록

GitHub 저장소에서:

1. **Settings** → **Secrets and variables** → **Actions** 클릭
2. **New repository secret** 버튼 클릭
3. 다음 Secret들을 하나씩 추가:

| Secret Name | Value | 설명 |
|------------|-------|------|
| `GEMINI_API_KEY` | `AIzaSyA...` | Gemini API 키 |
| `WORDPRESS_URL` | `https://quanroot.com` | 워드프레스 블로그 URL |
| `WORDPRESS_USERNAME` | `SoulTree` | 워드프레스 사용자명 |
| `WORDPRESS_APP_PASSWORD` | `fKyz DdgT vkWx...` | 워드프레스 앱 비밀번호 |
| `WORDPRESS_CATEGORY_ID` | `1` | 카테고리 ID (선택사항) |

**중요:** 각 Secret을 추가할 때 Name과 Value를 정확히 입력하세요!

### 2단계: 워크플로우 파일 푸시

```bash
git add .github/workflows/wordpress-auto-post.yml
git commit -m "Add WordPress auto-posting workflow"
git push origin main
```

### 3단계: 워크플로우 활성화 확인

1. GitHub 저장소 페이지에서 **Actions** 탭 클릭
2. "WordPress Auto Poster" 워크플로우 확인
3. 수동 테스트: **Run workflow** 버튼 클릭

## ⏰ 실행 시간

- **한국 시간(KST)**: 매일 오전 7:00
- **UTC 시간**: 매일 오후 10:00 (전날)
- **cron 표현식**: `0 22 * * *`

## 🔧 시간 변경 방법

다른 시간에 실행하려면 `.github/workflows/wordpress-auto-post.yml` 파일의 cron 표현식을 수정:

```yaml
schedule:
  - cron: '0 22 * * *'  # 한국 시간 오전 7시
```

### 시간 변환표 (한국 → UTC)

| 한국 시간 (KST) | UTC 시간 | cron 표현식 |
|---------------|----------|------------|
| 오전 6:00 | 21:00 (전날) | `0 21 * * *` |
| 오전 7:00 | 22:00 (전날) | `0 22 * * *` |
| 오전 8:00 | 23:00 (전날) | `0 23 * * *` |
| 오전 9:00 | 00:00 | `0 0 * * *` |
| 오후 12:00 | 03:00 | `0 3 * * *` |

## 🧪 수동 실행

언제든지 수동으로 실행 가능:

1. GitHub → **Actions** 탭
2. **WordPress Auto Poster** 선택
3. **Run workflow** → **Run workflow** 버튼 클릭

## 📊 실행 로그 확인

1. **Actions** 탭
2. 최근 실행된 워크플로우 클릭
3. **post-to-wordpress** job 클릭
4. 각 단계의 로그 확인

## ⚠️ 문제 해결

### 실행이 안 될 때

1. **GitHub Secrets 확인**
   - 모든 Secret이 정확히 입력되었는지 확인
   - 특히 WORDPRESS_APP_PASSWORD의 공백 포함 여부

2. **워크플로우 권한 확인**
   - Settings → Actions → General
   - "Read and write permissions" 선택

3. **워크플로우 활성화 확인**
   - Actions 탭에서 워크플로우가 활성화되어 있는지 확인

### 포스팅은 되는데 내용이 비어있을 때

- Gemini API 키 확인
- API 할당량 확인
- 실행 로그에서 오류 메시지 확인

### 인증 오류 (401)

- WORDPRESS_APP_PASSWORD 재생성
- WORDPRESS_USERNAME 확인

## 🎯 장점

✅ **완전 자동화**: 한 번 설정하면 계속 자동 실행  
✅ **무료**: GitHub Actions 월 2,000분 무료  
✅ **안정적**: GitHub 인프라에서 실행  
✅ **로그 보관**: 모든 실행 기록 저장  
✅ **쉬운 관리**: 웹 UI에서 모니터링  

## 📝 참고사항

- GitHub Actions는 UTC 시간 기준으로 작동
- cron 실행은 약간의 지연이 있을 수 있음 (보통 5분 이내)
- 무료 플랜: 월 2,000분 제공 (하루 1회 실행은 충분)
- Private 저장소에서도 작동

## 🔐 보안

- 모든 민감한 정보는 GitHub Secrets에 저장
- config.py는 .gitignore에 포함되어 커밋되지 않음
- Secrets는 암호화되어 저장되며 로그에 표시되지 않음

## 📞 지원

문제가 발생하면:
1. Actions 탭의 실행 로그 확인
2. Secret 설정 재확인
3. 로컬에서 `python wordpress_bot.py` 테스트
