# -*- coding: utf-8 -*-
import os, sys, json as _j
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import *
from parts import *
from series import BASE

SLUG = 'week_01_article_01'; P = 'livebench'; URL = BASE + SLUG + '/'
SRC = 'white2025livebench'

hero = '''<header class="hero" id="top"><div class="wrap"><div class="hero-text">
<p class="eyebrow">인퍼런스 스터디 북 · 1주차 논문 · ICLR 2025</p>
<h1>라이브벤치 — 새 시험지로만 재는 성적표</h1>
<p class="q">시험지가 이미 인터넷에 풀려 있다면, 그 점수는 실력일까 암기일까?</p>
<p>LLM 벤치마크는 공개되는 순간 다음 모델의 학습 데이터에 섞여 들어갑니다(<b>시험지 유출</b> = 테스트셋 오염). 그렇다고 사람이나 LLM이 채점하게 하면 취향과 편향이 끼고, 어려운 문제에서는 채점이 무너집니다. 이 논문은 <b>매달 새로 만든 문제</b>를 <b>객관적인 정답으로 자동 채점</b>하는 벤치마크를 제안합니다.</p>
<div class="kpis" id="heroK"></div>
<p class="cite">White, C., Dooley, S., Roberts, M., Pal, A., 외 (2025). <i>LiveBench: A Challenging, Contamination-Limited LLM Benchmark</i>. ICLR 2025. arXiv:2406.19314v2. <span class="chip-src">원문</span> 칩은 논문 수치 그대로입니다.</p>
<div class="dialog">''' + say('doc', 'think', '1장에서 "벤치마크는 포화되거나 조작될 수 있다"고 했죠. 이 논문은 그 문제를 정면으로 고치려는 시도예요.') + say('asst', 'smile', '논문의 표 1, 표 8·9, 그림 2를 직접 돌려 볼게요. 숫자는 원문 그대로 옮겼어요.') + say('fly', 'point', '문제를 매달 바꾸면 순위도 매달 춤추는 거 아냐? 그럼 비교가 안 되잖아.') + say('robo', 'chart', '점수는 점수지! 높은 점수가 나온 모델에 거는 게 정답이야.') + say('sia', 'explain', '논문 순서대로 갑니다. 질문 → 방법 → 결과 셋 → 모형 실험실 → 대결 → 다시 읽기.') + say('moa', 'report', '어려운 이름은 별명으로 불러요. 아래 별명 카드를 먼저 봐 주세요!') + '''</div></div></div></header>'''

NICK = [('시험지 유출', 'test set contamination', '벤치마크 문제가 새 모델의 학습 데이터에 섞여 점수가 부풀려지는 일'),
        ('채점 로봇', 'LLM-as-a-judge', 'LLM이 다른 LLM의 답을 채점하는 방식. 빠르지만 편향·실수'),
        ('정답지 채점', 'ground-truth scoring', '객관적인 정답과 맞춰 자동으로 채점'),
        ('라이브벤치', 'LiveBench', '매달 새 문제를 더하고 정답으로 채점하는 이 논문의 벤치마크'),
        ('여섯 과목', '6 categories', '수학·코딩·추론·언어·지시 따르기·데이터 분석 (과제 18개)'),
        ('사람 판정 무대', 'ChatBot Arena', '사람이 두 모델 답 중 나은 쪽을 고르는 공개 비교판')]
nick = '<h3>논문 속 용어 별명</h3><div class="nick">' + ''.join('<div class="card"><b>%s</b><div class="orig">%s</div><p style="margin:4px 0 0;font-size:14px">%s</p></div>' % n for n in NICK) + '</div>'
cast = crew({'doc': '해설·심판', 'asst': '원문 수치 발표', 'fly': '"매달 바꾸면 순위가 흔들려"를 의심', 'robo': '"점수가 곧 실력"을 믿는 쪽', 'sia': '논문 순서 안내·진행 신호', 'moa': '별명 카드·기록장', 'x1': '방청석', 'x2': '방청석', 'x3': '방청석'},
            extra=nick + '<h3>오늘의 순서</h3>' + route([('q', '1', '질문'), ('method', '2', '방법'), ('r1', '결과 ①', '유출을 막는 교체'), ('r2', '결과 ②', '채점 로봇의 실수'), ('r3', '결과 ③', '여섯 과목 성적표'), ('lab', '실험실', '벤치마크 만들기'), ('duel', '대결', '순위는 흔들릴까'), ('reread', '다시 읽기', '추론 엔지니어에게')]))

q = section('q', 1, '질문 — 공개된 시험지의 점수를 믿을 수 있나', '''
<div class="turn"><div class="card"><h4>기존 생각</h4><p>좋은 벤치마크 하나를 공개해 두고 모든 모델을 같은 문제로 재면 공정하다.</p></div><div class="arrow">→</div><div class="card"><h4>이 논문</h4><p>공개된 문제는 인터넷을 거쳐 <b>학습 데이터에 섞인다</b>. 사람·LLM 채점은 <b>편향</b>되고 어려운 문제에서 <b>틀린다</b>. 그러니 새 문제 + 객관 정답 + 다양한 과목이 필요하다.</p></div></div>
<div class="timeline"><div class="st"><b>증거 1</b>코드포스 문제 성적이 모델의 학습 마감일 <b>이후</b> 문제에서 뚝 떨어진다</div><div class="st"><b>증거 2</b>마감일 이전에는 문제가 깃허브에 나온 횟수와 성적이 강하게 비례</div><div class="st"><b>증거 3</b>GSM8K를 손으로 다시 만든 변형판에서 여러 모델이 과적합 흔적</div><div class="st"><b>대안의 문제</b>LLM 채점관은 자기 답·긴 답을 선호, 사람은 형식·말투에 끌림</div></div>
<p class="muted" style="font-size:14px">1장 도입부와 관련 연구(Roberts 외 2024, Jain 외 2024, Zhang 외 2024, Li 외 2024)를 정리 <span class="chip-src">원문</span></p>
''' + say('fly', 'magnify', '마감일 뒤 문제에서만 점수가 떨어진다면… 실력보다 기억이었다는 거네.') + '<div class="quiz" data-quiz="q"></div>', small='질문', tags=[('g', '논문: 1장')])

PIPE = [('출처 고르기', '최근 수학 대회(지난 11개월), arXiv 초록, 가디언 기사, 캐글·소크라타 데이터, 최근 영화 줄거리 같은 <b>새 정보원</b>. 또는 BBH·AMPS·IFEval 과제의 더 어렵고 다양한 변형.'),
        ('문제 만들기', '과제마다 40~100문항, 쉬운 것부터 아주 어려운 것까지. 최상위 모델 정답률이 대략 30~70%가 되도록.'),
        ('객관 정답만', '정답이 객관적으로 정해진 문제만 넣는다. 그래서 채점에 LLM 판정관이 필요 없다.'),
        ('자동 채점', '문항마다 0~1점. 과제 점수 = 문항 평균, 과목 점수 = 과제 평균, 라이브벤치 점수 = 여섯 과목 평균. 온도 0, 한 턴 평가.'),
        ('매달 교체', '업데이트마다 평균 1/6을 바꿔 약 6개월에 전부 새로워진다. 새 문제는 한 달 뒤에 공개해서 공개 순위표에는 늘 1/6의 비공개 문제가 있다.'),
        ('공개', '모든 문제·코드·모델 답을 공개한다. 순위표는 40~50개 모델로 유지.')]
