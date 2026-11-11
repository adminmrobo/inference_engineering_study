# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import *
from parts import *
from series import BASE

SLUG = 'week_01_textbook_ch00'; P = 'ch00'; URL = BASE + SLUG + '/'

hero = '''<header class="hero" id="top"><div class="wrap"><div class="hero-text">
<p class="eyebrow">인퍼런스 스터디 북 · 1주차 교재 · 0장 Inference</p>
<h1>추론이란 무엇인가</h1>
<p class="q">GPU를 사서 모델을 올리면 끝일까? 왜 생성 AI의 추론에는 '세 층'이 필요할까?</p>
<p>0장은 이 책 전체의 지도입니다. 모델의 일생을 <b>학습</b>과 <b>추론</b> 두 단계로 나누고, 생성 AI의 추론을 잘하려면 <b>런타임 · 인프라 · 도구</b> 세 층이 함께 맞물려야 한다고 말합니다. 그리고 1장부터 7장까지가 이 지도의 어디에 놓이는지 보여 줍니다.</p>
<div class="kpis" id="heroK"></div>
<p class="cite">교재: Kiely, P. (2026). <i>Inference Engineering</i>, Chapter 0. Baseten Books. 그림 0.1~0.3.</p>
<div class="dialog">''' + say('doc', 'think', '서문이 "왜"였다면 0장은 "무엇"이에요. 추론이 뭔지, 무엇으로 이뤄졌는지부터 지도를 그려 봅시다.') + say('asst', 'smile', '교재 그림 세 장을 따라가요. 0.1 세 층 쌓기, 0.2 추측 디코딩, 0.3 여러 클라우드 묶기.') + say('fly', 'point', '옛날 머신러닝은 CPU 한 대로도 추론했잖아. 생성 AI는 뭐가 그렇게 다른데?') + say('robo', 'chart', '기법이 여섯 개나 있다며? 다 켜면 여섯 배 빨라지는 거 아냐?') + say('sia', 'explain', '순서는 다섯 칸입니다. 두 단계 → 런타임 → 인프라 → 도구 → 책 지도.') + say('moa', 'smile', '각 칸 끝에서 퀴즈 두 개씩! 맞히면 오른쪽 아래 도우미에 기록돼요.') + '''</div></div></div></header>'''

cast = crew({'doc': '해설·심판. 세 층 지도를 그림', 'asst': '숫자 발표. 추측 디코딩 실험 진행', 'fly': '의심하는 쪽. "한 대만 빠르면 끝?"', 'robo': '확신하는 쪽. "기법을 다 켜자!"',
             'sia': '순서표·진행 신호', 'moa': '기록장·응원', 'x1': '방청석', 'x2': '방청석', 'x3': '방청석'},
            extra='<h3>오늘의 순서</h3>' + route([('lv1', '① 칸', '학습과 추론'), ('lv2', '② 칸', '런타임 층'), ('lv3', '③ 칸', '인프라 층'), ('lv4', '④ 칸', '도구 층'), ('lv5', '⑤ 칸', '책 지도'), ('duel', '대결', '초안을 쓸까?'), ('sum', '정리', '세 층 한 장')]))

big = section('big', '0', '큰 그림 — 세 층', '''
<div class="steps"><div><h4>런타임 (Runtime)</h4><p>GPU 한 대(또는 한 인스턴스 안의 여러 GPU) 위에서 <b>모델 하나</b>를 최대한 빠르고 효율적으로 돌리는 층.</p></div>
<div><h4>인프라 (Infrastructure)</h4><p>클러스터·지역·클라우드를 넘나들며 <b>규모를 키우고</b>, 고립된 칸(사일로) 없이 가동률을 지키는 층.</p></div>
<div><h4>도구 (Tooling)</h4><p>엔지니어에게 <b>알맞은 추상화</b>를 줘서 통제력과 생산성의 균형을 잡는 층.</p></div></div>
<figure class="fig"><div class="svgwrap"><svg viewBox="0 0 760 250" role="img" aria-label="그림 0.1을 다시 그린 세 층 도식: 아래부터 인프라, 런타임, 도구">
<rect x="10" y="170" width="740" height="66" rx="10" fill="#1d2a3a" stroke="#82b8ff"/><text x="24" y="192" fill="#82b8ff" font-size="14" font-weight="700">인프라</text>
<text x="24" y="218" fill="#eceaf3" font-size="13">GPU · 저장장치 · 네트워크 · 라우팅 · 로드 밸런싱 · 자동 확장 · 멀티 클라우드 용량 관리</text>
<rect x="10" y="64" width="740" height="98" rx="10" fill="#2a1d33" stroke="#d672d6"/><text x="24" y="86" fill="#d672d6" font-size="14" font-weight="700">런타임</text>
<text x="24" y="112" fill="#eceaf3" font-size="13">모델 성능 기법: 배칭 · 캐싱 · 양자화 · 추측 · 병렬화 · 분리</text>
<text x="24" y="136" fill="#9d9bb8" font-size="13">추론 엔진 vLLM · SGLang · TensorRT-LLM → PyTorch → CUDA</text>
<rect x="10" y="10" width="740" height="46" rx="10" fill="#1d3329" stroke="#5ee39c"/><text x="24" y="38" fill="#5ee39c" font-size="14" font-weight="700">도구</text><text x="80" y="38" fill="#eceaf3" font-size="13">엔지니어가 보는 추상화 (블랙박스 ↔ 기본 부품)</text></svg></div>
<figcaption>교재 그림 0.1을 글자 위주로 다시 그린 도식. 원문 그림은 교재를 보세요.</figcaption></figure>
''' + say('sia', 'guide', '아래 다섯 칸은 이 세 층을 아래에서 위로가 아니라, 일이 생기는 순서대로 따라갑니다.'), tags=[('g', '그림 0.1')])

lv1 = level(1, 'lv1', '두 단계 — 학습과 추론', [('g', '모델: 생성 AI 모델의 일생'), ('p', '교재: 0장 첫머리')],
    pair=('연구실에서는', '새 시약을 개발하는 건 한 번이지만, 그 시약을 써서 실험하는 일은 매일 수백 번 일어납니다. 개발실과 실험실은 다른 기술이 필요해요.', '모델에서는', '<b>학습</b>은 데이터에서 가중치를 배우는 과정이고, <b>추론</b>은 그 모델을 실제 서비스로 돌리는 과정이에요 <span class="chip-src">원문</span>. 학습은 몇 번, 추론은 요청마다 일어납니다.'),
    panel=panel('학습은 한 번, 추론은 요청마다', 'cLife', '학습 블록 하나 뒤로 추론 요청이 날마다 쌓이는 모습. 개수는 설명용입니다.',
                ctrl=slider('lR', '하루 요청', 100, 100000, 100, 10000, '') + slider('lD', '서비스 일수', 1, 365, 1, 30, '일') + btn_group('lM', '모델', [('ml', '고전 ML (XGBoost)'), ('gen', '생성 AI (LLM)')], 1),
                kp_id='lK', ins_id='lI'),
    explain=explain('풀이', ['지난 10년의 머신러닝 붐에서 많은 데이터 과학자가 학습부터 추론까지 다 해 봤어요. 고전 머신러닝의 추론은 비교적 단순했어요.', '교재 저자의 회사도 초기에는 XGBoost 같은 모델을 가벼운 CPU와 단순한 소프트웨어로 돌렸다고 합니다.', '생성 AI는 다릅니다. 가중치를 받고 GPU를 사도, 큰 규모의 서비스에 맞게 빠르고 안정적이지 않아요. 그래서 세 층이 필요해요.'],
                    limit='"학습은 한 번"은 단순화예요. 실제로는 미세조정·재학습이 반복됩니다. 하지만 추론이 요청마다 쌓인다는 점은 그대로예요.'),
    bridge=bridge(gen=('챗봇에 질문 하나를 보내면 그때마다 추론이 한 번 돌아요. 사용자가 많을수록 추론 비용이 학습 비용을 금세 넘어설 수 있어요.', '정확한 비율은 모델·사용량마다 다릅니다.'),
                  field=('공장의 금형(학습)은 한 번 만들지만 사출(추론)은 제품마다 반복됩니다. 사출 공정의 효율이 원가를 정해요.', '금형과 달리 모델은 같은 입력에도 매번 계산이 필요합니다.')),
    talk=say('fly', 'clip', '그러니까 "모델을 만든다"와 "모델을 서비스한다"는 다른 일이라는 거지. 둘째가 이 책이고.'))

