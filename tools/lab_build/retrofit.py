# -*- coding: utf-8 -*-
"""이미 연구실 스킬로 만든 페이지에 식구 전원(시아·모아·미공개)과 스터디 북 연결을 덧붙인다.

본문 섹션·시뮬레이션·지식 색인은 그대로 두고, 아래만 바꾼다(표시 <!-- lab-crew --> … <!-- /lab-crew -->):
  1) 글 표지 → 여섯 식구 줄 세운 표지 (그림 지시문은 COVER_*.md)
  2) 상단 내비 맨 앞에 스터디 북 목차 링크
  3) 히어로 대화에 시아·모아 한 줄씩
  4) 등장인물 카드에 시아·모아 + 버튼 뒤 미공개 X1~X3, 오늘의 순서
  5) 대결 아래 진행 신호(시아)·응원(모아)·방청석(미공개)
  6) 정리 섹션에 모아의 기록장
  7) 바닥글에 식구 표기
그림은 페이지 Cast와 섞이지 않도록 data-lx 속성으로 따로 채운다.
"""
import re, json, os, base64
from lab import resolve, PACK, esc

LX_CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extra.css'), encoding='utf-8').read()

def lx_img(who, mood, big=False, cls=''):
    return '<img data-lx="%s" data-lxm="%s"%s alt="" aria-hidden="true"%s>' % (who, mood, ' data-lxbig' if big else '', ' class="%s"' % cls if cls else '')

def lx_say(who, mood, name, text):
    return '<div class="say" data-who="%s">%s<div><b class="name">%s</b><p>%s</p></div></div>' % (who, lx_img(who, mood, cls='who'), name, text)

def cover_html(key, chip, alt, moods, motif):
    order = ['fly', 'asst', 'doc', 'sia', 'moa', 'robo']
    imgs = ''.join(lx_img(w, moods[w], big=True).replace('<img ', '<img data-who6="%s" ' % w) for w in order)
    return ('<header class="cover fallback" id="cover" data-img="%s" role="img" aria-label="%s"><div class="hex"></div><div class="bench"></div><div class="motif" aria-hidden="true">%s</div>'
            '<div class="line6">%s</div><span class="cover-chip">%s</span></header>') % (key, esc(alt), motif, imgs, chip)

def crew_block(roles, route_items):
    nos = {'sia': 'No.005', 'moa': 'No.006'}
    cards = ''.join('<div class="card" data-who="%s">%s<span class="no">%s</span><b>%s</b><span class="role">%s</span></div>' % (w, lx_img(w, m), nos[w], n, roles[w])
                    for w, m, n in [('sia', 'guide', '인턴 시아'), ('moa', 'smile', '인턴 모아')])
    xs = ''.join('<div class="card">%s<b>미공개 %s</b><span class="role">방청석 (정체 비공개)</span></div>' % (lx_img(x, 'hint'), x.upper()) for x in ['x1', 'x2', 'x3'])
    route = '<div class="route">%s</div>' % ''.join('<a href="#%s"><b>%s</b>%s</a>' % r for r in route_items)
    return ('<h3>새 식구</h3><div class="cast c6" style="grid-template-columns:repeat(2,1fr)">%s</div>'
            '<div class="hiddenrow" id="xrow"><button class="bt" data-reveal="xrow" aria-expanded="false" data-on="방청석의 미공개 식구 보기" data-off="다시 숨기기">방청석의 미공개 식구 보기</button><div class="xs">%s</div></div>'
            '<h3>오늘의 순서 (시아 정리)</h3>%s') % (cards, xs, route)

def duel_extra():
    return ('<p class="signal">%s<span><b>인턴 시아</b> · 진행 신호: 위 "결과 보기"는 맞혀 보기를 고른 뒤에 눌러 주세요.</span></p>'
            '<p class="signal cheer">%s<span><b>인턴 모아</b> · 방청석 응원 담당 — 어느 쪽이 이기든 기록장에 적어 둘게요!</span></p>'
            '<div class="audience" id="aud"><button class="bt" data-reveal="aud" aria-expanded="false" data-on="방청석 보기" data-off="방청석 닫기">방청석 보기</button>'
            '<div class="seats">%s%s%s<span>(반짝) (…) (짝짝)</span></div></div>') % (lx_img('sia', 'signal'), lx_img('moa', 'cheer'), lx_img('x1', 'cheer'), lx_img('x2', 'cheer'), lx_img('x3', 'cheer'))

LX_JS = r'''(function(){var S=window.LX_SPRITE||{},B=window.LX_BIG||{};
function src(w,m,big){var k=w+'_'+m;return (big&&B[k])||S[k]||S[w+'_'+({sia:'smile',moa:'smile',x1:'hint',x2:'hint',x3:'hint',doc:'front',asst:'smile',fly:'clip',robo:'smile'})[w]]||'';}
Array.prototype.forEach.call(document.querySelectorAll('img[data-lx]'),function(i){i.src=src(i.dataset.lx,i.dataset.lxm,i.hasAttribute('data-lxbig'));i.decoding='async';});
Array.prototype.forEach.call(document.querySelectorAll('[data-reveal]'),function(b){b.addEventListener('click',function(){var box=document.getElementById(b.dataset.reveal);if(!box)return;var on=!box.classList.contains('open');box.classList.toggle('open',on);b.setAttribute('aria-expanded',on?'true':'false');b.textContent=on?b.dataset.off:b.dataset.on;});});})();'''

