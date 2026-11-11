# 진짜 실력인가, 기출 암기인가? — LiveBench 해설 대시보드
**AI Lab Explainer Series · LB-01**

**[한국어](#ko) · [English](#en) · [中文](#zh) · [日本語](#ja) · [Oʻzbekcha](#uz) · [Русский](#ru) · [Tiếng Việt](#vi)**

---

<a id="ko"></a>
## 한국어

ICLR 2025에 발표된 LLM 벤치마크 논문 「LiveBench: A Challenging, Contamination-Limited LLM Benchmark」(Colin White, Samuel Dooley, Manley Roberts, Arka Pal et al.)을 연구실 네 친구들 — 박사 · 조수 세라 · 초파리 연구원 · 주판봇 — 의 대화로 풀어 설명하는 인터랙티브 대시보드다.

"AI가 시험을 미리 외웠다면 그 점수는 진짜 실력일까?"라는 질문에서 시작해, 데이터 오염(기출 과적합)이 점수를 어떻게 부풀리는지 직접 실험하고, LiveBench가 매월 문제를 갈아 끼우고 LLM 판사를 배제하는 이유를 눈으로 확인한다.

- **바로 보기**: https://adminmrobo.github.io/&lt;저장소&gt;/ ← 저장소 이름을 정한 뒤 &lt;저장소&gt;를 바꿔 넣는다
- **저자**: 글 · 그림 — 안상선 ((주)M-Robo 대표)

### 구성
| 편 | 제목 | 다루는 내용 | 난이도 |
|---|---|---|---|
| LB-01 | 진짜 실력인가, 기출 암기인가? | 데이터 오염 · 벤치마크 갱신 · 객관적 채점 | ★★★ |

### 핵심 숫자 (논문 기반, 대시보드 표시값)
| 숫자 | 뜻 |
|---|---|
| 64.7% | 최고 성능 모델(o1-preview)의 LiveBench 점수 |
| 44.8% | 기출에 과적합된 모델의 점수 |
| −19.9%p | 두 모델의 격차 — 기출 암기 거품의 크기 |
| 1/6 | 매월 갱신되는 문제 비율 |
| 0회 | LLM 판사 사용 횟수(객관 정답 자동 채점) |

### 페이지에 들어 있는 것
- 인터랙티브 실습 4종: 오염도 시뮬레이터 · 6개 영역 레이더 · LLM 판사 오류율 · 대결 시뮬레이션
- 확인 퀴즈 2문항, 학습 진도 추적
- 픽셀아트 일러스트 11장 내장(base64) — 외부 파일·네트워크 없이 동작

### 파일
```
LiveBench_해설_대시보드.html   본문 (그림·스크립트 전부 내장)
README.md · INDEX.md
LiveBench_해설_대시보드.{en,zh,ja,uz,ru,vi}.html   6개 언어판
images/                        원본 PNG 11장 (본문에는 전부 내장되어 있음)
image_prompts_lb.md            이미지 생성 프롬프트 전문
```

### 데이터와 이미지 (설명용 모형인 것)
- 일러스트 11장은 모두 생성 AI로 만든 설명용 픽셀아트다. 그림 속 글자는 없다.
- 실습 시뮬레이터의 기준 숫자는 논문 발표 값(64.7% / 44.8%)이고, 브라우저 애니메이션은 실행마다 조금씩 달라질 수 있다.
- 실제 사람 데이터는 사용하지 않았다.

### 언어
| 언어 | 파일 | 상태 |
|---|---|---|
| 한국어 (원본) | LiveBench_해설_대시보드.html | 준비됨 |
| English | LiveBench_해설_대시보드.en.html | 완료 |
| 中文 | LiveBench_해설_대시보드.zh.html | 완료 |
| 日本語 | LiveBench_해설_대시보드.ja.html | 완료 |
| Oʻzbekcha | LiveBench_해설_대시보드.uz.html | 완료 |
| Русский | LiveBench_해설_대시보드.ru.html | 완료 |
| Tiếng Việt | LiveBench_해설_대시보드.vi.html | 완료 |

### 용어 표기
- **데이터 오염(contamination)** — 평가 문제가 학습 데이터에 미리 섞여 들어간 것. "기출 과적합"과 같은 뜻으로 통일해 쓴다.
- **LLM 판사(LLM-as-judge)** — 다른 AI에게 채점을 맡기는 방식. "편향된 채점관" 비유로 통일.

### 라이선스
- 코드: Apache License 2.0 / 콘텐츠·이미지: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.ko) (페이지 메타에는 CC BY 4.0으로도 표기됨 — 하나로 통일 권장)
- 출처 표기 예: 「LiveBench 해설 대시보드」 LB-01, 안상선, CC BY-SA 4.0
- 원 논문: White et al., "LiveBench: A Challenging, Contamination-Limited LLM Benchmark", ICLR 2025

