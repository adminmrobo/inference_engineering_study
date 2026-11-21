# -*- coding: utf-8 -*-
"""확장 스킬북(ai-lab-extend v1.2) 덧입히기 — 1~4주차 교재·논문 페이지.

이미 만든 페이지(생성기 출력 · 옮겨 온 페이지)의 틀은 그대로 두고, 아래만 끼우거나 바꾼다.
  · 처음 오신 분께 3줄 상자 + 영어 약어 풀이(abbr.py에서 본문에 나온 것만)   → 히어로 바로 뒤
  · 단계마다: 박사의 현장 질문 · 왜 이 방법 + 조수가 대신 묻는 수식            → 비교 카드(.pair) 앞
               실험 앞 대화(박사 · 주판봇 · 초파리 · 조수)                     → 첫 실험 패널 앞
               박사의 업무 해석 · 인턴 다시 말하기 · AI 판단 코너 · 방청석 질문  → 퀴즈 앞
  · 본문 문장 고치기(데이터 파일의 REPL), 금지 표현 정리, 여백 완화 CSS, 바닥글 소개 주소
끼운 조각은 <!--ext:s--> … <!--ext:e--> 사이에 있어서 다시 돌리면 지우고 새로 끼운다.
문구는 전부 ext/<폴더>.py 데이터 파일에 있다. 문구만 고치려면 그 파일만 고치고 다시 돌리면 된다.

사용: python3 extend.py ../..            (모든 대상 페이지)
      python3 extend.py ../.. week_01_textbook_preface   (한 페이지)
순서: 생성기 · run_retrofit · factory · daylight 다음, 맨 마지막에 돌린다.
"""
import os, re, sys, json, html, base64, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for _p in [os.environ.get('LAB_PACK', ''), '/home/claude/ref/ahnboat_lab_explainer/packs/character/character_pack',
           '/home/claude/adminmrobo/ahnboat_lab_explainer/packs/character/character_pack']:
    if _p and os.path.isdir(_p):
        os.environ['LAB_PACK'] = _p; break
from lab import resolve, PACK, NAMES          # noqa: E402
import plain                                  # noqa: E402
from abbr import ABBR                         # noqa: E402

TARGETS = ['week_01_textbook_preface', 'week_01_textbook_ch00', 'week_01_textbook_ch01', 'week_01_article_01',
           'week_02_textbook_ch02_p1_p2', 'week_02_article_01', 'week_03_textbook_ch02_p3_to_end', 'week_03_article_01',
           'week_04_textbook_ch03', 'week_04_article_01']
FOOT_ONLY = ['week_05_textbook_ch04', 'week_05_article_01']   # 이미 비전공자판 — 바닥글 소개 주소만 맞춤
ABOUT = 'https://adminmrobo.github.io/who_am_i/who_am_i.html'
S, E = '<!--ext:s-->', '<!--ext:e-->'

EXT_CSS = plain.PLAIN_CSS + r'''
/* ai-lab-extend 4장 여백 완화 */
body{line-height:1.8}
.level{padding-block:88px}
.level>.wrap.stack{gap:40px}
.pair{gap:20px}.pair>div{padding:20px 22px}
.panel{padding:22px;gap:18px}
.explain{padding:22px 24px;gap:12px}
.explain ol,.explain ul{display:flex;flex-direction:column;gap:10px;padding-left:22px}
.dialog.lvtalk{gap:14px;padding:18px 20px;border-radius:12px;border:1px dashed var(--rule)}
@media (max-width:700px){.level{padding-block:64px}.level>.wrap.stack{gap:30px}}
#plain{padding:8px 0 0}
.wm .mech{margin:10px 0 0;padding:10px 12px;border-radius:10px;border:1px dashed var(--rule);font-size:15px}
.wm .mech b{color:var(--c-doc)}
.say img[data-ex]{image-rendering:pixelated}
footer a,footer p{overflow-wrap:anywhere}
.wm td,.wm th{overflow-wrap:anywhere}
'''

EX_JS = r'''(function(){var S=window.EXT_SPRITE||{};
Array.prototype.forEach.call(document.querySelectorAll('img[data-ex]'),function(i){var k=i.getAttribute('data-ex')+'_'+i.getAttribute('data-exm');if(S[k]){i.src=S[k];}i.decoding='async';});})();'''


def load(slug):
    f = os.path.join(HERE, 'ext', slug + '.py')
    spec = importlib.util.spec_from_file_location('ext_' + slug, f)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def ex_imgs(h):
    """공용 조각(plain.py)의 캐릭터 그림을 이 덧입히기 전용 그림 표시로 바꾼다(페이지 원래 Cast와 섞이지 않게)."""
    return re.sub(r'<img class="who" data-who="([a-z0-9]+)" data-mood="([a-z_]+)"', r'<img class="who" data-ex="\1" data-exm="\2"', h)