method = section('method', 2, '방법 — 라이브벤치를 만드는 여섯 단계', '<div class="pipe" id="pipe">' + ''.join('<button class="bt" data-p="%d" aria-pressed="%s">%d · %s</button>' % (i, 'true' if i == 0 else 'false', i + 1, p[0]) for i, p in enumerate(PIPE)) + '</div><div class="panel pipeout" id="pipeOut" aria-live="polite"></div>'
    + '<div class="bridge gen"><h4>추론 실무에서 비슷한 작업</h4><p>양자화·추측 디코딩처럼 품질을 떨어뜨릴 수 있는 최적화 전후를, 사내 평가셋(정답 있는 문제)으로 자동 채점해 비교하는 일과 같은 구조예요(1장 1.3.1 "기준선").</p><p class="lim">비유의 한계: 사내 평가셋은 매달 바꿀 필요가 없지만, 외부에 공개하면 같은 유출 문제가 생겨요.</p></div>'
    + say('sia', 'guide', '여섯 단계를 차례로 눌러 보세요. 다섯 번째 "매달 교체"가 이 논문의 이름(라이브)이 된 이유예요.') + '<div class="quiz" data-quiz="method"></div>', small='방법', tags=[('g', '논문: 2장, 2.7절, 3장')])

r1 = level('①', 'r1', '결과 ① — 매달 1/6을 바꾸면 유출이 따라오지 못한다', [('g', '모델: 월간 교체'), ('p', '논문: 2.7절, 3.4절')],
    pair=('연구실에서는', '실험실 출입 시험 문제를 매달 1/6씩 바꾸고, 새 문제는 한 달 동안 공개하지 않으면, 기출을 외운 사람의 이득이 계속 줄어요.', '모델에서는', '업데이트마다 평균 <b>1/6 교체</b> → 약 <b>6개월에 전부 새로</b>. 두 번의 업데이트 뒤 순위 상관은 <b>0.997 초과</b>, 평균 점수는 약 <b>1.2% 하락</b> — 순위는 그대로이면서 시험은 조금씩 어려워졌어요 <span class="chip-src">원문</span>.'),
    panel=panel('외운 문제 비율 시뮬레이터', 'cLeak', '달마다 새 문제가 섞이면서, 모델이 학습 중에 본(유출된) 문제의 비율이 줄어드는 모습. 유출 속도는 설명용입니다.',
                ctrl=slider('kM', '지난 달', 0, 12, 1, 3, '개월') + slider('kR', '한 번에 교체', 0, 0.5, 0.0417, 0.1667, '') + btn_group('kP', '새 문제 비공개 1개월', [('1', '함'), ('0', '안 함')]), kp_id='kK', ins_id='kI'),
    explain=explain('풀이', ['공개된 문제는 시간이 지나면 다음 모델 학습에 섞일 수 있다고 가정해요(설명용으로 공개 후 매달 일정 비율이 유출).', '교체 비율 1/6(≈0.167)이면 6개월쯤 지나 처음 문제는 거의 다 바뀌어요.', '새 문제를 한 달 늦게 공개하면, 공개 순위표의 1/6은 늘 아무도 못 본 문제예요.'],
                    limit='유출 속도 상수는 논문 값이 아니라 설명용이에요. 논문은 "언제 어떻게 유출되는지"를 재지 않고, 유출을 줄이는 설계를 제안합니다. 또 교체하려면 매달 사람과 계산이 들어요(논문 2.7 "지속 방안").'),
    talk=say('robo', 'calc', '순위 상관 0.997 초과라고? 문제를 바꿔도 줄 세우기는 거의 그대로네. 이건 내가 맞았지!'))

T8 = {'models': ['GPT-4-Turbo', 'Claude-3-Opus'], 'tasks': ['AMC12 2024', 'AIME 2024', 'SMC 2023', 'Zebra Puzzles'],
      'err': [[0.380, 0.214, 0.353, 0.420], [0.388, 0.103, 0.294, 0.460]],
      'gt': [[54, 13.793, 70.588, 38], [56, 6.897, 58.824, 34]], 'jd': [[64.000, 35.714, 58.824, 68], [42.857, 17.241, 52.941, 52]]}
r2 = level('②', 'r2', '결과 ② — 채점 로봇은 어려운 문제에서 크게 틀린다', [('g', '모델: 정답지 채점 vs 채점 로봇'), ('p', '논문: 부록 표 8·9')],
    pair=('연구실에서는', '자기도 못 푸는 문제를 채점하는 조교는, 그럴듯한 풀이에 점수를 주고 맞는 풀이를 틀렸다고 하기도 해요.', '모델에서는', 'GPT-4-Turbo를 채점 로봇으로 쓰자 오류율이 <b>0.103~0.460</b>. 같은 답안인데 AIME 2024에서 GPT-4-Turbo의 점수가 정답 채점 <b>13.793</b> → 로봇 채점 <b>35.714</b>로 부풀었어요 <span class="chip-src">원문</span>.'),
    panel=panel('같은 답안, 두 채점 방식', 'cJudge', '표 9의 정답 채점(GT)과 LLM 판정(LLM-Jdg.) 점수를 과제별 막대로 비교. 모든 값은 원문.',
                ctrl=btn_group('jM', '답안 쓴 모델', [('0', 'GPT-4-Turbo'), ('1', 'Claude-3-Opus')]) + btn_group('jV', '보기', [('score', '점수 비교 (표 9)'), ('err', '채점 오류율 (표 8)')]), kp_id='jK', ins_id='jI'),
    explain=explain('풀이', ['채점 로봇은 GPT-4-Turbo(2024-04-09). 답안은 GPT-4-Turbo와 Claude-3-Opus가 썼어요.', '모든 과제에서 오류율이 "합리적인 수준보다 훨씬 높다"고 논문은 결론 내려요. 어려운 수학·논리 과제에 LLM 판정관은 맞지 않는다는 거예요.', '부풀기도 하고(AIME, Zebra) 깎이기도 해요(SMC, Claude의 AMC). 방향이 일정하지 않아 보정하기도 어려워요.'],
                    limit='예비 실험이고 채점 로봇은 한 모델뿐이에요. 열린 질문(글쓰기 등)처럼 정답이 없는 일에는 여전히 사람·LLM 판정이 필요해요 — 라이브벤치는 그런 과제를 넣지 않는 대신 범위가 좁아져요.'),
    bridge=bridge(gen=('챗봇 품질을 다른 LLM에게 채점시키는 "LLM 판정"은 빠르고 싸지만, 어려운 추론 문제에서는 정답 기반 검사를 함께 둬야 해요.', '정답이 없는 문제는 이 방법으로 못 잽니다.'),
                  field=('사내 평가에서 "코드가 실제로 돌아가나", "SQL 결과가 맞나"처럼 실행해서 확인할 수 있는 채점이 가장 믿을 만해요.', '실행 환경을 만드는 비용이 들어요.')),
    talk=say('asst', 'report', 'AIME에서 GPT-4-Turbo 답안: 정답 채점 13.793점, 로봇 채점 35.714점이에요. 두 배 반 넘게 부풀었어요.'))

