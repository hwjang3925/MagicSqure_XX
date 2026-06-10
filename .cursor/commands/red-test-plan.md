# RED Test Plan — C2C · 테스트 플랜 (Ask)

MagicSquare_1004 **ARRR 실습** — Ask **③** 전용 Cursor Command.
**C2C 설계표·테스트 플랜만** 작성한다. 실제 테스트·구현 코드는 **`/red-skeleton`** 이후.

`/red-test-plan`만으로 동작한다 — **추가 입력·질문 금지**. 세션 주제·Test ID·FR은 **현재 채팅**, **`docs/PRD.md`**, **`.cursorrules`**, **`Report/Session3_Workbook.md`** 에서 자동 추출한다.

> **Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** — C2C·Track·ECB 관례는 Skill을 SSOT로 우선 적용한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (소문자 `red`):

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| **Phase** | `red` | 설계·플랜만 — 코드 RED 아님 |
| **Layer** | `entity` \| `boundary` | 세션 3 `validate_lines` 기본: **`entity`** |
| **Track** | `Logic` \| `UI` | 세션 3 기본: **`Logic`** (Track B) |

> **Track A(boundary):** 본 Command 본문은 **Track B(Logic · entity)** 기준이다. Boundary(UI) 작업 시 **`Layer: boundary`** 로만 바꾸면 **동일 절차·4블록 출력을 재사용**한다. Track은 UI로 두고 C2C·표·플랜·ECB 점검 형식은 그대로 따른다.

---

## Ask 목표

RED 실행 전 **Contract-to-Check(C2C)** 와 **pytest RED 묶음**을 문서화한다.

완료 조건:

1. **`tests/`·`src/` 파일을 생성·수정하지 않았다.**
2. 아래 **출력 4블록**을 표 형식으로 모두 채웠다.
3. Test ID·Given/When/Then·Expected RED Failure가 **`.cursorrules` 스키마**와 일치한다.
4. 마지막 줄: **`/red-skeleton 으로 넘길 준비됐다`**

---

## SSOT 추출 순서

추가 질문 없이 아래 순으로 읽고 반영한다.

| 순서 | 소스 | 추출 항목 |
|------|------|-----------|
| 1 | 현재 채팅 | 세션 주제, 이미 언급된 Test ID·함수명 |
| 2 | `docs/PRD.md` | FR 문구, Acceptance, Test ID 네이밍 (있으면) |
| 3 | `.cursorrules` | R1~R5, 10선 ID, `validate_lines` API, `MAGIC_SUM`, TDD 금지 |
| 4 | `Report/Session3_Workbook.md` | Mom Test 증거 ↔ 성공 기준, R-G-I-O |

`docs/PRD.md`가 없으면 **`.cursorrules` + 워크북**을 PRD FR 대용으로 쓴다.

### 세션 3 기본 앵커 (추출 실패 시)

| 항목 | 값 |
|------|-----|
| 주제 | 4×4 부분 마방진 — 빈칸 채운 직후 10선×34 판정, 틀린 줄 식별 |
| Command | `validate_lines(grid)` → `{ ok, status, failed_lines }` |
| 구현·테스트 경로 | `src/validate_lines.py` · `tests/test_validate_lines.py` |
| 줄 ID | `R1`~`R4`, `C1`~`C4`, `D1`, `D2` |
| 상수 | `MAGIC_SUM` (매직 넘버 `34` 직접 사용 금지) |

---

## 출력 4블록 (표 형식 · 필수)

응답 본문은 **아래 4개 섹션만** 순서대로 출력한다. 각 섹션은 **마크다운 표**로 작성한다.

### 1. C2C (Rule1~3)

Rule → PRD FR 인용 → **To-Do 1개** → Test ID + Given/When/Then.

| Rule | PRD FR (인용) | To-Do (1개) | Test ID | Given | When | Then |
|------|---------------|-------------|---------|-------|------|------|
| **Rule1** | FR: 완성 격자(0 없음)에서 10선 각각 합 = `MAGIC_SUM` | `pass` 시 `ok=true`, `status="pass"`, `failed_lines=[]` assert | `T-pass-01` | 4×4 정답 격자 | `validate_lines(grid)` | 위 Then |
| **Rule2** | FR: 합≠`MAGIC_SUM` 줄만 `failed_lines`에 id·sum·expected | `fail` 시 틀린 줄 **누락 없이** id·sum·`expected=MAGIC_SUM` assert | `T-fail-01` | R1 합만 틀린 격자 | 동일 | `status="fail"`, 해당 줄 1건 |
| **Rule3** | FR: `0` 포함 시 R5 — 합 계산·34 비교 생략, `incomplete` | `incomplete` ≠ `fail`; `failed_lines=[]` assert | `T-inc-01` | 0 포함 격자 | 동일 | `status="incomplete"`, `ok=false` |

- FR 인용은 **`docs/PRD.md` 해당 절**을 따옴표로 적는다. 없으면 `.cursorrules` 해당 Rule 문장을 인용한다.
- Test ID는 PRD·채팅에 있으면 그 네이밍을 쓰고, 없으면 **`T-{시나리오}-{nn}`** 형식으로 부여한다.
- Rule1~3 각 행 **To-Do는 정확히 1개**만.