def wrap(h):
    return S + ex_imgs(h) + E


def strip_old(page):
    page = re.sub(re.escape(S) + r'.*?' + re.escape(E), '', page, flags=re.S)
    page = re.sub(r'<style id="ext-css">.*?</style>', '', page, flags=re.S)
    page = re.sub(r'<script id="ext-js">.*?</script>', '', page, flags=re.S)
    return page


# ---------- 금지 표현 정리 (용어 규칙) ----------
TERM_FIX = [
    (r'이 칸의 한계', '이 단계의 한계'), (r'다음 칸', '다음 단계'), (r'앞 칸', '앞 단계'), (r'세 칸 비교', '세 단계 비교'),
    (r'([①-⑳0-9]+) ?칸', r'\1 단계'), (r'(\d+)<small>칸</small>', r'\1<small>단계</small>'), (r'<small>칸</small>', '<small>단계</small>'),
    (r'<th>칸</th>', '<th>단계</th>'), (r'세 칸', '세 단계'), (r'네 칸', '네 단계'), (r'다섯 칸', '다섯 단계'), (r'두 칸', '두 단계'),
    (r'한 칸 위로', '한 단계 위로'), (r'한 칸씩', '하나씩'), (r'칸막이 GPU', '나눠 쓰는 GPU'), (r'칸막이를', '구획을'), (r'칸막이가', '구획이'), (r'빈칸 (어디|아무)', r'빈자리 \1'), (r'칸막이', '구획'), (r'빈칸', '공란'),
    (r'이 칸', '이 단계'), (r'그 칸', '그 단계'), (r'나머지 칸', '나머지 단계'), (r'칸으로', '단계로'), (r'남는 칸', '남는 자리'), (r'고립된 칸', '따로 노는 구역'), (r'각 칸', '각 단계'), (r'멈춤 칸', '멈춤 시간'), (r'어긋난 칸', '어긋난 과제'), (r'마지막 칸', '마지막 자리'), (r'높았던 칸', '높았던 과제'), (r'남은 칸', '남은 자리'), (r'칸이 하나씩', '자리가 하나씩'), (r'칸을', '자리를'), (r'칸에', '자리에'), (r'칸의', '자리의'),
    (r'칸마다', '단계마다'), (r'칸 수', '개수'), (r'칸 숫자', '자리 숫자'), (r'캐시 칸', '캐시 자리'), (r'칸 ([①-⑳])', r'단계 \1'),
    (r'단계을', '단계를'), (r'단계이([ ,.)])', r'단계가\1'), (r'단계은', '단계는'), (r'단계과', '단계와'), (r'단계으로', '단계로'),
    (r'(만|\d\)) 칸', r'\1 개'), (r'칸끼리', '자리끼리'), (r'칸 밀림', '자리 밀림'), (r'테두리 칸', '테두리 자리'), (r'큰 칸이', '큰 자리가'), (r'칸이', '자리가'), (r'칸은', '자리는'),
    (r'(파란|보라|빨간|초록|회색|노란) 칸', r'\1 네모'),
    (r'칸 늦게', '단계 늦게'), (r'(전문가|토큰) 칸', r'\1 자리'), (r'한 칸', '한 자리'),
    (r'사다리', '개념정리'), (r'관통하는', '하나로 잇는'), (r'관통', '하나로 이음'),
]


JOSA = {'이': '가', '을': '를', '은': '는', '과': '와', '으로': '로'}


def kan_to_jari(t):
    return re.sub(r'칸(으로|이|을|은|과)?', lambda m: '자리' + (JOSA[m.group(1)] if m.group(1) else ''), t)


def fix_terms(page, pre=(), kan_all=False):
    # style 안은 건드리지 않는다 (script 안의 퀴즈·안내 문장은 한국어라 함께 고친다)
    parts = re.split(r'(<style\b.*?</style>)', page, flags=re.S)
    for i in range(0, len(parts), 2):
        t = parts[i]
        for a, b in list(pre):
            t = re.sub(a, b, t)
        if kan_all:
            t = kan_to_jari(t)
        for a, b in TERM_FIX:
            t = re.sub(a, b, t)
        parts[i] = t
    return ''.join(parts)


def leftover_terms(page):
    body = re.sub(r'<style\b.*?</style>', '', page, flags=re.S)
    return sorted(set(m.group(0) for m in re.finditer(r'.{0,12}(칸|사다리|관통).{0,12}', body)))


