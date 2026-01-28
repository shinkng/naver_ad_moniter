"""
requests_fetcher.py

셀레니움 없이
'첫 페이지 파워링크'만 빠르게 확인한다.
"""

import requests
from bs4 import BeautifulSoup

from config import TARGET_DOMAINS, get_random_headers
from models import PowerLinkResult


def fetch_page(keyword: str) -> BeautifulSoup:
    url = "https://search.naver.com/search.naver"
    params = {
        "where": "nexearch",
        "query": keyword,
    }

    response = requests.get(
        url,
        params=params,
        headers=get_random_headers(),
        timeout=7,   # 크론 기준 살짝 여유
    )
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


def scan(keyword: str) -> list[PowerLinkResult]:
    results: list[PowerLinkResult] = []

    try:
        soup = fetch_page(keyword)
    except Exception as e:
        print(f"[ERROR][REQUESTS] {keyword} → {e}")
        return results

    items = soup.select("#power_link_body > ul > li")

    if not items:
        return results

    total = len(items)

    for idx, li in enumerate(items, start=1):
        a = li.select_one("a.lnk_url")
        if not a:
            continue

        domain = a.get_text(strip=True).rstrip("/")

        if domain in TARGET_DOMAINS:
            results.append(
                PowerLinkResult(
                    keyword=keyword,
                    domain=domain,
                    rank=idx,
                    total=total,
                    source="requests",
                )
            )

    return results
