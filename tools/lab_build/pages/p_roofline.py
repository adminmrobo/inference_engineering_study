# -*- coding: utf-8 -*-
"""4주차 논문 · Williams, Waterman, Patterson (2008) Roofline (UCB/EECS-2008-134) — 낮의 연구실(v1.14)."""
import os, sys, json as _j
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import *
from parts import *
from series import BASE
from extras import short_course, teach_appendix, fill_defs

SLUG = 'week_04_article_01'; P = 'roofline'; URL = BASE + SLUG + '/'
SRC = 'williams2008roofline'
LIGHT = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'light.css'), encoding='utf-8').read()

def xask(who, q, a, amood='think', ans='asst'):
    return ('<details class="xask"><summary>방청석 질문 · 미공개 %s</summary>' % who.upper()
            + say(who, 'hint', q, name='방청석 %s' % who.upper()) + say(ans, amood, a) + '</details>')

hero = '''<header class="hero" id="top"><div class="wrap"><div class="hero-text">
<p class="eyebrow">인퍼런스 스터디 북 · 4주차 논문 · UC 버클리 기술 보고서 2008</p>
<h1>루프라인 — 지붕 두 개로 성능의 상한을 그린다</h1>
<p class="q">이 프로그램은 더 빨라질 수 있을까? 그렇다면 계산을 손봐야 할까, 메모리 통로를 손봐야 할까?</p>
<p>멀티코어 시대가 오자 컴퓨터 설계가 제각각이 됐습니다. 이 논문은 <b>완벽한 예측</b> 대신 <b>통찰을 주는 그림 한 장</b>을 제안합니다. 가로축은 <b>작업 강도</b>(메모리에서 1바이트 가져올 때마다 하는 계산 수), 세로축은 <b>성능</b>. 평평한 지붕(최대 계산력)과 비스듬한 지붕(메모리 대역폭 × 작업 강도) 중 <b>낮은 쪽</b>이 넘을 수 없는 상한입니다.</p>
<div class="kpis" id="heroK"></div>
<p class="cite">Williams, S., Waterman, A., &amp; Patterson, D. (2008). <i>Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures</i>. Technical Report UCB/EECS-2008-134, UC Berkeley. (2009년 CACM 게재판의 바탕) <span class="chip-src">원문</span> 칩은 논문 수치 그대로입니다.</p>
<div class="dialog">''' + say('doc', 'board', '3주차 교재 2.4절에서 "루프라인 게시판"을 잠깐 봤죠. 오늘은 그 그림을 처음 그린 사람들의 원본을 읽습니다.') \
    + say('asst', 'report', '논문의 그림 1 · 2와 표 1 · 4의 숫자를 계기판에 그대로 넣었어요. 2008년 CPU 이야기지만, 마지막 실험실에서 교재의 H100 숫자로 다시 그려요.') \
    + say('fly', 'arms', '그래프 하나로 성능을 안다고? 캐시, 프리페치, 지연시간… 다 빼먹은 거 아냐?') \
    + say('robo', 'chart', '지붕이 낮으면 아무리 애써도 못 넘는다 — 숫자로 딱 떨어지니 마음에 들어!') \
    + say('sia', 'explain', '논문 순서대로 갑니다. 질문 → 지붕 그리기 → 결과 넷(능선점 · 천장 · 네 컴퓨터 · 오해 풀기) → 실험실(오늘의 GPU) → 대결.') \
    + say('moa', 'report', '용어 별명 카드부터! 특히 "작업 강도"는 오늘 내내 나와요.') + '''</div></div></div></header>'''

NICK = [('작업 강도', 'operational intensity', 'DRAM에서 가져온 1바이트당 하는 연산 수 (Flops/byte). 캐시를 거친 뒤의 메모리 왕래로 센다'),
        ('지붕선', 'Roofline', '평평한 지붕(최대 계산력) + 비스듬한 지붕(대역폭 × 작업 강도). 둘 중 낮은 쪽이 상한'),
        ('능선점', 'ridge point', '두 지붕이 만나는 곳. 최대 성능을 내는 데 필요한 최소 작업 강도'),
        ('천장', 'ceiling', '특정 최적화를 하기 전에는 뚫을 수 없는 지붕 아래의 선'),
        ('커널', 'kernel', '성능을 재는 핵심 계산 덩어리 (예: 희소 행렬 × 벡터)'),
        ('일곱 난쟁이', 'Seven Dwarfs', '과학·공학에서 오래 중요할 일곱 가지 수치 계산 방법 (Colella)'),
        ('3C', 'compulsory · capacity · conflict', '캐시 미스의 세 종류. 줄이면 작업 강도가 오른쪽으로 간다')]
nick = '<h3>논문 속 용어 별명</h3><div class="nick">' + ''.join('<div class="card"><b>%s</b><div class="orig">%s</div><p style="margin:4px 0 0;font-size:14px">%s</p></div>' % n for n in NICK) + '</div>'
cast = crew({'doc': '해설 · 대결 심판', 'asst': '원문 수치 발표', 'fly': '"그림 하나로는 부족해"를 의심', 'robo': '"대역폭이 곧 속도"를 믿는 쪽', 'sia': '논문 순서 안내 · 진행 신호', 'moa': '별명 카드 · 기록장',
             'x1': '방청석 질문 담당', 'x2': '방청석 질문 담당', 'x3': '방청석 질문 담당'},
            extra=nick + short_course('루프라인 핵심만', [('method', '2 지붕 그리기', '식 한 줄과 그래프 읽는 법'), ('r2', '결과 ② 천장', '무엇을 어떤 순서로 최적화할까'), ('r3', '결과 ③ 표 4', '16개 실측 점이 모두 지붕 아래'), ('lab', '실험실', '오늘의 GPU와 배치 · KV 캐시'), ('duel', '대결', 'H100 → H200')]) + '<h3>오늘의 순서</h3>' + route([('q', '1', '질문'), ('method', '2', '지붕 그리기'), ('r1', '결과 ①', '능선점'), ('r2', '결과 ②', '천장'), ('r3', '결과 ③', '네 컴퓨터 × 네 커널'),
                                                        ('r4', '결과 ④', '작업 강도 옮기기 · 오해'), ('lab', '실험실', '오늘의 GPU로'), ('duel', '대결', 'H100 → H200'), ('reread', '다시 읽기', '추론 엔지니어에게')]))

q = section('q', 1, '질문 — 제각각인 멀티코어, 무엇을 고쳐야 빨라지나', '''
<div class="turn"><div class="card"><h4>예전</h4><p>데스크톱 · 서버 칩은 캐시 · 파이프라인 · 슈퍼스칼라 · 비순차 실행을 다 쓰는 <b>같은 학파</b>였다. 성능 감각도 하나로 통했다.</p></div><div class="arrow">→</div><div class="card"><h4>멀티코어 이후</h4><p>단순한 코어 여럿 vs 복잡한 코어 몇 개, 멀티스레딩, 캐시 대신 직접 주소를 쓰는 로컬 저장소… 설계가 제각각. 프로그래머 · 컴파일러 · 설계자 모두 길을 잃는다.</p></div></div>
<div class="timeline"><div class="st"><b>통계 · 확률 모형</b>정확히 예측하지만 "어떻게 고치나"는 잘 안 알려 주고, 비전문가가 쓰기 어렵다</div><div class="st"><b>한계·병목 분석</b>예측 대신 "무엇이 성능을 막고 있나"를 드러낸다. 대표 예: 암달의 법칙</div><div class="st"><b>본보기: 3C 캐시 모형</b>블록 크기 등을 무시한 불완전한 비유지만 20년 가까이 쓰였다 — 통찰을 주니까</div><div class="st"><b>이 논문</b>멀티코어용 한계·병목 그림. "모형은 완벽할 필요 없이 통찰을 주면 된다"</div></div>
<p class="muted" style="font-size:14px">논문 1 · 2장 정리 <span class="chip-src">원문</span></p>
''' + say('fly', 'magnify', '"완벽하지 않아도 된다"고 처음부터 못 박네. 좋아, 그럼 무엇을 빼고 무엇을 남겼는지 보자.') + '<div class="quiz" data-quiz="q"></div>', small='질문', tags=[('g', '논문: 1–2장')])

method = section('method', 2, '지붕 그리기 — 식 한 줄, 그래프 한 장', '''
<div class="eq">도달 가능한 성능 (GFlops/s) = min( <b>최대 계산력</b>, <em>최대 메모리 대역폭</em> × <i>작업 강도</i> )</div>
<div class="explain" style="margin:10px 0"><h4>그래프 읽는 법 — 로그 눈금</h4><p style="margin:0">이 페이지의 그래프는 가로·세로 모두 <b>로그 눈금</b>이에요. 눈금 한 칸을 갈 때마다 값이 <b>10배</b>(1 → 10 → 100)씩 커져요. 그래서 1/8부터 32까지, 0.5부터 256까지 아주 넓은 범위를 한 장에 담을 수 있고, "두 배"는 어디서나 같은 길이로 보여요. 비스듬한 지붕이 직선으로 보이는 것도 이 덕분이에요.</p></div><p>로그-로그 그래프에서 세로축은 GFlops/s, 가로축은 Flops/byte. 대역폭(바이트/초) = (Flops/초) ÷ (Flops/바이트)이므로 <b>대역폭은 45도 비스듬한 선</b>이 됩니다. 지붕은 <b>컴퓨터마다 한 번</b> 그리면 되고, 커널은 가로축의 한 점(세로 점선)으로 올려 봅니다. 점선이 지붕의 비스듬한 쪽에 닿으면 <b>메모리 한계</b>, 평평한 쪽에 닿으면 <b>계산 한계</b>.</p>''' + panel('지붕선 그리기 — 컴퓨터와 커널을 바꿔 보기', 'cRoof', '로그-로그 축 위의 지붕선. 평평한 지붕은 최대 계산력, 비스듬한 지붕은 대역폭 × 작업 강도. 세로 점선은 커널의 작업 강도.',
    ctrl=btn_group('rP', '본보기', [('x2', 'Opteron X2 (그림 1a)'), ('custom', '직접 정하기')]) + slider('rF', '최대 계산력', 1, 200, 0.1, 17.6, ' GFlops/s') + slider('rB', '최대 대역폭', 1, 100, 0.1, 15, ' GB/s') + slider('rO', '커널 작업 강도 (1/8 ~ 32)', -3, 5, 0.25, 0, ''), kp_id='rK', ins_id='rI', wide=True)
    + explain('풀이', ['<b>작업 강도</b>는 캐시를 <b>거친 뒤</b> DRAM과 오간 바이트로 셉니다(프로세서 ↔ 캐시가 아니라 캐시 ↔ DRAM). 그래서 캐시 최적화의 효과가 이 숫자에 들어가요. "산술 강도"라는 기존 말 대신 쓴 이유이기도 해요.',
                      '최대 계산력은 사양표나 작은 측정 프로그램으로, 최대 대역폭은 저자들이 직접 단계별로 최적화한 측정 프로그램(STREAM보다 정확)으로 구했어요. 칩 핀의 대역폭이 아니라 <b>실제로 꾸준히 낼 수 있는</b> 대역폭.',
                      '그림 1a의 Opteron X2(2.2 GHz, 2소켓): 최대 17.6 GFlops/s, 대역폭 15 GB/s. 작업 강도 2인 커널은 계산 한계, 1인 커널은 메모리 한계예요 <span class="chip-src">원문</span>.'],
              limit='예측 모형이 아니라 <b>상한</b>이에요. 실제 성능은 지붕 아래 어딘가. 여기서 쓴 Flops와 DRAM 바이트 말고 다른 지표로도 그릴 수 있어요(결과 ④).')
    + say('sia', 'guide', '작업 강도 단추를 왼쪽 끝(1/8)에서 오른쪽 끝(32)까지 밀어 보세요. 점이 비스듬한 지붕을 타고 오르다 평평한 지붕에서 멈춰요.') + '<div class="quiz" data-quiz="method"></div>', small='방법', tags=[('g', '논문: 3장, 그림 1a')])

