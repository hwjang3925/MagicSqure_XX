# MagicSquare_xx — 세션 3 워크북 (Mom Test → R-G-I-O)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx |
| 단계 | 세션 3 — Rule · Command · (Skill) · Test Loop |
| 근거 | [MomTest_STEP1_Report.md](./MomTest_STEP1_Report.md) |
| 프롬프트 | [Session3_Workbook_Prompt.md](../Prompt/Session3_Workbook_Prompt.md) |
| 일자 | 2026-06-10 |
| 상태 | **완료** |

---

## Mom Test 결과 (입력)

### 페르소나

4×4 **부분 마방진**을 손으로/코드로 다루는 학습자.  
4×4 마방진(합=34)에서 **빈칸 2개 위치 찾기·채우기**와 **ECB(엔티티·컨트롤·바운더리) 분류** 프로젝트를 진행 중.

### 진짜 문제 (한 문장)

> 부분 마방진을 맞출 때 검증 조건(행·열·대각선)을 하나 빠뜨리면, 이미 맞췄다고 믿은 채로 시간을 쓰게 된다.

### Mom Test 증거 3줄

1. **지난주**, 빈칸 2개를 넣고 행·열·대각선 합을 맞추는 작업을 했다.
2. **대각선 하나**를 검증에서 빼먹었다.
3. 그 때문에 **약 20분**을 썼다.

---

## 1) 주제 (1문장 · Mom Test 기반 · 솔루션 최소화)

> **4×4 부분 마방진에서 빈칸을 채운 직후, 행·열·대각선 10선이 각각 34인지 빠르게 확정하고, 틀리면 어느 줄인지 바로 짚을 수 있게 검증 규칙과 테스트 루프를 만든다.** 미완성 격자(0 포함)는 `incomplete`로 구분한다.

*(앱·솔버·UI·ECB 설계표가 아니라 **판정·확인 비용**만 다룸)*

---

## 2) R-G-I-O

| | 내용 |
|---|---|
| **R — Role** | 4×4 **부분** 마방진 학습자. 빈칸 2개(0)를 1~16으로 채운 뒤 **맞았는지 스스로 확인**해야 함 |
| **G — Goal** | 빈칸 채운 후 **10선 합 34 여부를 즉시 판정**하고, 틀리면 **어느 행·열·대각선**인지 식별 *(20분 낭비 → 처음·한 번에)* |
| **I — Input** | `grid: list[list[int]]` — 4×4 정수 격자. 셀 값 **0**(빈칸) 또는 **1~16** |
| **O — Output** | `validate_lines(grid)` → **ValidationResult**: `ok` (bool), `status` (`"pass"` \| `"fail"` \| `"incomplete"`), `lines[]` — fail 시 **틀린 줄만** `{ id, sum, expected: 34 }`. 줄 ID: `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`. **R5:** 격자에 `0`이 하나라도 있으면 `status=incomplete`, 합 계산·34 비교는 수행하지 않음 |

---

## 3) 성공 기준 3개 (Mom Test 증거 연결)

| # | 성공 기준 | 연결 증거 |
|---|-----------|-----------|
| 1 | **`validate_lines(grid)`** 한 번으로 **10선×34 검증**을 수행한다 (행 4 + 열 4 + 대각 2) | “행·열·**대각선** 합 맞췄는데 **대각선 하나를 빼먹어서**” |
| 2 | Test Loop **Red→Green**: Red — 합≠34 → `ok=false`, `status=fail`; Red — `0` 포함 → `status=incomplete`; Green — 정답 격자 → `ok=true`, `status=pass` | “**34가 안 맞아 20분** 날렸다” → 같은 실패를 테스트로 고정 |
| 3 | fail 시 `lines[]`에 **틀린 줄 ID**(`row:2`, `diag:main` 등)와 `sum`, `expected: 34`를 반환한다 (10선 전부 검사, 줄 누락 없음) | “맞는지 **판정하지 못하고**” 같은 시도 반복 → **줄 단위**로 짚어야 함 |

---

## 4) 표면 문제 — 이번 프로젝트에서 하지 않을 것

| 하지 않음 | 이유 (Mom Test) |
|-----------|-----------------|
| BCE 전체 / `GridUI` / `InputHandler` | UI·입력은 **표면 솔루션** — 이번 고통은 **판정·확인** |
| `Solver` / 빈칸 자동 채우기 / 힌트 | 학습자 고통은 **풀기**보다 **맞는지 확인** |
| BCE 분류·클래스 설계만 하고 테스트 없음 | 과제는 **설계표** — 검증·재현 없음 |
| 1~16 중복·범위 검증까지 한꺼번에 | 세션 3 범위 밖 — **합 34 판정**에 집중 |
| “Validator 클래스 필요”, “자동 검증 UI”, “TDD로 테스트 먼저” | 솔루션 제안 — **기록만** 하고 진짜 문제로 쓰지 않음 |

---

## 8계층 — 이번 세션에서 만드는 것만

| 계층 | 세션 3에서 할 일 | Mom Test 연결 |
|------|------------------|---------------|
| **Rule** | R1~R5: **행·열·대각선 합 = 34** 판정. R5 — 0(빈칸) 포함 시 `status=incomplete` (**fail과 구분**, 합 검증 생략) | “34가 안 맞았는지” **판정 기준**을 코드·문서로 고정 |
| **Command** | `validate_lines(grid)` → `ValidationResult` — 10선 합 계산 + 34 비교 + fail 시 **틀린 줄 ID·sum·expected** 반환 | 합 확인에 **20분** → **한 Command**로 대체 |
| **(Skill)** | *(선택)* pytest 실행 / 격자 fixture 준비 Skill | 매번 손으로 10선 더하기 제거 |
| **Test Loop** | Red: 합≠34 → `ok=false`, `status=fail`, **실패 줄** assert; Red: `0` 포함 → `status=incomplete`; Green: 정답 격자 → `ok=true`, `status=pass` | **20분 낭비** → **같은 실패를 1번에 재현** |

**이번 세션에서 만들지 않음:** Entity(`MagicSquare`/`Cell`), Boundary(`ResultDisplay`), Solver, MissingFinder, 전체 BCE, Hook, MCP

---

## 다음 단계

1. **Rule + Command + Test Loop 구현** — `validate_lines` 우선
2. **(선택) 추가 Mom Test** — 질문 3(누락 발견 전 심리 상태)으로 진짜 문제 문장 정교화
3. **Solver / UI / BCE 전체** — 세션 3 이후
