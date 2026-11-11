# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import *
from parts import *
from series import BASE

SLUG = 'week_01_textbook_preface'; P = 'preface'; URL = BASE + SLUG + '/'

hero = '''<header class="hero" id="top"><div class="wrap"><div class="hero-text">
<p class="eyebrow">인퍼런스 스터디 북 · 1주차 교재 · 서문 (Preface)</p>
<h1>추론은 이제 모두의 일</h1>
<p class="q">세상에 모델이 이백만 개를 넘었다면, 그 모델을 '잘 돌리는 일'은 누구의 몫일까?</p>
<p>『Inference Engineering』 서문은 한 가지 변화를 짚습니다. 2022년에는 소수의 연구소만 큰 모델을 서비스했지만, 지금은 누구나 열린 모델을 받아 자기 제품에 올립니다. 그러면 <b>추론</b>을 빠르고 싸고 안정적으로 만드는 일, 곧 추론 엔지니어링이 모든 팀의 숙제가 됩니다.</p>
<div class="kpis" id="heroK"></div>
<p class="cite">교재: Kiely, P. (2026). <i>Inference Engineering</i>, Preface. Baseten Books. 수치에 <span class="chip-src">원문</span> 칩이 붙은 것은 교재 그대로입니다.</p>
<div class="dialog">''' + say('doc', 'front', '첫 장을 펼치기 전에 서문부터! 이 책이 왜 지금 나왔는지가 여기 다 들어 있어요.') + say('asst', 'smile', '서문 그림 P.1부터 P.3까지 세 장, 핵심 숫자는 다섯 개예요. 하나씩 직접 돌려 볼게요.') + say('fly', 'point', '모델이 많아진 건 알겠어. 근데 그게 왜 "엔지니어링"이 필요하다는 얘기가 돼?') + say('robo', 'chart', '모델이 많을수록 고를 게 많고, 고를 게 많을수록 굴릴 GPU도 많지. 시장이 크다는 뜻이야!') + say('sia', 'guide', '오늘 순서는 세 칸입니다. 모델의 폭발 → 문턱을 넘는 열린 모델 → 세 개의 저울.') + say('moa', 'tea', '숫자는 제가 끝에서 기록장에 모아 둘게요. 편하게 따라오세요!') + '''</div></div></div></header>'''

cast = crew({'doc': '해설·심판. 서문의 주장을 한 줄로', 'asst': '그림 P.1~P.3 수치 발표', 'fly': '"그래서 우리한테 왜?"를 묻는 쪽', 'robo': '"모델이 많으면 기회도 많다"는 쪽',
             'sia': '오늘의 순서·진행 신호', 'moa': '숫자 기록장·응원', 'x1': '방청석', 'x2': '방청석', 'x3': '방청석'},
            extra='<h3>오늘의 순서</h3>' + route([('why', '도입', '왜 서문부터 읽나'), ('lv1', '① 칸', '모델의 폭발'), ('lv2', '② 칸', '문턱을 넘는 열린 모델'), ('lv3', '③ 칸', '세 개의 저울'), ('duel', '대결', '9의 개수'), ('sum', '정리', '모아의 기록장')]))

why = section('why', '0', '왜 서문부터 읽나', '''
<div class="steps"><div><h4>이 책의 출발점</h4><p>서문은 추론을 <b>AI 산업에서 가장 값진 영역</b>이라고 부르면서도, 추론 엔지니어링은 아직 걸음마 단계라고 말합니다. 쿠다(CUDA)부터 쿠버네티스까지, 모델을 실제로 서비스하는 전 구간을 다루는 일이에요.</p></div>
<div><h4>2022년 11월 30일</h4><p>챗GPT가 나온 날, 이런 일을 하는 사람은 세계에 <b>몇백 명</b> 정도였다고 합니다 <span class="chip-src">원문</span>. 대부분 큰 연구소와 빅테크에 있었어요.</p></div>
<div><h4>3년 뒤</h4><p>학습은 여전히 어렵고 비싸지만, 소수만 할 수 있을 만큼은 아니었습니다. 열린 모델이 쏟아졌고, 이제 엔지니어 누구나 자기 모델을 배포할 수 있습니다.</p></div></div>
<div class="pair"><div><span class="tag fly">연구실에서는</span><p>시약을 사다 쓰던 연구실이, 이제는 시약을 직접 만들어 쓸 수 있게 된 셈입니다. 그러면 <b>보관·운반·실험대 배치</b>가 연구실의 실력이 됩니다.</p></div><div><span class="tag nn">모델에서는</span><p>모델을 API로 빌려 쓰던 팀이, 이제는 열린 모델의 가중치를 받아 직접 돌립니다. 그러면 <b>GPU·소프트웨어·배포</b>를 다루는 추론 엔지니어링이 팀의 실력이 됩니다.</p></div></div>
''' + say('fly', 'clip', '"시약을 직접 만든다"는 건 비유야. 실제로는 모델을 처음부터 학습하는 게 아니라, 남이 공개한 가중치를 받아 돌리는 경우가 대부분이지.'), tags=[('g', '서문 1~4쪽')])

