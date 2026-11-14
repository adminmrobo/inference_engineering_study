# -*- coding: utf-8 -*-
"""연구실 해설 페이지 빌더 (ai-lab-explainer v1.12 규격).

페이지 내용(page spec)을 받아 단일 HTML 하나로 묶는다.
공용 CSS·JS(lab.css, extra.css, lab_core.js) + 그 페이지에 쓰는 캐릭터 그림만 base64로 넣는다.
"""
import base64, json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.environ.get('LAB_PACK', '/home/claude/ref/ahnboat_lab_explainer/packs/character/character_pack')
EXPR = json.load(open(os.path.join(HERE, 'expression_map.json'), encoding='utf-8'))
# 시아·모아·미공개 뜻 이름 키 (CHAR_lab4 18-5 → 표정 번호)
EXTRA_ALIAS = {
    'sia_smile': 'sia_e13', 'sia_signal': 'sia_e10', 'sia_explain': 'sia_e07', 'sia_guide': 'sia_e08', 'sia_think': 'sia_e09',
    'sia_firm': 'sia_e12', 'sia_proud': 'sia_e16', 'sia_doze': 'sia_e17', 'sia_stop': 'sia_e05', 'sia_angry': 'sia_e22', 'sia_shock': 'sia_e24',
    'moa_smile': 'moa_e13', 'moa_tea': 'moa_e01', 'moa_cheer': 'moa_e12', 'moa_plant': 'moa_e16', 'moa_report': 'moa_e07', 'moa_guide': 'moa_e08',
    'moa_think': 'moa_e09', 'moa_ok': 'moa_e10', 'moa_sparkle': 'moa_e19', 'moa_cry': 'moa_e21', 'moa_shock': 'moa_e24',
    'x1_hint': 'x1_e13', 'x2_hint': 'x2_e13', 'x3_hint': 'x3_e13', 'x1_cheer': 'x1_e01', 'x2_cheer': 'x2_e01', 'x3_cheer': 'x3_e01',
}
for k, v in EXPR.items():
    if k.split('_')[0] in ('sia', 'moa', 'x1', 'x2', 'x3'):
        EXTRA_ALIAS[k] = v['key']
ALIAS = {k: v['key'] for k, v in EXPR.items()}
ALIAS.update(EXTRA_ALIAS)
DEF = {'doc': 'front', 'asst': 'smile', 'fly': 'clip', 'robo': 'smile', 'sia': 'smile', 'moa': 'smile', 'x1': 'hint', 'x2': 'hint', 'x3': 'hint'}
NAMES = {'doc': '박사', 'asst': '조수(하루)', 'fly': '초파리 연구원', 'robo': '주판봇', 'sia': '인턴 시아', 'moa': '인턴 모아', 'x1': '미공개', 'x2': '미공개', 'x3': '미공개'}
# 대결에서 바뀌는 표정 (Duel 함수가 쓰는 키)
DUEL_KEYS = ['fly_point', 'fly_arms', 'fly_coffee', 'fly_cry', 'robo_coin', 'robo_sigh', 'robo_happy', 'robo_meh', 'robo_calc', 'robo_blush',
             'sia_signal', 'sia_stop', 'sia_proud', 'sia_think', 'moa_cheer', 'moa_think', 'moa_smile', 'moa_shock', 'doc_judge', 'doc_think']

def _b64(who, key, size):
    f = os.path.join(PACK, 'webp', str(size), who, key + '.webp')
    if not os.path.exists(f):
        return None
    return 'data:image/webp;base64,' + base64.b64encode(open(f, 'rb').read()).decode()

def resolve(key):
    """뜻 이름 키 → 표정 번호 키. 그림 파일이 없으면 같은 캐릭터 기본 표정."""
    who = key.split('_')[0]
    real = ALIAS.get(key, key)
    if not os.path.exists(os.path.join(PACK, 'webp', '96', who, real + '.webp')):
        real = ALIAS.get(who + '_' + DEF[who], who + '_e13')
    return real