r1 = level('①', 'r1', '결과 ① — 능선점이 오른쪽에 있을수록 최대 성능 내기가 어렵다', [('g', '모델: 능선점'), ('p', '논문: 3장, 그림 1b')],
    pair=('연구실에서는', '실험대(계산)를 네 배 넓혀도 시약 창고 문(대역폭)이 그대로면, 시약을 아주 아껴 쓰는 실험만 빨라져요.',
          '논문에서는', 'Opteron X4는 X2와 같은 소켓 · 같은 DRAM 채널(대역폭은 같고 프리페치만 더 좋음)인데 최대 계산력은 네 배 남짓. 능선점이 <b>1.0 → 4.4</b>로 오른쪽으로 갔어요. X4에서 이득을 보려면 작업 강도가 <b>1보다 커야</b> 해요 <span class="chip-src">원문</span>.'),
    panel=panel('X2 vs X4 — 같은 커널, 몇 배 빨라질까', 'cRidge', '두 컴퓨터의 지붕선을 겹친 로그-로그 그래프와 커널 작업 강도 점선.',
                ctrl=slider('kO', '커널 작업 강도 (1/8 ~ 16)', -3, 4, 0.25, -1, ''), kp_id='kK', ins_id='kI', wide=True),
    explain=explain('풀이', ['능선점의 x좌표 = 최대 성능을 내는 데 필요한 <b>최소 작업 강도</b>.',
                             '능선점이 멀리 오른쪽이면 작업 강도가 아주 높은 커널만 최대 성능에 닿아요. 왼쪽이면 거의 모든 커널이 닿을 수 있죠.',
                             '그래서 능선점은 프로그래머 · 컴파일러가 최대 성능을 내기가 <b>얼마나 어려운지</b>를 보여 줘요(결과 ③에서 확인).'],
                    limit='X2는 그림 1a 값(17.6 GFlops/s · 15 GB/s), X4는 <b>표 1</b> 값(74 GFlops/s · Stream 16.6 GB/s → 능선점 4.46 ≈ 논문의 4.4)으로 그렸어요. 이 페이지의 X4 지붕은 결과 ③ · ④에서도 정점 74를 쓰지만, 그 두 칸은 표 4의 실측 점이 지붕을 넘지 않도록 표 4의 "Stream BW" 천장 17.6 GB/s를 써요(논문 안의 두 값). 논문 본문은 X2 능선점을 1.0이라 적었지만 17.6 ÷ 15로 계산하면 약 1.17이에요.'),
    talk=say('robo', 'calc', '작업 강도 0.5짜리 커널이면… X4로 바꿔도 1.0배. 비싼 칩 사 놓고 그대로라니!'))

r2 = level('②', 'r2', '결과 ② — 천장: 무엇을 어떤 순서로 최적화할까', [('g', '모델: 천장'), ('p', '논문: 4장, 그림 2')],
    pair=('연구실에서는', '실험실 천장이 여러 겹이라 상상해 봐요. 한 겹은 "장비를 동시에 돌리기", 다른 겹은 "시약을 미리 꺼내 두기". 해당 정리를 해야만 그 겹을 뚫고 올라가요.',
          '논문에서는', '지붕 아래에 최적화별 <b>천장</b>을 그어요. Opteron X2의 계산 천장: 균형 없으면 <b>8.8</b>, ILP · SIMD까지 없으면 <b>2.2</b> GFlops/s. 메모리 천장: 소프트웨어 프리페치 없으면 <b>11</b>, 메모리 친화성도 없으면 <b>4.8</b>, 단위 보폭만이면 <b>2.7</b> GB/s <span class="chip-src">원문</span>.'),
    panel=panel('천장 뚫기 — 최적화를 하나씩 켜 보기 (Opteron X2)', 'cCeil', '지붕선 아래 계산 천장(가로선)과 메모리 천장(비스듬한 선). 켠 최적화까지의 천장이 지금의 상한.',
                ctrl=btn_group('cC', '계산 최적화', [('0', '없음 (스레드 병렬만)'), ('1', '+ ① ILP · SIMD'), ('2', '+ ② 곱셈·덧셈 균형')]) + btn_group('cM', '메모리 최적화 (그림 2b의 선 이름)', [('0', '③ 단위 보폭만 · 2.7'), ('1', '+ ④ 메모리 친화성 · 4.8'), ('2', '+ ⑤ 소프트웨어 프리페치 · 11'), ('3', '지붕 · 15')])
                     + slider('cO', '커널 작업 강도 (1/8 ~ 16)', -3, 4, 0.25, 0, ''), kp_id='qK', ins_id='qI', wide=True),
    explain=explain('풀이', ['계산 쪽 최적화 둘: ① 명령어 수준 병렬성(ILP)을 높이고 SIMD 쓰기(루프 펼치기 등), ② 부동소수점 곱셈·덧셈을 같은 수로 맞추기(곱셈-덧셈 명령, 같은 수의 덧셈기·곱셈기).',
                             '메모리 쪽 최적화 셋: ③ 단위 보폭 접근으로 루프 재구성(하드웨어 프리페치가 켜짐), ④ 메모리 친화성(데이터와 스레드를 같은 칩-메모리 쌍에), ⑤ 소프트웨어 프리페치(메모리 요청을 미리 많이 띄워 두기).',
                             '천장 사이 높이 = 그 최적화의 <b>기대 보상</b>. 그림 2에선 ①(ILP · SIMD)과 ④(친화성)의 보상이 커요.',
                             '천장은 아래서부터 <b>쉬운 것</b>(컴파일러가 해 주거나 품이 덜 드는 것) → <b>어려운 것</b> 순서로 쌓아요. 위 천장을 뚫으려면 아래 천장부터 뚫어야 해요.',
                             '커널의 작업 강도가 <b>어느 구역</b>에 있느냐가 할 일을 정해요: 왼쪽 아래(노랑) → 메모리 최적화만, 오른쪽(파랑) → 계산 최적화만, 가운데(초록) → 둘 다.'],
                    limit='메모리 천장 단추 이름은 <b>그림 2b의 선 이름</b>(3. unit stride accesses only · 4. memory affinity · 5. software prefetching)을 따랐어요. 본문 문장("프리페치 없으면 11, 친화성도 없으면 4.8, 단위 보폭만이면 2.7")은 선과 최적화를 한 칸씩 다르게 짝지은 것처럼 읽혀, 원문 안에서도 표기가 엇갈려요. 숫자(2.7 · 4.8 · 11 · 15)는 둘이 같아요. 구역 판정(노랑 · 초록 · 파랑)은 가장 낮은 · 가장 높은 천장으로 단순화한 설명용이에요. 곱셈·덧셈 균형은 커널에 따라 쉬움 · 어려움이 달라 천장 순서가 바뀌기도 해요(SpMV는 맨 아래).'),
    talk=say('fly', 'point', '천장 높이가 곧 보상이라니, 어디부터 손댈지 순서가 그림에 다 나와 있네. 이건 인정.') + xask('x1', '왜 천장마다 "아래 것부터 뚫어야" 해요?', '아래 천장일수록 거의 모든 코드에 기본으로 필요한 최적화예요. 예를 들어 SIMD를 안 쓰면 곱셈·덧셈 균형을 맞춰도 그 효과가 위로 드러나지 않아요. 논문은 그래서 쉬운 것부터 쌓았어요.'))

T4 = {'xeon': {'n': 'Intel Xeon (Clovertown)', 'peak': 75, 'bw': 11.2, 'ridge': 6.7, 'k': [['SpMV', 0.25, 2.8, 'M'], ['LBMHD', 1.07, 5.6, 'M'], ['Stencil', 0.50, 2.5, 'M'], ['3-D FFT', 1.64, 9.7, 'M']]},
      'x4': {'n': 'AMD Opteron X4 (Barcelona)', 'peak': 74, 'bw': 17.6, 'ridge': 4.4, 'k': [['SpMV', 0.25, 4.2, 'M'], ['LBMHD', 1.07, 11.4, 'M'], ['Stencil', 0.50, 8.0, 'M'], ['3-D FFT', 1.64, 14.0, 'M']]},
      't2': {'n': 'Sun UltraSPARC T2+ (Niagara 2)', 'peak': 19, 'bw': 36.7, 'ridge': 0.33, 'k': [['SpMV', 0.25, 7.3, 'M'], ['LBMHD', 0.70, 10.5, 'M'], ['Stencil', 0.33, 6.8, 'C'], ['3-D FFT', 1.09, 9.2, 'C']]},
      'cell': {'n': 'IBM Cell (QS20)', 'peak': 29, 'bw': 47.6, 'ridge': 0.65, 'k': [['SpMV', 0.25, 11.8, 'M'], ['LBMHD', 1.07, 16.7, 'M'], ['Stencil', 0.47, 14.2, 'C'], ['3-D FFT', 1.09, 15.7, 'C']]}}
