# 인퍼런스 스터디 북 · 05-A1 — 페이지드 어텐션 — KV 캐시를 서랍처럼 나눠 담는다

> 『Inference Engineering』 스터디 5주차 논문 해설 · 처음 오신 분을 위한 비전공자판 · 인턴 시아 · 인턴 모아와 방청석 X1 · X2 · X3 출연

- **바로 읽기:** https://adminmrobo.github.io/inference_engineering_study/week_05_article_01/
- **스터디 북 목차:** https://adminmrobo.github.io/inference_engineering_study/
- **자료:** Kwon et al. (2023) Efficient Memory Management for Large Language Model Serving with PagedAttention, SOSP 2023 (arXiv:2309.06180)
- **해설 페이지:** [`index.html`](index.html) (단일 HTML, 설치 없이 브라우저에서 열림)

> 여기 포스팅은 스터디 멤버의 발표자료가 아닌 ahnboat.xyz 주인장 안상선이 직접 정리한 자료입니다.

## 페이지 구성

표지 → 공장 5F 층 안내 → 히어로(처음 오신 분께 3줄 요약) → 등장인물(여섯 식구 + 앞자리 방청석 셋) → 개념정리 단계(단계마다: 박사의 상황 질문 · 왜 이 방법 · 조수가 대신 묻는 수식 · 실험 앞 대화 · 실험 · 풀이 · 업무에서는 · 인턴이 다시 말하기 · 방청석 질문 · 확인 퀴즈) → 대결 → 다시 읽기 → 한 장 요약 → 아웃트로 → 강의자용 부록 → 지식 색인 → 온톨로지 · 서지 꾸러미

## 정확성 표시

- 논문 수치는 원문 그대로이며 `원문` 칩을 붙였습니다.
- 계기판의 설명용 모형 · 예시값은 캔버스에 노란 도장을 찍고, 바닥글 "예시값 · 설명용 모형인 것"에 모았습니다.
- 본문에 코드가 없습니다. 원문의 코드 · 명령은 "몰라도 됩니다" 접기 상자에 한 줄씩 뜻과 함께 두었습니다.

## 파일

| 파일 | 내용 |
|---|---|
| `index.html` | 해설 페이지 |
| `thumb.jpg` | 목록 카드 썸네일 (1200×630) |
| `COVER_paged.md` | 글 표지 그림 지시문 (16비트 RPG 픽셀아트) |
| `IMG_paged.md` | 이미지 제작 명세서 |

다시 만들기: `tools/lab_build/pages/p_paged.py` (형식: ai-lab-explainer-plain v1.1 · 낮의 연구실)

글 · 안상선 ((주)M-Robo 대표) · 교재와 논문의 요약 · 해설이며 원문을 대신하지 않습니다. 캐릭터 설정 · 그림은 저작권자 허락 없이 사용할 수 없습니다.