def sprites(body, extra=(), big_keys=()):
    pairs = set()
    for m in re.finditer(r'<img[^>]*?data-who="([a-z0-9]+)"[^>]*>', body):
        tag = m.group(0); who = m.group(1)
        mm = re.search(r'data-mood="([a-z_]+)"', tag)
        pairs.add(who + '_' + (mm.group(1) if mm else DEF[who]))
    for who in DEF:
        pairs.add(who + '_' + DEF[who])
    pairs.update(extra)
    S, A, B = {}, {}, {}
    for k in sorted(pairs):
        who = k.split('_')[0]
        if who not in DEF:
            continue
        real = resolve(k)
        if real not in S:
            d = _b64(who, real, 96)
            if d: S[real] = d
        if k != real:
            A[k] = real
    for k in big_keys:
        who = k.split('_')[0]; real = resolve(k)
        d = _b64(who, real, 192)
        if d: B[k] = d
    return S, A, B

def esc(s):
    return html.escape(s, quote=True)

# ---------- 공용 HTML 조각 ----------
def say(who, mood, text, name=None):
    return ('<div class="say" data-who="%s"><img class="who" data-who="%s" data-mood="%s" alt="" aria-hidden="true">'
            '<div><b class="name">%s</b><p>%s</p></div></div>') % (who, who, mood, name or NAMES[who], text)

def cover(key, chip, alt, motif='', moods=None, img=None):
    moods = moods or {}
    order = ['fly', 'asst', 'doc', 'sia', 'moa', 'robo']
    if img:
        return ('<header class="cover" id="cover" data-img="%s"><img class="full" src="%s" width="1600" height="900" alt="%s" fetchpriority="high" decoding="async">'
                '<span class="cover-chip">%s</span></header>') % (key, img, esc(alt), chip)
    imgs = ''.join('<img data-big data-who="%s" data-mood="%s" alt="" aria-hidden="true">' % (w, moods.get(w, DEF[w])) for w in order)
    return ('<header class="cover fallback" id="cover" data-img="%s" role="img" aria-label="%s"><div class="hex"></div><div class="bench"></div>'
            '<div class="motif" aria-hidden="true">%s</div><div class="line6">%s</div><span class="cover-chip">%s</span></header>') % (key, esc(alt), motif, imgs, chip)

def crew(roles, title='등장인물 · 이 페이지 사용법', sec_id='cast', extra=''):
    """roles: {who: 역할 한 줄}. 미공개 셋은 버튼 뒤에."""
    cards = ''
    nos = {'doc': 'No.001', 'asst': 'No.002', 'fly': 'No.003', 'robo': 'No.004', 'sia': 'No.005', 'moa': 'No.006'}
    for w in ['doc', 'asst', 'fly', 'robo', 'sia', 'moa']:
        cards += ('<div class="card" data-who="%s"><img data-who="%s" alt="" aria-hidden="true"><span class="no">%s</span><b>%s</b>'
                  '<span class="role">%s</span></div>') % (w, w, nos[w], NAMES[w], roles.get(w, ''))
    xs = ''.join('<div class="card"><img data-who="%s" alt="" aria-hidden="true"><b>미공개 %s</b><span class="role">%s</span></div>'
                 % (x, x.upper(), roles.get(x, '방청석 (정체 비공개)')) for x in ['x1', 'x2', 'x3'])
    return ('<section class="level" id="%s"><div class="wrap"><h2>%s</h2><div class="cast c6">%s</div>'
            '<div class="hiddenrow" id="xrow"><button class="bt" data-reveal="xrow" aria-expanded="false" data-on="방청석의 미공개 식구 보기" data-off="다시 숨기기">방청석의 미공개 식구 보기</button><div class="xs">%s</div></div>'
            '%s</div></section>') % (sec_id, title, cards, xs, extra)