r3 = level('③', 'r3', '결과 ③ — 네 컴퓨터 × 네 커널, 16개 모두 지붕 아래', [('g', '모델: 지붕선 검증'), ('p', '논문: 6장, 표 1 · 2 · 4, 그림 3 · 4')],
    pair=('연구실에서는', '네 실험실(설계가 다른 컴퓨터)에서 같은 네 실험(커널)을 해 보고, 결과가 미리 그린 상한선을 하나라도 넘는지 확인해요.',
          '논문에서는', '2소켓 멀티코어 넷과 일곱 난쟁이에서 고른 커널 넷(SpMV · LBMHD · Stencil · 3-D FFT). 16개 조합 <b>모두</b> 지붕과 천장 사이에 놓였어요. 작업 강도는 0.25 ~ 1.64(중앙값 <b>0.60</b>)인데 x86 두 대의 능선점은 <b>4.4 · 6.7</b> <span class="chip-src">원문</span>.'),
    panel=panel('표 4의 실측 성능을 지붕 위에 찍기', 'cFour', '선택한 컴퓨터의 지붕선과 네 커널의 실측 성능 점.',
                ctrl=btn_group('fM', '컴퓨터', [('xeon', 'Intel Xeon'), ('x4', 'AMD Opteron X4'), ('t2', 'Sun T2+'), ('cell', 'IBM Cell')]), kp_id='fK', ins_id='fI', wide=True),
    explain=explain('풀이', ['커널 넷: <b>SpMV</b>(희소 행렬 × 벡터, 0.17 → 0.25) · <b>LBMHD</b>(격자 볼츠만 자기유체, 0.70 → 1.07) · <b>Stencil</b>(256³ 3차원 열 방정식, 8 Flops / 24 바이트 = 0.33, 최적화 후 0.50) · <b>3-D FFT</b>(1.09 ~ 1.64).',
                             'Xeon은 최대 계산력이 가장 높지만 능선점 6.7 — 8바이트 피연산자 하나당 55 Flops를 해야 균형. 전면 버스가 일관성 통신까지 실어 대역폭이 반쯤 깎이기 때문이에요.',
                             'T2+는 대역폭이 가장 커서 능선점이 0.33으로 가장 낮아요. 프로그래밍이 <b>가장 쉬웠고</b>, 능선점이 가장 높은 Xeon은 최적화 전 성능이 가장 나빴어요. Cell은 성능이 가장 높았지만 SIMD 컴파일 · 로컬 저장소(DMA) 때문에 품이 들었어요.',
                             'Xeon · X4에서는 거의 다 메모리 한계, T2+ · Cell에서는 메모리 · 계산이 반반이에요.'],
                    limit='지붕은 표 1의 최대 계산력과 표 4의 "Stream BW" 천장(X4는 17.6, 표 1의 Stream은 16.6 — 논문 안의 두 값)으로 그렸어요. 그래서 이 그림의 능선점(계산값)이 논문이 적은 능선점과 조금 달라요(KPI에 둘 다 표시). 점은 표 4의 실측 GFlop/s와 작업 강도(3-D FFT는 128³) 그대로.'),
    talk=say('asst', 'report', '표 4: Cell의 SpMV는 11.8 GFlop/s · 47.1 GB/s, 작업 강도 0.25 — 비스듬한 지붕에 거의 붙었어요. 메모리를 거의 다 쓴 거예요.'))

FALL = [('모형이 캐시 · 프리페치를 무시한다', '작업 강도를 캐시 ↔ DRAM 왕래로 세니 캐시가 들어가 있고, 대역폭 측정에도 프리페치 등 메모리 최적화가 들어가 있다.'),
        ('캐시를 두 배로 하면 작업 강도가 오른다', '자동 튜닝 후 세 커널은 이미 필수 트래픽에 가까워 효과가 없다. 128³ FFT처럼 평면 하나가 캐시에 들어갈 때만 오른다.'),
        ('긴 메모리 지연시간을 무시한다', '"소프트웨어 프리페치 없음" 천장이 낮은 이유가 바로 지연시간을 못 숨겨서다.'),
        ('정수 연산 장치를 무시한다', '정수 명령이 많으면 실제로 성능이 깎인다(T2+). 명령어 비율 천장으로 다룬다.'),
        ('멀티코어와 상관없다', '리틀의 법칙: 메모리를 한계까지 쓰려면 동시성이 많아야 하고, 그건 멀티코어에서 더 쉽다.'),
        ('커널마다 모형을 다시 계산해야 한다', '지붕과 천장은 컴퓨터마다 한 번. 커널마다 바뀌는 건 작업 강도(가로 위치)와 천장 순서뿐.'),
        ('캐시가 안 맞는 쉬운 커널에만 맞다', '이 커널들도 캐시 적중률이 높다(Stencil 94% 이상, FFT 98% 이상). 그리고 쉽지 않았다 — 결과 셋이 큰 학회에 실렸다.'),
        ('부동소수점 프로그램에만 쓴다', 'FFT 전치 단계는 Flops가 0. "교환 횟수 / 바이트"(1/32)로 바꿔 그려도 된다(그림 5).'),
        ('DRAM 대역폭만 써야 한다', '작업 집합이 L2에 들어가면 L2 대역폭으로 그린다. 비스듬한 선이 위로, 능선점이 왼쪽으로 간다.')]
SHIFT = {'spmv': ['SpMV', 0.17, 0.25, '레지스터 블로킹'], 'lbm': ['LBMHD', 0.70, 1.07, '캐시 우회 쓰기(no-allocate store)'], 'fft': ['3-D FFT 128³', 1.09, 1.64, '평면 하나가 캐시에 들어감 (Xeon · X4)']}
r4 = level('④', 'r4', '결과 ④ — 작업 강도는 옮길 수 있다, 그리고 아홉 가지 오해', [('g', '모델: 3C ↔ 작업 강도'), ('p', '논문: 5장 · 6.3 · 7장')],
    pair=('연구실에서는', '시약을 매번 창고에서 꺼내 오던 실험을, 실험대 서랍에 두고 여러 번 쓰게 바꾸면 "창고 한 번 왕복당 실험 횟수"가 늘어요.',
          '논문에서는', '캐시 미스 3C 중 <b>필수 미스</b>가 트래픽의 최소량 = 작업 강도의 최대치를 정해요. <b>용량 · 충돌 미스</b>를 줄이면 작업 강도가 <b>오른쪽으로</b> 가서 다른 최적화 구역에 들어갈 수 있어요. 그래서 조언: <b>작업 강도부터 높여라</b> <span class="chip-src">원문</span>.'),
    panel=panel('작업 강도 옮기기 (Opteron X4 지붕 위)', 'cShift', 'X4 지붕선 위에서 최적화 전후 작업 강도 점이 오른쪽으로 옮겨 가는 그림.',
                ctrl=btn_group('sK2', '커널', [('spmv', 'SpMV'), ('lbm', 'LBMHD'), ('fft', '3-D FFT 128³')]) + btn_group('sA', '최적화', [('0', '전'), ('1', '후')]), kp_id='sK', ins_id='sI', wide=True),
    explain=explain('풀이', ['충돌 미스는 배열 덧대기(padding)로 캐시 줄 주소를 바꿔 줄여요.',
                             '캐시 우회 쓰기(no-allocate store)는 어차피 덮어쓸 데이터를 캐시에 올리지 않아 트래픽을 줄이고, 쓸모 있는 데이터를 밀어내지도 않아요.',
                             '아래 카드는 논문 7장 "오해"예요. 눌러서 저자의 답을 보세요.'],
                    limit='지붕 위에 그린 높이는 X4의 지붕선(표 1 정점 74 · 표 4 Stream 천장 17.6) 상한이며 실측값이 아니에요. LBMHD 0.70은 T2+에서만 남은 값(다른 셋은 1.07)이에요.'),
    bridge=bridge(gen=('LLM 추론에서 작업 강도를 오른쪽으로 옮기는 대표 방법은 <b>배치 키우기</b>(한 번 읽은 무게로 여러 손님 토큰 계산)와 FlashAttention처럼 <b>왕복 줄이기</b>예요.', '배치를 키우면 손님 한 명의 지연시간이 늘 수 있어요(1장 지연 · 처리량 맞바꿈).'),
                  field=('공장 자재 창고를 기계 옆 선반으로 옮겨 한 번 가져온 자재로 여러 부품을 찍는 것과 같아요.', '선반 크기(캐시)는 한정돼 있어요.')),
    talk='<div class="flipcards" id="flip">' + ''.join('<button aria-expanded="false"><b>오해 %d</b>%s<span class="a">→ %s</span></button>' % (i + 1, f[0], f[1]) for i, f in enumerate(FALL)) + '</div>'
         + say('fly', 'coffee', '캐시 · 프리페치 · 지연시간 · 정수 연산… 내가 처음에 지적한 게 다 저기 답이 있네. 빼먹은 게 아니라 천장으로 넣었구나.'))

lab = section('lab', '실험실', '실험실 — 오늘의 GPU로 지붕 다시 그리기', '''
<p>논문 결론: "루프라인은 GPU 같은 다른 시스템에도 통찰을 줄 것". 교재 3장 표의 숫자(FP8 밀집 계산력, HBM 대역폭)로 지붕을 그리고, LLM 디코드 · 프리필을 점으로 올려 봅니다. 무게가 FP8(1바이트/파라미터)이면 토큰 하나에 파라미터마다 연산 2번 → <b>작업 강도 ≈ 2 × (함께 처리하는 토큰 수)</b>.</p>''' + panel('LLM 지붕선 실험실', 'cLab', '선택한 GPU의 지붕선 위에 배치 크기에 따른 디코드 점과 프리필 점.',
    ctrl=btn_group('gG', 'GPU (교재 3장 표)', [('H100', 'H100'), ('H200', 'H200'), ('B200', 'B200'), ('L4', 'L4')]) + slider('gBt', '디코드 배치 (1 ~ 1024)', 0, 10, 1, 0, '') + slider('gN', '프리필 입력 토큰 (64 ~ 16384)', 6, 14, 1, 11, '') + slider('gC', '문맥 길이 (KV 캐시)', 0, 32768, 1024, 8192, '토큰') + btn_group('gK2', 'KV 캐시 읽기', [('0', '빼고 보기 (논문식 단순화)'), ('1', '넣어 보기')])
         + btn_group('gP', '모델 (FP8)', [('8', '8B'), ('70', '70B')], 1), kp_id='gK', ins_id='gI', wide=True)
    + '<p class="muted" style="font-size:14px">KV 캐시 크기는 교재 밖 가정이에요: 문맥 토큰 하나당 8B 모델 64 KB, 70B 모델 160 KB(Llama 계열 구조, KV를 8비트로 저장). 디코드 계산량에는 어텐션 계산을 넣지 않았어요.</p>' + say('moa', 'think', '배치를 1에서 늘리면 디코드 점이 비스듬한 지붕을 타고 올라가요. KV 캐시를 빼면 H100은 배치 약 300에서 능선점을 지나요. KV를 넣으면… 문맥 8천 토큰에선 거기까지 못 가네요!') + '<div class="quiz" data-quiz="lab"></div>', small='모형', tags=[('g', '설명용 근사 · 교재 3장 수치')]).replace('<div class="hexno">실험실<small>','<div class="hexno">실<small>')

