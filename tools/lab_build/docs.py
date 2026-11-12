# -*- coding: utf-8 -*-
"""폴더별 README·표지 지시문·이미지 명세서와 저장소 맨 위 README·cover_manifest.json을 쓴다. 사용: python3 docs.py <스터디 북 루트>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from series import *

ROOT = sys.argv[1]
DESC = {  # 18-4 고정 외형 영어 묘사
 'doc': 'chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie',
 'asst': 'girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans',
 'fly': 'anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings',
 'robo': 'boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus',
 'sia': 'calm girl maid intern, long straight jet-black hair with side-swept bangs, no headdress, gray eyes, small silver drop earrings, charcoal-black long-sleeved maid dress, large gray bow, long white frilled apron',
 'moa': 'gentle girl maid intern, long ash-beige wavy hair, white frilled maid headband with a ribbon over the left ear, amber-brown eyes, red and navy plaid bow tie, camel knit cardigan, white frilled apron, black skirt'}

PAGES = [
 dict(folder='week_01_textbook_preface', key='cover_pre', n='01-0', title='추론은 이제 모두의 일 — 서문', kind='교재', src='Kiely (2026) Inference Engineering, Preface',
      scene='a tall glass reagent cabinet overflowing with countless small glowing bottles, some bottles floating out of the shelves', metaphor='an explosion of open models shown as thousands of small glowing bottles pouring out of a cabinet',
      poses={'doc': 'center back, arms wide toward the cabinet, excited', 'asst': 'beside the doctor, holding a clipboard, counting bottles', 'fly': 'on the left facing right, pointing at one bottle, skeptical', 'robo': 'on the right facing left, raising an upward chart', 'sia': 'front left, calmly sorting bottles into a rack', 'moa': 'front right, carrying a tray with a teapot and smiling'},
      ko_alt='연구실 식구 여섯이 병이 쏟아지는 시약장 앞에 모인 표지', duel='9의 개수 (F 초파리 승)', outro='sc_pre_outro'),
 dict(folder='week_01_textbook_ch00', key='cover_00', n='01-1', title='추론이란 무엇인가 — 0장', kind='교재', src='Kiely (2026) Inference Engineering, Chapter 0',
      scene='a three-tier lab shelf: bottom tier server racks with blue light, middle tier a glowing GPU chip with pink light, top tier a simple green control panel', metaphor='three stacked glowing tiers (infrastructure, runtime, tooling) like a layered lab shelf',
      poses={'doc': 'center back, pointing at the middle tier', 'asst': 'tightening a bolt on the bottom tier', 'fly': 'on the left facing right, inspecting the top tier with a magnifier', 'robo': 'on the right facing left, typing on a calculator', 'sia': 'labeling each tier with blank tags', 'moa': 'watering a small plant on the top tier'},
      ko_alt='연구실 식구 여섯이 세 층 선반 앞에 모인 표지', duel='초안을 쓸까? (R 주판봇 승)', outro='sc_00_outro'),
 dict(folder='week_01_textbook_ch01', key='cover_01', n='01-2', title='시작 전에 정할 것 — 1장', kind='교재', src='Kiely (2026) Inference Engineering, Chapter 1',
      scene='a lab arranged like a small sports field with different training equipment stations', metaphor='a long histogram of response times drawn as a row of glowing bars with one tall bar far to the right (the tail), no numbers',
      poses={'doc': 'center back, holding a stopwatch up', 'asst': 'writing measurements on a clipboard', 'fly': 'on the left facing right, pointing at the far-right tall bar', 'robo': 'on the right facing left, pointing at the middle of the bars', 'sia': 'standing by the start line with a small flag', 'moa': 'cheering from the side with both fists'},
      ko_alt='연구실 식구 여섯이 응답 시간 막대 앞에서 꼬리를 가리키는 표지', duel='평균 vs P99 (F 초파리 승)', outro='sc_01_outro'),
 dict(folder='week_01_article_01', key='cover_lb', n='01-A1', title='라이브벤치 — 새 시험지로만 재는 성적표', kind='논문', src='White et al. (2025) LiveBench, ICLR 2025',
      scene='a lab bulletin board where fresh blank exam sheets are being pinned while old sheets are taken down', metaphor='a monthly rotating board of blank exam papers, one sixth of them glowing new',
      poses={'doc': 'center back, holding a red stamp', 'asst': 'pinning a fresh blank sheet', 'fly': 'on the left facing right, examining an old sheet with a magnifier', 'robo': 'on the right facing left, holding a scoreboard with blank rows', 'sia': 'removing old sheets neatly into a box', 'moa': 'handing out new sheets from a stack'},
      ko_alt='연구실 식구 여섯이 매달 새 시험지가 붙는 게시판 앞에 선 표지', duel='문제를 바꾸면 순위가 흔들릴까 (R 주판봇 승)', outro='sc_lb_outro'),
 dict(folder='week_02_textbook_ch02_p1_p2', key='cover_ch2', n='02-1', title='모델 속 들여다보기 — 2장 전반', kind='교재', src='Kiely (2026) Inference Engineering, 2.1–2.2', page='02_models.html',
      scene='a lab kitchen counter where order tickets come in and small glowing plates (tokens) go out one by one', metaphor='plates leaving the kitchen one at a time on a conveyor, a prepared ingredient bin glowing (KV cache)',
      poses={'doc': 'center back, reading a long order ticket', 'asst': 'placing one plate on the conveyor', 'fly': 'on the left facing right, counting plates', 'robo': 'on the right facing left, assigning chefs from a small team of tiny figures', 'sia': 'arranging prepared ingredient bins', 'moa': 'carrying a teapot past the conveyor'},
      ko_alt='연구실 식구 여섯이 주방 같은 실험실에서 접시(토큰)가 하나씩 나가는 모습을 보는 표지', duel='(원본 대결 그대로)', outro=None, retro=True),
 dict(folder='week_02_article_01', key='cover_01', n='02-A1', title='트랜스포머 — 어텐션만으로 충분하다', kind='논문', src='Vaswani et al. (2017) Attention Is All You Need', page='01_transformer.html',
      scene='a long table of word cards with colored highlighter beams connecting distant cards', metaphor='several colored highlighter light beams jumping directly between far-apart cards',
      poses={'doc': 'center back, conducting the beams with both hands', 'asst': 'holding a pink highlighter', 'fly': 'on the left facing right, reading the cards in order one by one', 'robo': 'on the right facing left, holding many highlighters at once', 'sia': 'aligning the cards in a straight row', 'moa': 'sorting highlighters by color into a cup'},
      ko_alt='연구실 식구 여섯이 문장 카드 위로 뻗는 형광펜 빛줄기를 보는 표지', duel='(원본 대결 그대로)', outro=None, retro=True),
 dict(folder='week_03_article_01', key='cover_03', n='03-A1', title='번개 어텐션 — 창고를 덜 오가면 빨라진다', kind='논문', src='Dao et al. (2022) FlashAttention', page='03_flash_attention.html',
      scene='a small bright lab bench in front and a huge dim storage room at the end of a corridor', metaphor='trays of tiles carried from the storage room to a small bench, only one tile glowing green on the bench',
      poses={'doc': 'center back, watching with arms crossed', 'asst': 'carrying a tray of blocks', 'fly': 'on the left facing right, writing two lines in a notebook', 'robo': 'on the right facing left, standing at the storage room door with an abacus', 'sia': 'stacking empty trays neatly', 'moa': 'sweeping the corridor with a duster'},
      ko_alt='연구실 식구 여섯이 작은 실험대와 복도 끝 창고 사이에서 쟁반을 나르는 표지', duel='(원본 대결 그대로)', outro=None, retro=True),
]

def prompt(p):
    chars = ';\n  '.join('%s, %s' % (DESC[w], p['poses'][w]) for w in ['doc', 'asst', 'fly', 'robo', 'sia', 'moa'])
    return ('Website top cover illustration, wide 16:9.\nMatch the art style, proportions and colors of the attached reference images exactly\n'
            '  (if there are no reference images: 16-bit RPG style pixel art, bold dark outline, 2-3 tone shading, small highlights).\n'
            'Scene: night lab, indigo-violet background, purple light, teal monitor glow, %s.\nAll six characters together:\n  %s.\n'
            'Visual metaphor of the topic: %s.\nComposition: keep every face and hand inside the central safe area (12%% margin left and right, 10%% top, 18%% bottom);\n'
            '  keep the bottom-left corner dark and simple.\nMood: curious, friendly rivalry, the moment before the result.\n'
            'No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.') % (p['scene'], chars, p['metaphor'])

def cover_md(p):
    return ('# 표지 지시문 — %s %s\n\n| 항목 | 내용 |\n|---|---|\n| 키 · 판 | %s · L (16:9, 1920 이상) |\n| 장소 (앵커) | 밤의 연구실 |\n| 주제 은유 | %s |\n'
            '| 여섯 식구 포즈 | %s |\n| 대체 글 (alt) | %s |\n| 앞 표지와 다른 점 | 스터디 북 안의 다른 표지와 장소 소품·포즈가 겹치지 않게 정함 |\n\n'
            '**참고 이미지 (함께 올리기):** 여섯 식구 기본 그림 (기준: GitHub `adminmrobo/fruitfly-lab-expressions`, 시아·모아는 `specs/sia`, `specs/moa`).\n\n'
            '**지금 페이지에는** 그림이 없을 때 쓰는 대체 표지(여섯 식구 표정 그림을 한 줄로 세운 것)가 들어가 있습니다. 그림을 받으면 `assets/img/%s.webp`(1600×900, 220 KB 이하)로 넣고 표지 블록을 바꿉니다.\n\n'
            '**Genspark에 붙여 넣기 ↓**\n```\n웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.\n- 비율 16:9, 가로 1920px 이상\n- 첨부한 참고 이미지의 여섯 캐릭터(박사, 조수, 초파리 연구원, 주판봇, 인턴 시아, 인턴 모아)를 같은 그림체·같은 외형으로, 여섯 모두 등장\n'
            '- 그림 안에 글자·숫자·로고를 넣지 말 것\n- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 어둡고 단순하게\n아래 영어 프롬프트를 그대로 써 줘.\n\n%s\n```\n\n'
            '**고칠 때 (같은 대화에서):** `Same six characters, same art style and composition. Change only: {고칠 점}. Still no text.`\n') % (
        p['n'], p['title'], p['key'], p['metaphor'], ' / '.join('%s %s' % (k, v) for k, v in p['poses'].items()), p['ko_alt'], p['key'], prompt(p))

def img_md(p):
    rows = '| `%s` | L | 글 표지 (여섯 식구) | 페이지 맨 위 | 대체 표지 (표정 그림 줄 세우기) | P1 | 필요 |\n' % p['key']
    if p.get('outro'):
        rows += '| `%s` | E | 아웃트로 장면: 여섯 식구가 결과 앞에 모임 | 아웃트로 | 표정 그림 여섯 장 | P2 | 필요 |\n' % p['outro']
    return ('# 이미지 제작 명세서 — %s %s\n\n대결: %s\n\n| 키 | 판 | 내용 | 들어가는 곳 | 대신 쓰는 그림 | 우선 | 상태 |\n|---|---|---|---|---|---|---|\n%s'
            '| 표정 그림 | A~D | 캐릭터 팩 1.4 기본 표정 (페이지에 base64로 들어 있음) | 말풍선·등장인물·대결 | — | — | 있음 |\n\n'
            '- 그림 안 글자 없음, 실존 브랜드·인물 없음.\n- 미공개 X1~X3는 버튼 뒤(방청석)에만 둔다(캐릭터 팩 C9).\n- 표지 프롬프트는 `COVER_%s.md`.\n') % (p['n'], p['title'], p['duel'], rows, p['key'].replace('cover_', ''))

def readme(p):
    page = p.get('page', 'index.html')
    extra = ''
    if p.get('retro'):
        extra = ('\n## 이번 판에서 바뀐 것\n\n- 연구실 스킬 v1.12 규격으로 다시 적용: 식구 전원(박사·조수(하루)·초파리 연구원·주판봇·인턴 시아·인턴 모아, 방청석의 미공개 X1~X3) 등장\n'
                 '- 글 표지를 여섯 식구 표지로 교체(그림 지시문 `COVER_%s.md`), 히어로·등장인물·대결·정리에 시아·모아 자리 추가\n- 본문 실험·수치·지식 색인·꾸러미는 이전 판 그대로\n'
                 '- 외국어판(`*.en.html` 등)은 이전 판입니다. 새 판 번역은 언어팩으로 다시 만들 예정입니다.\n') % p['key'].replace('cover_', '')
    return ('# 인퍼런스 스터디 북 · %s — %s\n\n> 『Inference Engineering』 스터디 %s 해설 · 연구실 식구 전원 출연\n\n- **바로 읽기:** %s%s/\n- **스터디 북 목차:** %s\n- **자료:** %s\n- **해설 페이지:** [`%s`](%s) (단일 HTML, 설치 없이 브라우저에서 열림)\n%s\n'
            '## 페이지 구성\n\n표지 → 히어로 → 등장인물(여섯 식구 + 버튼 뒤 미공개) → 개념 사다리(또는 논문 순서) → 대결 → 정리(모아의 기록장) → 아웃트로 → 지식 색인 → 온톨로지·서지 꾸러미\n\n'
            '## 정확성 표시\n\n- 교재·논문 수치는 원문 그대로이며 `원문` 칩을 붙였습니다.\n- 시뮬레이션의 상수·예시는 설명용 모형이며 캔버스에 노란 도장을 찍었습니다.\n\n'
            '## 파일\n\n| 파일 | 내용 |\n|---|---|\n| `%s` | 해설 페이지 |\n| `COVER_%s.md` | 글 표지 그림 지시문 (Genspark 등) |\n| `IMG_%s.md` | 이미지 제작 명세서 |\n\n'
            '글 · 안상선 ((주)M-Robo 대표) · 캐릭터 설정·그림은 저작권자 허락 없이 사용할 수 없습니다.\n') % (
        p['n'], p['title'], p['kind'], BASE, p['folder'], BASE, p['src'], page, page, extra, page, p['key'], p['key'])

for p in PAGES:
    d = os.path.join(ROOT, p['folder'])
    for f in os.listdir(d):
        if f.startswith(('COVER_', 'IMG_')) and f.endswith('.md') and p.get('retro'):
            os.remove(os.path.join(d, f)) if f.startswith('COVER_') else None
    open(os.path.join(d, 'README.md'), 'w', encoding='utf-8').write(readme(p))
    open(os.path.join(d, 'COVER_%s.md' % p['key'].replace('cover_', '')), 'w', encoding='utf-8').write(cover_md(p))
    open(os.path.join(d, 'IMG_%s.md' % p['key'].replace('cover_', '')), 'w', encoding='utf-8').write(img_md(p))

# 목차 표지
idx = dict(n='00', title='인퍼런스 스터디 북 목차', key='cover_index', scene='a long lab corridor with ten doors in a row, each door leaking a different color of light',
           metaphor='a corridor of ten glowing doors, the first three doors open and bright, the rest softly lit', ko_alt='연구실 식구 여섯이 열 개의 문이 이어진 복도에 선 표지',
           poses={'doc': 'center back, pointing down the corridor', 'asst': 'holding an open book proudly', 'fly': 'on the left facing right, peeking into the first door', 'robo': 'on the right facing left, holding an upward chart', 'sia': 'holding a map of the doors', 'moa': 'carrying a tea tray at the entrance'})
open(os.path.join(ROOT, 'COVER_00_index.md'), 'w', encoding='utf-8').write(cover_md(idx))
open(os.path.join(ROOT, 'IMG_00_index.md'), 'w', encoding='utf-8').write(
    '# 이미지 제작 명세서 — 00 스터디 북 목차\n\n| 키 | 판 | 내용 | 우선 | 상태 |\n|---|---|---|---|---|\n| `cover_index` | L | 열 개의 문이 이어진 복도와 여섯 식구 (`COVER_00_index.md`) | P1 | 필요 (지금은 대체 표지) |\n| `thumb_{폴더}` | I | 폴더마다 표지를 3:2로 자른 썸네일 | P2 | 표지를 받은 뒤 |\n| `og_index` | K | 공유 미리보기 1200×630 | P3 | 표지를 받은 뒤 |\n')

# cover_manifest.json (18-16)
items = [{'id': 'cover_index', 'role': 'cover', 'path': 'index.html#cover', 'size': [1600, 900], 'characters': ['doc', 'asst', 'fly', 'jupanbot', 'sia', 'moa'], 'robot': 'jupanbot-v2', 'prompt_en': prompt(idx), 'source_of': None, 'status': 'todo'}]
ont = [{'path': 'index.html', 'kg': True, 'export': True}]
for p in PAGES:
    items.append({'id': p['folder'] + '/' + p['key'], 'role': 'cover', 'path': p['folder'] + '/index.html#cover', 'size': [1600, 900], 'characters': ['doc', 'asst', 'fly', 'jupanbot', 'sia', 'moa'], 'robot': 'jupanbot-v2', 'prompt_en': prompt(p), 'source_of': None, 'status': 'todo'})
    ont.append({'path': p['folder'] + '/index.html', 'kg': True, 'export': True})
ont.append({'path': 'week_03_textbook_ch02_p3_to_end/index.html', 'kg': True, 'export': True})
man = {'series_ko': '인퍼런스 스터디 북', 'title_ko': '인퍼런스 스터디 북 — 『Inference Engineering』 10주 연구실 해설', 'site_title': '인퍼런스 스터디 북', 'site_url': BASE,
       'ontology': {'pages': ont, 'files': []}, 'i18n': {'langs': ['ko'], 'pages': {'ko': len(ont)}, 'readme_langs': ['ko']}, 'languages': ['ko'], 'items': items, 'updated': '2026-11-11'}
open(os.path.join(ROOT, 'cover_manifest.json'), 'w', encoding='utf-8').write(json.dumps(man, ensure_ascii=False, indent=1))

# 저장소 README
rows = ''
for w in WEEKS:
    for it in w['items']:
        f = os.path.join(ROOT, it['folder'], 'index.html')
        st = '준비 중' if it['status'] == 'plan' else '원본 그대로' if it['status'] == 'kept' else ('연구실판 완성' if os.path.exists(f) and 'ai-lab-explainer v1.12' in open(f, encoding='utf-8').read() else '다시 만드는 중')
        link = '[%s](%s/)' % (it['folder'], it['folder']) if it['status'] != 'plan' else '`%s/` (예정)' % it['folder']
        rows += '| %d주차 | %s · %s | %s | %s | %s |\n' % (w['no'], '교재' if it['kind'] == 'textbook' else '논문', it['label'], it['title'], link, st)
for s in SPECIALS:
    rows += '| 부록 | %s | %s | `%s/` (예정) | 준비 중 |\n' % (s['label'], s['title'], s['folder'])
import factory
FROWS = ''.join('| %s %s | %s | %s |\n' % (f['fl'], f['name'], f['process'], ('%d주차 · ' % f['week'] if f['week'] else '') + factory.CHAP[f['chap']][0]) for f in reversed(factory.FLOORS))
open(os.path.join(ROOT, 'README.md'), 'w', encoding='utf-8').write('''# 인퍼런스 스터디 북 — 연구실 식구들과 읽는 『Inference Engineering』

> AI 모델을 더 빠르고, 더 싸고, 더 안정적으로 돌리려면 무엇을 알아야 할까?

『Inference Engineering』(Philip Kiely, Baseten Books, 2026)을 10주 동안 주차마다 **교재 한 꼭지 + 논문 한 편**씩 읽고, 연구실 식구들(박사 · 조수(하루) · 초파리 연구원 · 주판봇 · 인턴 시아 · 인턴 모아, 그리고 방청석의 미공개 셋)이 진행하는 해설 페이지로 만든 스터디 북입니다.

- **표지·목차 (바로 읽기):** %s
- 주차별 해설은 모두 이 저장소의 폴더 하나씩입니다. 예전 주차별 저장소(`inference_engineering_study_week_…`)는 그대로 남아 있지만, 이제 이 저장소의 폴더가 정식 주소입니다.

## 인퍼런스 공장 — 층 = 주차, 색 띠 = 책의 장

표지(목차) 첫 화면은 GPU로 답(토큰)을 만드는 3D 공장 건물입니다. 층을 누르면 그 층의 공정과 해설이 열리고, 각 해설 페이지 첫 화면에는 그 페이지가 맡은 층이 3D로 나와 기계 번호로 페이지 칸을 안내합니다.

| 층 | 공정 | 주차 · 장 |
|---|---|---|
%s
## 목차

| 주차 | 구분 | 제목 | 폴더 | 상태 |
|---|---|---|---|---|
%s
## 규칙

- 폴더 이름 = 옛 저장소 이름에서 `inference_engineering_study_`를 뺀 것: `week_{주차}_textbook_{장·범위}`, `week_{주차}_article_{번호}`, 부록은 `special_{번호}`.
- 한 주에 장이 바뀌면 장마다 따로 만든다(예: 3장, 5장, 7장). 큰 장은 범위로 나눈다(`_p1_p2`, `_p3_to_end`).
- 3주차 교재편(`week_03_textbook_ch02_p3_to_end/`)은 먼저 완성된 원본을 내용 수정 없이 그대로 옮겼다(맨 앞의 공장 층 안내만 덧붙임).
- 나머지 페이지는 연구실 해설 스킬(ai-lab-explainer v1.12, 캐릭터 팩 1.4) 규격으로 식구 전원이 나오도록 다시 적용했다.
- 페이지는 단일 HTML(외부 요청은 글꼴과, 첫 화면 공장 3D의 three.js뿐 — 불러오지 못해도 층·기계 목록 안내는 그대로 동작), 페이지마다 지식 색인(`#kg`)과 온톨로지·서지 꾸러미(`#export`)가 있다.
- 글 표지는 지금 대체 표지(여섯 식구 표정 그림 줄 세우기)이고, 그림 지시문은 폴더마다 `COVER_*.md`에 있다.

## 다시 만들기

```bash
cd tools/lab_build
python3 build_index.py ../..                    # 목차
python3 pages/p_preface.py ../..                # 1주차 서문 (p_ch00, p_ch01, p_livebench 같은 방식)
python3 run_retrofit.py <옛 저장소 사본 폴더> ../..  # 2·3주차 페이지에 식구 전원 더하기
python3 factory.py ../..                        # 모든 해설 페이지 첫 화면에 공장 층 안내 (층·기계 정의는 factory.py)
python3 build_index.py ../..                    # 목차 다시 (공장 3D 상태 반영)
python3 docs.py ../..                           # README·표지 지시문·cover_manifest.json
```

캐릭터 그림은 `adminmrobo/ahnboat_lab_explainer`의 캐릭터 팩(`LAB_PACK` 환경 변수로 위치 지정)에서 읽습니다.

글 · 안상선 ((주)M-Robo 대표) · 교재와 논문의 요약·해설이며 원문을 대신하지 않습니다. 캐릭터 설정·그림은 저작권자 허락 없이 사용할 수 없습니다.
''' % (BASE, FROWS, rows))
print('docs ok', len(PAGES))