lv2 = level(2, 'lv2', '런타임 층 — 여섯 가지 모델 성능 기법', [('g', '모델: 런타임 최적화'), ('p', '교재: 그림 0.2')],
    pair=('연구실에서는', '실험대 하나를 잘 쓰는 요령이 여러 가지 있어요: 시료를 모아서 한 번에(배칭), 쓴 시약 재사용(캐싱), 덜 정밀한 저울로 충분할 땐 그걸로(양자화)…', '모델에서는', '런타임 층은 쿠다 → 파이토치 → vLLM·SGLang·TensorRT-LLM 같은 추론 엔진 위에서, <b>배칭·캐싱·양자화·추측·병렬화·분리</b> 여섯 기법을 씁니다 <span class="chip-src">원문</span>. 플래시어텐션 같은 커널도 큰 성능 차이를 냅니다.'),
    panel=panel('기법 카드 — 무엇을 줄이고 무엇을 늘리나', None, '', ctrl=btn_group('rT', '기법', [('batch', '배칭'), ('cache', '캐싱'), ('quant', '양자화'), ('spec', '추측'), ('par', '병렬화'), ('dis', '분리')]), ins_id='rI')
          + panel('그림 0.2 따라 하기 — 추측 디코딩', 'cSpec', '초안 토큰을 여러 개 내고 큰 모델이 한 번에 검증하는 모습. 초록은 받아들인 토큰, 빨강은 버린 토큰.',
                  ctrl=slider('sA', '초안 적중률', 0.1, 0.95, 0.05, 0.7, '') + slider('sK', '초안 개수', 1, 8, 1, 4, '개') + '<button class="bt primary" id="sGo">한 번 더 생성</button>',
                  kp_id='sK2', eq='한 번 검증에 나오는 토큰 수 (기댓값) = (1 − a<sup>k+1</sup>) / (1 − a) &nbsp;·&nbsp; a = 적중률, k = 초안 개수', ins_id='sI'),
    explain=explain('풀이', ['보통 디코딩은 큰 모델을 한 번 돌릴 때(순전파 한 번) 토큰을 <b>하나</b> 냅니다.', '추측 디코딩은 작은 쪽이 초안 토큰 여러 개를 먼저 쓰고, 큰 모델이 한 번에 검증해요. 맞은 데까지 받아들이고 틀린 곳부터 버립니다(그림 0.2의 "tel·le·vis·ion" → "tel·le·scope").', '초안이 잘 맞으면 한 번에 여러 토큰이 나와서 지연시간이 줄어요. 자세한 방법은 5장 5.2절이에요.'],
                    limit='기법 여섯 개는 서로 겹치기도 하고 부딪치기도 해요. "다 켜면 여섯 배"가 아닙니다. 그리고 한 대가 아무리 빨라도 트래픽은 결국 넘칩니다 → ③ 칸.'),
    bridge=bridge(gen=('챗봇의 답이 "타다닥" 빠르게 나오는 데에는 배칭·캐싱·추측 같은 런타임 기법이 숨어 있어요. 이미지·음성·영상 모델에도 같은 기법들이 쓰입니다.', '모델 종류마다 맞는 기법이 달라요(6장).'),
                  field=('반복되는 서식 문서를 처리할 때 앞부분이 같으면 캐싱 효과가 큽니다.', '문서마다 앞부분이 다 다르면 캐싱 이득이 작아요.')) + math('기댓값 식은 어디서 왔나', '<p>초안 k개가 각각 확률 a로 맞고, 처음 틀린 곳에서 멈춘다고 하면, 한 번 검증에서 얻는 토큰 수의 기댓값은 1 + a + a² + … + a<sup>k</sup> = (1 − a<sup>k+1</sup>)/(1 − a) 입니다(마지막 1개는 큰 모델이 직접 내는 토큰). 추측 디코딩 연구에서 흔히 쓰는 단순화이고, 교재 0장에는 이 식이 없습니다. 이 페이지에서는 설명용으로 씁니다.</p>'),
    talk=say('robo', 'calc', '적중률 0.7, 초안 4개면 한 번에 2.8개쯤? 그럼 거의 세 배잖아! …아, 검증하는 데도 시간이 드는구나.'))

lv3 = level(3, 'lv3', '인프라 층 — 자동 확장에서 하나의 풀까지', [('g', '모델: 추론 인프라'), ('p', '교재: 그림 0.3')],
    pair=('연구실에서는', '실험실이 세 건물에 흩어져 있으면, 한 건물은 줄이 길고 다른 건물 실험대는 비어 있기도 해요. 예약을 하나로 합치면 빈자리를 바로 씁니다.', '모델에서는', '처음엔 <b>자동 확장</b>(언제 복제본을 늘리고 줄이나), 몇백 GPU를 넘으면 <b>용량</b>(GPU를 충분히 구하기)이 문제가 됩니다. 여러 지역·여러 클라우드로 퍼지면 <b>사일로</b>가 생기고, 마지막 단계는 모든 자원을 <b>하나의 풀</b>로 다루는 전 지구적 시스템이에요 <span class="chip-src">원문</span>.'),
    panel=panel('사일로 vs 하나의 풀', 'cPool', '세 클러스터의 수요와 용량. 사일로에서는 넘친 요청을 이웃이 받지 못하고, 풀에서는 남는 자리로 보냅니다. 수요는 시드 고정 설명용 값.',
                ctrl=btn_group('pM', '방식', [('silo', '사일로 (따로따로)'), ('pool', '하나의 풀')]) + slider('pS', '수요 쏠림', 0, 1, 0.1, 0.6, '') + '<button class="bt" id="pNext">다음 시간대</button>',
                kp_id='pK', ins_id='pI'),
    explain=explain('풀이', ['런타임을 아무리 최적화해도, 서버 한 대는 언젠가 감당 못 할 트래픽을 받습니다. 교재는 이것을 "쿠다나 파이토치 문제가 아니라 시스템 문제"라고 말해요.', '규모가 커질수록 문제의 성격이 바뀝니다: 자동 확장 → 용량 → 사일로 → 하나의 풀.', '여러 클라우드에 걸친 인프라는 가동률도 높여요(한 지역·한 클라우드가 멈춰도 버팀). 사용자 가까이에서 돌리면 전체 지연시간도 줄어요.'],
                    limit='하나의 풀은 강력하지만 만들기 어렵습니다. 그리고 아무리 좋은 인프라도 엔지니어가 쓰기 어려우면 소용없어요 → ④ 칸.'),
    bridge=bridge(gen=('전 세계 사용자가 쓰는 챗봇은 미국·유럽·아시아의 GPU를 묶어 씁니다. 사용자 가까운 곳에서 답하면 더 빨라요.', '데이터를 어느 나라에서 처리해도 되는지(1장 규제)가 풀을 제한할 수 있어요.'),
                  field=('콜센터의 지역별 상담원을 하나의 대기열로 묶는 것과 비슷해요.', '상담원과 달리 GPU는 모델을 미리 올려 둬야 해서 옮기는 데 시간이 걸립니다(7장 콜드 스타트).')),
    talk=say('moa', 'think', '사일로에서 버린 요청이 풀에서는 남은 칸으로 갔어요. 같은 GPU 수인데도요!'))

