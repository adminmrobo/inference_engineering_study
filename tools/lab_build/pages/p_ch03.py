# -*- coding: utf-8 -*-
"""4주차 교재 · 3장 하드웨어 (Kiely 2026, Inference Engineering Chapter 3 Hardware 3.1–3.5) — 낮의 연구실(v1.14)."""
import os, sys, json as _j
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import *
from parts import *
from series import BASE
from extras import short_course, teach_appendix, fill_defs

SLUG = 'week_04_textbook_ch03'; P = 'ch03'; URL = BASE + SLUG + '/'
BK = 'kiely2026inference'
LIGHT = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'light.css'), encoding='utf-8').read()

def xask(who, q, a, amood='think', ans='asst'):
    return ('<details class="xask"><summary>방청석 질문 · 미공개 %s</summary>' % who.upper()
            + say(who, 'hint', q, name='방청석 %s' % who.upper()) + say(ans, amood, a) + '</details>')

hero = '''<header class="hero" id="top"><div class="wrap"><div class="hero-text">
<p class="eyebrow">인퍼런스 스터디 북 · 4주차 교재 · 3장 하드웨어 (3.1–3.5)</p>
<h1>GPU 기계실 — 추론 공장의 엔진룸 둘러보기</h1>
<p class="q">같은 모델인데 어떤 GPU에선 빠르고 어떤 GPU에선 아예 안 올라간다. 무엇을 보고 골라야 할까?</p>
<p>추론은 <b>가속기</b>(accelerator) 위에서 돌아갑니다. 테라바이트급 데이터를 싣고 1초에 수조 번 계산하도록 만든 기계죠. 3장은 그 기계를 뜯어 봅니다 — 안에 무엇이 있고(연산 · 메모리), 세대마다 무엇이 바뀌고, 클라우드에서는 어떤 단위로 빌리고, GPU 말고 어떤 선택지가 있고, 내 컴퓨터에서는 어디까지 되는지.</p>
<div class="kpis" id="heroK"></div>
<p class="cite">Kiely, P. (2026). <i>Inference Engineering</i>, Chapter 3 Hardware. Baseten Books. <span class="chip-src">원문</span> 칩은 교재 수치 그대로입니다.</p>
<div class="dialog">''' + say('doc', 'board', '3주차에 "계산이 막혔나, 메모리 통로가 막혔나"를 배웠죠. 오늘은 그 통로와 계산기가 실제로 어떻게 생겼는지 보러 4층 기계실에 갑니다.') \
    + say('asst', 'report', '교재 표의 숫자(H100 · H200 · L4 · L40 · B200 · B300, RTX 5090 · M3 Ultra)는 전부 원문 그대로 계기판에 넣었어요.') \
    + say('fly', 'magnify', 'FLOPS 큰 GPU가 무조건 빠른 거 아냐? 비싼 게 좋은 거지.') \
    + say('robo', 'calc', '난 숫자만 봐. 대역폭이 크면 토큰이 빨리 나와. 그게 돈이야!') \
    + say('sia', 'explain', '교재 순서대로 갑니다. 3.1 구조(연산·메모리) → 3.2 세대 → 3.3 인스턴스 → 3.4 다른 가속기 → 3.5 로컬 추론, 그리고 대결.') \
    + say('moa', 'report', '어려운 영어 이름은 별명 카드에 모아 뒀어요. 먼저 한 번 훑어 주세요!') + '''</div></div></div></header>'''

NICK = [('계산 공방 (SM)', 'Streaming Multiprocessor', 'GPU 안의 작업장. 하나에 여러 개의 코어가 들어 있다'),
        ('행렬 프레스 (텐서 코어)', 'Tensor Core', '행렬·벡터를 통째로 곱하는 코어. 추론 계산의 주력'),
        ('곱하고 더하기 (MMA)', 'Matrix Multiply and Accumulate', 'D = (A × B) + C. 텐서 코어가 하는 기본 동작'),
        ('기계실 창고 (VRAM)', 'Video RAM · HBM', 'GPU에 붙은 큰 메모리. 모델 무게와 KV 캐시가 여기 산다'),
        ('창고 통로 (메모리 대역폭)', 'memory bandwidth', '창고에서 계산 공방으로 1초에 옮길 수 있는 양'),
        ('복도 · 다리 (인터커넥트)', 'NVLink · NVSwitch · InfiniBand', 'GPU끼리, 노드끼리 데이터를 주고받는 길'),
        ('칸막이 GPU (MIG)', 'Multi-Instance GPU', '큰 GPU 하나를 최대 일곱 조각으로 나눠 여럿이 쓰기'),
        ('내 책상 추론 (로컬)', 'local · edge inference', '서버가 아니라 사용자 기기에서 직접 돌리기')]
nick = '<h3>교재 속 용어 별명</h3><div class="nick">' + ''.join('<div class="card"><b>%s</b><div class="orig">%s</div><p style="margin:4px 0 0;font-size:14px">%s</p></div>' % n for n in NICK) + '</div>'
cast = crew({'doc': '해설 · 대결 심판', 'asst': '교재 수치 발표', 'fly': '"메모리가 먼저"를 주장', 'robo': '"대역폭이 곧 속도"를 주장', 'sia': '교재 순서 안내 · 진행 신호', 'moa': '별명 카드 · 기록장',
             'x1': '방청석 질문 담당', 'x2': '방청석 질문 담당', 'x3': '방청석 질문 담당'},
            extra=nick + short_course('3장 핵심만', [('lv2', '2 연산', 'FLOPS는 텐서 코어 · 밀집 · 같은 정밀도로'), ('lv3', '3 메모리', '들어가는가: 무게 + 50% 여유'), ('lv4', '4 어느 숫자를 볼까', '프리필은 FLOPS, 디코드는 대역폭'), ('lv7', '7 인스턴스 · 여러 GPU', 'NVLink vs InfiniBand, 비트와 바이트'), ('duel', '대결', '들어가야 돌린다')]) + '<h3>오늘의 순서</h3>' + route([('lv1', '1', '세 종류 · 세 자리'), ('lv2', '2', '연산'), ('lv3', '3', '메모리 · 캐시'), ('lv4', '4', '어느 숫자를 볼까'),
                                                        ('lv5', '5', 'GPU 세대'), ('lv6', '6', 'Grace · Vera CPU'), ('lv7', '7', '인스턴스 · 여러 GPU'), ('lv8', '8', '칸막이 GPU'),
                                                        ('lv9', '9', '다른 가속기'), ('lv10', '10', '로컬 추론'), ('duel', '대결', '어느 책상이 빠를까')]))

# ---------- 1 ----------
lv1 = level(1, 'lv1', '세 종류의 GPU, 세 가지 자리', [('g', '교재: 3장 도입')],
    pair=('공장에서는', '엔진에도 대형 발전소용 · 작업장용 · 가정용이 있어요. 큰 공장은 발전소용을 빌려 쓰거나(임대), 사서 내 건물에 두거나(자가), 외부와 완전히 끊긴 벙커에 둡니다.',
          'GPU에서는', '<b>데이터센터</b>(예: B200) · <b>워크스테이션</b>(예: RTX Pro 6000) · <b>개인용</b>(예: GeForce RTX 5090). 대규모 추론은 냉장고만 한 랙에 꽂힌 데이터센터 GPU로 하고, 자리는 <b>클라우드 · 온프레미스 · 에어갭</b> 셋 중 하나예요 <span class="chip-src">원문</span>.'),
    panel=panel('어디서 돌릴까 — 조건을 켜 보기', None, '',
                ctrl=btn_group('m1', '트래픽이 빠르게 늘어난다', [('1', '그렇다'), ('0', '아니다')]) + btn_group('m2', '데이터센터를 직접 통제해야 한다', [('0', '아니다'), ('1', '그렇다')])
                     + btn_group('m3', '사람이 직접 가서 만져야만 돌린다 (외부망 차단)', [('0', '아니다'), ('1', '그렇다')]), kp_id='mK', ins_id='mI'),
    explain=explain('풀이', ['데이터센터 GPU가 대규모 추론의 표준인 이유: 한 장 성능이 가장 높고, 무엇보다 <b>GPU끼리 잇는 고대역 연결</b>이 있고, 구성이 표준화돼 있고, 전 세계에 수백만 장이 깔려 있어서예요.',
                             '대부분의 추론 엔지니어는 <b>클라우드 GPU</b>를 씁니다. 하이퍼스케일러(AWS, GCP)나 네오클라우드(Coreweave, Nebius)에서 빌리죠.',
                             '대기업·정부는 온프레미스나 에어갭을 쓰지만, 빠르게 크는 AI 제품에는 클라우드의 유연성이 맞아요.'],
                    limit='위 판단표와 "증설에 걸리는 시간"은 교재의 세 정의를 단순한 조건으로 옮긴 설명용 감이에요(교재에 없는 수치). 실제 결정에는 비용 · 보안 규정 · 조달 기간이 함께 들어갑니다.'),
    talk=say('fly', 'arms', '책상 밑에 B200 있는 사람? …없지. 그래서 다들 빌려 쓰는 거구나.') + xask('x1', '워크스테이션 GPU랑 개인용 GPU는 뭐가 달라요?', '교재 기준으로는 쓰임새예요. 워크스테이션은 전문 작업용 데스크톱 GPU(RTX Pro 6000), 개인용은 일상용 데스크톱 GPU(RTX 5090). 둘 다 "한 장짜리"라는 점이 데이터센터 GPU와 달라요.'))

# ---------- 2 ----------
lv2 = level(2, 'lv2', '연산 — 계산 공방(SM)과 행렬 프레스(텐서 코어)', [('g', '교재: 3.1.1 Compute'), ('p', '그림 3.1')],
    pair=('공장에서는', 'CPU는 복잡한 일을 순서대로 척척 해내는 장인 몇 명, GPU는 같은 동작을 수천 개 재료에 한꺼번에 하는 프레스 수천 대예요.',
          'GPU에서는', 'GPU 안에는 <b>SM</b>(계산 공방)이 여럿, SM마다 코어가 여럿. 코어는 세 종류 — <b>CUDA 코어</b>(숫자 하나), <b>텐서 코어</b>(행렬·벡터), <b>SFU</b>(sin · cos · log). 추론 계산력은 <b>텐서 코어 기준</b>으로 잽니다 <span class="chip-src">원문</span>.'),
    extra_top='<div class="panel"><h3>그림 3.1 다시 그리기 · 곱하고 더하기 (MMA)</h3><p class="muted" style="margin:0">텐서 코어가 하는 일은 D = (A × B) + C. "더하기(accumulate)"는 곱한 결과를 바탕 행렬 C에 얹는 것이에요. 단추를 누르면 D의 칸이 하나씩 채워집니다.</p>'
              '<div class="mmrow" id="mmRow"></div><div class="ctrl"><button class="bt primary" id="mmNext">다음 칸 계산</button><button class="bt" id="mmNew">새 숫자</button></div><div class="insight" id="mmI" aria-live="polite"></div></div>',
    panel=panel('계산력 계기판 — 정밀도와 희소성을 바꿔 보기', 'cFlops', 'GPU별 텐서 코어 계산력 막대 그래프. FP8 밀집 값은 교재 표, 나머지는 교재 규칙으로 계산.',
                ctrl=btn_group('fP', '정밀도', [('8', 'FP8'), ('16', 'FP16'), ('4', 'FP4')]) + btn_group('fS', '희소성 (2:4)', [('0', '밀집 (기본)'), ('1', '희소')]), kp_id='fK', ins_id='fI', wide=True),
    explain=explain('풀이', ['스레드는 CPU와 GPU에서 뜻이 비슷해요. CPU는 수십~수백 개, GPU는 <b>수만~수십만 개</b>가 한 클럭에 일을 바꿔 가며 단순한 명령을 동시에 실행합니다.',
                             '계산력 단위는 <b>FLOPS</b>(1초에 하는 부동소수점 연산 수). 데이터센터 GPU는 테라(10<sup>12</sup>)~페타(10<sup>15</sup>) FLOPS.',
                             '사양표에는 <b>밀집</b>과 <b>희소</b> 두 값이 있어요. 희소 값은 0이 절반인 2:4 구조에서 0 곱하기를 건너뛴 값이라 보통 두 배(항상은 아님). <b>추론은 기본이 밀집</b>이니 밀집 값을 보세요.',
                             '정밀도를 반으로 줄이면 FLOPS는 대체로 두 배. 그래서 GPU를 비교할 땐 <b>같은 정밀도끼리</b> 비교해야 해요.',
                             '계산력이 병목인 일: <b>LLM 프리필</b>, <b>이미지·영상 생성</b>. 이런 일이 주력이면 FLOPS 큰 가속기를 고릅니다.'],
                    limit='FP16·FP4·희소 막대는 교재 규칙(정밀도 반 → 2배, 희소 → 보통 2배)으로 계산한 값이라 실제 사양표와 조금 다를 수 있어요. FP4는 블랙웰부터라 호퍼·러브레이스 칸은 "지원 안 함"으로 둡니다.'),
    talk=say('robo', 'chart', 'FP16에서 FP8로 바꾸면 막대가 두 배! …근데 교재가 5.1절에서 "그대로 두 배 성능은 아니다"라고 했지.') + xask('x2', '희소 값이 두 배 크면 그걸 보면 안 돼요?', '추론은 기본이 밀집이에요. 모델 무게의 절반이 정확히 0인 2:4 구조일 때만 희소 값이 나오니까, 평소엔 밀집 값으로 비교해야 속지 않아요.'))

