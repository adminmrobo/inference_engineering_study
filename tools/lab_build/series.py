# -*- coding: utf-8 -*-
"""스터디 북 시리즈 목록 — 목차(index)·README·cover_manifest가 함께 읽는 한 벌의 데이터."""
BASE = 'https://adminmrobo.github.io/inference_engineering_study/'
REPO = 'https://github.com/adminmrobo/inference_engineering_study'
OLD = 'https://github.com/adminmrobo/inference_engineering_study_'

# 책 장 (출판사 공개 목차 기준)
CHAPTERS = [
    (0, 'Inference', '추론이란', ['0 Inference']),
    (1, 'Prerequisites', '시작 전에 정할 것', ['1.1 Scale and Specialization', '1.2 About Your App', '1.3 Model Selection', '1.4 Measuring Latency and Throughput']),
    (2, 'Models', '모델', ['2.1 Neural Networks', '2.2 LLM Inference Mechanics', '2.3 Image Generation Inference Mechanics', '2.4 Calculating Inference Bottlenecks', '2.5 Optimizing Attention']),
    (3, 'Hardware', '하드웨어', ['3.1 GPU Architecture', '3.2 GPU Architecture Generations', '3.3 Instances', '3.4 Other Datacenter Accelerator Options', '3.5 Local Inference']),
    (4, 'Software', '소프트웨어', ['4.1 CUDA', '4.2 Deep Learning Frameworks and Libraries', '4.3 Inference Engines', '4.4 NVIDIA Dynamo', '4.5 Performance Benchmarking and Load Testing']),
    (5, 'Techniques', '최적화 기법', ['5.1 Quantization', '5.2 Speculative Decoding', '5.3 Caching', '5.4 Model Parallelism', '5.5 Disaggregation']),
    (6, 'Modalities', '입출력 유형', ['6.1 Vision Language Models', '6.2 Embedding Models', '6.3 ASR Models', '6.4 TTS Models', '6.5 Image Generation Models', '6.6 Video Generation Models']),
    (7, 'Production', '운영', ['7.1 Containerization', '7.2 Autoscaling', '7.3 Multi-Cloud Capacity Management', '7.4 Testing and Deployment', '7.5 Client Code', '7.6 Production Inference with Baseten']),
]

