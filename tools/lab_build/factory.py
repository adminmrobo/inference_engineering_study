# -*- coding: utf-8 -*-
"""인퍼런스 공장 — 스터디 북을 GPU 추론 공장 건물 하나로 보여 준다.

- 목차(index.html) 첫 화면: 건물 전체 3D (층 = 주차, 층 묶음 = 책의 장)
- 각 해설 페이지 첫 화면: 그 페이지가 맡은 층(공정)을 3D로 보여 주고 기계 번호 = 페이지 칸으로 안내

사용:
  python3 factory.py <스터디 북 루트>     # 모든 해설 페이지 첫 화면에 층 안내를 넣거나 새로 고친다 (몇 번 돌려도 같은 결과)
  build_index.py 는 index_section()으로 목차 첫 화면을 만든다.
3D는 three.js(CDN)를 쓰고, 불러오지 못하면 층 목록·기계 목록만으로도 안내가 된다.
"""
import base64, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from series import WEEKS, SPECIALS, STATUS_KO

HERE = os.path.dirname(os.path.abspath(__file__))
THREE_VER = '0.170.0'
START, END = '<!-- gf:floor -->', '<!-- /gf:floor -->'

# 장 색 (건물 오른쪽 띠)
CHAP = {
    'c01': ('서문 · 0장 · 1장', '#b07cff'), 'c2': ('2장 모델', '#5ee39c'), 'c3': ('3장 하드웨어', '#82b8ff'),
    'c4': ('4장 소프트웨어', '#57d0dc'), 'c5': ('5장 최적화 기법', '#f1b646'), 'c6': ('6장 입출력 유형', '#ff86b8'),
    'c7': ('7장 운영', '#ef5b5b'), 'ap': ('부록', '#9d9bb8'),
}

# 층 = 주차. stations: (기계 모양, 이름, 설명, 페이지 폴더, 칸 id)
# 칸 id는 그 페이지의 <section id>. 준비 중인 주차는 폴더만 있고 칸 id는 None.
P = {'pre': 'week_01_textbook_preface', 'c0': 'week_01_textbook_ch00', 'c1': 'week_01_textbook_ch01', 'lb': 'week_01_article_01',
     'm1': 'week_02_textbook_ch02_p1_p2', 'tf': 'week_02_article_01', 'm2': 'week_03_textbook_ch02_p3_to_end', 'fa': 'week_03_article_01'}
