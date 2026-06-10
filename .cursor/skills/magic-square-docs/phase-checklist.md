# Phase Checklist — magic-square-docs (MagicSquare_1004)

Export 전 **순서대로** 체크. `/export-session`만으로 동작 — **추가 입력·질문 금지**.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/export-session.md`

---

## A. 입력 수집

- [ ] **git status** — branch, staged/unstaged, untracked 요약
- [ ] **pytest** — 세션 범위 명령·stdout (실행했을 때만)
- [ ] **Phase** — `red` \| `green` \| `refactor` \| `repeat` (채팅 선언과 일치)
- [ ] **Layer / Track** — entity·boundary, Logic·UI (해당 시)
- [ ] **Test ID** — 이번 묶음 (없으면 `—`)
- [ ] **Command** — `/red-test-plan` … `/export-session` 중 사용분
- [ ] 채팅·터미널에 **없는 pytest 결과** 미기재

## B. 번호 (NN)

- [ ] `Report/` `^\d{2}\.` glob → 최대 NN
- [ ] `Prompting/` `^\d{2}\.` glob → 최대 NN
- [ ] **NN = max(Report, Prompting) + 1**
- [ ] **Slug** — 2~4단어 PascalCase (예: `ARRR_Validate_Lines`)

## C. Report

- [ ] [report-template.md](report-template.md) → `Report/NN.{Slug}_Report.md`
- [ ] Phase STEP — **해당 블록만** (RED / GREEN / REFACTOR / repeat)
- [ ] 산출물 표 — 이번 세션 생성·수정 파일만
- [ ] Transcript 상대 링크 정확
- [ ] pytest = **A단계 실행 결과**만

## D. Transcript

- [ ] [transcript-template.md](transcript-template.md) → `Prompting/NN.{Slug}_Transcript.md`
- [ ] `_Exported on` · `_Source` (uuid)
- [ ] User / Assistant 교대; 도구 `[tool]` 한 줄
- [ ] Report 상대 링크 정확

## E. README (있으면)

- [ ] 「세션 문서」표 1행 추가 (NN, Slug, Report, 요약)

## F. 완료 보고 (채팅)

- [ ] `Report/NN.{Slug}_Report.md`
- [ ] `Prompting/NN.{Slug}_Transcript.md`
- [ ] NN · Slug · Phase · Test ID (해당 시)

---

## Phase별 Report STEP · pytest

| Phase | STEP | pytest 기대 |
|-------|------|-------------|
| **red** | RED | 대상 FAIL/ERROR (의도) |
| **green** | GREEN | 대상 PASS |
| **refactor** | REFACTOR | 전부 PASS |
| **repeat** | repeat | ARRR 1사이클 + 최종 PASS |

---

## ARRR Command 체인 (참고)

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master → /refactor-smell → /refactor-safe → /export-session
```

---

## 금지

| 금지 | 이유 |
|------|------|
| git commit·push 임의 | 사용자 요청 전 |
| UPDATE_GOLDEN=1 임의 | `/golden-master`만 |
| 없는 pytest 결과 | 허위 PASS/FAIL |
| Report만 저장 | Transcript 쌍 필수 |
| `Prompt/`에 Transcript | `Prompting/` 전용 |
| 추가 입력·질문 | SSOT 자동 추출 |