# ---------- 3 ----------
SMS = ''.join('<div class="sm" data-sm="%d" tabindex="0" role="button" aria-label="SM %d">SM%d<i></i><i></i><i></i><i></i><u>L1</u></div>' % (i, i + 1, i + 1) for i in range(8))
lv3 = level(3, 'lv3', '메모리와 캐시 — 큰 창고와 작은 선반', [('g', '교재: 3.1.2 Memory and Caches'), ('p', '그림 3.2')],
    pair=('공장에서는', '기계실 바깥에 커다란 창고(VRAM)가 있고, 공방마다 손 닿는 선반(L1), 공방들이 함께 쓰는 중간 선반(L2)이 있어요. 창고는 크지만 멀고, 선반은 작지만 가까워요.',
          'GPU에서는', 'VRAM은 <b>DRAM</b>(칩 밖, 기가바이트 단위)이고 HBM3 · HBM3e · HBM4로 붙어 있어요. 캐시는 <b>SRAM</b>(칩 안, 킬로~메가바이트, 더 빠르고 비쌈). H100: SM마다 L1 <b>256 KB</b>, 칩 전체 L2 <b>50 MB</b> <span class="chip-src">원문</span>.'),
    extra_top='<div class="panel"><h3>그림 3.2 다시 그리기 — SM을 눌러 보세요</h3><div class="smgrid" id="smGrid">' + SMS + '</div><div class="l2bar">L2 캐시 — 모든 SM이 함께 씀 (H100 50 MB)</div><div class="vram">VRAM (HBM) — 칩 밖의 큰 창고 · 수십~수백 GB · 대역폭 = 이 창고에서 캐시로 데이터를 실어 오는 속도</div>'
              '<div class="insight" id="smI" aria-live="polite"></div><p class="muted" style="font-size:13px;margin:6px 0 0">보라 칸 = 텐서 코어(TC), 파란 칸 = SM 안의 L1(공유 메모리). L0는 텐서 코어 하나의 명령 캐시라 그림에선 생략했어요.</p></div>',
    panel=panel('모델이 들어갈까? — VRAM 계산기', 'cFit', '모델 무게와 KV 캐시 여유분(무게의 50%)을 GPU 메모리 용량과 비교하는 막대.',
                ctrl=slider('vP', '모델 크기', 1, 700, 1, 70, 'B') + btn_group('vB', '숫자 하나의 크기', [('2', '16비트 (2바이트)'), ('1', '8비트 (1바이트)'), ('0.5', '4비트 (0.5바이트)')])
                     + btn_group('vG', 'GPU', [('L4', 'L4'), ('L40', 'L40'), ('H100', 'H100'), ('H200', 'H200'), ('B200', 'B200'), ('B300', 'B300')], 2) + btn_group('vN', '몇 장', [('1', '1'), ('2', '2'), ('4', '4'), ('8', '8 (노드 하나)')]), kp_id='vK', ins_id='vI', wide=True),
    explain=explain('풀이', ['VRAM 총량이 올릴 수 있는 모델 크기를 정해요. 교재의 경험칙: <b>모델 무게 + 최소 50% 여유</b>(KV 캐시용). 긴 문맥 · 큰 배치 · 영상 생성 모델은 더 많이.',
                             '무게도 안 들어가면 모델을 올리다 <b>OOM</b>(메모리 부족)으로 실패. 여유가 모자라면 추론이 느려지거나 OOM으로 죽어요.',
                             '모델 무게 ≈ 파라미터 수 × 숫자 하나의 바이트. 70B × 2바이트 = 140 GB → H100 한 장(80 GB)에는 안 들어가요.',
                             '<b>메모리 대역폭</b>은 낮~중간 배치 <b>LLM 디코드</b>의 병목이에요. 토큰을 더 빨리 뽑고 싶다면 대역폭 큰 가속기(H100 대신 H200)를 고릅니다.'],
                    limit='무게 계산은 파라미터 × 바이트만 셌어요. 실제로는 활성값 · 엔진 작업 공간 · 여러 장으로 나눌 때의 중복이 더 들어갑니다. 여러 장 합산은 7칸(NVLink)처럼 잘 이어져 있을 때 이야기예요.'),
    bridge=bridge(gen=('챗봇 서비스로 치면 VRAM은 "모델 + 지금 대화 중인 모든 손님의 대화 기록(KV 캐시)"을 담는 그릇이에요. 손님이 늘수록 여유분이 빨리 줄어요.', 'KV 캐시 크기는 문맥 길이 · 배치 · 모델 구조에 따라 크게 달라요.'),
                  field=('공장 창고 계획과 같아요. 기계(무게)만 들어간다고 끝이 아니라, 하루 작업 재료(KV 캐시)를 쌓을 자리가 있어야 라인이 돌아요.', '창고는 넓힐 수 있지만 GPU 메모리는 장을 늘려야만 늘어요.')),
    talk=say('moa', 'think', '70B를 16비트로 올리려면 무게만 140 GB, 여유까지 210 GB… H100으론 세 장 이상이네요. 기록해 둘게요.'))

# ---------- 4 ----------
lv4 = level(4, 'lv4', '어느 숫자를 볼까 — 프리필은 FLOPS, 디코드는 대역폭', [('g', '교재: 3.1.1 · 3.1.2 결론'), ('p', '3주차 2.4절 복습')],
    pair=('공장에서는', '주문서 한 장을 통째로 읽어 들이는 일(프리필)은 프레스 힘이, 제품을 하나씩 찍어 내보내는 일(디코드)은 창고에서 재료를 실어 오는 속도가 좌우해요.',
          'GPU에서는', '교재: <b>계산력</b>은 LLM 프리필 · 이미지·영상 생성의 병목, <b>메모리 대역폭</b>은 낮~중간 배치 LLM 디코드의 병목. H100과 H200은 FP8 계산력이 같지만(1,979 TF) 대역폭은 3.35 → 4.8 TB/s <span class="chip-src">원문</span>.'),
    panel=panel('두 일의 속도 상한 비교 (설명용 근사)', 'cBn', '네 GPU의 디코드 토큰 속도 상한과 프리필 시간 하한 막대.',
                ctrl=btn_group('bM', '모델 (FP8 무게)', [('8', '8B'), ('70', '70B'), ('120', '120B')], 1) + slider('bT', '입력 길이', 1000, 32000, 1000, 8000, '토큰')
                     + btn_group('bV', '보기', [('dec', '디코드: 초당 토큰 상한'), ('pre', '프리필: 걸리는 시간 하한')]) + btn_group('bQ', '디코드 배치', [('1', '1'), ('8', '8'), ('32', '32'), ('64', '64')]) + '<div class="group"><label class="glabel" for="bPr">GPU 한 장 시간당 임대료 (직접 입력, 달러)</label><input type="number" id="bPr" min="0" step="0.1" placeholder="예: 제공사 견적" style="width:130px;padding:4px 8px;border:1px solid var(--rule);border-radius:8px"></div>', kp_id='bK', ins_id='bI', wide=True),
    explain=explain('풀이', ['배치 1 디코드: 토큰 하나를 만들 때마다 모델 무게를 창고에서 한 번 다 읽어야 해요. 그래서 <b>초당 토큰 상한 ≈ 대역폭 ÷ 무게 바이트</b>.',
                             '프리필: 입력 토큰 N개를 한꺼번에 계산해요. 토큰 하나에 파라미터마다 곱하기·더하기 2번이라 <b>계산량 ≈ 2 × 파라미터 × N</b>, 시간 하한 ≈ 계산량 ÷ FLOPS.',
                             '그래서 H100 → H200: 디코드 상한은 약 <b>1.43배</b>(4.8 ÷ 3.35), 프리필 하한은 <b>그대로</b>(계산력이 같으니까).',
                             '이 두 줄을 그래프 하나로 그린 것이 이번 주 논문 <b>루프라인 모델</b>이에요.'],
                    limit='효율 100%, KV 캐시 읽기 · 어텐션 · 통신은 무시한 상한 근사예요. 배치 B의 디코드 상한은 min(대역폭 × B ÷ 무게, FLOPS ÷ 2 × 파라미터)로 셌어요. 임대료는 교재에 없어 직접 넣게 했어요. 실제 속도는 이보다 낮고, 배치를 키우면 디코드도 계산 쪽으로 넘어갑니다(논문편 실험실).'),
    talk=say('fly', 'point', '어? H200이 계산력은 H100이랑 똑같네. 근데 토큰은 더 빨리 나온다고?') + say('robo', 'happy', '그러니까! 디코드는 대역폭 장사라니까.'))

# ---------- 5 ----------
lv5 = level(5, 'lv5', 'GPU 세대 — 이름 읽는 법과 세대별 특징', [('g', '교재: 3.2–3.2.4'), ('p', '그림 3.1(세대 연표)')],
    pair=('공장에서는', '엔진 모델명이 "세대 글자 + 크기 숫자"로 돼 있다면, 글자는 설계가 바뀐 세대를, 숫자는 같은 세대 안의 크기를 말해요.',
          'GPU에서는', '<b>글자 = 아키텍처 세대</b>(H = 호퍼, B = 블랙웰), <b>숫자 = 세대 안의 모델</b>. 숫자가 클수록 대체로 크고 비싸요. H100은 A100을 대체하고, H200은 같은 세대의 더 큰 GPU이며 B200이 그 뒤를 잇습니다 <span class="chip-src">원문</span>.'),
    extra_top=panel('세대 연표 — 아키텍처를 눌러 보기', 'cGen', '2017년 볼타부터 2028년 파인만까지 NVIDIA GPU 아키텍처 연표. 누르면 아래에 특징이 나옵니다.',
                    ctrl=btn_group('gA', '아키텍처', [('volta', '볼타'), ('turing', '튜링'), ('ampere', '암페어'), ('hopper', '호퍼'), ('lovelace', '러브레이스'), ('blackwell', '블랙웰'), ('rubin', '루빈'), ('feynman', '파인만')], 3), ins_id='gI', wide=True),
    panel=panel('세대별 사양 비교 (교재 표 그대로)', 'cSpec', '여섯 GPU의 FP8 계산력 · 메모리 · 대역폭 막대.',
                ctrl=btn_group('sM', '비교할 숫자', [('fp8', 'FP8 계산력 (밀집)'), ('mem', '메모리 용량'), ('bw', '메모리 대역폭')]), kp_id='sK', ins_id='sI', wide=True),
    explain=explain('풀이', ['설계 확정부터 출하까지 몇 년이 걸려요. 그래서 다음 세대도 지금과 전혀 다른 AI를 상상하며 설계된 것 — 수명 동안 쓰임새가 어떻게 바뀔지 내다봐야 해요. 학습이 주 용도였다가 이제 <b>추론이 주 용도</b>로 올라서며 최신 세대는 추론용 기능을 넣고 있어요.',
                             '추론 엔지니어는 보통 최근 <b>3~5세대</b> 안에서 일해요. 튜링(T4) · 암페어(A10, A100)는 저트래픽 · 레거시에서 가끔, 대부분은 러브레이스(L4, L40) · 호퍼(H100, H200) · 블랙웰(B200, B300).',
                             '<b>호퍼</b>(2022.3, H100): FP8 도입(FP16보다 텐서 코어 2배, 대역폭은 절반만 씀), 4세대 텐서 코어, 비동기 데이터 전송 → FlashAttention 3. 성능과 생태계가 균형 잡혀 가장 널리 쓰여요.',
                             '<b>러브레이스</b>(호퍼 6개월 뒤): 그래픽 쪽, FP8 지원. 하지만 <b>NVLink가 없어</b> 여러 장 묶기가 비효율. L4는 작은 모델(임베딩 · 비전)에 싸고 편하지만, L40은 추론에 대체로 좋은 선택이 아니에요(같은 메모리면 H100 MIG 조각이 더 빠름).',
                             '<b>블랙웰</b>(2024.11, B200 → B300): FP4와 마이크로스케일링 형식(MXFP8 · MXFP4 · NVFP4), 더 깊은 비동기 → FlashAttention 4. LLM과 영상 생성의 새 표준.',
                             '<b>루빈</b>(2026 예정): HBM4로 디코드 같은 대역폭 일에 이득, 프리필 같은 계산 일 전용 칩 <b>CPX</b>. <b>파인만</b>은 2028. 새 세대는 실제 벤치마크가 나올 때까지 판단을 미루세요 — 소프트웨어가 따라오는 데 1년쯤 걸려요.'],
                    limit='블랙웰 계산력은 교재 표기대로 "약 5 페타FLOPS", 대역폭은 "최대 8 TB/s"예요. 루빈 · 파인만 수치는 교재 출간 시점에 발표되지 않아 비워 뒀어요. 교재에서 세대 연표 그림 번호가 "그림 3.1"로 한 번 더 나오는데, 여기서는 "세대 연표"로 부릅니다.'),
    talk=say('asst', 'report', 'H200은 H100과 계산력이 같고(1,979 TF) 메모리 80 → 141 GB, 대역폭 3.35 → 4.8 TB/s. B200은 약 5 PF · 192 GB · 최대 8 TB/s예요.') + xask('x3', 'NVIDIA는 왜 과학자 이름을 붙여요?', '1998년부터 저명한 과학자 이름을 붙여 왔대요. 호퍼는 그레이스 호퍼 제독, 러브레이스는 최초의 프로그래머 에이다 러브레이스, 블랙웰은 수학자 데이비드 블랙웰, 루빈은 천문학자 베라 루빈이에요.', 'spark'))

# ---------- 6 ----------
lv6 = level(6, 'lv6', 'Grace · Vera CPU — GPU 옆 CPU와 이어진 넓은 다리', [('g', '교재: 3.2.5'), ('p', '그림 3.3')],
    pair=('공장에서는', '기계실 옆 대형 창고(CPU 메모리)가 훨씬 넓지만, 잇는 문이 좁으면 짐을 꺼내 오는 데 오래 걸려요. 문을 넓히면 그 창고를 보조 창고로 쓸 수 있죠.',
          'GPU에서는', 'NVIDIA의 ARM 기반 CPU <b>Grace</b>는 GH200 · GB200 같은 슈퍼칩으로 GPU와 붙어요. 핵심은 <b>NVLink-C2C</b>로 CPU ↔ GPU 메모리 사이 <b>최대 900 GB/s 양방향</b> — PCIe 같은 표준 연결보다 몇 배 빠름 <span class="chip-src">원문</span>.'),
    panel=panel('KV 캐시 꺼내 오기 — 문 넓이 비교', 'cC2C', '같은 크기의 데이터를 PCIe와 NVLink-C2C로 옮길 때 걸리는 시간 막대.',
                ctrl=slider('cS', '옮길 데이터 (KV 캐시 · LoRA 무게)', 1, 200, 1, 40, 'GB'), kp_id='cK', ins_id='cI'),
    explain=explain('풀이', ['어떤 추론 구성은 LoRA 미세조정 무게나 이전 호출의 KV 캐시를 GPU보다 훨씬 큰 <b>CPU 메모리로 내려 두었다가</b> 다시 꺼내 써요.',
                             'Grace CPU라면 그 꺼내 오기가 훨씬 빨라요. 루빈 세대에서는 Grace 자리를 <b>Vera</b> CPU가 이어받습니다.'],
                    limit='PCIe 막대는 교재 밖 참고값(PCIe 5.0 x16 양방향 약 128 GB/s)으로 그린 설명용이에요. 교재는 "몇 배 빠르다"고만 적었어요. 실제 전송은 두 방향 동시 사용 여부 · 효율에 따라 달라요.'),
    talk=say('sia', 'guide', '이 연결은 7주차(5.3 캐싱)에서 KV 캐시를 어디에 둘지 고를 때 다시 나와요. 표시해 두세요.'))

