# 표지 지시문 — 03 번개 어텐션 (FlashAttention)

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_03 · L (16:9, 가로 1920 이상) |
| 장소 (앵커) | B 연구실 — 밤의 연구실. 왼쪽 앞에 작은 실험대, 오른쪽 안쪽 복도 끝에 큰 시약 창고 선반 |
| 주제 은유 | 큰 창고에서 실험대로 작은 블록 쟁반이 하나씩 옮겨지고, 쟁반 위 칸들이 차례로 초록빛으로 켜진다. 실험대 위 펼친 노트에는 글자 없이 두 줄의 선만 |
| 네 캐릭터 포즈 | 박사: 가운데 뒤에서 턱에 손, 쟁반을 바라봄 / 조수: 오른쪽 옆에서 작은 쟁반을 실험대로 나름 / 초파리: 왼쪽에서 오른쪽을 보며 쟁반을 손가락으로 가리킴 / 주판봇: 오른쪽에서 왼쪽을 보며 주판을 들고 창고 쪽을 고개로 가리킴 |
| 대체 글 (alt) | 밤의 연구실에서 조수가 창고의 블록 쟁반을 실험대로 옮기고, 초파리 연구원과 주판봇이 양쪽에서 쟁반을 바라보며 박사가 뒤에서 지켜보는 표지 |
| 앞 표지와 다른 점 | 시리즈 첫 표지 계열 — 이후 표지와 겹치지 않도록 '쟁반 나르기 + 창고 복도' 구도를 이 페이지 전용으로 둔다 |

**참고 이미지 (함께 올리기):** 네 캐릭터 기본 그림 4장 (기준: GitHub `adminmrobo/fruitfly-lab-expressions`, 주판봇은 v2 gpt2 단체 사진·기본 표정 9종).

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- 비율 16:9, 가로 1920px 이상
- 첨부한 참고 이미지의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 어둡고 단순하게
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Match the art style, proportions and colors of the attached reference images exactly
(if there are no reference images: 16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights).
Cozy night laboratory mood, purple light, soft magenta and green fluorescent accents.
Scene: a night laboratory; in the foreground a small, tidy lab bench glowing softly green; far down a corridor in the back, a huge storage room with tall shelves full of identical crates; a dashed light path runs along the floor from the storage room to the bench.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, standing at the back center with a hand on his chin, watching the bench;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, on the right side carrying a small square tray of glowing tiles toward the bench;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing at the tray with one eye narrowed;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, nodding toward the distant storage room.
Visual metaphor of the topic: on the bench, a grid of square tiles where only one small block of tiles lights up green at a time, like processing a big table piece by piece; an open notebook beside it shows just two blank horizontal lines.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner dark and simple; the light falls on the glowing tray and the tile grid on the bench.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

**고칠 때 (같은 대화에서):** `Same four characters, same art style and composition. Change only: {고칠 점}. Still no text.`

## 받은 뒤
SKILL 18-15 절차: 16:9·글자·네 캐릭터 확인 → WebP 1600×900(220KB 이하)·960×540 → `<!-- lab-cover -->` 사이의 대체 표지를 `<img>`로 바꿈 → 390·768·1280 폭 점검.
