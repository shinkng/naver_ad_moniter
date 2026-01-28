"""
selenium_fetcher.py

requests 방식에서 파워링크를 못 찾았을 때만 사용하는 fallback.
URL 파라미터 방식으로 접근해 input 조작 에러를 원천 차단한다.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import TARGET_DOMAINS
from models import PowerLinkResult


def scan(keyword: str) -> list[PowerLinkResult]:
    # 크롬 옵션 설정
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    results: list[PowerLinkResult] = []

    try:
        # 검색어를 URL 파라미터로 직접 전달
        search_url = f"https://search.naver.com/search.naver?query={keyword}"
        driver.get(search_url)

        # 파워링크 영역 로딩 대기
        time.sleep(2)

        # 파워링크 아이템 전체 수집
        items = driver.find_elements(
            By.CSS_SELECTOR,
            "#power_link_body ul li"
        )

        for idx, li in enumerate(items, start=1):
            try:
                # 파워링크에 표시되는 도메인 추출
                domain = li.find_element(
                    By.CSS_SELECTOR,
                    "a.lnk_url"
                ).text.strip().rstrip("/")

                # 타겟 도메인인지 체크
                if domain in TARGET_DOMAINS:
                    results.append(
                        PowerLinkResult(
                            keyword=keyword,
                            domain=domain,
                            rank=idx,
                            source="selenium",
                        )
                    )
            except Exception:
                # 광고 포맷이 다른 경우 무시
                continue

    finally:
        driver.quit()

    return results
