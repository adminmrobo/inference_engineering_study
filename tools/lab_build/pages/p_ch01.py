# -*- coding: utf-8 -*-
import os, sys, json as _j
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import *
from parts import *
from series import BASE

SLUG = 'week_01_textbook_ch01'; P = 'ch01'; URL = BASE + SLUG + '/'

hero = '''<header class="hero" id="top"><div class="wrap"><div class="hero-text">
<p class="eyebrow">인퍼런스 스터디 북 · 1주차 교재 · 1장 Prerequisites (1.1–1.4)</p>
<h1>시작 전에 정할 것</h1>
<p class="q">"가장 빠른 모델"이 아니라 "우리 제품에 가장 알맞은 모델"을 고르려면, 먼저 무엇을 알아야 할까?</p>
<p>최적화는 여러 선택지 중 <b>최선</b>을 고르는 일입니다. 그런데 무엇이 최선인지는 제품마다 다릅니다. 1장은 추론 엔지니어링에 들어가기 전에 정해야 할 것 — 공유 API와 전용 배포, 앱의 성격, 모델 고르기와 평가, 그리고 지연시간·처리량을 재는 법 — 을 정리합니다.</p>
<div class="kpis" id="heroK"></div>
<p class="cite">교재: Kiely, P. (2026). <i>Inference Engineering</i>, Chapter 1 Prerequisites, 1.1–1.4. Baseten Books.</p>
<div class="dialog">''' + say('doc', 'front', '미식축구 선수는 크고 빠르고 힘이 세지만, 스모 선수만큼 크지도, 단거리 선수만큼 빠르지도 않아요. 자기 포지션에 맞게 다듬어진 거죠. 추론 서비스도 그래요.') + say('asst', 'smile', '1장 표 세 개와 그림 다섯 장을 따라가요. 계산기는 제가 맡을게요.') + say('fly', 'point', '평균 지연시간만 보면 되는 거 아냐? 왜 P99 같은 걸 따져?') + say('robo', 'chart', '모델은 클수록 똑똑하지! 제일 큰 걸로 시작하면 손해 볼 일 없어.') + say('sia', 'explain', '오늘은 다섯 칸입니다. 균형 → 공유와 전용 → 앱의 성격 → 모델 고르기 → 측정.') + say('moa', 'cheer', '1장 끝의 대결은 "평균 대 P99"예요. 미리 응원할 쪽 정해 두세요!') + '''</div></div></div></header>'''

cast = crew({'doc': '해설·심판. "최선"의 정의부터', 'asst': '숫자 발표. 비용·백분위 계산', 'fly': '꼬리(P99)를 의심하는 쪽', 'robo': '평균·큰 모델을 믿는 쪽',
             'sia': '순서표·진행 신호', 'moa': '기록장·응원', 'x1': '방청석', 'x2': '방청석', 'x3': '방청석'},
            extra='<h3>오늘의 순서</h3>' + route([('lv1', '① 칸', '최적화는 균형'), ('lv2', '② 칸', '1.1 공유와 전용'), ('lv3', '③ 칸', '1.2 앱의 성격'), ('lv4', '④ 칸', '1.3 모델 고르기'), ('lv5', '⑤ 칸', '1.4 재는 법'), ('duel', '대결', '평균 vs P99'), ('sum', '정리', '체크리스트')]))

KNOWS = [('model', '모델 요구사항', '어떤 모델(들)을 돌려야 하나?'), ('iface', '애플리케이션 인터페이스', '입력은 어떻게 오고, 출력은 어떤 형식이어야 하나?'), ('lat', '지연시간 예산', '사용자 행동에 제품이 처음부터 끝까지 얼마나 빨리 답해야 하나?'),
         ('unit', '단위 경제학', '요청당·사용자당·월마다 얼마까지 쓰는 게 맞나?'), ('usage', '사용 패턴', '동시 사용자는 몇 명이고, 업무 시간에 몰리는 식의 패턴이 있나?')]
lv1 = level(1, 'lv1', '최적화는 균형 — 다섯 가지 알아 둘 것', [('g', '모델: 지연시간·처리량·품질의 균형'), ('p', '교재: 1장 도입, 그림 1.1')],
    pair=('연구실에서는', '실험 장비를 고를 때 "제일 좋은 것"은 없어요. 시료가 몇 개인지, 얼마나 정밀해야 하는지, 예산이 얼마인지가 정해져야 고를 수 있어요.', '모델에서는', '많은 성능 개선은 <b>지연시간·처리량·품질</b> 사이의 거래에서 나옵니다. 그래서 한 가지를 끝까지 올리기보다 알맞은 균형을 찾는 일이 많아요. <b>제약을 많이 알수록</b> 결과가 좋아집니다 <span class="chip-src">원문</span>.'),
    panel=panel('알고 있는 것에 체크해 보세요', 'cKnow', '알고 있는 제약의 개수만큼 최적화할 수 있는 방향이 좁혀지는 모습을 과녁으로 그린 설명용 도식.',
                ctrl='<div class="group" id="kn">' + ''.join('<button class="bt" data-k="%s" aria-pressed="false">%s</button>' % (k, n) for k, n, _ in KNOWS) + '</div>', ins_id='kI'),
    explain=explain('풀이', ['다섯 가지: 모델 요구사항, 애플리케이션 인터페이스, 지연시간 예산, 단위 경제학, 사용 패턴.', '제품 초기에는 이 답들이 흐릿합니다. 그때는 <b>기성 API</b>를 쓰는 편이 대개 낫다고 교재는 말해요.', '제품이 커지고 요구사항이 또렷해지면, 그때 추론 엔지니어링이 할 만한 일이 됩니다.'],
                    limit='과녁 그림은 "아는 만큼 좁혀진다"는 생각을 보여 주는 설명용이에요. 다섯 가지 중 무엇이 먼저 정해지는지는 제품마다 다릅니다.'),
    talk=say('robo', 'sigh', '"제일 좋은 것"이 없다니… 그럼 가장 비싼 걸 사도 소용없을 때가 있다는 거네.'))