# ---------- 7 ----------
INST = [('GPU (디바이스)', '추론 작업을 하는 GPU 한 장 이상'), ('CPU (호스트)', 'GPU에서 안 도는 나머지 일'), ('호스트 메모리', 'CPU용 일반 RAM'), ('저장소', '큰 파일을 읽고 쓰는 디스크'), ('네트워크', '데이터센터와 인터넷으로 나가는 연결'), ('인터커넥트', 'GPU ↔ GPU, 노드 ↔ 노드 연결')]
lv7 = level(7, 'lv7', '인스턴스와 여러 GPU — 빌려 쓰는 단위, 잇는 길', [('g', '교재: 3.3 · 3.3.1'), ('p', '그림 3.4')],
    pair=('공장에서는', '공장을 빌릴 땐 엔진만이 아니라 전기 · 창고 · 도로 · 옆 건물로 가는 다리까지 같이 빌려요. 어느 하나라도 좁으면 거기서 막혀요.',
          'GPU에서는', '클라우드에서 GPU를 받는 최소 단위는 <b>인스턴스</b>(가상 머신). 여러 GPU가 필요하면 <b>노드</b>(GPU 8장) 안에서는 <b>NVLink</b>(블랙웰 1,800 GB/s · 호퍼 900 GB/s) + <b>NVSwitch</b>(전원 연결), 노드끼리는 <b>InfiniBand</b>(NIC당 최대 400 Gb/s) <span class="chip-src">원문</span>.'),
    extra_top='<div class="panel"><h3>인스턴스에 들어 있는 여섯 가지</h3><div class="cards">' + ''.join('<div class="card"><h4>%s</h4><p>%s</p></div>' % c for c in INST) + '</div>'
              '<p class="muted" style="font-size:14px;margin:6px 0 0">같은 GPU라도 제공사마다 구성이 달라요. 예: A100은 PCIe형과 SXM형이 있는데, 추론은 메모리 대역폭이 <b>5% 높은 SXM</b>형에서 주로 돌아요 <span class="chip-src">원문</span>.</p></div>',
    panel=panel('길마다 걸리는 시간 — 노드 안 vs 노드 사이', 'cNet', '두 노드(각 GPU 8장) 그림과 연결 종류별 전송 시간 막대(로그 눈금).',
                ctrl=slider('nS', '주고받을 데이터', 0.1, 100, 0.1, 10, 'GB') + btn_group('nL', '길', [('nvb', 'NVLink (블랙웰)'), ('nvh', 'NVLink (호퍼)'), ('ib', 'InfiniBand'), ('eth', '이더넷')]), kp_id='nK', ins_id='nI', wide=True),
    explain=explain('풀이', ['모델이 한 장에 안 들어가거나 더 빠르게 하고 싶으면 2 · 4 · 8장 이상을 묶어요(DeepSeek 같은 큰 모델, 영상 생성).',
                             '<b>단위 주의</b>: NVLink는 GB/s(바이트), InfiniBand · 이더넷은 Gb/s(비트). 400 Gb/s = <b>50 GB/s</b>. 이더넷은 NIC당 최대 100 Gb/s.',
                             'NVLink가 InfiniBand보다 한 자릿수 이상 빠르니, 많이 주고받는 일은 노드 안에 두는 게 유리해요. 5.4 병렬화 · 5.5 분리가 이 지형을 따라 설계돼요.',
                             '8장을 넘어 NVLink로 묶는 랙 시스템도 있어요: <b>GB200 NVL72</b>(블랙웰 72장 + Grace 36개, 랙 하나), 다음은 <b>Vera Rubin NVL144 CPX</b>.',
                             '모든 클라우드가 InfiniBand를 주는 건 아니에요. 받을 때 연결 종류와 대역폭을 꼭 확인하세요.'],
                    limit='시간 = 크기 ÷ 대역폭만 셌어요(지연시간 · 프로토콜 오버헤드 · 여러 NIC 묶기는 뺌). 실제 노드 하나엔 NIC가 여러 개 달려 있기도 해요.'),
    talk=say('robo', 'wow', '400이라고 해서 NVLink 900의 절반쯤인 줄 알았는데… 비트였어! 바이트로 바꾸면 50이네.') + xask('x1', 'NVSwitch는 NVLink랑 뭐가 달라요?', 'NVLink는 GPU 둘을 잇는 1:1 길이고, NVSwitch는 그 위에서 노드 안 모든 GPU가 서로 한꺼번에 이야기하게 해 주는 교차로예요.'))

# ---------- 8 ----------
lv8 = level(8, 'lv8', '칸막이 GPU (MIG) — 너무 큰 GPU를 나눠 쓰기', [('g', '교재: 3.3.2'), ('p', '그림 3.5')],
    pair=('공장에서는', '작은 부품 하나 찍자고 초대형 프레스를 통째로 쓰면 낭비예요. 칸막이를 쳐서 여러 작업이 나눠 쓰게 하죠.',
          'GPU에서는', 'A100 · H100 · H200 · B200은 하드웨어 수준에서 최대 <b>7조각</b>으로 나눌 수 있어요. H100은 메모리 조각 <b>8개(각 10 GB)</b> · 계산 조각 <b>7개</b>. 3조각 MIG는 계산 약 3/7, VRAM 최대 절반(40 GB), CPU · RAM · 저장소 · 네트워크도 약 절반 <span class="chip-src">원문</span>.'),
    panel=panel('H100 칸막이 실험', 'cMig', 'H100의 메모리 8조각과 계산 7조각 중 선택한 MIG 크기만큼 칠한 그림.',
                ctrl=btn_group('gZ', 'MIG 크기 (계산 조각)', [('1', '1조각'), ('2', '2조각'), ('3', '3조각'), ('4', '4조각'), ('7', '7조각 (통째)')], 2) + slider('gM', '올릴 모델 크기', 1, 40, 1, 3, 'B') + btn_group('gB', '숫자 크기', [('2', '16비트'), ('1', '8비트')]), kp_id='gK', ins_id='gI2', wide=True),
    explain=explain('풀이', ['수십억 파라미터 이하의 작은 모델은 H100 · B200 같은 큰 GPU를 다 못 써요. 배치를 키워도 자원이 남죠. 그렇다고 옛 GPU로 내려가지 말고 <b>새 GPU의 조각</b>에서 돌리는 방법이 MIG예요.',
                             '왜 하필 7? 계산 조각은 SM으로 만드는데 SM 수가 2의 배수로 딱 떨어지지 않아요. SXM H100은 SM <b>132개</b> → 같은 크기 7조각을 만들고 남는 SM은 쉬어요(132 ÷ 7 = 18.86…).',
                             '예: 3B 파라미터 음성 합성 모델 <b>Orpheus TTS</b>는 GPU 한 장을 통째로 주는 것보다 MIG 인스턴스 두 개로 돌리는 편이 자원을 더 잘 쓸 때가 있어요.'],
                    limit='조각별 메모리(1조각 10 GB, 2조각 20 GB, 3·4조각 40 GB, 통째 80 GB)와 "몇 개 띄울 수 있나"는 NVIDIA MIG 프로필 표(교재 밖)를 따랐어요. 교재는 3조각 예만 들었습니다. 계산 비율은 조각 수 ÷ 7로 근사.'),
    talk=say('fly', 'coffee', '큰 GPU를 쪼개 쓰는 게 작은 옛 GPU 통째보다 낫다… L40 칸에서 들은 이야기랑 이어지네.'))

# ---------- 9 ----------
ACC = [('AMD', '상장사', 'MI350 GPU', '자체 소프트웨어 스택 위에서 경쟁력 있는 사양의 데이터센터 GPU', 'etc'),
       ('AWS', '상장사', 'Inferentia · Trainium', '추론용 · 학습용으로 따로 만든 AWS 전용 칩 한 쌍', 'plat'),
       ('Cerebras', '스타트업', 'WSE-3', '웨이퍼 한 장 크기 칩. 메모리 대역폭이 극히 높아 디코드 병목을 없앰', 'bw'),
       ('Etched', '스타트업', 'Sohu', '트랜스포머 구조 전용 ASIC', 'etc'),
       ('Furiosa', '스타트업', 'RNGD', '텐서 축약 연산용 전력 효율 가속기', 'pw'),
       ('Google', '상장사', 'TPU', '추론 · 학습용 AI 전용 ASIC (텐서 처리 장치)', 'plat'),
       ('Groq', '스타트업', 'LPU', 'SRAM에 기대 높은 메모리 대역폭을 내는 언어 처리 장치', 'bw'),
       ('Qualcomm', '상장사', 'Cloud AI 100 Ultra', '전력 효율 좋은 모바일 GPU 여러 개를 묶은 풀사이즈 카드', 'pw'),
       ('Sambanova', '스타트업', 'RDU', '조 단위 파라미터 모델을 위한 큰 메모리의 재구성형 데이터 흐름 장치', 'etc')]
accs = '<div class="acc" id="accGrid">' + ''.join('<div class="card" data-e="%s"><b>%s</b> <span class="st">%s</span><p style="margin:4px 0;font-weight:700">%s</p><p style="margin:0;font-size:14px">%s</p></div>' % (a[4], a[0], a[1], a[2], a[3]) for a in ACC) + '</div>'
lv9 = level(9, 'lv9', '다른 데이터센터 가속기 — 저마다의 한 수', [('g', '교재: 3.4'), ('p', '가속기 표')],
    pair=('공장에서는', '범용 엔진(GPU) 시장 1위를 이기려는 회사들은 "우리는 이 한 가지만큼은 낫다"는 특기를 걸어요.',
          'GPU에서는', 'GPU는 꽤 범용이에요. 도전자들의 특기는 셋 — <b>메모리 대역폭</b>(Cerebras · Groq: 디코드 가속) · <b>전력 효율</b>(Furiosa · Qualcomm: 운영비) · <b>플랫폼 통합</b>(Amazon · Google: 자기 클라우드와 자체 모델) <span class="chip-src">원문</span>.'),
    panel=panel('특기로 걸러 보기', None, '', ctrl=btn_group('aE', '특기', [('all', '전체'), ('bw', '메모리 대역폭'), ('pw', '전력 효율'), ('plat', '플랫폼 통합'), ('etc', '교재가 특기로 묶지 않은 곳')]), kp_id='aK', ins_id='aI',
                act=accs),
    explain=explain('풀이', ['공통 과제 셋: <b>소프트웨어</b>(CUDA 없이 추론 스택 전체를 새로 지어야 함) · <b>제조</b>(인류가 만든 가장 복잡한 물건을 조립) · <b>유통</b>(만든 칩을 설치하고 켜서 시장에 용량을 내놓기).',
                             '경쟁은 혁신을 빠르게 해요. 데이터센터 선택지가 많을수록 추론 엔지니어에게 좋고, 추론의 가치가 커질수록 경쟁도 · 로컬 추론 탐색도 더 활발해져요.'],
                    limit='표의 한 줄 설명은 교재 표를 옮긴 것이고 성능 비교는 하지 않았어요. AMD · Etched · Sambanova는 교재가 세 특기 중 어디에도 묶지 않아 "기타"로 뒀어요.'),
    talk=say('moa', 'report', '기록장: 이 책은 NVIDIA GPU 최적화가 중심이지만, "왜 다른 칩을 쓰나"는 특기 세 가지로 기억하면 돼요.'))

# ---------- 10 ----------
lv10 = level(10, 'lv10', '로컬 추론 — 내 책상과 내 손 안에서', [('g', '교재: 3.5–3.5.2'), ('p', 'RTX 5090 vs M3 Ultra 표')],
    pair=('공장에서는', '본사 공장 대신 손님 집에 작은 기계를 두면 배송(네트워크)이 없고 손님 정보가 밖으로 안 나가요. 대신 기계가 작고, 열이 나고, 손님마다 기계가 제각각이에요.',
          'GPU에서는', '장점 넷: <b>네트워크 지연 0</b>(수십~수백 ms 절약) · <b>독립성</b> · <b>개인정보 보호</b> · <b>개발자 비용 0</b>. 약점 넷: <b>하드웨어 성능</b> · <b>발열</b> · <b>조합이 제각각</b> · <b>배터리</b> <span class="chip-src">원문</span>.'),
    panel=panel('내 책상에 올려 보기 — RTX 5090 vs M3 Ultra', 'cLoc', '두 데스크톱의 메모리 용량 대비 모델 크기와 디코드 토큰 속도 상한 막대.',
                ctrl=slider('lP', '모델 전체 크기', 1, 400, 1, 32, 'B') + btn_group('lB', '양자화', [('0.5', '4비트'), ('1', '8비트'), ('2', '16비트')]) + btn_group('lE', '구조', [('1', '밀집'), ('0.1', 'MoE (활성 10%)')]), kp_id='lK', ins_id='lI', wide=True),
    explain=explain('풀이', ['데스크톱: 고급 소비자 GPU 한두 장 달린 PC도 있지만, 데스크톱 추론의 선두는 점점 <b>Apple</b>이에요. M 시리즈는 CPU와 GPU가 <b>통합 메모리</b> 하나를 같이 써서, GPU가 훨씬 큰 메모리에 접근해요(대신 느림).',
                             '교재 표: RTX 5090 <b>32 GB · 1,792 GB/s · 컴퓨터 $5,000</b> vs M3 Ultra <b>512 GB · 819 GB/s · $10,000</b>. 용량과 속도의 맞바꿈이 중급 가격대까지 이어져요. 크롬북 같은 저가 기기는 의미 있는 로컬 추론이 어려워요.',
                             'Ollama · llama.cpp로 100B+ 모델을 강하게 양자화해 고급 개인 하드웨어에서 돌릴 수 있어요. <b>MoE</b>는 요청 하나가 전체 무게의 일부만 건드려 데스크톱에 유리해요. 이미지 생성은 ComfyUI, 브라우저는 WebLLM.',
                             '모바일: 온디바이스 작업의 대부분. Android는 AI Edge SDK · ML Kit GenAI(Gemini Nano, Gemma), iOS는 Foundation Models · Core ML. 고급 폰도 <b>1~2B 파라미터</b>를 넘으면 버거워요. 받아쓰기 · 음성 합성 · 번역처럼 작은 모델로 되는 일이 잘 맞아요.',
                             '결론: 로컬이냐 클라우드냐가 아니라 <b>둘 다</b>. 작은 모델 · 빠른 질의는 기기에서, 무거운 일은 데이터센터에서.'],
                    limit='토큰 속도 상한 = 대역폭 ÷ (한 토큰에 읽는 무게)로 계산한 설명용이에요. MoE는 전체 무게가 메모리에 다 있어야 하지만 토큰당 읽는 양은 활성 부분만이라고 근사했어요. 열 · 배터리 · 소프트웨어 효율은 뺐습니다. 일반 사용자는 최신 기기를 갖고 있지 않다는 점도 기억하세요.'),
    talk=say('fly', 'magnify', '512 GB면 웬만한 건 다 들어가겠네. 들어가야 돌릴 거 아냐?') + say('robo', 'chart', '들어가기만 하면 1,792 GB/s가 이기지. 속도는 대역폭이라니까!'))

duel_sec = section('duel', 'VS', '대결 — 70B 모델(4비트)을 혼자 쓸 때, 어느 책상이 더 빨리 답할까?', say('doc', 'think', '초파리는 "메모리 큰 M3 Ultra", 주판봇은 "대역폭 두 배 RTX 5090"을 골랐어요. 교재 표의 숫자로만 판정합니다.') + duel(
    '70B 파라미터 · 4비트(무게 약 35 GB) 밀집 모델, 배치 1 — 초당 토큰이 더 많은 쪽은?', 'Apple M3 Ultra (512 GB · 819 GB/s)', '일단 올라가야 돌리지. 메모리가 먼저야.', 'NVIDIA RTX 5090 (32 GB · 1,792 GB/s)', '대역폭이 2.2배야. 토큰도 2.2배 빨리 나와!')
    + '<p class="notice">판정 기준: 초당 토큰 상한 = 대역폭 ÷ 무게(35 GB). 무게가 메모리보다 크면 올라가지 않으므로 0으로 칩니다. 교재 표 수치 <span class="chip-src">원문</span> + 10칸의 설명용 공식.</p>', small='판', tags=[('g', '판정 기준: 들어가는가 → 대역폭')])