def duel(q, fly_pick, fly_line, robo_pick, robo_line, guess_note='', metric=''):
    return ('<div class="duel" id="duelBox"><p class="signal"><img data-who="sia" data-mood="signal" alt="" aria-hidden="true"><span><b>인턴 시아</b> · 진행 신호: 준비되면 결과 보기를 누르세요.</span></p>'
            '<div class="head"><div><img data-big data-who="fly" data-mood="point" alt="" aria-hidden="true"><b style="color:var(--c-fly)">초파리 연구원</b></div><div class="vs">VS</div>'
            '<div><img data-big data-who="robo" data-mood="coin" alt="" class="flip" aria-hidden="true"><b style="color:var(--c-robo)">주판봇</b></div></div>'
            '<p class="q" style="text-align:center;margin:8px 0">%s</p>'
            '<div class="choices"><div class="choice f"><b class="nm">초파리 연구원의 선택</b><p>%s</p><p class="muted">“%s”</p></div>'
            '<div class="choice r"><b class="nm">주판봇의 선택</b><p>%s</p><p class="muted">“%s”</p></div></div>'
            '<p class="glabel">먼저 맞혀 보기 (기록만, 저장 안 함)</p><div class="guess"><button class="bt" data-guess="fly" aria-pressed="false">초파리가 이길 것 같다</button><button class="bt" data-guess="robo" aria-pressed="false">주판봇이 이길 것 같다</button></div>'
            '<p style="text-align:center"><button class="bt primary reveal">결과 보기</button></p>'
            '<div class="result"><div class="bars"></div><p class="score duelScore"></p>'
            '<div class="say asst" data-who="asst"><img class="who" data-who="asst" data-mood="report" alt="" aria-hidden="true"><div><b class="name">조수(하루) · 숫자 발표</b><p></p></div></div>'
            '<div class="say verdict" data-who="doc"><img class="who" data-who="doc" data-mood="judge" alt="" aria-hidden="true"><div><b class="name">박사 · 판정</b><p></p></div></div>'
            '<p class="notice duelNote"></p>'
            '<p class="signal cheer"><img data-who="moa" data-mood="cheer" alt="" aria-hidden="true"><span><b>인턴 모아</b> · 방청석 응원 담당 — 어느 쪽이든 오늘의 기록장에 적어 둘게요!</span></p>'
            '<div class="audience" id="aud"><button class="bt" data-reveal="aud" aria-expanded="false" data-on="방청석 보기" data-off="방청석 닫기">방청석 보기</button>'
            '<div class="seats"><img data-who="x1" data-mood="cheer" alt="" aria-hidden="true"><img data-who="x2" data-mood="cheer" alt="" aria-hidden="true"><img data-who="x3" data-mood="cheer" alt="" aria-hidden="true"><span>(반짝) (…) (짝짝)</span></div></div>'
            '</div>%s</div>') % (q, fly_pick, fly_line, robo_pick, robo_line, metric)

def kg_section():
    return ('<section class="level" id="kg"><div class="wrap"><h2>지식 색인</h2><p class="muted">이 페이지에 나온 개념·방법·한계·주장을 찾아보고, 선을 따라 앞뒤 관계를 봅니다.</p>'
            '<div class="kpis" id="kgStats"></div><div class="kgtools"><input type="search" id="kgQ" placeholder="찾을 말 (예: 지연시간, KV 캐시)" aria-label="지식 색인 검색"></div>'
            '<div class="kgtools" id="kgChips"></div><div class="kggrid"><div class="kglist" id="kgList" aria-live="polite"></div>'
            '<div><div class="cwrap"><canvas id="cKG" aria-label="지식 그래프 미니 지도. 점을 누르면 왼쪽 목록에서 강조됩니다."></canvas></div><div class="legend" id="kgLegend"></div></div></div>'
            '<h3>한계 → 해결 사슬</h3><div class="flow" id="kgPath"></div><h3>열린 질문</h3><ul id="kgOpen"></ul></div></section>')

