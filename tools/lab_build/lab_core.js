/* 연구실 해설 공용 모듈 (ai-lab-explainer v1.12 규격 · 식구 6명 + 미공개 3) */
(function(){
'use strict';
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,r){return (r||document).querySelector(s)}
function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function fit(c,h){var d=window.devicePixelRatio||1,w=c.clientWidth||c.parentElement.clientWidth||600;
  if(c.width!==Math.round(w*d)||c.height!==Math.round(h*d)){c.width=Math.round(w*d);c.height=Math.round(h*d);c.style.height=h+'px';}
  var x=c.getContext('2d');x.setTransform(d,0,0,d,0,0);return w;}
function stamp(ctx,W,txt){ctx.save();ctx.font='700 11px "IBM Plex Sans KR",system-ui,sans-serif';
  var tw=ctx.measureText(txt).width+16,x=W-tw-8,y=8;ctx.fillStyle='rgba(241,182,70,.14)';ctx.strokeStyle='rgba(241,182,70,.7)';
  ctx.beginPath();if(ctx.roundRect)ctx.roundRect(x,y,tw,20,10);else ctx.rect(x,y,tw,20);ctx.fill();ctx.stroke();
  ctx.fillStyle='#f1b646';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillText(txt,x+8,y+14);ctx.restore();}
function grid(ctx,W,H){ctx.save();ctx.strokeStyle='rgba(157,155,184,.06)';ctx.lineWidth=1;for(var x=0;x<W;x+=24){ctx.beginPath();ctx.moveTo(x+.5,0);ctx.lineTo(x+.5,H);ctx.stroke();}for(var y=0;y<H;y+=24){ctx.beginPath();ctx.moveTo(0,y+.5);ctx.lineTo(W,y+.5);ctx.stroke();}ctx.restore();}
var FONT='"IBM Plex Sans KR",system-ui,sans-serif';
var C={text:'#eceaf3',muted:'#9d9bb8',rule:'#363a52',stain:'#d672d6',gfp:'#5ee39c',eye:'#f0604d',amber:'#f1b646',info:'#82b8ff',panel:'#1c1e2d',panel2:'#25283a',fly:'#ef5b5b',robo:'#57d0dc',doc:'#b07cff',asst:'#ff86b8',sia:'#b9c2d6',moa:'#e7b47c'};
function fmt(n,d){if(d!=null)return Number(n).toFixed(d);if(n>=1e12)return (n/1e12).toFixed(2)+'T';if(n>=1e9)return (n/1e9).toFixed(2)+'G';if(n>=1e6)return (n/1e6).toFixed(2)+'M';if(n>=1e3)return (n/1e3).toFixed(1)+'K';return String(Math.round(n*100)/100);}
function setTxt(el,t){if(typeof el==='string')el=$(el);if(el)el.textContent=t}
function kpis(el,arr){if(typeof el==='string')el=$(el);if(!el)return;el.innerHTML=arr.map(function(k){return '<div class="kpi '+k[2]+'"><b>'+k[0]+'</b><span>'+k[1]+'</span></div>'}).join('');}
function ins(el,arr){if(typeof el==='string')el=$(el);if(!el)return;el.innerHTML=arr.map(function(p){return '<p class="'+p[0]+'">'+p[1]+'</p>'}).join('');}
function bindSeg(sel,fn){$$(sel+' [data-v]').forEach(function(b){b.addEventListener('click',function(){$$(sel+' [data-v]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});fn(b.dataset.v,b);});});}

/* ---------- 캐릭터 ---------- */
var PAL={K:'#1d1a22',W:'#eceaf3',R:'#e04a3a',r:'#a8281c',U:'#3a6fd8',Y:'#f1c84a',L:'#5a4636',B:'#4aa3ff',F:'#f2c9a0',G:'#9fb4d0',P:'#ff86b8',N:'#2b3a7a',V:'#b9a6e8',E:'#eadfc6',D:'#17352c',M:'#5befa5',A:'#8b5a2b',Q:'#d2603c',H:'#9c978c'};
var MAPS={
fly:['....K......K....','.....K....K.....','....UUUUUUUU....','...UUYUUUUYUU...','..RRRUUUUUURRR..','.RRrRRKKKKRRrRR.','.RRRRKKKKKKRRRR.','..RRKKKKKKKKRR..','WW..WKKKKKKW..WW','WWW.WWKKKKWW.WWW','.WWWWWKKKKWWWWW.','..L.WWKKKKWW.L..','.L...WKKKKW...L.','L.....KKKK.....L','.......KK.......','................'],
robo:['.......Q........','.......K........','..KKKKKKKKKKKK..','..KEEEEEEEEEEK..','..KEDDDDDDDDEK..','..KEDMDDDDMDEK..','..KEDDDDDDDDEK..','..KEDMDDDDMDEK..','..KEDDMMMMDDEK..','.HKEEEEEEEEEEKH.','HHAAAAAAAAAAAAHH','HHAEQEQEEQEQEAHH','..AAAAAAAAAAAA..','..AEQEQEEQEQEA..','..AAAAAAAAAAAA..','.KKKK......KKKK.'],
doc:['....KKKKKKK.....','...KKKWKKKKK....','..KKKWWKKKKKK...','..KFFFFFFFFFK...','..FGGFFFFGGFF...','..FGKFFFFGKFF...','..FFFFFFFFFFF...','...FFFRRRFFF....','....FFFFFFF.....','...WWWKKKWWW....','..WWWWKRKWWWW...','..WWWWKRKWWWW...','..WFWWKKKWWFW...','..WWWWKKKWWWW...','...LL.....LL....','...KK.....KK....'],
asst:['.PP..........PP.','.PP..PPPPPP..PP.','PPPPPPPPPPNPPPPP','.PPPPFFFFFFPPPP.','..PPFFFFFFFFPP..','..PFFBFFFFBFFP..','..PFFBFFFFBFFP..','..PFFFFFFFFFFP..','...FFFFRRFFFF...','....FFFFFFFF....','...WWVVVVVVWW...','..WWWVVVVVVWWW..','..WWWVVVVVVWWW..','..WFWVVVVVVWFW..','...NN......NN...','...NN......NN...']};
var DEF={doc:'front',asst:'smile',fly:'clip',robo:'smile',sia:'smile',moa:'smile',x1:'hint',x2:'hint',x3:'hint'};
var pxCache={};
function pixel(who){if(pxCache[who])return pxCache[who];var cv=document.createElement('canvas');cv.width=64;cv.height=64;var c=cv.getContext('2d');
  if(MAPS[who]){MAPS[who].forEach(function(r,y){r.split('').forEach(function(ch,x){if(ch==='.')return;c.fillStyle=PAL[ch];c.fillRect(x*4,y*4,4,4);});});}
  else{var col={sia:'#2a2733',moa:'#c9b08e'}[who]||'#1f1d33';c.fillStyle=col;c.beginPath();c.arc(32,24,14,0,7);c.fill();c.fillRect(18,36,28,24);c.fillStyle='#fff';c.fillRect(25,22,4,4);c.fillRect(35,22,4,4);}
  return pxCache[who]=cv.toDataURL();}
function src(who,mood,big){var S=big?Object.assign({},window.SPRITE||{},window.SPRITE_BIG||{}):(window.SPRITE||{}),A=window.SPRITE_ALIAS||{};var k=who+'_'+mood;
  if(S[k])return S[k];if(A[k]&&S[A[k]])return S[A[k]];var dk=who+'_'+DEF[who];if(S[dk])return S[dk];if(A[dk]&&S[A[dk]])return S[A[dk]];return pixel(who);}
var Cast={fill:function(root){$$('img[data-who]',root).forEach(function(i){i.src=src(i.dataset.who,i.dataset.mood||DEF[i.dataset.who],i.hasAttribute('data-big'));i.decoding='async';});},
  set:function(img,who,mood){if(!img)return;img.dataset.mood=mood;var bg=img.hasAttribute('data-big');if(reduce){img.src=src(who,mood,bg);return;}img.style.transition='opacity .2s';img.style.opacity=0;setTimeout(function(){img.src=src(who,mood,bg);img.style.opacity=1;},200);}};
Cast.fill();
/* 미공개 식구: 버튼을 눌러야 보인다 (캐릭터 팩 C9) */
$$('[data-reveal]').forEach(function(b){b.addEventListener('click',function(){var box=document.getElementById(b.dataset.reveal);if(!box)return;var on=!box.classList.contains('open');box.classList.toggle('open',on);b.setAttribute('aria-expanded',on?'true':'false');b.textContent=on?(b.dataset.off||'다시 숨기기'):(b.dataset.on||b.textContent);});});

/* ---------- 애니메이션 루프 ---------- */
var mods=[],vis=new Set();
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target);});},{rootMargin:'100px'}):null;
function addMod(el,fn){if(!el)return;mods.push({el:el,fn:fn});if(io)io.observe(el);else vis.add(el);}
var last=0;function loop(ts){var dt=last?Math.min(0.05,(ts-last)/1000):0.016;last=ts;mods.forEach(function(m){if(vis.has(m.el))m.fn(reduce?0:dt);});requestAnimationFrame(loop);}
function drawAll(){mods.forEach(function(m){m.fn(0);});}

/* ---------- 대결 (6장) ---------- */
function Duel(cfg){var root=$(cfg.el||'#duelBox');if(!root)return;var shown=false,guess=null,flyImg=$('.head img[data-who=fly]',root),roboImg=$('.head img[data-who=robo]',root);
  var siaImg=$('.signal img[data-who=sia]',root),moaImg=$('.cheer img[data-who=moa]',root);
  $$('[data-guess]',root).forEach(function(b){b.addEventListener('click',function(){guess=b.dataset.guess;$$('[data-guess]',root).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});});});
  function bar(cls,nm,v,mx){return '<div class="bar '+cls+'"><span>'+nm+'</span><div class="track"><div class="fill" data-w="'+(Math.max(0,v)/mx*100).toFixed(1)+'"></div></div><span class="num">'+cfg.fmt(v)+'</span></div>';}
  $('.reveal',root).addEventListener('click',function(){var btn=this;
    if(shown){Cast.set(flyImg,'fly','point');Cast.set(roboImg,'robo','coin');if(siaImg)Cast.set(siaImg,'sia','signal');if(moaImg)Cast.set(moaImg,'moa','cheer');root.classList.remove('open');shown=false;btn.textContent='결과 보기';return;}
    var r=cfg.run(),mx=Math.max(r.fly,r.robo)||1;
    $('.bars',root).innerHTML=(r.bars||[['f','초파리',r.fly],['r','주판봇',r.robo]]).map(function(b){return bar(b[0],b[1],b[2],mx)}).join('');
    setTimeout(function(){$$('.fill',root).forEach(function(e){e.style.width=e.dataset.w+'%';});},30);
    var gap=Math.abs(r.fly-r.robo)/(mx||1);
    var M={F:['arms','sigh','proud','cheer'],R:[gap>=0.10?'cry':'coffee','happy','proud','cheer'],D:['coffee','meh','think','smile'],C:['coffee','calc','think','think'],X:['arms','blush','stop','shock']}[r.res];
    Cast.set(flyImg,'fly',M[0]);Cast.set(roboImg,'robo',M[1]);if(siaImg)Cast.set(siaImg,'sia',r.res==='X'?'stop':'signal');if(moaImg)Cast.set(moaImg,'moa',M[3]);
    setTxt($('.asst p',root),r.asst);setTxt($('.verdict p',root),r.verdict);
    var vimg=$('.verdict img[data-who=doc]',root);if(vimg)Cast.set(vimg,'doc',r.res==='C'||r.res==='D'?'think':'judge');
    setTxt($('.duelNote',root),(r.note||'')+(guess?(' 내 예측: '+(guess==='fly'?'초파리':'주판봇')+' → '+(((guess==='fly')&&r.res==='F')||((guess==='robo')&&r.res==='R')?'맞음!':(r.res==='C'||r.res==='D')?'조건에 따라 갈림':'빗나감')):''));
    setTxt($('.duelScore',root),{F:'F · 초파리 승',R:'R · 주판봇 승',D:'D · 무승부',C:'C · 조건부',X:'X · 주판봇 실격'}[r.res]);
    root.classList.add('open');shown=true;btn.textContent='다시 닫기';});}

