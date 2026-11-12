# -*- coding: utf-8 -*-
"""스터디 북 목차(index.html) 만들기. 사용: python3 build_index.py <저장소 루트>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab import *
from series import *

ROOT = sys.argv[1] if len(sys.argv) > 1 else '../..'

def status_of(it):
    f = os.path.join(ROOT, it['folder'], 'index.html')
    if it['status'] == 'kept':
        return 'kept' if os.path.exists(f) else 'plan'
    if it['status'] == 'plan':
        return 'plan'
    if os.path.exists(f) and 'ai-lab-explainer v1.12' in open(f, encoding='utf-8').read():
        return 'done'
    return 'wip'

for w in WEEKS:
    for it in w['items']:
        it['st'] = status_of(it)
done = sum(1 for w in WEEKS for it in w['items'] if it['st'] in ('done', 'kept'))
total = sum(len(w['items']) for w in WEEKS) + len(SPECIALS)

DIALOG = ''.join([
    say('doc', 'front', '어서 와요. 여기는 『Inference Engineering』을 10주 동안 읽으며 만든 <b>연구실 스터디 북</b>이에요. 오늘부터 한 권으로 묶어 둡니다.'),
    say('asst', 'smile', '주차마다 교재 해설 한 편, 논문 해설 한 편이 있어요. 모두 이 저장소 한곳에 모았어요.'),
    say('fly', 'point', '책 순서대로만 읽으면 돼? 3주차 교재편은 왜 표시가 달라?'),
    say('robo', 'chart', '3주차 교재편은 먼저 완성된 원본 그대로 보관했지. 나머지는 연구실 식구 전원이 나오는 새 판이야. 페이지 수로 치면 꽤 남는 장사지!'),
    say('sia', 'guide', '순서는 제가 정리했습니다. 아래 10주 지도에서 주차를 누르면 읽을 범위와 파일이 나와요.'),
    say('moa', 'tea', '읽고 나면 각 페이지 끝의 지식 색인에 기록이 모여요. 차 한 잔 하시면서 천천히 오세요!'),
])

def item_card(it):
    st = it['st']
    lab = STATUS_KO[st]
    cls = {'done': 'g', 'kept': 'p', 'wip': 'a', 'plan': ''}[st]
    if st in ('done', 'kept', 'wip'):
        link = '<a href="%s/">해설 열기 →</a>' % it['folder']
    else:
        link = '<span class="muted">폴더 예정: <code>%s/</code></span>' % it['folder']
    old = ''
    if it.get('old'):
        old = ' · <a href="%s%s" class="muted" style="font-size:12px">옛 저장소</a>' % (OLD, it['old'])
    kind = '교재' if it['kind'] == 'textbook' else '논문'
    return ('<div class="card bk %s"><span class="lvtag %s">%s · %s</span> <span class="lvtag">%s</span><h4>%s</h4><p class="muted" style="margin:0 0 6px;font-size:14px">%s</p>%s%s</div>'
            % (st, cls, kind, it['label'], lab, it['title'], it['range'], link, old))

weeks_html = ''
for w in WEEKS:
    weeks_html += ('<div class="wk" id="w%d"><div class="wkh"><span class="hexno sm">%d<small>주차</small></span><h3>%s</h3></div><div class="grid2">%s</div></div>'
                   % (w['no'], w['no'], w['title'], ''.join(item_card(it) for it in w['items'])))
spec_html = ''.join('<div class="card bk plan"><span class="lvtag">%s</span> <span class="lvtag">준비 중</span><h4>%s</h4><span class="muted">폴더 예정: <code>%s/</code></span></div>' % (s['label'], s['title'], s['folder']) for s in SPECIALS)

chap_html = ''.join('<details class="math"><summary><b>%d장 %s</b> · %s</summary><ul>%s</ul></details>' % (n, ko, en, ''.join('<li>%s</li>' % s for s in secs)) for n, en, ko, secs in CHAPTERS)

WEEK_JS = json.dumps([{'no': w['no'], 'title': w['title'], 'items': [{'label': it['label'], 'kind': it['kind'], 'title': it['title'], 'st': it['st'], 'folder': it['folder'], 'range': it['range']} for it in w['items']]} for w in WEEKS], ensure_ascii=False)

import factory
body = factory.index_section(ROOT) + '''
<header class="hero" id="top"><div class="wrap"><div class="hero-text">
<p class="eyebrow">INFERENCE STUDY BOOK · 2026 가을 · 10주 + 부록</p>
<h1>인퍼런스 스터디 북</h1>
<p class="q">AI 모델을 더 빠르고, 더 싸고, 더 안정적으로 돌리려면 무엇을 알아야 할까?</p>
<p>『Inference Engineering』(Philip Kiely, 2026)을 주차마다 교재 한 꼭지와 논문 한 편씩 읽고, 연구실 식구들이 진행하는 해설 페이지로 만들었습니다. 이 페이지는 그 해설들을 한 권으로 묶은 <b>표지이자 목차</b>입니다.</p>
<div class="kpis" id="heroKpis"></div>
<div class="dialog">''' + DIALOG + '''</div></div></div></header>
''' + crew({'doc': '해설·심판. 주차마다 핵심 한 줄을 정리', 'asst': '실험 진행·숫자 발표. 독자의 눈높이로 질문', 'fly': '의심하는 쪽. 한계와 다음 단계를 짚음', 'robo': '확신하는 쪽. 크고 많은 숫자를 좋아함',
            'sia': '순서 정리·진행 신호. 주차 지도 안내', 'moa': '기록 모으기·응원. 지식 색인과 꾸러미 소개', 'x1': '방청석 (…)', 'x2': '방청석 (반짝)', 'x3': '방청석 (짝짝)'},
           extra='<p class="muted" style="margin-top:12px">밑줄 친 말을 누르면 뜻이 나옵니다. 각 해설 페이지는 단일 HTML이라 설치 없이 브라우저에서 바로 열립니다.</p>') + '''
<section class="level" id="map"><div class="wrap"><div class="lvhead"><div class="hexno">1<small>지도</small></div><div><h2>10주 지도</h2><p class="sub"><span class="lvtag g">시아의 순서표</span><span class="lvtag p">주차를 누르면 아래에 나와요</span></p></div></div>
''' + say('sia', 'explain', '0장부터 7장까지, 큰 장은 둘로 나눴습니다. 2장은 2주차와 3주차, 5장은 6·7주차, 7장은 9·10주차예요. 장이 바뀌는 주차는 3장·4장·6장처럼 한 장씩 따로 만듭니다.') + '''
<div class="panel"><h3>주차를 고르세요</h3><div class="cwrap"><canvas id="cMap" class="wide" aria-label="10주 지도. 육각형 하나가 한 주차이고, 초록은 연구실판 완성, 파랑은 원본 그대로, 회색은 준비 중입니다."></canvas></div>
<div class="ctrl"><div class="group" id="wkBtns"></div></div><div id="wkOut" aria-live="polite"></div>
<div class="legend"><span><i style="background:#5ee39c"></i>연구실판 완성</span><span><i style="background:#82b8ff"></i>원본 그대로</span><span><i style="background:#f1b646"></i>다시 만드는 중</span><span><i style="background:#4a4e6a"></i>준비 중</span></div></div>
</div></section>
<section class="level" id="weeks"><div class="wrap"><div class="lvhead"><div class="hexno">2<small>목차</small></div><div><h2>주차별 목차</h2><p class="sub"><span class="lvtag g">교재 · 논문</span><span class="lvtag">폴더 = 옛 저장소 이름</span></p></div></div>
''' + say('asst', 'report', '옛 저장소 주소는 그대로 남겨 두고, 이제 이 저장소 안의 폴더가 정식 주소예요. 폴더 이름은 옛 저장소 이름에서 앞의 <code>inference_engineering_study_</code>만 뺀 것이에요.') + weeks_html + '''
</div></section>
<section class="level" id="special"><div class="wrap"><div class="lvhead"><div class="hexno">3<small>부록</small></div><div><h2>부록 · 특별편</h2><p class="sub"><span class="lvtag">2~3편 예정</span></p></div></div>
''' + say('fly', 'point', '부록은 주제가 아직 안 정해졌어. 정해지면 <code>special_01/</code>부터 채우는 거지?') + '<div class="grid3">' + spec_html + '''</div></div></section>
<section class="level" id="book"><div class="wrap"><div class="lvhead"><div class="hexno">4<small>책</small></div><div><h2>책 지도 — 여덟 개의 장</h2><p class="sub"><span class="lvtag p">출판사 공개 목차</span></p></div></div>
''' + say('robo', 'calc', '장은 0부터 7까지 여덟 개. 장을 펼치면 절 제목이 나와. 원문은 출판사 누리집에서 무료로 읽을 수 있어.') + chap_html + '''
<p class="muted">원문: Kiely, P. (2026). <i>Inference Engineering</i>. Baseten Books. <a href="https://www.baseten.co/inference-engineering/">출판사 누리집</a></p></div></section>
<section class="level" id="how"><div class="wrap"><div class="lvhead"><div class="hexno">5<small>사용법</small></div><div><h2>스터디 북 읽는 법</h2></div></div>
<div class="steps"><div><h4>① 교재편 먼저</h4><p>교재 해설은 개념 사다리를 한 칸씩 올라가요. 칸마다 직접 만지는 시뮬레이션과 확인 퀴즈가 있어요.</p></div>
<div><h4>② 논문편으로 확인</h4><p>같은 주차의 논문 해설은 교재 개념이 실제 연구에서 어떻게 쓰였는지 보여 줘요. 원문 수치에는 <span class="chip-src">원문</span> 칩이 붙어요.</p></div>
<div><h4>③ 끝에서 정리</h4><p>페이지 끝의 지식 색인에서 개념을 찾고, 온톨로지·서지 꾸러미를 ZIP으로 받을 수 있어요.</p></div></div>
''' + say('moa', 'report', '정확성 표시도 기억해 주세요. 노란 도장이 찍힌 그림은 설명용 모형이고, 파란 <span class="chip-src">원문</span> 칩은 교재·논문 수치 그대로예요.') + '''
<div class="explain"><h4>저장소 구조</h4><ul>
<li><code>index.html</code> — 이 목차 (스터디 북 표지)</li>
<li><code>week_{주차}_textbook_{장·범위}/</code> — 교재 해설 (예: <code>week_01_textbook_ch00/</code>)</li>
<li><code>week_{주차}_article_{번호}/</code> — 논문 해설</li>
<li><code>special_{번호}/</code> — 부록·특별편</li>
<li><code>tools/lab_build/</code> — 페이지를 만드는 공용 틀 (연구실 해설 스킬 v1.12 규격)</li></ul></div>
</div></section>
'''

KGN = []; KGE = []
P = 'index'
KGN.append(node('lab:question/inference-core', 'Question', 'AI 모델을 더 빠르고 싸고 안정적으로 돌리려면?', 'How to serve AI models faster, cheaper, more reliably?', '#top', P))
KGN.append(node('lab:work/kiely2026inference', 'Work', 'Kiely (2026) Inference Engineering', 'Kiely 2026', '#book', P, src=('kiely2026inference', '목차')))
for n, en, ko, secs in CHAPTERS:
    KGN.append(node('lab:concept/ie-ch%d' % n, 'Concept', '%d장 %s' % (n, ko), 'Chapter %d %s' % (n, en), '#book', P, defi=', '.join(secs), src=('kiely2026inference', 'Chapter %d' % n)))
    KGE.append(edge('lab:concept/ie-ch%d' % n, 'partOf', 'lab:work/kiely2026inference', '#book'))
    if n: KGE.append(edge('lab:concept/ie-ch%d' % (n - 1), 'prerequisiteOf', 'lab:concept/ie-ch%d' % n, '#book'))
PAPERS = [('livebench', 'White 외 (2025) LiveBench', 'White et al. 2025', 1), ('transformer', 'Vaswani 외 (2017) 트랜스포머', 'Vaswani et al. 2017', 2), ('flashattention', 'Dao 외 (2022) FlashAttention', 'Dao et al. 2022', 2)]
for slug, ko, en, ch in PAPERS:
    KGN.append(node('lab:work/' + slug, 'Work', ko, en, '#weeks', P))
    KGE.append(edge('lab:work/' + slug, 'relatedTo', 'lab:concept/ie-ch%d' % ch, '#weeks'))
KG = {'version': '1.0', 'page': 'index', 'nodes': KGN, 'edges': KGE}
REFS = [book_ref(),
        ref('white2025livebench', 'paper-conference', 'LiveBench: A Challenging, Contamination-Limited LLM Benchmark', ['Colin White', 'Samuel Dooley', 'Manley Roberts', 'Arka Pal', 'et al.'], 2025, 'ICLR 2025', 'https://arxiv.org/abs/2406.19314'),
        ref('vaswani2017attention', 'paper-conference', 'Attention Is All You Need', ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar', 'et al.'], 2017, 'NeurIPS 2017', 'https://arxiv.org/abs/1706.03762'),
        ref('dao2022flashattention', 'paper-conference', 'FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness', ['Tri Dao', 'Daniel Y. Fu', 'Stefano Ermon', 'Atri Rudra', 'Christopher Ré'], 2022, 'NeurIPS 2022', 'https://arxiv.org/abs/2205.14135')]
META = {'title': '인퍼런스 스터디 북 — 연구실 식구들과 읽는 『Inference Engineering』', 'description': '『Inference Engineering』 10주 스터디를 연구실 해설 페이지로 묶은 스터디 북 — 표지는 한 층이 한 주차인 3D GPU 추론 공장',
        'series': '인퍼런스 스터디 북', 'number': '00', 'slug': 'index', 'version': '1.0', 'date': '2026-11-11', 'creator': ['안상선'], 'license': 'CC BY-NC 4.0 (캐릭터 제외)',
        'url': BASE, 'image': BASE + 'cover_factory.jpg', 'kgStart': 'lab:concept/ie-ch0', 'citeKey': 'ahn2026inferencebook',
        'suggestedCitation': '안상선 (2026). 인퍼런스 스터디 북 — 연구실 식구들과 읽는 『Inference Engineering』. ' + BASE}
JS = r'''
var W=%s,COL={done:'#5ee39c',kept:'#82b8ff',wip:'#f1b646',plan:'#4a4e6a'},ST={done:'연구실판 완성',kept:'원본 그대로',wip:'다시 만드는 중',plan:'준비 중'};
var all=[];W.forEach(function(w){w.items.forEach(function(i){all.push(i)})});
var ok=all.filter(function(i){return i.st==='done'||i.st==='kept'}).length;
L.kpis('#heroKpis',[[10,'주차','g'],[all.length,'해설 칸 (교재·논문)','m'],[ok,'지금 열 수 있는 해설','i'],['2~3','부록 예정','a']]);
var sel=0,c=$('#cMap'),t=0;
$('#wkBtns').innerHTML=W.map(function(w,i){return '<button class="bt" data-w="'+i+'" aria-pressed="'+(i===0)+'">'+w.no+'주차</button>'}).join('');
$$('#wkBtns [data-w]').forEach(function(b){b.addEventListener('click',function(){pick(+b.dataset.w)})});
function pick(i){sel=i;$$('#wkBtns [data-w]').forEach(function(x){x.setAttribute('aria-pressed',+x.dataset.w===i?'true':'false')});var w=W[i];
  $('#wkOut').innerHTML='<p><b>'+w.no+'주차 · '+w.title+'</b></p>'+w.items.map(function(it){var on=it.st!=='plan';return '<p style="margin:4px 0"><span class="lvtag">'+(it.kind==='textbook'?'교재':'논문')+' · '+it.label+'</span> '+(on?'<a href="'+it.folder+'/">'+it.title+'</a>':it.title)+' <span class="muted" style="font-size:13px">'+it.range+' · '+ST[it.st]+'</span></p>'}).join('');draw(0);}
function draw(dt){t+=dt;var Wd=L.fit(c,220),x=c.getContext('2d');x.clearRect(0,0,Wd,220);L.grid(x,Wd,220);
  var n=W.length,pad=46,step=(Wd-pad*2)/(n-1);x.strokeStyle='#363a52';x.lineWidth=3;x.beginPath();x.moveTo(pad,110);x.lineTo(Wd-pad,110);x.stroke();x.lineWidth=1;
  W.forEach(function(w,i){var cx=pad+i*step,cy=110+(i%%2?-26:26),r=24+(i===sel?4+Math.sin(t*4)*1.5:0);
    x.beginPath();for(var k=0;k<6;k++){var a=Math.PI/3*k-Math.PI/2;x.lineTo(cx+r*Math.cos(a),cy+r*Math.sin(a));}x.closePath();
    var s=w.items.map(function(i){return i.st});var col=s.every(function(v){return v==='plan'})?COL.plan:s.indexOf('wip')>=0?COL.wip:s.some(function(v){return v==='plan'})?COL.wip:s.indexOf('kept')>=0?COL.kept:COL.done;
    if(s.every(function(v){return v==='done'||v==='kept'}))col=s.indexOf('kept')>=0?COL.kept:COL.done;
    x.fillStyle=col;x.globalAlpha=i===sel?1:.75;x.fill();x.globalAlpha=1;if(i===sel){x.strokeStyle='#eceaf3';x.lineWidth=2;x.stroke();x.lineWidth=1;}
    x.fillStyle='#10241a';x.font='700 15px '+L.FONT;x.textAlign='center';x.fillText(w.no,cx,cy+5);
    x.fillStyle='#9d9bb8';x.font='11px '+L.FONT;x.fillText(w.items.map(function(i){return i.label}).join(' · ').slice(0,14),cx,cy+(i%%2?-36:44));});
  x.fillStyle='#9d9bb8';x.font='12px '+L.FONT;x.textAlign='left';x.fillText('시작',8,114);x.textAlign='right';x.fillText('부록',Wd-6,114);}
c.addEventListener('pointerdown',function(e){var r=c.getBoundingClientRect(),mx=e.clientX-r.left,n=W.length,pad=46,step=(r.width-pad*2)/(n-1);var i=Math.round((mx-pad)/step);if(i>=0&&i<n)pick(i);});
L.addMod(c,draw);pick(0);
''' % WEEK_JS

CSS = '''.wk{margin:20px 0 28px}.wkh{display:flex;gap:12px;align-items:center;margin-bottom:8px}.wkh h3{margin:0}
.hexno.sm{width:46px;height:52px;font-size:18px}.card.bk h4{margin:8px 0 2px}.card.bk.plan{opacity:.72}.card.bk.kept{border-color:rgba(130,184,255,.45)}.card.bk.done{border-color:rgba(94,227,156,.45)}
code{font-size:.92em;background:var(--panel2);border-radius:5px;padding:0 5px}'''

spec = {'meta': META, 'kg': KG, 'refs': REFS, 'body': body, 'css': CSS, 'js': JS,
        'nav': nav([('factory', '공장'), ('map', '10주 지도'), ('weeks', '주차별 목차'), ('special', '부록'), ('book', '책 지도'), ('how', '읽는 법'), ('kg', '지식 색인'), ('export', '꾸러미')], home='#top', home_label='인퍼런스 스터디 북'),
        'gl': {'추론': ['추론 (inference)', '개념', '이미 학습을 마친 모델에 입력을 넣어 결과를 얻는 일. 학습(training)과 구분한다.'],
               '지연시간': ['지연시간 (latency)', '지표', '요청 하나가 답을 받기까지 걸리는 시간.'],
               '처리량': ['처리량 (throughput)', '지표', '일정 시간 동안 처리하는 요청·토큰의 양.'],
               '지식 색인': ['지식 색인', '페이지 구성', '페이지에 나온 개념·방법·주장을 검색하고 관계를 보는 칸.'],
               '시뮬레이션': ['시뮬레이션', '페이지 구성', '숫자를 바꿔 결과가 어떻게 달라지는지 직접 보는 장치. 노란 도장은 설명용 모형.'],
               '온톨로지': ['온톨로지 (ontology)', '용어', '개념과 개념 사이의 관계를 기계가 읽을 수 있게 정리한 것.']},
        'core': ['추론', '지연시간', '처리량', '지식 색인', '시뮬레이션', '온톨로지'],
        'quiz': {},
        'footer': footer([('교재', 'Kiely, P. (2026). Inference Engineering. Baseten Books.'), ('주차 구성', 'Inference Korea 추론 엔지니어링 스터디 10주 범위 (책 장 기준)'),
                          ('캐릭터 그림', 'adminmrobo/fruitfly-lab-expressions → ahnboat_lab_explainer 캐릭터 팩 1.4')],
                         ['10주 지도의 색은 이 저장소 폴더 상태를 빌드할 때 읽어 칠한 것입니다.', '4주차 이후 논문 제목은 예정이며 바뀔 수 있습니다.'])}
spec['footer'] = spec['footer'].replace('<a href="../index.html">스터디 북 목차</a>', '<a href="#top">맨 위로</a>')
n = build(spec, os.path.join(ROOT, 'index.html'))
print('index.html', n, 'bytes', done, '/', total)