T1 = [['o1-preview-2024-09-12', 64.7, 50.8, 64.0, 74.6, 68.7, 62.9, 67.4], ['claude-3-5-sonnet-20241022', 58.5, 67.1, 52.8, 69.3, 53.8, 51.3, 56.7], ['claude-3-5-sonnet-20240620', 58.2, 60.8, 56.7, 68.0, 53.2, 53.3, 57.2],
      ['o1-mini-2024-09-12', 56.7, 48.1, 54.1, 65.4, 40.9, 59.2, 72.3], ['gemini-exp-1114', 56.0, 52.4, 57.5, 77.1, 38.7, 54.9, 55.7], ['gemini-exp-1121', 56.0, 50.4, 57.0, 80.1, 40.0, 62.8, 45.8],
      ['step-2-16k-202411', 55.1, 46.9, 54.9, 79.9, 44.5, 48.9, 55.5], ['gpt-4o-2024-08-06', 53.8, 51.4, 52.9, 68.6, 47.6, 48.2, 53.9], ['gemini-1.5-pro-002', 53.4, 48.8, 52.3, 70.8, 43.3, 57.4, 47.9],
      ['gpt-4o-2024-05-13', 52.6, 49.4, 52.4, 68.2, 50.0, 46.0, 49.6], ['gemini-1.5-pro-exp-0827', 52.4, 40.9, 50.8, 69.3, 46.1, 56.1, 50.9], ['meta-llama-3.1-405b-instruct-turbo', 51.1, 43.8, 53.5, 72.8, 43.2, 40.5, 52.8],
      ['gpt-4o-2024-11-20', 50.6, 46.1, 47.2, 64.9, 47.4, 42.5, 55.7], ['dracarys2-72b-instruct', 50.1, 56.6, 49.1, 65.2, 33.5, 50.6, 45.8], ['chatgpt-4o-latest-0903', 50.1, 47.4, 48.7, 66.4, 45.3, 42.1, 50.5]]
r3 = level('③', 'r3', '결과 ③ — 여섯 과목 성적표, 과목마다 1등이 다르다', [('g', '모델: 과목별 점수'), ('p', '논문: 표 1, 그림 1·2, 3.3절')],
    pair=('연구실에서는', '종합 1등 학생이 모든 과목 1등은 아니에요. 진로를 정할 땐 내가 쓸 과목 점수를 봐야 해요.', '모델에서는', '종합 1위 o1-preview는 <b>64.7점</b>(70% 미만) — 그런데 코딩 1위는 claude-3-5-sonnet-20241022(<b>67.1</b>), 추론 1위는 o1-mini(<b>72.3</b>), 지시 따르기 1위는 gemini-exp-1121(<b>80.1</b>) <span class="chip-src">원문</span>.'),
    panel=panel('표 1 상위 15개 모델 — 과목을 골라 줄 세우기', 'cBoard', '선택한 과목의 점수로 상위 15개 모델을 줄 세운 막대 그래프. 값은 논문 표 1 그대로.',
                ctrl=btn_group('bC', '과목', [('1', '종합'), ('2', '코딩'), ('3', '데이터 분석'), ('4', '지시 따르기'), ('5', '언어'), ('6', '수학'), ('7', '추론')]), kp_id='bK', ins_id='bI', wide=True),
    explain=explain('풀이', ['문항 0~1점 → 과제 평균 → 과목 평균 → 여섯 과목 평균 = 라이브벤치 점수.', '수학·코딩·추론은 서로 상관이 높고, 언어는 데이터 분석과 꽤 상관이 있어요(둘 다 프롬프트 큰 부분을 고쳐 다시 쓰는 과제). 지시 따르기는 다른 과목과 상관이 약해요(그림 2).', '사람 판정 무대(ChatBot Arena)와의 상관은 <b>0.91</b>, Arena-Hard와는 <b>0.88</b>. 큰 흐름은 같지만, GPT-4를 판정관으로 쓰는 Arena-Hard에서 GPT-4 계열이 더 높게 나오는 등 판정 편향의 흔적이 보여요.'],
                    limit='표 1은 2024년 11월 무렵 모델들이에요. 순위표는 매달 바뀌므로, 지금 모델 비교에는 최신 순위표를 보세요(이 해설은 논문 v2 기준).'),
    talk=say('fly', 'point', '종합 1등을 골랐는데 우리 서비스가 코딩 도우미면? 코딩 칸을 눌러 봐. 순서가 꽤 바뀌지.'))

lab = section('lab', '실험실', '모형 실험실 — 벤치마크를 직접 설계해 보기', '''
<p>세 가상 모델(실력이 정해져 있음)을 내가 만든 벤치마크로 잽니다. 장치를 하나씩 켜고 끄며 <b>측정 점수가 진짜 실력에 얼마나 가까운지</b> 봅니다. 모든 값은 시드 고정 설명용입니다.</p>''' + panel('장치 켜고 끄기', 'cLab', '세 가상 모델의 진짜 실력(점선)과 측정 점수(막대). 장치를 켜면 측정이 진짜 실력에 가까워집니다.',
    ctrl=btn_group('xF', '새 문제', [('0', '끔 (공개 문제 그대로)'), ('1', '켬')]) + btn_group('xG', '채점', [('judge', '채점 로봇'), ('gt', '정답지')]) + btn_group('xD', '과목', [('1', '한 과목'), ('6', '여섯 과목')]), kp_id='xK', ins_id='xI')
    + say('moa', 'think', '셋 다 켜면 측정 순위가 진짜 순위와 같아져요. 라이브벤치가 세 가지를 한꺼번에 하는 이유예요!') + '<div class="quiz" data-quiz="lab"></div>', small='모형', tags=[('g', '설명용 모형')])

duel_sec = section('duel', 'VS', '대결 — 문제를 바꾸면 순위가 흔들릴까?', say('doc', 'think', '초파리는 "매달 문제를 바꾸면 순위가 춤춘다"고, 주판봇은 "실력 순서는 그대로"라고 해요. 논문 3.4절의 두 업데이트 결과로 판정합니다.') + duel(
    '업데이트 전후 모델 순위의 순위 상관이 0.9를 넘을까?', '아니다 — 문제를 1/6씩 바꾸면 순위가 크게 흔들린다', '새 문제에서 진짜 실력이 드러나면 순서가 바뀔걸.', '그렇다 — 순위는 거의 그대로다', '실력은 문제를 바꿔도 실력이지. 줄 세우기는 안 변해!') + '<p class="notice">판정 기준: 논문 3.4절 "원판↔1차, 1차↔2차 업데이트의 순위 상관이 모두 0.997 초과" <span class="chip-src">원문</span>. 막대는 "순위가 그대로인 정도"(순위 상관 하한)예요.</p>', small='판', tags=[('g', '판정 기준: 순위 상관')])