---

<a id="en"></a>
## English

An interactive dashboard that explains the ICLR 2025 paper "LiveBench: A Challenging, Contamination-Limited LLM Benchmark" (Colin White, Samuel Dooley, Manley Roberts, Arka Pal et al.) through a lab crew of four: the Doctor, the Assistant (Sera), the Fruit Fly Researcher, and AbaBot.

It starts from one question — "If an AI memorized the exam in advance, is its score real ability?" — and lets you run the experiments yourself: how data contamination (overfitting to past exams) inflates scores, and why LiveBench refreshes its problems every month and excludes LLM judges.

- **Read it here**: https://adminmrobo.github.io/&lt;repository&gt;/ ← replace &lt;repository&gt; once the repo name is fixed
- **Author**: Written & illustrated by Ahn Sangsun (CEO, M-Robo Co., Ltd.)

### Lineup
| Episode | Title | Topics | Level |
|---|---|---|---|
| LB-01 | Real Skill or Memorized Exams? | Data contamination · benchmark refresh · objective scoring | ★★★ |

### Key numbers (from the paper, as shown on the dashboard)
| Number | Meaning |
|---|---|
| 64.7% | Best model's (o1-preview) LiveBench score |
| 44.8% | Score of a model overfit to past exams |
| −19.9pp | The gap — the size of the memorization bubble |
| 1/6 | Share of problems refreshed monthly |
| 0 | Number of LLM-judge uses (objective ground-truth scoring) |

### What's inside
- 4 interactive labs: contamination simulator · 6-area radar · LLM-judge error rates · duel simulation
- 2 check quizzes, study-progress tracking
- 11 embedded pixel-art illustrations (base64) — works fully offline

### Files
```
LiveBench_해설_대시보드.html   the page (all images & scripts embedded)
README.md · INDEX.md
LiveBench_해설_대시보드.{en,zh,ja,uz,ru,vi}.html   6개 언어판
images/                        11 original PNGs (already embedded in the page)
image_prompts_lb.md            full image-generation prompts
```

### Data & images (what is an illustrative mock-up)
- All 11 illustrations are AI-generated pixel art for explanation; no letters appear inside the images.
- Simulator baselines follow the paper's values (64.7% / 44.8%); browser animation may vary slightly between runs.
- No real human data is used.

### Languages
| Language | File | Status |
|---|---|---|
| 한국어 (original) | LiveBench_해설_대시보드.html | Ready |
| English | LiveBench_해설_대시보드.en.html | Ready |
| 中文 / 日本語 / Oʻzbekcha / Русский / Tiếng Việt | *.zh.html / *.ja.html / *.uz.html / *.ru.html / *.vi.html | Ready |

### Terms
- **Data contamination** — evaluation problems leaked into training data. Used interchangeably with "overfitting to past exams".
- **LLM judge (LLM-as-judge)** — having another AI do the grading; consistently paraphrased as "a biased grader".

### License
- Code: Apache License 2.0 · Text & images: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en) (the page meta also shows CC BY 4.0 — pick one)
- Attribution example: "LiveBench Explainer Dashboard" LB-01, Ahn Sangsun, CC BY-SA 4.0