duel_sec = section('duel', 'VS', '대결 — H100을 H200으로 바꾸면 배치 1 디코드가 빨라질까?', say('doc', 'think', '초파리는 "계산력이 똑같으니 그대로", 주판봇은 "대역폭만큼 빨라진다"고 해요. 루프라인으로 판정합니다.') + duel(
    'H100 → H200 (교재: FP8 계산력 둘 다 1,979 TF, 대역폭 3.35 → 4.8 TB/s), 70B · FP8 · 배치 1 디코드의 속도 상한은 몇 배?', '1.0배 — 그대로다', 'FLOPS가 같잖아. 계산기가 같으면 속도도 같지.', '약 1.43배 빨라진다', '배치 1이면 작업 강도 2야. 비스듬한 지붕 위라고! 대역폭만큼 간다.')
    + '<p class="notice">판정 기준: 도달 가능한 성능 = min(1,979 TF, 대역폭 × 작업 강도 2). 둘 다 비스듬한 쪽(메모리 한계)이면 비율 = 대역폭 비율 <span class="chip-src">원문</span>(교재 수치) + 논문 식.</p>', small='판', tags=[('g', '판정 기준: 루프라인 식')])

reread = section('reread', '다시', '다시 읽기 — 추론 엔지니어에게 루프라인이란', '''
<div class="cards"><div class="card"><h4>작업 강도 ↔ 배치 크기</h4><p>LLM 디코드는 배치가 작으면 작업 강도가 낮아 메모리 한계. 배치를 키우면 오른쪽으로 간다.</p><p class="lim">한계: KV 캐시 읽기는 배치와 함께 늘어 작업 강도를 깎는다.</p></div>
<div class="card"><h4>지붕 두 개 ↔ 3장의 두 숫자</h4><p>평평한 지붕 = FLOPS(프리필 · 이미지), 비스듬한 지붕 = 대역폭(디코드).</p><p class="lim">한계: 정밀도마다 평평한 지붕 높이가 다르다(FP8 vs FP4).</p></div>
<div class="card"><h4>천장 ↔ 커널 최적화</h4><p>텐서 코어 활용, 비동기 전송, 타일링(FlashAttention) — 천장을 하나씩 뚫는 일.</p><p class="lim">한계: GPU 천장은 CPU와 종류가 다르다.</p></div>
<div class="card"><h4>DRAM 말고 다른 층 ↔ 계층 루프라인</h4><p>L2 · SRAM · NVLink · InfiniBand 대역폭으로도 지붕을 그릴 수 있다(오해 9).</p><p class="lim">한계: 층이 늘면 그림이 복잡해진다.</p></div></div>
<div class="eq">성능 ≤ min( <b>최대 계산력</b>, <em>대역폭</em> × <i>작업 강도</i> ) &nbsp;·&nbsp; 능선점 = 최대 계산력 ÷ 대역폭 &nbsp;·&nbsp; H100 FP8 ≈ 1,979 ÷ 3.35 ≈ <b>591</b> Flops/byte</div>
''' + say('asst', 'spark', '교재 3장 + 이 논문 = "어떤 GPU를 고르고, 무엇을 최적화할지"를 한 장의 그림으로. 5주차에는 이 그림을 실제로 재는 도구(4.5 벤치마크)가 나와요.'), small='다시', tags=[('g', '교재 3장과 연결')])

onepage = section('sum', '한 장', '한 장으로', '''
<div class="tw"><table class="tb"><tr><th>무엇</th><th>논문 수치</th></tr>
<tr><td>식</td><td>도달 가능 GFlops/s = min(최대 계산력, 최대 메모리 대역폭 × 작업 강도)</td></tr>
<tr><td>그림 1a (Opteron X2)</td><td class="n">17.6 GFlops/s · 15 GB/s</td></tr>
<tr><td>그림 1b 능선점</td><td class="n">X2 1.0 → X4 4.4</td></tr>
<tr><td>그림 2 천장 (X2)</td><td class="n">계산 8.8 · 2.2 GFlops/s / 메모리 11 · 4.8 · 2.7 GB/s</td></tr>
<tr><td>능선점 (6장)</td><td class="n">Xeon 6.7 · X4 4.4 · T2+ 0.33 · Cell 0.65</td></tr>
<tr><td>16개 조합 작업 강도</td><td class="n">0.25 ~ 1.64, 중앙값 0.60 — 모두 지붕 아래</td></tr></table></div>
<div class="notebook"><h4>모아의 기록장 — 읽을 때 주의할 점</h4><ul><li>2008년 CPU(멀티코어) 대상 논문 — GPU는 결론에서 "확장 가능"으로만 언급</li><li>지붕은 예측값이 아니라 상한</li><li>능선점 수치는 그림 · 본문 기준, 표 값으로 다시 계산하면 조금 다를 수 있음</li><li>실험실의 GPU 지붕은 교재 3장 수치와 단순화한 작업 강도(2 × 토큰 수)로 그린 설명용</li></ul></div>
''' + say('moa', 'ok', '핵심 세 줄: 지붕 두 개 중 낮은 쪽 · 능선점이 난이도 · 천장 높이가 보상. 기록 완료!'), small='끝', tags=[('g', '요약')]).replace('<div class="hexno">한 장<small>','<div class="hexno">요약<small>')

outro = section('outro', '끝', '아웃트로', '<div class="outro"><div class="scene" data-img="sc_roofline_outro" role="img" aria-label="연구실 식구 여섯이 벽에 그린 지붕선 그래프 앞에 모인 장면"><img data-who="robo" data-mood="happy" alt=""><img data-who="doc" data-mood="magic" alt=""><img data-who="asst" data-mood="spark" alt=""><img data-who="sia" data-mood="proud" alt=""><img data-who="moa" data-mood="sparkle" alt=""><img data-who="fly" data-mood="coffee" alt=""></div></div>'
    + say('doc', 'magic', '논문의 한 줄: 성능은 <b>두 지붕 중 낮은 쪽</b>을 넘지 못한다. 어느 지붕 아래 있는지 알면 무엇을 고칠지 보인다.')
    + say('robo', 'happy', '배치 1 디코드는 대역폭 장사! 이번엔 내가 이겼어. 교재편에서 진 거 만회!')
    + say('fly', 'coffee', '…배치가 300을 넘으면 평평한 지붕이라는 것도 잊지 마. 그땐 FLOPS 쪽이 이겨.')
    + say('sia', 'signal', '4주차 끝! 5주차는 4장 소프트웨어와 페이지드 어텐션(vLLM) 논문입니다.')
    + say('x3', 'cheer', '(반짝)', name='방청석 X3'), small='', tags=())

GL = {'작업 강도': ['작업 강도 (operational intensity)', '지표', 'DRAM에서 가져온 1바이트당 연산 수. 캐시를 거친 뒤 트래픽으로 센다.'],
      '루프라인': ['루프라인 (Roofline)', '모형', '최대 계산력과 대역폭 × 작업 강도 중 낮은 쪽이 성능 상한임을 보여 주는 그림.'],
      '능선점': ['능선점 (ridge point)', '모형', '두 지붕이 만나는 점. 최대 성능에 필요한 최소 작업 강도.'], '천장': ['천장 (ceiling)', '모형', '특정 최적화를 하기 전에는 넘을 수 없는 선.'],
      '커널': ['커널 (kernel)', '용어', '성능을 재는 핵심 계산 단위.'], 'SpMV': ['SpMV (희소 행렬 × 벡터)', '커널', 'y = A·x, A는 희소 행렬. 작업 강도 0.17 ~ 0.25.'],
      'ILP': ['ILP (명령어 수준 병렬성)', '최적화', '한 스레드 안에서 독립된 명령을 겹쳐 실행하기. 루프 펼치기 등.'], 'SIMD': ['SIMD', '최적화', '명령 하나로 여러 데이터를 한꺼번에 처리.'],
      '프리페치': ['프리페치 (prefetch)', '최적화', '필요하기 전에 데이터를 미리 가져오기. 하드웨어 · 소프트웨어 둘 다.'], '메모리 친화성': ['메모리 친화성 (memory affinity)', '최적화', '데이터와 그걸 쓰는 스레드를 같은 칩-메모리 쌍에 두기.'],
      '단위 보폭': ['단위 보폭 접근 (unit stride)', '최적화', '메모리를 연속으로 읽기. 하드웨어 프리페치가 잘 걸린다.'], '3C': ['3C 캐시 미스', '모형', '필수(compulsory) · 용량(capacity) · 충돌(conflict) 미스.'],
      '암달의 법칙': ['암달의 법칙 (Amdahl\'s Law)', '모형', '병렬화 이득은 순차 부분에 묶인다. 한계·병목 분석의 대표 예.'], '리틀의 법칙': ['리틀의 법칙 (Little\'s Law)', '모형', '대기 중인 양 = 처리율 × 대기 시간. 대역폭을 다 쓰려면 동시 요청이 많아야 한다.'],
      'STREAM': ['STREAM 벤치마크', '측정', '메모리 대역폭을 재는 표준 측정. 저자들은 더 정확한 자체 측정을 썼다.'], '배치': ['배치 (batch)', '추론', '여러 요청의 토큰을 한 번에 처리하는 묶음.']}