# status: done(연구실 스킬 재제작 완료) · kept(원본 그대로) · plan(예정) · wip(재제작 중)
# 폴더 이름 규칙: week_{NN}_textbook_{장·범위} / week_{NN}_article_{NN} / special_{NN}
WEEKS = [
    {'no': 1, 'title': '추론의 개념과 성능 평가', 'items': [
        {'kind': 'textbook', 'folder': 'week_01_textbook_preface', 'label': '서문', 'title': '추론은 이제 모두의 일', 'range': 'Preface', 'status': 'done', 'old': 'week_01_textbook_preface'},
        {'kind': 'textbook', 'folder': 'week_01_textbook_ch00', 'label': '0장', 'title': '추론이란 무엇인가', 'range': 'Chapter 0 Inference', 'status': 'done', 'old': 'week_01_textbook_ch00'},
        {'kind': 'textbook', 'folder': 'week_01_textbook_ch01', 'label': '1장', 'title': '시작 전에 정할 것', 'range': 'Chapter 1 Prerequisites 1.1–1.4', 'status': 'done', 'old': 'week_01_textbook_ch01'},
        {'kind': 'article', 'folder': 'week_01_article_01', 'label': '논문 1', 'title': '라이브벤치 — 새 시험지로만 재는 성적표', 'range': 'White et al. (ICLR 2025) LiveBench', 'status': 'done', 'old': 'week_01_article_01'}]},
    {'no': 2, 'title': '신경망과 언어 모델의 생성 과정', 'items': [
        {'kind': 'textbook', 'folder': 'week_02_textbook_ch02_p1_p2', 'label': '2장 전반', 'title': '모델 속 들여다보기', 'range': 'Chapter 2 Models 2.1–2.2', 'status': 'done', 'old': 'week_02_textbook_ch02_p1_p2'},
        {'kind': 'article', 'folder': 'week_02_article_01', 'label': '논문 1', 'title': '트랜스포머 — 어텐션만으로 충분하다', 'range': 'Vaswani et al. (2017) Attention Is All You Need', 'status': 'done', 'old': 'week_02_article_01'}]},
    {'no': 3, 'title': '이미지 생성과 추론 성능의 병목', 'items': [
        {'kind': 'textbook', 'folder': 'week_03_textbook_ch02_p3_to_end', 'label': '2장 후반', 'title': '병목을 찾아라', 'range': 'Chapter 2 Models 2.3–2.5', 'status': 'kept', 'old': 'week_03_textbook_ch02_p3_to_end'},
        {'kind': 'article', 'folder': 'week_03_article_01', 'label': '논문 1', 'title': '번개 어텐션 — 창고를 덜 오가면 빨라진다', 'range': 'Dao et al. (2022) FlashAttention', 'status': 'done', 'old': 'week_03_article_01'}]},
    {'no': 4, 'title': 'GPU 구조와 추론 실행 환경', 'items': [
        {'kind': 'textbook', 'folder': 'week_04_textbook_ch03', 'label': '3장', 'title': 'GPU 기계실 — 하드웨어', 'range': 'Chapter 3 Hardware 3.1–3.5', 'status': 'done'},
        {'kind': 'article', 'folder': 'week_04_article_01', 'label': '논문 1', 'title': '루프라인 — 지붕 두 개로 성능의 상한을 그린다', 'range': 'Williams, Waterman & Patterson (2008) Roofline', 'status': 'done'}]},
    {'no': 5, 'title': '추론 소프트웨어와 성능 측정', 'items': [
        {'kind': 'textbook', 'folder': 'week_05_textbook_ch04', 'label': '4장', 'title': '소프트웨어', 'range': 'Chapter 4 Software 4.1–4.5', 'status': 'plan'},
        {'kind': 'article', 'folder': 'week_05_article_01', 'label': '논문 1', 'title': '페이지드 어텐션 · vLLM (예정)', 'range': 'Kwon et al. (2023) PagedAttention', 'status': 'plan'}]},
    {'no': 6, 'title': '양자화와 추측 디코딩', 'items': [
        {'kind': 'textbook', 'folder': 'week_06_textbook_ch05_p1_p2', 'label': '5장 전반', 'title': '최적화 기법 ① 양자화·추측 디코딩', 'range': 'Chapter 5 Techniques 5.1–5.2', 'status': 'plan'},
        {'kind': 'article', 'folder': 'week_06_article_01', 'label': '논문 1', 'title': '추측 디코딩 논문 (예정)', 'range': 'DFlash (2026)', 'status': 'plan'}]},
    {'no': 7, 'title': '캐시 재사용과 모델 병렬화', 'items': [
        {'kind': 'textbook', 'folder': 'week_07_textbook_ch05_p3_to_end', 'label': '5장 후반', 'title': '최적화 기법 ② 캐시·병렬화·분리', 'range': 'Chapter 5 Techniques 5.3–5.5', 'status': 'plan'},
        {'kind': 'article', 'folder': 'week_07_article_01', 'label': '논문 1', 'title': 'SGLang (예정)', 'range': 'Zheng et al. (2023) SGLang', 'status': 'plan'}]},
    {'no': 8, 'title': '입출력 유형에 따른 모델과 추론 방식', 'items': [
        {'kind': 'textbook', 'folder': 'week_08_textbook_ch06', 'label': '6장', 'title': '입출력 유형', 'range': 'Chapter 6 Modalities 6.1–6.6', 'status': 'plan'},
        {'kind': 'article', 'folder': 'week_08_article_01', 'label': '논문 1', 'title': 'LLaVA (예정)', 'range': 'Liu et al. (2023) Visual Instruction Tuning', 'status': 'plan'}]},
    {'no': 9, 'title': '서비스 배포와 요청량에 따른 자원 조절', 'items': [
        {'kind': 'textbook', 'folder': 'week_09_textbook_ch07_p1_p2', 'label': '7장 전반', 'title': '운영 ① 컨테이너·자동 확장', 'range': 'Chapter 7 Production 7.1–7.2', 'status': 'plan'},
        {'kind': 'article', 'folder': 'week_09_article_01', 'label': '논문 1', 'title': 'Orca (예정)', 'range': 'Yu et al. (2022) Orca', 'status': 'plan'}]},
    {'no': 10, 'title': '추론 서비스의 안정적 운영과 전체 복습', 'items': [
        {'kind': 'textbook', 'folder': 'week_10_textbook_ch07_p3_to_end', 'label': '7장 후반', 'title': '운영 ② 멀티 클라우드·배포·클라이언트', 'range': 'Chapter 7 Production 7.3–7.6', 'status': 'plan'},
        {'kind': 'article', 'folder': 'week_10_article_01', 'label': '논문 1', 'title': 'AgentDojo (예정)', 'range': 'Debenedetti et al. (2024) AgentDojo', 'status': 'plan'}]},
]
SPECIALS = [
    {'folder': 'special_01', 'label': '부록 A', 'title': '특별편 1 (주제 준비 중)', 'status': 'plan'},
    {'folder': 'special_02', 'label': '부록 B', 'title': '특별편 2 (주제 준비 중)', 'status': 'plan'},
    {'folder': 'special_03', 'label': '부록 C', 'title': '특별편 3 (선택, 주제 준비 중)', 'status': 'plan'},
]
STATUS_KO = {'done': '연구실판 완성', 'kept': '원본 그대로', 'plan': '준비 중', 'wip': '다시 만드는 중'}

