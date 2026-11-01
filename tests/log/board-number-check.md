# board-number-check 테스트 실행 기록

- 결과 문서: [../results/board-number-check.md](../results/board-number-check.md)

### 읽은 파일
1. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-number-check\SKILL.md` (전체)
2. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-number-check\scripts\check_numbers.py` (실행 방법 확인용)
3. `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\tests\fixtures\doam-board-agenda.pdf` (5쪽 전체)

읽지 않은 파일: `references/worked-example.md`, `tests\results-v1` 및 tests 폴더의 다른 파일. 스킬 폴더 파일 목록만 Glob으로 확인했습니다.

### 실행한 명령과 전체 출력
모든 명령은 Bash(Git Bash)에서 `S="C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py"`로 경로를 지정하고 `python -I "$S" ...` 형태로 실행했습니다. 아래에는 `$S`를 풀어 쓴 전체 명령을 적습니다.

**명령 1** — 예산 합계(원래 단위)
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py sum --unit "백만 원" --requested 12000 플랫폼개발=5200 신용평가모형구축=2800 클라우드인프라=1900 정보보호=1300 마케팅=1600
```
```
[합계 점검]
  플랫폼개발             5,200 백만 원
  신용평가모형구축          2,800 백만 원
  클라우드인프라           1,900 백만 원
  정보보호              1,300 백만 원
  마케팅               1,600 백만 원
  합계               12,800 백만 원
  승인 요청액         12,000 백만 원
  결과: 합계가 승인 요청액보다 800 백만 원 큽니다.
  주의: 원인(계산 오류, 중복 항목, 별도 예산, 부가세·예비비 포함 범위)은
        자료만으로 알 수 없습니다. 원인을 단정하지 말고 두 값을 맞춘
        조정표를 요청하십시오.
exit=1
```

**명령 2** — 예산 합계(억 원 변환)
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py sum --requested 120 플랫폼개발=52 신용평가모형구축=28 클라우드인프라=19 정보보호=13 마케팅=16
```
```
[합계 점검]
  플랫폼개발                52 억 원
  신용평가모형구축             28 억 원
  클라우드인프라              19 억 원
  정보보호                 13 억 원
  마케팅                  16 억 원
  합계                  128 억 원
  승인 요청액            120 억 원
  결과: 합계가 승인 요청액보다 8 억 원 큽니다.
  주의: 원인(계산 오류, 중복 항목, 별도 예산, 부가세·예비비 포함 범위)은
        자료만으로 알 수 없습니다. 원인을 단정하지 말고 두 값을 맞춘
        조정표를 요청하십시오.
exit=1
```

**명령 3** — 1년 차 영업이익 기여
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py sum --label "표 기재 영업이익 기여" --requested 16 순이자이익=24 대손비용=-8
```
```
[합계 점검]
  순이자이익                24 억 원
  대손비용                 -8 억 원
  합계                   16 억 원
  표 기재 영업이익 기여         16 억 원
  결과: 일치합니다(합계 = 표 기재 영업이익 기여).
exit=0
```

**명령 4** — 2년 차 영업이익 기여
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py sum --label "표 기재 영업이익 기여" --requested 22 순이자이익=36 대손비용=-14
```
```
[합계 점검]
  순이자이익                36 억 원
  대손비용                -14 억 원
  합계                   22 억 원
  표 기재 영업이익 기여         22 억 원
  결과: 일치합니다(합계 = 표 기재 영업이익 기여).
exit=0
```

**명령 5** — 3년 차 영업이익 기여
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py sum --label "표 기재 영업이익 기여" --requested 27 순이자이익=45 대손비용=-18
```
```
[합계 점검]
  순이자이익                45 억 원
  대손비용                -18 억 원
  합계                   27 억 원
  표 기재 영업이익 기여         27 억 원
  결과: 일치합니다(합계 = 표 기재 영업이익 기여).
exit=0
```

**명령 6** — 운영비 내역
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py sum --label "안건 기재 운영비" --requested 9 클라우드이용료=6 모형검증유지보수=3
```
```
[합계 점검]
  클라우드이용료               6 억 원
  모형검증유지보수              3 억 원
  합계                    9 억 원
  안건 기재 운영비           9 억 원
  결과: 일치합니다(합계 = 안건 기재 운영비).
exit=0
```

**명령 7** — 파일럿 승인율
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py ratio 40 65 --stated 61.5
```
```
[비율 점검]
  분자  40
  분모  65
  결과: 61.54%
  안건 기재값: 61.5%
  대조: 반올림 범위(±0.05%p) 안에서 일치합니다.
exit=0
```

**명령 8** — 회수기간
```
python -I C:/Users/plusj/OneDrive/Desktop/skills/board-skills/skills/board-number-check/scripts/check_numbers.py payback --investment 120 --benefit 36 --opex 9 --credit-cost 14 --build-months 12
```
```
[단순 회수기간 계산]
  투자금(전액 선투자 가정) 120 억 원
  연간 기대 총편익         36 억 원
  편익 실현율              100% (총편익에만 적용)
  연간 운영비              9 억 원
  연간 대손비용            14 억 원
  구축 기간                12개월
  연간 실현 편익           36 억 원
  연간 순편익              13 억 원
  결과: 출시 후 약 9.23년
        구축 기간을 더하면 약 10.23년
  참고: 운영비·대손비용을 빠뜨린 잘못된 계산은 3.33년으로 나옵니다.

[실현율 민감도] (실현율은 총편익에만 적용)
     실현율        순편익        출시 후 회수        구축 포함
    100%         13          9.23년       10.23년
     80%        5.8         20.69년       21.69년
     60%       -1.4         회수 불성립            -
     40%       -8.6         회수 불성립            -

주의: 할인, 세금, 편익이 늘어나는 과정, 투자 지출 시점을 반영하지 않은
      단순 민감도입니다. NPV나 경제성 승인의 근거로 쓰지 않습니다.
exit=0
```

(참고: 명령 1은 실행 시 명령 문자열을 echo로 함께 출력했고, 명령 2~8은 한 번의 Bash 호출에서 `### 번호` 구분선을 echo하며 연속 실행했습니다. 위 출력은 구분선을 뺀 스크립트 출력 전문입니다.)