reread = section('reread', '다시', '다시 읽기 — 추론 엔지니어에게 라이브벤치란', '''
<div class="cards"><div class="card"><h4>시험지 유출 ↔ 1장 굿하트의 법칙</h4><p>측정이 목표가 되면 측정이 망가진다. 라이브벤치는 시험지를 계속 바꿔 목표가 되기 어렵게 만든다.</p><p class="lim">한계: 바꾸는 일 자체에 비용이 든다.</p></div>
<div class="card"><h4>정답지 채점 ↔ 최적화 기준선</h4><p>양자화·추측 디코딩 전후 품질 비교는 정답 있는 평가로 자동 채점해야 흔들리지 않는다.</p><p class="lim">한계: 정답 없는 생성 품질은 따로 재야 한다.</p></div>
<div class="card"><h4>과목별 1등 ↔ 1장 모델 고르기</h4><p>"종합 1등"이 아니라 "우리 과제에서 충분히 똑똑한 가장 작은 모델"을 고른다.</p><p class="lim">한계: 공개 과목이 우리 과제와 같지는 않다.</p></div>
<div class="card"><h4>40~50개 모델 유지 ↔ 계산 예산</h4><p>매달 최대 50개 모델 × 200문항을 다시 돌린다 — 평가에도 추론 비용이 든다.</p><p class="lim">한계: 커뮤니티 기여에 기대는 부분이 있다.</p></div></div>
<div class="eq">라이브벤치 점수 = 평균<sub>과목 6</sub>( 평균<sub>과제</sub>( 평균<sub>문항</sub>( <b>0~1점</b> ) ) ) &nbsp;·&nbsp; 교체: 업데이트마다 <i>1/6</i>, 약 <i>6개월</i>에 전부</div>
''' + say('asst', 'report', '추론 쪽으로 옮기면: 최적화 전후 품질을 "사내 라이브벤치"로 재세요. 정답 있는 문제로, 주기적으로 새 문제를 섞어서요.'), small='다시', tags=[('g', '1장과 연결')])

onepage = section('sum', '한 장', '한 장으로', '''
<div class="tw"><table class="tb"><tr><th>무엇</th><th>논문 수치</th></tr>
<tr><td>규모</td><td class="n">6과목 18과제, 업데이트 뒤 1,000문항, 40개 모델(0.5B ~ 405B)</td></tr>
<tr><td>난이도</td><td class="n">최고 모델도 70% 미만 (o1-preview 64.7)</td></tr>
<tr><td>교체</td><td class="n">업데이트마다 평균 1/6, 약 6개월에 전부, 새 문제 한 달 비공개</td></tr>
<tr><td>안정성</td><td class="n">업데이트 전후 순위 상관 0.997 초과, 평균 점수 약 1.2% 하락</td></tr>
<tr><td>다른 벤치마크와 상관</td><td class="n">ChatBot Arena 0.91, Arena-Hard 0.88</td></tr>
<tr><td>채점 로봇 오류율</td><td class="n">0.103 ~ 0.460 (AMC12·AIME·SMC·Zebra)</td></tr></table></div>
<div class="notebook"><h4>모아의 기록장 — 읽을 때 주의할 점</h4><ul><li>정답이 있는 과제만 다룬다 → 글쓰기 품질 같은 열린 과제는 범위 밖</li><li>문제 해석(정답 추출)에도 지시 따르기 능력이 조금 섞인다고 논문이 스스로 밝힘(부록 A.4)</li><li>표의 모델들은 2024년 말 기준</li></ul></div>
''' + say('moa', 'ok', '핵심 세 줄: 새 문제 · 정답 채점 · 여섯 과목. 기록 완료!'), small='끝', tags=[('g', '요약')])

outro = section('outro', '끝', '아웃트로', '<div class="outro"><div class="scene" data-img="sc_lb_outro" role="img" aria-label="연구실 식구 여섯이 매달 바뀌는 시험지 게시판 앞에 모인 장면"><img data-who="robo" data-mood="happy" alt=""><img data-who="doc" data-mood="magic" alt=""><img data-who="asst" data-mood="spark" alt=""><img data-who="sia" data-mood="proud" alt=""><img data-who="moa" data-mood="sparkle" alt=""><img data-who="fly" data-mood="coffee" alt=""></div></div>'
    + say('doc', 'magic', '논문의 한 줄: 시험지는 <b>새로</b>, 채점은 <b>정답으로</b>, 과목은 <b>넓게</b> — 그래야 점수가 실력을 말한다.')
    + say('robo', 'happy', '순위는 0.997! 실력은 문제를 바꿔도 실력이었지. 다음에도 여기에 투자.')
    + say('fly', 'coffee', '…순위는 안 흔들렸어도 평균 점수는 1.2% 떨어졌잖아. 시험이 어려워지는 건 맞았어. 그건 인정.')
    + say('asst', 'spark', '1주차 끝! 2주차는 2장 "모델"과 트랜스포머 논문이에요.'), small='', tags=())

GL = {'시험지 유출': ['시험지 유출 = 테스트셋 오염 (test set contamination)', '개념', '벤치마크 문제가 새 모델의 학습 데이터에 들어가 점수가 부풀려지는 일.'],
      '채점 로봇': ['채점 로봇 = LLM 판정관 (LLM-as-a-judge)', '방법', 'LLM이 다른 LLM의 답을 채점. 빠르지만 자기 답·긴 답 선호 등 편향과 실수.'],
      '정답지 채점': ['정답지 채점 (ground-truth scoring)', '방법', '객관적 정답과 맞춰 자동 채점. 판정관이 필요 없다.'],
      '벤치마크': ['벤치마크 (benchmark)', '평가', '여러 모델을 같은 문제로 재는 공통 시험.'], '순위 상관': ['순위 상관 (rank correlation)', '통계', '두 순위표가 얼마나 같은 순서인지. 1이면 완전히 같다.'],
      '학습 마감일': ['학습 마감일 (training cutoff)', '용어', '모델이 학습한 데이터의 마지막 날짜. 그 뒤 정보는 모른다.'], '과적합': ['과적합 (overfitting)', '개념', '시험 문제를 외워서 새 문제에서는 성적이 떨어지는 상태.'],
      '상관': ['상관 계수 (Pearson correlation)', '통계', '두 점수가 함께 오르내리는 정도. −1~1.'], '온도 0': ['온도 0 (temperature 0)', '설정', '가장 확률 높은 토큰만 고르게 해서 같은 입력에 같은 답이 나오게 하는 설정.'],
      'BBH': ['BBH (Big-Bench Hard)', '벤치마크', '어려운 추론 과제 모음. 라이브벤치는 그중 Web of Lies를 더 어렵게 만듦.'], 'IFEval': ['IFEval', '벤치마크', '확인 가능한 지시(단어 수 등)를 따르는지 재는 평가. 라이브벤치는 25개 지시 중 16개 사용.'],
      'ChatBot Arena': ['ChatBot Arena (사람 판정 무대)', '벤치마크', '사람이 두 모델의 답 중 나은 쪽을 골라 점수를 매기는 공개 비교판.'], 'Arena-Hard': ['Arena-Hard', '벤치마크', 'GPT-4를 판정관으로 쓰는 어려운 질문 모음.']}