reread = section('reread', '다시', '다시 읽기 — GPU를 고르는 질문 다섯', '''
<div class="cards"><div class="card"><h4>① 들어가는가? (VRAM)</h4><p>무게 + 50% 여유. 안 되면 장을 늘리거나 양자화(6주차 5.1).</p><p class="lim">한계: KV 캐시는 문맥·배치 따라 더 필요.</p></div>
<div class="card"><h4>② 무슨 일이 많은가?</h4><p>프리필 · 이미지 · 영상 → FLOPS. 디코드(낮~중간 배치) → 대역폭.</p><p class="lim">한계: 배치가 크면 디코드도 계산 쪽으로 간다 (논문편).</p></div>
<div class="card"><h4>③ 같은 정밀도로 비교했나?</h4><p>FP8끼리, 밀집끼리. 희소 값에 속지 않기.</p><p class="lim">한계: 정밀도를 낮추면 품질 확인이 필요.</p></div>
<div class="card"><h4>④ 길은 충분한가?</h4><p>여러 장이면 NVLink · NVSwitch, 노드 사이면 InfiniBand(비트 단위!).</p><p class="lim">한계: 클라우드마다 구성이 다르다.</p></div>
<div class="card"><h4>⑤ 너무 크지 않은가?</h4><p>작은 모델은 MIG 조각, 기기에서 될 일은 로컬로.</p><p class="lim">한계: MIG는 일부 GPU만, 로컬은 기기가 제각각.</p></div></div>
<div class="eq">디코드 상한 ≈ <b>대역폭</b> ÷ 무게 바이트 &nbsp;·&nbsp; 프리필 하한 ≈ 2 × 파라미터 × 토큰 ÷ <b>FLOPS</b> &nbsp;·&nbsp; 필요 VRAM ≈ 무게 × <i>1.5</i></div>
''' + say('asst', 'spark', '이 다섯 질문을 그래프 하나로 합친 게 이번 주 논문, 루프라인이에요. 논문편에서 H100의 지붕을 직접 그려 봐요.'), small='다시', tags=[('g', '3장 정리')])

onepage = section('sum', '한 장', '한 장으로 — 교재 표 모음', '''
<div class="tw"><table class="tb"><tr><th>GPU</th><th>세대</th><th>FP8 (밀집)</th><th>메모리</th><th>대역폭</th></tr>
<tr><td>H100</td><td>호퍼</td><td class="n">1,979 TF</td><td class="n">80 GB</td><td class="n">3.35 TB/s</td></tr>
<tr><td>H200</td><td>호퍼</td><td class="n">1,979 TF</td><td class="n">141 GB</td><td class="n">4.8 TB/s</td></tr>
<tr><td>L4</td><td>러브레이스</td><td class="n">242 TF</td><td class="n">24 GB</td><td class="n">300 GB/s</td></tr>
<tr><td>L40</td><td>러브레이스</td><td class="n">362 TF</td><td class="n">48 GB</td><td class="n">864 GB/s</td></tr>
<tr><td>B200</td><td>블랙웰</td><td class="n">~5 PF</td><td class="n">192 GB</td><td class="n">최대 8 TB/s</td></tr>
<tr><td>B300</td><td>블랙웰</td><td class="n">~5 PF</td><td class="n">288 GB</td><td class="n">최대 8 TB/s</td></tr></table></div>
<div class="tw"><table class="tb"><tr><th>연결</th><th>교재 수치</th></tr><tr><td>NVLink</td><td class="n">블랙웰 1,800 GB/s · 호퍼 900 GB/s</td></tr><tr><td>NVLink-C2C (Grace)</td><td class="n">최대 900 GB/s 양방향</td></tr><tr><td>InfiniBand</td><td class="n">NIC당 최대 400 Gb/s</td></tr><tr><td>이더넷</td><td class="n">NIC당 최대 100 Gb/s</td></tr><tr><td>노드</td><td class="n">GPU 8장 · NVL72는 블랙웰 72 + Grace 36</td></tr></table></div>
<div class="notebook"><h4>모아의 기록장 — 읽을 때 주의할 점</h4><ul><li>사양표의 FLOPS는 밀집 값을 볼 것 (희소 값은 보통 2배)</li><li>Gb/s(비트)와 GB/s(바이트)는 8배 차이</li><li>새 아키텍처는 실측 벤치마크가 나올 때까지 판단 보류 (소프트웨어가 따라오는 데 약 1년)</li><li>교재 수치는 출간 시점 기준 — 실제 구매·임대 전에는 제공사 최신 사양 확인</li></ul></div>
''' + say('moa', 'ok', '핵심 세 줄: 들어가는지(VRAM) · 무슨 일인지(FLOPS냐 대역폭이냐) · 어떻게 잇는지(NVLink · InfiniBand). 기록 완료!'), small='끝', tags=[('g', '요약')]).replace('<div class="hexno">한 장<small>','<div class="hexno">요약<small>')

outro = section('outro', '끝', '아웃트로', '<div class="outro"><div class="scene" data-img="sc_ch03_outro" role="img" aria-label="연구실 식구 여섯이 GPU 랙 앞에서 메모리 탑과 다리를 바라보는 장면"><img data-who="robo" data-mood="sigh" alt=""><img data-who="doc" data-mood="magic" alt=""><img data-who="asst" data-mood="proud" alt=""><img data-who="sia" data-mood="proud" alt=""><img data-who="moa" data-mood="sparkle" alt=""><img data-who="fly" data-mood="coffee" alt=""></div></div>'
    + say('doc', 'magic', '3장의 한 줄: GPU는 <b>계산 공방</b>과 <b>창고 통로</b>와 <b>다리</b>로 이루어진 기계다. 일에 맞는 숫자를 보면 고를 수 있다.')
    + say('robo', 'sigh', '대역폭이 속도인 건 맞았는데… 안 들어가면 0이었어. 다음엔 용량부터 볼게.')
    + say('fly', 'coffee', '올라가야 돌린다. 이번엔 내가 이겼지만, 들어가기만 하면 5090이 빠른 것도 인정.')
    + say('sia', 'signal', '다음은 같은 주의 논문편 — 루프라인 모델입니다. 오늘 본 두 숫자(FLOPS · 대역폭)가 지붕 두 개가 돼요.')
    + say('x2', 'cheer', '(짝짝짝)', name='방청석 X2'), small='', tags=())

GL = {'SM': ['SM = 계산 공방 (Streaming Multiprocessor)', '하드웨어', 'GPU 안의 작업장. SM마다 여러 코어와 L1 캐시가 들어 있다.'],
      '텐서 코어': ['텐서 코어 (Tensor Core)', '하드웨어', '행렬·벡터 곱을 한 번에 하는 코어. 추론 계산력은 이것으로 잰다.'],
      'CUDA 코어': ['CUDA 코어', '하드웨어', '숫자 하나(스칼라)를 다루는 코어.'], 'SFU': ['SFU (Special Function Unit)', '하드웨어', 'sin · cos · log 같은 함수를 빠르게. 소프트맥스에 필요.'],
      'MMA': ['MMA (Matrix Multiply and Accumulate)', '연산', 'D = (A × B) + C. 곱한 결과를 바탕 행렬에 더한다.'], 'FLOPS': ['FLOPS', '단위', '1초에 하는 부동소수점 연산 수. 테라 = 10¹², 페타 = 10¹⁵.'],
      'VRAM': ['VRAM (비디오 RAM)', '메모리', 'GPU에 붙은 큰 메모리(DRAM). 지금은 HBM 형태.'], 'HBM': ['HBM (고대역폭 메모리)', '메모리', 'HBM3 · HBM3e · HBM4. GPU 옆에 쌓아 올린 넓은 통로의 메모리.'],
      'SRAM': ['SRAM (정적 RAM)', '메모리', '칩 안의 빠르고 비싼 메모리. 캐시로 쓰인다.'], 'DRAM': ['DRAM (동적 RAM)', '메모리', '칩 밖의 범용 메모리. 기가바이트 단위.'],
      '대역폭': ['메모리 대역폭 (memory bandwidth)', '성능', 'VRAM에서 GPU 코어 쪽으로 1초에 옮길 수 있는 최대량.'], 'KV 캐시': ['KV 캐시 (KV cache)', '추론', '앞 토큰들의 키·값을 저장해 다시 계산하지 않게 하는 메모리.'],
      'OOM': ['OOM (out of memory)', '오류', '메모리가 모자라 실패하거나 멈추는 것.'], '프리필': ['프리필 (prefill)', '추론', '입력 토큰을 한꺼번에 처리하는 단계. 계산력이 병목.'],
      '디코드': ['디코드 (decode)', '추론', '토큰을 하나씩 만들어 내는 단계. 낮~중간 배치에선 대역폭이 병목.'], 'NVLink': ['NVLink', '연결', 'GPU 둘을 잇는 고대역 1:1 연결. 블랙웰 1,800 GB/s.'],
      'NVSwitch': ['NVSwitch', '연결', '노드 안 모든 GPU가 서로 통하게 하는 스위치 층.'], 'InfiniBand': ['InfiniBand', '연결', '노드끼리 잇는 네트워크. NIC당 최대 400 Gb/s.'],
      'MIG': ['MIG (Multi-Instance GPU)', '기능', '큰 GPU를 하드웨어 수준에서 최대 7조각으로 나누기.'], '노드': ['노드 (node)', '단위', 'GPU 8장을 묶은 표준 단위.'],
      '인스턴스': ['인스턴스 (instance)', '클라우드', 'GPU · CPU · 메모리 · 저장소 · 네트워크 · 인터커넥트를 묶어 빌리는 가상 머신.'], 'FP8': ['FP8', '정밀도', '8비트 부동소수점. 호퍼부터.'],
      'FP4': ['FP4', '정밀도', '4비트 부동소수점. 블랙웰부터.'], '희소성': ['2:4 구조적 희소성', '성능', '네 값 중 둘이 0인 구조. 텐서 코어가 0 곱하기를 건너뛴다.'],
      '통합 메모리': ['통합 메모리 (unified memory)', '하드웨어', 'Apple M 시리즈처럼 CPU와 GPU가 같은 메모리를 함께 쓰는 구조.'], 'MoE': ['MoE (전문가 혼합)', '모델', '요청마다 전체 무게의 일부(활성 파라미터)만 쓰는 모델 구조.']}
CORE = ['SM', '텐서 코어', 'MMA', 'FLOPS', 'VRAM', '대역폭', 'KV 캐시', 'NVLink', 'InfiniBand', 'MIG', '프리필', '디코드']

QUIZ = {
 'lv1': [{'q': '대부분의 추론 엔지니어가 쓰는 자리는?', 'o': ['클라우드 GPU', '에어갭', '책상 밑 B200'], 'a': 0, 'why': '맞아요. 빠르게 크는 제품에는 클라우드의 유연성과 접근성이 맞아요.', 'hint': '풀이 2번.'},
         {'q': '대규모 추론에서 데이터센터 GPU가 표준인 이유로 교재가 "무엇보다 중요하다"고 한 것은?', 'o': ['GPU끼리 잇는 고대역 연결 등', '가장 싸서', '게임도 잘 돌아서'], 'a': 0, 'why': '맞아요. 한 장 성능보다 고대역 GPU 간 연결 · 표준 구성 · 수백만 장의 가용성이 더 중요해요.', 'hint': '풀이 1번.'}],
 'lv2': [{'q': '추론 계산력을 잴 때 기준이 되는 코어는?', 'o': ['CUDA 코어', '텐서 코어', 'SFU'], 'a': 1, 'why': '맞아요. MMA 명령을 맡는 텐서 코어가 추론의 기초예요.', 'hint': '짝 카드 오른쪽.'},
         {'q': '[계산] FP16에서 1 PFLOPS인 GPU는 FP8에서 대략?', 'o': ['0.5 PFLOPS', '1 PFLOPS', '2 PFLOPS'], 'a': 2, 'why': '맞아요. 정밀도를 반으로 줄이면 FLOPS는 대체로 두 배예요.', 'hint': '풀이 4번.'},
         {'q': '사양표에서 추론용으로 봐야 할 FLOPS는?', 'o': ['희소(sparse) 값', '밀집(dense) 값'], 'a': 1, 'why': '맞아요. 추론은 기본이 밀집이에요.', 'hint': '희소 단추를 눌러 보세요.'}],
 'lv3': [{'q': 'H100의 L2 캐시는 칩 전체 몇 MB?', 'o': ['50 MB', '256 MB', '80 GB'], 'a': 0, 'why': '맞아요. L1은 SM마다 256 KB, L2는 전체 50 MB예요.', 'hint': 'SM 그림 아래 띠.'},
         {'q': '[계산] 70B 모델을 8비트로 올릴 때 교재 경험칙으로 필요한 VRAM은?', 'o': ['약 70 GB', '약 105 GB', '약 140 GB'], 'a': 1, 'why': '맞아요. 무게 70 GB × 1.5 = 105 GB. H100 한 장(80 GB)으론 모자라요.', 'hint': '계산기에서 70B · 8비트.'}],
 'lv4': [{'q': 'H100 → H200으로 바꿀 때 배치 1 디코드 속도 상한은 약 몇 배?', 'o': ['1.0배', '약 1.43배', '약 2배'], 'a': 1, 'why': '맞아요. 대역폭 4.8 ÷ 3.35 ≈ 1.43. 계산력은 같아서 프리필 하한은 그대로예요.', 'hint': 'KPI 줄을 보세요.'},
         {'q': '이미지 · 영상 생성이 주력이면 우선 볼 숫자는?', 'o': ['FLOPS', '메모리 대역폭', 'NIC 수'], 'a': 0, 'why': '맞아요. 계산이 병목인 일이에요.', 'hint': '짝 카드.'}],
 'lv5': [{'q': 'GPU 이름 B200에서 B가 뜻하는 것은?', 'o': ['아키텍처 세대(블랙웰)', '메모리 크기', '가격대'], 'a': 0, 'why': '맞아요. 글자는 세대, 숫자는 세대 안의 모델이에요.', 'hint': '짝 카드.'},
         {'q': 'FP4를 처음 도입한 세대는?', 'o': ['호퍼', '러브레이스', '블랙웰'], 'a': 2, 'why': '맞아요. 호퍼가 FP8, 블랙웰이 FP4와 마이크로스케일링 형식.', 'hint': '연표에서 블랙웰.'},
         {'q': '러브레이스 GPU의 큰 한계로 교재가 든 것은?', 'o': ['FP8 미지원', 'NVLink 미지원', '메모리 없음'], 'a': 1, 'why': '맞아요. 그래서 여러 장 묶기가 비효율이에요.', 'hint': '풀이 4번.'}],
 'lv6': [{'q': 'Grace CPU와 GPU 메모리 사이 NVLink-C2C 대역폭(양방향)은 최대?', 'o': ['90 GB/s', '900 GB/s', '9 TB/s'], 'a': 1, 'why': '맞아요. PCIe 같은 표준 연결보다 몇 배 빨라요.', 'hint': '짝 카드.'}],
 'lv7': [{'q': '[계산] InfiniBand 400 Gb/s는 몇 GB/s?', 'o': ['50 GB/s', '400 GB/s', '3,200 GB/s'], 'a': 0, 'why': '맞아요. 비트 → 바이트는 8로 나눠요.', 'hint': '풀이 2번.'},
         {'q': '노드 하나에 든 GPU는 보통 몇 장?', 'o': ['4장', '8장', '72장'], 'a': 1, 'why': '맞아요. 72장은 NVL72 랙 시스템이에요.', 'hint': '짝 카드.'}],
 'lv8': [{'q': 'H100 MIG의 계산 조각은 몇 개?', 'o': ['7개', '8개', '132개'], 'a': 0, 'why': '맞아요. 메모리 조각은 8개, 계산 조각은 7개(SM 132개가 7로 딱 안 나뉘어 남는 SM은 쉼).', 'hint': '그림 3.5.'},
         {'q': 'MIG를 쓰는 주된 이유는?', 'o': ['모델이 GPU보다 너무 작을 때 자원 낭비를 줄이려고', '모델이 너무 클 때 합치려고', '전력을 늘리려고'], 'a': 0, 'why': '맞아요. 큰 GPU의 조각에서 작은 모델을 돌려요.', 'hint': '풀이 1번.'}],
 'lv9': [{'q': 'Cerebras · Groq가 거는 특기는?', 'o': ['메모리 대역폭', '전력 효율', '플랫폼 통합'], 'a': 0, 'why': '맞아요. 초고대역 메모리로 디코드를 가속해요.', 'hint': '특기 단추.'},
         {'q': '도전자들의 공통 과제가 아닌 것은?', 'o': ['소프트웨어', '제조', '이름 짓기'], 'a': 2, 'why': '맞아요. 셋은 소프트웨어 · 제조 · 유통이에요.', 'hint': '풀이 1번.'}],
 'lv10': [{'q': '교재 표에서 M3 Ultra의 메모리와 대역폭은?', 'o': ['32 GB · 1,792 GB/s', '512 GB · 819 GB/s', '192 GB · 8 TB/s'], 'a': 1, 'why': '맞아요. 용량은 크고 속도는 RTX 5090보다 느려요.', 'hint': '계산기 KPI.'},
          {'q': '고급 폰에서도 버거워지는 모델 크기는 대략?', 'o': ['1~2B 파라미터 이상', '100B 이상만', '모든 모델이 거뜬'], 'a': 0, 'why': '맞아요. 그래서 폰에는 받아쓰기 · 음성 합성 · 번역 같은 작은 모델 일이 맞아요.', 'hint': '풀이 4번.'}]}

