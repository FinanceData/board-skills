# board-environ 테스트 실행 기록

- 결과 문서: [../results/board-environ.md](../results/board-environ.md)

**읽은 파일**
- `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-environ\SKILL.md` (전체)
- `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\tests\fixtures\doam-board-agenda.pdf` (5쪽 전체)
- `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-number-check\SKILL.md` (스크립트 사용법 확인용; `references\worked-example.md`는 열지 않음)
- `tests\` 폴더 목록만 확인(출력 폴더 존재 확인용). `results-v1` 등 다른 파일은 열지 않음.

**웹 검색/열람 (총 8회)**
1. WebSearch: "한국은행 통화정책방향 기준금리 결정 2026년 10월" — 성공. 결과는 대부분 언론·블로그(공식 자료 아님)여서 본문 수치 근거로 쓰지 않음.
2. WebFetch: https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643 — 성공(기준금리 추이 표).
3. WebSearch (allowed_domains: bok.or.kr): "bok.or.kr 통화정책방향 2026년 10월 22일 기준금리 3.00% 유지" — 성공(공식 URL 확보. 검색 요약 수치는 직접 열람한 페이지로 다시 확인함).
4. WebFetch: https://www.bok.or.kr/portal/bbs/P0000559/view.do?nttId=11064191&menuNo=200690&programType=newsData&relate=Y&depth=200690 (통화정책방향 2026.8.27) — 성공.
5. WebFetch: https://www.bok.or.kr/portal/main/main.do — 성공(10.22 게시물 nttId 확인).
6. WebFetch: https://www.bok.or.kr/portal/bbs/P0000559/view.do?nttId=11065823&...&menuNo=200690&oldMenuNo=201263 (통화정책방향 2026.10.22) — 성공.
7. WebSearch (allowed_domains: fss.or.kr, fsc.go.kr, korea.kr): "금융감독원 2026년 상반기 저축은행 영업실적 연체율 보도자료" — 성공했으나 목표 자료(금감원 저축은행 영업실적) 없음. 검색 요약의 2024년 말 업권 연체율 수치는 원문을 열지 않아 메모에 쓰지 않음.
8. WebFetch: https://fsc.go.kr/no010101/87675?...(2026년 8월 가계대출 동향, 2026.9.9) — 성공. 도구가 일부를 요약·재구성해 반환했음을 밝혀 둠(인용문 외).

참고: WebFetch는 페이지를 모델이 요약해 돌려주는 방식이라, 수치는 그 추출 결과를 기준으로 적었다.

**스크립트 실행** (작업 폴더: `skills\board-number-check\scripts`)
- `python -I check_numbers.py --help` — 실패(argparse 도움말 문자열의 `%` 처리 오류: `ValueError: unsupported format character ')'`). 스크립트 버그로 보임.
- `python -I check_numbers.py sum --help` — 성공.
- `python -I check_numbers.py sum --requested 2.25 --label "안건 가정 기준금리" --unit "%" 현행기준금리=3.00` → "합계가 안건 가정 기준금리보다 0.75 % 큽니다." (불일치 시 종료 코드 1)
- `python -I check_numbers.py sum --unit "%" 평균대출금리=10.5 평균조달금리=-3.4` → "합계 7.1 %"
- `python -I check_numbers.py sum --requested 2.50 --label "2026.7.16 인상 전 기준금리" --unit "%" 현행기준금리=3.00` → "합계가 2026.7.16 인상 전 기준금리보다 0.5 % 큽니다."
- 비고: 금리 차이 계산에 `sum` 하위 명령을 썼더니 "원인(계산 오류, 중복 항목, 별도 예산, 부가세·예비비…)" 같은 예산용 주의 문구가 함께 나옴. 금리 차이(%p) 전용 하위 명령이 없어 단위 표기가 "%"로 출력됨.
