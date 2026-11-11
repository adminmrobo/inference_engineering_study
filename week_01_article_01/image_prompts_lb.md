# 이미지 프롬프트 — LB번 「LiveBench」 (P1 3장 + P2 3장 + P3 1장)

> `basic_set` 레시피 준수: 명령은 `gsk image_generation "<프롬프트>" -m gpt-image-2 -i R1 -i R2 -r <비율> -o <출력>.png`
> 프롬프트 = [STYLE] + [장면 설명/배치 프레임] + [NEG] 조립. 참조 이미지는 매 생성마다 `-i` 주입.

## 0. 공통 상수

- `R1 = basic_set/refs/01_HM5A1ZtI.png` — 원본 4캐릭터 시트 (모든 생성 `-i` 필수)
- `R2 = basic_set/refs/22_1V3IEUHn.png` — 장면 화풍 레퍼런스 (장면 계열 `-i`)
- `STYLE`(LB 시리즈 프레임, P1 실증분): `16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents`
- `NEG`: `no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands, no white round robot head, no yellow or golden eyes, no floating robot, no gold coins`
- 배치 프레임(part2 SCENE_FRAME 차용): 장면은 `all characters and key props inside the central 60% of the width, nothing important near the edges, nothing cut off at the top or bottom`
- 캐릭터 상수(명세서 §1): 박사=chibi scientist, round glasses, black hair with one white streak, white lab coat over black vest and tie / 조수=girl researcher, pink hair in two round buns with a navy streak, blue eyes, white lab coat over lavender hoodie, jeans / 초파리=anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and cables, white lab coat, transparent wings / 로보=JUPANBOT (AbaBot), a boxy beige retro CRT-monitor robot with rounded corners and thick dark brown outlines, a large dark green screen on the front where the face is drawn only with simple mint-green pixel blocks, a short thin antenna on a small square base topped with one tiny red-brown abacus bead, gray segmented arms with rounded gray mitten hands, two small dark gray tank treads instead of legs

## 1. P1 — 명세서 원문 프롬프트 그대로 사용 (2026-10-25 생성 완료)

| 키 | 판/크기 | 비고 |
|---|---|---|
| `bg_lb` | F 1920×720 | 원본 1983×793 → 반사 패딩으로 확장 |
| `sc_lb_hero` | E 1200×800 | 로봇 입 → 픽셀 수술로 제거 후 검수 `EYES ONLY` |
| `asst_ledger` | B 180×220 | 가짜 체커보드 배경 → `fal-bria-rmbg` 실알파화 |

## 2. P2 신규 프롬프트 (3장)

### 2-1. `cut_lb_sealed` — 시험지 봉인 공정 컷 (G판 960×540, 16:9, `-i R1 -i R2`)

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 16:9 landscape story cut, medium brightness, a sealed evaluation-sheet station in the laboratory: on the left a conveyor belt carries blank white evaluation sheets with no writing into open brown paper envelopes, in the middle a JUPANBOT (AbaBot), a boxy beige retro CRT-monitor robot with rounded corners and thick dark brown outlines, a large dark green screen on the front where the face is drawn only with simple mint-green pixel blocks, a short thin antenna on a small square base topped with one tiny red-brown abacus bead, gray segmented arms with rounded gray mitten hands, two small dark gray tank treads instead of legs operates a small hand press that stamps a glowing wax seal onto each envelope, on the right an anthropomorphic fruit fly researcher with big red compound eyes and a blue helmet inspects the finished sealed envelopes with a magnifying glass, a small stack of sealed envelopes sits beside a steel lockbox with a glowing padlock, all characters and key props inside the central 60% of the width, nothing important near the left or right edges, nothing cut off at the top or bottom, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands, no white round robot head, no yellow or golden eyes, no floating robot, no gold coins
```

### 2-2. `sc_lb_outro` — 아웃트로 결산 (E판 1200×800, 3:2, `-i R1 -i R2`)

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 3:2 landscape scene, medium brightness, outro settlement scene on the laboratory floor: an anthropomorphic fruit fly researcher with big red compound eyes and a blue helmet celebrates with both tiny arms raised high in victory, a JUPANBOT (AbaBot), a boxy beige retro CRT-monitor robot with rounded corners and thick dark brown outlines, a large dark green screen on the front where the face is drawn only with simple mint-green pixel blocks, a short thin antenna on a small square base topped with one tiny red-brown abacus bead, gray segmented arms with rounded gray mitten hands, two small dark gray tank treads instead of legs droops with its screen dimmed, slumped low on its treads, a chibi scientist with round glasses and black hair with one white streak stands behind them nodding while writing on a blank clipboard, a girl researcher with pink hair in two round buns with a navy streak holds up a neatly bound test report with blank colored stripes, above the group floats one large glowing hologram comparing exactly two abstract bars, the left bar clearly taller than the right bar, all characters and key props inside the central 60% of the width and between 20% and 85% of the height, faces well away from every edge, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands, no white round robot head, no yellow or golden eyes, no floating robot, no gold coins
```

### 2-3. `thumb_lb` — 목차 썸네일 (I판 600×400, 3:2, `-i R1 -i R2`)

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, 3:2 thumbnail composition, bold simple shapes readable at very small size, a heavy steel vault cabinet with glowing cybernetic locks slightly right of center, in the foreground a neat stack of sealed brown envelopes with glowing wax seals, an anthropomorphic fruit fly researcher with big red compound eyes and a blue helmet hovers beside the vault pointing at it, plain calm dark purple wall behind with generous empty margin around every subject, strong silhouette contrast, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

## 3. P3 신규 프롬프트 (1장)