FLOORS = [
    {'week': 1, 'fl': '1F', 'name': '정문 · 설계실', 'chap': 'c01',
     'process': '주문 접수와 설계 — 무엇을, 누구에게, 어떤 눈금으로 만들지 정한다',
     'desc': '주문(요청)이 들어오는 정문입니다. 추론이 왜 모두의 일이 됐는지 보고, 학습과 추론을 나누고, 공유냐 전용이냐 · 어떤 모델이냐 · 무엇으로 재느냐를 먼저 정합니다.',
     'st': [('door', '정문 — 쏟아지는 모델', '해마다 늘어나는 모델이 정문으로 밀려 들어옵니다. 추론이 왜 모두의 일이 됐는지 여기서 시작해요.', P['pre'], 'lv1'),
            ('scale', '세 개의 저울', '지연시간 · 가용성 · 비용. 이 공장이 끝까지 지켜야 할 세 눈금입니다.', P['pre'], 'lv3'),
            ('twin', '학습동과 추론동', '모델은 한 번 만들고(학습), 주문마다 돌립니다(추론). 이 건물은 돌리는 쪽 공장이에요.', P['c0'], 'lv1'),
            ('board', '세 층 안내판', '런타임 · 인프라 · 도구. 책 전체가 이 세 층 위에 지어집니다.', P['c0'], 'big'),
            ('desk', '설계 책상', '공유 추론을 빌려 쓸까, 전용으로 띄울까. 우리 앱이 어떤 앱인지부터 정합니다.', P['c1'], 'lv2'),
            ('gauge', '계량대 — 지연·처리량', '평균만 보면 속습니다. 지연시간과 처리량을 재는 법, P99까지 봅니다.', P['c1'], 'lv5'),
            ('screen', '성적 게시판', '매달 문제를 바꾸는 시험지로 모델 성적을 잽니다. 모델 고르기와 짝을 이루는 논문이에요.', P['lb'], 'method')]},
    {'week': 2, 'fl': '2F', 'name': '모델 조립 라인', 'chap': 'c2',
     'process': '모델이라는 기계를 뜯어 본다 — 토큰 하나가 층을 지나 다음 토큰이 되기까지',
     'desc': '신경망의 기본 동작(행렬곱)부터 어텐션과 KV 캐시, 전문가 혼합까지 모델 내부 공정을 따라갑니다. 짝 논문은 트랜스포머입니다.',
     'st': [('conveyor', '주문 → 다음 토큰 컨베이어', '주문 한 줄이 토큰으로 쪼개져 모델을 지나 다음 토큰 하나로 나오는 큰 그림입니다.', P['m1'], 'big'),
            ('press', '행렬곱 프레스', '신경망이 하는 일의 대부분은 숫자 표끼리 곱하기입니다.', P['m1'], 'lv1'),
            ('layers', '어텐션 · KV 캐시 선반', '앞 토큰을 매번 다시 계산하지 않도록 키·값을 선반에 쌓아 둡니다.', P['m1'], 'lv4'),
            ('split', '전문가 작업대 (MoE)', '거대한 기계 하나 대신 작은 전문가 여럿 중 몇 명만 일을 맡깁니다.', P['m1'], 'lv5'),
            ('lamp', '형광펜 작업대', '질문 · 색인표 · 내용으로 문장의 어디를 볼지 칠합니다 (셀프 어텐션).', P['tf'], 'r1'),
            ('heads', '여러 색 형광펜', '머리 여러 개가 서로 다른 관계를 동시에 봅니다 (멀티헤드).', P['tf'], 'r2')]},
    {'week': 3, 'fl': '3F', 'name': '병목 진단실', 'chap': 'c2',
     'process': '느린 곳을 찾는다 — 계산이 막혔나, 메모리 통로가 막혔나',
     'desc': 'GPU를 주방에 빗대어 요리사(연산)와 재료 통로(메모리)를 나누고, 그림·영상 생성 공정과 루프라인으로 병목을 짚습니다. 짝 논문은 FlashAttention입니다.',
     'st': [('kitchen', 'GPU 주방', '요리사(연산)와 재료 통로(메모리 대역폭) — 두 자원 중 무엇이 모자란지 봅니다.', P['m2'], 'lv1'),
            ('denoise', '그림 닦기 라인', '그림 생성은 잡음을 서른 번 넘게 닦아 내는 공정입니다.', P['m2'], 'lv2'),
            ('roofline', '루프라인 게시판', '어디가 막혔나 — 지붕선 그래프 하나로 판정합니다.', P['m2'], 'lv6'),
            ('pipe', '동선 줄이기', '결과는 그대로 두고 오가는 길만 줄여 빨라지게 합니다.', P['m2'], 'lv8'),
            ('warehouse', '작은 창고 · 큰 창고', '작고 빠른 창고(SRAM)와 크고 느린 창고(HBM) 사이 왕복을 줄입니다.', P['fa'], 'method'),
            ('tiles', '타일 계산대', '쪼개서 계산해도 답은 똑같습니다 — 그래서 한 번에 다 올리지 않아도 돼요.', P['fa'], 'r2')]},
    {'week': 4, 'fl': '4F', 'name': 'GPU 기계실', 'chap': 'c3',
     'process': '공장의 엔진룸 — GPU의 구조와 세대, 빌려 쓰는 단위',
     'desc': 'GPU 내부 구조와 메모리, 세대별 차이, 클라우드 인스턴스, 다른 가속기와 로컬 추론까지 하드웨어를 둘러봅니다. 짝 논문은 루프라인 모델(예정)입니다.',
     'st': [('rack', 'GPU 랙', '3.1 GPU 구조 — 연산 장치가 어떻게 모여 있나.', 'week_04_textbook_ch03', None),
            ('tower', '메모리 탑 (HBM)', '3.1 — 모델 무게를 담는 고대역폭 메모리.', 'week_04_textbook_ch03', None),
            ('shelf', '세대별 진열장', '3.2 GPU 세대 — 세대가 바뀌면 무엇이 달라지나.', 'week_04_textbook_ch03', None),
            ('cells', '인스턴스 칸막이', '3.3 인스턴스 — 빌려 쓰는 단위와 묶음.', 'week_04_textbook_ch03', None),
            ('chip', '다른 가속기 코너', '3.4 GPU 말고 다른 데이터센터 가속기.', 'week_04_textbook_ch03', None),
            ('laptop', '로컬 추론 책상', '3.5 내 컴퓨터에서 돌리는 추론.', 'week_04_textbook_ch03', None),
            ('roofline', '루프라인 측정대', '논문 — 연산과 메모리의 지붕선 (예정).', 'week_04_article_01', None)]},
    {'week': 5, 'fl': '5F', 'name': '엔진 제어실', 'chap': 'c4',
     'process': '기계를 움직이는 소프트웨어 — CUDA부터 추론 엔진, 부하 시험까지',
     'desc': 'GPU를 부리는 CUDA, 딥러닝 프레임워크, 추론 엔진과 Dynamo, 성능 측정과 부하 시험을 다룹니다. 짝 논문은 페이지드 어텐션 · vLLM(예정)입니다.',
     'st': [('panel', 'CUDA 배전반', '4.1 — GPU에 일을 시키는 가장 아래 층.', 'week_05_textbook_ch04', None),
            ('wall', '프레임워크 공구벽', '4.2 딥러닝 프레임워크와 라이브러리.', 'week_05_textbook_ch04', None),
            ('turbine', '추론 엔진', '4.3 요청을 받아 모델을 돌리는 엔진.', 'week_05_textbook_ch04', None),
            ('hub', '분배기 (Dynamo)', '4.4 여러 GPU에 일을 나눠 주는 분배기.', 'week_05_textbook_ch04', None),
            ('load', '부하 시험대', '4.5 성능 측정과 부하 시험.', 'week_05_textbook_ch04', None),
            ('drawers', '페이지 서랍장', '논문 — KV 캐시를 서랍(페이지)처럼 나눠 담기 (예정).', 'week_05_article_01', None)]},
    {'week': 6, 'fl': '6F', 'name': '튜닝 공방 ①', 'chap': 'c5',
     'process': '같은 기계로 더 빨리 — 숫자를 줄이고, 초안을 먼저 쓰고 검수한다',
     'desc': '양자화로 숫자 크기를 줄이고, 작은 모델이 초안을 쓰면 큰 모델이 검수하는 추측 디코딩을 봅니다. 짝 논문은 추측 디코딩 논문(예정)입니다.',
     'st': [('press', '양자화 압축기', '5.1 숫자를 작게 눌러 담아 더 빨리, 더 싸게.', 'week_06_textbook_ch05_p1_p2', None),
            ('gauge', '품질 계량대', '5.1 줄여도 품질이 버티는지 잽니다.', 'week_06_textbook_ch05_p1_p2', None),
            ('draft', '초안 · 검수 쌍둥이 라인', '5.2 작은 모델이 먼저 쓰고 큰 모델이 한 번에 검수.', 'week_06_textbook_ch05_p1_p2', None),
            ('screen', '논문 부스', '논문 — 추측 디코딩 (예정).', 'week_06_article_01', None)]},
    {'week': 7, 'fl': '7F', 'name': '튜닝 공방 ②', 'chap': 'c5',
     'process': '다시 쓰고, 나눠 싣고, 갈라 세운다 — 캐시 · 병렬화 · 분리',
     'desc': '이미 한 계산을 다시 쓰는 캐시, 모델을 여러 GPU에 나눠 싣는 병렬화, 프리필과 디코드를 다른 방으로 나누는 분리를 다룹니다. 짝 논문은 SGLang(예정)입니다.',
     'st': [('cache', '캐시 창고', '5.3 한 번 만든 결과를 다시 꺼내 씁니다.', 'week_07_textbook_ch05_p3_to_end', None),
            ('parallel', '병렬 분할 라인', '5.4 큰 모델을 여러 GPU에 나눠 싣기.', 'week_07_textbook_ch05_p3_to_end', None),
            ('rooms', '프리필 · 디코드 분리실', '5.5 성격이 다른 두 공정을 다른 방에서.', 'week_07_textbook_ch05_p3_to_end', None),
            ('router', '프로그램 라우터', '논문 — SGLang (예정).', 'week_07_article_01', None)]},
    {'week': 8, 'fl': '8F', 'name': '다품종 라인', 'chap': 'c6',
     'process': '글만이 아니다 — 그림 · 소리 · 영상을 받고 내보내는 라인',
     'desc': '그림을 읽는 언어 모델, 임베딩, 음성 인식과 합성, 그림·영상 생성까지 입출력 유형별 추론을 봅니다. 짝 논문은 LLaVA(예정)입니다.',
     'st': [('eye', '그림 읽는 라인 (VLM)', '6.1 그림을 보고 글로 답하는 모델.', 'week_08_textbook_ch06', None),
            ('sorter', '임베딩 분류대', '6.2 글을 숫자 좌표로 바꿔 비슷한 것끼리.', 'week_08_textbook_ch06', None),
            ('booth', '듣기 · 말하기 부스', '6.3–6.4 음성 인식(ASR)과 음성 합성(TTS).', 'week_08_textbook_ch06', None),
            ('canvas', '그림 · 영상 라인', '6.5–6.6 그림과 영상 생성 모델.', 'week_08_textbook_ch06', None),
            ('screen', '논문 부스', '논문 — LLaVA (예정).', 'week_08_article_01', None)]},
    {'week': 9, 'fl': '9F', 'name': '출하 준비실', 'chap': 'c7',
     'process': '포장하고, 늘렸다 줄였다 — 컨테이너와 자동 확장',
     'desc': '모델을 컨테이너로 포장하고, 요청량에 따라 GPU를 늘리고 줄이는 자동 확장을 다룹니다. 짝 논문은 Orca(예정)입니다.',
     'st': [('container', '컨테이너 포장대', '7.1 어디서나 똑같이 돌게 포장하기.', 'week_09_textbook_ch07_p1_p2', None),
            ('servers', '자동 확장 서버 줄', '7.2 요청이 몰리면 늘리고, 빠지면 줄이기.', 'week_09_textbook_ch07_p1_p2', None),
            ('gauge', '요청량 계기판', '7.2 언제 늘릴지 정하는 눈금.', 'week_09_textbook_ch07_p1_p2', None),
            ('dispatcher', '반복 단위 배차기', '논문 — Orca (예정).', 'week_09_article_01', None)]},
    {'week': 10, 'fl': '10F', 'name': '운영 관제 · 출하장', 'chap': 'c7',
     'process': '멈추지 않게 운영하고 손님에게 내보낸다',
     'desc': '여러 클라우드에 걸친 용량 관리, 시험과 배포, 클라이언트 코드, 실제 운영까지 다룹니다. 짝 논문은 AgentDojo(예정)입니다.',
     'st': [('crane', '멀티 클라우드 크레인', '7.3 여러 클라우드의 GPU를 끌어다 쓰기.', 'week_10_textbook_ch07_p3_to_end', None),
            ('gate', '시험 · 배포 관문', '7.4 새 버전을 안전하게 내보내기.', 'week_10_textbook_ch07_p3_to_end', None),
            ('window', '클라이언트 창구', '7.5 손님 쪽 코드가 받는 법.', 'week_10_textbook_ch07_p3_to_end', None),
            ('panel', '운영 관제석', '7.6 실제 운영 사례.', 'week_10_textbook_ch07_p3_to_end', None),
            ('shield', '보안 시험장', '논문 — AgentDojo (예정).', 'week_10_article_01', None)]},
    {'week': 0, 'fl': 'RF', 'name': '옥상 연구 전망대', 'chap': 'ap',
     'process': '공장 밖을 내다본다 — 부록 · 특별편',
     'desc': '본편 10층을 다 오른 뒤 공장 밖을 내다보는 특별편 2~3편 자리입니다. 주제는 준비 중입니다.',
     'st': [('dome', '전망대', '부록 A — 특별편 1 (주제 준비 중).', 'special_01', None),
            ('antenna', '안테나', '부록 B — 특별편 2 (주제 준비 중).', 'special_02', None),
            ('board', '특별편 게시판', '부록 C — 특별편 3 (선택, 준비 중).', 'special_03', None)]},
]


