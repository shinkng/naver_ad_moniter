"""
requests_fetcher.py

셀레니움 없이
'첫 페이지 파워링크'만 빠르게 확인한다.
"""

import requests
from bs4 import BeautifulSoup

from config import HEADERS, TARGET_DOMAINS
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
        headers=HEADERS,
        timeout=5,
    )
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


def scan(keyword: str) -> list[PowerLinkResult]:
    results: list[PowerLinkResult] = []

    soup = fetch_page(keyword)

    items = soup.select("#power_link_body > ul > li")
    if not items:
        return results

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
                    source="requests",
                )
            )

    return results
