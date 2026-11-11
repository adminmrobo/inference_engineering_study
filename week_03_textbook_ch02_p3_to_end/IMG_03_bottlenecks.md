# 03번 「병목을 찾아라」 이미지 제작 명세서

| 항목 | 내용 |
|---|---|
| 페이지 | 03_bottlenecks.html (인퍼런스러닝 3주차, 『Inference Engineering』 2.3–2.5) |
| 모드 / 주 앵커 | 교과서 / D 생활·현장: 연구실 안 주방(창고 → 재료 통로 → 조리대) |
| 시즌 | 기본 |
| 대결 | 이미지 디노이저 행렬곱에 연산 ×2 vs 대역폭 ×2 → 결과 **R (주판봇 승)**, 속도 향상 1.00배 vs 2.00배, 차이 100%p |
| 새로 그릴 그림 | P1 1장 (cover_03) · P2 2장 · P3 2장 |
| 재사용 | 캐릭터 표정 23키 (기본 팩 @ 5269662, 96px, 페이지에 base64로 넣음) |
| 그림이 없을 때 | 페이지는 CSS 대체 표지와 캐릭터 팩 그림으로 이미 완성 상태 |

## 1. 그림체와 고정 외형
- 스타일: 캐릭터 팩 18-3 (16비트 RPG 픽셀아트, 굵은 외곽선, 2–3단계 명암)
- 고정 외형: 캐릭터 팩 18-4 그대로. 키 순서 박사 ≥ 조수 > 주판봇 > 초파리
- 장소: 밤의 연구실과 이어진 작은 주방. 창고 선반(HBM), 좁은 재료 통로(메모리 대역폭), 조리대(연산)
- 장소 영어 묘사: *a small kitchen built into the same night lab world, storage shelves on the left, a narrow glowing conveyor corridor in the middle, a cooking counter on the right, purple lab light spilling in from one side*
- 생물 앵커가 아니므로 현미경·초파리 해부 소품 없음

## 2. 필요한 그림 전체

| # | 키 | 판 | 크기 | 상태 | 우선 | 들어가는 곳 | 대신 쓰는 그림 |
|---|---|---|---|---|---|---|---|
| 0 | cover_03 | L | 1920×1080 | 새로 (COVER_03_bottlenecks.md) | P1 | 맨 위 글 표지 | CSS 대체 표지 + 캐릭터 넷 |
| 1 | bg_03 | F | 1920×720 | 새로 (표지 자르기 가능) | P3 | (히어로 배경, 지금은 벌집 무늬) | 표지 자르기 |
| 2 | cut_03_lv6 | G | 960×540 | 새로 | P2 | ⑥ 루프라인 칸 컷 (요리사가 바구니를 기다림) | 없음 (캔버스 주방 애니메이션이 대신) |
| 3 | sc_03_outro | E | 1200×800 | 새로 | P2 | 아웃트로 (주판봇 앞, 초파리 인정) | 말풍선 4개 |
| 4 | thumb_03 | I | 600×400 | 새로 (표지 3:2 자르기) | P3 | 목차 카드 | 색 카드 |
| 5 | og_03 | K | 1200×630 | 표지 자르기 | P3 | 공유 미리보기 | 없음 |
| — | 표정 23키 | A–D | 96 | 재사용 | — | 히어로·말풍선·대결·등장인물 | 기본 표정 |
| — | 행동으로 보기 (디노이징, 궤적, 주방, 바이트 막대, KV 칸) | — | — | 코드 | — | 캔버스 | — |

재사용 표정: doc_front·think·judge·magic, asst_smile·report·spark·proud, fly_clip·point·cry·coffee·magnify·type, robo_smile·coin·happy·calc (대결 뒤: fly_cry, robo_happy, asst_spark, doc_judge — 5-8 표, 차이 10%p 이상 규칙).

## 3. 새로 그릴 그림 상세

### 3-1. `cut_03_lv6` — 재료를 기다리는 요리사
| 항목 | 내용 |
|---|---|
| 판 · 크기 | G · 960×540 |
| 구도 | 왼쪽 창고 선반, 가운데 듬성듬성 바구니가 오는 통로, 오른쪽 조리대에서 주판봇이 칼을 내려놓고 기다림. 초파리가 통로 옆에서 바구니 간격을 잰다 |
| 피할 것 | 글자·숫자, 결과 암시(이 컷은 디코드 장면이라 승패와 무관) |
| 대체 글 | 재료 바구니가 띄엄띄엄 들어와 주판봇 요리사가 기다리고 초파리 연구원이 간격을 재는 장면 |
| 대신 쓰는 그림 | 없음 |

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 16:9 illustration panel, a small kitchen built into the same night lab world, storage shelves on the left, a long narrow glowing conveyor corridor in the middle with only a few amber ingredient baskets spaced far apart, a cooking counter on the right; boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, standing at the counter with the knife put down, waiting and tapping the counter; anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, beside the corridor facing right, measuring the gap between baskets with a small ruler, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-2. `sc_03_outro` — 그림 주방은 손이 병목
| 항목 | 내용 |
|---|---|
| 판 · 크기 | E · 1200×800 |
| 구도 | 앞쪽 오른쪽에 주판봇이 주판을 머리 위로(이김), 왼쪽 조금 뒤 초파리가 커피잔을 들고 고개를 끄덕임(인정, 조롱 없음). 박사는 가운데 뒤에서 벽의 꺾인 선 그래프 수평선 부분을 가리킴, 조수는 옆에서 뿌듯한 미소 |
| 대체 글 | 주판봇이 주판을 들어 기뻐하고 초파리 연구원이 커피를 들고 인정하는 밤의 연구실 주방 |
| 대신 쓰는 그림 | 아웃트로 말풍선 |

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 3:2 landscape scene, medium brightness, a small kitchen built into the same night lab world with a busy cooking counter and a wall chart of a cyan diagonal line bending into a flat line; boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, front right raising a wooden abacus over its head happily; anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, slightly behind on the left facing right, holding a coffee cup and nodding with a calm smile; chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, back center pointing at the flat part of the wall line; girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, at the side with a proud smile, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-3. `bg_03`, `thumb_03`, `og_03`
표지(cover_03)를 받으면 잘라서 만듭니다: bg_03 = 8:3 가운데 띠, thumb_03 = 3:2, og_03 = 1200×630. 따로 그리지 않아도 됩니다.

