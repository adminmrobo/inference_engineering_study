# -*- coding: utf-8 -*-
"""목록 카드 한 벌 — 썸네일 · 제목 · 소개 한 줄을 모든 편에 같은 틀로 맞춘다 (몇 번 돌려도 같은 결과).

틀
  제목   : 교재 = "{장 표기} · {제목}"            예) 1장 · 시작 전에 정할 것 / 2장 후반 · 병목을 찾아라
           논문 = "{장} 논문 · {제목} ({논문 이름})" 예) 2장 논문 · 번개 어텐션 (FlashAttention)
  소개   : "이 편을 읽으면 …할 수 있습니다." 한 줄 (series.CARDS[folder]['card'])
  썸네일 : 1200×630. 위 = 그 편이 맡은 공장 층(3D), 아래 흰 띠 = 층·주차 / 제목 / 교재·논문 꼬리표, 왼쪽 장 색 막대

사용
  python3 cards.py <루트> --shots <three 패키지 폴더>   # 3D 층을 찍어 thumb.jpg를 다시 만든다 (Chrome · Playwright · Pillow)
  python3 cards.py <루트> --extra <저장소 사본 폴더>     # 짝 저장소(스터디 보드 · 발표 자료) 카드 그림을 cards/ 에 다시 만든다
  python3 cards.py <루트>                             # og 메타 · catalog_cards.json만 고친다
만드는 것: <폴더>/thumb.jpg, 각 index.html 의 og:/twitter: 메타 (<!-- card:og --> 블록), 루트의 catalog_cards.json
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from series import WEEKS, CARDS, BASE, REPO
import factory

START, END = '<!-- card:og -->', '<!-- /card:og -->'
LANGS = ['ko', 'en', 'zh', 'ja', 'ru', 'uz', 'vi']
FONT_B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_R = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CHAP_COL = {'c01': '#7a3fd6', 'c2': '#13733a', 'c3': '#1e55c8', 'c4': '#0b7a86', 'c5': '#a35c00', 'c6': '#c42a6e', 'c7': '#c9302c', 'ap': '#5b6874'}


def entries(root):
    out = [{'folder': '', 'kind': 'index', 'chap': '목차', 'order': 0, 'title': '목차 · 인퍼런스 스터디 북',
            'summary': '『Inference Engineering』 10주 스터디를 장별로 묶은 연구실 해설 스터디 북 — 첫 화면의 추론 공정 제어판에서 "그래서 GPU로 LLM을 어떻게 돌리나"를 한 장으로 봅니다.',
            'eyebrow': '인퍼런스 스터디 북 · 3D GPU 추론 공장 · 10주', 'col': '#7a3fd6'}]
    n = 0
    for w in WEEKS:
        for it in w['items']:
            c = CARDS.get(it['folder'])
            if not c or not os.path.exists(os.path.join(root, it['folder'], 'index.html')):
                continue
            n += 1
            short = it['title'].split(' — ')[0]
            if it['kind'] == 'textbook':
                title = '%s · %s' % (it['label'], short)
            else:
                title = '%s 논문 · %s (%s)' % (c['chap'], short, c['paper'])
            fi = factory.floor_of(it['folder'])
            f = factory.FLOORS[fi]
            out.append({'folder': it['folder'], 'kind': it['kind'], 'chap': c['chap'], 'order': n, 'title': title, 'summary': c['card'],
                        'eyebrow': '인퍼런스 스터디 북 · %s %s · %d주차' % (f['fl'], f['name'], w['no']), 'col': CHAP_COL[f['chap']]})
    for e in out:
        d = os.path.join(root, e['folder'])
        e['langs'] = ['ko'] + [l for l in LANGS[1:] if any(x.endswith('.%s.html' % l) for x in os.listdir(d))] if e['folder'] else langs_all(root)
        e['site_url'] = BASE + (e['folder'] + '/' if e['folder'] else '')
        e['repo_url'] = REPO + ('/tree/main/' + e['folder'] if e['folder'] else '')
        e['thumb'] = e['site_url'] + 'thumb.jpg'
    return out


# 스터디 북 밖의 짝 저장소 — 같은 틀의 카드 그림만 이 저장소 cards/ 에 둔다 (그림은 --extra <저장소 사본 폴더> 로 다시 찍는다)
RELATED = [
    {'repo': 'inference_korea_study_page', 'kind': 'board', 'chap': '목차', 'title': '스터디 보드 · Inference Korea',
     'summary': '이 보드를 보면 『Inference Engineering』 10주 스터디의 일정(매주 토요일 저녁 8시 Zoom)과 주차별 범위를 한눈에 확인할 수 있습니다.',
     'eyebrow': 'Inference Korea · 스터디 일정 · 10주', 'col': '#7a3fd6', 'langs': ['ko', 'en', 'zh']},
    {'repo': 'inference_engineering_study_week_02_textbook_ch02_p3_to_end_slide', 'kind': 'slide', 'chap': '2장', 'title': '2장 후반 발표 · 병목을 찾아라',
     'summary': '이 자료로 2장 후반(2.3–2.5)의 병목 진단을 약 30분 발표 흐름으로 따라갈 수 있습니다.',
     'eyebrow': '인퍼런스 스터디 · 3주차 발표 자료 · 부록', 'col': '#5b6874', 'langs': ['ko']},
]


def related():
    out = []
    for r in RELATED:
        e = dict(r)
        e['site_url'] = 'https://adminmrobo.github.io/%s/' % r['repo']
        e['repo_url'] = 'https://github.com/adminmrobo/%s' % r['repo']
        e['thumb'] = BASE + 'cards/%s.jpg' % r['repo']
        out.append(e)
    return out


def extra_shots(root, src_dir):
    import asyncio
    from playwright.async_api import async_playwright

    async def route(r):
        u = r.request.url
        await (r.continue_() if u.startswith('file://') or u.startswith('data:') else r.abort())

    async def run():
        os.makedirs(os.path.join(root, 'cards'), exist_ok=True)
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
            for e in related():
                pg = await b.new_page(viewport={'width': 1280, 'height': 720}, device_scale_factor=1.5, locale='ko-KR')
                await pg.route('**/*', route)
                await pg.goto('file://' + os.path.abspath(os.path.join(src_dir, e['repo'], 'index.html')))
                await pg.wait_for_timeout(2500)
                tmp = os.path.join(root, 'cards', '_render.png')
                await pg.screenshot(path=tmp)
                await pg.close()
                compose(tmp, e, os.path.join(root, 'cards', e['repo'] + '.jpg'))
                os.remove(tmp)
                print('카드 그림', e['repo'])
            await b.close()
    asyncio.run(run())


def langs_all(root):
    s = set()
    for dp, _, fs in os.walk(root):
        for x in fs:
            m = re.search(r'\.([a-z]{2})\.html$', x)
            if m and m.group(1) in LANGS:
                s.add(m.group(1))
    return ['ko'] + [l for l in LANGS[1:] if l in s]


def og_block(e):
    esc = lambda t: t.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return (START + '\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:image" content="%s">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n'
            '<meta name="twitter:image" content="%s">\n' % (esc(e['title']), esc(e['summary']), e['thumb'], esc(e['title']), esc(e['summary']), e['thumb']) + END)


def apply_og(root, e):
    p = os.path.join(root, e['folder'], 'index.html')
    s = open(p, encoding='utf-8').read()
    t = re.sub(re.escape(START) + '.*?' + re.escape(END) + r'\n?', '', s, flags=re.S)
    t = re.sub(r'<meta (?:property="og:(?:title|description|image(?::\w+)?)"|name="twitter:\w+")[^>]*>\n?', '', t)
    t = t.replace('</head>', og_block(e) + '\n</head>', 1)
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)
    return t != s


def compose(render, e, out):
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    W, H, TOP = 1200, 630, 452
    im = Image.new('RGB', (W, H), '#ffffff')
    im.paste(ImageOps.fit(Image.open(render).convert('RGB'), (W, TOP), centering=(0.5, 0.45)), (0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, TOP, W, H], fill='#ffffff')
    d.line([0, TOP, W, TOP], fill='#d5dbe2', width=2)
    d.rectangle([0, TOP, 14, H], fill=e['col'])
    fe, ft, fp = ImageFont.truetype(FONT_R, 24), ImageFont.truetype(FONT_B, 46), ImageFont.truetype(FONT_B, 24)
    d.text((44, TOP + 22), e['eyebrow'], font=fe, fill='#5b6874')
    title = e['title']
    while d.textlength(title, font=ft) > W - 44 - 200 and len(title) > 8:
        title = title[:-2] + '…' if not title.endswith('…') else title[:-3] + '…'
    d.text((44, TOP + 62), title, font=ft, fill='#16212b')
    tag = {'textbook': '교재', 'article': '논문', 'index': '목차', 'board': '보드', 'slide': '발표'}[e['kind']]
    tw = d.textlength(tag, font=fp)
    x1, y1 = W - 44 - tw - 36, TOP + 74
    d.rounded_rectangle([x1, y1, W - 44, y1 + 44], radius=22, fill=e['col'])
    d.text((x1 + 18, y1 + 6), tag, font=fp, fill='#ffffff')
    lang = '%d개 언어' % len(e['langs']) if len(e['langs']) > 1 else '한국어'
    d.text((44, TOP + 132), '%s · %s' % (e['chap'], lang), font=fe, fill='#5b6874')
    im.save(out, 'JPEG', quality=86, optimize=True, progressive=True)


def shots(root, entries_, three):
    import asyncio
    from playwright.async_api import async_playwright

    async def route(r):
        u = r.request.url
        if 'cdn.jsdelivr.net/npm/three@' in u:
            await r.fulfill(path=os.path.join(three, u.split('three@%s/' % factory.THREE_VER)[1]), content_type='application/javascript')
        elif u.startswith('file://') or u.startswith('data:'):
            await r.continue_()
        else:
            await r.abort()

    async def run():
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path='/usr/bin/google-chrome',
                                        args=['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
            for e in entries_:
                folder = os.path.join(root, e['folder'])
                tmp = os.path.join(folder, '_render.png')
                if e['folder']:
                    pg = await b.new_page(viewport={'width': 1600, 'height': 1000}, device_scale_factor=1.5, locale='ko-KR')
                    await pg.route('**/*', route)
                    await pg.goto('file://' + os.path.abspath(os.path.join(folder, 'index.html')) + '?lang=ko')
                    await pg.add_style_tag(content='#factory .gf-tools,#factory .gf-hint{display:none!important}')
                    await pg.wait_for_timeout(4000)
                    await (await pg.query_selector('#factory .gf-stage')).screenshot(path=tmp)
                    await pg.close()
                    src = tmp
                else:
                    src = os.path.join(root, 'cover_factory.jpg')
                compose(src, e, os.path.join(folder, 'thumb.jpg'))
                if os.path.exists(tmp):
                    os.remove(tmp)
                print('썸네일', e['folder'] or '(목차)', e['title'])
            await b.close()
    asyncio.run(run())


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '../..'
    es = entries(root)
    if '--shots' in sys.argv:
        shots(root, es, sys.argv[sys.argv.index('--shots') + 1])
    if '--extra' in sys.argv:
        extra_shots(root, sys.argv[sys.argv.index('--extra') + 1])
    for e in es:
        if apply_og(root, e):
            print('og 메타', e['folder'] or 'index.html')
    keep = ['folder', 'kind', 'chap', 'order', 'title', 'summary', 'langs', 'site_url', 'repo_url', 'thumb']
    json.dump({'series': '인퍼런스 스터디 북', 'rule': '목록은 책의 장(chap) 순서, 같은 장 안에서는 order 순서. 제목·소개·썸네일은 이 파일이 기준.',
               'items': [{k: e[k] for k in keep} for e in es],
               'related': [{k: e[k] for k in ['repo', 'kind', 'chap', 'title', 'summary', 'langs', 'site_url', 'repo_url', 'thumb']} for e in related()]}, open(os.path.join(root, 'catalog_cards.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('catalog_cards.json', len(es), '편')
