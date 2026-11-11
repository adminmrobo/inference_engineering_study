# 01 트랜스포머 — 형광펜만으로 번역하기 · 7개 언어판

AI 연구실 해설 대시보드 01 (Attention Is All You Need 해설). 글 · 안상선 ((주)M-Robo 대표)

| 언어 | 파일 |
|---|---|
| 목차 (첫 화면) | `index.html` — 7개 언어, `?lang=` 또는 브라우저 언어로 표시 |
| 한국어 (원본) | `01_transformer.html` |
| English | `01_transformer.en.html` |
| 中文 (简体) | `01_transformer.zh.html` |
| 日本語 | `01_transformer.ja.html` |
| Русский | `01_transformer.ru.html` |
| Oʻzbekcha | `01_transformer.uz.html` |
| Tiếng Việt | `01_transformer.vi.html` |

배치: `layout: "suffix"` (같은 폴더에 7개 파일). GitHub 웹 업로드로 그대로 올리면 됩니다.

## 언어 전환
- 상단 내비 오른쪽 끝의 언어 고르기 → 같은 섹션(`#r3` 등)을 유지한 채 그 언어 파일로 이동.
- `?lang=en`처럼 주소에 붙이면 그 언어로 바로 이동.
- 한국어 원본에 다른 사이트에서 처음 들어오면, 브라우저 언어가 6개 언어 중 하나일 때 그 언어판으로 자동 이동. 한국어 브라우저이거나 같은 사이트 안에서 고른 경우에는 이동하지 않습니다(브라우저 저장소는 쓰지 않음).
- 각 파일 `<head>`에 `hreflang` 대체 링크 7개.

## 번역판에서 바뀐 것
- 본문·버튼·캔버스 글자·퀴즈·용어 말풍선·대사 전부.
- 지식 색인: 노드 이름·정의가 그 언어로(`kg-raw`에 `label.{언어}`·`definition.{언어}` 추가), 검색도 그 언어로. 영어판은 영어 보조 이름을 숨김. `kg-ld`(JSON-LD)는 원본 그대로.
- `page-meta`: `title`·`series`·`suggestedCitation`·`todo`를 번역하고 원문은 `title_ko` 등으로 보존, `language`·`translationOf` 추가.
- 글꼴: en·ru·uz·vi는 IBM Plex Sans(키릴·베트남어 글리프), zh는 Noto Sans SC, ja는 Noto Sans JP. 중·일은 `word-break:normal`, 일본어 제목은 `auto-phrase`.
- 바꾸지 않은 것: 논문 수치, 수식, 모델·데이터셋 이름, 논문 영어 예문, 참고문헌(CSL·BibTeX·RIS), 꾸러미 파일 구조.

## 검사 결과 (2026-11-01)
| 항목 | 결과 |
|---|---|
| roundtrip (번역 없이 다시 끼우기) | 원본과 글자 단위 일치 |
| check (6개 언어 × 774단위) | 첫 회 각 770/774 통과. 실패 4건은 모두 원본에 남아 있던 쓰지 않는 태그 탓이라 원본을 고치고 기존 번역에서 태그만 빼서 재사용 (재번역 호출 0) |
| merge | 번역 없음 0, 스크립트 구문 오류 0, JSON 블록 파싱 통과 |
| 헤드리스 7개 언어 × 390·1280 | 콘솔 오류 0, 가로 넘침 0, 번역판 화면 한글 0, 퀴즈 10문항, 대결 판정·지식 색인 검색 동작 |
| 언어 전환 | ko → ja 선택 시 `#r3` 유지, vi 브라우저로 ko 접속 시 vi판으로 `#lab` 유지 |

**원어민 검수 전입니다.** 특히 uz·ru·vi는 검수를 권합니다(문법 일치, ʻ ʼ 표기, 성조).

## 비용 기록
`i18n/work/cost.csv`. 묶음 6개(언어당 1개, 각 774단위·2만 6천 자), 재시도 0.
하위 에이전트 합계 약 103만 토큰, 원문 글자당 약 6.5토큰(고정비 포함).
- 묶음 파일이 커서 에이전트가 파일을 나눠 읽어 호출이 5~12회가 됐습니다(목표 4회). 다음 판은 묶음을 1만 5천 자로 줄이거나 hints를 빼면 읽기 1회로 끝납니다.
- hints에 스크립트 코드 문맥이 섞여 들어가 입력이 늘었습니다. 다음 판은 스크립트 단위의 hint를 문장 문맥만 남기도록 줄일 것.

## 다시 만들기 (원본을 고친 뒤)
```
python3 i18n/tool.py extract && python3 i18n/tool.py roundtrip
python3 i18n/tool.py pending <L>        # 번역 메모리에 없는 단위만 묶음으로
# 번역 AI: rules/common.md + rules/lang/<L>.md + 묶음 → <L>_00n.out.json
python3 i18n/tool.py check <L> i18n/work/<L>_00n.out.json <L>_00n.json
python3 i18n/tool.py merge <L>          # → dist/01_transformer.<L>.html
node i18n/browser_check.js              # 7개 언어 × 2개 폭 검사
```
번역 메모리(`i18n/work/<L>/tm.json`)는 한국어 문장을 열쇠로 하므로, 원본에서 바뀐 문장만 다시 번역합니다.

## 그림 (2026-11-01 반영)
- 페이지 안(단일 파일, base64): 표지 `cover_01`(1600 WebP), 히어로 배경 `bg_01`, 생각 컷 `cut_01_think`, 아웃트로 `sc_01_outro`. 7개 언어판 모두 같은 그림, 대체 글만 그 언어로.
- `assets/img/`: 위 그림의 WebP와 `cover_01_960.webp`, 목차 카드용 `thumb_01.webp`(400×267), 공유 미리보기용 `og_01.webp`(1200×630). GitHub Pages에 올린 뒤 공개 주소가 정해지면 `<meta property="og:image" content="https://…/assets/img/og_01.webp">`를 각 페이지 `<head>`에 넣으세요(절대 주소여야 함).

## 목차 index.html (2026-11-02)
- 저장소 맨 위에 두면 GitHub Pages 주소로 처음 열리는 화면이 됩니다.
- 한 파일 안에서 7개 언어로 바뀝니다. 우선순위는 `?lang=` → 브라우저 언어 → 한국어입니다. 편 카드의 "읽기"와 언어 칩은 그 언어판으로 이어집니다.
- 각 편 상단 메뉴의 로고를 누르면 같은 언어의 목차로 돌아옵니다.
- 새 편을 더할 때는 `build_index.py`의 `eps` 목록에 한 줄을 추가합니다. 그 편의 제목·설명 번역은 번역 메모리에서 가져옵니다.
- 목차 표지 그림(`cover_index`)은 아직 없습니다. 지금은 벌집 무늬와 캐릭터 넷으로 대신합니다.
