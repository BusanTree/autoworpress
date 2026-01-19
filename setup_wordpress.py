"""
워드프레스 연동을 위한 초기 설정 및 테스트 스크립트
"""

import os
import json

def setup_config():
    """
    config.py 파일을 생성하고 설정을 안내합니다.
    """
    print("=" * 60)
    print("🚀 워드프레스 자동 포스팅 초기 설정")
    print("=" * 60)
    print()
    
    print("📌 필요한 정보:")
    print("1. 워드프레스 블로그 URL")
    print("2. 워드프레스 사용자명")
    print("3. 워드프레스 애플리케이션 비밀번호")
    print()
    
    print("=" * 60)
    print("📝 애플리케이션 비밀번호 생성 방법:")
    print("=" * 60)
    print()
    print("1. 워드프레스 관리자 페이지 로그인")
    print("2. 사용자 → 프로필 메뉴로 이동")
    print("3. 아래로 스크롤하여 '애플리케이션 비밀번호' 섹션 찾기")
    print("4. '새 애플리케이션 비밀번호' 이름 입력 (예: AutoBlogBot)")
    print("5. '새 애플리케이션 비밀번호 추가' 버튼 클릭")
    print("6. 생성된 비밀번호 복사 (공백 포함, 한 번만 표시됨!)")
    print()
    print("⚠️ 주의: 생성된 비밀번호는 한 번만 표시되므로 반드시 복사하세요!")
    print()
    
    # 사용자 입력 받기
    print("=" * 60)
    print("설정 시작")
    print("=" * 60)
    print()
    
    wp_url = input("워드프레스 블로그 URL (예: https://yourblog.com): ").strip()
    wp_user = input("워드프레스 사용자명 [기본값: SoulTree]: ").strip() or "SoulTree"
    wp_pass = input("워드프레스 애플리케이션 비밀번호: ").strip()
    
    # config.py 업데이트
    config_content = f'''# ==========================================
# 워드프레스 자동 포스팅 설정 파일
# ==========================================

# Gemini API 키
GEMINI_API_KEY = "AIzaSyAWFMfczRNM0nKGwCxR1-edck8caG5osG4"

# 워드프레스 블로그 정보
WORDPRESS_URL = "{wp_url}"

# 워드프레스 로그인 정보
WORDPRESS_USERNAME = "{wp_user}"
WORDPRESS_APP_PASSWORD = "{wp_pass}"

# 카테고리 ID
WORDPRESS_CATEGORY_ID = 1

# 포스트 상태 ('publish' 또는 'draft')
POST_STATUS = 'publish'
'''
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print()
    print("✅ config.py 파일이 생성되었습니다!")
    print()
    
    # .gitignore 업데이트
    gitignore_path = '.gitignore'
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        if 'config.py' not in gitignore_content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write('\n# 워드프레스 설정 (민감 정보)\nconfig.py\n')
            print("✅ .gitignore에 config.py가 추가되었습니다.")
    
    return wp_url, wp_user, wp_pass

def test_connection(wp_url, wp_user, wp_pass):
    """
    워드프레스 연결을 테스트합니다.
    """
    import requests
    import base64
    
    print()
    print("=" * 60)
    print("🔍 워드프레스 연결 테스트")
    print("=" * 60)
    print()
    
    # API 엔드포인트
    api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
    
    # 인증
    credentials = f"{wp_user}:{wp_pass}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {token}',
    }
    
    try:
        print(f"📡 연결 중: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ 연결 성공!")
            posts = response.json()
            print(f"   최근 게시물 {len(posts)}개를 찾았습니다.")
            return True
        elif response.status_code == 401:
            print("❌ 인증 실패!")
            print("   사용자명 또는 애플리케이션 비밀번호를 확인하세요.")
            return False
        elif response.status_code == 404:
            print("❌ API 엔드포인트를 찾을 수 없습니다!")
            print("   워드프레스 URL이 올바른지 확인하세요.")
            print(f"   입력한 URL: {wp_url}")
            return False
        else:
            print(f"⚠️ 예상치 못한 응답: {response.status_code}")
            print(f"   응답: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 연결 오류!")
        print("   인터넷 연결 또는 URL을 확인하세요.")
        return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def get_categories(wp_url, wp_user, wp_pass):
    """
    카테고리 목록을 조회합니다.
    """
    import requests
    import base64
    
    print()
    print("=" * 60)
    print("📂 카테고리 목록 조회")
    print("=" * 60)
    print()
    
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
            print("사용 가능한 카테고리:")
            for cat in categories:
                print(f"   ID: {cat['id']:3d} - {cat['name']} ({cat['count']}개 게시물)")
            print()
            print("💡 config.py의 WORDPRESS_CATEGORY_ID를 원하는 ID로 변경하세요.")
            return categories
        else:
            print(f"⚠️ 조회 실패: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 오류: {e}")
        return []

if __name__ == "__main__":
    wp_url, wp_user, wp_pass = setup_config()
    
    if test_connection(wp_url, wp_user, wp_pass):
        get_categories(wp_url, wp_user, wp_pass)
        
        print()
        print("=" * 60)
        print("🎉 설정 완료!")
        print("=" * 60)
        print()
        print("이제 다음 명령으로 자동 포스팅을 실행하세요:")
        print("  python wordpress_bot.py")
        print()
    else:
        print()
        print("⚠️ 연결 테스트 실패. 설정을 다시 확인하세요.")