lv2 = level(2, 'lv2', '1.1 공유 추론과 전용 배포', [('g', '모델: 과금 방식'), ('p', '교재: 1.1, 표')],
    pair=('연구실에서는', '분석을 외부에 맡기면 건당 돈을 내고, 장비를 들이면 시간당 비용이 나가요. 시료가 적을 땐 외부, 많아지면 장비가 이득입니다.', '모델에서는', '<b>공유 추론</b>은 공개 API에 보내고 백만 토큰당 돈을 내요. <b>전용 배포</b>는 GPU를 빌려 우리만의 서비스를 두고 GPU 시간당 돈을 냅니다 <span class="chip-src">원문</span>. 공유 vs 전용은 닫힌 vs 열린 모델과 꼭 같은 얘기는 아니에요.'),
    panel=panel('언제 전용 배포가 싸질까? (교차점 계산기)', 'cCost', '월 사용량에 따른 공유 API 비용(직선)과 전용 배포 비용(계단). 단가는 모두 설명용입니다.',
                ctrl=slider('cV', '월 토큰', 1, 2000, 1, 300, '백만') + slider('cP', '백만 토큰당 가격', 0.5, 10, 0.5, 3, '') + slider('cG', 'GPU 시간당', 1, 10, 0.5, 4, '') + slider('cT', 'GPU 처리량', 200, 5000, 100, 1500, '토큰/초'),
                kp_id='cK', eq='공유 = 월 토큰(백만) × 단가 &nbsp;·&nbsp; 전용 = ⌈필요 GPU⌉ × 730시간 × GPU 시간당 가격 (필요 GPU = 월 토큰 ÷ (처리량 × 3,600 × 730))', ins_id='cI')
          + '''<div class="tw"><table class="tb"><tr><th>공유 추론의 장점</th><th>공유 추론의 단점</th></tr><tr><td>쓴 만큼만, 운영 부담 0</td><td>비용이 사용량에 비례해 늘어남</td></tr><tr><td>콜드 스타트 없음, 늘 켜져 있음</td><td>제공자 가동률이 우리 제품 가동률의 상한, 시끄러운 이웃</td></tr><tr><td>엔지니어링 거의 없음, API 키만</td><td>지연시간·모델 품질·속도 제한을 못 정함</td></tr></table></div><p class="muted" style="font-size:13px">교재 1.1 표를 한국어로 옮김 <span class="chip-src">원문</span></p>''',
    explain=explain('풀이', ['대부분의 AI 제품은 토큰당 과금 API로 시작해요. 제품-시장 적합성을 찾는 동안은 그게 맞는 거래예요.', '전용 배포로 옮길 세 가지 이유: <b>규모</b>(GPU당 내는 게 더 싸질 만큼 트래픽이 많음), <b>특화</b>(맞춤 모델, 지연시간·가동률 요구), <b>오케스트레이션</b>(여러 모델·여러 단계 파이프라인).', '전용으로 가면 유연성과 통제력을 얻지만, 엔지니어링 부담이 늘고 월 지출의 바닥이 올라가요. 분명하고 당장의 사업상 필요가 있을 때만 옮기라고 교재는 말합니다.'],
                    limit='계산기는 GPU를 늘 꽉 채워 쓴다고 가정했어요. 실제로는 트래픽이 들쭉날쭉해 GPU가 노는 시간이 생기고(7장 자동 확장), 엔지니어 인건비도 빠져 있어요.'),
    bridge=bridge(gen=('사내 문서 요약 봇이 하루 수천 건이면 API, 수백만 건이면 전용 배포를 검토하는 식이에요.', '어느 쪽이 싼지는 단가와 처리량 가정에 크게 달려요.'),
                  field=('전력 요금의 기본요금(전용)과 사용량 요금(공유)을 비교하는 것과 비슷해요.', '전기와 달리 GPU 처리량은 모델·최적화에 따라 몇 배씩 달라져요.')),
    talk=say('asst', 'report', '처리량 슬라이더를 올리면 교차점이 왼쪽으로 가요. 같은 GPU에서 토큰을 더 뽑을수록 전용이 빨리 이득이 돼요 — 이게 2장부터의 최적화가 돈이 되는 이유예요.'))

APPS = [('에이전트', '영업팀용 잠재 고객 탐색 에이전트', '사용자 행동 하나가 추론 호출 여러 번을 부른다'), ('채팅', 'RAG를 쓰는 고객 지원 채팅', '첫 토큰까지 시간이 채팅을 빠르게 느끼게 한다'),
        ('음성', '언어 간 실시간 통역', '자연스러운 대화를 위한 처음부터 끝까지 지연시간'), ('미디어', '옷·신발·장신구 가상 착용', '결과 품질과 속도의 균형'),
        ('검색', '법률 문서 탐색', '오프라인 말뭉치 채우기 vs 온라인 사용자 요청'), ('추천', '전자상거래 상품 추천', '많은 요청량에서도 일정한 지연시간'),
        ('완성', 'IDE 코딩 탭 완성', '사용자 타자 속도에 맞춰 완성 덩어리 전체'), ('검수', '사용자 생성 콘텐츠 안전 점검', '비용 효율을 위한 높은 처리량')]
lv3 = level(3, 'lv3', '1.2 우리 앱은 어떤 앱인가', [('g', '모델: 사용 사례가 정하는 설계'), ('p', '교재: 1.2.1~1.2.3, 표')],
    pair=('연구실에서는', '농구 코치는 반에서 키 큰 학생을, 체조 코치는 작은 학생을 뽑아요. 같은 교실이라도 종목이 고르는 기준을 정합니다.', '모델에서는', '모든 추론 결정은 사용 사례에서 흘러나와요 <span class="chip-src">원문</span>. 범용 API나 추론 플랫폼을 만드는 게 아니라면, 사용 사례를 구체적으로 정해 <b>제약을 최대한 더하는</b> 편이 좋습니다.'),
    panel=panel('AI 네이티브 앱 여덟 가지 (교재 1.2.1 표)', None, '', ctrl='<div class="group" id="apps">' + ''.join('<button class="bt" data-a="%d" aria-pressed="%s">%s</button>' % (i, 'true' if i == 0 else 'false', a[0]) for i, a in enumerate(APPS)) + '</div>', ins_id='appI')
          + panel('온라인과 오프라인 — 배치 크기 손잡이', 'cBatch', '배치 크기를 키우면 요청 하나의 지연시간은 늘고, 시스템 전체 처리량은 커지는 모습. 상수는 설명용입니다.',
                  ctrl=slider('bB', '배치 크기', 1, 64, 1, 8, '') + btn_group('bMode', '용도', [('on', '온라인 (실시간)'), ('off', '오프라인 (일괄)')]), kp_id='bK', ins_id='bI'),
    explain=explain('풀이', ['추론 엔지니어링의 큰 거래 하나: <b>지연시간 vs 처리량</b>. 지연이 낮으면 앱이 빠르고, 처리량이 높으면 같은 사용자 수를 GPU 더 적게 감당해 싸져요.', '코드 완성·채팅·음성 에이전트는 사용자가 기다리는 <b>온라인</b> 앱 → 지연시간 우선. 팟캐스트 받아쓰기, 문서 정기 처리, 학습용 말뭉치 준비는 <b>오프라인</b> 일괄 작업 → 처리량 우선.', '같은 모델(예: 음성 인식 Whisper)도 실시간 받아쓰기와 일괄 받아쓰기에 쓰일 수 있고, 양이 충분하면 배포를 둘로 나눠 각각 맞추는 편이 싸요.', '소비자 앱은 비용에 민감하고 갑자기 몰리는 일이 잦아 <b>한계 비용·유연성</b>을, B2B는 마진이 좋고 사용이 안정적이지만 <b>가용성·일정한 저지연</b>을 우선합니다. 규제(데이터 주권, 개인정보, 법규 준수)는 둘 다 인프라 선택을 제한할 수 있어요.'],
                    limit='배치 곡선은 "배치를 키우면 각자는 기다리고 전체는 많이 한다"는 모양만 보여 줘요. 실제 모양은 GPU와 모델에 따라 다르며, 2장 2.4절(병목 계산)에서 원리를 봅니다.'),
    bridge=bridge(gen=('같은 LLM이라도 채팅창(첫 토큰 빠르게)과 야간 문서 요약(처리량 최대)은 서로 다른 설정의 배포 두 개로 돌리는 게 보통이에요.', '규모가 작으면 둘로 나누는 운영 부담이 더 클 수 있어요.'),
                  field=('식당의 단품 주문(온라인)과 단체 도시락(오프라인)은 주방 동선을 다르게 짭니다.', '주방과 달리 GPU는 한 번에 처리하는 묶음이 커질수록 거의 공짜로 더 처리하는 구간이 있어요.')),
    talk=say('fly', 'clip', '음성 통역에 처리량 최대 설정을 쓰면 말이 끊기겠네. 용도부터 정하라는 게 이 뜻이구나.'))