CORE = ['시험지 유출', '채점 로봇', '정답지 채점', '벤치마크', '순위 상관', '학습 마감일', '과적합', '온도 0']
QUIZ = {'q': [{'q': '시험지 유출(테스트셋 오염)의 증거로 논문이 든 것은?', 'o': ['학습 마감일 이후 코드포스 문제에서 성적이 떨어진다', '모델이 클수록 점수가 높다', 'GPU가 빠를수록 점수가 높다'], 'a': 0, 'why': '맞아요. 마감일 전 문제는 외웠을 수 있지만, 이후 문제는 처음 보는 거예요.', 'hint': '타임라인 증거 1을 보세요.'},
              {'q': '사람·LLM 판정의 문제로 논문이 든 것이 아닌 것은?', 'o': ['LLM은 자기 답과 긴 답을 선호', '사람은 형식·말투에 끌림', '판정은 항상 느려서 쓸 수 없다'], 'a': 2, 'why': '맞아요. LLM 판정은 오히려 빠르다는 장점이 있어요. 문제는 편향과 실수예요.', 'hint': '타임라인 마지막 칸.'}],
        'method': [{'q': '라이브벤치 업데이트에서 한 번에 바꾸는 문제 비율(평균)은?', 'o': ['1/2', '1/6', '전부'], 'a': 1, 'why': '맞아요. 그래서 약 6개월에 전부 새로워져요.', 'hint': '방법 5단계.'},
                   {'q': '[계산] 과목 점수가 64.0, 74.6, 68.7, 62.9, 67.4, 50.8이면 라이브벤치 점수(소수 첫째 자리)는?', 'o': ['64.7', '68.7', '62.9'], 'a': 0, 'why': '맞아요. 여섯 과목 평균 = 388.4 ÷ 6 ≈ 64.7 — o1-preview의 표 1 값이에요.', 'hint': '여섯 개를 더해 6으로 나눠요.'}],
        'r1': [{'q': '논문 3.4절: 두 번의 업데이트 뒤 평균 점수는?', 'o': ['약 1.2% 하락', '약 12% 상승', '변화 없음'], 'a': 0, 'why': '맞아요. 순위는 그대로(상관 0.997 초과)인데 시험은 조금 어려워졌어요.', 'hint': '짝 카드 오른쪽.'},
               {'q': '새 문제를 한 달 늦게 공개하는 이유는?', 'o': ['공개 순위표에 늘 아무도 못 본 문제가 1/6 있게 하려고', '서버 비용을 줄이려고', '문제를 더 쉽게 하려고'], 'a': 0, 'why': '맞아요. 유출을 따라오지 못하게 하는 장치예요.', 'hint': '시뮬레이터의 비공개 버튼을 꺼 보세요.'}],
        'r2': [{'q': 'AIME 2024에서 GPT-4-Turbo 답안의 점수는 정답 채점과 로봇 채점에서 각각?', 'o': ['13.793 / 35.714', '54 / 64', '38 / 68'], 'a': 0, 'why': '맞아요. 로봇이 두 배 반 넘게 부풀렸어요(표 9).', 'hint': '점수 비교에서 AIME 막대.'},
               {'q': '채점 로봇 오류율이 가장 높았던 칸은?', 'o': ['Claude-3-Opus 답안의 Zebra Puzzles (0.460)', 'Claude-3-Opus 답안의 AIME (0.103)', 'GPT-4-Turbo 답안의 AIME (0.214)'], 'a': 0, 'why': '맞아요. 논리 퍼즐에서 판정이 거의 동전 던지기 수준까지 흔들렸어요.', 'hint': '"채점 오류율" 보기로 바꿔 보세요.'}],
        'r3': [{'q': '표 1에서 추론 과목 1위는?', 'o': ['o1-preview', 'o1-mini (72.3)', 'gemini-exp-1121'], 'a': 1, 'why': '맞아요. 종합 3위 o1-mini가 추론에서는 1위예요.', 'hint': '"추론" 버튼을 눌러 보세요.'},
               {'q': '라이브벤치와 ChatBot Arena의 상관 계수는?', 'o': ['0.51', '0.88', '0.91'], 'a': 2, 'why': '맞아요. Arena-Hard와는 0.88.', 'hint': '풀이 3번.'}],
        'lab': [{'q': '모형 실험실에서 측정 순위가 진짜 순위와 같아지는 조합은?', 'o': ['공개 문제 + 채점 로봇 + 한 과목', '새 문제 + 정답지 + 여섯 과목', '공개 문제 + 정답지 + 한 과목'], 'a': 1, 'why': '맞아요. 세 장치를 모두 켜야 해요 — 논문의 세 가지 바람(desiderata)이에요.', 'hint': '세 버튼을 모두 오른쪽으로.'}],
        'reread': []}
del QUIZ['reread']

