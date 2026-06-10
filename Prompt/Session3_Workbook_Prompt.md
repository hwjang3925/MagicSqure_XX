# MagicSquare_xx — 세션 3 워크북 프롬프트 (Mom Test → R-G-I-O)

## 사용법

- **입력:** [MomTest_STEP1_Report.md](../Report/MomTest_STEP1_Report.md)의 Mom Test 결과(페르소나 · 진짜 문제 · 증거 3줄)
- **실행:** 아래 「워크북 작성 프롬프트」를 AI에 붙여 넣기
- **결과:** `Report/Session3_Workbook.md` 형식으로 정리
- **저장:** 「저장 프롬프트」로 Report · Prompt 폴더에 보관

---

## 워크북 작성 프롬프트

```
Mom Test 결과:
- 페르소나: [4×4 부분 마방진을 손으로/코드로 다루는 학습자 · 빈칸 2개 · ECB 분류 프로젝트]
- 진짜 문제 (한 문장): [부분 마방진을 맞출 때 검증 조건(행·열·대각선)을 하나 빠뜨리면, 이미 맞췄다고 믿은 채로 시간을 쓰게 된다]
- Mom Test 증거 3줄:
  1. 지난주, 빈칸 2개를 넣고 행·열·대각선 합을 맞추는 작업을 했다.
  2. 대각선 하나를 검증에서 빼먹었다.
  3. 그 때문에 약 20분을 썼다.

MagicSquare_xx 세션 3 워크북을 채워줘:
1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
2) R-G-I-O (Role/Goal/Input/Output)
3) 성공 기준 3개 (Mom Test 증거와 연결)
4) 표면 문제 — 이번 프로젝트에서 하지 않을 것
8계층 중 이번 세션에서 만드는 것만: Rule, Command, (Skill), Test Loop
```

*(대괄호 `[...]` 안을 Mom Test 보고서 내용으로 바꿔 사용)*

---

## 저장 프롬프트

```
종료하고 Report 폴더와 Prompt 폴더에 보고서와 프롬프트 저장해주세요
```

---

## 워크북 출력 체크리스트 (멘토용)

| # | 항목 | 확인 |
|---|------|------|
| 1 | 주제 1문장에 **솔루션(UI·솔버·클래스)** 최소화 | ☐ |
| 2 | R-G-I-O에 **Input/Output** 타입·함수명 명시 | ☐ |
| 3 | 성공 기준 3개 각각 **Mom Test 증거**와 1:1 연결 | ☐ |
| 4 | 표면 문제에 **하지 않을 것** + Mom Test 근거 | ☐ |
| 5 | 8계층 — **Rule · Command · (Skill) · Test Loop**만 | ☐ |
| 6 | R5 — `0`(빈칸) 포함 시 `incomplete` (**fail과 구분**) | ☐ |

---

## 세션 3 범위 요약

| 만들 것 | 만들지 않음 |
|---------|-------------|
| Rule (R1~R5: 10선 합=34) | Entity, Boundary, Solver |
| Command `validate_lines(grid)` | GridUI, MissingFinder |
| (Skill) pytest / fixture | 전체 BCE, Hook, MCP |
| Test Loop Red→Green | 1~16 중복·범위 검증 |

---

## Mom Test 규칙 (워크북 작성 시)

| 허용 | 금지 |
|------|------|
| 과거 사실·숫자(20분, 대각선 1개) | 미래 의견 ("~하면 좋겠다") |
| 고통·비용·제약 | 솔루션을 진짜 문제로 쓰기 |
| 증거 ↔ 성공 기준 연결 | "Validator 클래스 필요" 등을 **목표**로 쓰기 |

---

## 관련 문서

- `Report/Session3_Workbook.md` — 세션 3 워크북 (완료)
- `Report/MomTest_STEP1_Report.md` — Mom Test STEP 1 인터뷰 결과
- `Prompt/MomTest_STEP1_Interview.md` — STEP 1 인터뷰 실행 프롬프트
- `Report/MomTest_Questions10_Report.md` — Mom Test 질문 10개 보고서
- `Prompt/MomTest_Questions10_Prompt.md` — 질문 10개 프롬프트