def _status(root, folder, declared):
    f = os.path.join(root, folder, 'index.html')
    if declared == 'plan' or not os.path.exists(f):
        return 'plan'
    if declared == 'kept':
        return 'kept'
    return 'done' if 'ai-lab-explainer v1.12' in open(f, encoding='utf-8').read() else 'wip'


def pages_by_folder(root):
    out = {}
    for w in WEEKS:
        for it in w['items']:
            out[it['folder']] = {'folder': it['folder'], 'kind': it['kind'], 'label': it['label'], 'title': it['title'],
                                 'range': it['range'], 'week': w['no'], 'st': _status(root, it['folder'], it['status'])}
    for s in SPECIALS:
        out[s['folder']] = {'folder': s['folder'], 'kind': 'special', 'label': s['label'], 'title': s['title'], 'range': '', 'week': 0, 'st': 'plan'}
    return out


def world(root):
    """3D와 안내판이 함께 읽는 데이터."""
    pg = pages_by_folder(root)
    floors = []
    for i, f in enumerate(FLOORS):
        folders = []
        for s in f['st']:
            if s[3] not in folders:
                folders.append(s[3])
        if f['week']:
            for w in WEEKS:
                if w['no'] == f['week']:
                    for it in w['items']:
                        if it['folder'] not in folders:
                            folders.append(it['folder'])
        pages = [pg[x] for x in folders if x in pg]
        sts = [p['st'] for p in pages]
        fst = 'done' if 'done' in sts else 'kept' if 'kept' in sts else 'wip' if 'wip' in sts else 'plan'
        cname, ccol = CHAP[f['chap']]
        floors.append({'i': i, 'fl': f['fl'], 'week': f['week'], 'name': f['name'], 'chap': cname, 'col': ccol, 'process': f['process'], 'desc': f['desc'], 'st': fst,
                       'pages': pages,
                       'stations': [{'type': s[0], 'name': s[1], 'desc': s[2], 'page': s[3], 'sec': s[4], 'st': pg.get(s[3], {}).get('st', 'plan')} for s in f['st']]})
    return {'floors': floors, 'statusKo': STATUS_KO}