KG = {'version': '1.0', 'page': P, 'nodes': [
    node('lab:method/livebench', 'Method', '라이브벤치', 'LiveBench', '#method', P, '매달 새 문제를 더하고 객관 정답으로 자동 채점하는 여섯 과목 벤치마크.', (SRC, '2장'), 3, 'evaluation'),
    node('lab:concept/contamination', 'Concept', '시험지 유출 (테스트셋 오염)', 'test set contamination', '#q', P, '벤치마크 문제가 학습 데이터에 섞여 점수가 부풀려짐.', (SRC, '1장'), 2, 'evaluation'),
    node('lab:method/llm-judge', 'Method', '채점 로봇 (LLM 판정관)', 'LLM-as-a-judge', '#r2', P, 'LLM이 LLM 답을 채점.', (SRC, '1장, 부록'), 2, 'evaluation'),
    node('lab:method/ground-truth', 'Method', '정답지 채점', 'ground-truth scoring', '#method', P, '객관 정답과 맞춰 자동 채점.', (SRC, '2장'), 2, 'evaluation'),
    node('lab:method/monthly-update', 'Method', '월간 1/6 교체', 'monthly question replacement', '#r1', P, '업데이트마다 평균 1/6 교체, 새 문제 한 달 비공개.', (SRC, '2.7절'), 3, 'evaluation'),
    node('lab:concept/human-crowdsourcing', 'Concept', '사람 출제·판정', 'human crowdsourcing', '#q', P, '사람이 문제를 내고 판정.', (SRC, '1장'), 2, 'evaluation'),
    node('lab:concept/six-categories', 'Concept', '여섯 과목', 'six categories', '#r3', P, '수학·코딩·추론·언어·지시 따르기·데이터 분석, 과제 18개.', (SRC, '1장'), 1, 'evaluation'),
    node('lab:metric/livebench-score', 'Metric', '라이브벤치 점수', 'LiveBench score', '#method', P, '문항→과제→과목→여섯 과목 평균.', (SRC, '3장'), 1, 'evaluation'),
    node('lab:metric/rank-correlation', 'Metric', '순위 상관', 'rank correlation', '#duel', P, '두 순위표의 같은 정도.', None, 2, 'evaluation'),
    node('lab:metric/judge-error', 'Metric', '판정 오류율', 'judge error rate', '#r2', P, 'LLM 판정이 정답과 다른 비율.', (SRC, '표 8'), 2, 'evaluation'),
    node('lab:limitation/contamination', 'Limitation', '공개 벤치마크는 유출된다', 'public benchmarks get contaminated', '#q', P),
    node('lab:limitation/judge-bias', 'Limitation', '판정 편향·실수', 'judge bias and errors', '#r2', P, '자기 답·긴 답 선호, 어려운 문제에서 실수.'),
    node('lab:limitation/upkeep-cost', 'Limitation', '매달 교체 비용', 'monthly upkeep cost', '#r1', P, '사람과 계산이 매달 필요.'),
    node('lab:limitation/objective-only', 'Limitation', '정답 있는 과제만', 'objective tasks only', '#sum', P, '열린 생성 과제는 범위 밖.'),
    node('lab:claim/top-below-70', 'Claim', '최고 모델도 70% 미만 (o1-preview 64.7)', 'top models below 70%', '#r3', P, None, (SRC, '초록, 표 1')),
    node('lab:claim/rank-stable', 'Claim', '업데이트 전후 순위 상관 0.997 초과', 'rank correlation > 0.997', '#r1', P, None, (SRC, '3.4절')),
    node('lab:claim/harder', 'Claim', '평균 점수 약 1.2% 하락', 'scores dropped ~1.2%', '#r1', P, None, (SRC, '3.4절')),
    node('lab:claim/arena-corr', 'Claim', 'ChatBot Arena 0.91, Arena-Hard 0.88', 'correlations 0.91 and 0.88', '#r3', P, None, (SRC, '3.3절')),
    node('lab:claim/judge-error', 'Claim', '판정 오류율 0.103~0.460', 'judge error 0.103-0.460', '#r2', P, None, (SRC, '표 8')),
    node('lab:claim/aime-inflate', 'Claim', 'AIME 13.793 → 35.714 (로봇 채점)', 'AIME inflated by LLM judge', '#r2', P, None, (SRC, '표 9')),
    node('lab:analogy/entrance-exam', 'Analogy', '매달 바뀌는 출입 시험 ↔ 월간 교체', 'monthly exam rotation', '#r1', P),
    node('lab:analogy/ta-grading', 'Analogy', '못 푸는 문제를 채점하는 조교 ↔ 채점 로봇', 'TA grading unsolved problems', '#r2', P),
    node('lab:question/core', 'Question', '공개된 시험지의 점수는 실력일까 암기일까?', 'Skill or memorization?', '#top', P),
    node('lab:question/duel', 'Question', '대결: 문제를 바꾸면 순위가 흔들릴까?', 'Duel: do rankings shift?', '#duel', P),
    node('lab:question/open-tasks', 'Question', '정답 없는 열린 과제는 어떻게 오염 없이 잴까?', 'Contamination-free open-ended evals?', '#sum', P),
    node('lab:sim/leak', 'Simulation', '외운 문제 비율 시뮬레이터', 'contamination simulator', '#r1', P), node('lab:sim/judge', 'Simulation', '두 채점 방식 비교', 'GT vs judge', '#r2', P),
    node('lab:sim/board', 'Simulation', '과목별 줄 세우기', 'category leaderboard', '#r3', P), node('lab:sim/design', 'Simulation', '벤치마크 설계 실험실', 'benchmark design lab', '#lab', P),
    node('lab:work/' + SRC, 'Work', 'White 외 (2025) LiveBench', 'White et al. 2025', '#top', P), node('lab:work/kiely2026inference', 'Work', 'Kiely (2026) Inference Engineering', 'Kiely 2026', '#reread', P)],
 'edges': [edge('lab:method/livebench', 'hasLimitation', 'lab:limitation/upkeep-cost', '#r1'), edge('lab:concept/contamination', 'prerequisiteOf', 'lab:method/monthly-update', '#r1'),
           edge('lab:limitation/contamination', 'addressedBy', 'lab:method/monthly-update', '#r1'), edge('lab:method/llm-judge', 'hasLimitation', 'lab:limitation/judge-bias', '#r2'),
           edge('lab:limitation/judge-bias', 'addressedBy', 'lab:method/ground-truth', '#r2'), edge('lab:method/ground-truth', 'hasLimitation', 'lab:limitation/objective-only', '#sum'),
           edge('lab:method/monthly-update', 'partOf', 'lab:method/livebench', '#method'), edge('lab:method/ground-truth', 'partOf', 'lab:method/livebench', '#method'), edge('lab:concept/six-categories', 'partOf', 'lab:method/livebench', '#r3'),
           edge('lab:metric/livebench-score', 'relatedTo', 'lab:concept/six-categories', '#method'), edge('lab:concept/human-crowdsourcing', 'relatedTo', 'lab:method/llm-judge', '#q'), edge('lab:metric/judge-error', 'relatedTo', 'lab:method/llm-judge', '#r2')]
          + [edge(c, 'assertedIn', 'lab:work/' + SRC, '#r1') for c in ['lab:claim/top-below-70', 'lab:claim/rank-stable', 'lab:claim/harder', 'lab:claim/arena-corr', 'lab:claim/judge-error', 'lab:claim/aime-inflate']]
          + [edge('lab:claim/rank-stable', 'supports', 'lab:method/monthly-update', '#r1'), edge('lab:claim/judge-error', 'supports', 'lab:method/ground-truth', '#r2'),
             edge('lab:analogy/entrance-exam', 'relatedTo', 'lab:method/monthly-update', '#r1'), edge('lab:analogy/ta-grading', 'relatedTo', 'lab:method/llm-judge', '#r2'),
             edge('lab:sim/leak', 'relatedTo', 'lab:method/monthly-update', '#r1'), edge('lab:sim/judge', 'relatedTo', 'lab:method/llm-judge', '#r2'), edge('lab:method/livebench', 'relatedTo', 'lab:work/kiely2026inference', '#reread')]}
REFS = [ref(SRC, 'paper-conference', 'LiveBench: A Challenging, Contamination-Limited LLM Benchmark', ['Colin White', 'Samuel Dooley', 'Manley Roberts', 'Arka Pal', 'Benjamin Feuer', 'Siddhartha Jain', 'Ravid Shwartz-Ziv', 'Neel Jain', 'Khalid Saifullah', 'Sreemanti Dey', 'Shubh-Agrawal', 'Sandeep Singh Sandha', 'Siddartha Naidu', 'Chinmay Hegde', 'Yann LeCun', 'Tom Goldstein', 'Willie Neiswanger', 'Micah Goldblum'], 2025, 'International Conference on Learning Representations (ICLR 2025)', 'https://arxiv.org/abs/2406.19314', note='arXiv:2406.19314v2'),
        book_ref()]
REFS[1]['lab']['role'] = 'background'