# ---------- 블록 ----------
def three(m, page):
    body = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', '', page, flags=re.S)
    body = re.sub(r'<[^>]+>', ' ', body)
    found = set(re.findall(r'(?<![A-Za-z])([A-Z][A-Za-z0-9]*[A-Z0-9][A-Za-z0-9]*)(?![A-Za-z])', body))
    ab = [(k, '%s — %s' % ABBR[k]) for k in sorted(ABBR, key=lambda x: (x.lower())) if k in found]
    ab = [(k, v) for k, v in ab if k not in getattr(m, 'ABBR_SKIP', ())]
    what, why, work = m.THREE
    h = plain.three_lines(what, why, work, ab)
    h = h.replace('코드와 수식을 몰라도 됩니다. 수식은 조수가 대신 묻고, 코드는 접어 두었어요.',
                  '코드와 수식을 몰라도 됩니다. 수식은 조수가 대신 묻고 숫자로 한 번 풀어 보며, 기계 이야기는 일상 예시로 먼저 봅니다.')
    return '<section id="plain"><div class="wrap">%s</div></section>' % h


def whybox(st):
    w = st.get('why')
    if not w:
        return ''
    title = st.get('why_title', '왜 이 방법을 쓰나')
    mt = st.get('math')
    h = plain.whymath(w, mt)
    h = h.replace('<h4>왜 이 방법을 쓰나</h4>', '<h4>%s</h4>' % title)
    if st.get('mech'):
        # 기계·장치 이야기를 일상 예시로 한 번 더 (어렵다는 반응이 많은 곳)
        h = h.replace('</p></div>', '</p><p class="mech"><b>기계로 보면</b> %s</p></div>' % st['mech'], 1)
    return h


def blocks_before_pair(st):
    h = ''
    if st.get('recap'):
        h += plain.recap(st['recap'])
    if st.get('situ'):
        h += plain.situ(st['situ'])
    h += whybox(st)
    return h


def blocks_before_panel(st):
    c = st.get('chat')
    return plain.stepchat(*c) if c else ''


def blocks_end(st):
    h = ''
    if st.get('interp'):
        it = st['interp']
        h += plain.interp(it[0], it[1] if len(it) > 1 else None)
    if st.get('again'):
        h += plain.again(*st['again'])
    if st.get('x'):
        h += plain.xbox(st['x'])
    if st.get('ai'):
        h += plain.aicheck(*st['ai'])
    if st.get('code'):
        h += plain.codefold(st['code'], st.get('code_title', '원문의 코드로 보면 (몰라도 됩니다)'))
    return h


def section_span(page, sid):
    m = re.search(r'<section class="level[^"]*" id="%s"' % re.escape(sid), page)
    if not m:
        return None
    a = m.start()
    # 다음 단계 섹션 시작(또는 바닥글) 직전까지
    n = re.search(r'<section class="level[^"]*" id="|<footer', page[m.end():])
    b = m.end() + n.start() if n else len(page)
    return a, b


def first(seg, pats):
    best = None
    for p in pats:
        mm = re.search(p, seg)
        if mm and (best is None or mm.start() < best):
            best = mm.start()
    return best


def inject_step(page, sid, st, warn):
    sp = section_span(page, sid)
    if not sp:
        warn.append('단계 없음: %s' % sid); return page
    a, b = sp
    seg = page[a:b]
    pre = blocks_before_pair(st)
    mid = blocks_before_panel(st)
    end = blocks_end(st)
    # 1) 비교 카드 앞 (없으면 실험 패널 앞, 그것도 없으면 단계 머리 뒤)
    i_pair = first(seg, [r'<div class="pair">'])
    i_panel = first(seg, [r'<section class="panel', r'<div class="panel'])
    i_quiz = first(seg, [r'<div class="quiz"'])
    if i_quiz is None:
        mm = list(re.finditer(r'</div>\s*</section>', seg))
        i_quiz = mm[-1].start() if mm else len(seg)
    ins = []
    if pre:
        if i_pair is not None:
            at = i_pair
        elif i_panel is not None:
            at = i_panel
        else:
            hm = re.search(r'</h2>.*?</div>\s*</div>|</h2>\s*<p class="sub">.*?</p>\s*</div>', seg, flags=re.S)
            at = hm.end() if hm else i_quiz
        ins.append((at, wrap(pre)))
    if mid:
        at = i_panel if (i_panel is not None and (i_pair is None or i_panel > i_pair)) else None
        if at is None:
            at = i_quiz
        ins.append((at, wrap(mid)))
    if end:
        ins.append((i_quiz, wrap(end)))
    for at, h in sorted(ins, key=lambda x: -x[0]):
        seg = seg[:at] + h + seg[at:]
    return page[:a] + seg + page[b:]