CORE = ['작업 강도', '루프라인', '능선점', '천장', '커널', 'ILP', 'SIMD', '프리페치', '메모리 친화성', '3C', '배치']
QUIZ = {
 'q': [{'q': '논문이 지향한 모형의 성격은?', 'o': ['완벽한 예측', '통찰을 주는 한계·병목 그림', '통계 회귀식'], 'a': 1, 'why': '맞아요. 3C 모형처럼 불완전해도 통찰을 주면 된다는 입장이에요.', 'hint': '타임라인 마지막 칸.'},
       {'q': '한계·병목 분석의 대표 예로 논문이 든 것은?', 'o': ['암달의 법칙', '무어의 법칙', '굿하트의 법칙'], 'a': 0, 'why': '맞아요. 병렬 이득이 순차 부분에 묶인다는 법칙이에요.', 'hint': '타임라인 두 번째.'}],
 'method': [{'q': '[계산] 최대 17.6 GFlops/s, 대역폭 15 GB/s, 작업 강도 0.5인 커널의 상한은?', 'o': ['7.5 GFlops/s', '17.6 GFlops/s', '30 GFlops/s'], 'a': 0, 'why': '맞아요. min(17.6, 15 × 0.5 = 7.5) = 7.5 — 메모리 한계예요.', 'hint': '식에 넣어 보세요.'},
            {'q': '작업 강도를 셀 때의 바이트는?', 'o': ['프로세서 ↔ 캐시 왕래', '캐시를 거친 뒤 DRAM 왕래', '디스크 왕래'], 'a': 1, 'why': '맞아요. 그래서 캐시 최적화 효과가 작업 강도에 반영돼요.', 'hint': '풀이 1번.'}],
 'r1': [{'q': 'Opteron X4의 능선점(논문)은?', 'o': ['1.0', '4.4', '6.7'], 'a': 1, 'why': '맞아요. 6.7은 Xeon이에요.', 'hint': '짝 카드 오른쪽.'},
        {'q': '능선점이 오른쪽에 있다는 뜻은?', 'o': ['최대 성능 내기가 쉽다', '작업 강도가 아주 높은 커널만 최대 성능에 닿는다', '메모리가 크다'], 'a': 1, 'why': '맞아요. 그래서 프로그래밍 난이도의 지표가 돼요.', 'hint': '풀이 2번.'}],
 'r2': [{'q': '천장 사이의 높이가 뜻하는 것은?', 'o': ['그 최적화의 기대 보상', '전력 소모', '캐시 크기'], 'a': 0, 'why': '맞아요. 그림 2에선 ILP · SIMD와 메모리 친화성의 보상이 커요.', 'hint': '풀이 3번.'},
        {'q': '그림 2에서 ILP · SIMD가 없을 때 계산 천장은?', 'o': ['17.6', '8.8', '2.2'], 'a': 2, 'why': '맞아요. 균형만 없으면 8.8, ILP · SIMD까지 없으면 2.2 GFlops/s.', 'hint': '계산 최적화 "없음".'}],
 'r3': [{'q': '16개 조합의 작업 강도 중앙값은?', 'o': ['0.25', '0.60', '4.4'], 'a': 1, 'why': '맞아요. x86 능선점(4.4 · 6.7)보다 훨씬 왼쪽 — 대부분 메모리 한계였어요.', 'hint': '짝 카드.'},
        {'q': '프로그래밍이 가장 쉬웠던 컴퓨터는?', 'o': ['Intel Xeon', 'Sun T2+', 'IBM Cell'], 'a': 1, 'why': '맞아요. 능선점이 가장 낮고(0.33) 대역폭이 커서요.', 'hint': '풀이 3번.'}],
 'r4': [{'q': '논문의 조언: 다른 최적화보다 먼저 할 일은?', 'o': ['작업 강도 높이기', '클럭 올리기', '코어 늘리기'], 'a': 0, 'why': '맞아요. 작업 강도가 오른쪽으로 가면 최적화 구역 자체가 바뀌어요.', 'hint': '짝 카드.'},
        {'q': 'LBMHD의 작업 강도를 0.70 → 1.07로 올린 최적화는?', 'o': ['캐시 우회 쓰기', '레지스터 블로킹', 'DMA'], 'a': 0, 'why': '맞아요. SpMV는 레지스터 블로킹(0.17 → 0.25)이에요.', 'hint': '커널 단추 LBMHD.'}],
 'lab': [{'q': '[계산] H100 FP8의 능선점은 약?', 'o': ['59', '591', '5,910'], 'a': 1, 'why': '맞아요. 1,979 TF ÷ 3.35 TB/s ≈ 591 Flops/byte.', 'hint': 'KPI 줄.'},
         {'q': 'FP8 무게 디코드에서 배치 1의 작업 강도는 대략?', 'o': ['2', '591', '2,000'], 'a': 0, 'why': '맞아요. 바이트(파라미터)당 곱하기·더하기 2번. 능선점보다 한참 왼쪽 → 메모리 한계.', 'hint': '실험실 첫 문단.'}]}

N = lambda i, t, ko, en, a, d=None, s=None, lv=None: node(i, t, ko, en, a, P, d, (SRC, s) if s else None, lv)
KG = {'version': '1.0', 'page': P, 'nodes': [
    N('lab:method/roofline', 'Method', '루프라인 모형', 'Roofline model', '#method', '성능 상한 = min(최대 계산력, 대역폭 × 작업 강도)를 로그-로그 그림으로.', '3장', 2),
    N('lab:metric/operational-intensity', 'Metric', '작업 강도', 'operational intensity', '#method', 'DRAM 1바이트당 연산 수.', '3장', 2),
    N('lab:concept/ridge-point', 'Concept', '능선점', 'ridge point', '#r1', '최대 성능에 필요한 최소 작업 강도.', '3장', 2),
    N('lab:concept/ceiling', 'Concept', '천장', 'performance ceiling', '#r2', None, '4장', 3),
    N('lab:concept/compute-bound', 'Concept', '계산 한계', 'compute bound', '#method', None, '3장', 2),
    N('lab:concept/memory-bound', 'Concept', '메모리 한계', 'memory bound', '#method', None, '3장', 2),
    N('lab:concept/bound-bottleneck', 'Concept', '한계·병목 분석', 'bound and bottleneck analysis', '#q', None, '2장', 1),
    N('lab:concept/3c', 'Concept', '3C 캐시 미스', '3Cs model', '#r4', None, '5장', 2),
    N('lab:method/ilp-simd', 'Method', 'ILP · SIMD', 'ILP and SIMD', '#r2', None, '4장', 3), N('lab:method/fp-balance', 'Method', '곱셈·덧셈 균형', 'floating-point balance', '#r2', None, '4장', 3),
    N('lab:method/unit-stride', 'Method', '단위 보폭 접근', 'unit-stride access', '#r2', None, '4장', 3), N('lab:method/affinity', 'Method', '메모리 친화성', 'memory affinity', '#r2', None, '4장', 3),
    N('lab:method/sw-prefetch', 'Method', '소프트웨어 프리페치', 'software prefetching', '#r2', None, '4장', 3),
    N('lab:task/four-kernels', 'Task', '커널 넷 (SpMV · LBMHD · Stencil · 3-D FFT)', 'four kernels', '#r3', None, '표 2', 2),
    N('lab:dataset/four-machines', 'Dataset', '멀티코어 넷 (Xeon · X4 · T2+ · Cell)', 'four multicores', '#r3', None, '표 1', 2),
    node('lab:limitation/not-prediction', 'Limitation', '예측이 아니라 상한', 'bound, not prediction', '#method', P), node('lab:limitation/high-ridge', 'Limitation', '높은 능선점 = 최대 성능 내기 어려움', 'high ridge is hard', '#r1', P),
    node('lab:limitation/dram-only', 'Limitation', 'DRAM 한 층만 봄', 'single memory level', '#r4', P), node('lab:limitation/cpu-era', 'Limitation', '2008년 CPU 대상', 'CPU-era evaluation', '#sum', P),
    node('lab:claim/x2-x4', 'Claim', '능선점 X2 1.0 → X4 4.4', 'ridge shift X2 to X4', '#r1', P, None, (SRC, '그림 1b')),
    node('lab:claim/ceilings', 'Claim', 'X2 천장 8.8 · 2.2 GFlops/s, 11 · 4.8 · 2.7 GB/s', 'Opteron X2 ceilings', '#r2', P, None, (SRC, '그림 2')),
    node('lab:claim/all-bounded', 'Claim', '16개 조합 모두 지붕·천장 사이', 'all 16 cases bounded', '#r3', P, None, (SRC, '6.3.6, 표 4')),
    node('lab:claim/median-oi', 'Claim', '작업 강도 0.25 ~ 1.64, 중앙값 0.60', 'OI median 0.60', '#r3', P, None, (SRC, '8장')),
    node('lab:claim/t2-easiest', 'Claim', '능선점 가장 낮은 T2+가 가장 프로그래밍 쉬움', 'low ridge easiest', '#r3', P, None, (SRC, '6.3.5')),
    node('lab:analogy/roof', 'Analogy', '지붕에 닿는 기둥 ↔ 커널 작업 강도', 'column hits the roof', '#method', P), node('lab:analogy/ceilings', 'Analogy', '여러 겹의 천장 ↔ 최적화 순서', 'layered ceilings', '#r2', P),
    node('lab:question/core', 'Question', '무엇을 고쳐야 빨라지나 — 계산인가 메모리인가?', 'Compute or memory?', '#top', P),
    node('lab:question/duel', 'Question', '대결: H100 → H200, 배치 1 디코드는?', 'Duel: H100 vs H200', '#duel', P),
    node('lab:question/hierarchy', 'Question', 'SRAM · NVLink 등 여러 층을 한 그림에?', 'hierarchical roofline?', '#reread', P),
    node('lab:sim/roof', 'Simulation', '지붕선 그리기', 'roofline drawer', '#method', P), node('lab:sim/ridge', 'Simulation', 'X2 vs X4', 'ridge comparison', '#r1', P),
    node('lab:sim/ceil', 'Simulation', '천장 뚫기', 'ceiling breaker', '#r2', P), node('lab:sim/four', 'Simulation', '표 4 점 찍기', 'Table 4 plot', '#r3', P),
    node('lab:sim/shift', 'Simulation', '작업 강도 옮기기', 'OI shift', '#r4', P), node('lab:sim/llm', 'Simulation', 'LLM 지붕선 실험실', 'LLM roofline lab', '#lab', P),
    node('lab:work/' + SRC, 'Work', 'Williams 외 (2008)', 'Williams et al. 2008', '#top', P, 'Roofline 원 논문 (UCB/EECS-2008-134)'), node('lab:work/kiely2026inference', 'Work', 'Kiely (2026)', 'Kiely 2026', '#lab', P, '교재 Inference Engineering 3장 하드웨어')],
 'edges': [edge('lab:metric/operational-intensity', 'prerequisiteOf', 'lab:method/roofline', '#method'), edge('lab:concept/ridge-point', 'partOf', 'lab:method/roofline', '#r1'), edge('lab:concept/ceiling', 'partOf', 'lab:method/roofline', '#r2'),
           edge('lab:concept/bound-bottleneck', 'prerequisiteOf', 'lab:method/roofline', '#q'), edge('lab:method/roofline', 'hasLimitation', 'lab:limitation/not-prediction', '#method'), edge('lab:concept/ridge-point', 'hasLimitation', 'lab:limitation/high-ridge', '#r1'),
           edge('lab:method/roofline', 'hasLimitation', 'lab:limitation/dram-only', '#r4'), edge('lab:method/roofline', 'hasLimitation', 'lab:limitation/cpu-era', '#sum'), edge('lab:concept/3c', 'relatedTo', 'lab:metric/operational-intensity', '#r4'),
           edge('lab:concept/memory-bound', 'relatedTo', 'lab:method/roofline', '#method'), edge('lab:concept/compute-bound', 'relatedTo', 'lab:method/roofline', '#method')]
          + [edge(m, 'relatedTo', 'lab:concept/ceiling', '#r2') for m in ['lab:method/ilp-simd', 'lab:method/fp-balance', 'lab:method/unit-stride', 'lab:method/affinity', 'lab:method/sw-prefetch']]
          + [edge(c, 'assertedIn', 'lab:work/' + SRC, '#sum') for c in ['lab:claim/x2-x4', 'lab:claim/ceilings', 'lab:claim/all-bounded', 'lab:claim/median-oi', 'lab:claim/t2-easiest']]
          + [edge('lab:claim/all-bounded', 'supports', 'lab:method/roofline', '#r3'), edge('lab:claim/t2-easiest', 'supports', 'lab:concept/ridge-point', '#r3'), edge('lab:task/four-kernels', 'relatedTo', 'lab:dataset/four-machines', '#r3'),
             edge('lab:analogy/roof', 'relatedTo', 'lab:method/roofline', '#method'), edge('lab:analogy/ceilings', 'relatedTo', 'lab:concept/ceiling', '#r2'), edge('lab:limitation/dram-only', 'addressedBy', 'lab:question/hierarchy', '#reread'),
             edge('lab:sim/llm', 'relatedTo', 'lab:work/kiely2026inference', '#lab'), edge('lab:sim/ceil', 'relatedTo', 'lab:concept/ceiling', '#r2'), edge('lab:sim/four', 'relatedTo', 'lab:claim/all-bounded', '#r3'),
             edge('lab:sim/shift', 'relatedTo', 'lab:concept/3c', '#r4'), edge('lab:sim/roof', 'relatedTo', 'lab:method/roofline', '#method'), edge('lab:sim/ridge', 'relatedTo', 'lab:concept/ridge-point', '#r1')]}