lv4 = level(4, 'lv4', '도구 층 — 블랙박스와 부품 사이', [('g', '모델: 개발자 경험'), ('p', '교재: 0장 후반')],
    pair=('연구실에서는', '버튼 하나로 끝나는 자동 분석기는 편하지만 조건을 못 바꾸고, 부품만 잔뜩 있는 실험대는 뭐든 되지만 하루 종일 조립해야 해요.', '모델에서는', '한쪽 끝은 <b>블랙박스</b>(가중치를 주면 API가 나옴), 다른 끝은 컴퓨트·네트워크·디스크 같은 <b>기본 부품</b>만 주는 것. 알맞은 개발자 경험은 그 사이 어딘가라고 교재는 말합니다 <span class="chip-src">원문</span>.'),
    panel=panel('추상화 손잡이', 'cAbs', '추상화 정도에 따라 통제력과 생산성이 반대로 움직이는 모습. 곡선은 설명용입니다.', ctrl=slider('aX', '추상화', 0, 100, 1, 50, ''), kp_id='aK', ins_id='aI'),
    explain=explain('풀이', ['통제력이 너무 적으면 중요한 서비스를 믿고 맡길 수 없어요.', '추상화가 너무 낮으면 매번 바닥부터 만들어 생산성이 떨어져요.', '그래서 추론 플랫폼을 만드는 쪽(외부 업체든 사내 팀이든)은 도구·개발자 경험을 세 번째 층으로 함께 설계해야 합니다.'],
                    limit='"알맞은 지점"은 팀과 서비스마다 다르고, 교재도 이것을 주관적이라고 말합니다. 그래프의 가운데 표시는 설명용이에요.'),
    talk=say('asst', 'report', '손잡이 50 근처에서 두 막대의 합이 가장 커요. 하지만 이 곡선 자체가 설명용이라, 실제 지점은 팀이 정해요.'))

CH = [(1, '시작 전에 정할 것', 'pre', '사용 사례 정의, 지연시간·비용 예산, 모델 고르기·평가'), (2, '모델', 'run', '모델 구조와 병목, 어텐션 최적화'), (3, '하드웨어', 'run', 'GPU 사양: 연산과 메모리, 엔비디아 세대, 다른 가속기'),
      (4, '소프트웨어', 'run', 'CUDA → PyTorch·Transformers·Diffusers → vLLM·SGLang·TensorRT-LLM, Dynamo'), (5, '최적화 기법', 'run', '양자화, 추측 디코딩, KV 캐시 재사용, 병렬화, 분리'),
      (6, '입출력 유형', 'run', 'VLM, 임베딩, 음성 인식(ASR), 음성 합성, 이미지·영상 생성'), (7, '운영', 'infra', '운영 인프라와 성능 좋은 애플리케이션 만들기')]
lv5 = level(5, 'lv5', '책 지도 — 1장부터 7장까지', [('g', '모델: 이 책의 구성'), ('p', '교재: 0장 끝')],
    panel=panel('장을 누르면 지도에 불이 들어와요', 'cMap', '1장부터 7장이 세 층 지도의 어디에 놓이는지 보여 주는 도식.', ctrl=btn_group('mC', '장', [(str(n), '%d장' % n) for n, *_ in CH]), ins_id='mI'),
    explain=explain('풀이', ['1장은 추론 엔지니어링을 시작하기 <b>전</b>의 일 — 제품 생각과 AI 엔지니어링이에요.', '2~6장은 대부분 런타임 층(모델·하드웨어·소프트웨어·기법·입출력 유형), 7장은 운영(인프라)이에요.', '부록 A는 용어집, 부록 B는 더 읽을 거리입니다.'],
                    limit='장과 층이 일대일로 딱 맞지는 않아요. 예를 들어 4장의 Dynamo는 분산 서빙(인프라 쪽)과도 닿아 있어요. 그리고 이 책은 2026년 1월에 마무리되었다고 밝힙니다 — 세부는 바뀌어도 원리는 오래간다고요.'),
    talk=say('sia', 'proud', '스터디 10주 지도와 거의 같아요: 1주차 0·1장, 2·3주차 2장, 4주차 3장… 순서대로 확인했습니다.'))

duel_sec = section('duel', 'VS', '대결 — 초안을 쓸까, 한 글자씩 갈까?', say('doc', 'think', '그림 0.2의 추측 디코딩을 판으로 붙입니다. 60토큰짜리 답을 내는 데 큰 모델을 몇 번 돌려야 하는지로 겨뤄요.') + duel(
    '60토큰을 만드는 데 큰 모델 순전파가 더 적게 드는 쪽은?', '한 번에 한 토큰씩 (보통 디코딩)', '초안이 틀리면 헛수고잖아. 정직하게 하나씩.', '초안 4개 + 한 번에 검증 (적중률 0.7)', '네 개씩 베팅! 맞으면 한 번에 여러 개 번다고.') + '<p class="notice">판정: 시드 고정 시뮬레이션의 순전파 횟수(적을수록 좋음). 초안을 만드는 작은 모델의 비용은 이 판에서 빼고 셉니다 — 그 비용까지는 5장에서.</p>', small='판', tags=[('g', '판정 기준: 큰 모델 순전파 횟수')])

summary = section('sum', '정리', '정리 — 세 층 한 장', '''
<div class="tw"><table class="tb"><tr><th>칸</th><th>무엇</th><th>대표 낱말</th><th>한계 → 다음 칸</th></tr>
<tr><td>① 두 단계</td><td>학습(가중치 배우기) vs 추론(서비스로 돌리기)</td><td>XGBoost·CPU vs 생성 AI·GPU</td><td>생성 AI는 GPU만으론 안 됨</td></tr>
<tr><td>② 런타임</td><td>모델 하나를 GPU 위에서 빠르게</td><td>배칭·캐싱·양자화·추측·병렬화·분리</td><td>한 대는 결국 넘침</td></tr>
<tr><td>③ 인프라</td><td>규모 키우기, 사일로 없애기</td><td>자동 확장 → 용량 → 하나의 풀</td><td>쓰기 어려우면 소용없음</td></tr>
<tr><td>④ 도구</td><td>알맞은 추상화</td><td>블랙박스 ↔ 기본 부품</td><td>알맞은 지점은 팀마다</td></tr>
<tr><td>⑤ 책 지도</td><td>1~7장 위치</td><td>준비(1) · 런타임(2~6) · 운영(7)</td><td>세부는 바뀌어도 원리는 남음</td></tr></table></div>
<div class="notebook"><h4>모아의 기록장</h4><ul><li>추론 = 생성 AI 모델의 일생 중 두 번째 단계</li><li>런타임 기법은 LLM만이 아니라 VLM·임베딩·음성·이미지·영상 모델에도 쓰인다</li><li>인프라 문제는 몇백 GPU쯤부터 "용량" 문제가 된다</li><li>책 마무리: 2026년 1월</li></ul></div>
''' + say('moa', 'ok', '기록 완료! 다음은 1장, 추론 엔지니어링을 시작하기 전에 정할 다섯 가지예요.'), small='끝', tags=[('g', '다섯 칸 비교')])