def floor_of(folder):
    for i, f in enumerate(FLOORS):
        if any(s[3] == folder for s in f['st']):
            return i
    return None


def _guide_img():
    try:
        import lab
        real = lab.resolve('sia_guide')
        return lab._b64('sia', real, 96) or ''
    except Exception:
        return ''


def _asset(name):
    return open(os.path.join(HERE, name), encoding='utf-8').read()


def _scripts(cfg):
    J = json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/')
    return ('<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@%s/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@%s/examples/jsm/"}}</script>'
            '<script type="application/json" id="gf-data">%s</script><script type="module">%s</script>') % (THREE_VER, THREE_VER, J, _asset('factory3d.js'))


def index_section(root):
    """목차 첫 화면 — 건물 전체."""
    W = world(root)
    cfg = {'mode': 'building', 'focus': -1, 'page': None, 'base': '', **W}
    img = _guide_img()
    return ('<style>' + _asset('factory.css') + '</style>'
            '<section class="gf gf-building" id="factory" aria-label="인퍼런스 공장 — 건물 전체">'
            '<div class="gf-head"><p class="gf-eye">INFERENCE FACTORY · 표지</p><h2 class="gf-h">인퍼런스 공장</h2>'
            '<p class="gf-lead">GPU로 답(토큰)을 만들어 내는 공장 하나를 지었습니다. <b>한 층이 한 주차</b>, 같은 색 띠로 묶인 층이 <b>책의 한 장</b>입니다. '
            '아래층부터 올라가면 주문 접수 → 모델 조립 → 병목 진단 → GPU 기계실 → … → 출하장 순서로 책을 다 읽게 됩니다.</p></div>'
            '<div class="gf-grid"><div class="gf-stage"><div class="gf-cv" id="gf-cv" role="img" aria-label="인퍼런스 공장 3D 건물. 층을 누르면 그 층의 공정이 열립니다."></div><div class="gf-labels" id="gf-labels" aria-hidden="true"></div>'
            '<div class="gf-err" id="gf-err">3D 건물을 불러오지 못했습니다 (three.js 연결이나 WebGL 지원 확인). 오른쪽 층 목록으로 그대로 둘러볼 수 있어요.</div>'
            '<div class="gf-tools"><button type="button" class="gf-bt" id="gf-all">건물 전체</button><span class="gf-hint" id="gf-hint">끌어서 돌리기 · 휠로 확대 · 층을 누르면 열림</span></div></div>'
            '<aside class="gf-side"><div class="gf-guide"><img alt="" aria-hidden="true" src="%s"><div><b>인턴 시아 · 층 안내</b><p id="gf-say">어서 오세요. 엘리베이터 버튼으로 층을 고르면 그 층에서 일어나는 공정과 해설을 안내해 드려요. 불이 켜진 층은 지금 읽을 수 있는 층이고, 회색 층은 공사 중이에요.</p></div></div>'
            '<div class="gf-lift" id="gf-lift" role="group" aria-label="층 고르기 (엘리베이터)"></div><div class="gf-info" id="gf-info" aria-live="polite"></div>'
            '<div class="gf-legend"><span><i style="background:#5ee39c"></i>연구실판 완성</span><span><i style="background:#82b8ff"></i>원본 그대로</span><span><i style="background:#f1b646"></i>다시 만드는 중</span><span><i style="background:#4a4e6a"></i>공사 중(준비 중)</span></div>'
            '</aside></div>'
            '<p class="gf-note">설명용 가상 공장입니다. 층과 기계는 책의 장·절과 해설 칸을 공정에 빗댄 것이며 실제 설비 배치가 아닙니다.</p>'
            '</section>' % img) + _scripts(cfg)


