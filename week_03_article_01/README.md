# 추론 엔지니어링 스터디 3주차 · 논문 1 — 번개 어텐션 (FlashAttention)

![번개 어텐션 표지](assets/img/cover_03_960.webp)

> 계산을 줄이지 않고도, 어텐션을 몇 배 빠르게 만들 수 있을까?

박사 · 조수(하루) · 초파리 연구원 · 주판봇, 연구실 네 캐릭터가 진행하는 **FlashAttention 논문 인터랙티브 해설**입니다. 설치할 것 없이 브라우저에서 바로 엽니다.

- **바로 읽기:** https://adminmrobo.github.io/inference_engineering_study_week_03_article_01/
- **해설 페이지:** [`03_flash_attention.html`](03_flash_attention.html)
- **원문:** Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)

## 무엇을 배우나

| 절 | 내용 | 직접 해 보기 |
|---|---|---|
| 1 질문 | 근사 어텐션은 왜 실제로 빨라지지 않았나 — 메모리 계층(SRAM 19TB/s vs HBM 1.5TB/s) | — |
| 2 방법 | 블록 나누기 → K·V 올리기 → Q 돌며 계산 → 노트로 합치기 → 역방향 다시 계산 | 단계 버튼 |
| 결과 ① | 창고 왕복 Θ(Nd+N²) → Θ(N²d²/M), 그림 2: 40.3 → 4.4 GB, 41.7 → 7.3 ms | 왕복 계산기 · 쟁반 나르기 |
| 결과 ② | 온라인 소프트맥스(m, ℓ)로 쪼개도 답이 똑같다 — 정확한 어텐션 | 블록 소프트맥스 실험 |
| 결과 ③ | BERT·GPT-2 학습 속도, 긴 문맥(Path-X 61.4), 표 20·21 벤치마크 | 길이별 시간·메모리 그래프 |
| 모형 실험실 | 몰아 하기 → 쟁반 나누기 → 다시 계산을 하나씩 켜기 | 블록 크기 슬라이더 |
| 대결 | FLOP가 적은 쪽이 더 빠를까? (판정: 원문 실측값) | 예측 → 결과 보기 |

페이지 끝에는 **지식 색인**(검색·미니 그래프)과 **온톨로지·서지 꾸러미**(JSON-LD · Turtle · CSV · CSL-JSON · BibTeX · RIS를 ZIP 하나로)가 있습니다.

## 정확성 표시

- 논문 수치는 원문 그대로 옮겼습니다(반올림하지 않음). 화면에 `원문` 칩으로 표시합니다.
- 시뮬레이션·계산기 상수·예시 점수는 설명용 모형이며, 캔버스에 노란 도장을 찍었습니다.
- 이 해설은 2022년 arXiv v2와 A100 등 당시 GPU 기준입니다. 이후 개정판·후속 연구는 다루지 않습니다.

## 저장소 구조

```
index.html                  3주차 목차 (GitHub Pages 첫 화면)
03_flash_attention.html     논문 1 해설 페이지 (단일 HTML, 외부 라이브러리 없음)
assets/img/                 표지·장면·컷·배경 (WebP), og 이미지
assets/img/src/             그림 원본 PNG
docs/kg_03.json             지식 그래프 (노드 61 · 관계 79)
docs/KG_00_registry_add_03.json  시리즈 등록부 추가분
docs/IMG_03_flash_attention.md   이미지 제작 명세서 · 매니페스트
docs/COVER_03_flash_attention.md 글 표지 생성 지시문
```

## GitHub Pages로 열기

Settings → Pages → Source를 **Deploy from a branch**, Branch를 **main / (root)** 로 두면 위 주소로 공개됩니다. 로컬에서는 `index.html`을 더블클릭해도 됩니다.

## 이 페이지 인용하기

> 안상선 (2026). 번개 어텐션 — 창고를 덜 오가면 빨라진다 (FlashAttention 논문 해설). 추론 엔지니어링 스터디 3주차 논문 1, v1.0.

## 저작권

- 글 · 안상선 ((주)M-Robo 대표) — [소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)
- 캐릭터 박사 · 조수 · 초파리 연구원 · 주판봇 © 안상선
- 논문 내용·그림·표의 저작권은 원저자에게 있으며, 이 저장소는 학습용 해설입니다.
