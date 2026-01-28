import requests
from bs4 import BeautifulSoup

keywords = [
    "경도를 기다리며 ott",
    "무료영화",
    "ott"
]

target_domains = ["filecity.me", "fileis.co"]

base_url = "https://search.naver.com/search.naver"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

results = []

for keyword in keywords:
    params = {
        'where': 'nexearch',
        'query': keyword
    }

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    power_links = soup.select('#power_link_body > ul > li')

    print(f"\n{'='*80}")
    print(f"키워드: {keyword}")

    # 1 파워링크 존재 여부
    if not power_links:
        print("파워링크 없음")
        continue

    print(f"파워링크 존재 (총 {len(power_links)}개)")

    # 2 순번 + 도메인 추출
    for idx, li in enumerate(power_links, start=1):
        a = li.select_one('a.lnk_url')
        if not a:
            continue

        domain = a.get_text(strip=True).rstrip('/')

        # 3 타겟 도메인인지 체크
        if domain in target_domains:
            result = {
                'keyword': keyword,
                'domain': domain,
                'rank': idx
            }
            results.append(result)

            print(f"🎯 발견: {domain} → {idx}번째")

# 최종 요약
print(f"\n{'='*80}")
print("최종 결과 요약")

if not results:
    print("타겟 도메인 노출 없음")
else:
    for r in results:
        print(
            f"키워드='{r['keyword']}' | "
            f"도메인='{r['domain']}' | "
            f"순위={r['rank']}"
        )
