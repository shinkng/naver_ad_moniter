# Naver PowerLink Checker

이 프로젝트는 네이버 검색 결과의 파워링크 광고 영역에서  
특정 도메인이 노출되는지 여부와 노출 시 **순위(rank)**를 확인

requests 기반의 빠른 방식으로 먼저 확인하고,  
결과가 없을 경우에만 Selenium을 사용하는 2단계 구조로 설계됨

---

## 프로젝트 배경 및 설계 의도

네이버 파워링크 영역은 다음과 같은 특성이 있습니다.

- HTML 구조가 자주 변경됨
- requests 방식으로는 모든 케이스를 안정적으로 처리하기 어려움
- Selenium만 사용하면 속도가 느리고 리소스 소모가 큼

이를 해결하기 위해 다음과 같은 전략을 사용합니다.

- 1차: requests로 첫 페이지 파워링크만 빠르게 확인
- 2차: requests에서 결과가 없을 때만 Selenium으로 보조 확인

이 구조를 통해 속도와 안정성의 균형을 맞춥니다.

---

## 디렉토리 구조

```text
project/
├─ main.py                     # 프로그램 진입점
├─ config.py                   # 키워드 / 타겟 도메인 / 헤더 설정
├─ models.py                   # 결과 데이터 모델
├─ README.md
│
├─ fetchers/
│   ├─ __init__.py
│   ├─ requests_fetcher.py     # 1차: requests 기반 파워링크 스캔
│   └─ selenium_fetcher.py     # 2차: Selenium fallback
│
└─ requirements.txt