lv1 = level(1, 'lv1', '모델의 폭발 — 그림 P.1', [('g', '모델: 열린 모델 수'), ('p', '교재: 그림 P.1')],
    pair=('연구실에서는', '시약장에 병이 25배로 늘었다면, 이제 문제는 "어떤 병이 있나"보다 "어떤 병을 어떻게 빨리 꺼내 쓰나"입니다.', '모델에서는', '허깅페이스의 열린 모델은 <b>이백만 개를 훨씬 넘고</b>, 5년 전보다 <b>25배</b> 많습니다 <span class="chip-src">원문</span>. 고르는 일과 돌리는 일이 둘 다 중요해졌어요.'),
    panel=panel('5년에 25배면, 한 해에 몇 배일까?', 'cGrow', '열린 모델 수가 5년 동안 25배로 늘어나는 곡선. 양 끝 두 점만 교재 값이고 그 사이 곡선은 설명용입니다.',
                ctrl=slider('gY', '몇 년째', 0, 5, 1, 5, '년'), kp_id='gK', eq='한 해 배율 r = <b>25</b><sup>1/5</sup> ≈ <i>1.90</i> &nbsp;·&nbsp; n년 뒤 = 처음 × r<sup>n</sup>', ins_id='gI'),
    explain=explain('풀이', ['교재가 준 숫자는 둘뿐이에요: 지금 이백만 개 이상, 그리고 5년 전의 25배.', '25배를 5년에 고르게 나누면 한 해에 약 1.9배씩 늘어난 셈이에요(25의 5제곱근).', '곡선 가운데는 이 계산으로 그린 <b>설명용</b>이에요. 실제 해마다의 개수는 그림 P.1 원문을 보세요.'],
                    limit='모델 수가 많다고 쓸 만한 모델이 그만큼 많은 건 아닙니다. 대부분은 작은 파생 모델이에요. "어떤 모델이 우리 제품에 쓸 만한가"는 ② 칸의 문턱 이야기로 넘어갑니다.'),
    bridge=bridge(gen=('챗봇 하나를 만들 때도 "어느 모델을 쓸까"부터 고민하게 된 이유예요. 선택지가 늘면 비교·평가(evals)가 먼저 필요해집니다.', '개수는 품질을 말해 주지 않아요.'),
                  field=('사내 도구를 만드는 팀이라면, 큰 모델 하나 대신 작은 열린 모델 여러 개를 업무별로 고를 수 있어요.', '라이선스(상업적 사용 제한)를 꼭 확인해야 합니다 — 서문도 이 점을 당부합니다.')),
    talk=say('robo', 'happy', '한 해 1.9배! 이 정도면 복리 상품 부럽지 않은데? (물론 모델 수 얘기야.)'))

lv2 = level(2, 'lv2', '문턱을 넘는 열린 모델 — 그림 P.2·P.3', [('g', '모델: 닫힌 모델 vs 열린 모델'), ('p', '교재: 그림 P.2, P.3')],
    pair=('연구실에서는', '실험 장비마다 "이 정밀도는 넘어야 쓸 수 있다"는 기준선이 있어요. 새 장비가 그 선을 넘는 순간, 그 실험이 가능해집니다.', '모델에서는', '닫힌 모델(가중치 비공개)과 열린 모델(가중치 공개)이 함께 똑똑해지면서, <b>탭 완성 → 코드 생성 → 추론 에이전트</b> 같은 능력 문턱을 차례로 넘습니다. 열린 모델은 몇 주~몇 달 늦게 따라오고, 2024년 12월 이후로는 격차가 사라졌다고 교재는 말합니다 <span class="chip-src">원문</span>.'),
    panel=panel('언제 어떤 제품이 가능해질까?', 'cThr', '닫힌 모델과 열린 모델의 능력 곡선, 그리고 세 개의 능력 문턱. 모든 곡선은 설명용 모형입니다.',
                ctrl=slider('tT', '시간', 0, 100, 1, 40, '') + slider('tLag', '열린 모델 지연', 0, 30, 1, 12, '') + btn_group('tFt', '미세조정', [('0', '안 함'), ('1', '함')]),
                kp_id='tK', ins_id='tI', wide=True),
    explain=explain('풀이', ['초록 선은 닫힌 모델, 분홍 선은 열린 모델이에요. 가로줄 세 개가 제품 문턱입니다.', '"열린 모델 지연"을 줄이면 분홍 선이 초록 선에 붙어요. 교재가 말하는 2024년 12월 이후의 모습이에요.', '"미세조정 함"을 누르면 열린 모델이 자기 분야에서 한 칸 위로 올라가요. 그림 P.3: 열린 모델을 고쳐 쓰면 새 능력을 열면서도 지연시간·안정성·비용을 직접 쥘 수 있어요.'],
                    limit='곡선 모양과 문턱 높이는 모두 설명용이에요. 교재 그림 P.2·P.3도 눈금 없는 개념도입니다. 능력을 실제로 재는 방법은 1주차 논문(라이브벤치)에서 다룹니다.'),
    bridge=bridge(gen=('IDE의 탭 완성처럼 빨라야 하는 기능은 작은 열린 모델로, 복잡한 에이전트는 큰 모델로 나누는 식의 설계가 여기서 나옵니다.', '문턱은 한 줄이 아니라 업무마다 다릅니다.'),
                  field=('콜센터 음성 상담처럼 "예전 모델은 느리고 비싸서 못 하던 일"이 문턱을 넘으면서 회사가 생겨났다고 서문은 설명합니다.', '문턱을 넘었다고 곧바로 서비스가 되진 않아요 — 그다음이 추론 엔지니어링입니다.')),
    talk=say('fly', 'point', '격차가 사라졌다는 건 "벤치마크 점수" 얘기 아니야? 우리 제품에서도 그런지는 따로 재야지.'))

