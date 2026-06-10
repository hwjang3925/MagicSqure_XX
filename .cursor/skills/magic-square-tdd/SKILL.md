---
name: magic-square-tdd
description: >-
  MagicSquare_1004 Dual-Track TDD (ARRR Ask/Respond/Refine ↔ RED/GREEN/REFACTOR).
  Applies when Phase is red, green, or refactor; when running Commands
  /red-test-plan, /red-skeleton, /green-minimal, /golden-master,
  /refactor-smell, or /refactor-safe; or when the user mentions TDD, RED,
  GREEN, REFACTOR, Dual-Track, C2C, or pytest.fail. SSOT: .cursorrules and
  docs/PRD.md.
disable-model-invocation: true
---

# Magic Square TDD — MagicSquare_1004

4×4 부분 마방진 **Rule · Command · Test Loop** ARRR 실습 Skill.
**명시 호출·Command 실행 시에만** 적용 (`disable-model-invocation: true`).

각 Command는 **`/슬래시명`만**으로 동작 — **추가 입력·질문 금지**.

## SSOT (읽기 순서)

| 순서 | 소스 | 용도 |
|------|------|------|
| 1 | `.cursorrules` | API·10선 ID·`MAGIC_SUM`·TDD 금지·경로 |
| 2 | `docs/PRD.md` | FR·Acceptance·Test ID (없으면 `.cursorrules` + `Report/Session3_Workbook.md`) |
| 3 | `.cursor/commands/*.md` | Command별 Phase·금지·보고 형식 |
| 4 | `.cursor/commands/export-session.md` | 세션 Export·Report 규칙 |
| 5 | 본 Skill | Dual-Track·ARRR·체인·관례 (1·2와 충돌 시 1·2 우선) |

---

## 1. ARRR ↔ TDD 매핑

| ARRR | 단계 | TDD | Command | 산출 |
|------|------|-----|---------|------|
| **A — Ask** | ③ | RED plan | `/red-test-plan` | C2C 4블록 (코드 없음) |
| **A — Ask** | ④ | RED skeleton | `/red-skeleton` | `tests/` + `pytest.fail` |
| **A — Ask** | ⑤ | RED assert | `/tdd-red` | 엄격 assert · **FAIL** |
| **R — Respond** | GREEN | GREEN | `/green-minimal` | `src/` 최소 구현 · **PASS** |
| **R — Respond** | GREEN+ | golden | `/golden-master` | Approval baseline · matched |
| **R — Refine** | ⑦ | REFACTOR smell | `/refactor-smell` | 스멜 표 (수정 금지) |
| **R — Refine** | ⑧ | REFACTOR safe | `/refactor-safe` | P0 1건 · pytest 유지 |
| **—** | export | — | `/export-session` | Report · Transcript |

**한 번에 한 Phase만.** RED → GREEN → REFACTOR 순서 준수.

---

## 2. Phase 선언 (응답 첫 줄 · 필수)

| Phase | 선언 형식 |
|-------|-----------|
| RED plan/skeleton | `Phase: red \| Layer: entity \| Track: Logic` |
| RED assert | `Phase: RED` |
| GREEN / golden | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |

Track A(UI): `Layer: boundary` · `Track: UI` — Mock·emit만 분기.

---

## 3. C2C Rule 1~3

| Rule | 조건 | Then |
|------|------|------|
| **Rule1** | 0 없음, 10선 = `MAGIC_SUM` | `ok=true`, `status="pass"`, `failed_lines=[]` |
| **Rule2** | 0 없음, 합≠`MAGIC_SUM` | `ok=false`, `status="fail"`, 틀린 줄 `{id,sum,expected}` **누락 없음** |
| **Rule3 (R5)** | `0` 포함 | `ok=false`, `status="incomplete"`, `failed_lines=[]`, **합 미계산** |

- 줄 ID: `R1`~`R4`, `C1`~`C4`, `D1`, `D2`
- `expected` = `MAGIC_SUM` (리터럴 `34` 금지)
- `incomplete` ≠ `fail`

---

## 4. RED 절대 금지

| 금지 | 이유 |
|------|------|
| **`tests/` 외 경로 수정** (`src/` 포함) | RED = tests only |
| **`skip` / `xfail` / `pytest.skip()`** | TDD 우회 |
| **assert 완화·모호한 matcher** | Then 우회 |
| **Logic Track Domain Mock** | Command 직접 검증 |
| **GREEN · REFACTOR 동시** | Phase 혼합 |
| **E001~E005 emit** | ECB 범위 |