DEFS = {'lab:concept/ceiling': '특정 최적화를 하기 전에는 넘을 수 없는, 지붕 아래의 가로선(계산) 또는 비스듬한 선(메모리).',
 'lab:concept/compute-bound': '커널의 작업 강도가 능선점보다 커서 평평한 지붕(최대 계산력)에 막힌 상태.',
 'lab:concept/memory-bound': '커널의 작업 강도가 능선점보다 작아 비스듬한 지붕(대역폭 × 작업 강도)에 막힌 상태.',
 'lab:concept/bound-bottleneck': '성능을 예측하는 대신 무엇이 성능을 막는지(한계)를 드러내는 분석. 암달의 법칙이 대표 예.',
 'lab:concept/3c': '캐시 미스의 세 종류(필수 · 용량 · 충돌). 필수 미스가 작업 강도의 최대치를 정한다.',
 'lab:method/ilp-simd': '최적화 ①: 명령어 수준 병렬성을 높이고(루프 펼치기) SIMD 명령을 쓴다.',
 'lab:method/fp-balance': '최적화 ②: 부동소수점 곱셈과 덧셈 수를 맞춰 곱셈-덧셈 장치를 다 쓴다.',
 'lab:method/unit-stride': '최적화 ③: 메모리를 연속으로 읽게 루프를 바꿔 하드웨어 프리페치를 켠다.',
 'lab:method/affinity': '최적화 ④: 데이터와 그 데이터를 쓰는 스레드를 같은 칩-메모리 쌍에 둔다.',
 'lab:method/sw-prefetch': '최적화 ⑤: 소프트웨어로 메모리 요청을 미리 많이 띄워 지연시간을 숨긴다.',
 'lab:task/four-kernels': '일곱 난쟁이에서 고른 SpMV · LBMHD · Stencil · 3-D FFT (표 2).',
 'lab:dataset/four-machines': '2소켓 멀티코어 넷: Intel Xeon, AMD Opteron X4, Sun UltraSPARC T2+, IBM Cell (표 1).',
 'lab:limitation/not-prediction': '루프라인은 넘을 수 없는 상한이지 실제 성능의 예측값이 아니다.',
 'lab:limitation/high-ridge': '능선점이 오른쪽일수록 작업 강도가 아주 높은 커널만 최대 성능에 닿는다.',
 'lab:limitation/dram-only': '이 논문의 기본 그림은 DRAM 한 층의 대역폭만 본다(L2 등으로 바꿔 그릴 수는 있음).',
 'lab:limitation/cpu-era': '2008년 멀티코어 CPU로 검증했고 GPU는 결론에서 확장 가능성만 언급했다.',
 'lab:claim/x2-x4': '같은 대역폭에 계산력만 네 배 남짓 늘자 능선점이 1.0에서 4.4로 이동(그림 1b).',
 'lab:claim/ceilings': 'Opteron X2 천장: 계산 8.8 · 2.2 GFlops/s, 메모리 11 · 4.8 · 2.7 GB/s(그림 2).',
 'lab:claim/all-bounded': '네 컴퓨터 × 네 커널 16개 조합의 실측 성능이 모두 지붕과 천장 사이에 놓였다(표 4).',
 'lab:claim/median-oi': '16개 조합의 작업 강도는 0.25~1.64, 중앙값 0.60 — x86 능선점(4.4 · 6.7)보다 한참 왼쪽.',
 'lab:claim/t2-easiest': '능선점이 가장 낮은 T2+가 프로그래밍이 가장 쉬웠고, 가장 높은 Xeon이 가장 어려웠다.',
 'lab:analogy/roof': '작업 강도라는 기둥을 세우면 평평한 지붕이나 비스듬한 지붕 중 한 곳에 닿는다는 논문의 비유.',
 'lab:analogy/ceilings': '실험실 천장이 여러 겹이라 정리(최적화)를 해야 한 겹씩 뚫고 올라간다는 비유.',
 'lab:question/core': '이 프로그램을 빠르게 하려면 계산을 고칠까, 메모리 통로를 고칠까?',
 'lab:question/duel': 'H100을 H200으로 바꾸면 배치 1 디코드 속도 상한은 몇 배가 될까?',
 'lab:question/hierarchy': 'SRAM · L2 · NVLink처럼 여러 층의 대역폭을 한 그림에 어떻게 함께 그릴까?',
 'lab:sim/roof': '최대 계산력 · 대역폭 · 작업 강도를 바꿔 지붕과 점을 그려 보는 계기판.',
 'lab:sim/ridge': 'Opteron X2와 X4의 지붕을 겹쳐 같은 커널의 속도 비를 보는 계기판.',
 'lab:sim/ceil': '그림 2의 천장을 최적화 단추로 하나씩 뚫어 보는 계기판.',
 'lab:sim/four': '표 4의 실측 성능을 컴퓨터별 지붕 위에 찍는 계기판.',
 'lab:sim/shift': '최적화 전후 작업 강도가 오른쪽으로 옮겨 가는 모습을 보는 계기판.',
 'lab:sim/llm': '교재 3장 GPU 수치로 LLM 디코드 · 프리필을 지붕 위에 올리는 실험실(KV 캐시 선택).'}
_miss = fill_defs(KG, DEFS)
assert not _miss, _miss
REFS = [ref(SRC, 'report', 'Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures', ['Samuel Williams', 'Andrew Waterman', 'David Patterson'], 2008, 'Technical Report UCB/EECS-2008-134, EECS Department, University of California, Berkeley', 'http://www.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.html', publisher='University of California, Berkeley', note='2008-10-17. CACM 52(4), 2009 게재판의 바탕'),
        book_ref()]
REFS[1]['lab']['role'] = 'background'