/* ---------- 용어 사전 ---------- */
var GL=window.GL||{},CORE=window.CORE||[];
var GMODE='core',tip=$('#tip');
function glossWrap(){$$('.jt').forEach(function(s){s.replaceWith(document.createTextNode(s.textContent));});document.body.normalize&&document.body.normalize();
  if(GMODE==='off')return;var keys=(GMODE==='core'?CORE:Object.keys(GL).filter(function(k){return k.length>1})).filter(function(k){return GL[k]}).slice().sort(function(a,b){return b.length-a.length});
  $$('header.hero, section.level:not(#kg):not(#export), footer').forEach(function(sec){var seen={};
    var w=document.createTreeWalker(sec,NodeFilter.SHOW_TEXT,{acceptNode:function(n){var p=n.parentNode;while(p&&p!==sec){var t=p.nodeName;if(/^(BUTTON|H1|H2|H3|CANVAS|SVG|SCRIPT|STYLE|A|TH|SUMMARY|B)$/i.test(t)||(p.classList&&(p.classList.contains('kpis')||p.classList.contains('jt')||p.classList.contains('eq')||p.classList.contains('quiz')||p.classList.contains('insight')||p.classList.contains('nojt'))))return NodeFilter.FILTER_REJECT;p=p.parentNode;}return NodeFilter.FILTER_ACCEPT;}});
    var nodes=[];while(w.nextNode())nodes.push(w.currentNode);
    nodes.forEach(function(n){var t=n.nodeValue;for(var i=0;i<keys.length;i++){var k=keys[i];if(seen[k])continue;var idx=t.indexOf(k);if(idx<0)continue;seen[k]=1;
      var a=n.splitText(idx);a.splitText(k.length);var s=document.createElement('span');s.className='jt';s.tabIndex=0;s.dataset.k=k;s.textContent=k;a.parentNode.replaceChild(s,a);break;}});});}
