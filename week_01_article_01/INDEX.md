# INDEX — LiveBench 해설 대시보드 (AI Lab Explainer Series · LB-01)

> GitHub 저장소 루트에 그대로 올리는 파일 목록. 모든 HTML은 그림·데이터·스크립트를 한 파일에 담았다(base64). 브라우저로 열기만 하면 동작한다.

## 1. 페이지

| 파일 | 내용 | 크기 |
|---|---|---|
| `LiveBench_해설_대시보드.html` | LB-01 본문. 오염도 시뮬레이터 · 6개 영역 레이더 · LLM 판사 오류율 · 대결 시뮬레이션 · 퀴즈 2문항 · 학습 진도 추적 내장 | 약 823KB |
| `LiveBench_해설_대시보드.en.html` | English판 (같은 내용의 English 번역) | 약 827KB |
| `LiveBench_해설_대시보드.zh.html` | 中文판 (같은 내용의 中文 번역) | 약 827KB |
| `LiveBench_해설_대시보드.ja.html` | 日本語판 (같은 내용의 日本語 번역) | 약 827KB |
| `LiveBench_해설_대시보드.uz.html` | Oʻzbekcha판 (같은 내용의 Oʻzbekcha 번역) | 약 827KB |
| `LiveBench_해설_대시보드.ru.html` | Русский판 (같은 내용의 Русский 번역) | 약 827KB |
| `LiveBench_해설_대시보드.vi.html` | Tiếng Việt판 (같은 내용의 Tiếng Việt 번역) | 약 827KB |

- 기반 논문: Colin White, Samuel Dooley, Manley Roberts, Arka Pal et al., 「LiveBench: A Challenging, Contamination-Limited LLM Benchmark」, **ICLR 2025**.
- 등장인물: 박사(DOC) · 조수 세라(ASST) · 초파리 연구원(FLY) · 주판봇(ROBO).

## 2. 이미지 11장 (`images/`) — 본문에는 전부 base64로 내장

| # | 파일 | 키 | 판/크기 | 들어가는 곳 | 검수 |
|---|---|---|---|---|---|
| 1 | `bg_lb.png` | bg_lb | F 1920×720 | 히어로 배경 | ✅ 캐릭터·글자 없음 |
| 2 | `sc_lb_hero.png` | sc_lb_hero | E 1200×800 | 히어로 무대 4인 앙상블 | ✅ 4인 인식, 로보 입 수정 |
| 3 | `asst_ledger.png` | asst_ledger | B 180×220 투명 | 조수 결과 발표 말풍선 + 프로필 | ✅ 실알파 |
| 4 | `cut_lb_sealed.png` | cut_lb_sealed | G 960×540 | Section 2 시험지 봉인 컷 | ✅ 로보 입 수정 |
| 5 | `sc_lb_outro.png` | sc_lb_outro | E 1200×800 | 아웃트로 결산 | ✅ 막대 2개(좌>우) |
| 6 | `thumb_lb.png` | thumb_lb | I 600×400 | 목차 썸네일 · 파비콘 | ✅ 1차 통과 |
| 7 | `og_lb.png` | og_lb | K 1200×630 | 소셜 공유 미리보기(og:image) | ✅ 크롭 안전 |
| 8 | `fly_point.png` | fly_point | C 220×220 투명 | 대결 전 초파리(의심 포인팅) | ✅ 1차 통과 |
| 9 | `robo_coin.png` | robo_coin | D 180×200 투명 | 대결 전 로보(주판 확신) | ✅ `EYES ONLY` |
| 10 | `fly_arms.png` | fly_arms | C 220×220 투명 | 대결 후 초파리(승리 만세) | ✅ 1차 통과 |
| 11 | `robo_sigh.png` | robo_sigh | D 180×200 투명 | 대결 후 로보(패배 시무룩) | ✅ `EYES ONLY` |

- 스타일: 16-bit RPG 픽셀아트, 굵은 외곽선, 2~3단 명암. **그림 속 글자 일체 없음**(검수 완료).
- 화면 표시 글자는 전부 본문 HTML/캔버스가 담당한다.
- `og:image`만 외부 플랫폼 URL을 쓴다(HTML head에 기재).

## 3. 문서

| 파일 | 내용 |
|---|---|
| `README.md` | 저장소 소개 — 한국어 → English → 中文 → 日本語 → Oʻzbekcha → Русский → Tiếng Việt 순으로 조립 |
| `image_prompts_lb.md` | 이미지 11장의 생성 프롬프트 전문(상수·명령·검수 결과·옛 로봇(교체 전) 입 수술 레시피) |

## 4. GitHub 업로드 순서 (직접 업로드용)

1. 저장소 루트에 `LiveBench_해설_대시보드.html`, `README.md`, `INDEX.md`를 올린다(폴더 없이).
2. `images/` 11장과 `image_prompts_lb.md`는 원본 보존용으로 함께 올린다(본문 동작에는 불필요).
3. `og:image`의 플랫폼 URL은 업로드 후 저장소의 `images/og_lb.png` raw 주소로 바꿔도 된다.
4. README의 「바로 보기」 주소는 `<저장소>` 자리에 실제 저장소 이름을 넣어 `https://adminmrobo.github.io/<저장소>/` 형태로 확정한다.
