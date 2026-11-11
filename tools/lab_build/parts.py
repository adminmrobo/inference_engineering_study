# -*- coding: utf-8 -*-
"""사다리 칸·섹션 조각 (SKILL 4-3 블록 순서)."""
from lab import say

def level(no, sid, title, tags, pair=None, panel='', explain='', bridge='', talk='', quiz=True, small='칸', extra_top=''):
    tg = ''.join('<span class="lvtag %s">%s</span>' % (c, t) for c, t in tags)
    pr = ''
    if pair:
        pr = ('<div class="pair"><div><span class="tag fly">%s</span><p>%s</p></div><div><span class="tag nn">%s</span><p>%s</p></div></div>'
              % (pair[0], pair[1], pair[2], pair[3]))
    q = '<div class="quiz" data-quiz="%s"></div>' % sid if quiz else ''
    return ('<section class="level" id="%s"><div class="wrap"><div class="lvhead"><div class="hexno">%s<small>%s</small></div><div><h2>%s</h2><p class="sub">%s</p></div></div>'
            '%s%s%s%s%s%s%s</div></section>') % (sid, no, small, title, tg, extra_top, pr, panel, explain, bridge, talk, q)

def panel(title, canvas_id, h_label, ctrl='', kp_id=None, eq='', ins_id=None, act='', wide=False):
    kp = '<div class="kpis" id="%s"></div>' % kp_id if kp_id else ''
    ii = '<div class="insight" id="%s" aria-live="polite"></div>' % ins_id if ins_id else ''
    eqh = '<div class="eq">%s</div>' % eq if eq else ''
    cv = '<div class="cwrap"><canvas id="%s"%s aria-label="%s"></canvas></div>' % (canvas_id, ' class="wide"' if wide else '', h_label) if canvas_id else ''
    return '<div class="panel"><h3>%s</h3>%s<div class="ctrl">%s</div>%s%s%s%s</div>' % (title, cv, ctrl, kp, eqh, ii, act)

def act(title, canvas_id, label, note=''):
    return ('<div class="panel"><h3>행동으로 보기 · %s</h3><div class="cwrap"><canvas id="%s" aria-label="%s"></canvas></div>%s</div>'
            % (title, canvas_id, label, '<p class="muted" style="font-size:14px;margin:8px 0 0">%s</p>' % note if note else ''))

def explain(title, items, limit=None, ordered=True):
    tag = 'ol' if ordered else 'ul'
    lim = '<p class="lim"><b>이 칸의 한계:</b> %s</p>' % limit if limit else ''
    return '<div class="explain"><h4>%s</h4><%s>%s</%s>%s</div>' % (title, tag, ''.join('<li>%s</li>' % i for i in items), tag, lim)

def bridge(gen=None, field=None):
    h = ''
    if gen: h += '<div class="bridge gen"><h4>생성 AI로 치면</h4><p>%s</p><p class="lim">비유의 한계: %s</p></div>' % gen
    if field: h += '<div class="bridge field"><h4>현장에 옮기면</h4><p>%s</p><p class="lim">비유의 한계: %s</p></div>' % field
    return h

def math(summary, body):
    return '<details class="math"><summary>%s</summary>%s</details>' % (summary, body)

def btn_group(gid, label, opts, sel=0):
    return '<div class="group" id="%s"><span class="glabel">%s</span>%s</div>' % (gid, label, ''.join(
        '<button class="bt" data-v="%s" aria-pressed="%s">%s</button>' % (v, 'true' if i == sel else 'false', t) for i, (v, t) in enumerate(opts)))

def slider(sid, label, mn, mx, step, val, unit=''):
    return ('<div class="group"><label class="glabel" for="%s">%s</label><input type="range" id="%s" min="%s" max="%s" step="%s" value="%s"><span class="val" id="%sV">%s%s</span></div>'
            % (sid, label, sid, mn, mx, step, val, sid, val, unit))

def section(sid, no, title, inner, small='절', tags=()):
    tg = ''.join('<span class="lvtag %s">%s</span>' % (c, t) for c, t in tags)
    return ('<section class="level" id="%s"><div class="wrap"><div class="lvhead"><div class="hexno">%s<small>%s</small></div><div><h2>%s</h2><p class="sub">%s</p></div></div>%s</div></section>'
            % (sid, no, small, title, tg, inner))

def route(items):
    return '<div class="route">%s</div>' % ''.join('<a href="#%s"><b>%s</b>%s</a>' % (i, n, t) for i, n, t in items)