---

<a id="zh"></a>
## 中文

一个交互式讲解页面，用研究室的四位成员——博士、助手Sera、果蝇研究员和算盘宝——的对话来讲解 ICLR 2025 论文《LiveBench: A Challenging, Contamination-Limited LLM Benchmark》（Colin White、Samuel Dooley、Manley Roberts、Arka Pal 等）。

从"如果 AI 提前背下了考题，这个分数还算真实实力吗？"这个问题出发，你将亲手做实验，看看数据污染（对旧题的过拟合）如何抬高分数，并直观理解 LiveBench 为什么每月更新题目、为什么不使用 LLM 评委。

- **在线阅读**：https://adminmrobo.github.io/&lt;repository&gt;/ ←（确定仓库名后替换）
- **作者**：文 · 图 — Ahn Sangsun（M-Robo 株式会社代表）

### 构成
| 篇 | 标题 | 内容 | 难度 |
|---|---|---|---|
| LB-01 | 真本事，还是背旧题？ | 数据污染 · 基准更新 · 客观评分 | ★★★ |

### 关键数字（来自论文，即页面显示值）
| 数字 | 含义 |
|---|---|
| 64.7% | 最强模型（o1-preview）的 LiveBench 得分 |
| 44.8% | 对旧题过拟合的模型的得分 |
| −19.9pp | 两者差距——死记硬背泡沫的大小 |
| 1/6 | 每月更新的题目比例 |
| 0次 | LLM 评委使用次数（用客观正确答案自动评分） |

### 页面内容
- 4 个互动实验：污染度模拟器 · 6 领域雷达图 · LLM 评委错误率 · 对决模拟
- 2 道检查题、学习进度跟踪
- 内置 11 幅像素画（base64）——无需外部文件即可运行

### 文件
```
LiveBench_해설_대시보드.html   正文（图像、脚本全部内嵌）
README.md · INDEX.md
LiveBench_해설_대시보드.{en,zh,ja,uz,ru,vi}.html   6개 언어판
images/                        11 张原始 PNG（已内嵌于正文）
image_prompts_lb.md            图像生成提示词全文
```

### 数据与图像（仅供说明的示意部分）
- 11 幅插图均为 AI 生成的说明用像素画，图内没有任何文字。
- 模拟器的基准数字采用论文发表值（64.7% / 44.8%），浏览器动画每次运行可能略有不同。
- 未使用真实人物数据。

### 语言
| 语言 | 文件 | 状态 |
|---|---|---|
| 한국어（原文） | LiveBench_해설_대시보드.html | 已就绪 |
| 中文 | LiveBench_해설_대시보드.zh.html | 已就绪 |
| English / 日本語 / Oʻzbekcha / Русский / Tiếng Việt | *.en.html / *.ja.html / *.uz.html / *.ru.html / *.vi.html | 已就绪 |

### 术语
- **数据污染（contamination）**——评测题目混入训练数据。与"对旧题过拟合"同义使用。
- **LLM 评委（LLM-as-judge）**——让另一个 AI 批改。"有偏见的评分员"的比喻贯穿全篇。

### 许可
- 代码：Apache License 2.0 · 文字与图像：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hans)（页面元数据中亦标为 CC BY 4.0——建议统一）
- 署名示例：《LiveBench 讲解仪表盘》LB-01，Ahn Sangsun，CC BY-SA 4.0

---

<a id="ja"></a>
## 日本語

ICLR 2025で発表されたLLMベンチマーク論文「LiveBench: A Challenging, Contamination-Limited LLM Benchmark」（Colin White、Samuel Dooley、Manley Roberts、Arka Pal ら）を、研究室の仲間四人——博士・助手セラ・ショウジョウバエ研究員・アバボット——の対話で解説するインタラクティブ・ダッシュボードである。