# ── 추론 공정 제어판 ───────────────────────────────────────────────
# "그래서 GPU로 LLM을 어떻게 돌리나?"에 대한 책 전체의 답을 한 장의 제어판으로 정리한 것.
# 목차 첫 화면(build_index)과 각 해설 첫 화면(factory.floor_block), 목록 카드(cards.py)가 함께 읽는다.
FLOW = [  # (키, 이름, 한 줄)
    ('goal', '목표 정하기', '빨리(지연시간) · 많이(처리량) · 싸게(비용) 중 무엇을 먼저 지킬까'),
    ('model', '모델 성질 보기', '질문 읽기(프리필)는 계산이 막히고, 한 토큰씩 쓰기(디코드)는 메모리 통로가 막힌다'),
    ('hw', '기계 맞추기', '모델이 VRAM에 들어가나, 메모리 대역폭은 충분한가'),
    ('dial', '다이얼 돌리기', '아래 다섯 다이얼을 목표에 맞춰 조절한다'),
    ('measure', '재고 병목 찾기', '계기판(TTFT · TPS · P99)과 루프라인으로 막힌 곳을 찾고 → 다시 ②로'),
]
DIALS = [  # (키, 이름, 무엇을 정하나, 돌리면)
    ('batch', '배치', '한 번에 몇 주문을 함께 돌릴까', '많이 묶을수록 처리량은 오르고, 주문 하나의 기다림은 길어질 수 있다'),
    ('precision', '정밀도', '숫자를 몇 자리로 담을까 (양자화)', '작게 담으면 메모리와 속도에서 이득, 품질은 다시 재 봐야 한다'),
    ('kv', 'KV 캐시', '앞 토큰의 메모를 어떻게 쌓고 다시 쓸까', '메모가 길고 많을수록 GPU 메모리를 차지한다'),
    ('split', '나눠 싣기', '모델과 공정을 GPU 여러 대에 어떻게 나눌까 (병렬화 · 분리)', '한 대에 안 들어가거나 더 빨라야 할 때 쓴다'),
    ('kernel', '계산 방식', '같은 답을 어떤 순서로 계산할까 (커널)', '메모리 왕복을 줄이면 답은 같고 빨라진다'),
]
# 폴더별 카드: chap(목록 묶음 = 책의 장) · card(목록 소개 한 줄, "이 편을 읽으면 …") · flow · dials · so("그래서" 한 줄)
CARDS = {
    'week_01_textbook_preface': dict(chap='서문', card='이 편을 읽으면 추론이 왜 모두의 일이 됐는지 지연시간 · 가용성 · 비용 세 저울로 설명할 수 있습니다.',
        flow=['goal'], dials={},
        so='다이얼을 만지기 전에 무엇을 위해 돌리는지부터 정합니다. 이 편의 세 저울이 제어판의 목표 눈금이에요.'),
    'week_01_textbook_ch00': dict(chap='0장', card='이 편을 읽으면 학습과 추론을 나누고, 추론 일이 놓인 세 층(런타임 · 인프라 · 도구)을 짚을 수 있습니다.',
        flow=['goal'], dials={'precision': '런타임 층 — 모델을 실제로 돌리는 소프트웨어에서 정합니다.', 'kernel': '런타임 층 — 같은 답을 내는 계산 순서도 여기서 바꿉니다.',
                              'split': '인프라 층 — GPU 몇 대를 어떻게 묶어 쓸지 정합니다.'},
        so='다섯 다이얼이 공장의 어느 층에 붙어 있는지 위치를 익히는 편입니다.'),
    'week_01_textbook_ch01': dict(chap='1장', card='이 편을 읽으면 우리 앱에 맞는 모델과 목표 눈금(TTFT · TPS · P99)을 정할 수 있습니다.',
        flow=['goal', 'measure'], dials={'batch': '처리량과 지연시간은 서로 당기는 줄다리기 — 배치 다이얼은 이 두 눈금을 보며 돌립니다.'},
        so='다이얼을 돌리기 전에 계기판부터 답니다. 무엇을 재는지 정해야 돌린 결과가 나아졌는지 알 수 있어요.'),
    'week_01_article_01': dict(chap='1장', paper='LiveBench', card='이 편을 읽으면 문제가 새어 나간 시험지와 매달 바뀌는 새 시험지의 차이로, 모델 성적을 믿을 만하게 재는 법을 설명할 수 있습니다.',
        flow=['goal', 'measure'], dials={'precision': '정밀도를 낮추거나 모델을 바꾼 뒤 품질이 버티는지 잴 때 이런 시험지가 필요합니다.'},
        so='다이얼은 속도를 바꾸지만 품질도 흔들 수 있어요. 이 편은 품질 계기판을 고르는 법입니다.'),
    'week_02_textbook_ch02_p1_p2': dict(chap='2장', card='이 편을 읽으면 질문 한 줄이 토큰으로 쪼개져 모델을 지나 다음 토큰 하나로 나오기까지를 따라갈 수 있습니다.',
        flow=['model'], dials={'kv': 'KV 캐시가 처음 나옵니다 — 앞 토큰을 매번 다시 계산하지 않으려고 쌓아 두는 메모예요.',
                               'batch': '질문 읽기(프리필)와 한 토큰씩 쓰기(디코드)는 성질이 달라서 배치의 효과도 다릅니다.',
                               'precision': '모델이 하는 일 대부분이 숫자 표 곱하기라, 숫자 크기가 곧 메모리와 속도입니다.'},
        so='모델 안의 공정을 알아야 다이얼 손잡이마다 무슨 뜻인지 보입니다.'),
    'week_02_article_01': dict(chap='2장', paper='Transformer', card='이 편을 읽으면 어텐션이 문장의 어디를 볼지 고르는 원리와, 문장이 길수록 일이 커지는 이유를 설명할 수 있습니다.',
        flow=['model'], dials={'kv': '어텐션의 키 · 값이 바로 KV 캐시에 쌓이는 메모입니다.',
                               'kernel': '어텐션 계산은 문장이 길수록 크게 늘어서, 계산 방식 다이얼의 주된 대상이 됩니다.'},
        so='오늘날 LLM의 출발점입니다. KV 캐시와 계산 방식, 두 다이얼이 바로 이 구조에서 나와요.'),
    'week_03_textbook_ch02_p3_to_end': dict(chap='2장', card='이 편을 읽으면 느린 원인이 계산(요리사)인지 메모리 통로(재료 통로)인지 판정할 수 있습니다.',
        flow=['model', 'measure'], dials={'batch': '주문을 여러 개 묶으면 한 번 꺼낸 재료로 더 많이 요리해 메모리 통로 병목이 덜해집니다.',
                                          'kernel': '메모리 왕복을 줄이는 어텐션 최적화가 이 편 끝에 나옵니다.'},
        so='다이얼을 아무거나 돌리지 않으려면 어디가 막혔는지부터 판정해야 합니다. 이 편이 그 진단법이에요.'),
    'week_03_article_01': dict(chap='2장', paper='FlashAttention', card='이 편을 읽으면 답은 그대로 두고 작은 창고와 큰 창고 사이 왕복만 줄여 어텐션을 빠르게 하는 원리를 설명할 수 있습니다.',
        flow=['dial'], dials={'kernel': '계산 방식 다이얼의 대표 사례 — 타일로 쪼개 작은 창고(SRAM) 안에서 끝내고 큰 창고(HBM) 왕복을 줄입니다.'},
        so='모델은 그대로, 계산 순서만 바꿔 빨라지는 다이얼입니다. 모델 구조(어텐션)와 GPU 구조(메모리 계층)를 둘 다 알아야 돌릴 수 있어요.'),
    'week_04_textbook_ch03': dict(chap='3장', card='이 편을 읽으면 모델이 어떤 GPU에 들어가고 얼마나 빠를지 VRAM과 메모리 대역폭으로 어림할 수 있습니다.',
        flow=['hw'], dials={'split': '한 대에 안 들어가면 여러 대로 — NVLink로 묶인 인스턴스가 나눠 싣기의 무대입니다.',
                            'precision': '숫자를 작게 담으면 같은 VRAM에 더 큰 모델이 들어갑니다.',
                            'kv': '모델 무게를 싣고 남은 VRAM이 KV 캐시 자리 — 동시에 받을 수 있는 주문 수를 정합니다.'},
        so='다이얼이 붙은 기계 자체를 아는 편입니다. VRAM과 대역폭이 다이얼을 어디까지 돌릴 수 있는지 정해요.'),
    'week_04_article_01': dict(chap='3장', paper='Roofline', card='이 편을 읽으면 지붕선 두 개로 성능의 상한을 그리고, 어떤 최적화부터 할지 고를 수 있습니다.',
        flow=['measure'], dials={'batch': '작업 강도를 올려 경사 지붕(메모리) 구간에서 평평한 지붕(계산) 쪽으로 옮깁니다.',
                                 'kernel': '최적화 하나마다 천장이 한 칸씩 뚫립니다 — 남은 다이얼이 무엇인지 보여 줘요.'},
        so='제어판의 계기판입니다. 지금 점이 지붕 어디에 있는지 보면 다음에 돌릴 다이얼이 정해집니다.'),
}
