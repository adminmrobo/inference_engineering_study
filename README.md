# 인퍼런스 스터디 북 — 연구실 식구들과 읽는 『Inference Engineering』

> AI 모델을 더 빠르고, 더 싸고, 더 안정적으로 돌리려면 무엇을 알아야 할까?

『Inference Engineering』(Philip Kiely, Baseten Books, 2026)을 10주 동안 주차마다 **교재 한 꼭지 + 논문 한 편**씩 읽고, 연구실 식구들(박사 · 조수(하루) · 초파리 연구원 · 주판봇 · 인턴 시아 · 인턴 모아, 그리고 방청석의 미공개 셋)이 진행하는 해설 페이지로 만든 스터디 북입니다.

- **표지·목차 (바로 읽기):** https://adminmrobo.github.io/inference_engineering_study/
- 주차별 해설은 모두 이 저장소의 폴더 하나씩입니다. 예전 주차별 저장소(`inference_engineering_study_week_…`)는 그대로 남아 있지만, 이제 이 저장소의 폴더가 정식 주소입니다.

## 목차

| 주차 | 구분 | 제목 | 폴더 | 상태 |
|---|---|---|---|---|
| 1주차 | 교재 · 서문 | 추론은 이제 모두의 일 | [week_01_textbook_preface](week_01_textbook_preface/) | 연구실판 완성 |
| 1주차 | 교재 · 0장 | 추론이란 무엇인가 | [week_01_textbook_ch00](week_01_textbook_ch00/) | 연구실판 완성 |
| 1주차 | 교재 · 1장 | 시작 전에 정할 것 | [week_01_textbook_ch01](week_01_textbook_ch01/) | 연구실판 완성 |
| 1주차 | 논문 · 논문 1 | 라이브벤치 — 새 시험지로만 재는 성적표 | [week_01_article_01](week_01_article_01/) | 연구실판 완성 |
| 2주차 | 교재 · 2장 전반 | 모델 속 들여다보기 | [week_02_textbook_ch02_p1_p2](week_02_textbook_ch02_p1_p2/) | 연구실판 완성 |
| 2주차 | 논문 · 논문 1 | 트랜스포머 — 어텐션만으로 충분하다 | [week_02_article_01](week_02_article_01/) | 연구실판 완성 |
| 3주차 | 교재 · 2장 후반 | 병목을 찾아라 | [week_03_textbook_ch02_p3_to_end](week_03_textbook_ch02_p3_to_end/) | 원본 그대로 |
| 3주차 | 논문 · 논문 1 | 번개 어텐션 — 창고를 덜 오가면 빨라진다 | [week_03_article_01](week_03_article_01/) | 연구실판 완성 |
| 4주차 | 교재 · 3장 | 하드웨어 | `week_04_textbook_ch03/` (예정) | 준비 중 |
| 4주차 | 논문 · 논문 1 | 루프라인 모델 (예정) | `week_04_article_01/` (예정) | 준비 중 |
| 5주차 | 교재 · 4장 | 소프트웨어 | `week_05_textbook_ch04/` (예정) | 준비 중 |
| 5주차 | 논문 · 논문 1 | 페이지드 어텐션 · vLLM (예정) | `week_05_article_01/` (예정) | 준비 중 |
| 6주차 | 교재 · 5장 전반 | 최적화 기법 ① 양자화·추측 디코딩 | `week_06_textbook_ch05_p1_p2/` (예정) | 준비 중 |
| 6주차 | 논문 · 논문 1 | 추측 디코딩 논문 (예정) | `week_06_article_01/` (예정) | 준비 중 |
| 7주차 | 교재 · 5장 후반 | 최적화 기법 ② 캐시·병렬화·분리 | `week_07_textbook_ch05_p3_to_end/` (예정) | 준비 중 |
| 7주차 | 논문 · 논문 1 | SGLang (예정) | `week_07_article_01/` (예정) | 준비 중 |
| 8주차 | 교재 · 6장 | 입출력 유형 | `week_08_textbook_ch06/` (예정) | 준비 중 |
| 8주차 | 논문 · 논문 1 | LLaVA (예정) | `week_08_article_01/` (예정) | 준비 중 |
| 9주차 | 교재 · 7장 전반 | 운영 ① 컨테이너·자동 확장 | `week_09_textbook_ch07_p1_p2/` (예정) | 준비 중 |
| 9주차 | 논문 · 논문 1 | Orca (예정) | `week_09_article_01/` (예정) | 준비 중 |
| 10주차 | 교재 · 7장 후반 | 운영 ② 멀티 클라우드·배포·클라이언트 | `week_10_textbook_ch07_p3_to_end/` (예정) | 준비 중 |
| 10주차 | 논문 · 논문 1 | AgentDojo (예정) | `week_10_article_01/` (예정) | 준비 중 |
| 부록 | 부록 A | 특별편 1 (주제 준비 중) | `special_01/` (예정) | 준비 중 |
| 부록 | 부록 B | 특별편 2 (주제 준비 중) | `special_02/` (예정) | 준비 중 |
| 부록 | 부록 C | 특별편 3 (선택, 주제 준비 중) | `special_03/` (예정) | 준비 중 |

## 규칙

- 폴더 이름 = 옛 저장소 이름에서 `inference_engineering_study_`를 뺀 것: `week_{주차}_textbook_{장·범위}`, `week_{주차}_article_{번호}`, 부록은 `special_{번호}`.
- 한 주에 장이 바뀌면 장마다 따로 만든다(예: 3장, 5장, 7장). 큰 장은 범위로 나눈다(`_p1_p2`, `_p3_to_end`).
- 3주차 교재편(`week_03_textbook_ch02_p3_to_end/`)은 먼저 완성된 원본을 내용 수정 없이 그대로 옮겼다.
- 나머지 페이지는 연구실 해설 스킬(ai-lab-explainer v1.12, 캐릭터 팩 1.4) 규격으로 식구 전원이 나오도록 다시 적용했다.
- 페이지는 단일 HTML(외부 요청은 글꼴뿐), 페이지마다 지식 색인(`#kg`)과 온톨로지·서지 꾸러미(`#export`)가 있다.
- 글 표지는 지금 대체 표지(여섯 식구 표정 그림 줄 세우기)이고, 그림 지시문은 폴더마다 `COVER_*.md`에 있다.

## 다시 만들기

```bash
cd tools/lab_build
python3 build_index.py ../..                    # 목차
python3 pages/p_preface.py ../..                # 1주차 서문 (p_ch00, p_ch01, p_livebench 같은 방식)
python3 run_retrofit.py <옛 저장소 사본 폴더> ../..  # 2·3주차 페이지에 식구 전원 더하기
python3 docs.py ../..                           # README·표지 지시문·cover_manifest.json
```

캐릭터 그림은 `adminmrobo/ahnboat_lab_explainer`의 캐릭터 팩(`LAB_PACK` 환경 변수로 위치 지정)에서 읽습니다.

글 · 안상선 ((주)M-Robo 대표) · 교재와 논문의 요약·해설이며 원문을 대신하지 않습니다. 캐릭터 설정·그림은 저작권자 허락 없이 사용할 수 없습니다.
