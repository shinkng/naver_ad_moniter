"""
database.py
DB 연결 및 기본 함수
"""

import pymysql
from contextlib import contextmanager
from typing import List, Dict
from config import DB_CONFIG
from pprint import pprint

# 캐시용
_SITE_CACHE = {}

@contextmanager
def get_db_connection():
    """DB 커넥션 컨텍스트 매니저"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


def test_connection():
    """DB 연결 테스트"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                result = cursor.fetchone()
                print(f"[SUCCESS] DB 연결 성공")
                print(f"[INFO] MySQL 버전: {result[0]}")
                print(f"[INFO] 데이터베이스: {DB_CONFIG['database']}")
                return True
    except pymysql.err.OperationalError as e:
        print(f"[ERROR] DB 연결 실패 (접속 오류)")
        print(f"[ERROR] {e}")
        return False
    except Exception as e:
        print(f"[ERROR] DB 연결 실패: {e}")
        return False



def get_site_info_cached(site_id: int):
    """
    사이트 정보 캐싱 조회 (프로세스당 1회 DB 조회)
    """
    if site_id not in _SITE_CACHE:
        sql = """
            SELECT 
                id,
                site_name,
                domain
            FROM crawler_sites
            WHERE id = %s
              AND is_active = 1
        """
        with get_db_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, (site_id,))
                _SITE_CACHE[site_id] = cursor.fetchone()

    return _SITE_CACHE[site_id]

def get_distinct_keywords(limit: int = None):
    """
    오늘 아직 크롤링 안 한 키워드만 DISTINCT 조회
    """
    sql = """
        SELECT DISTINCT ck.keyword
        FROM crawler_keywords ck
        JOIN crawler_sites cs ON cs.id = ck.crawler_site_id
        WHERE ck.is_active = 1
          AND cs.is_active = 1
          AND (
                ck.crawled_at IS NULL
                OR DATE(ck.crawled_at) < CURDATE()
          )
    """

    params = []
    if limit is not None:
        sql += " LIMIT %s"
        params.append(limit)

    with get_db_connection() as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()


def get_site_keywords_by_keyword(keyword: str):
    """
    특정 키워드를 사용하는 사이트별 키워드 row 조회
    """
    sql = """
        SELECT
            ck.id AS keyword_id,
            ck.crawler_site_id,
            cs.domain
        FROM crawler_keywords ck
        JOIN crawler_sites cs ON cs.id = ck.crawler_site_id
        WHERE ck.keyword = %s
          AND ck.is_active = 1
          AND cs.is_active = 1
    """

    with get_db_connection() as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (keyword,))
            return cursor.fetchall()



def get_active_keywords(site_id: int = None, limit: int = None) -> List[Dict]:
    """
    활성화된 키워드 목록 조회
    1. api_update_at이 크론이 도는 날짜와 같을때 == 즉 업데이트가 된 최신 키워드만
    2. crawler_at이 없거나, 오래된 애들인 경우

    Args:
        site_id: 사이트 ID (None이면 전체)
        limit: 조회 개수 제한

    Returns:
        [{
            'id': 1,
            'keyword': '파일공유',
            'crawler_site_id': 1,
            'domain': 'filecity.me',
            'crawled_at': '2025-02-03 12:00:00'
        }, ...]
    """
    sql = """
        SELECT 
            ck.id,
            ck.keyword,
            ck.crawler_site_id,
            cs.domain,
            ck.crawled_at
        FROM crawler_keywords ck
        INNER JOIN crawler_sites cs ON ck.crawler_site_id = cs.id
        WHERE ck.is_active = 1
          AND cs.is_active = 1
    """

    params = []

    if site_id is not None:
        sql += " AND ck.crawler_site_id = %s"
        params.append(site_id)

    # 오래된 것 우선 (NULL이면 제일 먼저)
    sql += " ORDER BY ck.crawled_at IS NULL DESC, ck.crawled_at ASC"

    if limit is not None:
        sql += " LIMIT %s"
        params.append(limit)

    with get_db_connection() as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results


def bulk_update_keywords(updates: List[tuple]) -> int:
    """
    배치 업데이트

    Args:
        updates: [(keyword_id, total_ads, crawl_rank), ...]

    Returns:
        affected rows
    """
    if not updates:
        return 0

    sql = """
        UPDATE crawler_keywords
        SET 
            total_ads = %s,
            crawl_rank = %s,
            crawled_at = NOW()
        WHERE id = %s
    """

    # (total_ads, crawl_rank, keyword_id) 순서로 변경
    data = [(total, rank, kid) for kid, total, rank in updates]

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            affected = cursor.executemany(sql, data)
            conn.commit()
            return affected


if __name__ == "__main__":
    print("=" * 60)
    print("DB 연결 테스트")
    print("=" * 60)

    if test_connection():
        keywords = get_active_keywords(limit=5)
        print(f"\n활성 키워드 샘플 {len(keywords)}개:")
        for kw in keywords:
            print(f"  - {kw['keyword']} (사이트: {kw['domain']})")

    print("=" * 60)