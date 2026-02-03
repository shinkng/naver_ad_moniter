"""
crawler.py
메인 크롤러 실행 파일 (키워드 1회 크롤링 구조)
"""

import sys
import time
from datetime import datetime
from pprint import pprint

from fetchers.requests_fetcher import scan_all_domains, normalize_domain
from database import (
    get_distinct_keywords,
    get_site_keywords_by_keyword,
    bulk_update_keywords,
)
from config import CRAWL_DELAY, BATCH_SIZE


def crawl_keywords(limit: int = None):
    start_time = datetime.now()

    print("=" * 60)
    print(f"키워드 크롤링 시작: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("방식: 키워드 1회 크롤링 → 사이트별 매핑")
    if limit:
        print(f"제한 개수: {limit}개")
    print("=" * 60)

    keywords = get_distinct_keywords(limit)

    if not keywords:
        print("[WARNING] 크롤링할 키워드가 없습니다")
        return

    total_count = len(keywords)
    print(f"[INFO] 크롤링 대상 키워드: {total_count}개\n")

    updates = []
    success_count = 0
    error_count = 0

    for idx, row in enumerate(keywords, 1):
        keyword = row["keyword"]
        progress = (idx / total_count) * 100

        print(f"[{idx}/{total_count}] ({progress:.1f}%) {keyword}")

        try:
            scan_result, total_ads = scan_all_domains(keyword)
            site_keywords = get_site_keywords_by_keyword(keyword)

            keyword_has_rank = False

            for sk in site_keywords:
                keyword_id = sk["keyword_id"]
                domain = normalize_domain(sk["domain"])
                rank = scan_result.get(domain)

                if rank:
                    keyword_has_rank = True

                updates.append((keyword_id, total_ads, rank))

            if keyword_has_rank:
                success_count += 1

            if len(updates) >= BATCH_SIZE:
                affected = bulk_update_keywords(updates)
                print(f"  [DB] {affected}개 저장 완료\n")
                updates = []

            if idx < total_count:
                time.sleep(CRAWL_DELAY)

        except Exception as e:
            print(f"  [ERROR] {e}")
            error_count += 1

    if updates:
        affected = bulk_update_keywords(updates)
        print(f"\n[DB] 마지막 {affected}개 저장 완료")

    end_time = datetime.now()
    elapsed = end_time - start_time

    print("\n" + "=" * 60)
    print("크롤링 완료")
    print("=" * 60)
    print(f"시작 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"종료 시간: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"소요 시간: {elapsed}")
    print(f"키워드 수: {total_count}개")
    print(f"순위 발견: {success_count}개")
    print(f"에러: {error_count}개")
    print("=" * 60)


if __name__ == "__main__":

    # python crawler.py
    # python crawler.py 1000
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])

    crawl_keywords(limit)
