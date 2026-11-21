# -*- coding: utf-8 -*-
"""비전공자판 조각 (ai-lab-explainer-plain v1.1) — 5주차부터.

처음 오신 분께 3줄 상자, 왜 이 방법 + 조수 수식 상자, 단계 대화, 방청석 X1~X3 질문, 인턴 다시 말하기,
AI 판단 코너, 코드 접기 상자, 30초 복습, 박사의 교육자 대사(상황 질문 · 해석 문장 · 안심 신호).
"""
from lab import say

PLAIN_CSS = r'''
.three{border:2px solid var(--gfp);border-radius:16px;padding:16px 20px;margin:18px 0;background:var(--gfp-soft)}
.three h3{margin:0 0 8px;font-size:18px}
.three ol{margin:0;padding-left:22px}.three li{margin:6px 0;line-height:1.8}
.three .nocode{margin:10px 0 0;font-size:14px;color:var(--muted)}
.three details{margin-top:8px}.three summary{cursor:pointer;font-size:14px;color:var(--info)}
.three dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px;margin:8px 0 0;font-size:14px}.three dt{font-weight:700}.three dd{margin:0}
.situ{border-left:4px solid var(--c-doc);padding:2px 0 2px 12px;margin:6px 0 18px}
.situ .say{margin:0}
.wm{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:18px 0}
@media (max-width:860px){.wm{grid-template-columns:1fr}}
.wm>div{border:1px solid var(--rule);border-radius:14px;padding:18px 20px;background:#fff;line-height:1.8}
.wm h4{margin:0 0 10px;font-size:16px}
.wm .why h4{color:var(--gfp)}.wm .mq h4{color:var(--c-asst)}
.wm .why ol{margin:0;padding-left:20px}.wm .why li{margin:6px 0}
.wm .easy{margin:10px 0 0;padding:10px 12px;border-radius:10px;background:var(--gfp-soft);font-size:15px}
.wm .school{display:inline-block;margin:8px 0;padding:2px 10px;border-radius:999px;background:var(--info-soft);color:var(--info);font-size:13px;font-weight:700}
.wm table{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0}.wm td,.wm th{border-bottom:1px solid var(--rule);padding:6px 4px;text-align:left;vertical-align:top}
.wm .try{margin:10px 0;padding:10px 12px;border-radius:10px;background:var(--panel);font-size:15px;line-height:2}
.wm .say{margin:8px 0}
.stepchat{border:1px dashed var(--rule);border-radius:14px;padding:10px 14px;margin:16px 0;background:var(--panel)}
.stepchat>b{display:block;font-size:13px;color:var(--muted);margin-bottom:2px}
.stepchat .say{margin:6px 0}
.xbox{border:1px solid var(--rule);border-radius:14px;padding:12px 16px;margin:16px 0;background:#fff}
.xbox>b{display:block;font-size:14px;margin-bottom:4px}
.xbox .say{margin:6px 0}
.again{border-radius:14px;padding:10px 14px;margin:16px 0;background:var(--stain-soft)}
.again .say{margin:0}
.interp{border-radius:14px;padding:10px 14px;margin:16px 0;background:var(--info-soft)}
.interp .say{margin:0}
.calm{font-size:14px;color:var(--muted);margin:8px 0 0}
.recap{border-left:4px solid var(--amber);background:var(--amber-soft);border-radius:0 12px 12px 0;padding:10px 14px;margin:14px 0;font-size:15px}
.recap b{color:var(--amber)}
.aicheck{border:2px solid var(--c-robo);border-radius:16px;padding:14px 18px;margin:18px 0;background:#f1fafb}
.aicheck h4{margin:0 0 8px;color:var(--c-robo)}
.aicheck .claim{margin:6px 0;padding:10px 12px;border-radius:10px;background:#fff;border:1px solid var(--rule);font-size:15px}
.aicheck ul{margin:8px 0;padding-left:22px}
.aicheck details{margin-top:8px}.aicheck summary{cursor:pointer;font-weight:700;color:var(--c-robo)}
.codefold{margin:16px 0}.codefold summary{cursor:pointer;font-size:14px;color:var(--muted)}
.codefold table{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px}.codefold td{border-bottom:1px solid var(--rule);padding:6px 6px;vertical-align:top}
.codefold code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;white-space:pre-wrap;word-break:break-all;background:var(--panel);padding:1px 4px;border-radius:4px}
section.level{padding-top:88px;padding-bottom:20px}
@media (max-width:600px){section.level{padding-top:64px}}
.level p,.level li{line-height:1.8}
.explain li{margin-bottom:10px}
.xrole{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}
@media (max-width:700px){.xrole{grid-template-columns:1fr}}
.xrole .c{border:1px solid var(--rule);border-radius:12px;padding:10px 12px;display:flex;gap:10px;align-items:center;background:#fff}
.xrole img{width:56px;height:56px;image-rendering:pixelated}
.xrole b{display:block}.xrole span{font-size:14px;color:var(--muted)}
.blk{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px;margin:10px 0}
'''