N = lambda i, t, ko, en, a, d=None, s=None, lv=None, fam='systems': node(i, t, ko, en, a, P, d, (BK, s) if s else None, lv, fam)
KG = {'version': '1.0', 'page': P, 'nodes': [
    N('lab:concept/accelerator', 'Concept', '가속기', 'accelerator', '#top', '대량 데이터를 싣고 초당 수조 번 계산하도록 만든 하드웨어.', '3장 도입', 1),
    N('lab:concept/gpu-types', 'Concept', 'GPU 세 종류 (데이터센터 · 워크스테이션 · 개인)', 'three GPU types', '#lv1', None, '3장 도입', 1),
    N('lab:concept/deploy-modes', 'Concept', '클라우드 · 온프레미스 · 에어갭', 'cloud, on-prem, air-gapped', '#lv1', None, '3장 도입', 1),
    N('lab:concept/sm', 'Concept', 'SM (계산 공방)', 'Streaming Multiprocessor', '#lv2', None, '3.1.1', 2),
    N('lab:concept/tensor-core', 'Concept', '텐서 코어', 'Tensor Core', '#lv2', '행렬·벡터 연산 코어. MMA 담당.', '3.1.1', 2),
    N('lab:concept/mma', 'Concept', 'MMA (D = A×B + C)', 'Matrix Multiply and Accumulate', '#lv2', None, '그림 3.1', 2),
    N('lab:metric/flops', 'Metric', 'FLOPS (밀집 · 희소)', 'FLOPS dense vs sparse', '#lv2', None, '3.1.1', 2),
    N('lab:concept/vram', 'Concept', 'VRAM (HBM)', 'VRAM / HBM', '#lv3', None, '3.1.2', 2),
    N('lab:concept/cache', 'Concept', '캐시 L0 · L1 · L2 (SRAM)', 'GPU caches', '#lv3', None, '3.1.2', 2),
    N('lab:metric/bandwidth', 'Metric', '메모리 대역폭', 'memory bandwidth', '#lv3', None, '3.1.2', 2),
    N('lab:concept/headroom', 'Concept', 'VRAM = 무게 + 50% 여유', 'VRAM headroom rule', '#lv3', None, '3.1.2', 2),
    N('lab:concept/prefill-compute', 'Concept', '프리필 · 이미지 · 영상 = 계산 병목', 'compute-bound workloads', '#lv4', None, '3.1.1', 3),
    N('lab:concept/decode-memory', 'Concept', '디코드(낮~중간 배치) = 대역폭 병목', 'memory-bound decode', '#lv4', None, '3.1.2', 3),
    N('lab:concept/naming', 'Concept', 'GPU 이름 = 세대 글자 + 모델 숫자', 'GPU naming', '#lv5', None, '3.2', 1),
    N('lab:concept/hopper', 'Concept', '호퍼 (H100 · H200, FP8)', 'Hopper', '#lv5', None, '3.2.1', 2),
    N('lab:concept/lovelace', 'Concept', '러브레이스 (L4 · L40, NVLink 없음)', 'Ada Lovelace', '#lv5', None, '3.2.2', 2),
    N('lab:concept/blackwell', 'Concept', '블랙웰 (B200 · B300, FP4)', 'Blackwell', '#lv5', None, '3.2.3', 2),
    N('lab:concept/rubin', 'Concept', '루빈 (HBM4 · CPX)', 'Rubin', '#lv5', None, '3.2.4', 3),
    N('lab:concept/grace', 'Concept', 'Grace · Vera CPU (NVLink-C2C 900 GB/s)', 'Grace and Vera CPUs', '#lv6', None, '3.2.5', 3),
    N('lab:concept/instance', 'Concept', '인스턴스 (여섯 구성 요소)', 'instance', '#lv7', None, '3.3', 1),
    N('lab:concept/node', 'Concept', '노드 (GPU 8장)', 'node', '#lv7', None, '3.3.1', 2),
    N('lab:concept/interconnect', 'Concept', 'NVLink · NVSwitch · InfiniBand', 'interconnects', '#lv7', None, '3.3.1', 3),
    N('lab:method/mig', 'Method', 'MIG (칸막이 GPU)', 'Multi-Instance GPU', '#lv8', None, '3.3.2', 3),
    N('lab:concept/other-accel', 'Concept', '다른 가속기 (TPU · LPU · WSE-3 …)', 'other accelerators', '#lv9', None, '3.4', 2),
    N('lab:concept/local', 'Concept', '로컬 추론 (데스크톱 · 모바일)', 'local inference', '#lv10', None, '3.5', 2),
    N('lab:concept/unified-memory', 'Concept', '통합 메모리 (Apple M 시리즈)', 'unified memory', '#lv10', None, '3.5.1', 3),
    node('lab:limitation/oom', 'Limitation', '메모리 부족(OOM)', 'out of memory', '#lv3', P), node('lab:limitation/no-nvlink', 'Limitation', 'NVLink 없음 → 병렬화 비효율', 'no NVLink', '#lv5', P),
    node('lab:limitation/too-big-gpu', 'Limitation', '작은 모델엔 GPU가 너무 큼', 'GPU too big for model', '#lv8', P), node('lab:limitation/no-cuda', 'Limitation', 'CUDA 없는 소프트웨어 재구축', 'no CUDA', '#lv9', P),
    node('lab:limitation/local-hw', 'Limitation', '로컬 하드웨어 · 발열 · 배터리', 'local hardware limits', '#lv10', P), node('lab:limitation/ib-slow', 'Limitation', '노드 사이 연결은 한 자릿수 느림', 'inter-node slower', '#lv7', P),
    node('lab:claim/h100-h200', 'Claim', 'H100 · H200 FP8 1,979 TF, 대역폭 3.35 → 4.8 TB/s', 'H100 vs H200 specs', '#lv5', P, None, (BK, '3.2.1')),
    node('lab:claim/b200', 'Claim', 'B200 · B300 약 5 PF, 192 · 288 GB, 최대 8 TB/s', 'B200/B300 specs', '#lv5', P, None, (BK, '3.2.3')),
    node('lab:claim/nvlink', 'Claim', 'NVLink 블랙웰 1,800 · 호퍼 900 GB/s, InfiniBand 400 Gb/s', 'interconnect speeds', '#lv7', P, None, (BK, '3.3.1')),
    node('lab:claim/mig-h100', 'Claim', 'H100 MIG: 메모리 8조각 · 계산 7조각, SM 132개', 'H100 MIG slices', '#lv8', P, None, (BK, '3.3.2')),
    node('lab:claim/desktop', 'Claim', 'RTX 5090 32 GB · 1,792 GB/s vs M3 Ultra 512 GB · 819 GB/s', 'desktop comparison', '#lv10', P, None, (BK, '3.5.1')),
    node('lab:analogy/factory', 'Analogy', '계산 공방 · 창고 통로 · 다리 ↔ GPU', 'factory analogy', '#lv3', P), node('lab:analogy/partition', 'Analogy', '칸막이 친 프레스 ↔ MIG', 'partitioned press', '#lv8', P),
    node('lab:question/core', 'Question', '같은 모델이 왜 GPU마다 빠르기도, 안 올라가기도 할까?', 'Why does hardware matter?', '#top', P),
    node('lab:question/duel', 'Question', '대결: 70B 4비트를 혼자 쓸 때 어느 책상이 빠를까?', 'Duel: which desktop?', '#duel', P),
    node('lab:question/new-arch', 'Question', '새 아키텍처는 언제 판단할 수 있나?', 'When to judge new architectures?', '#lv5', P),
    node('lab:sim/fit', 'Simulation', 'VRAM 계산기', 'VRAM fit calculator', '#lv3', P), node('lab:sim/flops', 'Simulation', '계산력 계기판', 'FLOPS gauge', '#lv2', P),
    node('lab:sim/bottleneck', 'Simulation', '프리필 · 디코드 상한 비교', 'prefill vs decode', '#lv4', P), node('lab:sim/net', 'Simulation', '연결별 전송 시간', 'interconnect timing', '#lv7', P),
    node('lab:sim/mig', 'Simulation', 'H100 칸막이 실험', 'MIG slicer', '#lv8', P), node('lab:sim/local', 'Simulation', '내 책상에 올려 보기', 'desktop fit', '#lv10', P),
    node('lab:work/' + BK, 'Work', 'Kiely (2026)', 'Kiely 2026 ch.3', '#top', P, '교재 Inference Engineering 3장 하드웨어'), node('lab:work/williams2009roofline', 'Work', 'Williams 외 (2009)', 'Roofline', '#reread', P, '루프라인 모형 논문 — 4주차 논문편')],
 'edges': [edge('lab:concept/sm', 'partOf', 'lab:concept/accelerator', '#lv2'), edge('lab:concept/tensor-core', 'partOf', 'lab:concept/sm', '#lv2'), edge('lab:concept/mma', 'relatedTo', 'lab:concept/tensor-core', '#lv2'),
           edge('lab:metric/flops', 'relatedTo', 'lab:concept/tensor-core', '#lv2'), edge('lab:concept/cache', 'partOf', 'lab:concept/sm', '#lv3'), edge('lab:concept/vram', 'prerequisiteOf', 'lab:concept/headroom', '#lv3'),
           edge('lab:concept/headroom', 'addressedBy', 'lab:limitation/oom', '#lv3'), edge('lab:metric/flops', 'prerequisiteOf', 'lab:concept/prefill-compute', '#lv4'), edge('lab:metric/bandwidth', 'prerequisiteOf', 'lab:concept/decode-memory', '#lv4'),
           edge('lab:concept/naming', 'relatedTo', 'lab:concept/hopper', '#lv5'), edge('lab:concept/lovelace', 'hasLimitation', 'lab:limitation/no-nvlink', '#lv5'), edge('lab:concept/blackwell', 'relatedTo', 'lab:concept/hopper', '#lv5'),
           edge('lab:concept/rubin', 'relatedTo', 'lab:concept/blackwell', '#lv5'), edge('lab:concept/grace', 'relatedTo', 'lab:concept/hopper', '#lv6'), edge('lab:concept/node', 'partOf', 'lab:concept/instance', '#lv7'),
           edge('lab:concept/interconnect', 'partOf', 'lab:concept/instance', '#lv7'), edge('lab:concept/interconnect', 'hasLimitation', 'lab:limitation/ib-slow', '#lv7'), edge('lab:limitation/too-big-gpu', 'addressedBy', 'lab:method/mig', '#lv8'),
           edge('lab:concept/other-accel', 'hasLimitation', 'lab:limitation/no-cuda', '#lv9'), edge('lab:concept/local', 'hasLimitation', 'lab:limitation/local-hw', '#lv10'), edge('lab:concept/unified-memory', 'partOf', 'lab:concept/local', '#lv10'),
           edge('lab:concept/gpu-types', 'relatedTo', 'lab:concept/deploy-modes', '#lv1'), edge('lab:concept/decode-memory', 'relatedTo', 'lab:work/williams2009roofline', '#reread'), edge('lab:concept/prefill-compute', 'relatedTo', 'lab:work/williams2009roofline', '#reread')]
          + [edge(c, 'assertedIn', 'lab:work/' + BK, '#sum') for c in ['lab:claim/h100-h200', 'lab:claim/b200', 'lab:claim/nvlink', 'lab:claim/mig-h100', 'lab:claim/desktop']]
          + [edge('lab:claim/h100-h200', 'supports', 'lab:concept/decode-memory', '#lv4'), edge('lab:claim/desktop', 'supports', 'lab:concept/unified-memory', '#lv10'),
             edge('lab:analogy/factory', 'relatedTo', 'lab:concept/vram', '#lv3'), edge('lab:analogy/partition', 'relatedTo', 'lab:method/mig', '#lv8'),
             edge('lab:sim/fit', 'relatedTo', 'lab:concept/headroom', '#lv3'), edge('lab:sim/bottleneck', 'relatedTo', 'lab:concept/decode-memory', '#lv4'), edge('lab:sim/mig', 'relatedTo', 'lab:method/mig', '#lv8'),
             edge('lab:sim/net', 'relatedTo', 'lab:concept/interconnect', '#lv7'), edge('lab:sim/local', 'relatedTo', 'lab:concept/local', '#lv10'), edge('lab:sim/flops', 'relatedTo', 'lab:metric/flops', '#lv2')]}