outro = section('outro', '끝', '아웃트로', '<div class="outro"><div class="scene" data-img="sc_00_outro" role="img" aria-label="연구실 식구 여섯이 세 층 도식 앞에 선 장면"><img data-who="robo" data-mood="happy" alt=""><img data-who="doc" data-mood="magic" alt=""><img data-who="asst" data-mood="spark" alt=""><img data-who="sia" data-mood="proud" alt=""><img data-who="moa" data-mood="sparkle" alt=""><img data-who="fly" data-mood="coffee" alt=""></div></div>'
    + say('doc', 'magic', '0장의 한 줄: 생성 AI 추론은 <b>런타임·인프라·도구</b> 세 층이 함께 맞물려야 큰 규모에서 믿고 쓸 수 있다.')
    + say('robo', 'happy', '초안 베팅이 통했지! 다음에도 여기에 투자.')
    + say('fly', 'coffee', '…적중률이 높을 때 얘기야. 0.3으로 내려 보면 금방 알걸. 그건 5장에서 다시 붙자.')
    + say('asst', 'spark', '다음은 1장이에요. 최적화를 하기 전에 "무엇이 최선인지"부터 정해요.'), small='', tags=())

GL = {'학습': ['학습 (training)', '개념', '데이터에서 모델 가중치를 배우는 과정.'], '추론': ['추론 (inference)', '개념', '생성 AI 모델을 실제 서비스에서 돌리는 과정.'],
      '런타임': ['런타임 층 (runtime)', '층', '모델 하나를 GPU 인스턴스 위에서 최대한 빠르고 효율적으로 돌리는 층.'], '인프라': ['인프라 층 (infrastructure)', '층', '클러스터·지역·클라우드에 걸쳐 규모를 키우고 가동률을 지키는 층.'],
      '도구': ['도구 층 (tooling)', '층', '엔지니어에게 알맞은 추상화를 주는 층.'], '배칭': ['배칭 (batching)', '기법', '들어오는 요청들을 토큰 단위로 엮어 함께 처리해 처리량을 높인다.'],
      '캐싱': ['캐싱 (caching)', '기법', '앞부분(접두사)이 같은 요청끼리 KV 캐시를 재사용한다.'], '양자화': ['양자화 (quantization)', '기법', '모델 일부의 숫자 정밀도를 낮춰 연산을 늘리고 메모리 부담을 줄인다.'],
      '추측 디코딩': ['추측 디코딩 (speculative decoding)', '기법', '초안 토큰을 만들고 검증해 순전파 한 번에 토큰을 여러 개 낸다.'], '병렬화': ['병렬화 (parallelism)', '기법', 'GPU 여러 장으로 큰 모델을 새 병목 없이 빠르게 돌린다.'],
      '분리': ['분리 (disaggregation)', '기법', 'LLM 추론의 두 단계(프리필·디코드)를 따로 확장되는 일꾼에 나눈다.'], 'KV 캐시': ['KV 캐시', '용어', '어텐션 계산 결과(키·값)를 저장해 둔 것.'],
      '사일로': ['사일로 (silo)', '용어', '한 클러스터는 모자라고 다른 클러스터는 남는, 서로 나눠 쓰지 못하는 상태.'], '자동 확장': ['자동 확장 (autoscaling)', '기법', '트래픽에 따라 복제본을 늘리고 줄이는 일. 7장.'],
      '순전파': ['순전파 (forward pass)', '용어', '입력을 넣어 모델을 한 번 계산하는 것. 보통 디코딩은 순전파 한 번에 토큰 하나.'], '추론 엔진': ['추론 엔진 (inference engine)', '소프트웨어', 'vLLM·SGLang·TensorRT-LLM처럼 모델 서빙에 맞춘 실행 소프트웨어. 4장.'],
      '커널': ['커널 (kernel)', '소프트웨어', 'GPU에서 실행되는 계산 단위. 플래시어텐션이 대표 예(3주차 논문).'], '토큰': ['토큰 (token)', '용어', '모델이 읽고 쓰는 글자 조각.']}
CORE = ['학습', '추론', '런타임', '인프라', '도구', '배칭', '캐싱', '양자화', '추측 디코딩', '병렬화', '분리', '사일로']
QUIZ = {'lv1': [{'q': '교재가 말하는 생성 AI 모델 일생의 두 번째 단계는?', 'o': ['데이터 수집', '학습', '추론'], 'a': 2, 'why': '맞아요. 학습 다음이 추론(서비스로 돌리기)이에요.', 'hint': '이 책의 제목을 떠올려 보세요.'},
                {'q': '고전 머신러닝 추론과 생성 AI 추론의 차이로 교재가 든 것은?', 'o': ['고전 ML은 GPU가 꼭 필요했다', '생성 AI는 가중치와 GPU만으로는 큰 규모에서 빠르고 안정적이지 않다', '둘은 같다'], 'a': 1, 'why': '맞아요. 그래서 세 층이 필요하다고 해요.', 'hint': '① 칸 풀이 3번을 보세요.'}],
        'lv2': [{'q': '[계산] 초안 적중률 a=0.5, 초안 k=1개일 때 한 번 검증에서 나오는 토큰 수의 기댓값은? (1 − a^(k+1))/(1 − a)', 'o': ['1.0', '1.5', '2.0'], 'a': 1, 'why': '맞아요. (1 − 0.25)/0.5 = 1.5.', 'hint': '0.5의 제곱은 0.25예요.'},
                {'q': '프리필과 디코드를 따로 확장되는 일꾼에 나누는 기법은?', 'o': ['양자화', '분리(disaggregation)', '캐싱'], 'a': 1, 'why': '맞아요. 5장 5.5절에서 자세히 다뤄요.', 'hint': '기법 카드 마지막 것을 눌러 보세요.'}],
        'lv3': [{'q': '교재에 따르면 인프라 문제가 "용량" 문제로 바뀌는 대략의 규모는?', 'o': ['GPU 몇 장', 'GPU 몇백 장', 'GPU 수백만 장'], 'a': 1, 'why': '맞아요. 대략 몇백 GPU를 넘으면 GPU를 충분히 구하는 일이 핵심이 됩니다.', 'hint': '③ 칸 짝 카드 오른쪽을 보세요.'},
                {'q': '사일로를 하나의 풀로 바꾸면 같은 GPU 수에서 무엇이 줄어드나?', 'o': ['버려지는(처리 못 한) 요청', 'GPU 메모리', '모델 크기'], 'a': 0, 'why': '맞아요. 남는 칸으로 보낼 수 있어서 버리는 요청이 줄어요.', 'hint': '시뮬레이션의 빨간 칸을 비교해 보세요.'}],
        'lv4': [{'q': '교재가 말하는 알맞은 개발자 경험의 위치는?', 'o': ['완전한 블랙박스', '기본 부품만', '그 사이 어딘가'], 'a': 2, 'why': '맞아요. 믿고 돌릴 통제력과 일할 만한 추상화가 함께 있어야 해요.', 'hint': '손잡이를 양 끝으로 밀어 보세요.'}],
        'lv5': [{'q': '추론 엔지니어링을 시작하기 "전"의 일(사용 사례, 예산, 모델 평가)을 다루는 장은?', 'o': ['1장', '4장', '7장'], 'a': 0, 'why': '맞아요. 1장 Prerequisites.', 'hint': '다음 페이지 제목이에요.'},
                {'q': '양자화·추측 디코딩·KV 캐시 재사용·병렬화·분리를 다루는 장은?', 'o': ['3장 하드웨어', '5장 최적화 기법', '6장 입출력 유형'], 'a': 1, 'why': '맞아요. 스터디에서는 6·7주차에 나눠 읽어요.', 'hint': '책 지도에서 5장을 눌러 보세요.'}]}

