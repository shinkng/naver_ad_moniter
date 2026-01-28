"""
config.py

이 파일은 '설정 전용' 파일이다.
비즈니스 로직이 들어가면 안 된다.

나중에:
- 키워드 추가
- 도메인 변경
- 요청 횟수 조절
같은 작업을 코드 수정 없이 여기서만 하게 된다.
"""

# 검색할 키워드 목록
KEYWORDS = [
    "경도를 기다리며 ott",
    "ott",
    "무료영화",
]

# 파워링크에서 추적할 도메인
TARGET_DOMAINS = [
    "filecity.me",
    "fileis.co",
]

# requests 요청 시 사용할 HTTP 헤더
# 네이버는 User-Agent / Referer 없으면 결과를 비워주는 경우가 많다
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

# requests 방식에서 더보기(page) 몇 페이지까지 볼지
# 너무 크게 잡으면 차단 리스크 증가
MAX_PAGE = 2
