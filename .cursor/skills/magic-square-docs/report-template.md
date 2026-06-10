# Report Template — magic-square-docs (MagicSquare_1004)

`Report/NN.{Slug}_Report.md` 본문 SSOT. `{placeholder}` 를 세션 **사실**로 치환.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/export-session.md`

---

```markdown
# {제목} — MagicSquare_1004

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_1004 |
| 세션 | {세션 N — 주제 한 줄} |
| Phase | {red \| green \| refactor \| repeat} |
| Layer | {entity \| boundary \| —} |
| Track | {Logic \| UI \| —} |
| Test ID | {Test ID 또는 —} |
| Command | {/red-test-plan, /green-minimal, …} |
| 일자 | {YYYY-MM-DD} |
| 상태 | **종료** |
| Transcript | [Prompting/{NN}.{Slug}_Transcript.md](../Prompting/{NN}.{Slug}_Transcript.md) |

---

## 요약

{세션 목표·결과 2~4문장. 채팅·pytest·git에서 확인한 사실만.}

## Phase STEP

<!-- Phase에 맞는 블록만 남기고 나머지 삭제 -->

### RED

| 항목 | 내용 |
|------|------|
| Test ID | {ID} |
| Command | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| 변경 | `tests/` only |
| pytest | {명령} → {FAIL/ERROR — 실행 결과} |
| Expected | 구현 부재·미완성 FAIL |

### GREEN

| 항목 | 내용 |
|------|------|
| Test ID | {ID} |
| Command | `/green-minimal` {→ `/golden-master`} |
| 변경 | {src/ 또는 entity/} |
| pytest | {명령} → {PASS — 실행 결과} |
| golden | {matched / —} |
| 회귀 | {없음 \| 1줄} |

### REFACTOR

| 항목 | 내용 |
|------|------|
| Command | `/refactor-smell` → `/refactor-safe` |
| 스멜 ID | {S-01 또는 —} |
| Budget | {파일·메서드 요약} |
| pytest | {명령} → {전부 PASS — 실행 결과} |
| 동작 변경 | 없음 |

### repeat (ARRR 1사이클 완료)

| 항목 | 내용 |
|------|------|
| 사이클 | plan → skeleton → tdd-red → green → golden → smell → safe |
| Test ID | {ID 목록} |
| pytest 최종 | {명령} → {결과 — 실행 결과} |

## 산출물

| 파일 | 설명 |
|------|------|
| `{path}` | {한 줄} |

## 결정·규칙

- {`.cursorrules` · PRD · Command에서 확정된 것}

## git 스냅샷 (참고)

| 항목 | 내용 |
|------|------|
| branch | {git branch --show-current} |
| status | {clean \| N files changed} |

> commit·push는 사용자 요청 시만.

## 다음 단계

- {bullet}
```

---

## 파일명 SSOT

| 항목 | 패턴 | 예시 |
|------|------|------|
| Report | `Report/NN.{Slug}_Report.md` | `Report/03.ARRR_Validate_Lines_Report.md` |
| Slug | PascalCase · 공백 없음 | `ARRR_Validate_Lines` |
| NN | 양쪽 폴더 max + 1 | `03` |

구형(`Session3_Workbook.md` 등) 유지; **신규 export부터** `NN.` 적용.