DEFS = {'lab:concept/gpu-types': '데이터센터(예: B200) · 워크스테이션(예: RTX Pro 6000) · 개인용(예: RTX 5090) GPU.',
 'lab:concept/deploy-modes': '데이터센터 GPU를 쓰는 세 자리: 빌리기(클라우드) · 사서 직접 통제(온프레미스) · 외부망 차단(에어갭).',
 'lab:concept/sm': 'GPU 안의 작업장. SM마다 여러 코어(CUDA · 텐서 · SFU)와 L1 캐시가 있다.',
 'lab:concept/mma': 'D = (A × B) + C. 곱한 결과를 바탕 행렬에 더하는 텐서 코어의 기본 동작(그림 3.1).',
 'lab:metric/flops': '초당 부동소수점 연산 수. 사양표의 밀집 값을 보고 같은 정밀도끼리 비교한다.',
 'lab:concept/vram': 'GPU에 붙은 큰 메모리(DRAM, HBM 형태). 모델 무게와 KV 캐시를 담는다.',
 'lab:concept/cache': '칩 안 SRAM 캐시. L0(텐서 코어 명령) · L1(SM마다, H100 256 KB) · L2(공유, H100 50 MB).',
 'lab:metric/bandwidth': 'VRAM에서 GPU 코어 쪽으로 1초에 옮길 수 있는 최대량. 디코드 속도의 상한을 정한다.',
 'lab:concept/headroom': '필요 VRAM ≈ 모델 무게 + 최소 50% 여유(KV 캐시). 긴 문맥 · 큰 배치 · 영상 모델은 더.',
 'lab:concept/prefill-compute': 'LLM 프리필, 이미지 · 영상 생성은 계산력(FLOPS)이 병목이다.',
 'lab:concept/decode-memory': '낮~중간 배치의 LLM 디코드는 메모리 대역폭이 병목이다.',
 'lab:concept/naming': 'GPU 이름의 글자는 아키텍처 세대(H, B), 숫자는 세대 안의 모델(100, 200).',
 'lab:concept/hopper': '2022년 H100으로 시작. FP8, 4세대 텐서 코어, 비동기 전송(FlashAttention 3).',
 'lab:concept/lovelace': '호퍼 6개월 뒤의 그래픽 쪽 세대(L4 · L40). FP8 지원, NVLink 없음.',
 'lab:concept/blackwell': '2024년 B200으로 시작. FP4와 마이크로스케일링 형식, FlashAttention 4.',
 'lab:concept/rubin': '2026년 예정. HBM4, 프리필용 CPX 칩, Vera CPU.',
 'lab:concept/grace': 'NVIDIA의 ARM CPU. NVLink-C2C로 GPU 메모리와 최대 900 GB/s(양방향) 연결.',
 'lab:concept/instance': '클라우드 GPU 할당의 최소 단위. GPU · CPU · 호스트 메모리 · 저장소 · 네트워크 · 인터커넥트.',
 'lab:concept/node': 'GPU 8장을 묶은 표준 단위(예: B200 노드).',
 'lab:concept/interconnect': 'NVLink(1:1) · NVSwitch(노드 안 전원 연결) · InfiniBand(노드 사이, NIC당 최대 400 Gb/s).',
 'lab:method/mig': '큰 GPU를 하드웨어 수준에서 최대 7조각으로 나눠 작은 모델을 효율적으로 돌리기.',
 'lab:concept/other-accel': 'AMD · AWS · Cerebras · Etched · Furiosa · Google · Groq · Qualcomm · Sambanova의 가속기.',
 'lab:concept/local': '사용자 기기(데스크톱 · 모바일)에서 직접 돌리는 추론. 지연 0 · 독립성 · 개인정보 · 비용 0.',
 'lab:concept/unified-memory': 'Apple M 시리즈처럼 CPU와 GPU가 같은 메모리를 함께 쓰는 구조. 크지만 느리다.',
 'lab:limitation/oom': '무게나 KV 캐시가 VRAM보다 크면 올리다 실패하거나 추론 중에 멈춘다.',
 'lab:limitation/no-nvlink': '러브레이스 GPU는 NVLink가 없어 파이프라인 병렬 같은 비효율적 방법으로만 묶는다.',
 'lab:limitation/too-big-gpu': '수십억 파라미터 이하의 작은 모델은 큰 GPU의 자원을 다 쓰지 못한다.',
 'lab:limitation/no-cuda': 'NVIDIA 밖 가속기는 CUDA 없이 추론 스택을 새로 지어야 한다.',
 'lab:limitation/local-hw': '로컬 기기는 성능 · 발열 · 기기 조합 · 배터리의 한계가 있다.',
 'lab:limitation/ib-slow': '노드 사이 연결(InfiniBand 50 GB/s)은 NVLink보다 한 자릿수 이상 느리다.',
 'lab:claim/h100-h200': 'H100 · H200은 FP8 계산력이 같고(1,979 TF) 메모리 80 → 141 GB, 대역폭 3.35 → 4.8 TB/s.',
 'lab:claim/b200': 'B200 · B300은 약 5 PF(FP8), 192 · 288 GB, 최대 8 TB/s.',
 'lab:claim/nvlink': 'NVLink 블랙웰 1,800 · 호퍼 900 GB/s, InfiniBand NIC당 최대 400 Gb/s, 이더넷 100 Gb/s.',
 'lab:claim/mig-h100': 'H100은 메모리 8조각 · 계산 7조각, SXM H100의 SM은 132개.',
 'lab:claim/desktop': 'RTX 5090 32 GB · 1,792 GB/s · $5,000 vs M3 Ultra 512 GB · 819 GB/s · $10,000.',
 'lab:analogy/factory': '계산 공방(SM) · 창고(VRAM) · 창고 통로(대역폭) · 다리(인터커넥트)로 GPU를 보는 비유.',
 'lab:analogy/partition': '초대형 프레스에 칸막이를 쳐 여러 작업이 나눠 쓰는 비유(MIG).',
 'lab:question/core': '같은 모델이 왜 어떤 GPU에선 빠르고 어떤 GPU에선 아예 안 올라갈까?',
 'lab:question/duel': '70B 4비트 모델을 혼자 쓸 때 RTX 5090과 M3 Ultra 중 어느 쪽이 빠를까?',
 'lab:question/new-arch': '새 아키텍처는 실측 벤치마크와 소프트웨어 지원이 나온 뒤(약 1년) 판단한다.',
 'lab:sim/fit': '모델 크기 · 숫자 크기 · GPU · 장 수로 VRAM에 들어가는지 보는 계산기.',
 'lab:sim/flops': '정밀도와 희소성에 따라 GPU별 계산력을 비교하는 계기판.',
 'lab:sim/bottleneck': '디코드 토큰 상한(배치 · 비용 포함)과 프리필 시간 하한을 GPU별로 비교하는 계기판.',
 'lab:sim/net': '데이터 크기와 연결 종류로 전송 시간을 비교하는 계기판(로그 눈금).',
 'lab:sim/mig': 'H100을 MIG 크기별로 나눠 보고 모델이 들어가는지 보는 계기판.',
 'lab:sim/local': 'RTX 5090과 M3 Ultra에 모델을 올려 메모리와 토큰 속도를 비교하는 계기판.'}
_miss = fill_defs(KG, DEFS)
assert not _miss, _miss
REFS = [book_ref(), ref('williams2009roofline', 'article-journal', 'Roofline: An Insightful Visual Performance Model for Multicore Architectures', ['Samuel Williams', 'Andrew Waterman', 'David Patterson'], 2009, 'Communications of the ACM', 'https://doi.org/10.1145/1498765.1498785', role='background', note='기술 보고서 UCB/EECS-2008-134 (2008)')]