KG = {'version': '1.0', 'page': P, 'nodes': [
    node('lab:concept/training', 'Concept', '학습', 'training', '#lv1', P, '데이터에서 가중치를 배우는 과정.', ('kiely2026inference', '0장'), 1, 'basics'),
    node('lab:concept/inference', 'Concept', '추론', 'inference', '#lv1', P, '생성 AI 모델을 서비스에서 돌리는 과정.', ('kiely2026inference', '0장'), 1, 'basics'),
    node('lab:concept/runtime-layer', 'Concept', '런타임 층', 'runtime layer', '#lv2', P, '모델 하나를 GPU 인스턴스 위에서 빠르게 돌리는 층.', ('kiely2026inference', '0장, 그림 0.1'), 2),
    node('lab:concept/infrastructure-layer', 'Concept', '인프라 층', 'infrastructure layer', '#lv3', P, '클러스터·지역·클라우드에 걸친 확장과 가동률.', ('kiely2026inference', '0장, 그림 0.3'), 2),
    node('lab:concept/tooling-layer', 'Concept', '도구 층', 'tooling layer', '#lv4', P, '알맞은 추상화를 주는 층.', ('kiely2026inference', '0장'), 2),
    node('lab:method/batching', 'Method', '배칭', 'batching', '#lv2', P, '요청을 토큰 단위로 엮어 처리량을 높인다.', ('kiely2026inference', '0장'), 2),
    node('lab:method/caching', 'Method', '캐싱 (KV 캐시 재사용)', 'caching (KV cache re-use)', '#lv2', P, '접두사가 같은 요청끼리 KV 캐시를 재사용한다.', ('kiely2026inference', '0장'), 2),
    node('lab:method/quantization', 'Method', '양자화', 'quantization', '#lv2', P, '일부 정밀도를 낮춰 연산을 늘리고 메모리를 줄인다.', ('kiely2026inference', '0장'), 2),
    node('lab:method/speculative-decoding', 'Method', '추측 디코딩', 'speculative decoding', '#lv2', P, '초안 토큰을 만들고 검증해 순전파 한 번에 여러 토큰.', ('kiely2026inference', '0장, 그림 0.2'), 3),
    node('lab:method/parallelism', 'Method', '병렬화', 'model parallelism', '#lv2', P, 'GPU 여러 장 활용.', ('kiely2026inference', '0장'), 3),
    node('lab:method/disaggregation', 'Method', '분리', 'disaggregation', '#lv2', P, '프리필과 디코드를 따로 확장되는 일꾼에.', ('kiely2026inference', '0장'), 3),
    node('lab:method/autoscaling', 'Method', '자동 확장', 'autoscaling', '#lv3', P, '복제본을 늘리고 줄이기.', ('kiely2026inference', '0장'), 2),
    node('lab:method/unified-pool', 'Method', '하나의 풀', 'unified compute pool', '#lv3', P, '모든 자원을 하나의 계산 풀로 다루는 전 지구적 시스템.', ('kiely2026inference', '0장, 그림 0.3'), 3),
    node('lab:limitation/single-instance', 'Limitation', '한 대는 결국 넘친다', 'single instance saturates', '#lv2', P, '런타임 최적화만으로는 트래픽 증가를 감당 못 한다.'),
    node('lab:limitation/silos', 'Limitation', '사일로', 'silos', '#lv3', P, '한쪽은 모자라고 한쪽은 남는 상태.'),
    node('lab:limitation/genai-complex', 'Limitation', '가중치 + GPU만으로는 부족', 'weights plus GPUs is not enough', '#lv1', P, '생성 AI 추론은 큰 규모에서 빠르고 안정적이지 않다.'),
    node('lab:limitation/hard-to-use', 'Limitation', '쓰기 어려운 인프라', 'infrastructure without usable tooling', '#lv3', P, '좋은 인프라도 추상화가 맞지 않으면 생산성이 떨어진다.'),
    node('lab:metric/forward-passes', 'Metric', '순전파 횟수', 'forward passes', '#duel', P, '큰 모델을 몇 번 돌렸나.', None, 2, 'evaluation'),
    node('lab:claim/three-layers', 'Claim', '추론을 잘하려면 세 층이 필요', 'three layers: runtime, infrastructure, tooling', '#big', P, None, ('kiely2026inference', '0장')),
    node('lab:claim/capacity-scale', 'Claim', '몇백 GPU부터 용량 문제', 'capacity problems past a few hundred GPUs', '#lv3', P, None, ('kiely2026inference', '0장')),
    node('lab:claim/cutoff', 'Claim', '책 마무리 2026년 1월', 'book finished January 2026', '#lv5', P, None, ('kiely2026inference', '0장')),
    node('lab:analogy/reagent-lab', 'Analogy', '시약 개발실 ↔ 실험실', 'development room vs lab bench', '#lv1', P), node('lab:analogy/three-buildings', 'Analogy', '세 건물 예약 합치기 ↔ 하나의 풀', 'merged booking', '#lv3', P),
    node('lab:question/core', 'Question', '왜 생성 AI 추론에는 세 층이 필요할까?', 'Why three layers?', '#top', P), node('lab:question/duel', 'Question', '대결: 초안을 쓸까?', 'Duel: speculate?', '#duel', P),
    node('lab:question/low-acceptance', 'Question', '적중률이 낮으면 추측 디코딩은? (5장)', 'Speculation at low acceptance?', '#sum', P),
    node('lab:sim/lifecycle', 'Simulation', '학습 한 번, 추론 요청마다', 'lifecycle counter', '#lv1', P), node('lab:sim/speculation', 'Simulation', '추측 디코딩 따라 하기', 'speculation demo', '#lv2', P),
    node('lab:sim/pool', 'Simulation', '사일로 vs 풀', 'silo vs pool', '#lv3', P), node('lab:sim/abstraction', 'Simulation', '추상화 손잡이', 'abstraction dial', '#lv4', P),
    node('lab:work/kiely2026inference', 'Work', 'Kiely (2026) Inference Engineering', 'Kiely 2026', '#top', P)],
 'edges': [edge('lab:concept/training', 'prerequisiteOf', 'lab:concept/inference', '#lv1'), edge('lab:concept/inference', 'hasLimitation', 'lab:limitation/genai-complex', '#lv1'),
           edge('lab:limitation/genai-complex', 'addressedBy', 'lab:concept/runtime-layer', '#lv2'), edge('lab:concept/runtime-layer', 'hasLimitation', 'lab:limitation/single-instance', '#lv2'),
           edge('lab:limitation/single-instance', 'addressedBy', 'lab:concept/infrastructure-layer', '#lv3'), edge('lab:concept/infrastructure-layer', 'hasLimitation', 'lab:limitation/silos', '#lv3'),
           edge('lab:limitation/silos', 'addressedBy', 'lab:method/unified-pool', '#lv3'), edge('lab:method/unified-pool', 'hasLimitation', 'lab:limitation/hard-to-use', '#lv3'), edge('lab:limitation/hard-to-use', 'addressedBy', 'lab:concept/tooling-layer', '#lv4'),
           ] + [edge('lab:method/' + m, 'partOf', 'lab:concept/runtime-layer', '#lv2') for m in ['batching', 'caching', 'quantization', 'speculative-decoding', 'parallelism', 'disaggregation']] + [
           edge('lab:method/autoscaling', 'partOf', 'lab:concept/infrastructure-layer', '#lv3'), edge('lab:method/unified-pool', 'partOf', 'lab:concept/infrastructure-layer', '#lv3'),
           edge('lab:claim/three-layers', 'assertedIn', 'lab:work/kiely2026inference', '#big'), edge('lab:claim/capacity-scale', 'assertedIn', 'lab:work/kiely2026inference', '#lv3'), edge('lab:claim/cutoff', 'assertedIn', 'lab:work/kiely2026inference', '#lv5'),
           edge('lab:sim/speculation', 'relatedTo', 'lab:method/speculative-decoding', '#lv2'), edge('lab:sim/pool', 'relatedTo', 'lab:method/unified-pool', '#lv3'), edge('lab:metric/forward-passes', 'relatedTo', 'lab:method/speculative-decoding', '#duel'),
           edge('lab:analogy/three-buildings', 'relatedTo', 'lab:method/unified-pool', '#lv3'), edge('lab:analogy/reagent-lab', 'relatedTo', 'lab:concept/inference', '#lv1')]}

