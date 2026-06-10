# Golden Master — Approval Test 구축·검증 (GREEN 후)

MagicSquare_1004 **ARRR 실습** — GREEN 직후 전용 Cursor Command.
**대상 Test ID가 pytest PASS인 상태**에서 Golden Master(Approval Test)를 구축·검증한다.

`/golden-master`만으로 동작한다 — **추가 입력·질문 금지**. 대상 Test ID는 채팅·`tests/`의 **최근 PASS assert 테스트** · **`docs/PRD.md`** · **`.cursorrules`** 에서 자동 추출한다.

직전 **`/green-minimal`** 로 PASS된 **Test ID 1건**(또는 명시된 GREEN 묶음)만 Golden 한다.

> **Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** — 직렬화·golden 경로·assert 관례는 Skill을 SSOT로 우선 적용한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (소문자 `green`):

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| **Phase** | `green` | Approval harness·golden 연결 — REFACTOR 아님 |
| **Layer** | `entity` \| `boundary` | Track B 기본: **`entity`** |
| **Track** | `Logic` \| `UI` | Track B 기본: **`Logic`** |

> **Track A(boundary):** `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 동일 절차·금지·보고 형식을 재사용한다.

---

## Golden 목표

이번 GREEN 묶음의 **Test ID 1건**에 대해 Approval Test를 **구축**하고 **matched**를 확인한다.

완료 조건:

1. **전제:** 대상 Test ID **pytest PASS** (GREEN 완료 상태).
2. `tests/_approval.py`에 `assert_matches_golden`이 있고, 없으면 **생성**했다.
3. `tests/golden/{id}.approved.txt`가 대상 Test ID와 **연결**되었다.
4. `UPDATE_GOLDEN=1`로 기준 파일을 **생성**했다 (최초 1회 또는 의도적 갱신 시만).
5. **`UPDATE_GOLDEN` 없이** pytest 실행 → **matched** 확인.
6. golden **수동 편집으로 통과 우회**하지 않았다.

---

## 전제 (필수)

| 조건 | 확인 |
|------|------|
| **대상 Test ID pytest PASS** | `/green-minimal` 완료 — `pytest.fail` 제거·엄격 assert 통과 |
| **구현 안정** | golden 생성 전 대상 테스트가 **의도한 Then**을 만족 |
| **범위** | 이번 Test ID 1묶음만 — 다른 ID golden 동시 갱신 금지 |

PASS가 아니면 **본 Command 중단** → `/green-minimal` 먼저.

---

## 절차 (순서 고정)

| # | 단계 | 담당 경로 | 내용 |
|---|------|-----------|------|
| 1 | **PASS 재확인** | — | 대상 Test ID pytest **PASS** |
| 2 | **Harness** | `tests/_approval.py` | `assert_matches_golden` — 없으면 **생성** |
| 3 | **Golden 연결** | `tests/` 해당 테스트 | `assert_matches_golden(test_id, actual_text)` 호출 추가 |
| 4 | **기준 생성** | `tests/golden/` | `UPDATE_GOLDEN=1 pytest …` → `{id}.approved.txt` 작성 |
| 5 | **matched 확인** | — | `UPDATE_GOLDEN` **없이** 동일 pytest → **PASS (matched)** |
| 6 | **보고** | 채팅 | golden 경로 · matched 여부 · diff 요약 |

### 1. `tests/_approval.py` — `assert_matches_golden`

없으면 생성. 최소 API:

```python
import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(test_id: str, actual: str) -> None:
    """Compare actual canonical text to tests/golden/{id}.approved.txt."""
    golden_path = GOLDEN_DIR / f"{_golden_filename(test_id)}.approved.txt"
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8", newline="\n")
        return
    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"Golden mismatch: {golden_path}\n"
            f"--- expected ---\n{expected}\n"
            f"--- actual ---\n{actual}"
        )


def _golden_filename(test_id: str) -> str:
    """D-LOC-01 -> d-loc-01"""
    return test_id.lower().replace("_", "-")
