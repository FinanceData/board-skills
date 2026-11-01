# board-skills

임원 및 사외이사가 AI로 **더 나은 질문과 판단**을 준비하도록 돕는 스킬 모음입니다. 

각 `SKILL.md`는 에이전트가 그대로 따를 수 있도록 **실행 절차(명령형 지시), 금지 규칙과 예외 처리, 입력·출력 예시, 자유도(매뉴얼대로 할 영역과 판단해도 되는 영역)**로 구성했습니다. `references/`, `assets/`, `scripts/`의 가상 사례 파일은 모두 **테스트 예시**입니다.

AI는 결론을 대신 내주는 도구가 아니라, 제한된 자료에서 근거를 확인하고 물어야 할 질문을 준비하게 돕는 도구입니다. 이 스킬들은 그 원칙을 따릅니다.

> 모든 사례와 수치는 실습용 가상 자료이며 실제 투자나 의결 판단에 쓰지 않습니다. 이 저장소는 법률·투자·금융 자문이 아닙니다.

## 스킬 목록

| 스킬 | 언제 쓰나 | 결과물 |
|---|---|---|
| [`board-agenda-review`](skills/board-agenda-review/SKILL.md) | 이사회 안건을 검토할 때 | 검토 메모 1장, 우선 질문 5개, 추가 요청자료 3개 |
| [`board-number-check`](skills/board-number-check/SKILL.md) | 회수기간 같은 숫자를 검증 | 계산한 합계·비율 대조와 회수기간 민감도 |
| [`board-expert-questions`](skills/board-expert-questions/SKILL.md) | 내 전문분야 관점의 질문이 필요할 때 | 분야별 점검, 질문, 요청자료 |
| [`board-compliance-check`](skills/board-compliance-check/SKILL.md) | 법령·감독 지침과 맞는지 볼 때 | 원문 → 적용 → 대조 → 확인 표와 담당자 질문 |
| [`board-environ`](skills/board-environ/SKILL.md) | 금리·규제 같은 환경 변화 검토 | 변화 → 영향 경로 → 반대 시나리오 → 질문 |
| [`board-ai-safety-check`](skills/board-ai-safety-check/SKILL.md) | 자료를 AI에 안전 점검  | 입력 가능 여부 판단, 학습·보관·접근·전송 점검 |

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

### Claude 외 다른 AI에 설치

이 저장소의 스킬은 `skills/<이름>/SKILL.md`(이름과 설명 메타데이터 + 마크다운 지침) 형식이라 Agent Skills를 지원하는 도구에서 그대로 쓸 수 있습니다. 도구마다 스킬을 읽는 폴더만 다릅니다.

#### 한 번에 설치: `npx skills`

Node.js 22.20 이상이 필요합니다. 대상 도구는 `-a`로 지정하고, 전역 설치는 `-g`를 붙입니다. `-a`를 생략하면 설치할 도구를 고르는 화면이 나옵니다.

```bash
npx skills add FinanceData/board-skills -a codex
```

`-a`에는 `claude-code`, `codex`, `cursor`, `gemini-cli`, `github-copilot`, `opencode`, `windsurf`, `antigravity` 등을 쓸 수 있습니다. 스킬 하나만 설치하려면 `--skill board-agenda-review`를 붙입니다.

#### 도구별 폴더에 직접 복사

먼저 저장소를 받습니다.

```bash
git clone https://github.com/FinanceData/board-skills.git
```

그다음 `board-skills/skills/*`를 아래 폴더에 복사합니다.

| 도구 | 프로젝트 폴더 | 전역 폴더 |
|---|---|---|
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.agents/skills/` 또는 `.cursor/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` 또는 `.agents/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |
| OpenCode | `.agents/skills/` | `~/.config/opencode/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |

예: Codex에 전역 설치(macOS·Linux·Git Bash)

```bash
mkdir -p ~/.agents/skills && cp -r board-skills/skills/* ~/.agents/skills/
```

예: Codex에 전역 설치(Windows PowerShell)

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"; Copy-Item -Recurse -Force board-skills\skills\* "$HOME\.agents\skills\"
```

설치 후 안내:
- 새로 넣은 스킬이 안 보이면 해당 도구를 다시 시작합니다.
- Codex에서는 `/skills`를 실행하거나 `$board-agenda-review`처럼 `$`와 스킬 이름으로 부를 수 있습니다. Cursor는 Agent 채팅에서 `/`를 입력해 고릅니다. 그 밖에는 요청 내용이 스킬 설명과 맞으면 도구가 알아서 고릅니다.
- Gemini CLI는 `gemini skills link board-skills/skills`로 복사 없이 연결할 수도 있습니다.
- 위 폴더 경로는 2026년 10월 31일에 각 도구의 공식 문서와 `npx skills`의 문서로 확인했습니다. 도구가 업데이트되면 달라질 수 있으니 안 되면 해당 도구의 Skills 문서를 확인하세요.

#### 스킬을 지원하지 않는 챗봇 (ChatGPT, Gemini, Claude 웹·앱 등)

스킬 폴더를 읽지 못하는 환경에서는 `SKILL.md` 내용을 지침으로 붙여 넣어 씁니다.

1. 쓰려는 스킬의 `SKILL.md`에서 맨 위 `---` 사이의 메타데이터를 뺀 본문을 복사합니다.
2. 새 대화의 첫 메시지나 프로젝트(또는 Gem, 맞춤 GPT)의 지침 칸에 붙여 넣습니다.
3. 안건 검토에는 `skills/board-agenda-review/references/prompt-template.md`의 공통 프롬프트를 그대로 쓰는 편이 가장 간단합니다.
4. 스킬이 가리키는 참고 파일(`references/` 등)이 필요하면 그 내용도 같이 붙여 넣거나 파일로 올립니다.

주의: `board-number-check`의 계산 스크립트는 코드를 실행할 수 있는 환경(터미널 에이전트, 코드 실행 기능이 있는 챗봇)에서만 돌아갑니다. 코드 실행이 없으면 `references/worked-example.md`의 계산식을 따라 직접 계산하거나 계산기로 확인하고, AI의 암산 결과를 그대로 믿지 마세요.

미공개 안건이나 고객정보는 어떤 도구를 쓰든 회사가 허용한 환경이 아니면 넣지 않습니다(`board-ai-safety-check` 참고).

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
  board-environ/           금융환경 변화 읽기
  board-ai-safety-check/   AI 입력 전 점검
```

## 라이선스

[MIT](LICENSE)
