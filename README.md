# board-skills

사외이사가 AI로 **더 나은 질문과 판단**을 준비하도록 돕는 스킬 모음입니다. 금융연수원 사외이사 과정 "더 나은 질문과 판단을 위한 AI"(120분, 교안 44장)의 내용을 실제로 쓸 수 있는 Claude 스킬로 옮겼습니다.

AI는 결론을 대신 내주는 도구가 아니라, 제한된 자료에서 근거를 확인하고 물어야 할 질문을 준비하게 돕는 도구입니다. 이 스킬들은 그 원칙을 따릅니다.

> 모든 사례와 수치는 실습용 가상 자료이며 실제 투자나 의결 판단에 쓰지 않습니다. 이 저장소는 법률·투자·금융 자문이 아닙니다.

## 스킬 목록

| 스킬 | 언제 쓰나 | 결과물 |
|---|---|---|
| [`board-agenda-review`](skills/board-agenda-review/SKILL.md) | 받은 이사회 안건을 검토할 때 | 검토 메모 1장, 우선 질문 5개, 추가 요청자료 3개 |
| [`board-number-check`](skills/board-number-check/SKILL.md) | 예산 합계, 회수기간 같은 숫자를 검증할 때 | 스크립트로 계산한 합계 대조와 실현율 민감도 |
| [`board-expert-questions`](skills/board-expert-questions/SKILL.md) | 내 전문분야 관점의 질문이 필요할 때 | 분야별 점검 부분, 질문, 요청자료, 다관점 통합 |
| [`board-compliance-check`](skills/board-compliance-check/SKILL.md) | 법령·감독 지침·모범사례와 맞는지 볼 때 | 원문 → 적용 → 대조 → 확인 표와 담당자 질문 |
| [`board-environment-brief`](skills/board-environment-brief/SKILL.md) | 금리·규제 같은 환경 변화를 읽을 때 | 변화 → 영향 경로 → 반대 시나리오 → 질문 |
| [`board-ai-safety-check`](skills/board-ai-safety-check/SKILL.md) | 자료를 AI에 넣기 전 | 입력 가능 여부 판단, 학습·보관·접근·전송 점검 |
| [`board-lecture-guide`](skills/board-lecture-guide/SKILL.md) | 이 과정을 강의하는 강사 | 시간표, 준비 체크리스트, 장별 노트, 예상 질문 |

## 설치

### Claude Code 플러그인으로 설치

```bash
/plugin marketplace add FinanceData/board-skills
/plugin install board-skills@board-skills
```

### 스킬만 복사해서 설치

`skills/` 아래 폴더를 `~/.claude/skills/`(전역) 또는 프로젝트의 `.claude/skills/`에 복사합니다.

```bash
git clone https://github.com/FinanceData/board-skills.git
cp -r board-skills/skills/* ~/.claude/skills/
```

`npx skills add FinanceData/board-skills`처럼 `skills/<이름>/SKILL.md` 구조를 읽는 도구로도 설치할 수 있습니다.

## 사용 예

처음 써 볼 때는 실제 안건 대신 가상 안건으로 연습합니다.

1. `skills/board-agenda-review/assets/sample-agenda.md`의 가상 안건을 붙여 넣습니다.
2. "이 안건을 이사회 검토 메모로 정리해 줘. 내 전문분야는 리스크야."라고 요청합니다.
3. 예산 합계가 요청액과 맞는지, 회수기간이 실현율에 따라 어떻게 달라지는지 `board-number-check`로 확인합니다.
4. 같은 파일 아래쪽의 "확인 지점"과 결과를 비교합니다.

숫자 계산 스크립트는 Python 3만 있으면 됩니다.

```bash
python skills/board-number-check/scripts/check_numbers.py sum --requested 150 개발=90 시스템연계=35 인프라=25 교육전환=15
python skills/board-number-check/scripts/check_numbers.py payback --investment 150 --benefit 45 --opex 12 --build-months 18
```

## 공통 원칙

모든 스킬이 같은 원칙을 따릅니다.

- 최종 찬반을 내지 않고, 판단에 필요한 근거를 정리합니다.
- 모든 쟁점에 근거 위치(쪽수, 원문 문구)를 붙이고, 자료에 없으면 `확인 필요`로 표시합니다.
- 미기재를 미실시로 단정하지 않습니다.
- 기대치를 실현치처럼 쓰지 않습니다.
- 규정 원문과 실제 사실관계가 없으면 법규 적합성을 확정하지 않습니다.
- AI가 만든 질문과 지적도 원문에 대조합니다. 질문의 책임은 이사에게 있습니다.
- 미공개 안건이나 고객정보는 회사가 허용한 환경이 아니면 AI에 넣지 않습니다.

## 구성

```text
.claude-plugin/        플러그인·마켓플레이스 매니페스트
skills/
  board-agenda-review/     안건 검토 (프롬프트·메모 양식·가상 안건 포함)
  board-number-check/      숫자 검증 (scripts/check_numbers.py)
  board-expert-questions/  전문분야별 질문
  board-compliance-check/  규정 검토 절차
  board-environment-brief/ 금융환경 변화 읽기
  board-ai-safety-check/   AI 입력 전 점검
  board-lecture-guide/     강의 진행 (references/lecture-notes.md)
```

강의용 HTML/PDF 교안 파일은 이 저장소에 포함하지 않았습니다.

## 라이선스

[MIT](LICENSE). 강의 교안이 사용한 Reveal.js(MIT)와 Pretendard(SIL OFL)의 라이선스는 해당 프로젝트를 따릅니다.