lv4 = level(4, 'lv4', '1.3 모델 고르기 — 평가, 미세조정, 증류', [('g', '모델: 모델 선택'), ('p', '교재: 1.3, 그림 1.2·1.3')],
    pair=('연구실에서는', '현미경 배율을 올릴수록 보이는 건 많지만 느리고 비싸요. "이 실험에 필요한 만큼"의 배율을 고르는 게 실력이에요.', '모델에서는', '다른 조건이 같다면, 파라미터가 적은 작은 모델의 추론이 더 빠르고 쌉니다. 그래서 모델 성능 최적화에서 가장 중요한 결정은 엔진도 추측 알고리즘도 아닌 <b>어떤 모델을 고르느냐</b>예요 <span class="chip-src">원문</span>.'),
    panel=panel('증류 — 선생 모델의 "확률 분포"를 보여 주면', 'cDist', '선생 모델의 다음 토큰 확률 분포와, 정답 하나만 보여 줄 때(미세조정 방식)의 차이를 막대로 비교한 설명용 도식.',
                ctrl=btn_group('dMode', '학생에게 보여 줄 것', [('soft', '선생의 확률 분포 (증류)'), ('hard', '정답 하나만')]) + slider('dT', '분포 퍼짐', 0.3, 3, 0.1, 1, ''), kp_id='dK', ins_id='dI'),
    explain=explain('풀이', ['초기 제품은 프런티어 모델의 토큰당 API를 쓰고, 규모를 키울 때는 반대로 — 일을 해낼 만큼 똑똑한 <b>가장 작고 돌리기 쉬운 모델</b>을 찾거나 만들라고 교재는 말해요. 인기 있는 모델 구조를 고르면 최적화 도구 지원도 넓어요.', '<b>평가(evals)</b>: 모델 지능을 체계적으로 재는 일. 빠르게 만들기 전에 쓸모를 확인하고, 품질을 떨어뜨릴 수 있는 최적화의 <b>기준선</b>이 됩니다. 공통 벤치마크는 후보를 추리는 데 쓰되 포화·조작될 수 있어요(굿하트의 법칙: 측정이 목표가 되면 좋은 측정이 아니게 된다).', '<b>미세조정</b>: 사전학습 모델을 새 데이터로 특정 용도에 맞추기. 예: 자연어 → SQL은 범위가 좁아서 수십억 파라미터 정도의 작은 미세조정 모델이 같은 일에서 비슷한 성능을 낼 수 있어요.', '<b>증류</b>: 큰 선생 모델로 작은 학생 모델을 학습시켜 행동을 흉내 내게 하기. 정답만이 아니라 선생의 <b>확률 분포</b>를 보여 줘요. 딥시크-R1(671B)의 라마·큐웬 기반 증류판이 대표 예예요.'],
                    limit='증류는 미세조정보다 실제로 덜 쓰인다고 교재는 말합니다. 그리고 선생의 좋은 점뿐 아니라 나쁜 버릇도 따라 배워요.'),
    bridge=bridge(gen=('회사 SQL 도우미를 만든다면, 거대 범용 모델 대신 SQL만 잘하는 작은 미세조정 모델이 더 빠르고 쌀 수 있어요.', '모든 분야가 이만큼 작게 줄지는 않아요 — 교재도 "극단적인 예"라고 해요.'),
                  field=('신입에게 정답지만 주는 것(미세조정)과 선배의 판단 과정을 함께 보여 주는 것(증류)의 차이와 비슷해요.', '사람과 달리 모델은 선배의 실수도 그대로 흉내 냅니다.')),
    talk=say('robo', 'blush', '…큰 모델이 늘 정답은 아니라고? 작은 모델이 같은 점수면 GPU 값이 확 줄긴 하네.'))

lv5 = level(5, 'lv5', '1.4 지연시간과 처리량 재기', [('g', '모델: 지표'), ('p', '교재: 1.4, 그림 1.4·1.5, 표')],
    pair=('연구실에서는', '실험 결과를 평균 하나로만 보고하면, 가끔 크게 튀는 값을 놓쳐요. 그래서 분포와 꼬리를 함께 봅니다.', '모델에서는', 'LLM의 대표 지표는 <b>TTFT</b>(첫 토큰까지 시간)와 <b>TPS</b>(초당 토큰). 지연시간은 오른쪽으로 꼬리가 긴 분포라서 평균 대신 <b>백분위</b>(P50·P90·P95·P99)로 봅니다 <span class="chip-src">원문</span>.'),
    panel=panel('스트리밍 한 번 — TTFT · ITL · TPS', 'cStream', '요청부터 첫 토큰까지(TTFT), 그 뒤 토큰 사이 간격(ITL)을 시간 축에 그린 도식.',
                ctrl=slider('sT', 'TTFT', 50, 2000, 50, 400, 'ms') + slider('sI', 'ITL', 5, 100, 1, 10, 'ms') + slider('sN', '출력 토큰', 10, 400, 10, 100, '개'), kp_id='sK',
                eq='체감 TPS = 1000 ÷ ITL(ms) &nbsp;·&nbsp; ITL 10ms → <b>100 TPS</b> <span class="chip-src">원문</span> &nbsp;·&nbsp; 전체 응답 시간 = TTFT + (토큰 수 − 1) × ITL')
          + panel('오른쪽 꼬리 분포와 백분위', 'cPct', '요청 1,000개의 응답 시간 히스토그램(시드 고정 로그정규 표본)과 평균·P50·P90·P99 선.',
                  ctrl=slider('pT', '꼬리 길이', 0.2, 1.0, 0.05, 0.5, '') + btn_group('pE', '재는 범위', [('inf', '추론 시간만'), ('e2e', '처음부터 끝까지')]), kp_id='pK', ins_id='pI', wide=True),
    explain=explain('풀이', ['TTFT는 계산이 몰리는 프리필에, TPS는 대역폭이 몰리는 디코드에 달려 있어요(2장에서 자세히). TTFT는 낮을수록, TPS는 높을수록 좋아요.', 'TPS는 헷갈리는 말이에요: <b>체감 TPS</b>(사용자 한 명이 받는 속도, 지연 지표)와 <b>전체 TPS</b>(서비스 전체가 내는 양, 처리량 지표). 토큰 사이 간격 <b>ITL</b> 10ms는 사용자당 100 TPS예요.', '에이전트의 도구 호출처럼 토큰 하나하나가 쓸모없는 요청은 TTFT·TPS 대신 <b>전체 응답 시간</b>을 재요.', '평균은 꼬리 때문에 P50보다 커지는 경우가 많아요(그림 1.5). P50은 둘에 하나, P90은 열에 하나, P95는 스물에 하나, P99는 백에 하나가 그보다 느리다는 뜻이에요.', '<b>추론 시간</b>(GPU에서 토큰 만드는 시간)과 <b>처음부터 끝까지</b>(네트워크·대기열 포함)를 둘 다 보세요. 추론은 빠른데 전체가 느리면, 모델 최적화보다 인프라를 볼 때예요.'],
                    limit='표본은 설명용 로그정규 분포예요. 실제 서비스의 분포 모양은 부하·배치·요청 길이에 따라 달라요.'),
    bridge=bridge(gen=('채팅 앱은 TTFT를, 긴 보고서 생성은 체감 TPS를, 에이전트는 전체 응답 시간을 먼저 봐요.', '사용자가 느끼는 속도에는 화면 그리기 같은 앱 쪽 시간도 섞여요.'),
                  field=('택배 평균 배송일이 이틀이어도, 열 번에 한 번 일주일 걸리면 고객은 그 한 번을 기억해요. P90·P99가 신뢰를 정합니다.', '택배와 달리 서버 꼬리는 몇 초 단위라 사용자가 금방 다시 누르고, 그게 또 부하가 돼요.')),
    talk=say('fly', 'magnify', '평균만 보면 열에 하나 몇 초씩 기다리는 사람을 못 봐. 그 사람이 다음 달에 떠나는 거야.'))

duel_sec = section('duel', 'VS', '대결 — 평균이 낮은 쪽 vs P99가 낮은 쪽', say('doc', 'think', '두 배포가 있어요. A는 평균이 더 낮고, B는 평균은 조금 높지만 꼬리가 짧아요. 1장이 권하는 대로 P99로 판정합니다.') + duel(
    '사용자 백 명 중 가장 느린 한 명의 경험(P99)이 더 나은 쪽은?', '배포 B (평균 약간 높음, 꼬리 짧음)', '평균에 속지 마. 꼬리를 봐.', '배포 A (평균이 가장 낮음)', '평균이 제일 낮잖아! 숫자 하나면 충분하지.'), small='판', tags=[('g', '판정 기준: P99 응답 시간 (시드 고정 표본 각 1,000개)')])

