"""
requests_fetcher.py
셀레니움 없이 첫 페이지 파워링크만 빠르게 확인
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import get_random_headers


def normalize_domain(domain: str) -> str:
    if not domain:
        return ""

    domain = domain.strip().lower()

    if domain.startswith("http"):
        parsed = urlparse(domain)
        domain = parsed.netloc or parsed.path

    domain = domain.replace("www.", "").rstrip("/")
    return domain


session = requests.Session()

def fetch_page(keyword: str) -> BeautifulSoup:
    response = session.get(
        "https://search.naver.com/search.naver",
        params={"where": "nexearch", "query": keyword},
        headers=get_random_headers(),
        timeout=7,
    )
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scan_all_domains(keyword: str) -> tuple[dict, int]:
    """
    키워드 1회 크롤링 → 전체 도메인 순위 반환

    return:
        (
            {
                "filecity.me": 1,
                "filecast.co": 2,
            },
            total_ads
        )
    """
    try:
        soup = fetch_page(keyword)
    except Exception as e:
        print(f"[ERROR][REQUESTS] {keyword} → {e}")
        return {}, 0

    # TODO 추후 네이버에서 바뀔수있음..
    items = soup.select("ul.lst_type > li.lst")
    if not items:
        return {}, 0

    total_ads = len(items)

    result = {}

    for idx, li in enumerate(items, start=1):
        a = li.select_one("a.lnk_url")
        if not a:
            continue

        raw_domain = a.get_text(strip=True)
        domain = normalize_domain(raw_domain)

        # 같은 도메인 중복 광고 방지
        if domain not in result:
            result[domain] = idx

    return result, total_ads