## 4. 일관성 지침
- 참고 이미지: fruitfly-lab-expressions @ 5269662의 doctor/E08, haru/E13, fruitfly/E08, jupanbot/E16
- 같은 대화에서 표지 → 컷 → 아웃트로 순서로 만들면 그림체가 맞습니다
- 표정만 바꿀 때: *same character, same size and position, only change the facial expression and pose to ...*
- 박사·조수는 좌우로 뒤집지 않습니다 (브릿지 위치)

## 5. 넘겨받은 뒤 처리
1. 비율·글자·네 캐릭터 외형 확인 2. WebP로 변환(표지 1600 220 KB 이하) 3. 390·768·1280 폭에서 얼굴 잘림 확인 4. `data-img` 자리에 넣고 그림 합계 600 KB 이하 확인

### 이 저장소에 넣는 곳

| 키 | 저장소 경로 | 페이지 반영 |
|---|---|---|
| cover_03 | `images/cover_03.webp` | 올리기만 하면 자동 (그림이 있으면 CSS 대체 표지 대신 그림 표지를 씀) |
| og_03 | `images/og_03.webp` (1200×630) | 자동 (`og:image` 메타 태그가 이미 이 경로를 가리킴) |
| thumb_03 | `images/thumb_03.webp` (600×400) | 목차·현황 사이트용, 페이지에는 쓰지 않음 |
| bg_03 | `images/bg_03.webp` (1920×720) | 자동 (제목 영역 배경, 어둡게 덮어 글자를 살림) |
| cut_03_lv6 | `images/cut_03_lv6.webp` (960×540) | 자동 (⑥ 루프라인 칸, 실험 패널 바로 위) |
| sc_03_outro | `images/sc_03_outro.webp` (1200×800) | 자동 (아웃트로 제목 아래) |

모든 자리는 파일이 있을 때만 보이고, 없으면 조용히 숨습니다. 파일 이름은 소문자 키 그대로 씁니다.

**반영 현황 (2026-11-07):** 여섯 장 모두 받아 `images/`에 넣고 페이지에 연결함.

## 6. 체크리스트
- [x] HTML의 `data-img` 키(cover_03, 표정 키)가 명세서에 있음
- [x] 결과 전 그림(cover_03)에 승패 암시 없음
- [x] 모든 프롬프트에 고정 외형·금지 구절
- [x] 장소가 D 앵커와 일치, 현미경·해부 소품 없음
- [x] P1 1장 (표지 제외 0장)
- [x] 받은 그림 6장 반영: cover_03 · og_03 · thumb_03 · bg_03 · cut_03_lv6 · sc_03_outro

## 7. 매니페스트
```json
{
  "page": "03_bottlenecks",
  "anchor": "D:lab-kitchen-corridor",
  "season": "default",
  "duel": {"result": "R", "gap": 1.00},
  "images": [
    {"key":"cover_03","plate":"L","size":[1920,1080],"status":"new","priority":"P1","slot":"cover","fallback":"css-pixel-four","alt":"재료 바구니가 좁은 통로에 밀려 있는 밤의 연구실 주방에서 네 캐릭터가 벽의 꺾인 선 그래프를 바라보는 표지"},
    {"key":"cut_03_lv6","plate":"G","size":[960,540],"status":"new","priority":"P2","slot":"lv6-cut","fallback":"none","alt":"재료 바구니가 띄엄띄엄 들어와 주판봇 요리사가 기다리고 초파리 연구원이 간격을 재는 장면"},
    {"key":"sc_03_outro","plate":"E","size":[1200,800],"status":"new","priority":"P2","slot":"outro","fallback":"say-bubbles","alt":"주판봇이 주판을 들어 기뻐하고 초파리 연구원이 커피를 들고 인정하는 밤의 연구실 주방"},
    {"key":"bg_03","plate":"F","size":[1920,720],"status":"crop-of-cover","priority":"P3","slot":"hero-bg","fallback":"honeycomb"},
    {"key":"thumb_03","plate":"I","size":[600,400],"status":"crop-of-cover","priority":"P3","slot":"index-card","fallback":"color-card"},
    {"key":"og_03","plate":"K","size":[1200,630],"status":"crop-of-cover","priority":"P3","slot":"og","fallback":"none"}
  ]
}
```
