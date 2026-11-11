# -*- coding: utf-8 -*-
"""2주차 교재·논문, 3주차 논문 페이지에 식구 전원을 더한다. 사용: python3 run_retrofit.py <원본 저장소들 폴더> <스터디 북 루트>"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retrofit import retrofit

SRC, ROOT = sys.argv[1], sys.argv[2]
MOT = lambda pat: ''.join('<i class="%s"></i>' % c for c in pat)
CFG = {
 'week_02_textbook_ch02_p1_p2': dict(file='02_models.html', cover_key='cover_ch2', chip='인퍼런스 스터디 북 · 2주차 · 2장 전반',
    alt='연구실 식구 여섯이 주방 같은 실험실에서 주문서와 접시(토큰)를 바라보는 대체 표지', moods={'doc': 'front', 'asst': 'smile', 'fly': 'point', 'robo': 'chart', 'sia': 'guide', 'moa': 'tea'},
    motif=MOT(['on', 'on', 'm', 'm', 'a', 'on', 'on', 'm', 'm', 'a', 'on', 'on']),
    sia_hero='순서는 다섯 칸입니다. 행렬곱 → 활성화 → 토큰 → 어텐션·KV 캐시 → MoE. 칸마다 실험이 하나씩 있어요.',
    moa_hero='주방 비유가 나와요! 밑손질해 둔 재료통이 KV 캐시래요. 차 한 잔 하시면서 천천히요.',
    cast_id='cast', duel_id='duel', sum_id='summary',
    roles={'sia': '순서 정리·진행 신호. 다섯 칸 안내', 'moa': '기록 모으기·응원. 정리의 기록장'},
    route=[('why', '도입', '왜 모델 속을'), ('lv1', '① 칸', '행렬곱'), ('lv2', '② 칸', '활성화'), ('lv3', '③ 칸', '토큰'), ('lv4', '④ 칸', '어텐션·KV'), ('lv5', '⑤ 칸', 'MoE'), ('duel', '대결', ''), ('summary', '정리', '')],
    notebook=['선형층 두 개는 행렬곱으로 한 층에 접힌다 → 활성화 함수가 접힘을 막는다', '대부분 모델의 어휘 크기는 100,000개 이상', 'Qwen3: 전체 235B 중 요청당 22B 활성, 전문가 128명 중 8명, 94층', '추론 시간 대부분은 프리필(KV 캐시 만들기)과 디코드(로짓 만들기)'],
    moa_sum='2주차 교재 끝! 같은 주의 논문은 트랜스포머(Attention Is All You Need)예요.'),
 'week_02_article_01': dict(file='01_transformer.html', cover_key='cover_01', chip='인퍼런스 스터디 북 · 2주차 · 논문',
    alt='연구실 식구 여섯이 문장 카드 위로 뻗는 형광펜 빛줄기를 바라보는 대체 표지', moods={'doc': 'think', 'asst': 'smile', 'fly': 'point', 'robo': 'chart', 'sia': 'explain', 'moa': 'sparkle'},
    motif=MOT(['m', 'on', 'm', 'on', 'a', 'on', 'm', 'on', 'm', 'on', 'a', 'on']),
    sia_hero='논문 순서대로 갑니다. 질문 → 방법 → 결과 넷 → 모형 실험실 → 대결 → 다시 읽기.',
    moa_hero='형광펜 색이 여러 개래요(여러 머리). 저는 색깔별로 기록해 둘게요!',
    cast_id='cast', duel_id='duel', sum_id='onepage',
    roles={'sia': '논문 순서 안내·진행 신호', 'moa': '기록장·응원'},
    route=[('q', '1', '질문'), ('method', '2', '방법'), ('r1', '결과', '①'), ('r2', '결과', '②'), ('r3', '결과', '③'), ('r4', '결과', '④'), ('lab', '실험실', ''), ('duel', '대결', ''), ('reread', '다시 읽기', ''), ('onepage', '한 장', '')],
    notebook=['영→독 BLEU 28.4, 영→불 41.8 (표 2, 시험 세트 newstest2014)', '영→불 big 점수는 논문 안에서 41.8(초록·표 2)과 41.0(6.1절)으로 다르게 적혀 있음', '표 3은 개발 세트(newstest2013) — 표 2와 섞어 비교하지 않기', '"머리가 문법을 배운다"는 저자의 해석'],
    moa_sum='2주차 끝! 3주차는 2장 후반(병목)과 번개 어텐션이에요.'),
 'week_03_article_01': dict(file='03_flash_attention.html', cover_key='cover_03', chip='인퍼런스 스터디 북 · 3주차 · 논문',
    alt='연구실 식구 여섯이 작은 실험대와 복도 끝 큰 창고 사이에서 블록 쟁반을 나르는 대체 표지', moods={'doc': 'think', 'asst': 'firm', 'fly': 'magnify', 'robo': 'calc', 'sia': 'guide', 'moa': 'smile'},
    motif=MOT(['on', 'on', 'on', 'on', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']),
    sia_hero='논문 순서대로 갑니다. 질문 → 방법 → 결과 셋 → 모형 실험실 → 대결 → 다시 읽기.',
    moa_hero='창고와 실험대 사이를 몇 번 오가는지가 오늘의 핵심이래요. 쟁반 나르기는 저도 자신 있어요!',
    cast_id='cast', duel_id='duel', sum_id='summary',
    roles={'sia': '논문 순서 안내·진행 신호', 'moa': '기록장·응원'},
    route=[('q', '1', '질문'), ('method', '2', '방법'), ('r1', '결과 ①', '창고 왕복'), ('r2', '결과 ②', '온라인 소프트맥스'), ('r3', '결과 ③', '속도·메모리'), ('lab', '실험실', ''), ('duel', '대결', ''), ('reread', '다시 읽기', ''), ('summary', '한 장', '')],
    notebook=['SRAM 약 19TB/s · 20MB, HBM 1.5TB/s · 40GB (그림 1, A100)', 'GPT-2 medium: 창고 R/W 40.3 → 4.4GB, 41.7 → 7.3ms, GFLOPs 66.6 → 75.2 (그림 2 왼쪽)', '창고 접근: 표준 Θ(Nd+N²) vs 번개 Θ(N²d²/M) (정리 2)', '번개 어텐션은 근사가 아니다 — 블록 희소판만 근사'],
    moa_sum='3주차 끝! 4주차는 3장 하드웨어예요. 이제 GPU 자체를 들여다봐요.'),
}

for folder, c in CFG.items():
    src_dir = os.path.join(SRC, folder); dst = os.path.join(ROOT, folder)
    html = open(os.path.join(src_dir, c['file']), encoding='utf-8').read()
    if 'lab-crew' in html:
        print('skip (already)', folder); continue
    out = retrofit(html, c)
    if folder == 'week_02_article_01':
        out = out.replace('AbaBot', '주판봇')
    open(os.path.join(dst, c['file']), 'w', encoding='utf-8').write(out)
    open(os.path.join(dst, 'index.html'), 'w', encoding='utf-8').write(out)
    print(folder, len(out.encode()))