summary = section('sum', '정리', '정리 — 시작 전 체크리스트', '''
<div class="tw"><table class="tb"><tr><th>칸</th><th>정할 것</th><th>판단 기준</th><th>한계</th></tr>
<tr><td>① 균형</td><td>모델·인터페이스·지연 예산·단위 경제학·사용 패턴</td><td>제약을 많이 알수록 좋은 결과</td><td>초기에는 흐릿함 → 기성 API</td></tr>
<tr><td>② 1.1</td><td>공유 추론 vs 전용 배포</td><td>규모·특화·오케스트레이션</td><td>전용은 지출 바닥과 엔지니어링 부담 ↑</td></tr>
<tr><td>③ 1.2</td><td>앱 종류, 온라인/오프라인, 소비자/B2B, 규제</td><td>지연시간 vs 처리량</td><td>같은 모델도 배포를 나눌 수 있음</td></tr>
<tr><td>④ 1.3</td><td>모델 크기, 평가, 미세조정, 증류</td><td>일을 해낼 만큼 똑똑한 가장 작은 모델</td><td>벤치마크 포화·조작(굿하트)</td></tr>
<tr><td>⑤ 1.4</td><td>TTFT·TPS·ITL, 백분위, 처음부터 끝까지</td><td>P90·P99까지 줄이기</td><td>추론 시간만 보면 인프라 문제를 놓침</td></tr></table></div>
<div class="notebook"><h4>모아의 기록장</h4><ul><li>ITL 10ms = 사용자당 100 TPS</li><li>P50 = 둘에 하나, P90 = 열에 하나, P95 = 스물에 하나, P99 = 백에 하나가 더 느림</li><li>딥시크-R1 671B → 라마 3·큐웬 2.5 기반 증류판 (2025년 1월)</li><li>평가 요령: 데이터를 직접 보라, 정확하게(가장 어려운 문제에 집중), 도구를 써라</li></ul></div>
''' + say('moa', 'ok', '1주차 교재 끝! 같은 주의 논문 라이브벤치는 ④ 칸의 "벤치마크가 오염·포화되는 문제"를 정면으로 다뤄요.'), small='끝', tags=[('g', '다섯 칸 비교')])

outro = section('outro', '끝', '아웃트로', '<div class="outro"><div class="scene" data-img="sc_01_outro" role="img" aria-label="연구실 식구 여섯이 응답 시간 히스토그램 앞에 모인 장면"><img data-who="fly" data-mood="arms" alt=""><img data-who="doc" data-mood="magic" alt=""><img data-who="asst" data-mood="spark" alt=""><img data-who="sia" data-mood="proud" alt=""><img data-who="moa" data-mood="plant" alt=""><img data-who="robo" data-mood="sigh" alt=""></div></div>'
    + say('doc', 'magic', '1장의 한 줄: 최적화하기 전에 <b>무엇이 최선인지</b>를 정하라 — 사용 사례, 모델, 그리고 백분위로 잰 지연시간.')
    + say('fly', 'arms', '봐, 평균이 꼬리를 숨기고 있었잖아.')
    + say('robo', 'sigh', '평균만 보고 베팅한 건 손절. 다음엔 분포까지 보고 들어간다.')
    + say('asst', 'spark', '2주차는 2장 "모델"이에요. 프리필과 디코드가 왜 TTFT와 TPS를 정하는지 안으로 들어가 봐요.'), small='', tags=())

GL = {'최적화': ['최적화 (optimization)', '개념', '여러 선택지 중 최선을 고르는 일. 무엇이 최선인지 먼저 정해야 한다.'], '지연시간': ['지연시간 (latency)', '지표', '요청 하나가 답을 받기까지 걸리는 시간.'],
      '처리량': ['처리량 (throughput)', '지표', '시스템 전체가 정해진 시간에 처리하는 양.'], '공유 추론': ['공유 추론 (shared inference)', '방식', '공개 API에 보내고 백만 토큰당 등 사용량으로 내는 방식.'],
      '전용 배포': ['전용 배포 (dedicated deployment)', '방식', 'GPU를 빌려 우리만의 추론 서비스를 두고 GPU 시간으로 내는 방식.'], '단위 경제학': ['단위 경제학 (unit economics)', '용어', '요청당·사용자당·월마다 쓸 수 있는 비용.'],
      '콜드 스타트': ['콜드 스타트 (cold start)', '용어', '꺼져 있던 서버가 모델을 올리고 첫 요청에 답하기까지 걸리는 시간. 7장.'], '오프라인': ['오프라인 (offline batch)', '용어', '사용자가 기다리지 않는 일괄 작업. 처리량 우선.'],
      '온라인': ['온라인 (online)', '용어', '사용자가 실시간으로 기다리는 앱. 지연시간 우선.'], '평가': ['평가 (evals)', '방법', '모델 지능을 제품·분야·과제에 맞춰 체계적으로 재는 일.'],
      '벤치마크': ['벤치마크 (benchmark)', '평가', 'MMLU·SWE-bench처럼 공통 과제로 모델을 재는 시험.'], '굿하트의 법칙': ['굿하트의 법칙', '원리', '측정이 목표가 되면 더 이상 좋은 측정이 아니게 된다.'],
      '미세조정': ['미세조정 (fine-tuning)', '기법', '사전학습 모델에 새 데이터를 넣어 특정 용도에 맞추기. 구조는 그대로, 가중치 값이 바뀐다(그림 1.2).'],
      '증류': ['증류 (distillation)', '기법', '큰 선생 모델의 확률 분포를 보여 주며 작은 학생 모델을 학습시키기(그림 1.3).'], 'TTFT': ['TTFT (time to first token)', '지표', '첫 출력 토큰이 보이기까지 시간. 계산이 몰리는 프리필에 달림.'],
      'TPS': ['TPS (tokens per second)', '지표', '초당 토큰. 체감 TPS(사용자당, 지연 지표)와 전체 TPS(서비스 전체, 처리량 지표)를 구분한다.'], 'ITL': ['ITL (inter-token latency)', '지표', '이어지는 토큰 사이 간격. 10ms면 사용자당 100 TPS.'],
      '백분위': ['백분위 (percentile)', '통계', 'P90 = 요청 열 개 중 하나가 이보다 느린 값.'], 'P99': ['P99', '지표', '요청 백 개 중 하나가 이보다 느린 응답 시간.'], 'P50': ['P50 (중앙값)', '지표', '요청 둘 중 하나가 이보다 느린 응답 시간.'],
      '프리필': ['프리필 (prefill)', '단계', '입력 토큰 전체를 한꺼번에 처리하는 단계. 계산 바운드.'], '디코드': ['디코드 (decode)', '단계', '출력 토큰을 하나씩 만드는 단계. 대역폭 바운드.'],
      '파라미터': ['파라미터 (parameter)', '용어', '모델 속 학습된 숫자의 개수. 클수록 대체로 느리고 비싸다.']}