lv3 = level(3, 'lv3', '세 개의 저울 — 지연시간·가용성·비용', [('g', '모델: 전용 배포'), ('p', '교재: 서문 목록 세 줄')],
    pair=('연구실에서는', '공용 장비실을 빌려 쓰면 편하지만, 줄이 길면 기다리고, 장비실이 문을 닫으면 실험도 멈춥니다. 우리 실험실에 장비를 두면 그 셋을 우리가 정해요.', '모델에서는', '열린 모델로 바꾸면 세 저울을 직접 움직일 수 있어요: <b>지연시간</b>(API는 처리량 위주), <b>가용성</b>(API는 9가 두 개, 전용 배포는 네 개 이상도 가능), <b>비용</b>(규모가 크면 흔히 80% 이상 저렴) <span class="chip-src">원문</span>.'),
    panel=panel('9의 개수 계산기', 'cUp', '1년 365일을 칸으로 그리고, 가용성에 따라 멈춰 있는 시간을 빨간 칸으로 칠합니다.',
                ctrl=slider('uN', '9의 개수', 2, 5, 1, 2, '개') + slider('uC', '규모 비용 절감', 0, 90, 5, 80, '%'),
                kp_id='uK', eq='멈춤 시간 = 1년(8,760시간) × (1 − 가용성) &nbsp;·&nbsp; 99% → <i>87.6시간</i>, 99.99% → <b>52.6분</b>', ins_id='uI'),
    explain=explain('풀이', ['"9가 두 개"는 가용성 99%예요. 1년 8,760시간의 1%, 곧 87.6시간 동안 멈출 수 있다는 뜻이에요.', '"9가 네 개"(99.99%)면 1년에 약 52.6분이에요. 같은 1%의 차이가 아니라 <b>100배</b> 차이예요.', '비용 막대는 교재의 "흔히 80% 이상 저렴" 문장을 막대로 그린 것이에요. 실제 가격은 모델·GPU·사용량마다 달라요.'],
                    limit='네 개의 9는 "가능하다"는 뜻이지 저절로 되는 게 아니에요. 그걸 해내는 기술이 이 책의 7장(운영)까지 이어집니다.'),
    bridge=bridge(gen=('챗 서비스가 1년에 87시간 멈추면, 사용자는 "가끔 안 되는 서비스"로 기억합니다. 52분이면 거의 느끼지 못해요.', '가용성은 모델 하나가 아니라 네트워크·서버·외부 API가 다 함께 정해요.'),
                  field=('공장 설비의 가동률을 따지는 것과 같은 계산이에요. 99%와 99.99%는 정비팀 규모부터 다릅니다.', '설비와 달리 AI 서비스는 트래픽이 갑자기 몰리는 일이 잦아요.')) + math('수식으로 보기', '<p>가용성 A = 1 − 10<sup>−k</sup> (k = 9의 개수). 1년 멈춤 시간 D = 8760 × 10<sup>−k</sup> 시간. k=2 → 87.6 h, k=3 → 8.76 h, k=4 → 0.876 h = 52.6 min, k=5 → 5.26 min.</p>'),
    talk=say('sia', 'think', '9가 하나 늘 때마다 멈춤 시간이 10분의 1로 줄어요. 순서대로 확인했습니다.'))

duel_sec = section('duel', 'VS', '대결 — 1년에 몇 시간 멈출까?', say('doc', 'think', '서문이 비교한 두 길을 그대로 붙여 봅니다. 숫자는 교재 문장의 9의 개수로만 계산해요.') + duel(
    '같은 1년, 어느 쪽이 덜 멈출까?', '열린 모델을 전용 배포로 (9가 네 개)', '9 하나가 멈춤 시간을 10분의 1로 줄여.', '가장 똑똑한 닫힌 모델 API (9가 두 개)', '제일 똑똑한 모델이면 다 해결이지!'), small='판', tags=[('g', '판정 기준: 1년 멈춤 시간')])

summary = section('sum', '정리', '정리 — 모아의 기록장', '''
<div class="tw"><table class="tb"><tr><th>칸</th><th>새로 알게 된 것</th><th>숫자</th><th>한계</th></tr>
<tr><td>① 모델의 폭발</td><td>열린 모델이 쏟아져 고르는 일·돌리는 일이 중요</td><td class="n">이백만 개 이상, 5년 전의 25배</td><td>개수 ≠ 품질</td></tr>
<tr><td>② 문턱</td><td>닫힌·열린 모델이 함께 문턱을 넘고, 열린 모델은 빠르게 따라옴</td><td class="n">2024년 12월 이후 격차 사라짐</td><td>벤치마크 ≠ 우리 제품</td></tr>
<tr><td>③ 세 저울</td><td>열린 모델 + 전용 배포로 지연·가용성·비용을 직접 조절</td><td class="n">9 두 개 vs 네 개, 80% 이상 저렴</td><td>"가능"하지 저절로가 아님</td></tr></table></div>
<div class="notebook"><h4>모아의 기록장</h4><ul><li>2022-11-30: 추론 엔지니어는 세계에 몇백 명 정도</li><li>열린 모델 = 가중치 공개 (예: 라마, 딥시크), 닫힌 모델 = 가중치 비공개</li><li>열린 모델도 라이선스는 꼭 확인 (상업적 사용 제한이 있을 수 있음)</li><li>저자는 4년 동안 추론 플랫폼 회사에서 일하며 이 책을 썼다고 소개함 — "당신은 이르다(You are early)"</li></ul></div>
<div class="cards"><div class="card"><h4>비유: 시약을 직접 만드는 연구실</h4><p>열린 모델 = 직접 쓰는 시약.</p><p class="lim">실제로는 대부분 남이 만든 가중치를 받아 씁니다.</p></div><div class="card"><h4>비유: 공용 장비실</h4><p>공유 API = 공용 장비실, 전용 배포 = 우리 실험실 장비.</p><p class="lim">장비와 달리 GPU는 시간 단위로 빌릴 수 있어요(1장 1.1절).</p></div></div>
''' + say('moa', 'ok', '기록 완료! 다음 장(0장)에서는 이 일을 세 층(런타임·인프라·도구)으로 나눠 봐요.'), small='끝', tags=[('g', '세 칸 비교')])

