# -*- coding: utf-8 -*-
"""스킬 v1.14 '낮의 연구실' — 생성기 없이 옮겨 온 옛 페이지(2·3주차)와 목차를 흰 배경으로 바꾼다.

글·상자·단추는 흰 화면 색 토큰(light.css)으로 덮고, 페이지 안 그래프(canvas)와 도식(svg)은
색이 그림 코드에 박혀 있어 어두운 '모니터 화면' 바탕을 그대로 둔다. 몇 번 돌려도 같은 결과.
사용: python3 daylight.py <스터디 북 루트>
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1]
FILES = ['index.html',
         'week_02_textbook_ch02_p1_p2/index.html', 'week_02_textbook_ch02_p1_p2/02_models.html',
         'week_02_article_01/index.html', 'week_02_article_01/01_transformer.html',
         'week_03_article_01/index.html', 'week_03_article_01/03_flash_attention.html',
         'week_03_textbook_ch02_p3_to_end/index.html']
light = open(os.path.join(HERE, 'light.css'), encoding='utf-8').read()
MON = ('\n/* 그림 코드에 색이 박힌 그래프·도식은 어두운 모니터 화면으로 둔다 */\n'
       'canvas{background:#161826;border-radius:10px}\n'
       '.svgwrap svg,figure svg,.fig svg,.diagram svg{background:#161826;border-radius:10px}\n'
       '.cwrap{background:#161826}\n'
       'body::before{background:#fff}\n.notebook{background:var(--amber-soft);border-color:rgba(163,92,0,.35)}\n.gentxt,pre.cite{background:var(--panel)}\n'
       '.hero-bg::after,.hero-bg:after{background:linear-gradient(90deg,#fff 0%,rgba(255,255,255,.9) 45%,rgba(255,255,255,.45) 100%),linear-gradient(0deg,#fff,transparent 30%)}\n'
       '.badge.no,.explain .lim{color:var(--amber)}\n.badge.ok,.lvtag.g,.qitem .fb.ok{color:var(--gfp)}\n.flow span.s.on{color:var(--gfp)}\n.bt[aria-pressed=true],.bt.primary{color:#fff}\n.kgitem p{color:var(--muted)}\n.lvtag,.pathchips span.l,.qitem .fb.no{color:var(--eye)}\n'
       'header.hero .hero-bg.img::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#fff 0%,rgba(255,255,255,.88) 40%,rgba(255,255,255,.45) 100%),linear-gradient(0deg,#fff,transparent 30%)}\n')
BLOCK = '<style id="daylight">' + light + MON + '</style>'
for f in FILES:
    p = os.path.join(ROOT, f)
    if not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<style id="daylight">.*?</style>', '', s, flags=re.S)
    i = s.rfind('</head>')
    s = s[:i] + BLOCK + s[i:]
    open(p, 'w', encoding='utf-8').write(s)
    print('낮의 연구실', f)