def export_section():
    return ('<section class="level" id="export"><div class="wrap"><h2>온톨로지·서지 꾸러미</h2>'
            + say('moa', 'report', '<span id="exSay"></span>') +
            '<div class="kpis" id="exStats"></div><h3>이 페이지 인용하기</h3><div class="group"><button class="bt" data-cf="text" aria-pressed="true">글</button><button class="bt" data-cf="bib" aria-pressed="false">BibTeX</button><button class="bt" data-cf="ris" aria-pressed="false">RIS</button><button class="bt" id="citeCopy">복사</button></div>'
            '<pre class="citebox" id="citeBox"></pre><h3>참고문헌</h3><div class="reflist" id="refList"></div>'
            '<h3>범위 고르기 → 내려받기</h3><div class="group"><button class="bt" data-sc="all" aria-pressed="true">전체</button><button class="bt" data-sc="concepts" aria-pressed="false">개념만</button><button class="bt" data-sc="claims" aria-pressed="false">주장·문헌</button><button class="bt" data-sc="prereq" aria-pressed="false">선수 관계</button></div>'
            '<p><button class="bt primary" id="zipBtn">ZIP 하나로 내려받기 (JSON-LD · Turtle · CSV · CSL-JSON · BibTeX · RIS)</button> <button class="bt" id="kgJson">kg.json만</button></p>'
            '<details class="math"><summary>파일 하나씩 받기</summary><div class="dl" id="fileBtns"></div></details>'
            '<details class="math"><summary>확인할 항목</summary><ul id="todoList"></ul></details><p class="notice" id="exVer"></p></div></section>')

def nav(items, home='../index.html', home_label='스터디 북'):
    links = ''.join('<a class="l" href="#%s">%s</a>' % (i, l) for i, l in items)
    return '<nav class="top" aria-label="이 페이지 바로가기"><a class="logo" href="%s"><i></i>%s</a>%s</nav>' % (home, home_label, links)

def build(spec, out):
    css = open(os.path.join(HERE, 'lab.css'), encoding='utf-8').read() + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read() + spec.get('css', '')
    core = open(os.path.join(HERE, 'lab_core.js'), encoding='utf-8').read()
    body = spec['body']
    big = []
    for m in re.finditer(r'<img data-big data-who="([a-z0-9]+)" data-mood="([a-z_]+)"', body):
        big.append(m.group(1) + '_' + m.group(2))
    S, A, B = sprites(body, DUEL_KEYS + list(spec.get('extra_sprites', [])), big)
    meta = spec['meta']
    J = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
    head = ('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            '<title>%s</title><meta name="description" content="%s"><meta name="author" content="안상선">'
            '<meta property="og:type" content="article"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s">%s'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">'
            '<style>%s</style></head><body>') % (esc(meta['title']), esc(meta['description']), esc(meta['title']), esc(meta['description']), esc(meta.get('url', '')), ('<meta property="og:image" content="%s">' % esc(meta['image']) if meta.get('image') else ''), css)
    tail = ('<div id="tip" role="tooltip"></div><div id="study" aria-label="학습 도우미"><span id="stRead">읽은 곳 0%</span><span id="stQuiz">퀴즈 0/0</span><button class="bt" id="stMode">밑줄: 핵심</button></div>'
            '<script type="application/json" id="kg-raw">' + J(spec['kg']) + '</script>'
            '<script type="application/ld+json" id="kg-ld">' + J({'@context': {'skos': 'http://www.w3.org/2004/02/skos/core#', 'schema': 'https://schema.org/'}, '@type': 'schema:LearningResource', 'schema:name': meta['title'], 'schema:author': '안상선', 'schema:inLanguage': 'ko'}) + '</script>'
            '<script type="application/json" id="refs-csl">' + J(spec['refs']) + '</script>'
            '<script type="application/json" id="page-meta">' + J(meta) + '</script>'
            '<script>var SPRITE=' + J(S) + ';var SPRITE_ALIAS=' + J(A) + ';var SPRITE_BIG=' + J(B) + ';'
            'var GL=' + J(spec.get('gl', {})) + ';var CORE=' + J(spec.get('core', [])) + ';var QUIZ=' + J(spec.get('quiz', {})) + ';</script>'
            '<script>' + core + '</script><script>(function(){var L=window.LAB,$=L.$,$$=L.$$;' + spec.get('js', '') + '\nL.start();})();</script></body></html>')
    page = head + '<div id="prog" aria-hidden="true"></div>' + spec['nav'] + body + kg_section() + export_section() + spec['footer'] + tail
    try:  # 인퍼런스 공장 — 이 페이지가 맡은 층을 첫 화면에 (층이 없는 페이지는 그대로)
        import factory
        ab = os.path.abspath(out)
        page = factory.apply(page, os.path.dirname(os.path.dirname(ab)), os.path.basename(os.path.dirname(ab)))
    except ImportError:
        pass
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page)
    return len(page.encode('utf-8'))

