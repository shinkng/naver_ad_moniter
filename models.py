"""
models.py

파워링크 결과를 dict로 쓰지 않고
dataclass로 정의하는 이유:

1. 필드가 명확해진다
2. IDE 자동완성
3. 나중에 DB / JSON 변환 쉬움
"""

from dataclasses import dataclass

@dataclass(slots=True)
class PowerLinkResult:
    # 검색 키워드
    keyword: str

    # 광고에 표시된 도메인 (filecity.me 등)
    domain: str

    # 파워링크 내 순위 (1부터 시작)
    rank: int

    # 결과를 가져온 방식 (requests / selenium)
    source: str