```

- `UPDATE_GOLDEN=1`일 때만 golden 파일 **쓰기**.
- 그 외에는 **바이트 단위 동일** 비교 — trim·정규화 우회 금지.

### 2. `tests/golden/{id}.approved.txt`

| 항목 | 규칙 |
|------|------|
| **경로** | `tests/golden/{test_id_lower}.approved.txt` |
| **파일명** | Test ID 소문자·하이픈 — `D-LOC-01` → `d-loc-01.approved.txt` |
| **내용** | 테스트에서 `format_golden(...)` 으로 만든 **canonical 문자열 1벌** |
| **생성** | `UPDATE_GOLDEN=1` pytest로만 — 수동 생성·수정 **금지** (우회) |

### 3. 테스트 연결 예시

```python
from tests._approval import assert_matches_golden
from tests._golden_format import format_entity_golden  # 직렬화 헬퍼 (없으면 동 파일·_approval 인근)


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given
    grid = grid_g1

    # When
    result = find_blank_coords(grid)

    # Then
    assert result == [(2, 3), (4, 4)]
    actual = format_entity_golden(test_id="D-LOC-01", coords=result)
    assert_matches_golden("D-LOC-01", actual)
```

- **기존 assert 유지** — golden은 **추가 회귀 락**이지 assert 대체가 아님.

### 4. `UPDATE_GOLDEN=1` — 기준 파일 생성

**PowerShell (Windows):**

```powershell
$env:UPDATE_GOLDEN=1; pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v; Remove-Item Env:UPDATE_GOLDEN
```

**bash:**

```bash
UPDATE_GOLDEN=1 pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

- **대상 Test ID 1건만** 실행 — 전체 suite golden 일괄 갱신 금지.
- 생성 후 `tests/golden/{id}.approved.txt` 존재·내용 확인.

### 5. matched 확인 (`UPDATE_GOLDEN` 없음)

```bash
pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

- **PASS** = matched.
- **FAIL** = `AssertionError: Golden mismatch` — diff 요약을 보고에 포함; **golden 수동 수정으로 맞추지 않음** → 구현·직렬화 수정.

---

## Canonical 직렬화 (고정 포맷)

Golden 내용은 **한 줄짜리 고정 필드**로 직렬화한다. 구현·테스트가 달라져도 **동일 입력 → 동일 문자열**이어야 한다.

### `int[6]` — 1-index 좌표·메타 (entity Logic)

**정확히 6개 정수**, 쉼표 구분, **공백 없음**. 좌표는 **1-index** (행·열 모두 1~4).

| 인덱스 | 필드 | 설명 |
|--------|------|------|
| 0–1 | `r1,c1` | row-major **첫 번째** 빈칸 (1-index) |
| 2–3 | `r2,c2` | row-major **두 번째** 빈칸 (1-index) |
| 4 | `n_blanks` | 빈칸 개수 (`0` 셀 수) |
| 5 | `reserved` | 예약 — 현재 **`0` 고정** |

**예 (D-LOC-01, blanks at (2,3) and (4,4)):**

```
INT6:2,3,4,4,2,0
```

- 빈칸 1개만인 시나리오: `(r1,c1)`만 채우고 `(r2,c2)`는 **`0,0`**, `n_blanks=1`.
- `int[6]` 필드 수·순서·1-index 규칙 변경 **금지** — golden 전 테스트 불일치.

### 에러 코드 문자열 (ECB · 고정)

Logic Track golden에 ECB 위반 코드를 기록할 때:

| 형식 | 규칙 |
|------|------|
| **패턴** | `E` + 3자리 숫자 — `E001` … `E005` |
| **대소문자** | **대문자 고정** (`e001` 금지) |
| **구분자** | 복수 코드 시 `;` — 예: `ECB:E001;E004` |
| **없음** | 해당 없으면 `ECB:` (빈) |

```
ECB:
```

- 본 세션 GREEN 범위에서 ECB emit이 없으면 **`ECB:`** 한 줄 유지.

### `validate_lines` Command golden (해당 Test ID일 때)

`int[6]` 다음 줄에 상태·줄 실패 요약 (줄 ID `.cursorrules` 표준):

```
STATUS:fail
LINES:R1:33:34
```

| 필드 | 형식 |
|------|------|
| `STATUS` | `pass` \| `fail` \| `incomplete` |
| `LINES` | 틀린 줄만, **ID 오름차순** (`R1`…`R4`,`C1`…`C4`,`D1`,`D2`) — `{id}:{sum}:{expected}` 콜론 구분, 줄마다 **쉼표 없이** `;` 로 연결 |
| `pass` / `incomplete` | `LINES:` (빈) |

**예 (fail, R1 only):**

```
INT6:0,0,0,0,0,0
ECB:
STATUS:fail
LINES:R1:33:34
```

- `expected`는 **`34` 리터럴 금지** — 직렬화 시 `MAGIC_SUM` 값 사용.

### 전체 golden 블록 순서 (고정)

```
INT6:{6 integers}
ECB:{codes}
STATUS:{status}
LINES:{line entries}
```

- 줄 끝 `\n`, 마지막 줄 뒤 **trailing newline 1개**.
- 필드 라벨(`INT6:`, `ECB:` 등) **변경 금지**.

---

## pytest 명령

### 단일 Test ID (권장)

```bash
pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

