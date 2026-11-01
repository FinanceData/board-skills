# board-compliance-check 테스트 실행 기록

- 결과 문서: [../results/board-compliance-check.md](../results/board-compliance-check.md)

**읽은 파일**
- `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\skills\board-compliance-check\SKILL.md` (성공)
- `C:\Users\plusj\OneDrive\Desktop\skills\board-skills\tests\fixtures\doam-board-agenda.pdf` (성공, 5쪽)
- tests 폴더의 다른 파일은 열지 않음

**스킬 호출·명령**
1. Skill `korean-law-search` 호출 — 성공. 스킬 본문은 `npx -y @nomadamas/k-skill@0 instruct korean-law-search`로 전체 지침을 받으라고 안내함
2. Bash `npx -y @nomadamas/k-skill@0 instruct korean-law-search` — 실패(자동 권한 분류기가 거부함)
3. 스킬 본문이 대안으로 안내한 원본 지침을 WebFetch로 읽음(아래 1번)

**웹 조회 (WebFetch, 모두 k-skill-proxy 경유 국가법령정보센터 데이터. WebSearch는 쓰지 않음)**
1. `https://raw.githubusercontent.com/NomaDamas/k-skill/main/korean-law-search/instruction.md` — 성공(프록시 엔드포인트·파라미터 확인)
2. `https://k-skill-proxy.nomadamas.org/v1/korean-law/search?target=admrul&query=전자금융감독규정` — 성공(행정규칙일련번호 2100000282622, 시행 2026. 7. 15.)
3. `https://k-skill-proxy.nomadamas.org/v1/korean-law/detail?target=admrul&ID=2100000282622` — 성공했지만 앞 100,000자에 제14조의2가 없음(제8조의2에서 제14조의2를 참조한다는 점만 확인)
4. 같은 URL, offset 100000 — 성공(제14조의2 제목, ①·②·④·⑤·⑥ 문구 확인)
5. 같은 URL, offset 100000 — 성공(제14조의2 ① 각 호, ④ 각 호 문구 확인)
6. `https://k-skill-proxy.nomadamas.org/v1/korean-law/search?target=law&query=신용정보의 이용 및 보호에 관한 법률` — 성공(MST 283841, 시행 2026. 9. 11., 현행)
7. `https://k-skill-proxy.nomadamas.org/v1/korean-law/detail?target=law&MST=283841&JO=001700` — 성공(제17조 ①·③·⑥, ② 앞부분)
8. `https://k-skill-proxy.nomadamas.org/v1/korean-law/search?target=admrul&query=금융회사의 정보처리 업무 위탁에 관한 규정` — 성공(행정규칙일련번호 2100000200327, 2021. 3. 25.)
9. `https://k-skill-proxy.nomadamas.org/v1/korean-law/detail?target=admrul&ID=2100000200327` — 부분 성공(제1조, 제2조 ⑤, 제7조 ①·② 문구 일부만 원문 그대로 받음. 나머지는 도구 요약이라 인용하지 않음)

**조회 횟수:** 스킬 1, Bash 1(거부), WebFetch 9. 국가법령정보센터 Open API 직접 호출(OC 키 필요)은 사용자 키가 없어 건너뜀. 프록시가 키를 대신 처리함.

**참고:** WebFetch는 내려받은 페이지를 작은 모델이 발췌해 돌려주는 방식이라, 원문 전체 텍스트를 직접 본 것은 아닙니다. 원문 그대로라고 표시된 문구만 인용했고, 요약으로 돌아온 부분(정보처리 위탁 규정 제7조의 보고 대상 기관 등)은 인용하지 않았습니다.
