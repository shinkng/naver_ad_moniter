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
import random

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
HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Accept-Language": "ko-KR,ko;q=0.9",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Edg/122.0.0.0",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
    },
]

def get_random_headers():
    return random.choice(HEADERS_LIST)

# requests 방식에서 더보기(page) 몇 페이지까지 볼지
# 너무 크게 잡으면 차단 리스크 증가
MAX_PAGE = 2