CORE = ['최적화', '공유 추론', '전용 배포', '단위 경제학', '평가', '굿하트의 법칙', '미세조정', '증류', 'TTFT', 'TPS', 'ITL', '백분위']
QUIZ = {'lv1': [{'q': '교재가 말하는 "알아 둘 것" 다섯 가지에 들지 않는 것은?', 'o': ['지연시간 예산', '사용 패턴', 'GPU 제조사'], 'a': 2, 'why': '맞아요. 모델 요구사항·인터페이스·지연 예산·단위 경제학·사용 패턴이에요.', 'hint': '체크 버튼 다섯 개를 다시 보세요.'},
                {'q': '제품 초기에 요구사항이 흐릿할 때 교재의 권고는?', 'o': ['처음부터 전용 GPU 클러스터', '기성 API 활용', '자체 모델 학습'], 'a': 1, 'why': '맞아요. 요구사항이 또렷해지면 그때 추론 엔지니어링이 할 만해요.', 'hint': '① 칸 풀이 2번.'}],
        'lv2': [{'q': '전용 배포로 옮길 이유로 교재가 든 세 가지가 아닌 것은?', 'o': ['규모', '특화', '무료'], 'a': 2, 'why': '맞아요. 규모·특화·오케스트레이션이에요. 전용은 월 지출의 바닥을 올려요.', 'hint': '② 칸 풀이 2번.'},
                {'q': '[계산] 월 300백만 토큰, 백만 토큰당 3이면 공유 API 월 비용은? (같은 화폐 단위)', 'o': ['100', '900', '3,000'], 'a': 1, 'why': '맞아요. 300 × 3 = 900.', 'hint': '월 토큰(백만) × 단가.'}],
        'lv3': [{'q': '오프라인 일괄 작업에 맞는 우선순위는?', 'o': ['지연시간 최소', '처리량 최대', 'TTFT 최소'], 'a': 1, 'why': '맞아요. 기다리는 사용자가 없으니 전체를 많이 처리하는 쪽이 싸요.', 'hint': '배치 손잡이의 "오프라인"을 눌러 보세요.'},
                {'q': 'B2B 제품의 추론에서 교재가 먼저 챙기라고 한 것은?', 'o': ['한계 비용', '가용성과 일정한 저지연', '바이럴 대비'], 'a': 1, 'why': '맞아요. 소비자 앱은 한계 비용·유연성, B2B는 지연시간·가동률이 먼저예요.', 'hint': '③ 칸 풀이 4번.'}],
        'lv4': [{'q': '증류가 미세조정과 다른 점은?', 'o': ['학생에게 선생의 확률 분포를 보여 준다', '모델 구조를 바꾼다', '데이터가 필요 없다'], 'a': 0, 'why': '맞아요. 정답만이 아니라 분포를 보여 줘서 행동을 흉내 내게 해요.', 'hint': '증류 도식에서 두 버튼을 번갈아 눌러 보세요.'},
                {'q': '굿하트의 법칙이 벤치마크에 주는 경고는?', 'o': ['측정이 목표가 되면 좋은 측정이 아니게 된다', '벤치마크는 늘 정확하다', '큰 모델이 항상 이긴다'], 'a': 0, 'why': '맞아요. 그래서 우리 제품에 맞춘 평가가 필요해요.', 'hint': '④ 칸 풀이 2번.'}],
        'lv5': [{'q': '[계산] ITL이 20ms면 체감 TPS는?', 'o': ['20', '50', '200'], 'a': 1, 'why': '맞아요. 1000 ÷ 20 = 50 토큰/초.', 'hint': '1000을 ITL로 나눠요.'},
                {'q': 'P95의 뜻은?', 'o': ['요청 스물 개 중 하나가 이보다 느리다', '평균의 95%', '요청의 95%가 실패'], 'a': 0, 'why': '맞아요. 교재 표: P95 = 스물에 하나.', 'hint': '모아의 기록장을 보세요.'},
                {'q': '추론 시간은 빠른데 처음부터 끝까지 시간이 느리다면 먼저 볼 곳은?', 'o': ['모델 양자화', '인프라(네트워크·대기열)', '모델 크기'], 'a': 1, 'why': '맞아요. 교재 1.4.2절의 권고예요.', 'hint': '"재는 범위" 버튼을 바꿔 보세요.'}]}

KG = {'version': '1.0', 'page': P, 'nodes': [
    node('lab:concept/optimization-balance', 'Concept', '최적화는 균형', 'optimization as balance', '#lv1', P, '지연시간·처리량·품질 사이의 알맞은 균형.', ('kiely2026inference', '1장 도입'), 1),
    node('lab:concept/constraints', 'Concept', '다섯 가지 알아 둘 것', 'five things to know', '#lv1', P, '모델 요구사항, 인터페이스, 지연 예산, 단위 경제학, 사용 패턴.', ('kiely2026inference', '1장 도입'), 1),
    node('lab:method/shared-inference', 'Method', '공유 추론', 'shared inference', '#lv2', P, '공개 API, 사용량 과금.', ('kiely2026inference', '1.1'), 1),
    node('lab:method/dedicated-deployment', 'Method', '전용 배포', 'dedicated deployment', '#lv2', P, 'GPU 시간 과금, 우리만의 서비스.', ('kiely2026inference', '1.1'), 2),
    node('lab:concept/online-offline', 'Concept', '온라인 vs 오프라인', 'online versus offline', '#lv3', P, '실시간 앱은 지연시간, 일괄 작업은 처리량.', ('kiely2026inference', '1.2.2'), 2),
    node('lab:concept/consumer-b2b', 'Concept', '소비자 vs B2B', 'consumer versus B2B', '#lv3', P, '한계 비용·유연성 vs 가용성·일정한 저지연.', ('kiely2026inference', '1.2.3'), 2),
    node('lab:concept/compliance', 'Concept', '규제 준수', 'compliance', '#lv3', P, '데이터 주권, 개인정보, 법규.', ('kiely2026inference', '1.2.3'), 2),
    node('lab:method/model-selection', 'Method', '모델 고르기', 'model selection', '#lv4', P, '일을 해낼 만큼 똑똑한 가장 작은 모델.', ('kiely2026inference', '1.3'), 2),
    node('lab:method/evals', 'Method', '평가 (evals)', 'model evaluation', '#lv4', P, '제품 맞춤으로 모델 지능을 재는 일.', ('kiely2026inference', '1.3.1'), 2, 'evaluation'),
    node('lab:method/fine-tuning', 'Method', '미세조정', 'fine-tuning', '#lv4', P, '새 데이터로 특정 용도에 맞추기.', ('kiely2026inference', '1.3.2, 그림 1.2'), 2, 'training'),
    node('lab:method/distillation', 'Method', '증류', 'distillation', '#lv4', P, '선생 모델의 확률 분포로 학생 모델 학습.', ('kiely2026inference', '1.3.3, 그림 1.3'), 3, 'training'),
    node('lab:metric/ttft', 'Metric', 'TTFT', 'time to first token', '#lv5', P, '첫 토큰까지 시간.', ('kiely2026inference', '1.4'), 1, 'evaluation'),
    node('lab:metric/tps', 'Metric', 'TPS (체감·전체)', 'tokens per second', '#lv5', P, '초당 토큰.', ('kiely2026inference', '1.4'), 1, 'evaluation'),
    node('lab:metric/itl', 'Metric', 'ITL', 'inter-token latency', '#lv5', P, '토큰 사이 간격.', ('kiely2026inference', '1.4'), 2, 'evaluation'),
    node('lab:metric/percentiles', 'Metric', '지연시간 백분위', 'latency percentiles', '#lv5', P, 'P50·P90·P95·P99.', ('kiely2026inference', '1.4.1'), 2, 'evaluation'),
    node('lab:metric/end-to-end', 'Metric', '처음부터 끝까지 지연', 'end-to-end latency', '#lv5', P, '네트워크·대기열 포함.', ('kiely2026inference', '1.4.2'), 2, 'evaluation'),
    node('lab:limitation/unclear-early', 'Limitation', '초기에는 요구사항이 흐릿함', 'requirements unclear early', '#lv1', P),
    node('lab:limitation/linear-cost', 'Limitation', '공유 API 비용은 사용량에 비례', 'cost scales linearly', '#lv2', P),
    node('lab:limitation/spend-floor', 'Limitation', '전용 배포는 지출 바닥 ↑', 'higher spend floor', '#lv2', P),
    node('lab:limitation/benchmark-gamed', 'Limitation', '벤치마크 포화·조작', 'saturated or gamed benchmarks', '#lv4', P, '굿하트의 법칙.'),
    node('lab:limitation/mean-hides-tail', 'Limitation', '평균은 꼬리를 숨긴다', 'mean hides the tail', '#lv5', P),
    node('lab:claim/itl-100', 'Claim', 'ITL 10ms = 사용자당 100 TPS', 'ITL 10 ms equals 100 TPS per user', '#lv5', P, None, ('kiely2026inference', '1.4')),
    node('lab:claim/r1-distill', 'Claim', '딥시크-R1 671B의 라마·큐웬 증류판', 'DeepSeek-R1 distills', '#lv4', P, None, ('kiely2026inference', '1.3.3')),
    node('lab:claim/text-to-sql', 'Claim', 'SQL은 작은 미세조정 모델로도 비슷한 성능 가능', 'small fine-tuned text-to-SQL', '#lv4', P, None, ('kiely2026inference', '1.3.2')),
    node('lab:claim/smaller-faster', 'Claim', '같은 조건이면 작은 모델이 더 빠르고 싸다', 'smaller models are faster and cheaper', '#lv4', P, None, ('kiely2026inference', '1.3')),
    node('lab:analogy/athletes', 'Analogy', '미식축구 선수 ↔ 특화된 추론 서비스', 'athletes specialized by position', '#top', P),
    node('lab:analogy/coach', 'Analogy', '종목별 코치 ↔ 사용 사례가 정하는 설계', 'coach recruiting by sport', '#lv3', P),
    node('lab:question/core', 'Question', '우리 제품에 가장 알맞은 모델을 고르려면?', 'What is best for our product?', '#top', P),
    node('lab:question/duel', 'Question', '대결: 평균 vs P99', 'Duel: mean vs P99', '#duel', P),
    node('lab:question/next', 'Question', 'TTFT와 TPS는 모델 안에서 무엇이 정하나? (2장)', 'What determines TTFT and TPS?', '#sum', P),
    node('lab:sim/crossover', 'Simulation', '공유·전용 교차점 계산기', 'cost crossover', '#lv2', P), node('lab:sim/batch', 'Simulation', '배치 크기 손잡이', 'batch size dial', '#lv3', P),
    node('lab:sim/distill', 'Simulation', '증류 분포', 'distillation bars', '#lv4', P), node('lab:sim/percentile', 'Simulation', '백분위 히스토그램', 'percentile histogram', '#lv5', P),
    node('lab:work/kiely2026inference', 'Work', 'Kiely (2026) Inference Engineering', 'Kiely 2026', '#top', P)],
 'edges': [edge('lab:concept/constraints', 'prerequisiteOf', 'lab:concept/optimization-balance', '#lv1'), edge('lab:concept/optimization-balance', 'hasLimitation', 'lab:limitation/unclear-early', '#lv1'),
           edge('lab:limitation/unclear-early', 'addressedBy', 'lab:method/shared-inference', '#lv2'), edge('lab:method/shared-inference', 'hasLimitation', 'lab:limitation/linear-cost', '#lv2'),
           edge('lab:limitation/linear-cost', 'addressedBy', 'lab:method/dedicated-deployment', '#lv2'), edge('lab:method/dedicated-deployment', 'hasLimitation', 'lab:limitation/spend-floor', '#lv2'),
           edge('lab:limitation/spend-floor', 'addressedBy', 'lab:method/model-selection', '#lv4'), edge('lab:method/model-selection', 'hasLimitation', 'lab:limitation/benchmark-gamed', '#lv4'),
           edge('lab:limitation/benchmark-gamed', 'addressedBy', 'lab:method/evals', '#lv4'), edge('lab:method/evals', 'prerequisiteOf', 'lab:method/fine-tuning', '#lv4'),
           edge('lab:method/fine-tuning', 'relatedTo', 'lab:method/distillation', '#lv4'), edge('lab:metric/percentiles', 'hasLimitation', 'lab:limitation/mean-hides-tail', '#lv5'),
           edge('lab:metric/itl', 'relatedTo', 'lab:metric/tps', '#lv5'), edge('lab:metric/ttft', 'relatedTo', 'lab:metric/end-to-end', '#lv5'), edge('lab:concept/online-offline', 'relatedTo', 'lab:concept/optimization-balance', '#lv3'),
           edge('lab:concept/consumer-b2b', 'relatedTo', 'lab:concept/online-offline', '#lv3'), edge('lab:concept/compliance', 'relatedTo', 'lab:method/dedicated-deployment', '#lv3')]
           + [edge(c, 'assertedIn', 'lab:work/kiely2026inference', '#lv4') for c in ['lab:claim/itl-100', 'lab:claim/r1-distill', 'lab:claim/text-to-sql', 'lab:claim/smaller-faster']]
           + [edge('lab:sim/crossover', 'relatedTo', 'lab:method/dedicated-deployment', '#lv2'), edge('lab:sim/percentile', 'relatedTo', 'lab:metric/percentiles', '#lv5'), edge('lab:sim/distill', 'relatedTo', 'lab:method/distillation', '#lv4'),
              edge('lab:analogy/athletes', 'relatedTo', 'lab:concept/optimization-balance', '#top'), edge('lab:analogy/coach', 'relatedTo', 'lab:concept/online-offline', '#lv3')]}