outro = section('outro', '끝', '아웃트로', '<div class="outro"><div class="scene" data-img="sc_pre_outro" role="img" aria-label="박사·조수·초파리 연구원·주판봇·시아·모아가 연구실 문 앞에 모인 장면"><img data-who="fly" data-mood="arms" alt=""><img data-who="doc" data-mood="magic" alt=""><img data-who="asst" data-mood="spark" alt=""><img data-who="sia" data-mood="proud" alt=""><img data-who="moa" data-mood="sparkle" alt=""><img data-who="robo" data-mood="sigh" alt=""></div></div>'
    + say('doc', 'magic', '서문의 한 줄: 추론은 이제 몇몇 연구소가 아니라 <b>모든 AI 제품 팀</b>의 숙제다.')
    + say('fly', 'arms', '9 하나에 10분의 1. 숫자로 보니까 "똑똑한 모델"만으론 부족하다는 게 보이네.')
    + say('robo', 'sigh', '이번 판은 손절. 그래도 모델이 많을수록 기회가 많다는 건 맞잖아? 0장에서 본전 찾는다.')
    + say('asst', 'spark', '다음은 0장, "추론이란 무엇인가"예요. 런타임·인프라·도구 세 층으로 지도를 그려요.'), small='', tags=())

GL = {'추론': ['추론 (inference)', '개념', '학습을 마친 모델을 실제 서비스에서 돌려 답을 내는 일. 학습(training)과 구분한다.'],
      '추론 엔지니어링': ['추론 엔지니어링 (inference engineering)', '분야', 'CUDA부터 쿠버네티스까지, 생성 AI 모델을 더 빠르고 싸고 안정적으로 서비스하는 일.'],
      '열린 모델': ['열린 모델 (open model)', '용어', '가중치(weights)를 공개한 모델. 라마·딥시크 등. 라이선스는 모델마다 다르다.'],
      '닫힌 모델': ['닫힌 모델 (closed model)', '용어', '가중치를 공개하지 않고 API로만 쓰게 하는 모델.'],
      '가중치': ['가중치 (weights)', '용어', '학습으로 정해진 모델 속 숫자들. 이것이 있으면 모델을 직접 돌릴 수 있다.'],
      '가용성': ['가용성 (availability, uptime)', '지표', '서비스가 정상으로 응답한 시간의 비율. 99% = "9가 두 개".'],
      '지연시간': ['지연시간 (latency)', '지표', '요청 하나가 답을 받기까지 걸리는 시간.'],
      '처리량': ['처리량 (throughput)', '지표', '정해진 시간에 처리하는 요청·토큰의 양.'],
      '미세조정': ['미세조정 (fine-tuning)', '기법', '이미 학습된 모델을 새 데이터로 조금 더 학습시켜 특정 분야에 맞추는 일. 1장 1.3.2절.'],
      '전용 배포': ['전용 배포 (dedicated deployment)', '용어', 'GPU를 빌려 우리 서비스만을 위한 추론 서버를 두는 방식. 1장 1.1절.'],
      '허깅페이스': ['허깅페이스 (Hugging Face)', '서비스', '열린 모델을 공유하는 대표 저장소.'],
      '능력 문턱': ['능력 문턱 (capability threshold)', '개념', '어떤 제품을 만들 수 있게 되는 모델 능력의 기준선. 그림 P.2.'],
      '벤치마크': ['벤치마크 (benchmark)', '평가', '여러 모델을 같은 문제로 재는 공통 시험. 1주차 논문 라이브벤치 참고.']}
