# TDD RED — assert 본문 RED (Ask ⑤)

MagicSquare_1004 **ARRR 실습** — Ask **⑤** 전용 Cursor Command.
직전 **`/red-skeleton`** 스켈레톤(`pytest.fail`)을 **assert 본문 RED**로 교체한다.

`/tdd-red`만으로 동작한다 — **추가 입력·질문 금지**. 채팅에 스켈레톤이 없으면 **`tests/`** · **`.cursorrules`** · **`docs/PRD.md`** · **`Report/Session3_Workbook.md`** 에서 RED 묶음을 자동 추출한다.

GREEN·REFACTOR는 **`/green-minimal`** · **`/refactor-safe`** 담당.

> **Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** — fixture·상수·네이밍·AAA·assert 관례는 Skill을 SSOT로 우선 적용한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (소문자 `red`):

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| **Phase** | `red` | assert RED — `src/` 수정 금지 |
| **Layer** | `entity` \| `boundary` | Track B 기본: **`entity`** |
| **Track** | `Logic` \| `UI` | Track B 기본: **`Logic`** |

> **Track A(boundary):** `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 동일 절차·금지·보고 형식을 재사용한다.

---

## RED 목표

`/red-skeleton`의 **`pytest.fail` 한 줄**을 **C2C·Track B Then 계약에 맞는 assert 본문**으로 교체한다.

완료 조건:

1. **`tests/`만** 수정 (`src/` **수정 금지**).
2. 각 테스트: AAA 주석 유지, **Then = assert 본문** (`pytest.fail` 제거).
3. `skip` / `xfail` / `pytest.skip()` **없음**.
4. `pytest` 실행 후 **의도대로 FAIL** (stub/미구현으로 ImportError·AttributeError 또는 assert FAIL).
5. 보고: Test ID · FAIL/ERROR 한 줄 · 변경 파일(`tests/`만).

---

## 입력 (SSOT)

| 순서 | 소스 | 사용 |
|------|------|------|
| 1 | 현재 채팅 | `/red-skeleton` 출력 — Test ID · 함수명 · Then 계약 |
| 2 | `.cursor/commands/red-skeleton.md` | AAA·pytest.fail 형식 |
| 3 | `.cursor/commands/red-test-plan.md` | C2C·Track B·Then 계약 |
| 4 | `.cursorrules` | API·줄 ID·`MAGIC_SUM`·TDD 금지 |
| 5 | `magic-square-tdd` Skill | assert·fixture·상수 관례 **우선** |

---

## assert 규칙

| 단계 | 주석 | 내용 |
|------|------|------|
| **Arrange** | `# Given` | 스켈레톤 Given 유지 |
| **Act** | `# When` | `validate_lines(grid)` 등 호출 |
| **Assert** | `# Then` | **C2C·Track B Then에 맞는 `assert` 본문** |

### Then assert 예시 (D-LOC-01)

```python
# Then
assert result["ok"] is False
assert result["status"] == "fail"
assert len(result["failed_lines"]) >= 1
line = result["failed_lines"][0]
assert line["id"] == "R1"
assert line["sum"] != MAGIC_SUM
assert line["expected"] == MAGIC_SUM
```

- `MAGIC_SUM`은 `entity.constants` import (리터럴 `34` 금지).
- 줄 ID: `R1`~`R4`, `C1`~`C4`, `D1`, `D2` (`.cursorrules` 표준).
- assert 완화·모호한 matcher (`in`만, `>=`만) **금지**.

### 금지 (Then·Assert)

| 금지 | 이유 |
|------|------|
| **`pytest.fail` 잔존** | RED 완성 = assert 본문 |
| **`skip` / `xfail` / `pytest.skip()`** | TDD 금지 |
| **통과 더미** (`pass`, `assert True`) | RED 아님 |
| **Mock으로 Domain 대체** | Logic Track |
| **`src/` 수정** | GREEN 담당 |

---

## 상수 · fixture

```python
from entity.constants import GRID_SIZE, MAGIC_SUM, CELL_MAX
```

- **`entity/constants.py` 수정 금지** (Harness·Skill SSOT).
- `grid_g1` 등 conftest fixture는 스켈레톤·Skill 정의 유지.

---

## 파일 범위

| 경로 | RED에서 |
|------|---------|
| `tests/test_*.py` | **수정** — `pytest.fail` → assert |
| `tests/conftest.py` | 플랜·Skill 명시 fixture만 |
| `src/` | **수정 금지** |

---

## 실행 절차 (에이전트)

1. 채팅·`tests/`에서 RED 묶음·Test ID·스켈레톤 함수 추출.
2. `magic-square-tdd` Skill 있으면 읽고 관례 적용.
3. `tests/test_*.py` — 각 스켈레톤의 Then을 assert 본문으로 교체.
4. **`pytest`** 실행.
5. **보고 형식** 출력.

---

## 보고 형식

```
Phase: red | Layer: entity | Track: Logic

## 변경 (tests/만)
- tests/test_validate_lines.py: test_d_loc_01_… — D-LOC-01 assert RED

## pytest 결과
| Test ID | 결과 |
|---------|------|
| D-LOC-01 | FAIL — assert status / ImportError … |

## 다음
- `/green-minimal`: src/validate_lines.py 최소 구현
```

---

## 금지 (RED 위반)

| 금지 | 이유 |
|------|------|
| **`src/` 수정** | GREEN 담당 |
| **GREEN · REFACTOR** | 한 Phase만 |
| **`skip` / `xfail`** | TDD 금지 |
| **assert 완화** | C2C Then 준수 |
| **매직 넘버 `34`/`16`/`4` 직접 산포** | `entity.constants` |

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 |
| **⑤** | **`/tdd-red`** | assert 본문 RED |
| ⑥ | `/green-minimal` | src/ 최소 구현 |

---

## 참조

- skeleton: `.cursor/commands/red-skeleton.md`
- 플랜: `.cursor/commands/red-test-plan.md`
- GREEN: `.cursor/commands/green-minimal.md`
- Skill: `magic-square-tdd`
- PRD: `docs/PRD.md`
- 규칙: `.cursorrules`