JS = r'''
var C=L.C,F=L.FONT,fit=L.fit,grid=L.grid,stamp=L.stamp,KN=%s,APPS=%s;
L.kpis('#heroK',[[5,'알아 둘 것','g'],[8,'AI 네이티브 앱 종류','m'],['TTFT·TPS','LLM 대표 지표','i'],['P99','백에 하나','a']]);
/* ① */
var cK=$('#cKnow'),known={},kt=0;
function drawK(dt){kt+=dt;var W=fit(cK,200),x=cK.getContext('2d');x.clearRect(0,0,W,200);grid(x,W,200);var n=Object.keys(known).filter(function(k){return known[k]}).length,cx=W/2,cy=100;
  for(var r=5;r>=1;r--){x.strokeStyle=r<=5-n?'rgba(157,155,184,.25)':C.gfp;x.beginPath();x.arc(cx,cy,r*17,0,7);x.stroke();}
  var rr=L.rng(5),spread=(5-n)*17+6;for(var i=0;i<26;i++){var a=rr()*7,d=rr()*spread,wob=Math.sin(kt*2+i)*1.5;x.fillStyle='rgba(241,182,70,.8)';x.beginPath();x.arc(cx+Math.cos(a)*d+wob,cy+Math.sin(a)*d,3,0,7);x.fill();}
  x.fillStyle=C.muted;x.font='12px '+F;x.textAlign='left';x.fillText('점 = 시도해 볼 만한 설정',12,190);stamp(x,W,'설명용 도식');}
function updK(){var n=Object.keys(known).filter(function(k){return known[k]}).length;L.ins('#kI',[[n>=4?'g':n>=2?'a':'r','알고 있는 제약 '+n+'/5. '+(n>=4?'방향이 좁혀졌어요 — 추론 엔지니어링을 시작할 만해요.':n>=2?'아직 흐릿한 게 있어요.':'초기 단계예요 — 교재는 기성 API를 권해요.')]].concat(KN.filter(function(k){return !known[k[0]]}).slice(0,2).map(function(k){return ['m','아직 모름: '+k[1]+' — '+k[2]]})));drawK(0);}
$$('#kn [data-k]').forEach(function(b){b.addEventListener('click',function(){known[b.dataset.k]=!known[b.dataset.k];b.setAttribute('aria-pressed',known[b.dataset.k]?'true':'false');updK();});});L.addMod(cK,drawK);updK();
/* ② 비용 */
var cC=$('#cCost'),cv=300,cp=3,cg=4,ct=1500;
function gpus(v){return Math.max(1,Math.ceil(v*1e6/(ct*3600*730)));}
function drawC(){var W=fit(cC,240),x=cC.getContext('2d');x.clearRect(0,0,W,240);grid(x,W,240);var L0=56,R=W-16,T=16,B=206,mxV=2000,mxC=Math.max(2000*cp,gpus(2000)*730*cg)*1.05;
  function px(v){return L0+(R-L0)*v/mxV}function py(c){return B-(B-T)*c/mxC}
  x.strokeStyle=C.rule;x.beginPath();x.moveTo(L0,T);x.lineTo(L0,B);x.lineTo(R,B);x.stroke();
  x.strokeStyle=C.robo;x.lineWidth=2;x.beginPath();x.moveTo(px(0),py(0));x.lineTo(px(mxV),py(mxV*cp));x.stroke();
  x.strokeStyle=C.fly;x.beginPath();for(var v=1;v<=mxV;v+=4){var y=py(gpus(v)*730*cg);v===1?x.moveTo(px(v),y):x.lineTo(px(v),y);}x.stroke();x.lineWidth=1;
  x.strokeStyle=C.text;x.setLineDash([4,3]);x.beginPath();x.moveTo(px(cv),T);x.lineTo(px(cv),B);x.stroke();x.setLineDash([]);
  x.fillStyle=C.robo;x.font='12px '+F;x.textAlign='left';x.fillText('공유 API',L0+6,T+12);x.fillStyle=C.fly;x.fillText('전용 배포',L0+6,T+28);x.fillStyle=C.muted;x.textAlign='center';x.fillText('월 토큰 (백만) →',(L0+R)/2,B+22);stamp(x,W,'단가·처리량 모두 설명용');}
function updC(){L.setTxt('#cVV',cv+'백만');L.setTxt('#cPV',(+cp).toFixed(1));L.setTxt('#cGV',(+cg).toFixed(1));L.setTxt('#cTV',ct+'토큰/초');var sh=cv*cp,g=gpus(cv),de=g*730*cg,cross=null;
  for(var v=1;v<=5000;v++){if(v*cp>gpus(v)*730*cg){cross=v;break;}}
  L.kpis('#cK',[[Math.round(sh).toLocaleString(),'공유 월 비용','i'],[Math.round(de).toLocaleString(),'전용 월 비용 (GPU '+g+'장)','r'],[cross?cross+'백만':'없음','교차점 (월 토큰)','a'],[sh<de?'공유':'전용','지금 더 싼 쪽','g']]);
  L.ins('#cI',[[sh<de?'a':'g',sh<de?'지금은 공유 API가 싸요. 사용량이 '+(cross||'—')+'백만 토큰을 넘으면 전용이 싸지기 시작해요.':'규모가 커서 GPU당 내는 편이 싸요 — 교재가 말하는 "규모" 이유예요.'],['m','GPU를 늘 꽉 채운다는 가정이에요. 실제 사용률이 50%%면 전용 비용은 사실상 두 배.']]);drawC();}
[['cV',function(v){cv=v}],['cP',function(v){cp=v}],['cG',function(v){cg=v}],['cT',function(v){ct=v}]].forEach(function(p){$('#'+p[0]).addEventListener('input',function(){p[1](+this.value);updC();});});L.addMod(cC,function(dt){if(dt===0)drawC();});updC();
/* ③ 앱 */
function app(i){var a=APPS[i];L.ins('#appI',[['g','<b>'+a[0]+'</b> · 예: '+a[1]],['a','고려할 점: '+a[2]]]);}
$$('#apps [data-a]').forEach(function(b){b.addEventListener('click',function(){$$('#apps [data-a]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});app(+b.dataset.a);});});app(0);
var cB=$('#cBatch'),bb=8,bm='on';function blat(b){return 30+4*b;}function bthr(b){return b/blat(b)*1000;}
function drawB(){var W=fit(cB,220),x=cB.getContext('2d');x.clearRect(0,0,W,220);grid(x,W,220);var L0=50,R=W-50,T=16,B=186;function px(b){return L0+(R-L0)*(b-1)/63}
  function curve(f,mx,col){x.strokeStyle=col;x.lineWidth=2;x.beginPath();for(var b=1;b<=64;b++){var y=B-(B-T)*f(b)/mx;b===1?x.moveTo(px(b),y):x.lineTo(px(b),y);}x.stroke();x.lineWidth=1;}
  curve(blat,blat(64),C.eye);curve(bthr,bthr(64),C.gfp);x.strokeStyle=C.text;x.beginPath();x.moveTo(px(bb),T);x.lineTo(px(bb),B);x.stroke();
  x.fillStyle=C.eye;x.font='12px '+F;x.textAlign='left';x.fillText('요청 하나의 지연시간',L0+4,T+12);x.fillStyle=C.gfp;x.fillText('전체 처리량',L0+4,T+28);x.fillStyle=C.muted;x.textAlign='center';x.fillText('배치 크기 →',(L0+R)/2,B+24);stamp(x,W,'설명용 상수');}
function updB(){L.setTxt('#bBV',bb);L.kpis('#bK',[[blat(bb)+'ms','요청 하나 지연 (설명용)','r'],[Math.round(bthr(bb)),'초당 요청 (설명용)','g']]);
  var good=bm==='on'?bb<=8:bb>=32;L.ins('#bI',[[good?'g':'a',bm==='on'?(bb<=8?'온라인: 지연시간이 낮게 유지돼요.':'온라인인데 배치가 커서 사용자가 기다려요.'):(bb>=32?'오프라인: 처리량이 커서 같은 일을 GPU 적게 해요.':'오프라인인데 배치가 작아 GPU를 덜 쓰고 있어요.')]]);drawB();}
$('#bB').addEventListener('input',function(){bb=+this.value;updB();});L.bindSeg('#bMode',function(v){bm=v;bb=v==='on'?4:48;$('#bB').value=bb;updB();});L.addMod(cB,function(dt){if(dt===0)drawB();});updB();
/* ④ 증류 */
var cD=$('#cDist'),dm='soft',dt=1,LOG=[2.2,1.6,0.9,0.3,-0.4],TOK=['SELECT','WITH','select','FROM','--'];
function soft(t){var e=LOG.map(function(v){return Math.exp(v/t)}),s=e.reduce(function(a,b){return a+b},0);return e.map(function(v){return v/s});}
function drawD(){var W=fit(cD,210),x=cD.getContext('2d');x.clearRect(0,0,W,210);grid(x,W,210);var p=dm==='soft'?soft(dt):[1,0,0,0,0],bw=(W-80)/5;
  p.forEach(function(v,i){var h=v*150,cx=40+i*bw;x.fillStyle=dm==='soft'?'rgba(214,114,214,.7)':'rgba(130,184,255,.7)';x.fillRect(cx+8,180-h,bw-16,h);x.fillStyle=C.text;x.font='12px '+F;x.textAlign='center';x.fillText(TOK[i],cx+bw/2,198);x.fillStyle=C.muted;x.fillText((v*100).toFixed(0)+'%%',cx+bw/2,172-h);});
  stamp(x,W,'설명용 · 가상의 다음 토큰 확률');}
function updD(){L.setTxt('#dTV',(+dt).toFixed(1));var p=soft(dt),ent=-p.reduce(function(a,v){return a+(v>0?v*Math.log2(v):0)},0);
  L.kpis('#dK',[[dm==='soft'?ent.toFixed(2):'0.00','보여 주는 정보량 (비트, 엔트로피)','m'],[dm==='soft'?'5개 후보 전부':'정답 1개','학생이 보는 것','i']]);
  L.ins('#dI',[dm==='soft'?['m','증류: 학생은 "SELECT가 가장 그럴듯하지만 WITH도 꽤 그럴듯하다"는 선생의 판단까지 배워요.']:['i','정답만: 학생은 SELECT 하나만 봐요(미세조정의 입력-출력 쌍과 같은 모양).'],['a','선생의 나쁜 버릇(엉뚱한 후보에 준 확률)도 함께 배운다는 점을 잊지 마세요.']]);drawD();}
L.bindSeg('#dMode',function(v){dm=v;updD();});$('#dT').addEventListener('input',function(){dt=+this.value;updD();});L.addMod(cD,function(dt0){if(dt0===0)drawD();});updD();
/* ⑤ 스트리밍 */
var cS=$('#cStream'),st=400,si=10,sn=100,stt=0;
function drawS(d){stt+=d;var W=fit(cS,150),x=cS.getContext('2d');x.clearRect(0,0,W,150);grid(x,W,150);var tot=st+(sn-1)*si,L0=20,R=W-20;function px(t){return L0+(R-L0)*t/tot}
  x.fillStyle='rgba(240,96,77,.35)';x.fillRect(px(0),50,px(st)-px(0),30);x.fillStyle=C.eye;x.font='12px '+F;x.textAlign='left';x.fillText('TTFT '+st+'ms',px(0)+4,44);
  var play=L.reduce?tot:(stt*1000)%%(tot*1.3);for(var k=0;k<sn;k++){var t=st+k*si;if(t>play)break;x.fillStyle=C.gfp;x.fillRect(px(t),52,Math.max(1.5,(R-L0)*si/tot*0.6),26);}
  x.fillStyle=C.muted;x.textAlign='right';x.fillText('전체 '+(tot/1000).toFixed(2)+'초',R,44);x.textAlign='left';x.fillText('초록 막대 하나 = 토큰 하나 (간격 = ITL)',L0,110);stamp(x,W,'계산 도식');}
function updS(){L.setTxt('#sTV',st+'ms');L.setTxt('#sIV',si+'ms');L.setTxt('#sNV',sn+'개');L.kpis('#sK',[[st+'ms','TTFT','r'],[(1000/si).toFixed(0),'체감 TPS','g'],[si+'ms','ITL','m'],[((st+(sn-1)*si)/1000).toFixed(2)+'초','전체 응답 시간','i']]);}
['sT','sI','sN'].forEach(function(id){$('#'+id).addEventListener('input',function(){if(id==='sT')st=+this.value;if(id==='sI')si=+this.value;if(id==='sN')sn=+this.value;updS();});});L.addMod(cS,drawS);updS();
/* ⑤ 백분위 */
var cP=$('#cPct'),pt=0.5,pe='inf';
function sample(sig,mu,seed,extra){var r=L.rng(seed),a=[];for(var i=0;i<1000;i++){var u=0;while(!u)u=r();var z=Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*r());var v=Math.exp(mu+sig*z);if(extra){v+=40+r()*30+(r()<0.05?r()*600:0);}a.push(v);}return a.sort(function(p,q){return p-q});}
function pc(a,p){return a[Math.min(a.length-1,Math.floor(a.length*p))];}function mean(a){return a.reduce(function(s,v){return s+v},0)/a.length;}
function drawP(){var a=sample(pt,Math.log(600),42,pe==='e2e'),W=fit(cP,250),x=cP.getContext('2d');x.clearRect(0,0,W,250);grid(x,W,250);var mx=pc(a,0.995),L0=30,R=W-20,B=210,T=20,nb=60,h=[];for(var i=0;i<nb;i++)h.push(0);
  a.forEach(function(v){var b=Math.min(nb-1,Math.floor(v/mx*nb));h[b]++;});var hm=Math.max.apply(0,h),bw=(R-L0)/nb;h.forEach(function(c,i){x.fillStyle='rgba(130,184,255,.55)';x.fillRect(L0+i*bw,B-(B-T)*c/hm,bw-1,(B-T)*c/hm);});
  [['평균',mean(a),C.amber],['P50',pc(a,.5),C.gfp],['P90',pc(a,.9),C.stain],['P99',pc(a,.99),C.eye]].forEach(function(l,i){var px=L0+(R-L0)*Math.min(1,l[1]/mx);x.strokeStyle=l[2];x.lineWidth=2;x.beginPath();x.moveTo(px,T);x.lineTo(px,B);x.stroke();x.lineWidth=1;x.fillStyle=l[2];x.font='12px '+F;x.textAlign='left';x.fillText(l[0],px+3,T+12+i*14);});
  x.fillStyle=C.muted;x.textAlign='center';x.fillText('응답 시간 (ms) →',(L0+R)/2,B+24);stamp(x,W,'시드 고정 로그정규 표본 1,000개');return a;}
function updP(){L.setTxt('#pTV',(+pt).toFixed(2));var a=drawP();L.kpis('#pK',[[Math.round(mean(a))+'ms','평균','a'],[Math.round(pc(a,.5))+'ms','P50 (둘에 하나)','g'],[Math.round(pc(a,.9))+'ms','P90 (열에 하나)','m'],[Math.round(pc(a,.99))+'ms','P99 (백에 하나)','r']]);
  L.ins('#pI',[['a','평균('+Math.round(mean(a))+') > P50('+Math.round(pc(a,.5))+'): 꼬리가 평균을 끌어올렸어요(그림 1.5).'],pe==='e2e'?['r','처음부터 끝까지: 네트워크·대기열이 더해지고, 가끔 긴 대기가 꼬리를 늘렸어요.']:['g','추론 시간만: GPU에서 토큰을 만드는 시간이에요.']]);}
$('#pT').addEventListener('input',function(){pt=+this.value;updP();});L.bindSeg('#pE',function(v){pe=v;updP();});L.addMod(cP,function(dt0){if(dt0===0)updP();});updP();
/* 대결 */
L.Duel({fmt:function(v){return Math.round(v)+' ms'},run:function(){var A=sample(0.75,Math.log(430),11,false),Bs=sample(0.28,Math.log(600),12,false);var f=pc(Bs,.99),r=pc(A,.99);
  return {fly:f,robo:r,res:f<r?'F':'R',asst:'P99는 초파리 쪽(B) '+Math.round(f)+'ms, 주판봇 쪽(A) '+Math.round(r)+'ms예요. 평균은 A '+Math.round(mean(A))+'ms, B '+Math.round(mean(Bs))+'ms로 A가 더 낮았어요.',
  verdict:'평균이 낮아도 백에 하나가 오래 기다리면 그 서비스는 느리다. 초파리 승.',note:'시드 고정 로그정규 표본 각 1,000개(설명용). 막대는 P99, 짧을수록 좋아요.'};}});
''' % (_j.dumps(KNOWS, ensure_ascii=False), _j.dumps(APPS, ensure_ascii=False))

