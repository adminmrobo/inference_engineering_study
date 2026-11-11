# 03번 「번개 어텐션 — 창고를 덜 오가면 빨라진다」 이미지 제작 명세서

| 항목 | 내용 |
|---|---|
| 페이지 | 03_flash_attention.html |
| 모드 / 주 앵커 | 논문 / B 연구실 (실험대 = SRAM, 시약 창고 = HBM) |
| 시즌 | 기본 |
| 대결 | FLOP가 적은 쪽이 더 빠를까? → 결과 **F** (초파리 승), 실행 시간 7.3 vs 41.7 ms (차이 82%) |
| 새로 그릴 그림 | P1 2장 (cover_03, sc_03_hero) · P2 3장 · P3 2장 |
| 재사용 | 표정 17장 (기본 캐릭터 팩 96px, 페이지에 base64로 들어 있음) |
| 그림이 없을 때 | 페이지는 캐릭터 팩 표정 + CSS 대체 표지 + SVG 히어로 소품으로 이미 완성 상태 |

## 1. 그림체와 고정 외형
- 스타일: SKILL 18-3 (16비트 RPG 픽셀아트, 굵은 외곽선, 2~3단계 명암)
- 고정 외형: 캐릭터 팩 18-4 그대로
- 장소: 밤의 연구실 — 앞쪽 작은 실험대, 안쪽 복도 끝 큰 시약 창고
- 장소 영어 묘사: *a night laboratory with a small tidy lab bench in the foreground and, at the far end of a corridor, a huge storage room with tall shelves of identical crates*

## 2. 필요한 그림 전체

| # | 키 | 판 | 크기 | 상태 | 우선 | 들어가는 곳 | 대신 쓰는 그림 |
|---|---|---|---|---|---|---|---|
| 0 | cover_03 | L | 1920×1080 | 새로 (COVER_03_flash_attention.md) | P1 | 맨 위 글 표지 | CSS 대체 표지 + 표정 넷 |
| 1 | sc_03_hero | E | 1200×800 | 새로 | P1 | 히어로 무대 (지금은 SVG 선반 소품) | SVG 소품 |
| 2 | bg_03 | F | 1920×720 | 새로 | P3 (표지 있음) | 히어로 배경 | 표지 자르기 |
| 3 | doc_think / doc_front / doc_judge / doc_magic | A | 96 | 재사용 (doc_e09/e08/e10/e16) | — | 히어로·등장인물·판정·아웃트로 | — |
| 4 | asst_smile / asst_firm / asst_report / asst_spark | B | 96 | 재사용 (asst_e13/e12/e07/e01) | — | 히어로·대결 발표·아웃트로 | — |
| 5 | fly_point / fly_clip / fly_magnify / fly_arms | C | 96 | 재사용 (fly_e08/e10/e07/e16), 좌우 뒤집어 씀 | — | 대결 전·본문·대결 후(승) | — |
| 6 | robo_coin / robo_smile / robo_calc / robo_sigh / robo_happy | D | 96 | 재사용 (robo_e16/e13/e09/e20/e12) | — | 대결 전·결과 ③·대결 후(패) | — |
| 7 | cut_03_tray | G | 960×540 | 새로 | P2 | 결과 ① 컷: 조수가 쟁반 나르기 | 캔버스 애니메이션 |
| 8 | sc_03_outro | E | 1200×800 | 새로 | P2 | 아웃트로 장면 | 표정 넷 나란히 |
| 9 | thumb_03 | I | 600×400 | 새로 (cover_03 3:2 자르기) | P2 | 목차 카드 | 색 카드 |
| 10 | og_03 | K | 1200×630 | 새로 (cover_03 자르기) | P3 | 공유 미리보기 | 없음 |
| — | 행동으로 보기 (쟁반 나르기, 노트, 메모리 저울) | — | — | 코드 | — | 캔버스 | — |

## 3. 새로 그릴 그림 상세

### 3-1. `cover_03` — 쟁반 나르기 표지
→ `COVER_03_flash_attention.md` 참조.