CORE = ['추론 엔지니어링', '열린 모델', '닫힌 모델', '가중치', '가용성', '지연시간', '처리량', '미세조정', '전용 배포', '능력 문턱']
QUIZ = {
 'lv1': [{'q': '[계산] 5년에 25배로 늘었다면, 한 해 평균 몇 배씩 늘어난 셈일까? (가장 가까운 값)', 'o': ['5배', '약 1.9배', '약 1.2배'], 'a': 1, 'why': '맞아요. 25의 5제곱근 ≈ 1.90. 1.9를 다섯 번 곱하면 약 24.8이에요.', 'hint': '5배를 다섯 번 곱하면 3,125배가 돼요.'},
         {'q': '열린 모델과 닫힌 모델을 가르는 기준은?', 'o': ['성능이 높은지', '가중치를 공개했는지', '무료인지'], 'a': 1, 'why': '맞아요. 서문은 가중치 공개 여부로 나눕니다. 열린 모델도 라이선스 조건은 따로 확인해야 해요.', 'hint': '"weights"라는 말을 떠올려 보세요.'}],
 'lv2': [{'q': '교재에 따르면 닫힌 모델과 열린 모델의 의미 있는 능력 격차가 사라진 때는?', 'o': ['2022년 11월', '2024년 12월 무렵', '아직 격차가 크다'], 'a': 1, 'why': '맞아요. 딥시크 V3·R1이 나온 2024년 12월 무렵 격차가 사라졌다고 서문은 말합니다.', 'hint': '딥시크 모델이 나온 때예요.'},
         {'q': '그림 P.3이 말하는 "열린 모델 고쳐 쓰기(customizing)"의 장점이 아닌 것은?', 'o': ['새 능력을 연다', '지연시간·안정성·비용을 직접 쥔다', '학습 없이도 저절로 더 똑똑해진다'], 'a': 2, 'why': '맞아요. 미세조정은 데이터와 학습이 필요해요. 저절로 되는 건 없어요.', 'hint': '"고쳐 쓴다"는 무엇을 한다는 뜻일까요?'}],
 'lv3': [{'q': '[계산] 가용성 99.9%(9가 세 개)면 1년에 최대 몇 시간 멈출 수 있나?', 'o': ['87.6시간', '8.76시간', '0.876시간'], 'a': 1, 'why': '맞아요. 8,760시간 × 0.001 = 8.76시간.', 'hint': '8,760에 0.001을 곱해 보세요.'},
         {'q': '서문이 꼽은 열린 모델 전용 배포의 세 저울에 들지 않는 것은?', 'o': ['지연시간', '가용성', '학습 데이터 양'], 'a': 2, 'why': '맞아요. 세 저울은 지연시간·가용성·비용이에요.', 'hint': '③ 칸 제목을 다시 보세요.'}]}

KG = {'version': '1.0', 'page': P, 'nodes': [
    node('lab:concept/inference', 'Concept', '추론', 'inference', '#why', P, '학습을 마친 모델을 서비스에서 돌려 답을 내는 일.', ('kiely2026inference', 'Preface'), 1, 'basics'),
    node('lab:concept/inference-engineering', 'Concept', '추론 엔지니어링', 'inference engineering', '#why', P, 'CUDA부터 쿠버네티스까지, 생성 AI 서비스를 더 빠르고 싸고 안정적으로 만드는 일.', ('kiely2026inference', 'Preface'), 1),
    node('lab:concept/open-model', 'Concept', '열린 모델', 'open model', '#lv1', P, '가중치를 공개한 모델.', ('kiely2026inference', 'Preface'), 1),
    node('lab:concept/closed-model', 'Concept', '닫힌 모델', 'closed model', '#lv1', P, '가중치를 공개하지 않는 모델.', ('kiely2026inference', 'Preface'), 1),
    node('lab:concept/capability-threshold', 'Concept', '능력 문턱', 'capability threshold', '#lv2', P, '제품을 만들 수 있게 되는 모델 능력의 기준선.', ('kiely2026inference', '그림 P.2'), 2),
    node('lab:method/fine-tuning', 'Method', '미세조정', 'fine-tuning', '#lv2', P, '사전학습 모델을 새 데이터로 특정 용도에 맞추는 일.', ('kiely2026inference', '그림 P.3'), 2, 'training'),
    node('lab:method/dedicated-deployment', 'Method', '전용 배포', 'dedicated deployment', '#lv3', P, '우리 서비스만을 위한 추론 서버를 두는 방식.', ('kiely2026inference', 'Preface'), 2),
    node('lab:metric/latency', 'Metric', '지연시간', 'latency', '#lv3', P, '요청이 답을 받기까지 걸리는 시간.', None, 1, 'evaluation'),
    node('lab:metric/availability', 'Metric', '가용성', 'availability (uptime)', '#lv3', P, '정상 응답 시간의 비율. 9의 개수로 말한다.', ('kiely2026inference', 'Preface'), 1, 'evaluation'),
    node('lab:metric/cost', 'Metric', '비용', 'cost', '#lv3', P, '같은 일을 하는 데 드는 돈. 규모가 크면 열린 모델이 흔히 80% 이상 저렴.', ('kiely2026inference', 'Preface'), 1, 'evaluation'),
    node('lab:claim/two-million', 'Claim', '열린 모델 이백만 개 이상, 5년 전의 25배', 'well over 2M open models, 25x', '#lv1', P, None, ('kiely2026inference', '그림 P.1')),
    node('lab:claim/gap-closed', 'Claim', '2024년 12월 무렵 열린·닫힌 모델 격차 사라짐', 'gap disappeared around Dec 2024', '#lv2', P, None, ('kiely2026inference', 'Preface')),
    node('lab:claim/nines', 'Claim', 'API는 9 두 개, 전용 배포는 네 개 이상 가능', 'two nines vs four nines', '#lv3', P, None, ('kiely2026inference', 'Preface')),
    node('lab:claim/cost-80', 'Claim', '규모에서 열린 모델은 흔히 80% 이상 저렴', 'often at least 80% less expensive at scale', '#lv3', P, None, ('kiely2026inference', 'Preface')),
    node('lab:limitation/count-not-quality', 'Limitation', '개수 ≠ 품질', 'count is not quality', '#lv1', P, '모델이 많다고 쓸 만한 모델이 그만큼 많지는 않다.'),
    node('lab:limitation/benchmark-not-product', 'Limitation', '벤치마크 ≠ 우리 제품', 'benchmarks are not your product', '#lv2', P, '격차가 사라졌다는 말은 공통 시험 기준이다.'),
    node('lab:limitation/possible-not-automatic', 'Limitation', '"가능"하지 저절로가 아님', 'possible, not automatic', '#lv3', P, '네 개의 9는 엔지니어링으로 얻는다.'),
    node('lab:analogy/reagent', 'Analogy', '시약을 직접 쓰는 연구실 ↔ 열린 모델', 'self-made reagents', '#why', P),
    node('lab:analogy/shared-room', 'Analogy', '공용 장비실 ↔ 공유 API', 'shared equipment room', '#lv3', P),
    node('lab:question/core', 'Question', '모델을 잘 돌리는 일은 누구의 몫일까?', 'Whose job is inference now?', '#top', P),
    node('lab:question/duel', 'Question', '대결: 1년에 몇 시간 멈출까?', 'Duel: annual downtime', '#duel', P),
    node('lab:question/next', 'Question', '네 개의 9를 실제로 얻는 기술은? (7장)', 'How to reach four nines?', '#sum', P),
    node('lab:sim/growth', 'Simulation', '한 해 배율 계산', 'growth rate', '#lv1', P), node('lab:sim/threshold', 'Simulation', '능력 문턱 모형', 'threshold model', '#lv2', P), node('lab:sim/nines', 'Simulation', '9의 개수 계산기', 'nines calculator', '#lv3', P),
    node('lab:work/kiely2026inference', 'Work', 'Kiely (2026) Inference Engineering', 'Kiely 2026', '#top', P)],
 'edges': [edge('lab:concept/inference', 'prerequisiteOf', 'lab:concept/inference-engineering', '#why'), edge('lab:concept/open-model', 'prerequisiteOf', 'lab:method/dedicated-deployment', '#lv3'),
           edge('lab:concept/closed-model', 'relatedTo', 'lab:concept/open-model', '#lv1'), edge('lab:concept/open-model', 'hasLimitation', 'lab:limitation/count-not-quality', '#lv1'),
           edge('lab:limitation/count-not-quality', 'addressedBy', 'lab:concept/capability-threshold', '#lv2'), edge('lab:concept/capability-threshold', 'hasLimitation', 'lab:limitation/benchmark-not-product', '#lv2'),
           edge('lab:limitation/benchmark-not-product', 'addressedBy', 'lab:method/dedicated-deployment', '#lv3'), edge('lab:method/dedicated-deployment', 'hasLimitation', 'lab:limitation/possible-not-automatic', '#lv3'),
           edge('lab:method/fine-tuning', 'relatedTo', 'lab:concept/open-model', '#lv2'), edge('lab:method/dedicated-deployment', 'relatedTo', 'lab:metric/latency', '#lv3'),
           edge('lab:method/dedicated-deployment', 'relatedTo', 'lab:metric/availability', '#lv3'), edge('lab:method/dedicated-deployment', 'relatedTo', 'lab:metric/cost', '#lv3'),
           edge('lab:claim/two-million', 'assertedIn', 'lab:work/kiely2026inference', '#lv1'), edge('lab:claim/gap-closed', 'assertedIn', 'lab:work/kiely2026inference', '#lv2'),
           edge('lab:claim/nines', 'assertedIn', 'lab:work/kiely2026inference', '#lv3'), edge('lab:claim/cost-80', 'assertedIn', 'lab:work/kiely2026inference', '#lv3'),
           edge('lab:claim/two-million', 'supports', 'lab:concept/open-model', '#lv1'), edge('lab:claim/nines', 'supports', 'lab:metric/availability', '#lv3'),
           edge('lab:analogy/reagent', 'relatedTo', 'lab:concept/open-model', '#why'), edge('lab:analogy/shared-room', 'relatedTo', 'lab:method/dedicated-deployment', '#lv3'),
           edge('lab:sim/nines', 'relatedTo', 'lab:metric/availability', '#lv3'), edge('lab:sim/threshold', 'relatedTo', 'lab:concept/capability-threshold', '#lv2'), edge('lab:sim/growth', 'relatedTo', 'lab:claim/two-million', '#lv1')]}