JS = r'''
Object.assign(L.C,{text:'#16212b',muted:'#5b6874',rule:'#d5dbe2',stain:'#9b3fb5',gfp:'#13733a',eye:'#c9302c',amber:'#a35c00',info:'#1e55c8',panel:'#f6f8fa',panel2:'#eef2f6',fly:'#c93030',robo:'#0b7a86',doc:'#7a3fd6',asst:'#c42a6e',sia:'#5a5a6e',moa:'#93651a'});
var C=L.C,F=L.FONT,fit=L.fit,grid=L.grid,stamp=L.stamp,T4=__T4__,SHIFT=__SHIFT__;
function f(v,d){return v.toLocaleString('ko-KR',{maximumFractionDigits:d==null?2:d})}
function oiTxt(v){return v>=1?f(v,2):'1/'+f(1/v,1)}
/* 로그-로그 지붕선 그리기: o={x0,x1,y0,y1,lines:[{p,b,c,lab,dash,w}],pts:[{x,y,c,lab}],v:[{x,c}],region:fn,yl,xl} */
function roof(cv,H,o){var W=fit(cv,H),x=cv.getContext('2d');x.clearRect(0,0,W,H);grid(x,W,H);var L0=56,R=W-16,T=14,B=H-34,lx0=Math.log10(o.x0),lx1=Math.log10(o.x1),ly0=Math.log10(o.y0),ly1=Math.log10(o.y1);
  function px(v){return L0+(R-L0)*(Math.log10(v)-lx0)/(lx1-lx0)}function py(v){return B-(B-T)*(Math.log10(v)-ly0)/(ly1-ly0)}
  x.font='11px '+F;x.fillStyle=C.muted;x.strokeStyle='rgba(22,33,43,.08)';
  for(var e=Math.ceil(lx0);e<=Math.floor(lx1);e++){var v=Math.pow(10,e);x.beginPath();x.moveTo(px(v),T);x.lineTo(px(v),B);x.stroke();x.textAlign='center';x.fillText(v>=1?String(v):String(v),px(v),B+14);}
  for(var e2=Math.ceil(ly0);e2<=Math.floor(ly1);e2++){var v2=Math.pow(10,e2);x.beginPath();x.moveTo(L0,py(v2));x.lineTo(R,py(v2));x.stroke();x.textAlign='right';x.fillText(String(v2),L0-6,py(v2)+4);}
  x.textAlign='center';x.fillText(o.xl||'작업 강도 (Flops/byte, 로그)',(L0+R)/2,H-4);x.save();x.translate(12,(T+B)/2);x.rotate(-Math.PI/2);x.fillText(o.yl||'GFlops/s (로그)',0,0);x.restore();
  x.save();x.beginPath();x.rect(L0,T,R-L0,B-T);x.clip();
  if(o.region)o.region(x,px,py,L0,R,T,B);
  (o.lines||[]).forEach(function(l){x.strokeStyle=l.c;x.lineWidth=l.w||2.5;x.setLineDash(l.dash||[]);x.beginPath();var n=80;for(var i=0;i<=n;i++){var xv=Math.pow(10,lx0+(lx1-lx0)*i/n),yv=Math.min(l.p,l.b*xv);i?x.lineTo(px(xv),py(yv)):x.moveTo(px(xv),py(yv));}x.stroke();x.setLineDash([]);
    if(l.lab&&W>=520){x.fillStyle=l.c;x.font='12px '+F;x.textAlign='right';x.fillText(l.lab,R-4,py(l.p)-6);}});
  (o.v||[]).forEach(function(v){x.strokeStyle=v.c||C.stain;x.lineWidth=1.5;x.setLineDash([5,4]);x.beginPath();x.moveTo(px(v.x),T);x.lineTo(px(v.x),B);x.stroke();x.setLineDash([]);});
  (o.pts||[]).forEach(function(p){x.fillStyle=p.c;x.beginPath();x.arc(px(p.x),py(p.y),p.r||6,0,7);x.fill();x.strokeStyle='#fff';x.lineWidth=1.5;x.stroke();if(p.lab){x.font='12px '+F;x.textAlign='left';var tw=x.measureText(p.lab).width,lx=px(p.x)+9,ly=py(p.y)+(p.dy||-6);if(lx+tw>R-2)lx=px(p.x)-9-tw;x.fillStyle='rgba(255,255,255,.88)';x.fillRect(lx-3,ly-12,tw+6,16);x.fillStyle=C.text;x.fillText(p.lab,lx,ly);}});
  x.restore();x.lineWidth=1;return {x:x,W:W,px:px,py:py};}
L.kpis('#heroK',[['min(·,·)','지붕 두 개 중 낮은 쪽','g'],['4 × 4','컴퓨터 × 커널','i'],['16/16','모두 지붕 아래','m'],['0.60','작업 강도 중앙값','a']]);
/* 방법 */
var cR=$('#cRoof'),rf=17.6,rb=15,ro=1;
function drawR(){var a=Math.min(rf,rb*ro);var g=roof(cR,320,{x0:1/8,x1:32,y0:0.5,y1:256,lines:[{p:rf,b:rb,c:C.gfp,lab:'최대 '+f(rf,1)+' GFlops/s'}],v:[{x:ro}],pts:[{x:ro,y:a,c:rb*ro<rf?C.amber:C.info,lab:f(a,1)+' GFlops/s'},{x:rf/rb,y:rf,c:C.stain,r:5,lab:'능선점 '+f(rf/rb,2),dy:18}]});stamp(g.x,g.W,'논문 식');}
function updR(){L.setTxt('#rFV',f(rf,1)+' GFlops/s');L.setTxt('#rBV',f(rb,1)+' GB/s');L.setTxt('#rOV',oiTxt(ro)+' Flops/B');var a=Math.min(rf,rb*ro),mem=rb*ro<rf;
  L.kpis('#rK',[[f(a,2),'도달 가능 GFlops/s',mem?'a':'i'],[mem?'메모리 한계':'계산 한계','점선이 닿는 지붕',mem?'a':'i'],[f(rf/rb,2),'능선점 (Flops/byte)','m']]);
  L.ins('#rI',[[mem?'a':'i',mem?'비스듬한 지붕 아래예요. 대역폭을 늘리거나 작업 강도를 높여야(오른쪽으로) 빨라져요.':'평평한 지붕 아래예요. 계산 쪽 최적화(또는 더 센 칩)만 도움이 돼요.'],['g','지붕은 컴퓨터마다 한 번 그리면 커널을 바꿔 가며 계속 쓸 수 있어요.']]);drawR();}
function syncR(){$('#rF').value=rf;$('#rB').value=rb;}
L.bindSeg('#rP',function(v){if(v==='x2'){rf=17.6;rb=15;syncR();}updR();});$('#rF').addEventListener('input',function(){rf=+this.value;updR()});$('#rB').addEventListener('input',function(){rb=+this.value;updR()});
$('#rO').addEventListener('input',function(){ro=Math.pow(2,+this.value);updR()});L.addMod(cR,function(dt){if(dt===0)drawR()});updR();
/* ① 능선점 */
var cK=$('#cRidge'),ko=0.5,X2={p:17.6,b:15},X4={p:74,b:16.6};
function drawK(){var g=roof(cK,300,{x0:1/8,x1:16,y0:1,y1:128,lines:[{p:X4.p,b:X4.b,c:C.info,lab:'Opteron X4 (표 1)'},{p:X2.p,b:X2.b,c:C.gfp,lab:'Opteron X2'}],v:[{x:ko}],
  pts:[{x:ko,y:Math.min(X2.p,X2.b*ko),c:C.gfp},{x:ko,y:Math.min(X4.p,X4.b*ko),c:C.info,lab:'×'+f(Math.min(X4.p,X4.b*ko)/Math.min(X2.p,X2.b*ko),2)}]});stamp(g.x,g.W,'그림 1a · 표 1 값');}
function updK(){L.setTxt('#kOV',oiTxt(ko)+' Flops/B');var a=Math.min(X2.p,X2.b*ko),b=Math.min(X4.p,X4.b*ko),r=b/a;
  L.kpis('#kK',[[f(a,1),'X2 상한 (GFlops/s)','g'],[f(b,1),'X4 상한 (GFlops/s)','i'],['×'+f(r,2),'X4 ÷ X2',r>1.05?'g':'r']]);
  L.ins('#kI',[[r>1.05?'g':'r',r>1.05?'작업 강도가 X2의 능선점보다 커서 X4의 넓은 실험대를 써먹어요.':'둘 다 같은 대역폭의 비스듬한 지붕 아래 — 계산력이 네 배여도 그대로예요.'],['i','논문: X4에서 이득을 보려면 작업 강도가 1보다 커야 한다.']]);drawK();}
$('#kO').addEventListener('input',function(){ko=Math.pow(2,+this.value);updK()});L.addMod(cK,function(dt){if(dt===0)drawK()});updK();
/* ② 천장 */
var cQ=$('#cCeil'),cc=0,cm=0,co=1,CC=[2.2,8.8,17.6],CM=[2.7,4.8,11,15],CCN=['스레드 병렬만','+ ILP · SIMD','+ 곱셈·덧셈 균형 (지붕)'],CMN=['③ 단위 보폭만','④ 메모리 친화성 천장','⑤ 소프트웨어 프리페치 천장','측정 대역폭 지붕'];
function region(o){return CM[3]*o<=CC[0]?'mem':CM[0]*o>=CC[2]?'comp':'both'}
function drawQ(){var lines=[];CM.forEach(function(b,i){lines.push({p:1e9,b:b,c:i<=cm?C.amber:'rgba(163,92,0,.3)',w:i===3?2.5:1.5,dash:i===3?[]:[6,4]})});
  CC.forEach(function(p,i){lines.push({p:p,b:1e9,c:i<=cc?C.info:'rgba(30,85,200,.3)',w:i===2?2.5:1.5,dash:i===2?[]:[6,4],lab:f(p,1)})});
  var a=Math.min(CC[cc],CM[cm]*co);
  var g=roof(cQ,330,{x0:1/8,x1:16,y0:0.5,y1:32,lines:lines,v:[{x:co}],region:function(x,px,py,L0,R,T,B){var xa=CC[0]/CM[3],xb=CC[2]/CM[0];x.fillStyle='rgba(163,92,0,.16)';x.fillRect(L0,T,px(xa)-L0,B-T);x.fillStyle='rgba(19,115,58,.14)';x.fillRect(px(xa),T,px(xb)-px(xa),B-T);x.fillStyle='rgba(30,85,200,.14)';x.fillRect(px(xb),T,R-px(xb),B-T);x.font='700 12px '+F;x.textAlign='center';x.fillStyle=C.amber;x.textAlign='left';x.fillText('메모리만',L0+3,B-8);x.textAlign='center';x.fillStyle=C.gfp;x.fillText('둘 다',(px(xa)+px(xb))/2,B-8);x.fillStyle=C.info;x.fillText('계산만',(px(xb)+R)/2,B-8);},
    pts:[{x:co,y:a,c:C.stain,lab:'지금 상한 '+f(a,1)}]});stamp(g.x,g.W,'그림 2 값 · 구역은 단순화');}
function updQ(){L.setTxt('#cOV',oiTxt(co)+' Flops/B');var a=Math.min(CC[cc],CM[cm]*co),bind=CM[cm]*co<CC[cc]?'mem':'comp',rg=region(co),
  nxt=bind==='mem'?(cm<3?Math.min(CC[cc],CM[cm+1]*co):a):(cc<2?Math.min(CC[cc+1],CM[cm]*co):a);
  L.kpis('#qK',[[f(a,2),'지금 상한 (GFlops/s)','m'],[bind==='mem'?'메모리 천장':'계산 천장','막고 있는 것',bind==='mem'?'a':'i'],['+'+f(nxt-a,2),'다음 최적화의 기대 보상','g'],[rg==='mem'?'노랑':rg==='comp'?'파랑':'초록','구역',rg==='mem'?'a':rg==='comp'?'i':'g']]);
  L.ins('#qI',[[bind==='mem'?'a':'i','지금 막는 천장: '+(bind==='mem'?CMN[cm]+' ('+CM[cm]+' GB/s)':CCN[cc]+' ('+CC[cc]+' GFlops/s)')+'. '+(nxt>a?'다음 '+(bind==='mem'?'메모리':'계산')+' 최적화를 켜 보세요.':'이 방향으론 더 오를 곳이 없어요 — 다른 쪽 천장을 보세요.')],
    ['g',rg==='mem'?'노란 구역: 메모리 최적화만 해 보라는 뜻이에요.':rg==='comp'?'파란 구역: 계산 최적화만 해 보라는 뜻이에요.':'초록 구역: 두 종류 다 해 볼 만해요(그림 2c의 커널 1).']]);drawQ();}
L.bindSeg('#cC',function(v){cc=+v;updQ()});L.bindSeg('#cM',function(v){cm=+v;updQ()});$('#cO').addEventListener('input',function(){co=Math.pow(2,+this.value);updQ()});L.addMod(cQ,function(dt){if(dt===0)drawQ()});updQ();
/* ③ 네 컴퓨터 */
var cF=$('#cFour'),fm='xeon',KC=['#c9302c','#13733a','#9b3fb5','#1e55c8'];
function drawF(){var m=T4[fm];var g=roof(cF,320,{x0:1/8,x1:16,y0:0.5,y1:128,lines:[{p:m.peak,b:m.bw,c:C.text,lab:'최대 '+m.peak+' GFlops/s'}],
  pts:m.k.map(function(k,i){return {x:k[1],y:k[2],c:KC[i],lab:k[0]+' '+k[2],dy:i%2?16:-6}})});stamp(g.x,g.W,'표 1 · 표 4 값');}
function updF(){var m=T4[fm],mem=m.k.filter(function(k){return k[3]==='M'}).length,eff=m.k.map(function(k){return k[2]/Math.min(m.peak,m.bw*k[1])});
  L.kpis('#fK',[[f(m.peak/m.bw,2),'그린 능선점 (계산)','i'],[String(m.ridge),'논문 능선점','m'],[mem+' / 4','위쪽 천장이 메모리인 커널','a'],[f(Math.max.apply(0,eff)*100,0)+'%','지붕 대비 가장 가까운 점','g']]);
  L.ins('#fI',[['i',m.n+': '+(fm==='xeon'?'최대 계산력은 가장 높지만 능선점이 가장 오른쪽. 네 점 모두 비스듬한 지붕 아래 — 메모리 한계.':fm==='x4'?'Xeon보다 능선점이 왼쪽. 이것저것 최적화가 가장 많이 먹혔지만 메모리 동작은 Xeon보다 이해하기 쉬웠다.':fm==='t2'?'능선점이 가장 낮아 Stencil · FFT는 평평한 지붕 쪽. 프로그래밍이 가장 쉬웠다.':'성능이 가장 높다. SpMV는 지붕선에 거의 붙었다(47.1 GB/s).')],['g','네 점 모두 지붕을 넘지 않아요 — 16개 조합 전부 같은 결과.']]);drawF();}
L.bindSeg('#fM',function(v){fm=v;updF()});L.addMod(cF,function(dt){if(dt===0)drawF()});updF();
/* ④ 옮기기 */
var cS=$('#cShift'),sk='spmv',sa=0,XP=74,XB=17.6;
function drawS(){var s=SHIFT[sk],o=sa?s[2]:s[1];var g=roof(cS,280,{x0:1/8,x1:16,y0:1,y1:128,lines:[{p:XP,b:XB,c:C.text,lab:'Opteron X4'}],v:[{x:o}],
  pts:[{x:s[1],y:Math.min(XP,XB*s[1]),c:'rgba(201,48,44,.45)',lab:'전 '+s[1]},{x:s[2],y:Math.min(XP,XB*s[2]),c:sa?C.gfp:'rgba(19,115,58,.35)',lab:'후 '+s[2],dy:18}]});stamp(g.x,g.W,'높이는 지붕 상한');}
function updS(){var s=SHIFT[sk],r=Math.min(XP,XB*s[2])/Math.min(XP,XB*s[1]);L.kpis('#sK',[[s[1]+' → '+s[2],'작업 강도 (Flops/byte)','g'],['×'+f(r,2),'지붕 상한 변화','i'],[s[3],'쓴 최적화','m']]);
  L.ins('#sI',[['g',sa?'점이 오른쪽으로 옮겨 가 비스듬한 지붕을 타고 올라갔어요. 같은 대역폭으로 더 많은 계산.':'최적화 "후"를 눌러 점을 옮겨 보세요.']]);drawS();}
L.bindSeg('#sK2',function(v){sk=v;updS()});L.bindSeg('#sA',function(v){sa=+v;updS()});L.addMod(cS,function(dt){if(dt===0)drawS()});updS();
$$('#flip button').forEach(function(b){b.addEventListener('click',function(){b.setAttribute('aria-expanded',b.getAttribute('aria-expanded')==='true'?'false':'true')})});
/* 실험실 */
var cL=$('#cLab'),gg='H100',gb=1,gn=2048,gp=70,gc=8192,gk=0,GPU={H100:[1979,3.35,80],H200:[1979,4.8,141],B200:[5000,8,192],L4:[242,0.3,24]},KVB={8:65536,70:163840};
function dstep(){var W=gp*1e9,kv=gk?gb*gc*KVB[gp]:0,fl=2*gp*1e9*gb;return {oi:fl/(W+kv),kvGB:gb*gc*KVB[gp]/1e9}}
function drawL(){var g=GPU[gg],P=g[0],B=g[1],d=dstep(),od=d.oi,op=2*gn,ad=Math.min(P,B*od),ap=Math.min(P,B*op);
  var r=roof(cL,330,{x0:1,x1:16384,y0:0.5,y1:20000,yl:'TFLOPS (로그)',lines:[{p:P,b:B,c:C.text,lab:gg+' FP8 '+f(P,0)+' TF'}],
    pts:[{x:od,y:ad,c:C.amber,lab:'디코드 (배치 '+gb+(gk?', KV 포함':'')+')',dy:-12},{x:op,y:ap,c:C.info,lab:'프리필 ('+gn+'토큰)',dy:20},{x:P/B,y:P,c:C.stain,r:5,lab:'능선점 '+f(P/B,0),dy:-14}]});stamp(r.x,r.W,gk?'설명용: KV 캐시 = Llama 계열 구조 가정':'설명용: 작업 강도 ≈ 2 × 토큰 수, KV 캐시 무시');}
function updL(){L.setTxt('#gBtV',String(gb));L.setTxt('#gNV',String(gn));L.setTxt('#gCV',f(gc,0)+'토큰');var g=GPU[gg],P=g[0],B=g[1],d=dstep(),ad=Math.min(P,B*d.oi),tps=ad*1e12/(2*gp*1e9),w=gp,need=w*1.5,oom=w+d.kvGB>g[2];
  L.kpis('#gK',[[f(P/B,0),'능선점 (Flops/byte)','m'],[B*d.oi<P?'메모리':'계산','디코드가 닿는 지붕',B*d.oi<P?'a':'i'],[f(tps,0),'디코드 합계 토큰/초 상한','g'],[f(tps/gb,0),'손님 1명당 토큰/초 상한','i'],
    [oom?'OOM':need>g[2]?'여유 부족':'여유 있음',gg+' 한 장 메모리 ('+g[2]+' GB) · 무게 '+w+' GB'+(gk?' + KV '+f(d.kvGB,1)+' GB':''),oom?'r':need>g[2]?'a':'g']]);
  L.ins('#gI',[[B*d.oi<P?'a':'i',B*d.oi<P?'배치 '+gb+'에서는 메모리 한계 — 배치를 키우면 같은 무게 읽기로 더 많은 손님을 처리해 합계 처리량이 늘어요.':'능선점을 넘었어요. 이제 배치를 더 키워도 합계 처리량은 늘지 않고 손님당 속도만 줄어요.'],
    [gk?'r':'i',gk?'KV 캐시를 넣으면 손님마다 문맥 '+f(gc,0)+'토큰의 KV('+f(d.kvGB/gb,2)+' GB)를 매 토큰 읽어요. 배치를 키워도 작업 강도가 '+f(d.oi,0)+'에서 멈춰 능선점에 잘 못 닿아요 — 긴 문맥 서빙이 메모리 한계에 머무는 이유예요.':'"KV 캐시 읽기: 넣어 보기"를 누르면 긴 문맥에서 능선점이 얼마나 멀어지는지 보여요.'],
    [oom||need>g[2]?'r':'g',oom?'이 GPU 한 장에는 무게와 KV 캐시가 다 안 들어가요(OOM). 실제로는 여러 장으로 나눠야 해요(교재 5.4).':need>g[2]?'무게는 들어가지만 교재 경험칙(무게 × 1.5 = '+f(need,0)+' GB)에 못 미쳐요. 실제 서빙은 2장 이상을 권해요.':'교재 경험칙(무게 × 1.5)도 만족해요.'],
    ['g','프리필('+gn+'토큰)은 작업 강도 '+f(2*gn,0)+'로 '+(2*gn>P/B?'평평한 지붕 — 계산 한계(교재 3.1.1과 같은 결론).':'아직 비스듬한 지붕 — 입력이 짧으면 프리필도 메모리 한계일 수 있어요.')]]);drawL();}
L.bindSeg('#gG',function(v){gg=v;updL()});$('#gBt').addEventListener('input',function(){gb=Math.pow(2,+this.value);updL()});$('#gN').addEventListener('input',function(){gn=Math.pow(2,+this.value);updL()});
$('#gC').addEventListener('input',function(){gc=Math.max(1,+this.value);updL()});L.bindSeg('#gK2',function(v){gk=+v;updL()});L.bindSeg('#gP',function(v){gp=+v;updL()});L.addMod(cL,function(dt){if(dt===0)drawL()});updL();
/* 대결 */
L.Duel({fmt:function(v){return v.toFixed(2)+'배'},run:function(){var h1=Math.min(1979,3.35*2),h2=Math.min(1979,4.8*2),r=h2/h1;
  return {fly:1,robo:r,res:'R',bars:[['f','초파리 (FLOPS 비율)',1],['r','주판봇 (루프라인 계산)',r]],asst:'배치 1이면 작업 강도 2, 능선점 591 · 412보다 한참 왼쪽이에요. 둘 다 비스듬한 지붕이라 상한 비율 = 4.8 ÷ 3.35 ≈ '+r.toFixed(2)+'배.',
  verdict:'메모리 한계에서는 대역폭이 속도다. 주판봇 승.',note:'초파리 말도 반은 맞아요: 프리필처럼 평평한 지붕 쪽 일은 정말 1.0배예요. 실험실에서 배치를 300 넘게 올려 보세요. (상한 근사, 효율 100% 가정)'};}});
'''.replace('__T4__', _j.dumps(T4, ensure_ascii=False)).replace('__SHIFT__', _j.dumps(SHIFT, ensure_ascii=False))