TECH = {'batch': ('배칭', '들어오는 요청들을 토큰 단위로 엮어 함께 처리합니다.', '처리량 ↑', '요청 하나의 대기 시간이 늘 수 있어요'),
        'cache': ('캐싱', '접두사가 같은 요청끼리 KV 캐시(어텐션 계산 결과)를 재사용합니다.', '중복 계산 ↓, 첫 토큰 지연 ↓', '캐시를 둘 메모리가 필요해요'),
        'quant': ('양자화', '모델 일부의 숫자 정밀도를 낮춰 더 많은 연산을 쓰고 메모리 부담을 줄입니다.', '속도 ↑, 메모리 ↓', '품질이 떨어질 위험 → 기준선과 비교 필요'),
        'spec': ('추측', '초안 토큰을 만들고 검증해 디코드 순전파 한 번에 토큰을 여러 개 냅니다.', '지연시간 ↓', '초안이 자주 틀리면 이득이 작아요'),
        'par': ('병렬화', 'GPU 여러 장으로 큰 모델을 빠르게 돌립니다. 새 병목을 만들지 않는 게 관건이에요.', '큰 모델 지연시간 ↓', 'GPU 사이 통신이 병목이 될 수 있어요'),
        'dis': ('분리', 'LLM 추론의 두 단계, 프리필과 디코드를 따로 확장되는 일꾼에 나눕니다.', '단계별 맞춤 확장', '두 일꾼 사이 KV 캐시를 옮겨야 해요')}