「AIが試験を丸暗記していたら、その点数は実力といえるのか？」という問いから始め、データ汚染（過去問への過剰適合）が点数をどう膨らませるかを自分の手で確かめ、LiveBenchが毎月問題を刷新しLLM審査員を使わない理由を目で見て理解する。

- **すぐ見る**：https://adminmrobo.github.io/&lt;repository&gt;/ ←（リポジトリ名確定後に差し替え）
- **作者**：文・イラスト — アン・サンソン（株式会社M-Robo代表）

### 構成
| 回 | 題名 | 内容 | 難易度 |
|---|---|---|---|
| LB-01 | 実力か、過去問の暗記か | データ汚染 · ベンチマーク更新 · 客観採点 | ★★★ |

### 重要な数字（論文に基づく、ダッシュボード表示値）
| 数字 | 意味 |
|---|---|
| 64.7% | 最良モデル（o1-preview）のLiveBench得点 |
| 44.8% | 過去問に過剰適合したモデルの得点 |
| −19.9pp | 両者の差——暗記バブルの大きさ |
| 1/6 | 毎月更新される問題の割合 |
| 0回 | LLM審査員の使用回数（正解による自動採点） |

### ページの中身
- インタラクティブ実習4種：汚染度シミュレータ · 6分野レーダー · LLM審査員の誤り率 · 対決シミュレーション
- 確認クイズ2問、学習進度の記録
- ピクセルアート11枚を内蔵（base64）——外部ファイルなしで動く

### ファイル
```
LiveBench_해설_대시보드.html   本文（画像・スクリプト全部内蔵）
README.md · INDEX.md
LiveBench_해설_대시보드.{en,zh,ja,uz,ru,vi}.html   6개 언어판
images/                        元PNG 11枚（本文に内蔵済み）
image_prompts_lb.md            画像生成プロンプト全文
```

### データと画像（説明用の模型であるもの）
- 11枚のイラストはすべて生成AIによる説明用ピクセルアートで、画像内に文字はない。
- シミュレータの基準値は論文の発表値（64.7% / 44.8%）で、ブラウザのアニメーションは実行ごとに多少変わることがある。
- 実在の人物データは使っていない。

### 言語
| 言語 | ファイル | 状態 |
|---|---|---|
| 한국어（原文） | LiveBench_해설_대시보드.html | 完成済み |
| 日本語 | LiveBench_해설_대시보드.ja.html | 完成済み |
| English / 中文 / Oʻzbekcha / Русский / Tiếng Việt | *.en.html / *.zh.html / *.uz.html / *.ru.html / *.vi.html | 完成済み |

### 用語
- **データ汚染（contamination）**——評価問題が学習データに混ざり込むこと。「過去問への過剰適合」と同じ意味で統一。
- **LLM審査員（LLM-as-judge）**——別のAIに採点させる方式。「偏った採点官」の比喩で統一。

### ライセンス
- コード：Apache License 2.0 · 本文・画像：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.ja)（ページメタではCC BY 4.0とも表記——統一推奨）
- 出典表記例：「LiveBench解説ダッシュボード」LB-01、アン・サンソン、CC BY-SA 4.0

---

<a id="uz"></a>
## Oʻzbekcha

ICLR 2025 da taqdim etilgan «LiveBench: A Challenging, Contamination-Limited LLM Benchmark» (Colin White, Samuel Dooley, Manley Roberts, Arka Pal va boshqalar) maqolasini laboratoriya jamoasi — Doktor, Yordamchi Sera, Drozofila tadqiqotchisi va AbaBot — suvbatlari orqali tushuntiruvchi interaktiv panel.

«AI imtihonni oldindan yodlab qoʻygan boʻlsa, uning bali haqiqiy qobiliyatmi?» degan savoldan boshlanadi: maʼlumot ifloslanishi (eski savollarga moslashib qolish) balni qanday sunʼiy koʻtarishini oʻzingiz sinab koʻrasiz va LiveBench nima uchun savollarni har oy yangilashi hamda LLM hakamlarni islatmasligi kerakligini koʻrib tushunasiz.