def floor_block(root, folder):
    """해설 페이지 첫 화면 — 이 페이지가 맡은 층."""
    i = floor_of(folder)
    if i is None:
        return ''
    W = world(root)
    f = W['floors'][i]
    cfg = {'mode': 'floor', 'focus': i, 'page': folder, 'base': '../', **W}
    me = [s for s in f['stations'] if s['page'] == folder]
    img = _guide_img()
    lead = ('여기는 <b>%s %s</b>이에요. %s. 이 해설은 이 층의 기계 %d대를 맡았어요. 번호를 누르면 그 칸으로 내려갑니다.'
            % (f['fl'], f['name'], f['process'].split(' — ')[-1].rstrip('.'), len(me)))
    return (START + '<style>' + _asset('factory.css') + '</style>'
            '<section class="gf gf-floor" id="factory" aria-label="인퍼런스 공장 — 이 페이지의 층">'
            '<div class="gf-grid"><div class="gf-stage"><div class="gf-cv" id="gf-cv" role="img" aria-label="%s %s 3D. 번호 붙은 기계가 이 페이지의 칸입니다."></div><div class="gf-labels" id="gf-labels" aria-hidden="true"></div>'
            '<div class="gf-err" id="gf-err">3D 층을 불러오지 못했습니다. 오른쪽 기계 목록으로 그대로 안내받을 수 있어요.</div>'
            '<div class="gf-tools"><a class="gf-bt" href="../index.html#f%d">건물 전체 보기 ↗</a><span class="gf-hint" id="gf-hint">끌어서 돌리기 · 휠로 확대</span></div></div>'
            '<aside class="gf-side"><p class="gf-eye">INFERENCE FACTORY · %s · %s</p><h2 class="gf-h2">%s %s</h2><p class="gf-proc">%s</p>'
            '<div class="gf-guide"><img alt="" aria-hidden="true" src="%s"><div><b>인턴 시아 · 공정 안내</b><p id="gf-say">%s</p></div></div>'
            '<ol class="gf-st" id="gf-st"></ol><div class="gf-mini" id="gf-mini" aria-label="건물 속 위치"></div></aside></div>'
            '</section>'
            % (f['fl'], f['name'], i, ('%d주차' % f['week']) if f['week'] else '부록', f['chap'], f['fl'], f['name'], f['process'], img, lead)) + _scripts(cfg) + END