### 2. Track B 표 (Logic · entity)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| `T-pass-01` | `validate_lines` | 정답 4×4 격자 → `ok=true`, `status="pass"`, `failed_lines=[]` | 10선 ID 표준; `expected`는 `MAGIC_SUM` | `ImportError` / `AttributeError` / assert `status` |
| `T-fail-01` | `validate_lines` | R1 sum ≠ `MAGIC_SUM` → `status="fail"`, `failed_lines=[{id,sum,expected}]` | fail 시 10선 전수 검사; 줄 ID `R1`~`D2` | assert `failed_lines` 내용 |
| `T-inc-01` | `validate_lines` | 0 포함 → `status="incomplete"`, `failed_lines=[]` | incomplete 시 **합 미계산** | assert `status` 또는 `failed_lines` 비어 있지 않음 |

- **Invariant:** RED에서도 깨지면 안 되는 계약 (줄 ID, `MAGIC_SUM`, incomplete≠fail 등).
- **Expected RED Failure:** `/red-skeleton` 실행 시 기대하는 pytest 결과 (`FAIL` / `ERROR` / assert 메시지 한 줄).

### 3. 테스트 플랜

| 항목 | 내용 |
|------|------|
| **테스트 파일** | `tests/test_validate_lines.py` |
| **대상 src** | `src/validate_lines.py` (`validate_lines`, `MAGIC_SUM`) |
| **테스트 함수 (RED 묶음)** | `test_pass_all_ten_lines_sum_to_magic_constant` · `test_fail_reports_wrong_line_with_id_sum_and_expected` · `test_incomplete_skips_line_validation_when_zero_present` (Test ID ↔ 1:1 매핑 명시) |
| **conftest / fixture** | 파일 내 `PASS_GRID`, `FAIL_GRID_*`, `INCOMPLETE_GRID` Arrange 상수; 공통 fixture 필요 시 `tests/conftest.py`에 `magic_sum` → `MAGIC_SUM` re-export **만** (플랜에 명시, 이 Command에서 생성 금지) |
| **pytest 명령** | `pytest tests/test_validate_lines.py -v` |
| **RED 묶음 범위** | 이번 Ask에서 확정한 Test ID 전부 — **한 번에 skeleton에 넣을 함수 목록**; GREEN 전까지 `src/` 미구현 가정 |

### 4. ECB · Mock 점검

| 점검 | Logic Track (entity) | UI Track (boundary) |
|------|----------------------|---------------------|
| **Domain Mock** | **금지** — `validate_lines`·격자를 Mock/stub으로 대체하지 않음 | Boundary만 Mock 가능 (플랜에 대상 명시) |
| **E001 emit** | Entity `MagicSquare` 생성·import **금지** | — |
| **E002 emit** | Entity `Cell` **금지** | — |
| **E003 emit** | Entity `SolveResult` **금지** | — |
| **E004 emit** | Control `Solver` / `MissingFinder` **금지** | — |
| **E005 emit** | Boundary `GridUI` / `InputHandler` / `ResultDisplay` **금지** | boundary Layer에서만 허용 |
| **범위** | 1~16 중복·범위 검증, Solver, UI **테스트·플랜에 포함 안 함** | 동일 |

Logic Track RED는 **순수 격자 + Command 호출**만. E001~E005에 해당하는 클래스·UI emit을 테스트 플랜에 넣지 않는다.

---

## 실행 절차 (에이전트)

1. SSOT 추출 (채팅 → PRD → `.cursorrules` → 워크북).
2. **Phase 선언** 한 줄 출력.
3. **출력 4블록** 표 작성 (세션에 맞게 행 추가·Test ID 갱신; 형식 유지).
4. ECB·Mock 점검표에서 **위반 항목 없음** 확인.
5. 마지막 줄: **`/red-skeleton 으로 넘길 준비됐다`**

---

## 금지 (Ask 위반)

| 금지 | 이유 |
|------|------|
| **`tests/`·`src/` 파일 생성·수정** | skeleton·RED 담당 |
| **`src/` 구현·스텁** | GREEN 담당 |
| **GREEN · REFACTOR 동시 진행** | Ask는 플랜만 |
| **`skip` / `xfail` / `pytest.skip()`** | 플랜·RED 모두 금지 |
| **assert 완화·모호한 matcher** (`in`, `>=`만 등) | C2C Then에 엄격 계약 명시 |
| **줄 ID 다른 형식** (`row:0`, `diag:main` 등) | `.cursorrules` 표준 |
| **매직 넘버 `34` 직접 산포** | `MAGIC_SUM` SSOT |
| **Logic Track Domain Mock** | Command 계약 직접 검증 |
| **E001~E005 emit** | 세션 3 범위 밖 ECB |

---

## 다음 Command

| Command | 역할 |
|---------|------|
| **`/red-skeleton`** | 본 플랜대로 `tests/`에 RED skeleton(실패 테스트) 작성 |
| **`/tdd-red`** | skeleton 이후 assert 본문 RED |

## Command 체인 (MagicSquare_1004 ARRR)

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master → /refactor-smell → /refactor-safe → /export-session
```

---

## 참조

- 프로젝트 규칙: `.cursorrules`
- PRD: `docs/PRD.md` (없으면 워크북 + rules)
- Skill: `magic-square-tdd`
- RED assert: `.cursor/commands/tdd-red.md`
- Export: `.cursor/commands/export-session.md`
- Mom Test · R-G-I-O: `Report/Session3_Workbook.md`
