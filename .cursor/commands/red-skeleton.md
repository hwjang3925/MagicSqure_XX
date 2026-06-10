# RED Skeleton — pytest.fail 스켈레톤 (Ask ④)

MagicSquare_1004 **ARRR 실습** — Ask **④** 전용 Cursor Command.
직전 **`/red-test-plan`** 설계표(C2C · Track B · 테스트 플랜)를 기준으로 **`pytest.fail` 스켈레톤만** `tests/`에 작성한다.

`/red-skeleton`만으로 동작한다 — **추가 입력·질문 금지**. 플랜이 채팅에 없으면 **`docs/PRD.md`** · **`.cursorrules`** · **`tests/`** · **`Report/Session3_Workbook.md`** 에서 RED 묶음을 자동 추출한다.

실제 **assert 본문**·GREEN·REFACTOR는 **`/tdd-red`** (또는 후속 RED Command) 담당.

> **Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** — fixture·상수·네이밍·AAA 관례는 Skill을 SSOT로 우선 적용한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (소문자 `red`):

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| **Phase** | `red` | 스켈레톤만 — assert·구현 없음 |
| **Layer** | `entity` \| `boundary` | Track B 기본: **`entity`** |
| **Track** | `Logic` \| `UI` | Track B 기본: **`Logic`** |

> **Track A(boundary):** `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 동일 절차·금지·보고 형식을 재사용한다.

---

## Skeleton 목표

`/red-test-plan`에서 확정한 **RED 묶음 Test ID**마다 테스트 함수 1개를 추가한다.

완료 조건:

1. **`tests/`만** 생성·수정했다 (`src/` **수정 금지**).
2. 각 테스트는 **AAA 주석** (`# Given` / `# When` / `# Then`)을 갖는다.
3. **Then**은 **`pytest.fail("RED: {Test ID} — …")` 한 줄만** — assert 본문·통과 더미·`return` 없음.
4. `skip` / `xfail` / `pytest.skip()` **없음**.
5. `pytest` 실행 후 **의도대로 FAIL** (메시지에 `RED: {Test ID}` 포함).
6. 보고: Test ID · FAIL 한 줄 · 변경 파일(`tests/`만).

---

## 입력 (SSOT)

추가 질문 없이 아래 순으로 읽는다.

| 순서 | 소스 | 사용 |
|------|------|------|
| 1 | 현재 채팅 | 직전 `/red-test-plan` 출력 — Test ID · 함수명 · Given/When/Then · RED 묶음 범위 |
| 2 | `.cursor/commands/red-test-plan.md` | 4블록 형식·금지·ECB 점검 |
| 3 | `.cursorrules` | API·줄 ID·`MAGIC_SUM` (Then 메시지 문구용) |
| 4 | `magic-square-tdd` Skill | 있으면 fixture·상수·함수명 관례 **우선** |

플랜에 Test ID·함수명이 없으면 **`test_{test_id_snake}`** (예: `D-LOC-01` → `test_d_loc_01_…`).

---

## AAA · pytest.fail 규칙

| 단계 | 주석 | 내용 |
|------|------|------|
| **Arrange** | `# Given` | 플랜의 Given — `grid_g1` fixture 또는 Arrange 상수·좌표 |
| **Act** | `# When` | 플랜의 When — `validate_lines(grid)` 등 **호출 한 줄** (stub이면 ERROR도 허용; Then은 여전히 `pytest.fail`) |
| **Assert** | `# Then` | **`pytest.fail("RED: {Test ID} — {Then 요약}")` 단 한 줄** |

### Then 메시지 형식

```python
pytest.fail("RED: D-LOC-01 — ok=false, status=fail, failed_lines=[R1 id sum expected=MAGIC_SUM]")
```

- `{Test ID}`는 플랜 Test ID와 **정확히 일치** (`D-LOC-01`, `U-IN-01` 등).
- Then 요약은 C2C·Track B 표의 **Then 계약**을 한 줄로 (assert 식 아님).

### 금지 (Then·Assert)

| 금지 | 이유 |
|------|------|
| **`assert …` 본문** | `/tdd-red`에서 교체 |
| **`pytest.fail` 외 통과 경로** | `pass`, 빈 함수, `return`만 |
| **`skip` / `xfail` / `pytest.skip()`** | 실패 숨김 |
| **Mock으로 Domain 대체** | Logic Track — `.cursorrules` |

---

## 상수 · fixture

### `entity/constants.py` (읽기 전용 SSOT)

격자·마법상수 **리터럴 금지** — 픽스처·Arrange 데이터에서만 import:

```python
from entity.constants import GRID_SIZE, MAGIC_SUM, CELL_MAX
```

| 상수 | 용도 |
|------|------|
| `GRID_SIZE` | `4` |
| `MAGIC_SUM` | `34` |
| `CELL_MAX` | `16` |

- **`entity/constants.py`는 본 Command에서 생성·수정하지 않는다** (Harness·Skill 담당).
- 없으면 Skill/Harness 안내 후 **중단** — `tests/`에 `34`/`16`/`4` 리터럴 산포 금지.

### `tests/conftest.py` — `grid_g1`

