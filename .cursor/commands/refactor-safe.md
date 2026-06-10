# REFACTOR Safe — Budget 내 P0 1건 안전 리팩터 (Refine ⑧)

MagicSquare_1004 **ARRR 실습** — Refine **⑧** 전용 Cursor Command.
직전 **`/refactor-smell`** 스멜 표에서 **P0 후보 1건**만 Change Budget 내에서 안전 리팩터한다.

`/refactor-safe`만으로 동작한다 — **추가 입력·질문 금지**. 채팅에 후보가 없으면 `src/`·`tests/`를 읽고 Budget **OK**인 **P0 1건**을 자동 선정한다.

> **Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** — Budget·golden·ECB 관례는 Skill을 SSOT로 우선 적용한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (소문자 `refactor`):

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

| 필드 | 값 | 비고 |
|------|-----|------|
| **Phase** | `refactor` | **적용** — Refine ⑧, smell(⑦) 다음 |
| **Scope** | `src/` · `tests/` | entity/·boundary 포함 |
| **Track** | `Logic+UI` | Dual-Track 동일 Budget·golden 규칙 |

---

## Safe 목표

**P0 스멜 1건**을 Budget 내에서 리팩터하고 **C2C·golden·pytest 전부 PASS**를 유지한다.

완료 조건:

1. **전제 pytest 전부 PASS** — 아니면 **즉시 중단**.
2. 적용 대상 **스멜 ID 1건**(P0, Budget OK) 확정.
3. **Change Budget** 이내 diff만 (`파일≤3` · `클래스≤1` · `메서드≤3`).
4. 리팩터 후 `python -m pytest tests/ -v` **전부 PASS**.
5. **기능 추가·C2C Then 변경·assert 완화 없음**.
6. **commit은 사용자 요청 시만**.

---

## Change Budget (1회 상한)

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

Budget **초과** 작업은 **분할** — 본 Command에서 하지 않고 `/refactor-smell` 재실행 안내.

---

## 전제 (필수 · 실패 시 중단)

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|------|------|
| **전부 PASS** | 리팩터 진행 |
| **FAIL·ERROR** | **즉시 중단** — GREEN/fix 먼저 |

---

## 입력 (SSOT · 추가 질문 없음)

| 순서 | 소스 | 사용 |
|------|------|------|
| 1 | 현재 채팅 | `/refactor-smell` 스멜 표 · `/refactor-safe` 후보 #1 |
| 2 | `.cursor/commands/refactor-smell.md` | P0·Budget·스멜 유형 |
| 3 | `.cursorrules` | API·`MAGIC_SUM`·줄 ID·TDD 금지 |
| 4 | `docs/PRD.md` | FR·Test ID (없으면 `.cursorrules` + `Report/Session3_Workbook.md`) |
| 5 | `magic-square-tdd` Skill | Budget·golden·constants SSOT |

후보 자동 선정: smell 후보 **#1**(P0·Budget OK) → 없으면 스캔 후 **가장 작은 P0** 1건.

---

## 절차 (순서 고정)

| # | 단계 | 내용 |
|---|------|------|
| 1 | **pytest 전제** | 전부 PASS 확인 |
| 2 | **대상 확정** | 스멜 ID · 파일 · 함수 · 한 줄 제안 |
| 3 | **Budget 확인** | 예상 diff가 상한 이내 |
| 4 | **리팩터** | 동작 동일 — 추출·rename·상수화·중복 제거만 |
| 5 | **pytest 재실행** | `python -m pytest tests/ -v` 전부 PASS |
| 6 | **보고** | 적용 요약 · Budget · 회귀 없음 |

### 허용 리팩터 (예)

| 스멜 | Safe 조치 |
|------|-----------|
| Magic Number | `MAGIC_SUM`·`GRID_SIZE` import, 리터럴 제거 |
| Duplicated Code | private helper 추출 (메서드≤3) |
| Long Method | 10선 순회·합 계산 분리 (동작 동일) |
| Mysterious Name | 변수·함수 rename (public API 변경 시 tests 동기화) |

### 금지 리팩터

| 금지 | 이유 |
|------|------|
| C2C Then·status 의미 변경 | 계약 위반 |
| assert 완화·삭제 | golden·TDD 우회 |
| `failed_lines` 줄 ID 형식 변경 | `.cursorrules` |
| E001~E005 emit | ECB 범위 |
| Budget 초과 일괄 정리 | 1회 1 P0 |

---

## golden 유지

- `/golden-master`로 연결된 `tests/golden/*.approved.txt`가 있으면 **matched 유지**.
- 직렬화 포맷(`INT6:`·`STATUS:`·`LINES:`) **변경 금지**.
- golden FAIL 시 구현·직렬화 수정 후 `UPDATE_GOLDEN=1`은 **`/golden-master`·사용자 지시**에서만.

---

## pytest 명령

```bash
python -m pytest tests/ -v
```

단일 파일 회귀 (선택):

```bash
python -m pytest tests/test_validate_lines.py -v
```

Safe 완료 = **전후 전부 PASS** + **C2C Then 불변**.

---

## git · 커밋

- **사용자 명시 요청 전 `git commit` · `push` 금지.**
- 커밋 시: `refactor: {스멜 ID} {한 줄 요약}` (예: `refactor: S-01 MAGIC_SUM SSOT`).

---

## 보고 형식

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## 적용
| 스멜 ID | 스멜 유형 | 변경 요약 | Budget |
|---------|-----------|-----------|--------|
| S-01 | Magic Number | src/validate_lines.py expected→MAGIC_SUM | 파일1·메서드1 |

## 변경 파일
- src/validate_lines.py: …

## pytest
- 전: N passed → 후: N passed

## golden
- matched 유지 / 해당 없음

## 회귀
- 없음

## 다음
- 추가 P0: /refactor-smell → /refactor-safe
- 세션 종료: /export-session
```

---

## 금지 (Safe 위반)

| 금지 | 이유 |
|------|------|
| **P0 2건 이상 동시 적용** | 1회 1 P0 |
| **Budget OVER** | 범위 초과 |
| **pytest FAIL 상태에서 리팩터** | 전제 위반 |
| **기능 추가·RED·GREEN 혼합** | Phase 혼합 |
| **`skip` / `xfail` / `pytest.skip()`** | TDD 금지 |
| **golden 수동 편집으로 PASS** | Approval 우회 |
| **git commit·push (사용자 미요청)** | 프로젝트 규칙 |

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ⑦ | `/refactor-smell` | 스멜 표 + safe 후보 1~3 |
| **⑧** | **`/refactor-safe`** | P0 1건 · pytest 유지 |
| — | `/export-session` | Report · Transcript (선택) |

---

## 참조

- smell: `.cursor/commands/refactor-smell.md`
- golden: `.cursor/commands/golden-master.md`
- Skill: `magic-square-tdd`
- 규칙: `.cursorrules`
- PRD: `docs/PRD.md` (없으면 워크북 + rules)
- Export: `.cursor/commands/export-session.md`