def spec():
    return {'meta': {'title': '루프라인 — 지붕 두 개로 성능의 상한을 그린다 (Roofline 연구실 해설)', 'description': '인퍼런스 스터디 북 4주차 논문: Williams · Waterman · Patterson (2008) Roofline — 작업 강도, 능선점, 천장, 네 멀티코어 × 네 커널, 오늘의 GPU로 다시 그리기',
                     'series': '인퍼런스 스터디 북', 'number': '04-A1', 'slug': 'roofline', 'version': '1.0', 'date': '2026-11-14', 'creator': ['안상선'], 'license': 'CC BY-NC 4.0 (캐릭터 제외)', 'url': URL,
                     'kgStart': 'lab:method/roofline', 'citeKey': 'ahn2026roofline', 'domain': 'ai',
                     'suggestedCitation': '안상선 (2026). 루프라인 — 지붕 두 개로 성능의 상한을 그린다. 인퍼런스 스터디 북 4주차 논문 해설. ' + URL},
            'kg': KG, 'refs': REFS, 'gl': GL, 'core': CORE, 'quiz': QUIZ, 'js': JS, 'css': LIGHT,
            'nav': nav([('cast', '식구'), ('q', '1 질문'), ('method', '2 지붕'), ('r1', '결과①'), ('r2', '결과②'), ('r3', '결과③'), ('r4', '결과④'), ('lab', '실험실'), ('duel', '대결'), ('reread', '다시 읽기'), ('sum', '한 장'), ('teach', '강의자'), ('kg', '색인'), ('export', '꾸러미')]),
            'body': cover('cover_roofline', '인퍼런스 스터디 북 · 4주차 · 논문', '연구실 식구 여섯이 벽에 그려진 지붕 모양 그래프 앞에 모인 대체 표지',
                          motif=''.join('<i class="%s"></i>' % c for c in ['a', 'a', 'm', 'on', 'on', 'on', 'a', 'm', 'on', 'on', 'on', 'on']),
                          moods={'doc': 'board', 'asst': 'report', 'fly': 'arms', 'robo': 'chart', 'sia': 'explain', 'moa': 'report'})
                    + hero + cast + q + method + r1 + r2 + r3 + r4 + lab + duel_sec + reread + onepage + outro + teach_appendix(QUIZ, {'q': '1 질문', 'method': '2 지붕', 'r1': '결과 ①', 'r2': '결과 ②', 'r3': '결과 ③', 'r4': '결과 ④', 'lab': '실험실'}),
            'footer': footer([('논문', 'Williams, S., Waterman, A., & Patterson, D. (2008). Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures. Tech. Rep. UCB/EECS-2008-134, UC Berkeley'),
                              ('그림 1 · 2', '논문 3 · 4장 Opteron X2 · X4 수치 (원문 그대로)'), ('표 1 · 4', '논문 6장 네 멀티코어 사양과 실측 성능 (원문 그대로)'), ('실험실 GPU 수치', 'Kiely (2026) Inference Engineering 3장 표')],
                             ['결과 ① X4 지붕(능선점 4.4로 역산)', '결과 ② 구역 판정(가장 낮은 · 높은 천장으로 단순화)', '실험실 작업 강도 ≈ 2 × 토큰 수(KV 캐시 · 어텐션 무시)', '대결의 비율(효율 100% 상한)'],
                             prev=('../week_04_textbook_ch03/', '4주차 교재 3장 하드웨어'), nxt=None, ver='v1.14 (낮의 연구실)')}

if __name__ == '__main__':
    out = os.path.join(sys.argv[1], SLUG, 'index.html')
    print(out, build(spec(), out))
