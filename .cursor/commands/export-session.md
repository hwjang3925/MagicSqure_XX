# Export Session — Report · Transcript

MagicSquare_1004 **ARRR 실습** — 세션 종료 시 **보고서**와 **Transcript**를 `NN.XXX` 파일명 규칙으로 저장하는 Cursor Command.

`/export-session`만으로 동작한다 — **추가 입력·질문 금지**. 슬러그·Phase·Test ID는 **현재 채팅** · **`.cursorrules`** · **`docs/PRD.md`** · **pytest/git 결과**에서 자동 추출한다.

> **Skill:** Export 시 **magic-square-docs** Skill 로드 → [phase-checklist.md](../skills/magic-square-docs/phase-checklist.md) Step A~F 수행.

---

## 파일명 규칙 (`01.XXX`)

| 항목 | 패턴 | 예시 |
|------|------|------|
| **번호** | `01`, `02`, … — 해당 폴더 기존 `NN.` 접두 최대값 + 1 | `01`, `02` |
| **슬러그** | PascalCase 또는 Snake_Case, 공백·특수문자 없음 | `TDD_RED_Command` |
| **Report** | `Report/NN.Slug_Report.md` | `Report/01.TDD_RED_Command_Report.md` |
| **Transcript** | `Prompting/NN.Slug_Transcript.md` | `Prompting/01.TDD_RED_Command_Transcript.md` |

- Report와 Transcript는 **같은 NN·Slug**를 쌍으로 사용한다.
- 폴더가 없으면 `Report/`, `Prompting/`을 만든다.
- 기존 `Session3_Workbook.md` 등 **구형 파일명**은 유지; **신규 export부터** `01.XXX` 적용.

---

## 실행 절차

1. **슬러그 결정** — 세션 주제를 2~4단어 PascalCase로 (예: `TDD_RED_Command`, `MomTest_STEP1`)
2. **번호 부여** — `Report/`·`Prompting/`에서 `^\d{2}\.` 파일 glob 후 다음 번호
3. **Report 작성** — 아래 템플릿
4. **Transcript export** — 현재 대화를 읽기 쉬운 Markdown으로 (user / assistant 구분, 도구 호출은 `[tool]` 한 줄 요약)
5. **완료 보고** — 저장 경로 2개와 슬러그·번호 명시

---

## Report 템플릿

```markdown
# {제목} — MagicSquare_1004

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_1004 |
| 단계 | {세션 단계} |
| 일자 | {YYYY-MM-DD} |
| 상태 | **종료** |
| Transcript | [Prompting/{NN}.{Slug}_Transcript.md](../Prompting/{NN}.{Slug}_Transcript.md) |

---

## 요약

{세션 목표·결과 2~4문장}

## 산출물

| 파일 | 설명 |
|------|------|
| `{path}` | {한 줄 설명} |

## 결정·규칙

- {bullet}

## 다음 단계

- {bullet}
```

---

## Transcript 템플릿

```markdown
# Transcript — {제목}

| 항목 | 내용 |
|------|------|
| 세션 ID | {agent transcript uuid 또는 "current"} |
| 일자 | {YYYY-MM-DD} |
| Report | [Report/{NN}.{Slug}_Report.md](../Report/{NN}.{Slug}_Report.md) |

---

## 대화

### User
{질문·요청}

### Assistant
{응답 요약 — 코드·경로 포함}

...
```

---

## 금지

- Report만 저장하고 Transcript 생략
- `01.XXX` 규칙 없이 임의 파일명 사용
- Transcript를 `Prompt/`에 저장 (`Prompting/` 전용)
- git commit·push (사용자 명시 요청 전)

---

## 참조

- Skill: `.cursor/skills/magic-square-docs/SKILL.md` — Report·Transcript SSOT·Step A~F
- TDD Skill: `.cursor/skills/magic-square-tdd/SKILL.md`
- Command 체인: `red-test-plan` → … → `refactor-safe` → **`export-session`**
- TDD RED: `.cursor/commands/tdd-red.md`
- PRD: `docs/PRD.md` (없으면 `.cursorrules` + 워크북)
- 프로젝트 규칙: `.cursorrules`