XNAME = {'x1': '방청석 X1', 'x2': '방청석 X2', 'x3': '방청석 X3'}


def three_lines(what, why, work, abbr=()):
    ab = ''
    if abbr:
        ab = ('<details><summary>이 페이지의 영어 약어 풀이 (펼치기)</summary><dl>%s</dl></details>'
              % ''.join('<dt>%s</dt><dd>%s</dd>' % a for a in abbr))
    return ('<div class="three" id="three"><h3>처음 오신 분께 — 이 페이지를 3줄로</h3><ol>'
            '<li><b>무엇을:</b> %s</li><li><b>왜 중요한가:</b> %s</li><li><b>업무에서는:</b> %s</li></ol>'
            '<p class="nocode">코드와 수식을 몰라도 됩니다. 수식은 조수가 대신 묻고, 코드는 접어 두었어요.</p>%s</div>') % (what, why, work, ab)


def situ(text, mood='board'):
    """단계 시작 — 박사가 현장 질문 하나로 문을 연다(① 상황)."""
    return '<div class="situ">' + say('doc', mood, text) + '</div>'


def whymath(why, math=None):
    """why = (문제 상황, 앞 방법의 한계, 해법, 쉽게 말하면)
    math = dict(q=조수 질문, school=학교 수학 단원, rows=[(식 조각, 읽는 법, 뜻)], doc=박사 답, try_=숫자로 한 번, comment=조수 코멘트)"""
    w = ('<div class="why"><h4>왜 이 방법을 쓰나</h4><ol><li><b>문제 상황:</b> %s</li><li><b>앞 방법의 한계:</b> %s</li><li><b>해법:</b> %s</li></ol>'
         '<p class="easy"><b>쉽게 말하면</b> %s</p></div>') % why
    if not math:
        return '<div class="wm" style="grid-template-columns:1fr">%s</div>' % w
    rows = ''.join('<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>' % r for r in math['rows'])
    m = ('<div class="mq"><h4>수학 수식을 어려워하는 조수가 대신 물어봅니다</h4>' + say('asst', 'shock', math['q']) +
         '<span class="school">학교 수학으로 보면 · %s</span>' % math['school'] +
         (say('doc', 'front', math['doc']) if math.get('doc') else '') +
         '<table><tr><th>식 조각</th><th>읽는 법</th><th>뜻</th></tr>%s</table>' % rows +
         '<div class="try"><b>숫자로 한 번 해 보기</b><br>%s</div>' % math['try_'] +
         say('asst', 'spark', math['comment']) + '</div>')
    return '<div class="wm">%s%s</div>' % (w, m)


def stepchat(doc_q, robo, fly, asst):
    """실험 패널 바로 앞의 단계 대화: 박사 질문 · 주판봇 성급한 확신 · 초파리 의심과 '이걸 눌러 봐' · 조수 보고."""
    return ('<div class="stepchat"><b>실험 앞 대화</b>' + say('doc', 'think', doc_q) + say('robo', 'calc', robo)
            + say('fly', 'point', fly) + say('asst', 'report', asst) + '</div>')


def xbox(items, title='방청석 질문 — X1 · X2 · X3'):
    """items: [(x, mood, 질문, 답하는 이, 답 표정, 답)]"""
    h = ''
    for x, mood, q, who, am, a in items:
        h += say(x, mood, q, name=XNAME[x]) + say(who, am, a)
    return '<div class="xbox"><b>%s</b>%s</div>' % (title, h)