| fixture | 내용 |
|---------|------|
| **`grid_g1`** | 4×4 격자, **`0` 두 칸**, **row-major** 순서로 빈칸 위치가 테스트에서 추론 가능 |

- 플랜·Skill에 정의가 있으면 그 정의를 따른다.
- conftest에 **`grid_g1`만** 추가·수정 (다른 fixture는 플랜에 명시된 경우만).
- `grid_g1` 예시 의도: 부분 마방진(빈칸 2개) Arrange — `test_*_blank_coords_row_major` 계열에서 row-major 좌표 `(r,c)` 도출.

---

## 파일 범위

| 경로 | Skeleton에서 |
|------|----------------|
| `tests/test_*.py` | **작성·수정** — RED 묶음 함수 추가 |
| `tests/conftest.py` | **`grid_g1` 등 플랜 명시 fixture만** |
| `src/` | **수정 금지** |
| `entity/constants.py` | **import만** (수정 금지) |

---

## 템플릿 예시

파일: `tests/test_validate_lines.py`  
Test ID: `D-LOC-01` · 함수: `test_d_loc_01_blank_coords_row_major`

```python
import pytest

from entity.constants import MAGIC_SUM
from src.validate_lines import validate_lines


def _blank_coords_row_major(grid):
    """Return [(r, c), ...] for cells == 0 in row-major order."""
    coords = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                coords.append((r, c))
    return coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given
    grid = grid_g1
    blank_coords = _blank_coords_row_major(grid)

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: D-LOC-01 — ok=false, status=fail, "
        f"failed_lines=[{{id:R1, sum:33, expected:{MAGIC_SUM}}}] "
        f"(blank_coords row-major={blank_coords})"
    )
```

- **Given:** `grid_g1` + row-major 빈칸 좌표 (플랜이 `FAIL_GRID_R1`이면 파일 내 상수로 Given만 바꾸고 **Then은 여전히 `pytest.fail` 한 줄**).
- **When:** 대상 Command 1회 호출 (플랜의 대상 함수).
- **Then:** assert 없음 — **`pytest.fail`만**.

함수명·Test ID·Then 문구는 **플랜 Track B 표**와 1:1 매핑한다.

---

## 실행 절차 (에이전트)

1. 채팅에서 `/red-test-plan` RED 묶음·Test ID·함수명·Then 추출.
2. `magic-square-tdd` Skill 있으면 읽고 관례 적용.
3. `tests/conftest.py` — `grid_g1` 없으면 플랜/Skill 기준 추가.
4. `tests/test_*.py` — RED 묶음마다 AAA + `pytest.fail` 스켈레톤 추가.
5. **`pytest`** 실행 (플랜 명령 또는 `pytest tests/ -v`).
6. **보고 형식** 출력.

---

## 보고 형식

```
Phase: red | Layer: entity | Track: Logic

## 변경 (tests/만)
- tests/conftest.py: grid_g1 fixture (없을 때만)
- tests/test_validate_lines.py: test_d_loc_01_blank_coords_row_major — D-LOC-01 스켈레톤

## pytest 결과
| Test ID | 결과 |
|---------|------|
| D-LOC-01 | FAIL — RED: D-LOC-01 — … |

- 명령: pytest tests/test_validate_lines.py::test_d_loc_01_blank_coords_row_major -v

## 다음
- `/tdd-red`: pytest.fail → assert 본문으로 RED 완성
- `/green-minimal`: src/validate_lines.py 최소 구현
- 이후: `/golden-master` → `/refactor-smell` → `/refactor-safe`
```

각 Test ID당 **FAIL 한 줄** 요약. PASS인 새 테스트가 있으면 **스켈레톤 위반** — `pytest.fail` 누락 확인.

---

## 금지 (Skeleton 위반)

| 금지 | 이유 |
|------|------|
| **`src/` 수정** | GREEN 담당 |
| **`entity/constants.py` 수정** | Harness·Skill SSOT |
| **`assert` 본문** | `/tdd-red` |
| **`skip` / `xfail` / `pytest.skip()`** | TDD 금지 |
| **통과 더미** (`pass`, assert True) | RED 아님 |
| **GREEN · REFACTOR** | 한 Phase만 |
| **플랜 밖 Test ID** | RED 묶음 범위 준수 |
| **매직 넘버 `34`/`16`/`4` 직접 산포** | `entity.constants` import |
| **Logic Track Domain Mock** | ECB 점검 |

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ③ | `/red-test-plan` | C2C · Track B · 테스트 플랜 (코드 없음) |
| ④ | **`/red-skeleton`** | `pytest.fail` 스켈레톤 (`tests/`만) |
| ⑤ | `/tdd-red` | assert 본문 RED · GREEN 준비 |

---

## 참조

- 설계(앞단): `.cursor/commands/red-test-plan.md`
- assert RED: `.cursor/commands/tdd-red.md`
- GREEN: `.cursor/commands/green-minimal.md`
- golden: `.cursor/commands/golden-master.md`
- Export: `.cursor/commands/export-session.md`
- Skill: `magic-square-tdd`
- PRD: `docs/PRD.md`
- 규칙: `.cursorrules`
- Mom Test · R-G-I-O: `Report/Session3_Workbook.md`
