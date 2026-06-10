# REFACTOR Smell — 코드 스멜 탐지 (Refine)

MagicSquare_1004 **ARRR 실습** — Refine **⑦** 전용 Cursor Command.
**코드 스멜 탐지·분류만** 수행한다. **수정·commit 금지.**

`/refactor-smell`만으로 동작한다 — **추가 입력·질문 금지**. `src/`·`tests/`를 읽고 스멜을 자동 분류한다.

GREEN 완료 후, `/refactor-safe` 실행 전 **스멜 후보를 식별·우선순위화**한다.

> **Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** — 상수·레이어·ECB 관례는 Skill을 SSOT로 우선 적용한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (소문자 `refactor`):

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

| 필드 | 값 | 비고 |
|------|-----|------|
| **Phase** | `refactor` | **탐지만** — Refine ⑦, 실제 리팩터는 `/refactor-safe` |
| **Scope** | `src/` · `tests/` | 스캔 대상 경로 (entity/·boundary/ 포함 시 동일 절차) |
| **Track** | `Logic+UI` | Logic(entity/src) + UI(boundary) 모두 점검 |

---

## Refine 목표

현재 코드베이스에서 **리팩터 후보 스멜**을 찾아 **P0/P1/P2**로 분류한다.

완료 조건:

1. **전제 pytest 전부 PASS** — 아니면 **즉시 중단** (스멜 보고 없음).
2. **`src/`·`tests/`를 읽고** 스멜 후보를 식별했다.
3. **스멜 표**와 **`/refactor-safe` 넘길 후보 1~3개**를 출력했다.
4. **파일·코드 수정·commit 없음.**

---

## 전제 (필수 · 실패 시 중단)

아래 명령을 **먼저** 실행한다.

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|------|------|
| **전부 PASS** | 스멜 탐지 진행 |
| **FAIL·ERROR 1건이라도** | **즉시 중단** — 스멜 표·후보 출력 **금지**. FAIL Test ID·원인 1~2줄만 보고하고 GREEN/fix 먼저 안내 |

> RED·GREEN 미완 상태에서 Refine하지 않는다.

---

## 스멜 분류 (P0 / P1 / P2)

| 우선순위 | 의미 | `/refactor-safe` 적용 |
|----------|------|------------------------|
| **P0** | 테스트·계약·ECB에 직접 위협; Change Budget 내 **즉시** 다룰 가치 | **1회 1건만** 선택 |
| **P1** | 가독성·중복·명명 — 동작은 안전, 다음 사이클 | 후보 풀 |
| **P2** | 미미·취향·범위 밖 — 기록만 | 보통 보류 |

### 스멜 유형 (열)

| 스멜 | 탐지 힌트 |
|------|-----------|
| **Long Method** | 한 함수·메서드가 **20줄 초과** 또는 책임 2개 이상 (10선 순회 + 상태 조립 + 반환 등) |
| **Duplicated Code** | 동일·유사 블록 **2회 이상** (행/열/대각 합 계산, failed_lines 조립, fixture Arrange 등) |
| **Mysterious Name** | `x`, `tmp`, `data`, `check` 등 **의도 불명**; 줄 ID·status·grid 역할이 이름에 없음 |
| **Magic Number** | `34`, `4`, `16` 등 **리터럴 산포** — `MAGIC_SUM`·`GRID_SIZE`·`CELL_MAX` SSOT 미사용 |
| **ECB 위반** | entity → boundary/control import; E001~E005 **조기 emit**; Command가 UI·Solver에 누수 |
| **Feature Envy** | A 모듈이 B의 데이터·구조를 **과다 순회·변형** (테스트가 src 내부 순서에 과의존 등) |

Logic Track(`src/`, `entity/`)과 UI Track(`boundary/`, 테스트 Arrange) **모두** 위 유형으로 점검한다.

---

## Change Budget (후보 선정 시 필터)

`/refactor-safe` 한 번 실행당 **예상 변경 상한**. 스멜 보고 시 각 후보가 Budget **이내**인지 표시한다.

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

Budget **초과** 스멜은 P0라도 **`/refactor-safe` 후보에서 제외**하고 P1·분할 제안으로 내린다.

---

## 실행 절차 (에이전트)

