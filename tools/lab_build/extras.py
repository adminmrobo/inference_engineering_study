# -*- coding: utf-8 -*-
"""4주차부터 쓰는 보조 조각: 짧은 코스 안내, 강의자용 정답·해설 부록, 지식 색인 빈 정의 채우기."""
from lab import say


def short_course(title, stops, minutes='30분'):
    """stops: [(id, 이름, 왜 보는지)]"""
    lis = ''.join('<li><a href="#%s"><b>%s</b></a> — %s</li>' % s for s in stops)
    return ('<div class="panel" id="course"><h3>%s 코스 — %s</h3><p class="muted" style="margin:0 0 6px">시간이 없을 때(수업 · 스터디 발표) 이 순서로만 보세요. 나머지 칸은 복습용입니다.</p>'
            '<ol style="margin:0">%s</ol></div>') % (minutes, title, lis)


def teach_appendix(quiz, titles, extra=''):
    """quiz: {칸id: [문항]}, titles: {칸id: 칸 이름}. 정답·해설을 접어 둔 강의자용 부록."""
    rows = ''
    n = 0
    for sid, items in quiz.items():
        for q in items:
            n += 1
            rows += '<tr><td>%s</td><td>%s</td><td><b>%s</b></td><td>%s</td></tr>' % (titles.get(sid, sid), q['q'], q['o'][q['a']], q['why'])
    return ('<section class="level" id="teach"><div class="wrap"><h2>강의자용 부록 — 퀴즈 정답과 해설</h2>'
            + say('sia', 'guide', '수업이나 스터디에서 쓰실 분을 위해 퀴즈 %d문항의 정답과 해설을 모았어요. 학습자에게 보여 주기 전에는 접어 두세요.' % n) +
            '<details class="math"><summary>정답 · 해설 펼치기 (%d문항)</summary><div class="tw"><table class="tb"><tr><th>칸</th><th>문항</th><th>정답</th><th>해설</th></tr>%s</table></div></details>%s</div></section>') % (n, rows, extra)


def fill_defs(kg, defs):
    """정의가 비어 있는 노드에 정의를 채운다. 빠진 것이 있으면 목록을 돌려준다."""
    missing = []
    for nd in kg['nodes']:
        if 'definition' not in nd:
            d = defs.get(nd['id'])
            if d:
                nd['definition'] = {'ko': d}
            else:
                missing.append(nd['id'])
    return missing