JS = r'''
var C=L.C,F=L.FONT,fit=L.fit,grid=L.grid,stamp=L.stamp,PIPE=%s,T8=%s,T1=%s;
L.kpis('#heroK',[['6 · 18','과목 · 과제','g'],['64.7','최고 점수 (70%% 미만)','m'],['1/6','업데이트마다 교체','i'],['0.997+','업데이트 전후 순위 상관','a']]);
/* 방법 */
function pipe(i){var p=PIPE[i];$('#pipeOut').innerHTML='<h3>'+(i+1)+' · '+p[0]+'</h3><p>'+p[1]+'</p>';$$('#pipe [data-p]').forEach(function(b){b.setAttribute('aria-pressed',+b.dataset.p===i?'true':'false')});}
$$('#pipe [data-p]').forEach(function(b){b.addEventListener('click',function(){pipe(+b.dataset.p)})});pipe(0);
/* ① 유출 */
var cK=$('#cLeak'),km=3,kr=1/6,kp=1,LEAK=0.25;
function leakSeries(r,priv){var age=[1],s=[];for(var m=0;m<=12;m++){var seen=0,tot=0;age.forEach(function(w,a){tot+=w;var exposed=priv?Math.max(0,a-1):a;seen+=w*(1-Math.pow(1-LEAK,exposed));});s.push(seen/tot);var nx=age.map(function(w){return w*(1-r)});nx.unshift(r);if(r===0){nx=age.slice();nx.unshift(0);}age=nx;}return s;}
function drawK(){var W=fit(cK,220),x=cK.getContext('2d');x.clearRect(0,0,W,220);grid(x,W,220);var L0=40,R=W-20,T=16,B=186;function px(m){return L0+(R-L0)*m/12}function py(v){return B-(B-T)*v}
  [[0,C.eye,'교체 안 함'],[kr,C.gfp,'지금 설정']].forEach(function(c){var s=leakSeries(c[0],kp);x.strokeStyle=c[1];x.lineWidth=2;x.beginPath();s.forEach(function(v,m){m?x.lineTo(px(m),py(v)):x.moveTo(px(m),py(v));});x.stroke();x.lineWidth=1;x.fillStyle=c[1];x.font='12px '+F;x.textAlign='right';x.fillText(c[2],R-4,py(s[12])+16);});
  x.strokeStyle=C.text;x.setLineDash([4,3]);x.beginPath();x.moveTo(px(km),T);x.lineTo(px(km),B);x.stroke();x.setLineDash([]);
  x.fillStyle=C.muted;x.font='11px '+F;x.textAlign='center';for(var m=0;m<=12;m+=2)x.fillText(m+'개월',px(m),B+16);x.textAlign='left';x.fillText('유출된 문제 비율',L0+4,T+10);stamp(x,W,'유출 속도는 설명용');}
function updK(){L.setTxt('#kMV',km+'개월');L.setTxt('#kRV',kr<0.01?'0':'1/'+Math.round(1/kr));var s=leakSeries(kr,kp),s0=leakSeries(0,kp);
  L.kpis('#kK',[[(s[km]*100).toFixed(0)+'%%','유출된 비율 (설명용)','r'],[(s0[km]*100).toFixed(0)+'%%','교체 안 했다면','a'],[kr>0?Math.round(1/kr)+'개월':'—','전부 바뀌는 데 (대략)','g'],[kp?'1/6':'0','늘 비공개인 몫','i']]);
  L.ins('#kI',[[s[km]<s0[km]?'g':'r',kr>0?'교체 덕분에 유출 비율이 '+((s0[km]-s[km])*100).toFixed(0)+'%%p 낮아요.':'교체가 없으면 유출은 계속 쌓여요.'],['a','논문 기본값: 업데이트마다 1/6 교체, 새 문제 한 달 비공개.']]);drawK();}
$('#kM').addEventListener('input',function(){km=+this.value;updK();});$('#kR').addEventListener('input',function(){kr=+this.value;updK();});L.bindSeg('#kP',function(v){kp=+v;updK();});L.addMod(cK,function(dt){if(dt===0)drawK();});updK();
/* ② 판정 */
var cJ=$('#cJudge'),jm=0,jv='score';
function drawJ(){var W=fit(cJ,240),x=cJ.getContext('2d');x.clearRect(0,0,W,240);grid(x,W,240);var n=4,gw=(W-40)/n,B=200,T=24;
  T8.tasks.forEach(function(t,i){var cx=20+i*gw;x.fillStyle=C.text;x.font='12px '+F;x.textAlign='center';x.fillText(t,cx+gw/2,B+18);
    if(jv==='score'){var g=T8.gt[jm][i],j=T8.jd[jm][i],bw=(gw-30)/2;[[g,C.gfp,'정답'],[j,C.stain,'로봇']].forEach(function(v,k){var h=(B-T)*v[0]/100;x.fillStyle=v[1];x.fillRect(cx+10+k*(bw+10),B-h,bw,h);x.fillStyle=C.text;x.fillText(String(v[0]),cx+10+k*(bw+10)+bw/2,B-h-4);});}
    else{var e=T8.err[jm][i],h=(B-T)*e/0.5;x.fillStyle=C.eye;x.fillRect(cx+gw*0.25,B-h,gw*0.5,h);x.fillStyle=C.text;x.fillText(e.toFixed(3),cx+gw/2,B-h-4);}});
  x.textAlign='left';x.fillStyle=C.muted;x.fillText(jv==='score'?'초록 = 정답지 채점(GT), 분홍 = 채점 로봇':'채점 로봇 오류율 (0~0.5 눈금)',20,16);}
function updJ(){var g=T8.gt[jm],j=T8.jd[jm],diff=g.map(function(v,i){return j[i]-v}),mx=0,mi=0;diff.forEach(function(d,i){if(Math.abs(d)>Math.abs(mx)){mx=d;mi=i;}});
  L.kpis('#jK',[[T8.models[jm],'답안 쓴 모델','i'],['GPT-4-Turbo','채점 로봇','m'],[(mx>0?'+':'')+mx.toFixed(1),'가장 크게 어긋난 칸 ('+T8.tasks[mi]+')','r'],[Math.min.apply(0,T8.err[jm]).toFixed(3)+'~'+Math.max.apply(0,T8.err[jm]).toFixed(3),'오류율 범위','a']]);
  L.ins('#jI',[['r','로봇 채점이 '+diff.filter(function(d){return d>0}).length+'개 과제에서 부풀리고 '+diff.filter(function(d){return d<0}).length+'개 과제에서 깎았어요. 방향이 일정하지 않아요.']]);drawJ();}
L.bindSeg('#jM',function(v){jm=+v;updJ();});L.bindSeg('#jV',function(v){jv=v;updJ();});L.addMod(cJ,function(dt){if(dt===0)drawJ();});updJ();
/* ③ 성적표 */
var cB=$('#cBoard'),bc=1,NM=['','종합','코딩','데이터 분석','지시 따르기','언어','수학','추론'];
function drawB(){var W=fit(cB,420),x=cB.getContext('2d');x.clearRect(0,0,W,420);grid(x,W,420);var rows=T1.slice().sort(function(a,b){return b[bc]-a[bc]}),L0=230,R=W-60;
  rows.forEach(function(r,i){var y=14+i*26,w=(R-L0)*r[bc]/90;x.fillStyle=i===0?C.gfp:/^o1/.test(r[0])?'rgba(214,114,214,.7)':'rgba(130,184,255,.55)';x.fillRect(L0,y,w,18);
    x.fillStyle=C.text;x.font='12px '+F;x.textAlign='right';x.fillText(r[0],L0-8,y+13);x.textAlign='left';x.fillText(r[bc].toFixed(1),L0+w+6,y+13);});}
function updB(){var rows=T1.slice().sort(function(a,b){return b[bc]-a[bc]}),ov=T1.slice().sort(function(a,b){return b[1]-a[1]});var top=rows[0],orank=ov.indexOf(top)+1;
  L.kpis('#bK',[[top[bc].toFixed(1),NM[bc]+' 1위 점수','g'],[top[0],NM[bc]+' 1위','m'],[orank+'위','그 모델의 종합 순위','a']]);
  L.ins('#bI',[[bc===1?'g':'a',bc===1?'종합 1위 o1-preview 64.7 — 70%% 미만이에요.':NM[bc]+' 1위는 종합 '+orank+'위 모델이에요.'],['i','분홍 막대 = o1 계열. 과목마다 선두가 바뀌는지 눌러 보세요.']]);drawB();}
L.bindSeg('#bC',function(v){bc=+v;updB();});L.addMod(cB,function(dt){if(dt===0)drawB();});updB();
/* 실험실 */
var cL=$('#cLab'),xf=0,xg='judge',xd=1,TRUE=[0.72,0.60,0.48],NAMES=['모델 갑','모델 을','모델 병'];
function measure(){var r=L.rng(9),out=[];for(var i=0;i<3;i++){var t=TRUE[i],m=t;if(!xf)m+= [0.05,0.22,0.12][i];if(xg==='judge')m+=[ -0.06,0.08,0.10][i]*(1)+(r()-0.5)*0.08;if(xd===1)m+=[ -0.04,0.06,0.02][i];m=Math.max(0.05,Math.min(0.98,m));out.push(m);}return out;}
function drawL(){var W=fit(cL,230),x=cL.getContext('2d'),m=measure();x.clearRect(0,0,W,230);grid(x,W,230);var bw=Math.min(140,(W-80)/3),B=190,T=20;
  m.forEach(function(v,i){var cx=40+i*(bw+20),h=(B-T)*v,ht=(B-T)*TRUE[i];x.fillStyle='rgba(130,184,255,.6)';x.fillRect(cx,B-h,bw,h);x.strokeStyle=C.gfp;x.setLineDash([5,3]);x.lineWidth=2;x.beginPath();x.moveTo(cx-6,B-ht);x.lineTo(cx+bw+6,B-ht);x.stroke();x.setLineDash([]);x.lineWidth=1;
    x.fillStyle=C.text;x.font='12px '+F;x.textAlign='center';x.fillText(NAMES[i]+' · 측정 '+(v*100).toFixed(0)+' / 진짜 '+(TRUE[i]*100).toFixed(0),cx+bw/2,B+18);});stamp(x,W,'시드 고정 설명용');}
function updL(){var m=measure(),err=m.reduce(function(s,v,i){return s+Math.abs(v-TRUE[i])},0)/3,order=m.map(function(v,i){return [v,i]}).sort(function(a,b){return b[0]-a[0]}).map(function(a){return a[1]}),ok=order.join()==='0,1,2';
  L.kpis('#xK',[[(err*100).toFixed(1),'평균 측정 오차 (점)','r'],[ok?'같음':'다름','측정 순위 vs 진짜 순위',ok?'g':'a'],[[xf?'새 문제':'공개 문제',xg==='gt'?'정답지':'채점 로봇',xd+'과목'].join(' · '),'지금 설계','i']]);
  L.ins('#xI',[[ok?'g':'r',ok?'측정 순위가 진짜 순위와 같아요.':'측정 순위가 뒤집혔어요: '+order.map(function(i){return NAMES[i]}).join(' > ')]]);drawL();}
L.bindSeg('#xF',function(v){xf=+v;updL();});L.bindSeg('#xG',function(v){xg=v;updL();});L.bindSeg('#xD',function(v){xd=+v;updL();});L.addMod(cL,function(dt){if(dt===0)drawL();});updL();
/* 대결 */
L.Duel({fmt:function(v){return v.toFixed(3)},run:function(){var r=0.997,f=0.9;
  return {fly:f,robo:r,res:'R',bars:[['f','초파리 (0.9 미만 예상)',f],['r','주판봇 (실측 하한)',r]],asst:'원판↔1차, 1차↔2차 업데이트의 순위 상관이 모두 0.997을 넘었어요(논문 3.4절). 초파리가 예상한 "0.9 미만"과는 거리가 멀어요.',
  verdict:'문제를 바꿔도 줄 세우기는 그대로였다. 주판봇 승.',note:'초파리 막대는 초파리 주장의 기준선(0.9)이고, 주판봇 막대는 논문이 밝힌 하한(0.997)이에요. 다만 평균 점수는 약 1.2%% 떨어져 시험이 어려워진 건 맞아요.'};}});
''' % (_j.dumps(PIPE, ensure_ascii=False), _j.dumps(T8), _j.dumps(T1))

