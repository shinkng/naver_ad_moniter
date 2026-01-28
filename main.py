"""
main.py

프로그램 진입점
1. requests로 빠르게 확인
2. 결과 없을 때만 selenium 전환
"""

from config import KEYWORDS
from fetchers import requests_fetcher, selenium_fetcher


def main():
    for keyword in KEYWORDS:
        print("=" * 60)
        print(f"키워드: {keyword}")

        # 1차: requests
        results = requests_fetcher.scan(keyword)

        if results:
            for r in results:
                print(f"[REQUESTS] {r.domain} / {r.rank}")
            continue

        print("requests 결과 없음 → selenium 전환")

        # 2차: selenium
        results = selenium_fetcher.scan(keyword)
        if results:
            for r in results:
                print(f"[SELENIUM] {r.domain} / {r.rank}")
        else:
            print("최종 결과 없음")


if __name__ == "__main__":
    main()
