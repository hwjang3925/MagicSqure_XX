# GREEN Minimal — RED 1묶음 최소 구현 (Respond)

MagicSquare_1004 **ARRR 실습** — Respond **GREEN** 전용 Cursor Command.
**RED 1묶음당** 최소 구현만 수행한다. **1커밋 = 1 RED 묶음** (커밋은 사용자 요청 시만).

`/green-minimal`만으로 동작한다 — **추가 입력·질문 금지**. 대상 Test ID는 채팅·`tests/`의 **`pytest.fail("RED: …")`** · **`docs/PRD.md`** · **`.cursorrules`** 에서 자동 추출한다 (첫 FAIL Test ID 1건).

직전 **`/red-skeleton`** · **`/tdd-red`** 로 확정된 **Test ID 1건**(또는 명시된 RED 묶음)만 GREEN한다.

> **Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** — 상수·레이어·assert 관례는 Skill을 SSOT로 우선 적용한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (소문자 `green`):

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| **Phase** | `green` | 최소 구현 + assert PASS — REFACTOR 아님 |
| **Layer** | `entity` \| `boundary` | Track B 기본: **`entity`** |
| **Track** | `Logic` \| `UI` | Track B 기본: **`Logic`** |

> **Track A(boundary):** `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 동일 절차·금지·보고 형식을 재사용한다.

---

## GREEN 목표

이번 RED 묶음의 **Test ID 1건**을 pytest **PASS**로 만든다.

완료 조건:

1. RED 계약(C2C Then · Track B · assert)을 **재확인**했다.
2. **구현 대상 모듈**에 **최소 코드**만 추가했다 (이번 Test ID 통과에 필요한 만큼).
3. `pytest.fail`을 **제거**하고 **엄격 assert**로 교체했다 (`/tdd-red` 미완이면 본 Command에서 수행).
4. 대상 Test ID **PASS** + **기존 PASS 테스트 회귀 없음**.
5. **REFACTOR·다른 Test ID 동시 해결** 없음.

---

## 절차 (순서 고정)

| # | 단계 | 담당 경로 | 내용 |
|---|------|-----------|------|
| 1 | **RED 재확인** | 채팅 · 플랜 | Test ID · Given/When/Then · Invariant · 대상 함수·파일 |
| 2 | **최소 구현** | `entity/` 또는 `src/` | stub(`...`) → 이번 Then을 만족하는 **최소** 로직만 |
| 3 | **assert 교체** | `tests/` | `pytest.fail("RED: …")` 제거 → C2C Then과 **1:1 assert** |
| 4 | **PASS 확인** | — | pytest 실행 — 대상 Test ID PASS, 회귀 FAIL 시 **즉시 수정** |

### 레이어별 구현 경로

| Layer | 구현 위치 | 예 |
|-------|-----------|-----|
| **entity** | `entity/*.py` | `find_blank_coords` → `entity/blank_coords.py` |
| **boundary** | boundary 모듈 (Skill·플랜) | UI·입력 어댑터 |
| **Command** (세션 3) | `src/*.py` | `validate_lines` → `src/validate_lines.py` |

- **GREEN에서 `tests/` 수정**은 `pytest.fail` → assert 교체·RED 묶음 테스트 보완에 **한정**.
- **구현 본문**은 해당 레이어 모듈만 (`entity/` 또는 `src/` — **둘 다 최소 diff**).

---

## 상수 · ECB

### `entity/constants.py` SSOT

| 금지 | 대신 |
|------|------|
| 매직 넘버 `34` / `16` / `4` 직접 산포 | `from entity.constants import MAGIC_SUM, CELL_MAX, GRID_SIZE` |
| 하드코딩된 기대 좌표·합 | 테스트 Arrange·assert에서 fixture·상수 참조 |

`src/validate_lines.py`의 `MAGIC_SUM`은 **`.cursorrules`** 에 따라 `src/` 단일 정의 또는 `entity.constants`와 **한 방향 re-export만** (Skill·기존 Harness 따름). 중복 SSOT 금지.

### ECB · E001~E005

| 점검 | entity Layer (Logic) |
|------|----------------------|
| **E001~E005** | `MagicSquare` · `Cell` · `SolveResult` · `Solver`/`MissingFinder` · `GridUI`/`InputHandler`/`ResultDisplay` — **raise·return·import 금지** |
| **의존 방향** | **entity는 boundary/control import 금지** — 순수 격자·도메인 함수만 |
| **범위** | 1~16 중복·범위, Solver, UI — 이번 GREEN에 넣지 않음 |

---

## assert 교체 예시

**Before** (`/red-skeleton`):

```python
    # Then
    pytest.fail("RED: D-LOC-01 — find_blank_coords returns [(2,3),(4,4)] 1-index row-major")
```

**After** (`/green-minimal`):

```python
    # Then
    assert result == [(2, 3), (4, 4)]
```

- Then은 C2C·Track B **Then 계약**과 동일해야 한다.
- `in` / `>=` / `is not None`만으로 우회 **금지**.

---

## pytest 명령

### 단일 Test ID (권장 — GREEN 검증)

```bash
pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

```bash
pytest tests/test_validate_lines.py::test_fail_reports_wrong_line_with_id_sum_and_expected -v
```

### 파일 전체 (회귀 확인)

```bash
pytest tests/entity/test_d_loc_01.py -v
```

```bash
pytest tests/test_validate_lines.py -v
```

GREEN 완료 = **대상 Test ID PASS** + **같은 파일 내 기존 PASS 유지**.  
다른 FAIL Test ID가 있어도 **이번 묶음 외는 GREEN 범위 밖** — assert 완화로 맞추지 않는다.

---

## 입력 (SSOT)

| 순서 | 소스 | 사용 |
|------|------|------|
| 1 | 현재 채팅 | Test ID · RED 묶음 · Layer · 실패 중인 테스트 경로 |
| 2 | `/red-test-plan` 출력 | C2C Then · Invariant |
| 3 | `tests/` 해당 파일 | `pytest.fail` 메시지 · Given/When |
| 4 | `.cursorrules` | API·줄 ID·`MAGIC_SUM`·3상태 계약 |
| 5 | `magic-square-tdd` Skill | 있으면 자동 따름 |

---

## git · 커밋

- **사용자 명시 요청 전 `git commit` · `push` 금지.**
- 커밋 시: **1 RED 묶음 = 1 커밋** — 메시지에 Test ID 포함 (예: `green: D-LOC-01 find_blank_coords 1-index row-major`).

---

## 보고 형식

```
Phase: green | Layer: entity | Track: Logic

## PASS
| Test ID | 결과 |
|---------|------|
| D-LOC-01 | PASS |

## 변경 파일
- entity/blank_coords.py: find_blank_coords 최소 구현
- tests/entity/test_d_loc_01.py: pytest.fail → assert 교체

## pytest
- pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v → 1 passed
- pytest tests/entity/test_d_loc_01.py -v → N passed (회귀 없음)

## 회귀
- (FAIL 있으면 즉시 수정 내역 1줄; 없으면 "없음")

## 다음
- 다음 RED 묶음: /red-test-plan → /red-skeleton → /tdd-red
- GREEN PASS 후: /golden-master
- REFACTOR: /refactor-smell → /refactor-safe
```

**회귀 FAIL** 발견 시 보고 전에 **즉시 수정**하고 pytest 재실행한다.

---

## 금지 (GREEN 위반)

| 금지 | 이유 |
|------|------|
| **이번 RED 묶음 외 Test ID 동시 해결** | 1묶음 = 1 GREEN |
| **REFACTOR** (리네임·추출·구조 변경) | GREEN ≠ REFACTOR |
| **assert 완화·삭제·모호한 matcher** | 요구사항 우회 |
| **하드코딩·매직 넘버** | `entity/constants.py` SSOT |
| **E001~E005 raise/return/import** | ECB 범위 |
| **entity → boundary/control import** | 레이어 침범 |
| **`skip` / `xfail` / `pytest.skip()`** | TDD 금지 |
| **git commit·push (사용자 미요청)** | 프로젝트 규칙 |
| **플랜·테스트 없이 구현 선행** | RED 재확인 생략 |

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ③ | `/red-test-plan` | C2C · 테스트 플랜 |
| ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 |
| ⑤ | `/tdd-red` | assert 본문 RED (FAIL 확인) |
| **R** | **`/green-minimal`** | 최소 구현 + **PASS** |

---

## 참조

- 설계: `.cursor/commands/red-test-plan.md`
- 스켈레톤: `.cursor/commands/red-skeleton.md`
- golden: `.cursor/commands/golden-master.md`
- refactor: `.cursor/commands/refactor-smell.md`, `refactor-safe.md`
- assert RED: `.cursor/commands/tdd-red.md`
- Export: `.cursor/commands/export-session.md`
- Skill: `magic-square-tdd`
- 규칙: `.cursorrules`
- PRD: `docs/PRD.md`