```bash
pytest tests/test_validate_lines.py::test_fail_reports_wrong_line_with_id_sum_and_expected -v
```

### Golden 갱신 (의도적 변경 시만)

```powershell
$env:UPDATE_GOLDEN=1; pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v; Remove-Item Env:UPDATE_GOLDEN
```

Golden 완료 = **UPDATE_GOLDEN 없이 PASS (matched)** + **기존 assert 유지 PASS**.

---

## 입력 (SSOT)

| 순서 | 소스 | 사용 |
|------|------|------|
| 1 | 현재 채팅 | Test ID · GREEN 완료 테스트 경로 |
| 2 | `/green-minimal` 보고 | PASS 확인 · Then 계약 |
| 3 | `tests/` 해당 파일 | assert 본문 · 직렬화 입력 |
| 4 | `.cursorrules` | 줄 ID · `MAGIC_SUM` · 3상태 |
| 5 | `magic-square-tdd` Skill | 있으면 golden 관례 **우선** |

---

## git · 커밋

- **사용자 명시 요청 전 `git commit` · `push` 금지.**
- 커밋 시: golden 파일 + harness + 테스트 연결을 **같은 Test ID 묶음**으로 — 예: `golden: D-LOC-01 approval baseline`.

---

## 보고 형식

```
Phase: green | Layer: entity | Track: Logic

## Golden
| 항목 | 값 |
|------|-----|
| Test ID | D-LOC-01 |
| golden 경로 | tests/golden/d-loc-01.approved.txt |
| matched | yes / no |
| diff 요약 | (no이면 expected vs actual 1~3줄; yes이면 "—") |

## 변경 파일
- tests/_approval.py: assert_matches_golden (생성 또는 기존)
- tests/golden/d-loc-01.approved.txt: UPDATE_GOLDEN=1로 생성
- tests/entity/test_d_loc_01.py: assert_matches_golden 연결

## pytest
- UPDATE_GOLDEN=1 → 1 passed (baseline written)
- matched run → 1 passed

## 다음
- 다음 RED 묶음: /red-test-plan → … → /green-minimal → /golden-master
- REFACTOR: 사용자 요청 또는 별도 Command
```

**matched = no** 시 golden 파일 **수동 편집 금지** — 직렬화·구현을 수정한 뒤 `UPDATE_GOLDEN=1`로 **재생성** (의도적 계약 변경 시만).

---

## 금지 (Golden 위반)

| 금지 | 이유 |
|------|------|
| **PASS 전 golden 구축** | 기준 파일이 잘못된 동작을 고정 |
| **`tests/golden/*.approved.txt` 수동 편집으로 matched 맞추기** | Approval Test 우회 |
| **`UPDATE_GOLDEN` 없이 golden 파일 직접 작성** | canonical 포맷 미준수 |
| **assert 삭제·완화 후 golden만 의존** | Then 계약 약화 |
| **int[6] / 에러 코드 / STATUS·LINES 포맷 임의 변경** | golden 전 테스트 불일치 |
| **0-index 좌표를 golden에 기록** | 1-index SSOT 위반 |
| **이번 묶음 외 Test ID golden 일괄 갱신** | 1묶음 = 1 Golden |
| **`skip` / `xfail` / `pytest.skip()`** | TDD 금지 |
| **git commit·push (사용자 미요청)** | 프로젝트 규칙 |
| **REFACTOR·다른 Test ID 동시 해결** | 범위 초과 |

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ③ | `/red-test-plan` | C2C · 테스트 플랜 |
| ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 |
| ⑤ | `/tdd-red` | assert 본문 RED |
| **R** | `/green-minimal` | 최소 구현 + **PASS** |
| **R+** | **`/golden-master`** | Approval baseline + **matched** |

---

## 참조

- GREEN: `.cursor/commands/green-minimal.md`
- assert RED: `.cursor/commands/tdd-red.md`
- refactor: `.cursor/commands/refactor-smell.md`, `refactor-safe.md`
- Export: `.cursor/commands/export-session.md`
- Skill: `magic-square-tdd`
- PRD: `docs/PRD.md`
- 규칙: `.cursorrules`
