# TDD RED — validate_lines

`validate_lines` TDD 사이클의 **RED 단계 전용** Cursor Command.
**한 번에 RED만** 수행한다. GREEN·REFACTOR는 이 Command 범위 밖.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: RED
```

---

## RED 목표

`tests/test_validate_lines.py`에 **아직 통과하지 않는** 테스트를 추가·강화한다.
실패 원인은 **구현 부재 또는 미완성**이어야 하며, 테스트 자체 결함이면 안 된다.

RED 완료 조건:

1. `tests/`만 변경했다.
2. `pytest tests/test_validate_lines.py` — **새·강화한 테스트는 FAIL** (또는 `validate_lines` 미구현으로 ERROR).
3. assert는 `.cursorrules` 스키마를 **엄격히** 검증한다.

---

## AAA 절차

각 테스트 함수는 **Arrange → Act → Assert** 순서를 지킨다.

| 단계 | 내용 |
|------|------|
| **Arrange** | 4×4 `grid: list[list[int]]` 준비. 셀은 `0`(빈칸) 또는 `1~16`. 시나리오별로 pass / fail / incomplete 격자를 명확히 구분 |
| **Act** | `result = validate_lines(grid)` 한 번 호출 |
| **Assert** | `result["ok"]`, `result["status"]`, `result["failed_lines"]`를 시나리오별 규칙에 맞게 검증 |

### 시나리오별 assert 기준

| status | ok | failed_lines | 추가 검증 |
|--------|-----|--------------|-----------|
| `pass` | `True` | `[]` | 0 없음, 10선 모두 `MAGIC_SUM` |
| `fail` | `False` | 틀린 줄만, **누락 없음** | 각 항목 `id`, `sum`, `expected` (= `MAGIC_SUM`) |
| `incomplete` | `False` | `[]` | `0` 포함 — **합 계산·34 비교 없음** (status만으로 구분) |

- 줄 ID: **`R1`~`R4`, `C1`~`C4`, `D1`, `D2`** 만 사용
- `expected`는 매직 넘버 `34` 직접 사용 금지 → `MAGIC_SUM` 참조

---

## pytest 예시

파일: `tests/test_validate_lines.py`

```python
from src.validate_lines import MAGIC_SUM, validate_lines

# --- Arrange helpers (격자는 테스트 의도가 드러나게) ---

PASS_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

FAIL_GRID_R1 = [
    [16, 3, 2, 12],  # R1 sum != MAGIC_SUM
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

INCOMPLETE_GRID = [
    [0, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_pass_all_ten_lines_sum_to_magic_constant():
    # Arrange
    grid = PASS_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["ok"] is True
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


def test_fail_reports_wrong_line_with_id_sum_and_expected():
    # Arrange
    grid = FAIL_GRID_R1

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["ok"] is False
    assert result["status"] == "fail"
    assert result["failed_lines"] == [
        {"id": "R1", "sum": 33, "expected": MAGIC_SUM},
    ]


def test_incomplete_skips_line_validation_when_zero_present():
    # Arrange
    grid = INCOMPLETE_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["ok"] is False
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []
```

RED에서 **한 시나리오(또는 한 실패 줄)씩** 테스트를 추가해도 된다.  
`fail` 테스트는 `id`·`sum`·`expected`를 **모두** assert한다.

---

## 실행

```bash
pytest tests/test_validate_lines.py -v
```

RED 성공 = 새 테스트가 **의도대로 FAIL** (또는 미구현 ERROR).  
전체 suite가 GREEN이면 RED가 아니다 — assert를 더 엄격히 하거나 아직 없는 동작을 테스트한다.

---

## 보고 형식

작업 완료 시 아래 순서로 보고한다.

```
Phase: RED

## 변경
- tests/test_validate_lines.py: <추가·수정한 테스트 함수명과 의도 1줄>

## pytest 결과
- <실행 명령>
- <FAIL/ERROR 난 테스트명과 실패 메시지 요약>
- (pass한 기존 테스트가 있으면 함께 명시)

## 다음
- GREEN: src/validate_lines.py 최소 구현으로 위 FAIL 해소
```

---

## 금지 (RED 위반)

| 금지 | 이유 |
|------|------|
| **`src/` 및 `tests/` 외 경로 수정** | RED는 테스트만 |
| **`src/validate_lines.py` 구현·스텁 확장** | GREEN 담당 |
| **`skip` / `xfail` / `pytest.skip()`** | 실패를 숨김 |
| **assert 완화·삭제·모호한 matcher** (`in`, `>=`, `is not None`만으로 통과 등) | 요구사항 우회 |
| **GREEN·REFACTOR 동시 진행** | 한 Phase만 |
| **줄 ID 다른 형식** (`row:0`, `diag:main` 등) | 프로젝트 표준 위반 |
| **매직 넘버 `34` 직접 산포** | `MAGIC_SUM` SSOT |

---

## 참조

- API·10선·`MAGIC_SUM`: `.cursorrules`
- 구현 파일 (RED에서 수정 금지): `src/validate_lines.py`
- 테스트 파일 (RED에서만 수정): `tests/test_validate_lines.py`
