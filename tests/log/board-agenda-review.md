# board-agenda-review 테스트 실행 기록

- 결과 문서: [../results/board-agenda-review.md](../results/board-agenda-review.md)

### 읽은 파일
1. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-agenda-review\SKILL.md`
2. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-agenda-review\references\review-memo-template.md`
3. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-agenda-review\references\pitfalls.md`
4. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-agenda-review\references\prompt-template.md`
5. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-number-check\SKILL.md`
6. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\tests\fixtures\doam-board-agenda.pdf` (5쪽)

읽지 않은 파일: `assets\sample-agenda.md`, `board-number-check\references\worked-example.md`, `tests\results-v1\*` (지시에 따라 제외). `check_numbers.py` 소스는 열지 않고 `--help`로 사용법만 확인. 디렉터리 목록 확인: skill 폴더 Glob, `tests\`·`tests\results-v2\` ls(출력 폴더 존재 확인용).

### 실행한 명령과 핵심 출력
스크립트 경로 `S=C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py`, 모두 `python -I "$S" ...`로 실행.

| # | 명령(인자) | 핵심 출력 |
|---|---|---|
| 0 | `--help`, `sum --help`, `ratio --help`, `payback --help` | 최상위·`ratio` 도움말은 argparse `ValueError: unsupported format character ')'`로 실패(help 문자열의 `%` 미이스케이프로 추정되는 스크립트 결함). `sum`·`payback` 도움말은 정상 출력 |
| 1 | `sum --requested 12000 --unit "백만 원" 플랫폼개발=5200 신용평가모형구축=2800 클라우드인프라=1900 정보보호=1300 마케팅=1600` | 합계 12,800 백만 원, "합계가 승인 요청액보다 800 백만 원 큽니다." |
| 2 | 위와 같음 + `--label "표 기재 합계"` | "합계가 표 기재 합계보다 800 백만 원 큽니다." |
| 3 | `ratio 40 65 --stated 61.5` | 61.54%, "반올림 범위(±0.05%p) 안에서 일치합니다." |
| 4 | `payback --investment 120 --benefit 36 --no-sensitivity` | 출시 후 약 3.33년 (안건 산식 재현) |
| 5 | `payback --investment 120 --benefit 36 --opex 9 --credit-cost 14 --build-months 12` | 연간 순편익 13, 출시 후 약 9.23년, 구축 포함 약 10.23년. 민감도: 80% → 5.8 / 20.69년 / 21.69년, 60% → -1.4 회수 불성립, 40% → -8.6 회수 불성립 |
| 6 | `sum --requested 16 --label "표 기재 영업이익 기여(2028)" 순이자이익=24 대손비용=-8` | 일치(16) |
| 7 | `sum --requested 22 --label "표 기재 영업이익 기여(2029)" 순이자이익=36 대손비용=-14` | 일치(22) |
| 8 | `sum --requested 27 --label "표 기재 영업이익 기여(2030)" 순이자이익=45 대손비용=-18` | 일치(27) |
| 9 | `sum --requested 9 --label "표 기재 연간 운영비" 클라우드이용료=6 모형검증유지보수=3` | 일치(9) |
| 10 | `sum --requested 120 --label "총사업비" 영업이익기여2028=16 영업이익기여2029=22 영업이익기여2030=27` | 합계 65, "총사업비보다 55 억 원 작습니다." (스크립트의 '원인 단정 금지' 주의 문구도 출력되나, 이 항목은 불일치가 아닌 비교값으로만 사용) |
| 11 | `sum --unit "%" 평균대출금리=10.5 평균조달금리=-3.4` | 합계 7.1 % |
| 12 | `ratio 36 1100` | 3.27% |

### 스킬 적용 메모
- 1단계: 문서가 '대외비' 표기된 이사회 안건이고 사용자가 허용 환경을 밝히지 않아 첫 줄에 허용 환경 확인 문구를 넣음(문서에는 가상 문서 표기가 있으나 사용자는 실제 안건으로 제시).
- 예외 처리: "승인해도 되겠지?" → 지정 문구로 답하고 절차대로 진행. 찬반 표현 미사용.
- 전문분야(재무·회계)가 주어져 "전문분야를 알려 주시면…" 문구는 생략.
- 첨부 1 고객 사례는 성명이 이미 일부 가려져 있고 실명·계좌번호·주민번호는 보이지 않아 `[고객정보]` 마스킹 대상 인용은 없음. 사례 자체를 인용하지 않음.
- 계산 결과는 전부 스크립트 출력값을 그대로 옮김. 억 원↔백만 원 단위 변환만 본문에 명시.