import json as _j
JS = r'''
var C=L.C,F=L.FONT,fit=L.fit,grid=L.grid,stamp=L.stamp,TECH=%s;
L.kpis('#heroK',[[2,'단계 (학습·추론)','g'],[3,'층 (런타임·인프라·도구)','m'],[6,'런타임 기법','i'],[7,'이어지는 장 (1~7장)','a']]);
/* ① */
var cL=$('#cLife'),lr=10000,ld=30,lm='gen',lt=0;
function drawL(dt){lt+=dt;var W=fit(cL,200),x=cL.getContext('2d');x.clearRect(0,0,W,200);grid(x,W,200);
  x.fillStyle='rgba(214,114,214,.5)';x.fillRect(20,60,70,80);x.fillStyle=C.text;x.font='700 13px '+F;x.textAlign='center';x.fillText('학습',55,104);x.font='11px '+F;x.fillText('1번',55,122);
  var cols=Math.max(10,Math.floor((W-130)/9)),n=Math.min(cols*14,Math.round(ld*4));for(var i=0;i<n;i++){var px=110+(i%%cols)*9,py=30+Math.floor(i/cols)*10;var on=((i+Math.floor(lt*20))%%cols)<2;x.fillStyle=on?C.gfp:'rgba(94,227,156,.45)';x.fillRect(px,py,7,7);}
  x.fillStyle=C.muted;x.font='12px '+F;x.textAlign='left';x.fillText('추론 요청 (점 하나 = 많은 요청)',110,190);stamp(x,W,'설명용 · 개수 눈금 없음');}
function updL(){L.setTxt('#lRV',(+lr).toLocaleString());L.setTxt('#lDV',ld+'일');var tot=lr*ld;
  L.kpis('#lK',[['1','학습 (한 번)','m'],[tot.toLocaleString(),'추론 요청 합계','g'],[lm==='gen'?'GPU':'CPU','주로 쓰는 장치','i'],[lm==='gen'?'3층 필요':'단순한 스택','소프트웨어 스택','a']]);
  L.ins('#lI',[lm==='gen'?['r','생성 AI: 가중치와 GPU만으로는 큰 규모에서 빠르고 안정적이지 않아요. 런타임·인프라·도구가 필요해요.']:['g','고전 ML: XGBoost 같은 모델은 가벼운 CPU와 단순한 소프트웨어로도 추론했어요.'],['a','요청이 '+tot.toLocaleString()+'번이면 추론도 '+tot.toLocaleString()+'번. 학습은 그대로 1번이에요.']]);drawL(0);}
$('#lR').addEventListener('input',function(){lr=+this.value;updL();});$('#lD').addEventListener('input',function(){ld=+this.value;updL();});L.bindSeg('#lM',function(v){lm=v;updL();});L.addMod(cL,drawL);updL();
/* ② 기법 카드 */
function tech(k){var t=TECH[k];L.ins('#rI',[['m','<b>'+t[0]+'</b> — '+t[1]],['g','좋아지는 것: '+t[2]],['a','대가·주의: '+t[3]]]);}
L.bindSeg('#rT',tech);tech('batch');
/* ② 추측 디코딩 */
var cS=$('#cSpec'),sa=0.7,sk=4,seed=7,rows=[];
var WORDS=['Look','at','the','tel','le','scope','and','see','the','stars','to','night'];
function simSpec(a,k,total,sd){var r=L.rng(sd),pos=0,passes=0,log=[];while(pos<total){var acc=0;for(var i=0;i<k;i++){if(r()<a)acc++;else break;}passes++;log.push([acc,Math.min(k,acc+1)>acc?1:0]);pos+=acc+1;}return {passes:passes,log:log};}
function drawS(){var W=fit(cS,220),x=cS.getContext('2d');x.clearRect(0,0,W,220);grid(x,W,220);var r=L.rng(seed),y=26;x.font='12px '+F;
  for(var row=0;row<5;row++){var acc=0;for(var i=0;i<sk;i++){if(r()<sa)acc++;else break;}var px=16;x.fillStyle=C.muted;x.textAlign='left';x.fillText('검증 '+(row+1),px,y+14);px+=58;
    for(var i=0;i<sk;i++){var ok=i<acc,w=44;x.fillStyle=ok?'rgba(94,227,156,.25)':'rgba(240,96,77,.18)';x.strokeStyle=ok?C.gfp:C.eye;x.fillRect(px,y,w,20);x.strokeRect(px+.5,y+.5,w-1,20);x.fillStyle=ok?C.gfp:C.eye;x.textAlign='center';x.fillText(WORDS[(row*3+i)%%WORDS.length],px+w/2,y+14);px+=w+4;}
    x.fillStyle='rgba(130,184,255,.25)';x.strokeStyle=C.info;x.fillRect(px+6,y,48,20);x.strokeRect(px+6.5,y+.5,47,20);x.fillStyle=C.info;x.fillText('+1 직접',px+30,y+14);
    x.fillStyle=C.text;x.textAlign='left';x.fillText('→ '+(acc+1)+'토큰',px+62,y+14);y+=38;}stamp(x,W,'시드 고정 설명용');}
function updS(){L.setTxt('#sAV',(+sa).toFixed(2));L.setTxt('#sKV',sk+'개');var e=(1-Math.pow(sa,sk+1))/(1-sa),s=simSpec(sa,sk,60,seed+100);
  L.kpis('#sK2',[[e.toFixed(2),'검증 한 번당 토큰 (기댓값)','g'],[s.passes,'60토큰에 드는 순전파 (시뮬레이션)','m'],['60','보통 디코딩 순전파','r'],[(60/s.passes).toFixed(2)+'×','순전파 절약 배수','a']]);
  L.ins('#sI',[[sa>=0.6?'g':'r',sa>=0.6?'초안이 잘 맞아요: 한 번 검증에 '+e.toFixed(1)+'토큰.':'초안이 자주 틀려요: 이득이 작아요 ('+e.toFixed(1)+'토큰).'],['a','초안을 만드는 비용은 여기서 빼고 셌어요. 5장에서 함께 셉니다.']]);drawS();}
$('#sA').addEventListener('input',function(){sa=+this.value;updS();});$('#sK').addEventListener('input',function(){sk=+this.value;updS();});$('#sGo').addEventListener('click',function(){seed++;updS();});L.addMod(cS,function(dt){if(dt===0)drawS();});updS();
/* ③ 풀 */
var cP=$('#cPool'),pm='silo',ps=0.6,pt=0;
function demand(t){var r=L.rng(31+t),base=[0,0,0],hot=Math.floor(r()*3);for(var i=0;i<3;i++)base[i]=60+r()*30;base[hot]+=ps*90;for(var i=0;i<3;i++)if(i!==hot)base[i]-=ps*35;return base.map(function(v){return Math.max(10,Math.round(v))});}
function poolCalc(){var d=demand(pt),cap=100,served,drop;if(pm==='silo'){served=d.map(function(v){return Math.min(v,cap)});}else{var tot=d.reduce(function(a,b){return a+b},0),s=Math.min(tot,cap*3);served=d.map(function(v){return v/tot*s});}
  drop=d.reduce(function(a,b){return a+b},0)-served.reduce(function(a,b){return a+b},0);return {d:d,served:served,drop:drop,cap:cap};}
function drawP(){var W=fit(cP,230),x=cP.getContext('2d'),r=poolCalc();x.clearRect(0,0,W,230);grid(x,W,230);var bw=Math.min(150,(W-80)/3);
  ['클러스터 A','클러스터 B','클러스터 C'].forEach(function(n,i){var cx=40+i*(bw+20),base=200,sc=1.0;x.strokeStyle=C.info;x.setLineDash([4,3]);x.strokeRect(cx,base-r.cap*sc,bw,r.cap*sc);x.setLineDash([]);
    var sv=r.served[i],ov=r.d[i]-sv;x.fillStyle='rgba(94,227,156,.6)';x.fillRect(cx+6,base-sv*sc,bw-12,sv*sc);if(ov>0.5){x.fillStyle='rgba(240,96,77,.7)';x.fillRect(cx+6,base-sv*sc-ov*sc,bw-12,ov*sc);}
    x.fillStyle=C.text;x.font='12px '+F;x.textAlign='center';x.fillText(n+' · 수요 '+r.d[i],cx+bw/2,218);});
  if(pm==='pool'){x.strokeStyle=C.gfp;x.lineWidth=2;x.beginPath();x.moveTo(40,20);x.lineTo(40+3*(bw+20)-20,20);x.stroke();x.lineWidth=1;x.fillStyle=C.gfp;x.font='12px '+F;x.textAlign='left';x.fillText('하나의 풀로 묶음',44,16);}
  stamp(x,W,'시드 고정 설명용 수요');}
function updP(){var r=poolCalc(),tot=r.d.reduce(function(a,b){return a+b},0);L.setTxt('#pSV',(+ps).toFixed(1));
  L.kpis('#pK',[[tot,'전체 수요','i'],[300,'전체 용량 (100×3)','g'],[Math.round(r.drop),'처리 못 한 요청','r'],[pm==='silo'?'사일로':'풀','방식','a']]);
  L.ins('#pI',[[r.drop>0.5?'r':'g',r.drop>0.5?'넘친 요청 '+Math.round(r.drop)+'개를 버렸어요.':'버린 요청이 없어요.'],['a',pm==='silo'?'"하나의 풀"을 눌러 같은 수요를 비교해 보세요.':'같은 GPU 수로 남는 칸을 썼어요. 그래도 전체 수요가 300을 넘으면 용량을 늘려야 해요.']]);drawP();}
L.bindSeg('#pM',function(v){pm=v;updP();});$('#pS').addEventListener('input',function(){ps=+this.value;updP();});$('#pNext').addEventListener('click',function(){pt++;updP();});L.addMod(cP,function(dt){if(dt===0)drawP();});updP();
/* ④ 추상화 */
var cA=$('#cAbs'),ax=50;function ctl(v){return 100-v*0.9;}function prod(v){return 10+v*0.9;}
function drawA(){var W=fit(cA,200),x=cA.getContext('2d');x.clearRect(0,0,W,200);grid(x,W,200);var L0=30,R=W-30,T=20,B=170;function px(v){return L0+(R-L0)*v/100}function py(v){return B-(B-T)*v/100}
  x.fillStyle='rgba(94,227,156,.08)';x.fillRect(px(35),T,px(65)-px(35),B-T);
  [[ctl,C.stain,'통제력'],[prod,C.gfp,'생산성']].forEach(function(c){x.strokeStyle=c[1];x.lineWidth=2;x.beginPath();for(var v=0;v<=100;v++){var y=py(c[0](v));v?x.lineTo(px(v),y):x.moveTo(px(v),y);}x.stroke();x.lineWidth=1;x.fillStyle=c[1];x.font='12px '+F;x.textAlign='left';x.fillText(c[2],px(c===0?0:2),py(c[0](2))-6);});
  x.strokeStyle=C.text;x.beginPath();x.moveTo(px(ax),T);x.lineTo(px(ax),B);x.stroke();x.fillStyle=C.muted;x.textAlign='left';x.fillText('기본 부품',L0,190);x.textAlign='right';x.fillText('블랙박스',R,190);stamp(x,W,'설명용 곡선');}
function updA(){L.setTxt('#aXV',ax);var c=ctl(ax),p=prod(ax);L.kpis('#aK',[[c.toFixed(0),'통제력 (설명용)','m'],[p.toFixed(0),'생산성 (설명용)','g'],[Math.min(c,p).toFixed(0),'둘 중 작은 값','a']]);
  L.ins('#aI',[[ax<25?'r':ax>75?'r':'g',ax<25?'기본 부품만: 뭐든 되지만 매번 바닥부터 만들어요.':ax>75?'블랙박스: 편하지만 중요한 서비스를 믿고 맡길 통제력이 부족해요.':'가운데 영역: 교재가 말하는 "알맞은 지점"이 있을 만한 곳이에요.']]);drawA();}
$('#aX').addEventListener('input',function(){ax=+this.value;updA();});L.addMod(cA,function(dt){if(dt===0)drawA();});updA();
/* ⑤ 책 지도 */
var CH=%s,cM=$('#cMap'),mc=1;
function drawM(){var W=fit(cM,230),x=cM.getContext('2d');x.clearRect(0,0,W,230);grid(x,W,230);var lay=[['도구',C.gfp,14],['런타임',C.stain,64],['인프라',C.info,150]],cur=CH[mc-1];
  lay.forEach(function(l){var on=(cur[2]==='run'&&l[0]==='런타임')||(cur[2]==='infra'&&l[0]==='인프라');x.globalAlpha=on?1:.35;x.strokeStyle=l[1];x.fillStyle=on?'rgba(255,255,255,.04)':'transparent';x.lineWidth=on?2:1;x.strokeRect(14,l[2],W-28,l[0]==='런타임'?78:(l[0]==='도구'?40:52));x.lineWidth=1;x.fillStyle=l[1];x.font='700 13px '+F;x.textAlign='left';x.fillText(l[0],24,l[2]+20);x.globalAlpha=1;});
  if(cur[2]==='pre'){x.strokeStyle=C.amber;x.setLineDash([5,4]);x.strokeRect(W-170,8,156,30);x.setLineDash([]);x.fillStyle=C.amber;x.font='12px '+F;x.textAlign='center';x.fillText('추론 엔지니어링 이전',W-92,28);}
  x.fillStyle=C.text;x.font='12px '+F;x.textAlign='left';x.fillText(mc+'장 '+cur[1],24,222);}
function updM(v){mc=+v;var c=CH[mc-1];L.ins('#mI',[['g','<b>'+c[0]+'장 '+c[1]+'</b> — '+c[3]],['a',c[2]==='pre'?'층 지도 밖, 시작하기 전의 일':c[2]==='run'?'주로 런타임 층':'주로 인프라(운영) 층']]);drawM();}
L.bindSeg('#mC',updM);L.addMod(cM,function(dt){if(dt===0)drawM();});updM(1);
/* 대결 */
L.Duel({fmt:function(v){return Math.round(v)+'번'},run:function(){var s=simSpec(0.7,4,60,107),f=60,r=s.passes;
  return {fly:f,robo:r,res:r<f?'R':'F',asst:'60토큰에 큰 모델 순전파는 초파리 쪽 '+f+'번, 주판봇 쪽 '+r+'번이에요. 순전파 한 번에 평균 '+(60/r).toFixed(2)+'토큰이 나왔어요.',
  verdict:'초안이 잘 맞으면 한 번에 여러 토큰이 나온다. 주판봇 승.',note:'시드 고정 시뮬레이션(적중률 0.7, 초안 4개). 적중률을 낮추면 차이가 줄어요 — 위 ② 칸에서 직접 확인해 보세요.'};}});
''' % (_j.dumps(TECH, ensure_ascii=False), _j.dumps([list(c) for c in CH], ensure_ascii=False))