def apply(page_html, root, folder):
    """페이지 HTML에 층 안내를 넣거나 바꾼다. 첫 </nav> 바로 뒤."""
    block = floor_block(root, folder)
    s = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda m: '', page_html, flags=re.S)
    if not block:
        return s
    k = s.find('</nav>')
    if k < 0:
        k = s.find('<body>')
        k = k + len('<body>') if k >= 0 else 0
    else:
        k += len('</nav>')
    return s[:k] + block + s[k:]


def korean_pages(root, folder):
    d = os.path.join(root, folder)
    out = []
    if not os.path.isdir(d):
        return out
    for n in sorted(os.listdir(d)):
        if not n.endswith('.html'):
            continue
        if n == 'index.html' or re.fullmatch(r'\d\d_[a-z_]+\.html', n):  # 언어판(.en.html 등)은 건드리지 않는다
            out.append(os.path.join(d, n))
    return out


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '../..'
    n = 0
    for f in FLOORS:
        for folder in dict.fromkeys(s[3] for s in f['st']):
            for path in korean_pages(root, folder):
                src = open(path, encoding='utf-8').read()
                new = apply(src, root, folder)
                if new != src:
                    open(path, 'w', encoding='utf-8').write(new)
                n += 1
                print('층 안내', os.path.relpath(path, root), f['fl'], f['name'])
    print(n, '페이지')