- **Koʻrish**: https://adminmrobo.github.io/&lt;repository&gt;/ ←（ombor nomi tasdiqlangach almashtiriladi）
- **Muallif**: Matn va rasmlar — Ahn Sangsun (M-Robo kompaniyasi rahbari)

### Tarkib
| Qism | Sarlavha | Mavzular | Daraja |
|---|---|---|---|
| LB-01 | Haqiqiy bilimmi, eski savolmi? | Maʼlumot ifloslanishi · baholash yangilanishi · obyektiv baholash | ★★★ |

### Asosiy raqamlar (maqolaga asosan, panelda koʻrinadigan qiymatlar)
| Raqam | Maʼnosi |
|---|---|
| 64.7% | Eng kuchli model (o1-preview)ning LiveBench bali |
| 44.8% | Eski savollarga moslashib qolgan model bali |
| −19.9pp | Farq — yod olish pufakchasi kattaligi |
| 1/6 | Har oy yangilanadigan savollar ulushi |
| 0 | LLM hakam ishlatilganlik soni (toʻgʻri javob boʻyicha avtomatik baholash) |

### Sahifa ichidagi narsalar
- 4 ta interaktiv mashq: ifloslanish simulyatori · 6 soha radarini · LLM hakam xatolarini · duell simulyatsiyasi
- 2 ta nazorat testi, oʻqish jarayonini kuzatish
- 11 ta piksel-illyustratsiya ichda (base64) — tashqi faylsiz ishlaydi

### Fayllar
```
LiveBench_해설_대시보드.html   asosiy sahifa (barcha rasm va skript ichda)
README.md · INDEX.md
LiveBench_해설_대시보드.{en,zh,ja,uz,ru,vi}.html   6개 언어판
images/                        11 ta asl PNG (sahifaga oʻrnatilgan)
image_prompts_lb.md            rasm yaratish promtlari toʻliq matni
```

### Maʼlumot va rasmlar (tushuntirish uchun maket boʻlgan narsalar)
- 11 ta illyustratsiya hamda tushuntirish uchun AI yaratgan piksel-arta; rasmlar ichida yozuv yoʻq.
- Simulyator asosiy raqamlari maqoladagi qiymatlar (64.7% / 44.8%); brauzer animatsiyasi har ishga tushirishda biroz oʻzgarishi mumkin.
- Haqiqiy odam maʼlumotlari ishlatilmagan.

### Tillar
| Til | Fayl | Holat |
|---|---|---|
| 한국어 (asl nusxa) | LiveBench_해설_대시보드.html | Tayyor |
| Oʻzbekcha | LiveBench_해설_대시보드.uz.html | Tayyor |
| English / 中文 / 日本語 / Русский / Tiếng Việt | *.en.html / *.zh.html / *.ja.html / *.ru.html / *.vi.html | Tayyor |

### Atamalar
- **Maʼlumot ifloslanishi (contamination)** — baholash savollari oʻquv maʼlumotlariga oldindan aralashib qolishi. "Eski savollarga moslashish" maʼnosida bir xil ishlatiladi.
- **LLM hakam (LLM-as-judge)** — boshqa AIga baholashni topshirish usuli. "Kasbiy qarashli baholovchi" istirohi bilan yuritiladi.

### Litsenziya
- Kod: Apache License 2.0 · Matn va rasmlar: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en) (sahifa metasida CC BY 4.0 ham yozilgan — bittasiga keltirish tavsiya etiladi)
- Koʻrsatma: "LiveBench tushuntirish paneli" LB-01, Ahn Sangsun, CC BY-SA 4.0

---

<a id="ru"></a>
## Русский

Интерактивная пояснительная панель к статье «LiveBench: A Challenging, Contamination-Limited LLM Benchmark» (Colin White, Samuel Dooley, Manley Roberts, Arka Pal и др.), представленной на ICLR 2025: её ведут четверо сотрудников лаборатории — Доктор, Ассистент Сера, Исследователь-дрозофила и Робот АбаБот.