def sprites_for(html):
    keys = set()
    for m in re.finditer(r'data-lx="([a-z0-9]+)" data-lxm="([a-z_]+)"(\s+data-lxbig)?', html):
        keys.add((m.group(1) + '_' + m.group(2), bool(m.group(3))))
    for w, d in [('sia', 'smile'), ('moa', 'smile'), ('x1', 'hint'), ('x2', 'hint'), ('x3', 'hint')]:
        keys.add((w + '_' + d, False))
    S, B = {}, {}
    for k, big in keys:
        who = k.split('_')[0]; real = resolve(k)
        f = os.path.join(PACK, 'webp', '192' if big else '96', who, real + '.webp')
        if os.path.exists(f):
            (B if big else S)[k] = 'data:image/webp;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    return S, B

def mark(s):
    return '<!-- lab-crew -->' + s + '<!-- /lab-crew -->'

def retrofit(html, cfg):
    # 1 표지
    html, n = re.subn(r'<header class="cover[^"]*"[^>]*>.*?</header>', mark(cover_html(cfg['cover_key'], cfg['chip'], cfg['alt'], cfg['moods'], cfg['motif'])), html, count=1, flags=re.S)
    assert n == 1, 'cover not found'
    # 2 내비
    ni = html.find('<nav class="top"'); ne = html.find('</nav>', ni)
    html = html[:ne] + mark('<a class="l" href="../index.html" style="color:var(--gfp)">↩ 스터디 북 목차</a>') + html[ne:]
    # 3 히어로 대화: 첫 dialog 끝에
    i = html.find('class="dialog"')
    assert i > 0, 'dialog not found'
    j = html.find('</div></div></div>', i) if cfg.get('dialog_close') is None else html.find(cfg['dialog_close'], i)
    # dialog 블록의 끝: dialog 안 say들이 끝나는 지점 = 마지막 say 뒤
    depth = 0; k = html.find('>', i) + 1; pos = k
    while True:
        o = html.find('<div', pos); c = html.find('</div>', pos)
        if c < 0: raise ValueError('dialog end')
        if o != -1 and o < c: depth += 1; pos = o + 4
        else:
            if depth == 0: end = c; break
            depth -= 1; pos = c + 6
    html = html[:end] + mark(lx_say('sia', 'explain', '인턴 시아', cfg['sia_hero']) + lx_say('moa', 'tea', '인턴 모아', cfg['moa_hero'])) + html[end:]
    # 4 등장인물 섹션 끝 (</section> 직전의 </div>)
    m = re.search(r'<section class="level" id="%s"[^>]*>' % cfg['cast_id'], html)
    assert m, 'cast not found'
    se = html.find('</section>', m.end())
    inner_end = html.rfind('</div>', m.end(), se)
    html = html[:inner_end] + mark(crew_block(cfg['roles'], cfg['route'])) + html[inner_end:]
    # 5 대결
    m = re.search(r'<section class="level" id="%s"[^>]*>' % cfg['duel_id'], html)
    assert m, 'duel not found'
    se = html.find('</section>', m.end()); inner_end = html.rfind('</div>', m.end(), se)
    html = html[:inner_end] + mark(duel_extra()) + html[inner_end:]
    # 6 정리
    m = re.search(r'<section class="level" id="%s"[^>]*>' % cfg['sum_id'], html)
    assert m, 'summary not found'
    se = html.find('</section>', m.end()); inner_end = html.rfind('</div>', m.end(), se)
    nb = '<div class="notebook"><h4>모아의 기록장</h4><ul>%s</ul></div>' % ''.join('<li>%s</li>' % t for t in cfg['notebook'])
    html = html[:inner_end] + mark(nb + lx_say('moa', 'ok', '인턴 모아', cfg['moa_sum'])) + html[inner_end:]
    # 7 바닥글
    html = re.sub(r'(</footer>)', mark('<div class="wrap"><p class="muted" style="font-size:13px">인퍼런스 스터디 북 연구실판 · 식구: 박사 · 조수(하루) · 초파리 연구원 · 주판봇 · 인턴 시아 · 인턴 모아 (+ 미공개 X1~X3) · 형식: ai-lab-explainer v1.12 · <a href="../index.html">스터디 북 목차</a></p></div>') + r'\1', html, count=1)
    # CSS·JS·그림
    S, B = sprites_for(html)
    html = html.replace('</head>', mark('<style>' + LX_CSS + '.cover .line6 img[data-who6=doc]{width:min(17vw,170px)}.cover .line6 img[data-who6=asst]{width:min(15.5vw,155px)}.cover .line6 img[data-who6=sia]{width:min(15vw,150px)}.cover .line6 img[data-who6=moa]{width:min(14.5vw,145px)}.cover .line6 img[data-who6=robo]{width:min(13vw,130px)}.cover .line6 img[data-who6=fly]{width:min(10vw,100px)}'
                                             '.cover.fallback{position:relative;background:linear-gradient(160deg,#1b1533,#13141f);height:min(48vh,420px);overflow:hidden}.cover .hex{position:absolute;inset:0;background-image:radial-gradient(circle at 78% 22%,rgba(214,114,214,.25),transparent 55%),radial-gradient(circle at 20% 80%,rgba(94,227,156,.12),transparent 50%)}.cover .bench{position:absolute;left:0;right:0;bottom:0;height:34%;background:linear-gradient(180deg,#2a2342,#1a1628);border-top:3px solid #3a3058}</style>') + '</head>', 1)
    html = html.replace('</body>', mark('<script>var LX_SPRITE=' + json.dumps(S) + ';var LX_BIG=' + json.dumps(B) + ';' + LX_JS + '</script>') + '</body>', 1)
    if 'ai-lab-explainer v1.12' not in html:
        html = html.replace('</body>', '<!-- ai-lab-explainer v1.12 (retrofit: lab-crew) --></body>', 1)
    return html