JS = r'''
Object.assign(L.C,{text:'#16212b',muted:'#5b6874',rule:'#d5dbe2',stain:'#9b3fb5',gfp:'#13733a',eye:'#c9302c',amber:'#a35c00',info:'#1e55c8',panel:'#f6f8fa',panel2:'#eef2f6',fly:'#c93030',robo:'#0b7a86',doc:'#7a3fd6',asst:'#c42a6e',sia:'#5a5a6e',moa:'#93651a'});
var C=L.C,F=L.FONT,fit=L.fit,grid=L.grid,stamp=L.stamp,G=__GPU__;
function fmtN(v,d){return v.toLocaleString('ko-KR',{maximumFractionDigits:d==null?1:d})}
function hbars(x,W,rows,o){/* rows:[label,value,color,note] 가로 막대 */var L0=o.L0||120,R=W-(o.R||90),T=o.T||12,h=o.h||22,gap=o.gap||8,mx=o.max||Math.max.apply(0,rows.map(function(r){return r[1]}))||1;
  rows.forEach(function(r,i){var y=T+i*(h+gap),w=r[1]>0?(R-L0)*(o.log?Math.log10(1+r[1])/Math.log10(1+mx):r[1]/mx):0;x.fillStyle=r[2];x.fillRect(L0,y,Math.max(w,r[1]>0?2:0),h);
    x.fillStyle=C.text;x.font='12px '+F;x.textAlign='right';x.fillText(r[0],L0-8,y+h/2+4);x.textAlign='left';x.fillText(r[3]!=null?r[3]:fmtN(r[1]),L0+w+6,y+h/2+4);});}
L.kpis('#heroK',[['3 · 3','GPU 종류 · 자리','g'],['1,979 TF','H100 · H200 FP8 계산력','m'],['3.35 → 4.8','H100 → H200 대역폭 (TB/s)','i'],['8 · 7','노드의 GPU 수 · MIG 조각','a']]);
/* 1 자리 */
var m1=1,m2=0,m3=0;function updM(){var mode=m3?'에어갭':m2?(m1?'온프레미스 + 클라우드 병행':'온프레미스'):'클라우드',why=m3?'GPU를 내 데이터센터에 두고, 추론하려면 물리적으로 접근해야 하는 구성이에요.'+(m1?' 트래픽이 빠르게 늘어도 외부망을 쓸 수 없으니, 증설 기간(구매 · 설치)을 미리 계획해야 해요.':''):m2?(m1?'핵심 데이터는 직접 통제하는 온프레미스에 두고, 갑자기 늘어나는 트래픽은 클라우드로 받는 병행 구성을 생각해 볼 수 있어요.':'GPU를 사서 직접 통제하는 데이터센터에 설치해요. 대기업 · 정부가 주로 써요.'):(m1?'하이퍼스케일러(AWS · GCP)나 네오클라우드(Coreweave · Nebius)에서 빌려요. 대부분의 추론 엔지니어가 여기.':'트래픽이 안정적이면 클라우드에서 장기 예약으로 빌리거나, 규모가 크면 직접 사는 쪽도 비교해 볼 수 있어요.');
  L.kpis('#mK',[[mode,'추천 자리 (설명용 판단)',m3?'r':m2?'a':'g'],[m1?'중요':'보통','유연성 필요',m1?'g':'i'],[m3?'몇 달':m2?'몇 주~몇 달':'몇 분~며칠','증설에 걸리는 시간 (설명용 감)',m3?'r':m2?'a':'g']]);L.ins('#mI',[[m3?'r':m2?'a':'g',why],['i',m1&&(m2||m3)?'트래픽이 빠르게 늘면 직접 산 GPU는 증설이 느려요. 교재는 그래서 성장하는 제품엔 클라우드를 권해요.':'교재: 클라우드 GPU는 빠르게 크는 AI 제품에 필요한 유연성과 접근성을 줘요.']]);}
L.bindSeg('#m1',function(v){m1=+v;updM()});L.bindSeg('#m2',function(v){m2=+v;updM()});L.bindSeg('#m3',function(v){m3=+v;updM()});updM();
/* 2 MMA */
var MA,MB,MC,mk=0;function newMM(){var r=L.rng(Math.floor(Math.random()*999)+1);function m(){return [0,1,2,3].map(function(){return 1+Math.floor(r()*4)})}MA=m();MB=m();MC=m();mk=0;drawMM();}
function dval(k){var i=k>>1,j=k&1;return MA[i*2]*MB[j]+MA[i*2+1]*MB[2+j]+MC[k];}
function cell(arr,cls,hl){return '<span class="mm '+cls+'">'+arr.map(function(v,k){return '<span'+(hl&&hl.indexOf(k)>=0?' class="hl"':'')+'>'+v+'</span>'}).join('')+'</span>'}
function drawMM(){var k=mk-1,i=k>>1,j=k&1,ha=k>=0?[i*2,i*2+1]:[],hb=k>=0?[j,2+j]:[],hc=k>=0?[k]:[];var D=[0,1,2,3].map(function(t){return t<mk?dval(t):'?'});
  $('#mmRow').innerHTML='D'+cell(D,'d',hc)+'= ('+cell(MA,'a',ha)+'×'+cell(MB,'b',hb)+') +'+cell(MC,'c',hc);
  $('#mmI').innerHTML=k<0?'<p class="i">A의 한 행과 B의 한 열을 곱해 더하고, 마지막에 C의 같은 칸을 더해요.</p>':'<p class="g">D['+(i+1)+','+(j+1)+'] = '+MA[i*2]+'×'+MB[j]+' + '+MA[i*2+1]+'×'+MB[2+j]+' + '+MC[k]+' = <b>'+dval(k)+'</b> — 곱 2번 · 더하기 2번'+(mk===4?' · 네 칸 완성! 텐서 코어는 이런 칸 수천 개를 한 번에 해요.':'')+'</p>';}
$('#mmNext').addEventListener('click',function(){mk=mk>=4?1:mk+1;drawMM()});$('#mmNew').addEventListener('click',newMM);newMM();
/* 2 FLOPS */
var cF=$('#cFlops'),fp='8',fs=0,ORD=['L4','L40','H100','H200','B200','B300'];
function flops(g,p,s){var b=G[g].fp8,v=p==='8'?b:p==='16'?b/2:(G[g].fp4?b*2:0);return v*(s?2:1);}
function drawF(){var W=fit(cF,200),x=cF.getContext('2d');x.clearRect(0,0,W,200);grid(x,W,200);var mx=Math.max.apply(0,ORD.map(function(g){return flops(g,'4',1)}));
  hbars(x,W,ORD.map(function(g){var v=flops(g,fp,fs);return [g+' ('+G[g].arch+')',v,G[g].arch==='블랙웰'?C.gfp:G[g].arch==='호퍼'?C.info:C.amber,v?fmtN(v,0)+' TF':'지원 안 함'];}),{L0:130,max:mx,h:20,gap:8});
  stamp(x,W,fp==='8'&&!fs?'교재 표 값':'교재 규칙으로 계산');}
function updF(){var h=flops('H100',fp,fs),b=flops('B200',fp,fs);L.kpis('#fK',[[h?fmtN(h,0):'—','H100 (TF)','i'],['~'+fmtN(b,0),'B200 (TF, 교재 "약")','g'],[fs?'희소':'밀집',fs?'2:4 희소 — 추론 기본값 아님':'추론 기본값',fs?'r':'g']]);
  L.ins('#fI',[[fp==='4'?'a':'g',fp==='4'?'FP4는 블랙웰부터예요. 호퍼 · 러브레이스는 막대가 없어요.':fp==='16'?'FP16은 FP8의 절반 — 정밀도를 반으로 줄이면 FLOPS가 두 배라는 규칙을 거꾸로 본 거예요.':'교재 표의 FP8 밀집 값이에요. GPU 비교는 이렇게 같은 정밀도 · 같은 밀집끼리.'],[fs?'r':'i',fs?'희소 값은 0이 절반인 특수 구조일 때만 나와요. 사양표의 큰 숫자에 속지 마세요.':'이미지 · 영상 생성, LLM 프리필이 많다면 이 막대가 긴 GPU를 고르세요.']]);drawF();}
L.bindSeg('#fP',function(v){fp=v;updF()});L.bindSeg('#fS',function(v){fs=+v;updF()});L.addMod(cF,function(dt){if(dt===0)drawF()});updF();
/* 3 SM 그림 */
$$('#smGrid .sm').forEach(function(s){function on(){$$('#smGrid .sm').forEach(function(t){t.classList.toggle('on',t===s)});$('#smI').innerHTML='<p class="g">SM'+(+s.dataset.sm+1)+': 텐서 코어 4개(그림 기준)와 자기 L1(H100은 256 KB)을 가진 작업장. 이웃 SM과는 L2를 함께 쓰고, 그 너머 VRAM은 칩 밖이에요.</p>';}
  s.addEventListener('click',on);s.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();on()}})});
/* 3 VRAM 계산기 */
var cV=$('#cFit'),vp=70,vb=2,vg='H100',vn=1;
function drawV(){var W=fit(cV,170),x=cV.getContext('2d');x.clearRect(0,0,W,170);grid(x,W,170);var w=vp*vb,need=w*1.5,cap=G[vg].mem*vn,mx=Math.max(need,cap)*1.1,L0=110,R=W-30;function px(v){return L0+(R-L0)*v/mx}
  x.font='12px '+F;x.textAlign='right';x.fillStyle=C.text;x.fillText('필요한 양',L0-8,48);x.fillText('GPU 메모리',L0-8,112);
  x.fillStyle=C.stain;x.fillRect(L0,32,px(w)-L0,24);x.fillStyle='rgba(155,63,181,.3)';x.fillRect(px(w),32,px(need)-px(w),24);
  x.fillStyle=need<=cap?C.gfp:w<=cap?C.amber:C.eye;x.fillRect(L0,96,px(cap)-L0,24);
  x.strokeStyle=C.text;x.setLineDash([4,3]);x.beginPath();x.moveTo(px(cap),20);x.lineTo(px(cap),132);x.stroke();x.setLineDash([]);
  x.textAlign='left';x.fillStyle=C.text;x.fillText('무게 '+fmtN(w)+' GB',L0+4,26);x.fillText('+ KV 여유 '+fmtN(need-w)+' GB',Math.min(px(w)+4,R-120),70);x.fillText(vn+'장 × '+G[vg].mem+' GB = '+fmtN(cap,0)+' GB',L0+4,138);stamp(x,W,'파라미터 × 바이트 근사');}
function updV(){var w=vp*vb,need=w*1.5,cap=G[vg].mem*vn,st=need<=cap?['여유 있음','g']:w<=cap?['여유 부족 — 느려지거나 OOM','a']:['OOM — 무게도 안 들어감','r'],minN=Math.ceil(need/G[vg].mem);
  L.setTxt('#vPV',vp+'B');L.kpis('#vK',[[fmtN(w)+' GB','모델 무게','m'],[fmtN(need)+' GB','필요 (무게 × 1.5)','a'],[fmtN(cap,0)+' GB','가진 메모리','i'],[st[0],'판정',st[1]]]);
  L.ins('#vI',[[st[1],need<=cap?'올라가고 KV 캐시 자리도 있어요. 긴 문맥 · 큰 배치라면 더 넉넉히.':'경험칙대로라면 '+vg+' 최소 '+minN+'장'+(minN>8?' — 노드 하나(8장)를 넘어요. 노드 사이 연결(7칸)이 필요해요.':'이 필요해요.')],['i','숫자 크기를 줄이면(양자화, 6주차 5.1) 무게가 줄어요. 16 → 8비트면 절반.']]);drawV();}
$('#vP').addEventListener('input',function(){vp=+this.value;updV()});L.bindSeg('#vB',function(v){vb=+v;updV()});L.bindSeg('#vG',function(v){vg=v;updV()});L.bindSeg('#vN',function(v){vn=+v;updV()});L.addMod(cV,function(dt){if(dt===0)drawV()});updV();
/* 4 병목 */
var cB=$('#cBn'),bm=70,bt=8000,bv='dec',bq=1,BG=['L40','H100','H200','B200'];
function dec(g){var w=bm;if(w>G[g].mem)return 0;return Math.min(G[g].bw*1000*bq/w,G[g].fp8*1e12/(2*bm*1e9))}
function fitTxt(g){var w=bm;return w>G[g].mem?'안 들어감':w*1.5>G[g].mem?'여유 부족':''}
function pre(g){return 2*bm*1e9*bt/(G[g].fp8*1e12)}
function drawB(){var W=fit(cB,170),x=cB.getContext('2d');x.clearRect(0,0,W,170);grid(x,W,170);
  if(bv==='dec')hbars(x,W,BG.map(function(g){var v=dec(g),ft=fitTxt(g);return [g,v,!v?C.eye:ft?C.amber:g==='H200'?C.gfp:C.info,v?fmtN(v,0)+' 토큰/초'+(ft?' · '+ft+' ('+fmtN(bm*1.5,0)+' GB 권장 > '+G[g].mem+' GB)':''):'안 들어감 ('+bm+' GB > '+G[g].mem+' GB)']}),{h:24,gap:12,R:250});
  else hbars(x,W,BG.map(function(g){var v=pre(g);return [g,v,C.stain,(v*1000<1000?fmtN(v*1000,0)+' ms':fmtN(v,2)+' 초')]}),{h:24,gap:12});
  stamp(x,W,'설명용 상한 근사 (효율 100%, KV 캐시 무시)');}
function updB(){L.setTxt('#bTV',fmtN(bt,0)+'토큰');var r1=dec('H200')/dec('H100'),r2=pre('H100')/pre('H200'),pr=parseFloat(($('#bPr')||{}).value),kp=[[isFinite(r1)&&dec('H100')?r1.toFixed(2)+'배':'—','H200/H100 디코드','g'],[r2.toFixed(2)+'배','H200/H100 프리필','i'],[fmtN(bm,0)+' GB','FP8 무게','m']];
  if(pr>0){var t=dec('H100');kp.push([t?'$'+fmtN(pr/3600/t*1e6,2):'—','H100 100만 토큰당 비용 하한 (배치 '+bq+')','a']);}
  L.kpis('#bK',kp);var warn=BG.filter(function(g){return fitTxt(g)}).join(' · ');
  L.ins('#bI',[[bv==='dec'?'g':'i',bv==='dec'?'디코드 막대는 대역폭 순서예요(L40 0.864 < H100 3.35 < H200 4.8 < B200 8 TB/s). 배치를 키우면 같은 무게 읽기로 손님 여럿의 토큰을 만들어 합계가 늘어요.':'프리필 막대는 FLOPS 순서예요. H100과 H200은 같은 길이 — 계산력이 같으니까요.'],
    [warn?'r':'g',warn?warn+': 3칸 경험칙(무게 × 1.5)에 못 미치거나 아예 안 들어가요. 실제 서빙은 여러 장으로 나눠야 해요(5.4 병렬화).':'네 GPU 모두 3칸 경험칙(무게 × 1.5)을 만족해요.'],
    ['i',pr>0?'비용 하한 = 시간당 임대료 ÷ (초당 토큰 상한 × 3,600). 실제 효율은 100%가 아니라 이보다 비싸요.':'임대료 칸에 제공사 견적을 넣으면 100만 토큰당 비용 하한이 나와요(기본값은 비워 둠).']]);drawB();}
L.bindSeg('#bM',function(v){bm=+v;updB()});$('#bT').addEventListener('input',function(){bt=+this.value;updB()});L.bindSeg('#bV',function(v){bv=v;updB()});L.bindSeg('#bQ',function(v){bq=+v;updB()});$('#bPr').addEventListener('input',updB);L.addMod(cB,function(dt){if(dt===0)drawB()});updB();
/* 5 세대 연표 */
var cG=$('#cGen'),ga='hopper',ARCH=__ARCH__;
function drawG(){var W=fit(cG,150),x=cG.getContext('2d');x.clearRect(0,0,W,150);grid(x,W,150);var L0=30,R=W-30,y=78;function px(yr){return L0+(R-L0)*(yr-2016)/(2029-2016)}
  x.strokeStyle=C.rule;x.lineWidth=3;x.beginPath();x.moveTo(L0,y);x.lineTo(R,y);x.stroke();x.lineWidth=1;
  ARCH.forEach(function(a,i){var X=px(a.y)+(a.k==='lovelace'?14:a.k==='hopper'?-14:0),on=a.k===ga;x.fillStyle=on?C.gfp:a.f?C.muted:C.info;x.beginPath();x.arc(X,y,on?9:6,0,7);x.fill();
    x.font=(on?'700 ':'')+'12px '+F;x.textAlign='center';x.fillStyle=on?C.gfp:C.text;var up=i%2===0;x.fillText(a.n,X,up?y-18:y+28);x.fillStyle=C.muted;x.fillText(String(a.y)+(a.f?' 예정':''),X,up?y-34:y+44);});
  stamp(x,W,'교재 세대 연표');}
function updG(){var a=ARCH.filter(function(t){return t.k===ga})[0];L.ins('#gI',[[a.f?'a':'g','<b>'+a.n+'</b> ('+a.y+(a.f?' 예정':'')+') — '+a.d],['i',a.g]]);drawG();}
L.bindSeg('#gA',function(v){ga=v;updG()});L.addMod(cG,function(dt){if(dt===0)drawG()});updG();
var cS=$('#cSpec'),sm='fp8',UNIT={fp8:['TF',0],mem:['GB',0],bw:['TB/s',2]};
function drawS(){var W=fit(cS,200),x=cS.getContext('2d');x.clearRect(0,0,W,200);grid(x,W,200);
  hbars(x,W,ORD.map(function(g){var v=G[g][sm];return [g,v,G[g].arch==='블랙웰'?C.gfp:G[g].arch==='호퍼'?C.info:C.amber,(G[g].approx&&sm!=='mem'?'~':'')+fmtN(v,UNIT[sm][1])+' '+UNIT[sm][0]]}),{h:20,gap:8});stamp(x,W,'교재 표 그대로');}
function updS(){var r=G.H200[sm]/G.H100[sm],b=G.B200[sm]/G.H100[sm];L.kpis('#sK',[[r.toFixed(2)+'배','H200 ÷ H100','i'],['~'+b.toFixed(1)+'배','B200 ÷ H100','g']]);
  L.ins('#sI',[['g',sm==='fp8'?'H100 = H200: 같은 세대, 같은 계산력. B200은 약 2.5배.':sm==='mem'?'메모리는 세대 안에서도 커져요(H100 80 → H200 141, B200 192 → B300 288).':'대역폭: L4 0.3 TB/s부터 B200 · B300 최대 8 TB/s까지 — 디코드 속도의 상한을 정해요.'],['a','L4 · L40은 NVLink가 없어 여러 장 묶기에 불리해요.']]);drawS();}
L.bindSeg('#sM',function(v){sm=v;updS()});L.addMod(cS,function(dt){if(dt===0)drawS()});updS();
/* 6 C2C */
var cC=$('#cC2C'),cs=40;function drawC(){var W=fit(cC,120),x=cC.getContext('2d');x.clearRect(0,0,W,120);grid(x,W,120);
  hbars(x,W,[['PCIe (참고값 128)',cs/128,C.amber,fmtN(cs/128*1000,0)+' ms'],['NVLink-C2C (900)',cs/900,C.gfp,fmtN(cs/900*1000,0)+' ms']],{L0:150,h:26,gap:14,T:18,max:cs/128});stamp(x,W,'PCIe 값은 교재 밖 참고값');}
function updC(){L.setTxt('#cSV',cs+' GB');L.kpis('#cK',[[fmtN(cs/128*1000,0)+' ms','표준 연결 (설명용)','a'],[fmtN(cs/900*1000,0)+' ms','Grace NVLink-C2C','g'],[(900/128).toFixed(1)+'배','차이','i']]);
  L.ins('#cI',[['g','CPU 메모리는 GPU 메모리보다 훨씬 커요. 문이 넓으면 그 큰 창고를 보조 창고로 쓸 수 있어요.']]);drawC();}
$('#cS').addEventListener('input',function(){cs=+this.value;updC()});L.addMod(cC,function(dt){if(dt===0)drawC()});updC();
/* 7 연결 */
var cN=$('#cNet'),ns=10,nl='nvb',LINK={nvb:['NVLink 블랙웰',1800,'in'],nvh:['NVLink 호퍼',900,'in'],ib:['InfiniBand 400 Gb/s',50,'out'],eth:['이더넷 100 Gb/s',12.5,'out']},tick=0;
function drawN(){var W=fit(cN,300),x=cN.getContext('2d');x.clearRect(0,0,W,300);grid(x,W,300);var lk=LINK[nl],nw=Math.min(300,(W-80)/2),gx=[30,W-30-nw];
  [0,1].forEach(function(n){var X=gx[n];x.strokeStyle=C.rule;x.strokeRect(X,14,nw,92);x.fillStyle=C.muted;x.font='12px '+F;x.textAlign='left';x.fillText('노드 '+(n+1)+' (GPU 8장 · NVSwitch)',X+6,28);
    for(var g=0;g<8;g++){var cx=X+16+(g%4)*((nw-32)/3),cy=g<4?50:86;x.fillStyle=(lk[2]==='in'&&n===0&&(g===0||g===5))||(lk[2]==='out'&&g===0)?C.gfp:C.info;x.fillRect(cx-10,cy-10,20,16);}});
  var t=(tick%60)/60;x.strokeStyle=lk[2]==='in'?C.gfp:C.amber;x.lineWidth=2;x.beginPath();
  if(lk[2]==='in'){var ax=gx[0]+16,ay=50,bx=gx[0]+16+((nw-32)/3),by=86;x.moveTo(ax,ay);x.lineTo(bx,by);x.stroke();x.fillStyle=x.strokeStyle;x.beginPath();x.arc(ax+(bx-ax)*t,ay+(by-ay)*t,5,0,7);x.fill();}
  else{var ax2=gx[0]+16,bx2=gx[1]+16;x.moveTo(ax2,50);x.lineTo(ax2,112);x.lineTo(bx2,112);x.lineTo(bx2,50);x.stroke();x.fillStyle=x.strokeStyle;var px2=t<.2?[ax2,50+62*t/.2]:t<.8?[ax2+(bx2-ax2)*(t-.2)/.6,112]:[bx2,112-62*(t-.8)/.2];x.beginPath();x.arc(px2[0],px2[1],5,0,7);x.fill();}
  x.lineWidth=1;x.save();x.translate(0,140);var rows=Object.keys(LINK).map(function(k){var v=ns/LINK[k][1];return [LINK[k][0],v*1000,k===nl?C.gfp:'rgba(30,85,200,.45)',v<1?fmtN(v*1000,0)+' ms':fmtN(v,2)+' 초']});
  hbars(x,W,rows,{L0:150,h:22,gap:10,log:true,max:ns/12.5*1000});x.restore();stamp(x,W,'시간 = 크기 ÷ 대역폭 (로그 눈금)');}
function updN(){L.setTxt('#nSV',fmtN(ns,1)+' GB');var lk=LINK[nl],t=ns/lk[1];L.kpis('#nK',[[t<1?fmtN(t*1000,0)+' ms':fmtN(t,2)+' 초',lk[0],lk[2]==='in'?'g':'a'],[fmtN(lk[1],1)+' GB/s','바이트로 환산','i'],[(1800/50).toFixed(0)+'배','NVLink 블랙웰 ÷ InfiniBand','m']]);
  L.ins('#nI',[[lk[2]==='in'?'g':'a',lk[2]==='in'?'노드 안: GPU 8장이 NVLink · NVSwitch로 서로 통해요.':'노드 사이: 초록 길이 노드를 떠나 InfiniBand(또는 이더넷)를 건너요. Gb/s ÷ 8 = GB/s.'],['i','큰 텐서를 자주 주고받는 병렬화는 노드 안에 두는 게 유리해요(5.4 · 5.5).']]);drawN();}
$('#nS').addEventListener('input',function(){ns=+this.value;updN()});L.bindSeg('#nL',function(v){nl=v;updN()});L.addMod(cN,function(dt){tick++;drawN()});updN();
/* 8 MIG */
var cM=$('#cMig'),gz=3,gm=3,gb=2,MEM={1:1,2:2,3:4,4:4,7:8},CNT={1:7,2:3,3:2,4:1,7:1};
function drawM(){var W=fit(cM,210),x=cM.getContext('2d');x.clearRect(0,0,W,210);grid(x,W,210);var L0=110,R=W-20,mw=(R-L0)/8,cw=(R-L0)/7,n=CNT[gz],cols=[C.gfp,C.info,C.stain,C.amber,C.eye,'#0b7a86','#7a3fd6'];
  x.font='12px '+F;x.textAlign='right';x.fillStyle=C.text;x.fillText('메모리 8조각',L0-8,44);x.fillText('계산 7조각',L0-8,112);
  for(var i=0;i<8;i++){var owner=Math.floor(i/MEM[gz]);x.fillStyle=owner<n&&(i<MEM[gz]*n)?cols[owner]:C.panel2;x.fillRect(L0+i*mw+2,28,mw-4,26);x.fillStyle='#fff';x.textAlign='center';if(owner<n&&i<MEM[gz]*n)x.fillText('10GB',L0+i*mw+mw/2,46);}
  for(var j=0;j<7;j++){var ow=Math.floor(j/gz);x.fillStyle=ow<n&&(j<gz*n)?cols[ow]:C.panel2;x.fillRect(L0+j*cw+2,96,cw-4,26);x.fillStyle='#fff';x.textAlign='center';if(ow<n&&j<gz*n)x.fillText('계산',L0+j*cw+cw/2,114);}
  x.textAlign='left';x.fillStyle=C.muted;x.fillText('같은 색 = MIG 인스턴스 하나 · 회색 = 남는 조각',L0,150);x.fillText('SM 132개 ÷ 7 = 18.86… → 같은 크기로 나누고 남는 SM은 쉼',L0,172);stamp(x,W,'프로필 표는 교재 밖 NVIDIA 기준');}
function updM8(){var need=gm*gb*1.5,mem=MEM[gz]*10,n=CNT[gz],ok=need<=mem;L.setTxt('#gMV',gm+'B');
  L.kpis('#gK',[[(gz/7*100).toFixed(0)+'%','계산 비율 (약 '+gz+'/7)','i'],[mem+' GB','메모리','m'],[n+'개','H100 한 장에 띄울 수','g'],[ok?'들어감':'모자람','필요 '+fmtN(need)+' GB',ok?'g':'r']]);
  L.ins('#gI2',[[ok?'g':'r',ok?'이 크기 인스턴스 '+n+'개를 동시에 띄울 수 있어요. 작은 모델이면 GPU 한 장을 통째로 주는 것보다 자원을 잘 써요.':'이 조각에는 안 들어가요. 더 큰 조각을 고르거나 숫자 크기를 줄이세요.'],['i',gz===3?'교재 예: 3조각 = 계산 약 3/7, VRAM 최대 절반(40 GB), CPU · RAM · 저장소 · 네트워크도 약 절반.':'Orpheus TTS(3B)는 16비트로 무게 약 6 GB — 1조각에도 들어가요.']]);drawM();}
L.bindSeg('#gZ',function(v){gz=+v;updM8()});$('#gM').addEventListener('input',function(){gm=+this.value;updM8()});L.bindSeg('#gB',function(v){gb=+v;updM8()});L.addMod(cM,function(dt){if(dt===0)drawM()});updM8();
/* 9 가속기 */
var EK={all:'전체',bw:'메모리 대역폭',pw:'전력 효율',plat:'플랫폼 통합',etc:'기타'};function updA(v){var n=0;$$('#accGrid .card').forEach(function(c){var on=v==='all'||c.dataset.e===v;c.classList.toggle('dim',!on);if(on)n++;});
  L.kpis('#aK',[[n+'곳',EK[v],'g'],['9곳','교재 표 전체','i']]);L.ins('#aI',[['g',v==='bw'?'디코드 병목(대역폭)을 없애 LLM 초당 토큰을 높이는 쪽이에요.':v==='pw'?'전력을 덜 써서 운영비를 낮추는 쪽이에요.':v==='plat'?'자기 클라우드 · 자체 모델과 깊게 엮는 쪽이에요.':v==='etc'?'교재가 세 특기 중 어디에도 묶지 않은 곳이에요.':'모두 NVIDIA에서 추론 일을 가져오려고 특정한 한 수에 걸고 있어요.']]);}
L.bindSeg('#aE',updA);updA('all');
/* 10 로컬 */
var cLc=$('#cLoc'),lp=32,lb=0.5,le=1,DESK=[['RTX 5090',32,1792,5000],['M3 Ultra',512,819,10000]];
function loc(d){var w=lp*lb;return w>d[1]?0:d[2]/(w*le)}
function drawL(){var W=fit(cLc,190),x=cLc.getContext('2d');x.clearRect(0,0,W,190);grid(x,W,190);var w=lp*lb;
  x.font='12px '+F;x.fillStyle=C.muted;x.textAlign='left';x.fillText('메모리에 올라가나 (무게 '+fmtN(w)+' GB)',16,18);
  hbars(x,W,DESK.map(function(d){return [d[0],Math.min(w,d[1])/d[1]*100,w<=d[1]?C.gfp:C.eye,w<=d[1]?'사용 '+fmtN(w/d[1]*100,0)+'% · '+d[1]+' GB':'안 들어감 ('+d[1]+' GB)']}),{L0:110,h:20,gap:8,T:26,max:100});
  x.fillStyle=C.muted;x.fillText('초당 토큰 상한 (배치 1)',16,106);hbars(x,W,DESK.map(function(d){var v=loc(d);return [d[0],v,C.info,v?fmtN(v,0)+' 토큰/초':'0 (올라가지 않음)']}),{L0:110,h:20,gap:8,T:114});stamp(x,W,'대역폭 ÷ 토큰당 읽는 무게 (설명용)');}
function updL(){L.setTxt('#lPV',lp+'B');var a=loc(DESK[0]),b=loc(DESK[1]),win=a>b?'RTX 5090':b>a?'M3 Ultra':'둘 다 불가';
  L.kpis('#lK',[[fmtN(lp*lb)+' GB','모델 무게','m'],[win,'더 빠른 책상',a>b?'i':b>a?'g':'r'],['$5,000 · $10,000','컴퓨터 가격 (교재)','a']]);
  L.ins('#lI',[[a&&b?'i':'a',a&&b?'둘 다 올라가면 대역폭이 두 배 넘는 RTX 5090이 빨라요.':!a&&b?'RTX 5090(32 GB)엔 안 올라가요. 느려도 512 GB인 M3 Ultra만 돌릴 수 있어요.':'둘 다 안 올라가요. 양자화를 세게 하거나 더 작은 모델을 고르세요.'],['g',le<1?'MoE: 메모리엔 전체 무게가 다 있어야 하지만, 토큰마다 읽는 건 활성 부분뿐이라 속도 상한이 크게 올라가요.':'밀집 모델은 토큰마다 무게 전체를 읽어요.']]);drawL();}
$('#lP').addEventListener('input',function(){lp=+this.value;updL()});L.bindSeg('#lB',function(v){lb=+v;updL()});L.bindSeg('#lE',function(v){le=+v;updL()});L.addMod(cLc,function(dt){if(dt===0)drawL()});updL();
/* 대결 */
L.Duel({fmt:function(v){return v.toFixed(1)+' 토큰/초'},run:function(){var w=35,f=819/w,r=w>32?0:1792/w;
  return {fly:f,robo:r,res:'F',bars:[['f','초파리 · M3 Ultra (819 ÷ 35)',f],['r','주판봇 · RTX 5090 (35 GB > 32 GB)',r]],asst:'무게 35 GB는 RTX 5090의 32 GB를 넘어서 올라가지 않아요. M3 Ultra는 819 ÷ 35 ≈ 23.4 토큰/초가 상한이에요.',
  verdict:'들어가야 돌린다. 이번 판은 초파리 승.',note:'모델이 32 GB 안에 들어가는 크기(예: 8B · 4비트)였다면 대역폭 2.2배인 RTX 5090이 이겨요. 10칸 계산기에서 크기를 바꿔 보세요. (설명용 상한 근사)'};}});
'''.replace('__GPU__', _j.dumps({
    'H100': {'fp8': 1979, 'mem': 80, 'bw': 3.35, 'arch': '호퍼', 'fp4': False}, 'H200': {'fp8': 1979, 'mem': 141, 'bw': 4.8, 'arch': '호퍼', 'fp4': False},
    'L4': {'fp8': 242, 'mem': 24, 'bw': 0.3, 'arch': '러브레이스', 'fp4': False}, 'L40': {'fp8': 362, 'mem': 48, 'bw': 0.864, 'arch': '러브레이스', 'fp4': False},
    'B200': {'fp8': 5000, 'mem': 192, 'bw': 8, 'arch': '블랙웰', 'fp4': True, 'approx': True}, 'B300': {'fp8': 5000, 'mem': 288, 'bw': 8, 'arch': '블랙웰', 'fp4': True, 'approx': True}}, ensure_ascii=False)).replace('__ARCH__', _j.dumps([
    {'k': 'volta', 'n': '볼타', 'y': 2017, 'd': '최근 연표의 첫 세대.', 'g': '추론 엔지니어가 지금 쓰는 범위(최근 3~5세대) 밖이에요.'},
    {'k': 'turing', 'n': '튜링', 'y': 2018, 'd': 'T4.', 'g': '저트래픽 · 레거시 시스템에서 가끔 보여요.'},
    {'k': 'ampere', 'n': '암페어', 'y': 2020, 'd': 'A10 · A100. A100은 PCIe형과 SXM형(대역폭 5% 높음)이 있어요.', 'g': 'H100이 A100을 직접 대체했어요. 레거시에서 가끔.'},
    {'k': 'hopper', 'n': '호퍼', 'y': 2022, 'd': 'H100(2022.3) · H200. FP8, 4세대 텐서 코어, 비동기 전송 → FlashAttention 3. NVLink 900 GB/s.', 'g': '새롭고 빠르면서 업계 지원·최적화 커널이 갖춰져 가장 널리 쓰여요.'},
    {'k': 'lovelace', 'n': '러브레이스', 'y': 2022, 'd': 'L4 · L40. 호퍼 6개월 뒤, 그래픽 쪽 짝. FP8 지원, NVLink 없음.', 'g': 'L4는 작은 모델에 싸고 편하지만, L40은 추론에 대체로 좋은 선택이 아니에요.'},
    {'k': 'blackwell', 'n': '블랙웰', 'y': 2024, 'd': 'B200(2024.11) · B300. FP4 + MXFP8 · MXFP4 · NVFP4, NVLink 1,800 GB/s, FlashAttention 4.', 'g': '추론의 새 금본위 — LLM과 영상 생성 같은 무거운 일에 최고 성능.'},
    {'k': 'rubin', 'n': '루빈', 'y': 2026, 'f': True, 'd': 'HBM4(대역폭 일에 이득), 프리필 같은 계산 일 전용 칩 CPX, Vera CPU.', 'g': '실측 벤치마크가 나올 때까지 판단을 미루세요. 소프트웨어가 따라오는 데 1년쯤.'},
    {'k': 'feynman', 'n': '파인만', 'y': 2028, 'f': True, 'd': '알려진 것이 적어요. 더 크고 강한 칩, 더 빠른 메모리 구조가 될 가능성.', 'g': '교재 출간 시점 기준 정보예요.'}], ensure_ascii=False))