### 3-2. `sc_03_hero` — 실험대와 창고
| 항목 | 내용 |
|---|---|
| 판 · 크기 | E · 1200×800 |
| 구도 | 왼쪽 앞 실험대(작게 빛남), 오른쪽 뒤 복도 끝 큰 창고 선반. 초파리(왼쪽, 오른쪽 봄)와 주판봇(오른쪽, 왼쪽 봄)이 복도를 사이에 두고 마주 봄, 박사 가운데 뒤, 조수 실험대 옆 |
| 표정·몸짓 | 박사 턱에 손, 조수 미소, 초파리 한쪽 눈 가늘게 가리킴, 주판봇 주판알 들어 보임 |
| 소품 | 실험대 위 3×3 타일 판(한 칸만 초록), 바닥에 창고→실험대 점선 빛 |
| 피할 것 | 승패 암시, 글자, 숫자 |
| 대체 글 | 실험대와 복도 끝 창고 사이에서 네 캐릭터가 마주 선 밤의 연구실 |

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 3:2 landscape scene, medium brightness, a night laboratory with a small tidy lab bench on the left foreground and, at the far end of a corridor on the right, a huge storage room with tall shelves of identical crates, a dashed glowing path on the floor between them, chibi scientist with thin teal rectangular glasses, spiky black hair with one white streak and a small ponytail, white lab coat over black vest and tie, standing at the back center with a hand on his chin, girl researcher with long pink hair in two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, smiling beside the bench, anthropomorphic fruit fly researcher with big red compound eyes and a blue helmet with a gold stripe and pink and blue cables, white lab coat over black vest, black gloves, on the left facing right pointing with one eye narrowed, boxy beige retro CRT-monitor robot with a dark green screen face and mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, on the right facing left holding up a shining abacus bead, on the bench a 3x3 grid of square tiles with one tile glowing green, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-3. `cut_03_tray` — 쟁반 하나씩
| 항목 | 내용 |
|---|---|
| 판 · 크기 | G · 960×540 |
| 구도 | 조수가 작은 타일 쟁반을 들고 창고에서 실험대로 걷는 옆모습. 창고 쪽에는 같은 쟁반이 줄지어 대기 |
| 대체 글 | 조수가 창고에서 작은 블록 쟁반을 하나씩 실험대로 나르는 장면 |

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 16:9 illustration panel, girl researcher with long pink hair in two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, walking from a tall storage shelf on the left toward a small glowing lab bench on the right, carrying a small square tray of glowing green tiles, more identical trays waiting in a neat row on the shelf, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-4. `sc_03_outro` — 초파리 승 (결과 후)
| 항목 | 내용 |
|---|---|
| 판 · 크기 | E · 1200×800 |
| 구도 | 초파리가 앞·약간 크게 팔짱, 주판봇은 같은 화면에서 주판을 내려놓고 머리를 긁으며 인정, 박사는 양손 보랏빛 불꽃, 조수는 반짝이며 웃음. 실험대의 타일 판은 전부 초록 |
| 피할 것 | 조롱하는 몸짓, 글자 |
| 대체 글 | 타일이 모두 켜진 실험대 앞에서 초파리 연구원이 팔짱을 끼고 주판봇이 웃으며 인정하는 아웃트로 장면 |

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 3:2 landscape scene, medium brightness, in front of a lab bench whose grid of tiles is now fully glowing green, anthropomorphic fruit fly researcher with big red compound eyes and a blue helmet with a gold stripe and pink and blue cables, white lab coat over black vest, black gloves, in front and slightly larger with arms crossed and a confident look, boxy beige retro CRT-monitor robot with a dark green screen face and mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, setting down a wooden abacus and scratching its head with a good-natured smile, chibi scientist with thin teal rectangular glasses and black hair with one white streak in a white lab coat holding purple sparks in both hands, girl researcher with long pink hair in two round buns smiling with sparkles, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-5. `bg_03` (P3)
```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, wide 8:3 background, left side simple and calm for title text, details on the right, a long night lab corridor ending in a huge storage room of tall shelves on the right, a small glowing bench near the middle, no characters, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

## 4. 일관성 지침
- 참고 이미지: fruitfly-lab-expressions 기본 그림 4장 + 주판봇 v2 gpt2 단체 사진
- 같은 캐릭터는 같은 세션에서 연달아. 표정만 바꿀 때: *same character, same size and position, only change the facial expression and pose to ...*
- 투명 배경이 안 되면 *solid flat #00ff00 background*

## 5. 넘겨받은 뒤 처리
`build_character_pack.py --ingest ./받은그림 --plates cover_03=L,sc_03_hero=E,cut_03_tray=G,sc_03_outro=E --out received_03` → `data-img` 자리 채우기 → 그림 합계 표지 포함 600 KB 이하 확인 (현재 페이지 317 KB, 표정 base64 약 120 KB 포함).

## 6. 체크리스트 (18-13)
- [x] HTML의 `data-img` 키(cover_03, bg_03, fly_point, robo_coin, sc_03_outro)가 명세서에 있음
- [x] 대결 결과 후 표정: F → fly_arms, robo_sigh, doc_judge, asst_firm→발표
- [x] 결과 전 그림(표지·히어로)에 승패 암시 없음
- [x] 생물 앵커가 아니므로 현미경·해부 소품 없음
- [x] 모든 프롬프트에 고정 외형과 금지 구절
- [x] P1 2장 (6장 이하)

## 7. 매니페스트
```json
{
  "page": "03_flash_attention",
  "anchor": "B:lab-bench-storage",
  "season": "default",
  "duel": {"result": "F", "gap": 0.82},
  "images": [
    {"key":"cover_03","received":"2026-11-07","plate":"L","size":[1920,1080],"status":"done","priority":"P1","slot":"cover","files":["assets/img/cover_03.webp (1600x900)","assets/img/cover_03_960.webp"],"alt":"밤의 연구실에서 조수가 창고의 블록 쟁반을 실험대로 옮기고, 초파리 연구원과 주판봇이 실험대 타일 판을 바라보며 박사가 뒤에서 지켜보는 표지"},
    {"key":"sc_03_hero","received":"2026-11-07","plate":"E","size":[1200,800],"status":"done","priority":"P1","slot":"hero-stage","fallback":"svg-props","alt":"실험대와 복도 끝 창고 사이에서 네 캐릭터가 마주 선 밤의 연구실"},
    {"key":"bg_03","received":"2026-11-07","plate":"F","size":[1920,720],"status":"done","priority":"P3","slot":"hero-bg","fallback":"cover_03","alt":"밤의 연구실 복도 끝 큰 창고"},
    {"key":"cut_03_tray","received":"2026-11-07","plate":"G","size":[960,540],"status":"done","priority":"P2","slot":"r1-cut","fallback":"canvas","alt":"조수가 창고에서 작은 블록 쟁반을 하나씩 실험대로 나르는 장면"},
    {"key":"sc_03_outro","received":"2026-11-07","plate":"E","size":[1200,800],"status":"done","priority":"P2","slot":"outro","fallback":"expressions-row","alt":"타일이 모두 켜진 실험대 앞에서 초파리 연구원이 팔짱을 끼고 주판봇이 웃으며 인정하는 아웃트로 장면"},
    {"key":"thumb_03","plate":"I","size":[600,400],"status":"done","received":"2026-11-07","priority":"P2","slot":"index-card","fallback":"color-card","alt":"번개 어텐션 표지 축소판"},
    {"key":"og_03","plate":"K","size":[1200,630],"status":"done","received":"2026-11-07","priority":"P3","slot":"og","fallback":null,"alt":"번개 어텐션 공유 미리보기"},
    {"key":"fly_point","plate":"C","size":[96,96],"status":"reuse","slot":"duel-before","alt":""},
    {"key":"robo_coin","plate":"D","size":[96,96],"status":"reuse","slot":"duel-before","alt":""},
    {"key":"fly_arms","plate":"C","size":[96,96],"status":"reuse","slot":"duel-after","alt":""},
    {"key":"robo_sigh","plate":"D","size":[96,96],"status":"reuse","slot":"duel-after","alt":""}
  ]
}
```

## 8. 반영 기록 (2026-11-07)
| 키 | 받은 크기 | 넣은 크기 | 자리 |
|---|---|---|---|
| sc_03_hero | 1200×800 | 1200×675 WebP 90 KB | 글 표지 자리 (cover_03 받기 전 임시) |
| bg_03 | 1920×720 | 1280×480 WebP 26 KB | 히어로 배경 |
| cut_03_tray | 960×540 | 640×360 WebP 29 KB | 결과 ① 짝 카드 아래 |
| sc_03_outro | 1200×800 | 760×507 WebP 71 KB | 아웃트로 장면 |

- 점검: 390·768·1280 폭 가로 넘침 0, 깨진 그림 0, 스크립트 오류 0. 페이지 604 KB (그림 base64 합계 약 400 KB, 표지 포함 600 KB 기준 안).
- 메모: sc_03_outro는 초파리가 앞·크게가 아니라 오른쪽 뒤에 섰다(18-8과 다름). 팔짱·주판 내려놓기는 결과 F와 맞아 그대로 씀. cut_03_tray의 초파리 환호 몸짓은 대결 전 자리라 승패 암시로 읽힐 수 있음 — 다시 그릴 때 fly_clip 자세 권장.

## 9. 저장소 반영 (2026-11-07, 2차)
| 키 | 받은 크기 | 저장소 파일 | 자리 |
|---|---|---|---|
| cover_03 | 1600×900 (원본 PNG 1360×768) | assets/img/cover_03.webp 119 KB, cover_03_960.webp 57 KB | 글 표지 (목차 index.html 표지 겸용) |
| sc_03_hero | 1200×800 | assets/img/sc_03_hero.webp 760×507, 51 KB | 1절 질문 — 실험대와 창고 컷 (임시 표지 자리에서 옮김) |
| bg_03 | 1920×720 | assets/img/bg_03.webp 1280×480, 25 KB | 히어로 배경 |
| cut_03_tray | 960×540 (다시 그림: 초파리 클립보드 자세) | assets/img/cut_03_tray.webp 640×360, 27 KB | 결과 ① |
| sc_03_outro | 1200×800 | assets/img/sc_03_outro.webp 760×507, 70 KB | 아웃트로 |
| thumb_03 | 600×400 | assets/img/thumb_03.webp | 목차 카드 |
| og_03 | 1200×630 | assets/img/og_03.jpg | og:image |

- 저장소판은 그림을 base64로 넣지 않고 `assets/img/` 경로로 읽는다(HTML 319 KB). 원본 PNG는 `assets/img/src/`.
- cut_03_tray 다시 그림으로 "대결 전 승패 암시" 메모는 해결.
