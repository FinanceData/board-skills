# board-expert-questions 테스트 실행 기록

- 결과 문서: [../results/board-expert-questions.md](../results/board-expert-questions.md)

### 읽은 파일

1. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-expert-questions\SKILL.md` (전체)
2. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-expert-questions\references\perspectives.md` (테스트 예시, 방식만 참고)
3. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\tests\fixtures\doam-board-agenda.pdf` (5쪽 전체)
4. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-number-check\SKILL.md` (스크립트 사용법 확인)

읽지 않은 파일: `board-number-check\references\worked-example.md`, `tests\results-v1` 및 그 밖의 `tests\` 하위 파일, `check_numbers.py` 소스.

### 실행한 명령 (모두 `python -I`, 스크립트 경로 `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-number-check\scripts\check_numbers.py`)

| 명령 | 핵심 출력 |
|---|---|
| `--help` | 실패: argparse `ValueError: unsupported format character ')' (0x29) at index 4` (help 문자열에 이스케이프되지 않은 `%`가 있는 것으로 보임). 하위 명령 실행에는 영향 없음 |
| `sum --requested 12000 --unit "백만 원" 플랫폼개발=5200 신용평가모형=2800 클라우드인프라=1900 정보보호=1300 마케팅=1600` | 합계 12,800 백만 원, 승인 요청액 12,000 백만 원, "합계가 승인 요청액보다 800 백만 원 큽니다" |
| `payback --investment 120 --benefit 36 --opex 9 --credit-cost 14 --build-months 12` | 순편익 13억 원, 출시 후 약 9.23년, 구축 포함 약 10.23년, 비용 누락 시 3.33년. 실현율 80% → 20.69년(구축 포함 21.69년), 60% → 순편익 -1.4 회수 불성립, 40% → 회수 불성립 |
| `payback --investment 120 --benefit 36 --opex 0 --credit-cost 0` | 출시 후 약 3.33년(안건 산식 재현용) |
| `ratio 40 65 --stated 61.5` | 61.54%, 반올림 범위(±0.05%p) 안에서 일치 |
| `ratio 1300 12000` | 10.83% |
| `sum --requested 16 --label "표 기재 영업이익 기여(2028)" --unit "억 원" 순이자이익=24 대손비용=-8` | 16, 일치 |
| `sum --requested 22 --label "표 기재 영업이익 기여(2029)" --unit "억 원" 순이자이익=36 대손비용=-14` | 22, 일치 |
| `sum --requested 27 --label "표 기재 영업이익 기여(2030)" --unit "억 원" 순이자이익=45 대손비용=-18` | 27, 일치 |
| `sum --requested 9 --label "안건 기재 연간 운영비" --unit "억 원" 클라우드이용료=6 모형검증유지보수=3` | 9, 일치 |

### 스킬 적용 메모

- 사용자가 분야(IT·보안)를 밝혀서 A-1의 되묻기는 생략했다.
- 옆 분야는 준법으로 골랐다(자유도 영역).
- 통합 질문 5개 이내 규칙에 맞추려고 리스크의 '중단 기준'은 2번 질문에, IT·보안의 '장애 복구'는 4번 질문에 합쳤다.
- 관점별 결과가 모두 같지는 않아 예외 문구("공통 오류 가능성")는 같은 방향으로 본 쟁점(회수기간)에만 한 줄로 붙였다.
- 단위 변환(백만 원 → 억 원)은 자릿수 변환만 했고, 그 외 수치는 스크립트 출력값을 그대로 옮겼다.