Всё начинается с вопроса: «Если ИИ заранее вызубрил экзамен, означает ли его балл настоящий уровень?» Вы сами ставите опыты и видите, как загрязнение данных (переобучение на старых заданиях) завышает баллы, и наглядно понимаете, почему LiveBench обновляет задания каждый месяц и обходится без LLM-судей.

- **Открыть**: https://adminmrobo.github.io/&lt;repository&gt;/ ← замените &lt;repository&gt; после выбора имени репозитория
- **Автор**: текст и иллюстрации — Ан Сансон (генеральный директор M-Robo Co., Ltd.)

### Состав
| Выпуск | Название | Темы | Уровень |
|---|---|---|---|
| LB-01 | Настоящий уровень или зубрёжка? | Загрязнение данных · обновление бенчмарка · объективная оценка | ★★★ |

### Ключевые числа (по статье, значения на панели)
| Число | Смысл |
|---|---|
| 64.7% | Результат лучшей модели (o1-preview) на LiveBench |
| 44.8% | Результат модели, переобученной на старых заданиях |
| −19.9pp | Разрыв — размер «пузыря» зубрёжки |
| 1/6 | Доля заданий, обновляемых ежемесячно |
| 0 | Число обращений к LLM-судье (автоматическая проверка по правильным ответам) |

### Что внутри страницы
- 4 интерактивных опыта: симулятор загрязнения · радар 6 областей · ошибки LLM-судьи · симуляция дуэли
- 2 контрольных вопроса, отслеживание прогресса
- 11 встроенных пиксель-иллюстраций (base64) — работает без внешних файлов

### Файлы
```
LiveBench_해설_대시보드.html   сама страница (все изображения и скрипты встроены)
README.md · INDEX.md
LiveBench_해설_대시보드.{en,zh,ja,uz,ru,vi}.html   6개 언어판
images/                        11 исходных PNG (уже встроены в страницу)
image_prompts_lb.md            полные тексты промптов для изображений
```

### Данные и изображения (что здесь — иллюстративный макет)
- Все 11 иллюстраций — пояснительная пиксель-графика, созданная ИИ; внутри картинок букв нет.
- Базовые числа симуляторов соответствуют значениям статьи (64.7% / 44.8%); анимация в браузере может немного отличаться от запуска к запуску.
- Реальные данные людей не используются.

### Языки
| Язык | Файл | Статус |
|---|---|---|
| 한국어 (оригинал) | LiveBench_해설_대시보드.html | Готово |
| Русский | LiveBench_해설_대시보드.ru.html | Готово |
| English / 中文 / 日本語 / Oʻzbekcha / Tiếng Việt | *.en.html / *.zh.html / *.ja.html / *.uz.html / *.vi.html | Готово |

### Терминология
- **Загрязнение данных (contamination)** — оценочные задания заранее попали в обучающие данные. Употребляется как синоним «переобучения на старых заданиях».
- **LLM-судья (LLM-as-judge)** — способ, при котором проверяет другой ИИ; последовательно использована метафора «пристрастный проверяющий».

### Лицензия
- Код: Apache License 2.0 · Текст и изображения: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.ru) (в метаданных страницы указан и CC BY 4.0 — стоит унифицировать)
- Пример указания: «LiveBench. Пояснительная панель» LB-01, Ан Сансон, CC BY-SA 4.0

---

<a id="vi"></a>
## Tiếng Việt

Bảng điều khiển tương tác giải thích bài báo ICLR 2025 «LiveBench: A Challenging, Contamination-Limited LLM Benchmark» (Colin White, Samuel Dooley, Manley Roberts, Arka Pal và cộng sự) thông qua bốn thành viên phòng thí nghiệm: Tiến sĩ, Trợ lý Sera, Nhà nghiên cứu Ruồi giấm và Robot AbaBot.

