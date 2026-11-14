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