| # | 단계 | 내용 |
|---|------|------|
| 1 | **pytest 전제** | `python -m pytest tests/ -v` — FAIL이면 **중단** |
| 2 | **Scope 스캔** | `src/` · `tests/` (및 `entity/` · boundary 모듈) 읽기 |
| 3 | **스멜 식별** | 6유형 × P0/P1/P2 분류; 위치(파일·함수·줄 근사) 기록 |
| 4 | **Budget 필터** | P0·P1 중 Budget 이내만 `/refactor-safe` 후보 풀 |
| 5 | **출력** | 스멜 표 + 후보 1~3개 + 다음 안내 (수정·commit **없음**) |

---

## 출력 형식 (필수)

### 1. pytest 전제

```
pytest: N passed (전부 PASS) → Refine 진행
```

또는 (FAIL 시):

```
pytest: FAIL — Refine 중단. [Test ID / 파일 1줄]
```

### 2. 스멜 표

| ID | P | 스멜 유형 | 위치 (파일 · 함수) | 요약 | Budget |
|----|---|-----------|-------------------|------|--------|
| S-01 | P0 | Magic Number | `src/validate_lines.py` · `validate_lines` | `34` 리터럴 | OK (파일1·메서드1) |
| … | … | … | … | … | OK / OVER |

- **ID:** `S-01`, `S-02`, … (보고서 내 고유)
- **Budget:** `OK` = 파일≤3·클래스≤1·메서드≤3 예상 / `OVER` = 초과

### 3. `/refactor-safe` 후보 (1~3개)

Budget **OK**인 항목만. **P0 우선**, 동순위면 **영향 범위 작은 것** 우선.

| 후보 | 스멜 ID | 한 줄 제안 | 예상 diff |
|------|---------|------------|-----------|
| **1** | S-01 | `MAGIC_SUM` import로 매직 넘버 제거 | `src/validate_lines.py` 1파일 |
| 2 | … | … | … |

후보가 없으면: **`/refactor-safe` 넘길 P0 없음 — GREEN 유지`** 명시.

### 4. 다음 안내 (마지막 줄)

```
P0 후보 1개만 골라 /refactor-safe 실행
```

---

## 보고 예시

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest
python -m pytest tests/ -v → 12 passed — Refine 진행

## 스멜 표
| ID | P | 스멜 유형 | 위치 | 요약 | Budget |
|----|---|-----------|------|------|--------|
| S-01 | P0 | Magic Number | src/validate_lines.py · validate_lines | expected에 34 리터럴 | OK |
| S-02 | P1 | Duplicated Code | tests/test_validate_lines.py | PASS/FAIL grid Arrange 중복 | OK |

## /refactor-safe 후보
| 후보 | 스멜 ID | 한 줄 제안 | 예상 diff |
|------|---------|------------|-----------|
| 1 | S-01 | MAGIC_SUM SSOT 통일 | src/ 1파일 |

## 다음
P0 후보 1개만 골라 /refactor-safe 실행
```

---

## 금지 (Refine Smell 위반)

| 금지 | 이유 |
|------|------|
| **`src/`·`tests/`·기타 코드 수정** | 탐지만 — `/refactor-safe` 담당 |
| **git commit · push** | Refine은 read-only |
| **pytest FAIL 상태에서 스멜 보고** | 전제 위반 |
| **Budget OVER 후보를 `/refactor-safe`에 넣기** | 1회 리팩터 범위 초과 |
| **P0 여러 건 동시 `/refactor-safe` 권유** | **1회 1 P0** |
| **테스트 assert 완화·skip·xfail** | TDD 금지 |
| **기능 추가·GREEN·RED 혼합** | Refine ≠ Respond |

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| R | `/green-minimal` 등 | pytest **전부 PASS** |
| **⑦** | **`/refactor-smell`** | 스멜 표 + `/refactor-safe` 후보 1~3 |
| ⑧ | **`/refactor-safe`** | Budget 내 **P0 1건** 안전 리팩터 + pytest 유지 |

---

## 참조

- 규칙: `.cursorrules`
- PRD: `docs/PRD.md`
- GREEN: `.cursor/commands/green-minimal.md`
- 안전 리팩터: `.cursor/commands/refactor-safe.md`
- Export: `.cursor/commands/export-session.md`
- Skill: `magic-square-tdd`
- 워크북: `Report/Session3_Workbook.md`