Trang bắt đầu từ câu hỏi "Nếu AI đã học thuộc đề thi từ trước, thì điểm đó có phải năng lực thật không?"; bạn sẽ tự tay làm thí nghiệm để xem ô nhiễm dữ liệu (quá khớp với đề cũ) làm điểm số phình to thế nào, và hiểu trực quan vì sao LiveBench thay đề mỗi tháng và không dùng "giám khảo LLM".

- **Xem ngay**: https://adminmrobo.github.io/&lt;repository&gt;/ ← (thay &lt;repository&gt; sau khi chốt tên kho)
- **Tác giả**: Viết · vẽ — Ahn Sangsun (Giám đốc điều hành, M-Robo Co., Ltd.)

### Cấu trúc
| Phần | Tiêu đề | Nội dung | Độ khó |
|---|---|---|---|
| LB-01 | Năng lực thật hay học vẹt đề cũ? | Ô nhiễm dữ liệu · cập nhật bộ đề · chấm điểm khách quan | ★★★ |

### Số liệu chính (theo bài báo, là giá trị hiển thị trên bảng)
| Số | Ý nghĩa |
|---|---|
| 64.7% | Điểm LiveBench của mô hình mạnh nhất (o1-preview) |
| 44.8% | Điểm của mô hình quá khớp với đề cũ |
| −19.9pp | Khoảng cách — độ lớn của "bong bóng học vẹt" |
| 1/6 | Tỉ lệ đề được thay mới mỗi tháng |
| 0 lần | Số lần dùng giám khảo LLM (chấm tự động theo đáp án khách quan) |

### Bên trong trang
- 4 bài thực hành tương tác: mô phỏng ô nhiễm · radar 6 khu vực · tỉ lệ lỗi giám khảo LLM · mô phỏng đấu xếp hạng
- 2 câu hỏi kiểm tra, theo dõi tiến độ học
- 11 tranh pixel nhúng sẵn (base64) — chạy không cần tệp ngoài

### Tệp
```
LiveBench_해설_대시보드.html   thân trang (ảnh và mã nhúng đầy đủ)
README.md · INDEX.md
LiveBench_해설_대시보드.{en,zh,ja,uz,ru,vi}.html   6개 언어판
images/                        11 PNG gốc (đã nhúng trong trang)
image_prompts_lb.md            toàn văn prompt tạo ảnh
```

### Dữ liệu và hình ảnh (những gì là mô hình minh họa)
- Cả 11 tranh minh họa đều là ảnh pixel do AI tạo để minh họa; trong ảnh không có chữ.
- Số liệu cơ sở của mô phỏng lấy theo giá trị trong bài báo (64.7% / 44.8%); hiệu ứng hoạt hình trên trình duyệt có thể hơi khác mỗi lần chạy.
- Không dùng dữ liệu người thật.

### Ngôn ngữ
| Ngôn ngữ | Tệp | Trạng thái |
|---|---|---|
| 한국어 (bản gốc) | LiveBench_해설_대시보드.html | Đã xong |
| Tiếng Việt | LiveBench_해설_대시보드.vi.html | Đã xong |
| English / 中文 / 日本語 / Oʻzbekcha / Русский | *.en.html / *.zh.html / *.ja.html / *.uz.html / *.ru.html | Đã xong |

### Thuật ngữ
- **Ô nhiễm dữ liệu (contamination)** — đề đánh giá lọt vào dữ liệu huấn luyện từ trước. Dùng thống nhất cùng cụm "quá khớp với đề cũ".
- **Giám khảo LLM (LLM-as-judge)** — cách để một AI khác chấm điểm; thống nhất dùng phép so sánh "người chấm điểm thiên vị".

### Giấy phép
- Mã nguồn: Apache License 2.0 · Văn bản & hình ảnh: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.vi) (meta của trang cũng ghi CC BY 4.0 — nên thống nhất một loại)
- Cách ghi nguồn: "Bảng giải thích LiveBench" LB-01, Ahn Sangsun, CC BY-SA 4.0