def spec():
    return {'meta': {'title': '라이브벤치 — 새 시험지로만 재는 성적표 (LiveBench 연구실 해설)', 'description': '인퍼런스 스터디 북 1주차 논문: White 외(ICLR 2025) LiveBench — 시험지 유출, 채점 로봇의 실수, 여섯 과목 성적표',
                     'series': '인퍼런스 스터디 북', 'number': '01-A1', 'slug': 'livebench', 'version': '2.0', 'date': '2026-11-11', 'creator': ['안상선'], 'license': 'CC BY-NC 4.0 (캐릭터 제외)', 'url': URL,
                     'kgStart': 'lab:method/llm-judge', 'citeKey': 'ahn2026livebench', 'domain': 'ai',
                     'suggestedCitation': '안상선 (2026). 라이브벤치 — 새 시험지로만 재는 성적표. 인퍼런스 스터디 북 1주차 논문 해설. ' + URL},
            'kg': KG, 'refs': REFS, 'gl': GL, 'core': CORE, 'quiz': QUIZ, 'js': JS,
            'nav': nav([('cast', '식구'), ('q', '1 질문'), ('method', '2 방법'), ('r1', '결과①'), ('r2', '결과②'), ('r3', '결과③'), ('lab', '실험실'), ('duel', '대결'), ('reread', '다시 읽기'), ('sum', '한 장'), ('kg', '색인'), ('export', '꾸러미')]),
            'body': cover('cover_lb', '인퍼런스 스터디 북 · 1주차 · 논문', '연구실 식구 여섯이 매달 새 시험지가 붙는 게시판 앞에 서 있는 대체 표지',
                          motif=''.join('<i class="%s"></i>' % c for c in ['on', 'm', 'a', 'on', 'm', 'a', 'on', 'on', 'on', 'on', 'on', 'on']),
                          moods={'doc': 'think', 'asst': 'report', 'fly': 'magnify', 'robo': 'chart', 'sia': 'explain', 'moa': 'report'})
                    + hero + cast + q + method + r1 + r2 + r3 + lab + duel_sec + reread + onepage + outro,
            'footer': footer([('논문', 'White, C. 외 (2025). LiveBench: A Challenging, Contamination-Limited LLM Benchmark. ICLR 2025. arXiv:2406.19314v2'), ('표 1', '논문 표 1 상위 15개 모델 (원문 그대로)'), ('표 8·9', '논문 부록 LLM 판정 예비 실험 (원문 그대로)'),
                              ('연결', 'Kiely (2026) Inference Engineering 1장 1.3.1 평가')],
                             ['결과 ① 유출 속도 상수', '모형 실험실의 세 가상 모델과 오차', '대결의 초파리 막대(0.9)는 주장 기준선'],
                             prev=('../week_01_textbook_ch01/', '1장 시작 전에 정할 것'), nxt=('../week_02_textbook_ch02_p1_p2/', '2주차 2장 모델'))}

if __name__ == '__main__':
    out = os.path.join(sys.argv[1], SLUG, 'index.html')
    print(out, build(spec(), out))