JS = r'''
var C=L.C,F=L.FONT,fit=L.fit,grid=L.grid,stamp=L.stamp;
L.kpis('#heroK',[['2M+','허깅페이스 열린 모델','g'],['25×','5년 전 대비','m'],['2 vs 4','9의 개수 (API vs 전용)','i'],['80%+','규모에서 비용 절감','a']]);
/* ① 성장 */
var cG=$('#cGrow'),gy=5,gt=0;
function drawG(dt){gt+=dt;var W=fit(cG,240),x=cG.getContext('2d');x.clearRect(0,0,W,240);grid(x,W,240);var L0=56,R=W-20,T=24,B=200,r=Math.pow(25,1/5);
  x.strokeStyle=C.rule;x.beginPath();x.moveTo(L0,T);x.lineTo(L0,B);x.lineTo(R,B);x.stroke();
  function px(y){return L0+(R-L0)*y/5}function py(v){return B-(B-T)*Math.log(v)/Math.log(25)}
  x.strokeStyle=C.stain;x.lineWidth=2;x.setLineDash([5,4]);x.beginPath();for(var i=0;i<=50;i++){var y=i/10;var v=Math.pow(r,y);i?x.lineTo(px(y),py(v)):x.moveTo(px(y),py(v));}x.stroke();x.setLineDash([]);x.lineWidth=1;
  x.fillStyle=C.gfp;x.beginPath();x.arc(px(gy),py(Math.pow(r,gy)),6+Math.sin(gt*4)*1.2,0,7);x.fill();
  [[0,'5년 전 (1)'],[5,'지금 (25)']].forEach(function(p){x.fillStyle=C.info;x.beginPath();x.arc(px(p[0]),py(Math.pow(r,p[0])),4,0,7);x.fill();x.font='12px '+F;x.textAlign=p[0]?'right':'left';x.fillText(p[1],px(p[0])+(p[0]?-8:8),py(Math.pow(r,p[0]))+(p[0]?-6:-8));});
  x.fillStyle=C.muted;x.font='11px '+F;x.textAlign='center';for(var k=0;k<=5;k++)x.fillText(k+'년',px(k),B+16);x.save();x.translate(14,(T+B)/2);x.rotate(-Math.PI/2);x.fillText('5년 전 대비 배수 (로그 눈금)',0,0);x.restore();
  stamp(x,W,'설명용 곡선 · 양 끝만 교재 값');}
function updG(){var r=Math.pow(25,1/5),v=Math.pow(r,gy);L.setTxt('#gYV',gy+'년');L.kpis('#gK',[[r.toFixed(2)+'×','한 해 배율','g'],[v.toFixed(1)+'×','5년 전 대비','m'],[Math.round(2000000/25*v).toLocaleString()+'개','같은 배율이면 (설명용)','a']]);
  L.ins('#gI',[gy<5?['a','아직 '+(5-gy)+'년 남았어요. 같은 배율이면 지금의 '+(v/25*100).toFixed(0)+'% 수준.']:['g','5년째: 25배. 교재 그림 P.1의 "이백만 개 이상"에 해당해요.']]);drawG(0);}
$('#gY').addEventListener('input',function(){gy=+this.value;updG();});L.addMod(cG,drawG);updG();
/* ② 문턱 */
var cT=$('#cThr'),tt=40,lag=12,ft=0;var TH=[['탭 완성',0.3],['코드 생성',0.55],['추론 에이전트',0.8]];
function cap(t){return 0.08+0.88/(1+Math.exp(-(t-45)/14));}
function drawT(){var W=fit(cT,260),x=cT.getContext('2d');x.clearRect(0,0,W,260);grid(x,W,260);var L0=40,R=W-110,T=20,B=230;
  function px(t){return L0+(R-L0)*t/100}function py(v){return B-(B-T)*v}
  TH.forEach(function(h){x.strokeStyle='rgba(241,182,70,.55)';x.setLineDash([4,4]);x.beginPath();x.moveTo(L0,py(h[1]));x.lineTo(R,py(h[1]));x.stroke();x.setLineDash([]);x.fillStyle=C.amber;x.font='12px '+F;x.textAlign='left';x.fillText(h[0],R+6,py(h[1])+4);});
  function curve(off,boost,col){x.strokeStyle=col;x.lineWidth=2.5;x.beginPath();for(var t=0;t<=100;t++){var v=Math.min(0.99,cap(t-off)+boost);t?x.lineTo(px(t),py(v)):x.moveTo(px(t),py(v));}x.stroke();x.lineWidth=1;}
  curve(0,0,C.gfp);curve(lag,ft?0.08:0,C.stain);
  x.strokeStyle=C.text;x.beginPath();x.moveTo(px(tt),T);x.lineTo(px(tt),B);x.stroke();
  x.fillStyle=C.gfp;x.font='12px '+F;x.textAlign='left';x.fillText('닫힌 모델',L0+6,T+12);x.fillStyle=C.stain;x.fillText('열린 모델'+(ft?' + 미세조정':''),L0+6,T+28);
  x.fillStyle=C.muted;x.textAlign='center';x.fillText('시간 →',(L0+R)/2,B+20);stamp(x,W,'설명용 모형 · 눈금 없음');}
function updT(){L.setTxt('#tTV',tt);L.setTxt('#tLagV',lag);var c=cap(tt),o=Math.min(.99,cap(tt-lag)+(ft?0.08:0));
  function can(v){return TH.filter(function(h){return v>=h[1]}).map(function(h){return h[0]}).join(', ')||'아직 없음';}
  L.kpis('#tK',[[(c*100).toFixed(0),'닫힌 모델 능력 (설명용)','g'],[(o*100).toFixed(0),'열린 모델 능력 (설명용)','m'],[TH.filter(function(h){return o>=h[1]}).length+'/3','열린 모델로 가능한 제품','a']]);
  L.ins('#tI',[['g','닫힌 모델로 가능: '+can(c)],['m','열린 모델로 가능: '+can(o)],[lag<=3?'g':'a',lag<=3?'지연이 거의 없어요 — 교재가 말하는 지금의 모습.':'열린 모델이 '+lag+'칸 늦게 따라와요.']]);drawT();}
$('#tT').addEventListener('input',function(){tt=+this.value;updT();});$('#tLag').addEventListener('input',function(){lag=+this.value;updT();});
L.bindSeg('#tFt',function(v){ft=+v;updT();});L.addMod(cT,function(dt){if(dt===0)drawT();});updT();
/* ③ 9의 개수 */
var cU=$('#cUp'),un=2,uc=80;
function down(k){return 8760*Math.pow(10,-k);}
function hm(h){return h>=1?h.toFixed(h>=10?1:2)+'시간':(h*60).toFixed(1)+'분';}
function drawU(){var W=fit(cU,250),x=cU.getContext('2d');x.clearRect(0,0,W,250);grid(x,W,250);var cols=Math.max(20,Math.floor((W-40)/14)),cell=(W-40)/cols,rows=Math.ceil(365/cols);
  var bad=Math.max(down(un)/24,0);for(var d=0;d<365;d++){var cx=20+(d%cols)*cell,cy=16+Math.floor(d/cols)*cell;var fill=Math.min(1,Math.max(0,bad-d));x.fillStyle=fill>0?'rgba(240,96,77,'+(0.35+0.65*fill)+')':'rgba(94,227,156,.28)';x.fillRect(cx+1,cy+1,cell-2,cell-2);}
  var by=24+rows*cell;x.fillStyle=C.muted;x.font='12px '+F;x.textAlign='left';x.fillText('비용 막대: 공유 API = 100 / 열린 모델 전용 = '+(100-uc),20,by+8);
  x.fillStyle=C.robo;x.fillRect(20,by+16,(W-60),14);x.fillStyle=C.fly;x.fillRect(20,by+36,(W-60)*(100-uc)/100,14);stamp(x,W,'멈춤 칸은 계산값 · 비용은 교재 문장의 설명용 막대');}
function updU(){L.setTxt('#uNV',un+'개');L.setTxt('#uCV',uc+'%');var a=100*(1-Math.pow(10,-un));
  L.kpis('#uK',[[a.toFixed(un)+'%','가용성','g'],[hm(down(un)),'1년 멈춤 시간','r'],[hm(down(un)/12),'한 달 평균','a'],[(100-uc)+'','같은 일의 비용 (API=100)','i']]);
  L.ins('#uI',[[un<=2?'r':'g',un<=2?'9가 두 개: 1년에 하루 반 가까이 멈출 수 있어요.':'9가 '+un+'개: 1년 멈춤 '+hm(down(un))+'.'],['a','9를 하나 더할 때마다 멈춤 시간은 10분의 1이 돼요.']]);drawU();}
$('#uN').addEventListener('input',function(){un=+this.value;updU();});$('#uC').addEventListener('input',function(){uc=+this.value;updU();});L.addMod(cU,function(dt){if(dt===0)drawU();});updU();
/* 대결 */
L.Duel({fmt:function(v){return v>=1?v.toFixed(1)+' 시간':(v*60).toFixed(1)+' 분'},run:function(){var f=down(4),r=down(2);
  return {fly:f,robo:r,res:'F',bars:[['f','초파리',f],['r','주판봇',r]],asst:'1년 멈춤 시간은 초파리 쪽(9가 네 개) '+(f*60).toFixed(1)+'분, 주판봇 쪽(9가 두 개) '+r.toFixed(1)+'시간이에요. 100배 차이예요.',
  verdict:'똑똑한 모델도 멈춰 있으면 답하지 못한다. 멈춤 시간은 9의 개수가 정한다. 초파리 승.',note:'판정은 서문 문장(API는 9가 두 개, 전용 배포는 네 개 이상 가능)의 계산값으로 했어요. 막대는 짧을수록 좋아요. 네 개의 9는 "가능하다"는 뜻이라, 실제로 얻으려면 7장의 운영 기술이 필요해요.'};}});
'''