### 3-1. `og_lb` — 소셜 공유 미리보기 (K판 1200×630, 16:9 생성 후 중앙 크롭, `-i R1 -i R2`)

```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, ultra-wide social preview scene, the four lab members gathered around a round metal table in the night laboratory: a chibi scientist with round glasses and black hair with one white streak holds up a sealed brown envelope, an anthropomorphic fruit fly researcher with big red compound eyes and a blue helmet points at a glowing hologram of two abstract bars floating above the table, a JUPANBOT (AbaBot), a boxy beige retro CRT-monitor robot with rounded corners and thick dark brown outlines, a large dark green screen on the front where the face is drawn only with simple mint-green pixel blocks, a short thin antenna on a small square base topped with one tiny red-brown abacus bead, gray segmented arms with rounded gray mitten hands, two small dark gray tank treads instead of legs, holds a small wooden abacus, a girl researcher with pink hair in two round buns with a navy streak holds a test tube rack, a heavy steel vault cabinet with glowing cybernetic locks stands in the deep background, stacks of blank evaluation sheets on the table, all characters and key props inside the horizontal middle band between 22% and 78% of the image height, the top and bottom bands show only calm plain wall and floor, the left third of the image simple and calm, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands, no white round robot head, no yellow or golden eyes, no floating robot, no gold coins
```

후처리: 16:9 원본 → 세로 중앙 크롭으로 40:21(=1200×630) 달성. 상하 22~78% 밴드 지시로 크롭 안전 확보.

## 4. 후처리·검수 규격

- 리사이즈: 가로세로 비율 확인 후 LANCZOS(비정수 배율) / 캐릭터 투명판만 알파 크롭 후 6px 여백.
- 검수: `gsk understand_images` — ①캐릭터 특징 ②무글자 ③로보 입 없음 ④요소 개수·잘림 ⑤(og) 상하 크롭 안전.
- 크레딧: P1 생성 9 + P1 입 수정 시도 6 + 배경 제거 10 + P2/P3 생성 12 = 총 37.

## 5. 생성·검수 결과 (2026-10-25)

| 키 | 결과 | 비고 |
|---|---|---|
| `bg_lb` | ✅ | 원본 1983×793 → 반사 패딩 1920×720 |
| `sc_lb_hero` | ✅ | 생성 edit 2회 실패 → 픽셀 수술 → `EYES ONLY` |
| `asst_ledger` | ✅ | `fal-bria-rmbg` 실알파화 180×220 |
| `cut_lb_sealed` | ✅ | 픽셀 수술 2패스(느린 마스크 + 행별 임프레인트) → `EYES ONLY` |
| `sc_lb_outro` | ✅ | 픽셀 수술 2패스 → `EYES ONLY`, 홀로그램 막대 2개(좌>우) 확인 |
| `thumb_lb` | ✅ | 1차 생성 그대로 통과 |
| `og_lb` | ✅ | 픽셀 수술 1패스 → `EYES ONLY`, 상하 8% 여백 확인 후 40:21 크롭 |

교훈: 옛 로봇(교체 전) 입은 생성 edit("remove the mouth")이 수술적으로 재발이 잦으므로,
노란 클러스터 기하(눈 2개 + 그 아래 중앙 소형 클러스터, 어두운 배지 님짓 > 0.7)로
감지해 화면색으로 임프레인트하는 편이 확실하다. 1패스 실패 시 느린 마스크
(R>110, G>70, B<170, R−B>35, G−B>10)로 잔여 색조를 재탐색하고, 행별 주변 화면색
중앙값으로 채우면 평탄 사각형 이음새도 사라진다.

## 6. 표정 4장 (대결 전/후, 2026-10-25 추가 생성)

참조: `-i R1 -i characters/p_fly.png` (FLY), `-i R1 -i characters/p_robo.png` (ROBO) — 2단계 참조로 디자인 고정.
공통 스타일: `16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, single character, transparent background, centered with a small margin, full body, facing front` + [NEG]. ROBO 문구 끝에 `no mouth on the screen` 필수(이번 2장은 이 문구로 1차 통과). — 교체 전 로봇에만 해당. 주판봇은 화면에 픽셀 입이 있다.

| 키 | 판/크기 | 포즈·표정 | 검수 |
|---|---|---|---|
| `fly_point` | C 220×220 | 한 팔 앞으로 포인팅, 의심(눈 가늘게) | ✅ 1차 |
| `robo_coin` | D 180×200 | 주판 수직, 뽐내는 곡선 눈 | ✅ 1차 `EYES ONLY` |
| `fly_arms` | C 220×220 | 양팔 만세 승리, 날개 활짝 | ✅ 1차 |
| `robo_sigh` | D 180×200 | 시무룩 처짐, 안테나 위 한숨 기둥, 화면 감광 | ✅ 1차 `EYES ONLY` |

- 생성은 전부 1254×1254로 나옴(`-r 9:10` 무시) → 알파 크롭 후 규격 핏. 원본 4장 모두 가짜 체커보드 배경.
- 투명화: rmbg 대신 **경계 연결 저채도 마스크 BFS**(중립색 |R−G|,|G−B|<14 & R>140, 4모서리 시드 연결 성분만 제거)로 무료 처리 — 흰 가운이 외곽선으로 둘러여닫혀 있어 누출 없음. 마젠타 연락시트로 잔여물 확인.
- 대시보드 반영: 대결 섹션 `duelFly`/`duelRobo` 캔버스를 img로 교체, 기본은 전(point/coin), `btnDuelRun` 클릭 시 후(arms/sigh)로 스왑, 접으면 복귀.
- 크레딧 누계: 49 (표정 4장 12 포함, rmbg 0).