def again(who, text, mood=None):
    """인턴이 자기 말로 다시 말해 보기."""
    mood = mood or ('explain' if who == 'sia' else 'report')
    lab = '인턴 시아 · 제 말로 다시 해 보면' if who == 'sia' else '인턴 모아 · 기록장에 적은 한 줄'
    return '<div class="again">' + say(who, mood, text, name=lab) + '</div>'


def interp(text, calm=None):
    """⑦ 해석 문장 — '이 숫자는 업무에서 이런 뜻'. calm은 안심 신호."""
    c = '<p class="calm">박사: %s</p>' % calm if calm else ''
    return '<div class="interp">' + say('doc', 'magic', text, name='박사 · 업무에서는') + c + '</div>'


def recap(text):
    return '<div class="recap"><b>30초 복습</b> · %s</div>' % text


def aicheck(claim, checks, answer, title='AI 판단 코너 — 주판봇이 낸 결과, 그대로 믿어도 될까?'):
    lis = ''.join('<li>%s</li>' % c for c in checks)
    return ('<div class="aicheck"><h4>%s</h4>' % title + say('robo', 'happy', '<span class="claim" style="display:block">%s</span>' % claim, name='주판봇 · AI가 낸 결과')
            + say('doc', 'think', '바로 쓰기 전에 세 가지만 물어봅시다.') + '<ul>%s</ul>' % lis
            + '<details><summary>박사의 확인 결과 보기</summary>%s</details></div>' % say('doc', 'judge', answer))


def codefold(rows, title='원문의 코드로 보면 (몰라도 됩니다)'):
    """rows: [(코드 한 줄, 뜻 한 줄)]"""
    import html
    tr = ''.join('<tr><td><code>%s</code></td><td>%s</td></tr>' % (html.escape(c), m) for c, m in rows)
    return '<details class="codefold"><summary>%s</summary><table>%s</table></details>' % (title, tr)


def step(no, sid, title, tags, situation='', wm='', pair=None, chat='', panel='', explain='', extra='', after='', quiz=True):
    """비전공자판 단계 하나: 제목 → 상황 질문 → 왜/수식 상자 → 일상으로 치면|원문에서는 → 단계 대화 → 실험 → 풀이·한계 → 뒤 블록 → 퀴즈."""
    tg = ''.join('<span class="lvtag %s">%s</span>' % (c, t) for c, t in tags)
    pr = ''
    if pair:
        pr = ('<div class="pair"><div><span class="tag fly">%s</span><p>%s</p></div><div><span class="tag nn">%s</span><p>%s</p></div></div>'
              % pair)
    q = '<div class="quiz" data-quiz="%s"></div>' % sid if quiz else ''
    return ('<section class="level" id="%s"><div class="wrap"><div class="lvhead"><div class="hexno">%s<small>단계</small></div><div><h2>%s</h2><p class="sub">%s</p></div></div>'
            '%s%s%s%s%s%s%s%s%s</div></section>') % (sid, no, title, tg, situation, wm, pr, chat, panel, explain, extra, after, q)


def xroles(roles):
    """등장인물 아래 — 이번 편에서 앞자리로 나온 방청석 셋."""
    return ('<h3>이번 편은 방청석 셋이 앞자리에 앉았어요</h3><div class="xrole">%s</div>'
            % ''.join('<div class="c"><img data-who="%s" data-mood="e01" alt="" aria-hidden="true"><div><b>%s</b><span>%s</span></div></div>' % (x, XNAME[x], r) for x, r in roles))


def clean_terms(page):
    """사용자 용어 규칙: 결과물에 '칸'·'사다리'·'관통'을 쓰지 않는다 (공용 조각에 남은 말을 바꾼다)."""
    for a, b in [('이 칸의 한계', '이 단계의 한계'), ('나머지 칸은', '나머지 단계는'), ('<th>칸</th>', '<th>단계</th>'),
                 ('페이지 칸', '해설 단계'), ('그 칸으로', '그 단계로'), ('이 페이지의 칸', '이 페이지의 단계'), ('해설 칸', '해설 단계'),
                 ('핵심 칸', '핵심 단계'), ('천장 사다리', '천장 겹겹'), ('인스턴스 칸막이', '인스턴스 구획'), ('한 칸씩', '한 겹씩'), ('칸막이', '구획')]:
        page = page.replace(a, b)
    return page