def spec():
    return {'meta': {'title': 'GPU 기계실 — 3장 하드웨어 (인퍼런스 스터디 북 4주차 교재 연구실 해설)', 'description': '인퍼런스 스터디 북 4주차 교재: Inference Engineering 3장 하드웨어 — SM과 텐서 코어, VRAM과 대역폭, GPU 세대, 인스턴스와 NVLink, MIG, 다른 가속기, 로컬 추론',
                     'series': '인퍼런스 스터디 북', 'number': '04-3', 'slug': 'ch03-hardware', 'version': '1.0', 'date': '2026-11-14', 'creator': ['안상선'], 'license': 'CC BY-NC 4.0 (캐릭터 제외)', 'url': URL,
                     'kgStart': 'lab:concept/vram', 'citeKey': 'ahn2026ch03hardware', 'domain': 'ai',
                     'suggestedCitation': '안상선 (2026). GPU 기계실 — 3장 하드웨어. 인퍼런스 스터디 북 4주차 교재 해설. ' + URL},
            'kg': KG, 'refs': REFS, 'gl': GL, 'core': CORE, 'quiz': QUIZ, 'js': JS, 'css': LIGHT,
            'nav': nav([('cast', '식구'), ('lv1', '1 자리'), ('lv2', '2 연산'), ('lv3', '3 메모리'), ('lv4', '4 숫자'), ('lv5', '5 세대'), ('lv6', '6 CPU'), ('lv7', '7 인스턴스'), ('lv8', '8 MIG'), ('lv9', '9 가속기'), ('lv10', '10 로컬'), ('duel', '대결'), ('reread', '다시 읽기'), ('sum', '한 장'), ('teach', '강의자'), ('kg', '색인'), ('export', '꾸러미')]),
            'body': cover('cover_ch03', '인퍼런스 스터디 북 · 4주차 · 교재 3장', '연구실 식구 여섯이 GPU 랙과 메모리 탑이 있는 기계실에 모인 대체 표지',
                          motif=''.join('<i class="%s"></i>' % c for c in ['on', 'on', 'on', 'on', 'm', 'm', 'a', 'on', 'on', 'on', 'on', 'on']),
                          moods={'doc': 'board', 'asst': 'report', 'fly': 'magnify', 'robo': 'calc', 'sia': 'explain', 'moa': 'report'})
                    + hero + cast + lv1 + lv2 + lv3 + lv4 + lv5 + lv6 + lv7 + lv8 + lv9 + lv10 + duel_sec + reread + onepage + outro + teach_appendix(QUIZ, {k: '%s칸' % k[2:] for k in QUIZ}),
            'footer': footer([('교재', 'Kiely, P. (2026). Inference Engineering. Baseten Books. Chapter 3 Hardware (3.1–3.5)'), ('GPU 표', '교재 3.2.1–3.2.3 표 (원문 그대로)'), ('데스크톱 표', '교재 3.5.1 RTX 5090 vs M3 Ultra (원문 그대로)'),
                              ('가속기 표', '교재 3.4 표'), ('교재 밖 참고값', 'PCIe 5.0 x16 양방향 약 128 GB/s(6칸), NVIDIA H100 MIG 프로필 표(8칸)')],
                             ['1칸 자리 판단표', '2칸 FP16 · FP4 · 희소 막대(교재 규칙 계산)', '4 · 10칸 토큰 속도 상한과 프리필 시간 하한(효율 100% 근사)', '7칸 전송 시간(크기 ÷ 대역폭)', '대결 판정 공식'],
                             prev=('../week_03_article_01/', '3주차 논문 FlashAttention'), nxt=('../week_04_article_01/', '4주차 논문 루프라인'), ver='v1.14 (낮의 연구실)')}

if __name__ == '__main__':
    out = os.path.join(sys.argv[1], SLUG, 'index.html')
    print(out, build(spec(), out))