def spec():
    return {'meta': {'title': '추론은 이제 모두의 일 — 『Inference Engineering』 서문 연구실 해설', 'description': '인퍼런스 스터디 북 1주차 교재 · 서문: 열린 모델의 폭발, 능력 문턱, 지연시간·가용성·비용의 세 저울',
                     'series': '인퍼런스 스터디 북', 'number': '01-0', 'slug': 'preface', 'version': '1.0', 'date': '2026-11-11', 'creator': ['안상선'], 'license': 'CC BY-NC 4.0 (캐릭터 제외)', 'url': URL,
                     'kgStart': 'lab:concept/open-model', 'citeKey': 'ahn2026preface', 'domain': 'ai',
                     'suggestedCitation': '안상선 (2026). 추론은 이제 모두의 일 — 『Inference Engineering』 서문 연구실 해설. 인퍼런스 스터디 북 1주차. ' + URL},
            'kg': KG, 'refs': [book_ref()], 'gl': GL, 'core': CORE, 'quiz': QUIZ, 'js': JS,
            'nav': nav([('cast', '식구'), ('why', '도입'), ('lv1', '① 폭발'), ('lv2', '② 문턱'), ('lv3', '③ 저울'), ('duel', '대결'), ('sum', '정리'), ('kg', '색인'), ('export', '꾸러미')]),
            'body': cover('cover_pre', '인퍼런스 스터디 북 · 1주차 · 서문', '연구실 식구 여섯이 시약장 앞에 서서 쏟아지는 병들을 바라보는 대체 표지',
                          motif=''.join('<i class="%s"></i>' % ('on' if i % 3 == 0 else 'm') for i in range(12)), moods={'doc': 'front', 'asst': 'smile', 'fly': 'point', 'robo': 'chart', 'sia': 'guide', 'moa': 'tea'})
                    + hero + cast + why + lv1 + lv2 + lv3 + duel_sec + summary + outro,
            'footer': footer([('교재', 'Kiely, P. (2026). Inference Engineering, Preface. Baseten Books.'), ('그림 P.1~P.3', '교재 서문 그림 (이 페이지는 숫자만 옮기고 그림은 다시 그림)')],
                             ['① 칸 곡선의 가운데 (양 끝 두 점만 교재 값)', '② 칸의 능력 곡선·문턱 높이 전부', '③ 칸의 비용 막대 (교재 문장 "80% 이상"을 막대로 표현)', '대결의 멈춤 시간은 9의 개수로 계산한 값'],
                             nxt=('../week_01_textbook_ch00/', '0장 추론이란 무엇인가'))}

if __name__ == '__main__':
    out = os.path.join(sys.argv[1], SLUG, 'index.html')
    print(out, build(spec(), out))