def sprites_js(page):
    keys = set(m.group(1) + '_' + m.group(2) for m in re.finditer(r'data-ex="([a-z0-9]+)" data-exm="([a-z_]+)"', page))
    out = {}
    for k in sorted(keys):
        who = k.split('_')[0]; real = resolve(k)
        f = os.path.join(PACK, 'webp', '96', who, real + '.webp')
        if os.path.exists(f):
            out[k] = 'data:image/webp;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    return out


def footer_fix(page):
    # 글 · 안상선 (소개 주소) · 소속  — 이미 고쳤으면 그대로
    if ABOUT not in page:
        page = re.sub(r'글 · 안상선 \(\(주\)M-Robo 대표\)',
                      '글 · 안상선 (<a href="%s">%s</a>) · (주)M-Robo 대표' % (ABOUT, ABOUT), page)
        page = re.sub(r'글 · 안상선 \(\(주\)M-Robo\)',
                      '글 · 안상선 (<a href="%s">%s</a>) · (주)M-Robo 대표' % (ABOUT, ABOUT), page)
        if ABOUT not in page:   # 바닥글 표기가 다른 페이지
            page = re.sub(r'(<footer[^>]*>)', r'\1<p class="byline" style="margin:0 0 8px">글 · 안상선 (<a href="%s">%s</a>) · (주)M-Robo 대표</p>' % (ABOUT, ABOUT), page, count=1)
    # 기계용 저자 정보(JSON-LD creator)에 같은 url
    page = page.replace('"creator": ["안상선"]', '"creator": [{"@type": "Person", "name": "안상선", "url": "%s", "affiliation": "(주)M-Robo 대표"}]' % ABOUT)
    page = re.sub(r'"creator": \[\{"name": "안상선", "role": "author", "affiliation": "\(주\)M-Robo( 대표)?"',
                  '"creator": [{"@type": "Person", "name": "안상선", "url": "%s", "role": "author", "affiliation": "(주)M-Robo 대표"' % ABOUT, page)
    page = page.replace('비전공자판(plain v1.1) · 이 해설', '비전공자판(plain v1.1) · 확장(extend v1.2) · 이 해설') if 'extend v1.2' not in page else page
    return page


def run(root, slug, warn):
    f = os.path.join(root, slug, 'index.html')
    page = open(f, encoding='utf-8').read()
    page = strip_old(page)
    if slug in FOOT_ONLY:
        page = footer_fix(page)
        open(f, 'w', encoding='utf-8').write(page)
        return
    m = load(slug)
    page = fix_terms(page, getattr(m, 'TERM_PRE', ()), getattr(m, 'KAN_TO_JARI', False))   # 원문 표현을 먼저 맞춘 뒤 문장 바꾸기
    for a, b in getattr(m, 'REPL', []):
        if a in page:
            page = page.replace(a, b)
        elif b not in page:
            warn.append('%s: 바꿀 문장 없음 — %s' % (slug, a[:40]))
    # 3줄 상자
    hm = re.search(r'<header class="hero"[^>]*>', page)
    he = page.find('</header>', hm.end()) + len('</header>')
    page = page[:he] + wrap(three(m, page)) + page[he:]
    for sid, st in m.STEPS.items():
        page = inject_step(page, sid, st, warn)
    page = fix_terms(page, getattr(m, 'TERM_PRE', ()), getattr(m, 'KAN_TO_JARI', False))
    page = footer_fix(page)
    if 'ai-lab-explainer' in page and 'extend v1.2' not in page:
        page = re.sub(r'(형식: ai-lab-explainer[^·<]*)', r'\1· 확장(extend v1.2) ', page, count=1)
    sp = sprites_js(page)
    if not sp:
        raise SystemExit('캐릭터 팩을 찾지 못했습니다 — LAB_PACK 환경 변수를 지정하세요')
    page = page.replace('</head>', '<style id="ext-css">%s</style></head>' % EXT_CSS, 1)
    page = page.replace('</body>', '<script id="ext-js">window.EXT_SPRITE=%s;%s</script></body>' % (json.dumps(sp), EX_JS), 1)
    for t in leftover_terms(page):
        warn.append('%s: 금지 표현 남음 — %s' % (slug, t))
    open(f, 'w', encoding='utf-8').write(page)


if __name__ == '__main__':
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '../..')
    only = sys.argv[2:]
    warn = []
    for slug in TARGETS + FOOT_ONLY:
        if only and slug not in only:
            continue
        if slug in TARGETS and not os.path.exists(os.path.join(HERE, 'ext', slug + '.py')):
            warn.append('데이터 파일 없음: ' + slug); continue
        run(root, slug, warn)
        print('ok', slug)
    for w in warn:
        print('!', w)