def spec():
    return {'meta': {'title': '시작 전에 정할 것 — 『Inference Engineering』 1장 연구실 해설', 'description': '인퍼런스 스터디 북 1주차 교재 · 1장: 공유 vs 전용, 앱의 성격, 모델 고르기·평가·미세조정·증류, TTFT·TPS·백분위',
                     'series': '인퍼런스 스터디 북', 'number': '01-2', 'slug': 'ch01_prerequisites', 'version': '2.0', 'date': '2026-11-11', 'creator': ['안상선'], 'license': 'CC BY-NC 4.0 (캐릭터 제외)', 'url': URL,
                     'kgStart': 'lab:concept/optimization-balance', 'citeKey': 'ahn2026ch01', 'domain': 'ai',
                     'suggestedCitation': '안상선 (2026). 시작 전에 정할 것 — 『Inference Engineering』 1장 연구실 해설. 인퍼런스 스터디 북 1주차. ' + URL},
            'kg': KG, 'refs': [book_ref()], 'gl': GL, 'core': CORE, 'quiz': QUIZ, 'js': JS,
            'nav': nav([('cast', '식구'), ('lv1', '① 균형'), ('lv2', '② 공유·전용'), ('lv3', '③ 앱'), ('lv4', '④ 모델'), ('lv5', '⑤ 측정'), ('duel', '대결'), ('sum', '정리'), ('kg', '색인'), ('export', '꾸러미')]),
            'body': cover('cover_01', '인퍼런스 스터디 북 · 1주차 · 1장', '연구실 식구 여섯이 운동장 같은 실험실에서 서로 다른 종목의 기구 앞에 선 대체 표지',
                          motif=''.join('<i class="%s"></i>' % c for c in ['on', 'on', 'on', 'on', 'on', 'a', 'a', 'm', 'on', 'on', 'a', 'm']),
                          moods={'doc': 'front', 'asst': 'report', 'fly': 'magnify', 'robo': 'chart', 'sia': 'explain', 'moa': 'cheer'})
                    + hero + cast + lv1 + lv2 + lv3 + lv4 + lv5 + duel_sec + summary + outro,
            'footer': footer([('교재', 'Kiely, P. (2026). Inference Engineering, Chapter 1 Prerequisites (1.1–1.4). Baseten Books.'), ('표 3개', '교재 1.1(공유 장단점), 1.2.1(앱 종류), 1.4(TTFT·TPS, 백분위) — 한국어로 옮김')],
                             ['② 칸의 API 단가·GPU 시간당 가격·처리량', '③ 칸 배치 곡선 상수', '④ 칸 증류 확률 막대', '⑤ 칸 응답 시간 표본 (로그정규, 시드 고정)', '대결의 두 배포 분포'],
                             prev=('../week_01_textbook_ch00/', '0장 추론이란 무엇인가'), nxt=('../week_01_article_01/', '1주차 논문 라이브벤치'))}

if __name__ == '__main__':
    out = os.path.join(sys.argv[1], SLUG, 'index.html')
    print(out, build(spec(), out))
