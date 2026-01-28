"""
main.py

프로그램 진입점
1. requests로 빠르게 확인
2. 결과 없을 때만 selenium 전환
"""

import time
import random

from config import KEYWORDS
from fetchers import requests_fetcher, selenium_fetcher


def main():
    for i, keyword in enumerate(KEYWORDS, start=1):
        print("=" * 60)
        print(f"[{i}/{len(KEYWORDS)}] 키워드: {keyword}")

        results, total = requests_fetcher.scan(keyword)
        print(f"파워링크 총 {total}개") # 수가 다른경우는

        if results:
            for r in results:
                print(f"[REQUESTS] {r.rank}위 - {r.domain}")
        else:
            print("타겟 도메인 노출 없음")

        # 봇 패턴 방지 딜레이
        sleep_sec = random.uniform(1.5, 3.5)
        time.sleep(sleep_sec)

        # print("requests 결과 없음 → selenium 전환")
        #
        # # 2차: selenium
        # results = selenium_fetcher.scan(keyword)
        # if results:
        #     for r in results:
        #         print(f"[SELENIUM] {r.domain} / {r.rank}")
        # else:
        #     print("최종 결과 없음")


if __name__ == "__main__":
    main()