function showTip(el){var g=GL[el.dataset.k];if(!g||!tip)return;tip.innerHTML='<b>'+g[0]+'</b><span class="k">'+g[1]+'</span><div>'+g[2]+'</div>';tip.style.display='block';var r=el.getBoundingClientRect(),tw=Math.min(300,window.innerWidth-16);tip.style.maxWidth=tw+'px';
  var left=Math.max(8,Math.min(window.innerWidth-tw-8,r.left));tip.style.left=left+'px';var top=r.bottom+8;if(top+140>window.innerHeight)top=r.top-tip.offsetHeight-8;tip.style.top=top+'px';}
function hideTip(){if(tip)tip.style.display='none';}
document.addEventListener('pointerover',function(e){var j=e.target.closest&&e.target.closest('.jt');if(j&&e.pointerType==='mouse')showTip(j);});
document.addEventListener('pointerout',function(e){if(e.target.closest&&e.target.closest('.jt')&&e.pointerType==='mouse')hideTip();});
document.addEventListener('click',function(e){var j=e.target.closest&&e.target.closest('.jt');if(j){tip.style.display==='block'&&tip.dataset.k===j.dataset.k?hideTip():(showTip(j),tip.dataset.k=j.dataset.k);}else if(!(e.target.closest&&e.target.closest('#tip')))hideTip();});
document.addEventListener('focusin',function(e){if(e.target.classList&&e.target.classList.contains('jt'))showTip(e.target);});
document.addEventListener('focusout',function(e){if(e.target.classList&&e.target.classList.contains('jt'))hideTip();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')hideTip();});
window.addEventListener('scroll',hideTip,{passive:true});

/* ---------- 퀴즈 · 학습 도우미 ---------- */
var QUIZ=window.QUIZ||{};var qTotal=0,qOk={};Object.keys(QUIZ).forEach(function(k){qTotal+=QUIZ[k].length;});
$$('.quiz[data-quiz]').forEach(function(box){var arr=QUIZ[box.dataset.quiz]||[];arr.forEach(function(it,qi){var d=document.createElement('div');d.className='qi';var id=box.dataset.quiz+qi;
  d.innerHTML='<p class="qq">'+it.q+'</p><div class="opts">'+it.o.map(function(o,i){return '<button class="bt" data-i="'+i+'">'+o+'</button>'}).join('')+'</div><p class="fb" aria-live="polite"></p>';
  $$('button',d).forEach(function(b){b.addEventListener('click',function(){var i=+b.dataset.i,fb=$('.fb',d);$$('button',d).forEach(function(x){x.classList.remove('right','wrongp')});
    if(i===it.a){b.classList.add('right');fb.className='fb ok';fb.textContent=it.why;qOk[id]=1;}else{b.classList.add('wrongp');fb.className='fb no';fb.textContent='힌트: '+it.hint;}studyUpd();});});box.appendChild(d);});});
function studyUpd(){var h=document.documentElement,p=Math.round(100*h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight));p=Math.min(100,Math.max(0,p));setTxt('#stRead','읽은 곳 '+p+'%');setTxt('#stQuiz','퀴즈 '+Object.keys(qOk).length+'/'+qTotal);var pr=$('#prog');if(pr)pr.style.width=p+'%';}
window.addEventListener('scroll',studyUpd,{passive:true});
var stm=$('#stMode');if(stm)stm.addEventListener('click',function(){GMODE=GMODE==='core'?'all':GMODE==='all'?'off':'core';this.textContent='밑줄: '+({core:'핵심',all:'전체',off:'끄기'})[GMODE];glossWrap();});

/* ---------- 지식 색인 (O1) ---------- */
var KG={nodes:[],edges:[]},REF=[],META={};
try{KG=JSON.parse($('#kg-raw').textContent);REF=JSON.parse($('#refs-csl').textContent);META=JSON.parse($('#page-meta').textContent);}catch(e){}
var TYC={Concept:'#5ee39c',Method:'#d672d6',Task:'#82b8ff',Metric:'#f1b646',Dataset:'#c48a5a',Claim:'#9ab8ff',Work:'#9d9bb8',Term:'#eceaf3',Analogy:'#f0604d',Question:'#ff86b8',Limitation:'#ef5b5b',Simulation:'#57d0dc',QuizItem:'#6b6f8f',Section:'#6b6f8f'};
var TYK={Concept:'개념',Method:'방법',Task:'문제',Metric:'지표',Dataset:'데이터',Claim:'주장',Work:'문헌',Term:'용어',Analogy:'비유',Question:'질문',Limitation:'한계',Simulation:'시뮬레이션',QuizItem:'퀴즈',Section:'섹션'};
var CHIPS=['Concept','Method','Limitation','Metric','Claim','Analogy','Question','Task','Work'];var kgOn={};CHIPS.forEach(function(c){kgOn[c]=true;});
var nodeById={};KG.nodes.forEach(function(n){nodeById[n.id]=n;});
var deg={};KG.edges.forEach(function(e){deg[e.s]=(deg[e.s]||0)+1;deg[e.o]=(deg[e.o]||0)+1;});
var kgHL=null,cKG=$('#cKG'),gN=[],gIdx={},gP=[],gScr=[];
function kgRender(){var q=($('#kgQ').value||'').trim().toLowerCase();var list=KG.nodes.filter(function(n){if(CHIPS.indexOf(n.type)<0||!kgOn[n.type])return false;if(!q)return true;
  var hay=[n.label.ko,n.label.en,(n.altLabel&&n.altLabel.ko||[]).join(' '),(n.altLabel&&n.altLabel.en||[]).join(' '),n.definition&&n.definition.ko||''].join(' ').toLowerCase();return hay.indexOf(q)>=0;});
  $('#kgList').innerHTML=list.map(function(n){return '<div class="kgitem'+(kgHL===n.id?' hl':'')+'" id="ki-'+n.id.replace(/[^a-z0-9]/gi,'_')+'"><b>'+n.label.ko+'</b><span class="ty" style="color:'+TYC[n.type]+';border:1px solid '+TYC[n.type]+'">'+TYK[n.type]+'</span><span class="muted" style="font-size:13px">'+n.label.en+'</span>'+(n.definition?'<p>'+n.definition.ko+'</p>':'')+'<a href="'+n.anchor+'">설명 보러 가기 →</a> <span class="muted" style="font-size:12px">근거 '+((n.evidence||[]).length)+' · 관계 '+(deg[n.id]||0)+'</span></div>';}).join('')||'<p class="muted">찾는 항목이 없어요.</p>';}
function drawKG(){if(!cKG)return;var W=fit(cKG,380),H=380,x=cKG.getContext('2d');x.clearRect(0,0,W,H);grid(x,W,H);var px=function(p){return [W/2+p.x*(W/2-24),H/2+p.y*(H/2-24)];};gScr=[];
  KG.edges.forEach(function(e){var a=gIdx[e.s],b=gIdx[e.o];if(a==null||b==null)return;if(!kgOn[gN[a].type]||!kgOn[gN[b].type])return;var A=px(gP[a]),B=px(gP[b]);x.strokeStyle=e.p==='lab:prerequisiteOf'?'rgba(94,227,156,.45)':e.p==='lab:hasLimitation'||e.p==='lab:addressedBy'?'rgba(240,96,77,.45)':'rgba(157,155,184,.22)';x.beginPath();x.moveTo(A[0],A[1]);x.lineTo(B[0],B[1]);x.stroke();});
  gN.forEach(function(n,i){if(!kgOn[n.type])return;var P=px(gP[i]),r=3+Math.min(6,(deg[n.id]||0)*0.7);x.fillStyle=TYC[n.type];x.globalAlpha=kgHL&&kgHL!==n.id?.5:1;x.beginPath();x.arc(P[0],P[1],r,0,7);x.fill();x.globalAlpha=1;gScr.push([P[0],P[1],r+4,n.id]);
    if((deg[n.id]||0)>=4||kgHL===n.id){x.fillStyle=C.text;x.font='11px '+FONT;x.textAlign='center';x.fillText(n.label.ko,P[0],P[1]-r-3);}});}
if($('#kgList')){
  (function(){var byT={};KG.nodes.forEach(function(n){byT[n.type]=(byT[n.type]||0)+1;});var ver=KG.nodes.filter(function(n){return (n.match||[]).some(function(m){return m.verified})}).length;
   kpis('#kgStats',[[KG.nodes.length,'노드','g'],[KG.edges.length,'관계','m'],[(byT.Concept||0)+(byT.Method||0),'개념·방법','i'],[byT.Claim||0,'주장 (출처 있음)','a']]);})();
  $('#kgChips').innerHTML=CHIPS.map(function(c){return '<button class="chip" data-ty="'+c+'" aria-pressed="true" style="border-left:3px solid '+TYC[c]+'">'+TYK[c]+'</button>';}).join('');
  $('#kgLegend').innerHTML=CHIPS.map(function(c){return '<span><i style="background:'+TYC[c]+'"></i>'+TYK[c]+'</span>';}).join('');
  $('#kgQ').addEventListener('input',kgRender);
  $$('#kgChips .chip').forEach(function(b){b.addEventListener('click',function(){var t=b.dataset.ty;kgOn[t]=!kgOn[t];b.setAttribute('aria-pressed',kgOn[t]?'true':'false');kgRender();drawKG();});});
  (function(){var chain=[],cur=META.kgStart,guard=0;if(cur&&nodeById[cur]){chain.push(cur);while(guard++<10){var e1=KG.edges.filter(function(e){return e.s===cur&&e.p==='lab:hasLimitation'})[0];if(!e1)break;var e2=KG.edges.filter(function(e){return e.s===e1.o&&e.p==='lab:addressedBy'})[0];chain.push(e1.o);if(!e2)break;chain.push(e2.o);cur=e2.o;}}
   $('#kgPath').innerHTML=chain.map(function(id,i){var n=nodeById[id];if(!n)return '';return '<span class="s '+(n.type==='Limitation'?'bad':'done')+'">'+(n.type==='Limitation'?'한계: ':'')+n.label.ko+'</span>'+(i<chain.length-1?'<span class="muted">→</span>':'');}).join('');
   $('#kgOpen').innerHTML=KG.nodes.filter(function(n){return n.type==='Question'}).map(function(n){return '<li><a href="'+n.anchor+'">'+n.label.ko+'</a></li>';}).join('');})();
  gN=KG.nodes.filter(function(n){return CHIPS.indexOf(n.type)>=0}).slice(0,90);
  (function(){var r=rng(17);gN.forEach(function(n,i){gIdx[n.id]=i;gP.push({x:r()*2-1,y:r()*2-1,vx:0,vy:0});});var E=KG.edges.filter(function(e){return gIdx[e.s]!=null&&gIdx[e.o]!=null});
   for(var it=0;it<200;it++){for(var i=0;i<gP.length;i++)for(var j=i+1;j<gP.length;j++){var dx=gP[i].x-gP[j].x,dy=gP[i].y-gP[j].y,d2=dx*dx+dy*dy+0.01,f=0.004/d2;gP[i].vx+=dx*f;gP[i].vy+=dy*f;gP[j].vx-=dx*f;gP[j].vy-=dy*f;}
    E.forEach(function(e){var a=gP[gIdx[e.s]],b=gP[gIdx[e.o]],dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)+1e-6,f=(d-0.35)*0.03;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
    gP.forEach(function(p){p.vx-=p.x*0.01;p.vy-=p.y*0.01;p.x+=p.vx;p.y+=p.vy;p.vx*=0.6;p.vy*=0.6;});}
   var mx=0;gP.forEach(function(p){mx=Math.max(mx,Math.abs(p.x),Math.abs(p.y));});gP.forEach(function(p){p.x/=mx||1;p.y/=mx||1;});})();
  if(cKG){cKG.addEventListener('pointerdown',function(e){var r=cKG.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;for(var i=0;i<gScr.length;i++){var g=gScr[i];if((g[0]-mx)*(g[0]-mx)+(g[1]-my)*(g[1]-my)<=g[2]*g[2]){kgHL=g[3];$('#kgQ').value='';kgRender();drawKG();var el=document.getElementById('ki-'+g[3].replace(/[^a-z0-9]/gi,'_'));if(el)el.scrollIntoView({block:'nearest',behavior:reduce?'auto':'smooth'});break;}}});
   addMod(cKG,function(dt){if(dt===0)drawKG();});}
  kgRender();
}

/* ---------- 온톨로지·서지 꾸러미 (O2) ---------- */
function download(blob,name){var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);}
function dlText(t,name,type){download(new Blob([t],{type:type||'text/plain;charset=utf-8'}),name);}
var CRC=(function(){var t=[],c;for(var n=0;n<256;n++){c=n;for(var k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0;}return function(u8){var x=0xFFFFFFFF;for(var i=0;i<u8.length;i++)x=t[(x^u8[i])&255]^(x>>>8);return (x^0xFFFFFFFF)>>>0;};})();
function makeZip(files){var enc=new TextEncoder(),parts=[],central=[],off=0;function u16(v){return [v&255,(v>>8)&255]}function u32(v){return [v&255,(v>>8)&255,(v>>16)&255,(v>>>24)&255]}
  files.forEach(function(f){var name=enc.encode(f.name),data=enc.encode(f.text),crc=CRC(data);
    var head=[].concat(u32(0x04034b50),u16(20),u16(0x0800),u16(0),u16(0),u16(0),u32(crc),u32(data.length),u32(data.length),u16(name.length),u16(0));
    parts.push(new Uint8Array(head),name,data);central.push(new Uint8Array([].concat(u32(0x02014b50),u16(20),u16(20),u16(0x0800),u16(0),u16(0),u16(0),u32(crc),u32(data.length),u32(data.length),u16(name.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(off))),name);
    off+=head.length+name.length+data.length;});
  var cdStart=off,cdLen=0;central.forEach(function(c){parts.push(c);cdLen+=c.length;});
  parts.push(new Uint8Array([].concat(u32(0x06054b50),u16(0),u16(0),u16(files.length),u16(files.length),u32(cdLen),u32(cdStart),u16(0))));return new Blob(parts,{type:'application/zip'});}
var BIBT={'article-journal':'article','paper-conference':'inproceedings','book':'book','chapter':'incollection','webpage':'misc','dataset':'misc','report':'techreport','thesis':'phdthesis','software':'misc','article':'misc'};
var RIST={'article-journal':'JOUR','paper-conference':'CPAPER','book':'BOOK','chapter':'CHAP','webpage':'ELEC','dataset':'DATA','report':'RPRT','thesis':'THES','software':'COMP','article':'GEN'};
function names(a){return (a||[]).map(function(p){return p.literal||(p.family+(p.given?', '+p.given:''));});}
function toBib(r){var f=[],add=function(k,v){if(v!==undefined&&v!==null&&v!=='')f.push('  '+k+' = {'+v+'}');};add('title',r.title);add('author',names(r.author).map(function(n){return n==='et al.'?'others':n;}).join(' and '));add('year',r.issued&&r.issued['date-parts'][0][0]);
  add(r.type==='article-journal'?'journal':(r.type==='article'?'howpublished':'booktitle'),r['container-title']);add('volume',r.volume);add('number',r.issue);add('pages',r.page);add('publisher',r.publisher);add('doi',r.DOI);add('url',r.URL);
  if(r.lab&&r.lab.note)add('note',r.lab.note);return '@'+(BIBT[r.type]||'misc')+'{'+r.id+',\n'+f.join(',\n')+'\n}';}
function toRis(r){var L=['TY  - '+(RIST[r.type]||'GEN')],add=function(t,v){if(v)L.push(t+'  - '+v);};add('TI',r.title);names(r.author).forEach(function(n){add('AU',n);});add('PY',r.issued&&r.issued['date-parts'][0][0]);add('T2',r['container-title']);add('VL',r.volume);add('IS',r.issue);add('DO',r.DOI);add('UR',r.URL);if(r.lab&&r.lab.note)add('N1',r.lab.note);L.push('ER  - ');return L.join('\r\n');}
function citeText(r){var a=names(r.author);var au=a.length>3?a.slice(0,3).join(', ')+' 외':a.join(', ');return au+' ('+(r.issued&&r.issued['date-parts'][0][0]||'')+'). '+r.title+'. '+(r['container-title']||r.publisher||'')+(r.volume?' '+r.volume:'')+(r.page?', '+r.page:'')+'.'+(r.URL?' '+r.URL:'');}
var SCOPE='all';
function filterScope(g,sc){if(sc==='all')return g;var keep;
  if(sc==='concepts')keep=function(n){return ['Concept','Method','Term','Task','Metric','Limitation'].indexOf(n.type)>=0;};
  else if(sc==='claims')keep=function(n){return ['Claim','Work'].indexOf(n.type)>=0;};
  else keep=function(n){return KG.edges.some(function(e){return e.p==='lab:prerequisiteOf'&&(e.s===n.id||e.o===n.id);});};
  var nodes=g.nodes.filter(keep),ids={};nodes.forEach(function(n){ids[n.id]=1;});var edges=g.edges.filter(function(e){return ids[e.s]&&ids[e.o]&&(sc!=='prereq'||e.p==='lab:prerequisiteOf');});
  return {version:g.version,page:g.page,scope:sc,nodes:nodes,edges:edges};}
var CTX={'@vocab':'https://schema.org/',skos:'http://www.w3.org/2004/02/skos/core#',schema:'https://schema.org/',dct:'http://purl.org/dc/terms/',prov:'http://www.w3.org/ns/prov#',lab:'urn:lab:'};
var SKOSP={'lab:broader':'skos:broader','lab:relatedTo':'skos:related','lab:partOf':'dct:isPartOf','lab:assertedIn':'schema:citation'};
var TYPEMAP={Concept:['skos:Concept','schema:DefinedTerm'],Method:['skos:Concept','schema:DefinedTerm'],Task:['skos:Concept','schema:DefinedTerm'],Term:['skos:Concept','schema:DefinedTerm'],Limitation:['skos:Concept'],Metric:['skos:Concept','schema:DefinedTerm'],Work:['schema:ScholarlyArticle'],Claim:['schema:Claim'],Dataset:['schema:Dataset'],QuizItem:['schema:Question'],Section:['schema:WebPageElement'],Question:['schema:Question'],Analogy:['skos:Concept'],Simulation:['schema:CreativeWork']};
function toJsonLd(g){var graph=g.nodes.map(function(n){var o={'@id':n.id,'@type':(TYPEMAP[n.type]||['skos:Concept']).concat(['lab:'+n.type]),'skos:prefLabel':[{'@value':n.label.ko,'@language':'ko'},{'@value':n.label.en,'@language':'en'}]};
  if(n.definition)o['skos:definition']={'@value':n.definition.ko,'@language':'ko'};if(n.altLabel&&n.altLabel.ko)o['skos:altLabel']=n.altLabel.ko.map(function(v){return {'@value':v,'@language':'ko'}});o['schema:url']=META.url?META.url+n.anchor:n.anchor;
  g.edges.filter(function(e){return e.s===n.id}).forEach(function(e){var p=SKOSP[e.p]||e.p;(o[p]=o[p]||[]).push({'@id':e.o});});return o;});
  return {'@context':CTX,'@graph':graph};}
function ttlEsc(s){return String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\n/g,' ');}
function iri(id){return '<'+id.replace('lab:','urn:lab:')+'>';}
function toTurtle(g){var L=['@prefix skos: <http://www.w3.org/2004/02/skos/core#> .','@prefix schema: <https://schema.org/> .','@prefix lab: <urn:lab:> .',''];
  g.nodes.forEach(function(n){var t=(TYPEMAP[n.type]||['skos:Concept']).concat(['lab:'+n.type]);L.push(iri(n.id)+' a '+t.join(', ')+' ;');L.push('  skos:prefLabel "'+ttlEsc(n.label.ko)+'"@ko, "'+ttlEsc(n.label.en)+'"@en'+(n.definition?' ;':' .'));if(n.definition)L.push('  skos:definition "'+ttlEsc(n.definition.ko)+'"@ko .');});
  L.push('');g.edges.forEach(function(e){L.push(iri(e.s)+' '+(e.p.indexOf('lab:')===0?'lab:'+e.p.slice(4):e.p)+' '+iri(e.o)+' .');if(SKOSP[e.p])L.push(iri(e.s)+' '+SKOSP[e.p]+' '+iri(e.o)+' .');});return L.join('\n');}
function csvCell(v){v=v==null?'':String(v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;}
function toNodesCsv(g){return ['id,type,label_ko,label_en,status,level,family,page,anchor'].concat(g.nodes.map(function(n){return [n.id,n.type,n.label.ko,n.label.en,n.status,n.level||'',n.family||'',n.page,n.anchor].map(csvCell).join(',');})).join('\r\n');}
function toEdgesCsv(g){return ['source,predicate,target,anchor,confidence'].concat(g.edges.map(function(e){return [e.s,e.p,e.o,e.anchor,e.confidence].map(csvCell).join(',');})).join('\r\n');}
function toProvCsv(g){var rows=['item,kind,work,loc,factCard,confidence,verified,pageAnchor'];
  g.nodes.forEach(function(n){(n.source||[]).forEach(function(s){rows.push([n.id,'node',s.work,s.loc,(n.evidence||[]).join(' '),n.confidence,s.verified?'true':'false',n.anchor].map(csvCell).join(','));});});return rows.join('\r\n');}
function todo(){var t=[];REF.forEach(function(r){var v=r.lab&&r.lab.verified||{};Object.keys(v).forEach(function(k){if(!v[k])t.push(r.id+': '+k+' 확인 필요');});});
  KG.nodes.forEach(function(n){(n.match||[]).forEach(function(m){if(!m.verified)t.push(n.id+': '+m.scheme+' 외부 ID 미확인');});});
  ['creator','license','url'].forEach(function(k){var v=META[k];if(!v||(Array.isArray(v)&&!v.length))t.push('page_meta.'+k+': 채워 넣을 것');});return t;}
function readme(g){return [META.title,'시리즈: '+META.series+' · 번호 '+META.number+' · 판 '+META.version+' · 만든 날 '+META.date,'','권장 인용: '+META.suggestedCitation,'',
  '파일','- manifest.json: 목록','- page_meta.json: 이 페이지의 서지 정보','- kg.json: 중립 지식 그래프 (원본)','- kg.jsonld / kg.ttl: SKOS·schema.org 매핑','- nodes.csv / edges.csv: 표 (UTF-8 BOM)','- references.csl.json / .bib / .ris: 참고문헌','- provenance.csv: 주장 ↔ 문헌 ↔ 원문 위치','',
  '범위: '+(g.scope||'all')+' · 노드 '+g.nodes.length+' · 관계 '+g.edges.length+' · 문헌 '+REF.length,'','확인 필요'].concat(todo().map(function(t){return '- '+t;})).join('\n');}
function buildPackage(sc){var g=filterScope(KG,sc),B='﻿';var files=[{name:'page_meta.json',text:JSON.stringify(META,null,2)},{name:'kg.json',text:JSON.stringify(g,null,2)},{name:'kg.jsonld',text:JSON.stringify(toJsonLd(g),null,2)},{name:'kg.ttl',text:toTurtle(g)},
  {name:'nodes.csv',text:B+toNodesCsv(g)},{name:'edges.csv',text:B+toEdgesCsv(g)},{name:'references.csl.json',text:JSON.stringify(REF,null,2)},{name:'references.bib',text:REF.map(toBib).join('\n\n')},{name:'references.ris',text:REF.map(toRis).join('\r\n')},{name:'provenance.csv',text:B+toProvCsv(g)},{name:'README.txt',text:readme(g)}];
  files.unshift({name:'manifest.json',text:JSON.stringify({package:'lab-kg',version:META.version,page:META.number,created:META.date,scope:sc,counts:{nodes:g.nodes.length,edges:g.edges.length,refs:REF.length},registry:'KG_00_registry (ahnboat_lab_explainer)',files:['manifest.json'].concat(files.map(function(f){return f.name}))},null,2)});return files;}
window.LAB_EXPORT={buildPackage:buildPackage,makeZip:makeZip,toBib:toBib,toRis:toRis};
if($('#refList')){(function(){var claims=KG.nodes.filter(function(n){return n.type==='Claim'});
  var ver=REF.filter(function(r){var v=r.lab&&r.lab.verified||{};return v.title&&v.authors&&v.year;}).length;
  kpis('#exStats',[[KG.nodes.length,'노드','g'],[KG.edges.length,'관계','m'],[REF.length,'문헌 (확인 '+Math.round(ver/Math.max(1,REF.length)*100)+'%)','i'],[claims.length,'주장 (출처 있음)','a']]);
  var td=todo();setTxt('#exSay','출처 없는 주장은 꾸러미에 넣지 않았어요. 확인할 항목 '+td.length+'개는 아래에 있어요.');
  $('#todoList').innerHTML=td.map(function(t){return '<li>'+t+'</li>';}).join('');
  setTxt('#exVer','꾸러미 판 '+META.version+' · 만든 날 '+META.date+' · 등록부: ahnboat_lab_explainer/data/KG_00_registry.json');
  var self={id:META.citeKey||'ahn2026lab',type:'webpage',title:META.title,author:[{family:'안',given:'상선'}],issued:{'date-parts':[[2026]]},'container-title':META.series,URL:META.url||''};
  var CF={text:META.suggestedCitation,bib:toBib(self),ris:toRis(self)},cf='text';function showCite(){setTxt('#citeBox',CF[cf]);}showCite();
  $$('[data-cf]').forEach(function(b){b.addEventListener('click',function(){cf=b.dataset.cf;$$('[data-cf]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});showCite();});});
  $('#citeCopy').addEventListener('click',function(){var t=CF[cf],btn=this;function sel(){var r=document.createRange();r.selectNodeContents($('#citeBox'));var s=getSelection();s.removeAllRanges();s.addRange(r);}
    try{navigator.clipboard.writeText(t).then(function(){btn.textContent='복사됨';setTimeout(function(){btn.textContent='복사';},1200);},sel);}catch(e){sel();}});
  var ROLE={primary:'주 자료',background:'배경',data:'수치',figure:'그림',software:'코드'};
  $('#refList').innerHTML=REF.map(function(r){var v=r.lab&&r.lab.verified||{},ok=v.title&&v.authors&&v.year;
    return '<div class="ref"><span class="role">'+(ROLE[r.lab&&r.lab.role]||'참고')+'</span>'+citeText(r)+'<span class="badge '+(ok?'ok':'no')+'">'+(ok?'확인됨':'확인 필요')+'</span></div>';}).join('');
  $$('[data-sc]').forEach(function(b){b.addEventListener('click',function(){SCOPE=b.dataset.sc;$$('[data-sc]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});});});
  $('#zipBtn').addEventListener('click',function(){download(makeZip(buildPackage(SCOPE)),'kg_'+META.number+'_'+META.slug+(SCOPE==='all'?'':'_'+SCOPE)+'.zip');});
  var fl=['manifest.json','page_meta.json','kg.json','kg.jsonld','kg.ttl','nodes.csv','edges.csv','references.csl.json','references.bib','references.ris','provenance.csv','README.txt'];
  $('#fileBtns').innerHTML=fl.map(function(n){return '<button class="bt" data-fn="'+n+'">'+n+'</button>';}).join('');
  $$('[data-fn]').forEach(function(b){b.addEventListener('click',function(){var f=buildPackage(SCOPE).filter(function(x){return x.name===b.dataset.fn})[0];dlText(f.text,f.name,/json/.test(f.name)?'application/json':/csv/.test(f.name)?'text/csv;charset=utf-8':'text/plain;charset=utf-8');});});
  $('#kgJson').addEventListener('click',function(){dlText(JSON.stringify(KG,null,2),'kg_'+META.number+'.json','application/json');});})();}

/* ---------- 바깥에 내보내는 API ---------- */
window.LAB={$:$,$$:$$,rng:rng,fit:fit,stamp:stamp,grid:grid,FONT:FONT,C:C,fmt:fmt,setTxt:setTxt,kpis:kpis,ins:ins,bindSeg:bindSeg,Cast:Cast,addMod:addMod,drawAll:drawAll,Duel:Duel,reduce:reduce,
  start:function(){glossWrap();studyUpd();drawAll();window.addEventListener('resize',function(){drawAll();});requestAnimationFrame(loop);}};
})();
