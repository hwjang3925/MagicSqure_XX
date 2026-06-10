# Transcript Template — magic-square-docs (MagicSquare_1004)

`Prompting/NN.{Slug}_Transcript.md` 본문 SSOT.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/export-session.md`

---

```markdown
# Transcript — {제목}

| 항목 | 내용 |
|------|------|
| _Exported on | {YYYY-MM-DD HH:MM} |
| _Source | {agent-transcript uuid} |
| 프로젝트 | MagicSquare_1004 |
| 세션 | {세션 N — 주제} |
| Phase | {red \| green \| refactor \| repeat} |
| Test ID | {ID 또는 —} |
| Command | {/red-test-plan, …} |
| Report | [Report/{NN}.{Slug}_Report.md](../Report/{NN}.{Slug}_Report.md) |

---

## 대화

### User

{요청 — `/command` 단독 호출·제약 포함}

### Assistant

{Phase 선언 · 산출 · pytest/git 요약}

{`[tool] Read .cursorrules` / `[tool] pytest … → N passed`}

---

### User

{다음 턴}

### Assistant

{다음 턴}

...
```

---

## 작성 규칙

| 규칙 | 내용 |
|------|------|
| **User / Assistant** | `### User` · `### Assistant` 교대 |
| **_Exported on** | export 시각 |
| **_Source** | `agent-transcripts/{uuid}.jsonl`; 없으면 `current` |
| **도구** | `[tool] {한 줄}` — 전체 로그 금지 |
| **pytest** | **실행·확인한 결과만** |
| **Command** | `/슬래시명` 단독 호출 기록 |
| **비밀** | 토큰·credential 마스킹 |

## 파일명 SSOT

| 항목 | 패턴 |
|------|------|
| Transcript | `Prompting/NN.{Slug}_Transcript.md` |
| 쌍 | Report와 **동일 NN·Slug** |

저장: **`Prompting/` 전용**.