---

## 5. GREEN

| 규칙 | 내용 |
|------|------|
| **1 RED 묶음 = 1 GREEN** | Test ID 1건만 |
| **1 커밋 = 1 RED 묶음** | 사용자 요청 시만 |
| **수정** | `src/` (또는 `entity/`) 최소 diff |
| **`tests/`** | `pytest.fail` → assert 교체만 |
| **REFACTOR 금지** | Refine Command |

### constants SSOT

| 경로 | 상수 |
|------|------|
| `src/validate_lines.py` | `MAGIC_SUM` (Command SSOT) |
| `entity/constants.py` | `MAGIC_SUM`, `GRID_SIZE`, `CELL_MAX` |
| 테스트 | import만 — 리터럴 `34`/`4`/`16` 금지 |

---

## 6. REFACTOR

### Change Budget (`/refactor-safe` 1회)

파일 ≤ 3 · 클래스 ≤ 1 · 메서드 ≤ 3

### golden 유지

- 전제·사후: `python -m pytest tests/ -v` **전부 PASS**
- `/refactor-smell`: 탐지만 — 수정·commit 금지
- `/refactor-safe`: P0 **1건** — C2C·golden 불변

---

## 7. Track A (UI) vs Track B (Logic)

| 항목 | Track B — Logic | Track A — UI |
|------|-----------------|--------------|
| Layer | `entity` / `src/` | `boundary` |
| Domain Mock | **금지** | Boundary만 |
| E001~E005 | import·emit **금지** | E005 boundary만 |
| 의존 | entity → boundary **금지** | boundary → entity OK |
| 세션 3 기본 | `validate_lines` | 후속 세션 |

---

## 8. Command 체인

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master → /refactor-smell → /refactor-safe → /export-session
```

| Command | 수정 | 산출 |
|---------|------|------|
| `/red-test-plan` | 없음 | C2C · 플랜 |
| `/red-skeleton` | `tests/` | `pytest.fail` |
| `/tdd-red` | `tests/` | assert · FAIL |
| `/green-minimal` | `src/` | PASS |
| `/golden-master` | `tests/` harness | matched |
| `/refactor-smell` | 없음 | 스멜 표 |
| `/refactor-safe` | Budget 내 | P0 적용 |
| `/export-session` | Report | NN.Slug 쌍 |

---

## 9. pytest 명령

```bash
python -m pytest tests/ -v
```

```bash
python -m pytest tests/test_validate_lines.py::test_pass_all_ten_lines_sum_to_magic_constant -v
```

| 시점 | 기대 |
|------|------|
| RED skeleton | FAIL · `RED: {Test ID}` |
| RED assert | FAIL · assert 메시지 |
| GREEN | 대상 PASS |
| golden | matched PASS |
| REFACTOR | 전후 전부 PASS |

---

## 10. 완료 보고 형식

**첫 줄 = Phase 선언.** Command별 최소:

**plan:** 4블록 표 → `/red-skeleton 으로 넘길 준비됐다`

**skeleton/assert:** FAIL 표 · 변경 `tests/` · pytest · 다음 Command

**green:** PASS 표 · 변경 파일 · pytest · 회귀 · 다음

**golden:** matched · golden 경로 · UPDATE_GOLDEN / matched run

**smell:** pytest PASS · 스멜 표 · safe 후보 1~3 → `P0 후보 1개만 골라 /refactor-safe 실행`

**safe:** 적용 표 · pytest 전후 · golden · 회귀

---

## AAA · pytest.fail

```python
    pytest.fail("RED: T-fail-01 — ok=false, status=fail, failed_lines=[R1 id sum expected=MAGIC_SUM]")
```

GREEN Then:

```python
    assert result["ok"] is False
    assert result["status"] == "fail"
    assert result["failed_lines"] == [{"id": "R1", "sum": 33, "expected": MAGIC_SUM}]
```

---

## ECB · git

Logic: E001~E005 emit 금지. 사용자 요청 전 **commit·push 금지**.

---

## 참조

- `.cursorrules` · `docs/PRD.md`
- Commands: `red-test-plan`, `red-skeleton`, `tdd-red`, `green-minimal`, `golden-master`, `refactor-smell`, `refactor-safe`, `export-session`
- Docs Skill: `magic-square-docs`