# ---------- 지식 그래프 도우미 ----------
def node(i, typ, ko, en, anchor, page, defi=None, src=None, level=None, family='systems', alt=None, evidence=None, confidence='high'):
    n = {'id': i, 'type': typ, 'label': {'ko': ko, 'en': en}, 'page': page, 'anchor': anchor, 'domain': ['ai'], 'anchorType': 'B', 'flyStrength': 'none', 'status': 'known', 'confidence': confidence, 'family': family}
    if defi: n['definition'] = {'ko': defi}
    if level: n['level'] = level
    if alt: n['altLabel'] = {'ko': alt}
    if evidence: n['evidence'] = evidence
    if src: n['source'] = [{'cite': src[0], 'work': src[0], 'loc': src[1], 'verified': True}]
    return n

def edge(s, p, o, anchor='#top', conf='high'):
    return {'s': s, 'p': 'lab:' + p, 'o': o, 'anchor': anchor, 'confidence': conf}

def ref(i, typ, title, authors, year, container=None, url=None, role='primary', publisher=None, note=None):
    r = {'id': i, 'type': typ, 'title': title, 'author': [{'literal': a} if ' ' not in a or a.endswith('.') else {'family': a.split(' ')[-1], 'given': ' '.join(a.split(' ')[:-1])} for a in authors],
         'issued': {'date-parts': [[year]]}, 'lab': {'role': role, 'verified': {'title': True, 'authors': True, 'year': True}}}
    if container: r['container-title'] = container
    if url: r['URL'] = url
    if publisher: r['publisher'] = publisher
    if note: r['lab']['note'] = note
    return r

BOOK_REF = None
def book_ref():
    return ref('kiely2026inference', 'book', 'Inference Engineering', ['Philip Kiely'], 2026, publisher='Baseten Books',
               url='https://www.baseten.co/inference-engineering/', role='primary')

def footer(src_rows, demo_items, prev=None, nxt=None, extra='', ver='v1.12'):
    rows = ''.join('<tr><td>%s</td><td>%s</td></tr>' % r for r in src_rows)
    demos = ''.join('<li>%s</li>' % d for d in demo_items)
    links = ''
    if prev: links += '<a href="%s">← %s</a> · ' % prev
    links += '<a href="../index.html">스터디 북 목차</a>'
    if nxt: links += ' · <a href="%s">%s →</a>' % nxt
    return ('<footer><div class="wrap"><h3>출처</h3><div class="tw"><table class="tb"><tr><th>항목</th><th>출처</th></tr>%s</table></div>'
            '<h3>예시값·설명용 모형인 것</h3><ul>%s</ul>%s<p>%s</p>'
            '<p>글 · 안상선 ((주)M-Robo 대표) · 캐릭터: 박사 · 조수(하루) · 초파리 연구원 · 주판봇 · 인턴 시아 · 인턴 모아 (설정·그림 저작권 안상선, 허락 없이 사용 금지) · '
            '형식: ai-lab-explainer %s · 이 해설은 교재·논문의 요약·해설이며 원문을 대신하지 않습니다.</p></div></footer>') % (rows, demos, extra, links, ver)