def spec():
    return {'meta': {'title': '추론이란 무엇인가 — 『Inference Engineering』 0장 연구실 해설', 'description': '인퍼런스 스터디 북 1주차 교재 · 0장: 학습과 추론, 런타임·인프라·도구 세 층, 책 지도',
                     'series': '인퍼런스 스터디 북', 'number': '01-1', 'slug': 'ch00_inference', 'version': '1.0', 'date': '2026-11-11', 'creator': ['안상선'], 'license': 'CC BY-NC 4.0 (캐릭터 제외)', 'url': URL,
                     'kgStart': 'lab:concept/inference', 'citeKey': 'ahn2026ch00', 'domain': 'ai',
                     'suggestedCitation': '안상선 (2026). 추론이란 무엇인가 — 『Inference Engineering』 0장 연구실 해설. 인퍼런스 스터디 북 1주차. ' + URL},
            'kg': KG, 'refs': [book_ref()], 'gl': GL, 'core': CORE, 'quiz': QUIZ, 'js': JS,
            'nav': nav([('cast', '식구'), ('big', '큰 그림'), ('lv1', '① 두 단계'), ('lv2', '② 런타임'), ('lv3', '③ 인프라'), ('lv4', '④ 도구'), ('lv5', '⑤ 책 지도'), ('duel', '대결'), ('sum', '정리'), ('kg', '색인'), ('export', '꾸러미')]),
            'body': cover('cover_00', '인퍼런스 스터디 북 · 1주차 · 0장', '연구실 식구 여섯이 세 층으로 쌓인 실험 선반 앞에 서 있는 대체 표지',
                          motif='<i class="on"></i><i class="on"></i><i class="on"></i><i class="m"></i><i class="m"></i><i class="m"></i><i class="m"></i><i class="m"></i><i class="m"></i><i class="a"></i><i class="a"></i><i class="a"></i>',
                          moods={'doc': 'think', 'asst': 'smile', 'fly': 'point', 'robo': 'calc', 'sia': 'explain', 'moa': 'smile'})
                    + hero + cast + big + lv1 + lv2 + lv3 + lv4 + lv5 + duel_sec + summary + outro,
            'footer': footer([('교재', 'Kiely, P. (2026). Inference Engineering, Chapter 0 Inference. Baseten Books.'), ('그림 0.1~0.3', '교재 0장 (이 페이지는 다시 그린 도식)'),
                              ('추측 디코딩 기댓값 식', '추측 디코딩 연구에서 흔히 쓰는 단순화 (설명용, 교재 0장에는 없음)')],
                             ['① 칸의 요청 점 개수', '② 칸 추측 디코딩의 적중률과 초안 (시드 고정)', '③ 칸 클러스터 수요 (시드 고정)', '④ 칸 통제력·생산성 곡선', '대결의 순전파 횟수 (시뮬레이션)'],
                             prev=('../week_01_textbook_preface/', '서문'), nxt=('../week_01_textbook_ch01/', '1장 시작 전에 정할 것'))}

if __name__ == '__main__':
    out = os.path.join(sys.argv[1], SLUG, 'index.html')
    print(out, build(spec(), out))
