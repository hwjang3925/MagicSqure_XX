---
name: magic-square-docs
description: >-
  Export Session Report and Transcript for MagicSquare_1004 ARRR practice using
  NN.Slug naming. Use for Report Export, Transcript, /export-session, Phase
  repeat, ARRR 1-cycle completion, or session documentation. SSOT: .cursorrules,
  docs/PRD.md, export-session.md. Loads phase-checklist and writes
  Report/NN.Slug_Report.md plus Prompting/NN.Slug_Transcript.md.
disable-model-invocation: true
---

# magic-square-docs — Report · Transcript Export

MagicSquare_1004 **ARRR 실습** 세션 **문서 SSOT**.
`/export-session` 또는 Report·Transcript export 요청 시 본 Skill을 따른다.

`/export-session`만으로 동작한다 — **추가 입력·질문 금지**. 슬러그·Phase·Test ID는 **현재 채팅** · **`.cursorrules`** · **`docs/PRD.md`** · **터미널/pytest/git 결과**에서 자동 추출한다.

> **Command:** [export-session.md](../../commands/export-session.md) — 진입점 · `01.XXX` 파일명 규칙

---

## SSOT (읽기 순서)

| 순서 | 소스 | 용도 |
|------|------|------|
| 1 | `.cursorrules` | TDD·API·Phase·금지 |
| 2 | `docs/PRD.md` | FR·Test ID (없으면 `Report/Session3_Workbook.md`) |
| 3 | `.cursor/commands/export-session.md` | Export 절차·템플릿 |
| 4 | 본 Skill + templates | NN.Slug · Step A~F |

템플릿: [report-template.md](report-template.md) · [transcript-template.md](transcript-template.md) · [phase-checklist.md](phase-checklist.md)

---

## 트리거

- `/export-session` · Report Export · Transcript
- `Phase: repeat` — ARRR 1사이클 완료
- Command 체인 종료: `refactor-safe` · `golden-master` · GREEN 후 세션 마감

---

## 파일명 SSOT (`01.XXX` → `NN.`)

| 산출 | 경로 | 예시 |
|------|------|------|
| **Report** | `Report/NN.{Slug}_Report.md` | `Report/03.ARRR_Validate_Lines_Report.md` |
| **Transcript** | `Prompting/NN.{Slug}_Transcript.md` | `Prompting/03.ARRR_Validate_Lines_Transcript.md` |

- **NN**: `Report/`·`Prompting/` 양쪽 `^\d{2}\.` **최대값 + 1**
- **Slug**: PascalCase · 공백·특수문자 없음
- Report·Transcript **동일 NN·Slug** 쌍
- Transcript → **`Prompting/` 전용** (`Prompt/` 금지)

---

## 워크플로 (Step A → F)

[phase-checklist.md](phase-checklist.md) 순서대로 수행.

### Step A — 입력 수집 (추가 질문 없음)

| 입력 | 수집 |
|------|------|
| **git status** | branch · changed files |
| **pytest** | 세션 관련 명령 stdout (채팅·실행 결과만) |
| **Phase** | `red` \| `green` \| `refactor` \| `repeat` |
| **Layer / Track** | entity/boundary · Logic/UI |
| **Test ID** | RED/GREEN 묶음 (없으면 `—`) |
| **Command** | 사용한 `/red-test-plan` … `/export-session` |

**채팅·터미널에 없는 pytest 결과는 Report·Transcript에 쓰지 않는다.**

### Step B — NN · Slug

1. `Report/NN.*` · `Prompting/NN.*` glob → max NN
2. **NN = max + 1**
3. Slug = 세션 주제 2~4단어 PascalCase (예: `ARRR_Validate_Lines`)

### Step C — Report

[report-template.md](report-template.md) → `Report/NN.{Slug}_Report.md`  
Phase에 맞는 **STEP 블록만** 유지 (RED / GREEN / REFACTOR / repeat).

### Step D — Transcript

[transcript-template.md](transcript-template.md) → `Prompting/NN.{Slug}_Transcript.md`  
`_Exported on` · `_Source` (agent-transcript uuid) · User/Assistant 교대.

### Step E — README (있으면)

「세션 문서」표에 NN · Slug · Report 링크 · 한 줄 요약 **1행 추가**.

### Step F — 완료 보고

```
## Export 완료
- Report: Report/NN.{Slug}_Report.md
- Transcript: Prompting/NN.{Slug}_Transcript.md
- NN: {NN} | Slug: {Slug} | Phase: {phase}
```

---

## Phase · ARRR · Command 매핑

| Phase | Report STEP | Command |
|-------|-------------|---------|
| `red` | RED | `/red-test-plan`, `/red-skeleton`, `/tdd-red` |
| `green` | GREEN | `/green-minimal`, `/golden-master` |
| `refactor` | REFACTOR | `/refactor-smell`, `/refactor-safe` |
| `repeat` | repeat | ARRR 1사이클 + `/export-session` |

**Command 체인:**

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master → /refactor-smell → /refactor-safe → /export-session
```

---

## 금지

| 금지 | 대신 |
|------|------|
| **git commit·push 임의** | 사용자 명시 요청 |
| **UPDATE_GOLDEN=1 임의** | `/golden-master`·사용자 지시 |
| **없는 pytest 결과 기재** | Step A 실행 후만 |
| **Report만 저장** | Transcript 쌍 필수 |
| **임의 파일명** | `NN.{Slug}_Report` / `_Transcript` |
| **추가 입력·질문** | SSOT 자동 추출 |

---

## 참조

| 문서 | 용도 |
|------|------|
| `.cursor/commands/export-session.md` | `/export-session` |
| `.cursor/skills/magic-square-tdd/SKILL.md` | TDD · Phase · pytest |
| `.cursorrules` | API · TDD 금지 |
| `docs/PRD.md` | FR · Test ID |
| `Report/Session3_Workbook.md` | Mom Test · R-G-I-O |
