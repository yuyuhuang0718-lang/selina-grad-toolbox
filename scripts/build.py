#!/usr/bin/env python3
"""Validate lesson data and build a dependency-free, relative-path static site."""
from __future__ import annotations
import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
CATEGORIES = {'word': ('Word', '文件整理'), 'excel': ('Excel', '資料整理'), 'slides': ('簡報', '表達練習'), 'general': ('工具', '學習方法')}
TODAY = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()

def h(value):
    return html.escape(str(value), quote=True)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def require(ok, message):
    if not ok:
        raise ValueError(message)

def valid_date(value):
    try:
        return isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value) and dt.date.fromisoformat(value) <= TODAY
    except ValueError:
        return False

def validate_lesson(d, filename):
    required = {'slug', 'order', 'title', 'subtitle', 'category', 'minutes', 'updated', 'goals', 'intro', 'concepts', 'steps', 'demo', 'mistakes', 'practice', 'quiz', 'checklist', 'sources'}
    require(isinstance(d, dict) and set(d) == required, f'{filename}: 必要欄位缺少或多出未知欄位')
    require(nonempty(d['slug']) and re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', d['slug']), f'{filename}: slug 格式錯誤')
    require(d['slug'] == filename.stem, f'{filename}: slug 與檔名不同')
    for key in ('title', 'subtitle', 'intro'):
        require(nonempty(d[key]), f'{filename}: {key} 不可空白')
    require(type(d['order']) is int and d['order'] > 0, f'{filename}: order 必須為正整數')
    require(type(d['minutes']) is int and 1 <= d['minutes'] <= 60, f'{filename}: minutes 必須為 1–60')
    require(d['category'] in CATEGORIES, f'{filename}: category 不支援')
    require(valid_date(d['updated']), f'{filename}: updated 日期錯誤或晚於今天')
    for key, minimum in [('goals', 2), ('checklist', 3)]:
        require(isinstance(d[key], list) and len(d[key]) >= minimum and all(nonempty(x) for x in d[key]), f'{filename}: {key} 內容不足')
    for key, minimum, fields in [('concepts', 2, ('term', 'explanation')), ('steps', 3, ('title', 'description')), ('mistakes', 2, ('wrong', 'better'))]:
        require(isinstance(d[key], list) and len(d[key]) >= minimum, f'{filename}: {key} 內容不足')
        for item in d[key]:
            require(isinstance(item, dict) and set(item) == set(fields) and all(nonempty(item.get(f)) for f in fields), f'{filename}: {key} 子欄位錯誤')
    require(isinstance(d['demo'], dict) and set(d['demo']) == {'type', 'title', 'description'}, f'{filename}: demo 欄位錯誤')
    require(d['demo']['type'] in {'outline', 'cleaner', 'storyboard', 'none'} and all(nonempty(d['demo'][f]) for f in ('title', 'description')), f'{filename}: demo 格式錯誤')
    require(isinstance(d['practice'], dict) and set(d['practice']) == {'task', 'solution'} and all(nonempty(d['practice'][f]) for f in ('task', 'solution')), f'{filename}: practice 格式錯誤')
    require(isinstance(d['quiz'], list) and len(d['quiz']) >= 2, f'{filename}: quiz 至少兩題')
    for q in d['quiz']:
        require(isinstance(q, dict) and set(q) == {'question', 'choices', 'answer', 'explanation'}, f'{filename}: quiz 欄位錯誤')
        require(nonempty(q['question']) and nonempty(q['explanation']), f'{filename}: quiz 題目／解釋不可空白')
        require(isinstance(q['choices'], list) and 2 <= len(q['choices']) <= 4 and all(nonempty(x) for x in q['choices']) and len(set(q['choices'])) == len(q['choices']), f'{filename}: quiz 選項錯誤')
        require(type(q['answer']) is int and 0 <= q['answer'] < len(q['choices']), f'{filename}: quiz 答案索引錯誤')
    require(isinstance(d['sources'], list) and len(d['sources']) >= 1, f'{filename}: 缺少來源')
    for s in d['sources']:
        require(isinstance(s, dict) and set(s) == {'title', 'url', 'accessed'}, f'{filename}: 來源欄位錯誤')
        require(nonempty(s['title']) and isinstance(s['url'], str), f'{filename}: 來源標題或網址錯誤')
        u = urlsplit(s['url'])
        require(u.scheme == 'https' and bool(u.netloc) and valid_date(s['accessed']), f'{filename}: 來源必須為 HTTPS 及有效查閱日期')

def load_lessons():
    lessons = []
    for file in sorted((ROOT / 'content/lessons').glob('*.json')):
        d = json.loads(file.read_text(encoding='utf-8'))
        validate_lesson(d, file)
        lessons.append(d)
    require(bool(lessons), '至少需有一堂課')
    for key in ('slug', 'order'):
        require(len({x[key] for x in lessons}) == len(lessons), f'{key} 不可重複')
    return sorted(lessons, key=lambda x: x['order'])

def lesson_url(d, prefix=''):
    return f'{prefix}lessons/{d["slug"]}/index.html'

def page(title, description, content, lessons, prefix='', body_class='', slug=None):
    template = (ROOT / 'templates/page.html').read_text(encoding='utf-8')
    site_data = json.dumps({'slugs': [x['slug'] for x in lessons], 'current': slug}, ensure_ascii=False).replace('<', '\\u003c')
    values = {'title': h(title), 'description': h(description), 'content': content, 'prefix': prefix, 'body_class': h(body_class), 'site_data': site_data}
    return re.sub(r'\{\{([a-z_]+)\}\}', lambda m: values[m.group(1)], template)

def miniature(category):
    if category == 'word':
        return '<div class="mini-document"><span>目錄</span><i></i><i></i><i></i><b>1.1</b><em>有結構，就不慌。</em></div>'
    if category == 'excel':
        return '<div class="mini-table"><span>A</span><span>B</span><span>C</span><i></i><i></i><i>✓</i><i></i><i></i><i>✓</i><i></i><i></i><i>✓</i></div><span class="mini-label">整齊一點，清楚一點。</span>'
    if category == 'slides':
        return '<div class="mini-slide"><b>一個重點，就夠有力。</b><div><i></i><i></i><i></i></div><span>情境 → 發現 → 下一步</span></div>'
    return '<div class="mini-document"><span>學習筆記</span><i></i><i></i><i></i><em>今天又多學會一點。</em></div>'

def home(lessons, site):
    cards = []
    for n, d in enumerate(lessons, 1):
        label, sublabel = CATEGORIES[d['category']]
        search = ' '.join([d['title'], d['subtitle'], label, sublabel, d['intro'], *d['goals'], *[c['term'] + ' ' + c['explanation'] for c in d['concepts']], *[s['title'] + ' ' + s['description'] for s in d['steps']]])
        cards.append(f'''<article class="lesson-card {h(d['category'])}" data-category="{h(d['category'])}" data-search="{h(search.lower())}" data-slug="{h(d['slug'])}">
        <a class="card-visual" href="{lesson_url(d)}" tabindex="-1" aria-hidden="true"><span class="card-number">LESSON {n:02}</span>{miniature(d['category'])}<span class="card-stamp" data-stamp="{h(d['slug'])}" hidden>已完成 ✓</span></a>
        <div class="card-content"><div class="card-meta"><span class="category-tag">{h(label)} · {h(sublabel)}</span><span>約 {d['minutes']} 分鐘</span></div><h3><a href="{lesson_url(d)}">{h(d['title'])}</a></h3><p>{h(d['subtitle'])}</p><a class="text-link" href="{lesson_url(d)}">開始這堂小課 <span aria-hidden="true">↗</span></a></div></article>''')
    filters = '<button class="filter active" data-filter="all" aria-pressed="true">全部單元</button>'
    for key, (label, _) in CATEGORIES.items():
        count = sum(d['category'] == key for d in lessons)
        if count:
            filters += f'<button class="filter" data-filter="{key}" aria-pressed="false">{h(label)} <span>{count:02}</span></button>'
    return f'''<section class="hero container">
      <div class="hero-copy"><p class="eyebrow"><span class="tiny-star">✦</span> 給正在學習的你</p><h1>研究生活的小卡關，<br><em>我們一堂一堂解開。</em></h1><p class="hero-description">從一份整齊的文件、一張乾淨的表格，<br class="desktop-break">到一次清楚的表達。把常用工具，變成自己的小幫手。</p><div class="hero-actions"><a class="button" href="#lessons">挑一堂課，開始吧 <span aria-hidden="true">↗</span></a><span class="hand-note">不用一次學會所有事。</span></div><div class="hero-facts"><span><b>{len(lessons):02}</b> 個實用小單元</span><span>每堂約 <b>{min(d['minutes'] for d in lessons)}–{max(d['minutes'] for d in lessons)}</b> 分鐘</span><span>讀一讀，也動手做</span></div></div>
      <div class="desk" role="img" aria-label="整理文件、資料與簡報的小書桌插圖"><div class="desk-grid"></div><span class="desk-label">A LITTLE BETTER, EVERY DAY.</span><div class="paper-sheet"><div class="paper-top"><span>我的研究生活</span><span>↗</span></div><h2>整理思緒，<br>也整理日常。</h2><div class="paper-lines"><i></i><i></i></div><div class="paper-check"><span>✓</span> 學會一個小技巧</div><div class="paper-check"><span>✓</span> 留下自己的練習</div><div class="paper-check muted"><span>○</span> 明天，再前進一點</div><span class="paper-bottom">small steps / real progress</span></div><div class="desk-tab tab-word">W <span>文件</span></div><div class="desk-tab tab-excel">X <span>資料</span></div><div class="desk-tab tab-slides">P <span>表達</span></div><div class="desk-sticky">慢慢學，<br>也很可以。<span>✧</span></div><span class="desk-spark spark-one">✳</span><span class="desk-spark spark-two">✧</span></div>
    </section>
    <section class="container progress-strip" aria-label="我的學習進度"><div class="progress-icon" aria-hidden="true">↗</div><div class="progress-copy"><b id="progress-title">從一個小練習開始。</b><span id="progress-description">完成自我檢核，替今天的學習留下一個記號。</span></div><div class="progress-counter"><span id="progress-count">0 / {len(lessons)}</span><div class="meter" role="progressbar" aria-label="已完成課程" aria-valuemin="0" aria-valuemax="{len(lessons)}" aria-valuenow="0"><span id="progress-fill"></span></div></div><a class="text-link" id="continue-link" href="{lesson_url(lessons[0])}">開始學習 →</a></section>
    <section class="container courses-section" id="lessons"><div class="section-heading"><div><p class="eyebrow">THE LITTLE LESSONS</p><h2>今天，想學會哪一件小事？</h2></div><p>選一個眼前用得到的，<br>從小地方開始變得更順手。</p></div><div class="course-toolbar"><div class="filters" role="group" aria-label="課程分類">{filters}</div><div class="search-box"><span aria-hidden="true">⌕</span><label class="sr-only" for="course-search">搜尋課程</label><input id="course-search" type="search" placeholder="搜尋工具或關鍵字…" autocomplete="off"><button id="clear-search" class="clear-search" aria-label="清除搜尋與分類" hidden>×</button></div></div><p class="results" id="result-count" role="status">共 {len(lessons)} 個學習單元</p><div class="lesson-grid">{''.join(cards)}</div><div class="empty-state" id="empty-state" hidden><span>⌕</span><h3>還沒找到這個主題</h3><p>試試「目錄」、「資料」或「簡報」，也可以清除篩選重新看看。</p><button class="button secondary" id="reset-filters">看看全部單元</button></div></section>
    <section class="container learning-path" id="path"><div class="path-intro"><p class="eyebrow">MAKE IT YOURS</p><h2>學會，然後<br>用在自己的生活裡。</h2><p>不用背下所有功能。<br>知道怎麼開始，就能多做一點。</p></div><ol class="path-steps"><li><span>01</span><div><h3>先懂，為什麼這樣做</h3><p>用簡單的觀念，找到眼前問題的切入點。</p></div></li><li><span>02</span><div><h3>動手，把方法試一次</h3><p>跟著操作步驟與練習，把理解變成經驗。</p></div></li><li><span>03</span><div><h3>確認，自己真的會了</h3><p>做個小測驗，完成檢核，再把方法帶回作業裡。</p></div></li></ol></section>
    <section class="container about-banner"><div><span class="eyebrow">FROM SELINA</span><h2>把學過的，整理成能再用一次的方法。</h2><p>這間小教室會慢慢長大。每一堂課都沿用相同結構，讓下一次的學習更有方向。</p></div><a class="button secondary" href="about.html">認識小教室 <span aria-hidden="true">↗</span></a></section>'''

def render_demo(d):
    kind = d['demo']['type']
    if kind == 'outline':
        rows = [('第一章 緒論', 1), ('1.1 研究背景', 2), ('這裡是背景的內文。', 0), ('1.2 研究目的', 0)]
        controls = ''
        for i, (text, level) in enumerate(rows):
            options = ''.join(f'<option value="{v}" {"selected" if v == level else ""}>{name}</option>' for v, name in [(0, '一般內文'), (1, '標題 1'), (2, '標題 2')])
            controls += f'<div class="outline-row"><label for="outline-{i}">{h(text)}</label><select id="outline-{i}" data-outline-text="{h(text)}">{options}</select></div>'
        return f'<div class="demo-grid"><div><h4>文件中的文字</h4>{controls}</div><div class="outline-result"><h4>目錄預覽 <span>不含頁碼</span></h4><ol id="outline-preview" aria-live="polite"></ol><p class="small">試著把「1.2 研究目的」改成標題 2。</p></div></div><button class="button secondary small-button" id="reset-outline">還原範例</button>'
    if kind == 'cleaner':
        sample = 'ID\t名稱\t分數\nR001\t 樣本A \t85\nR002\t樣本B\t90\nR001\t樣本A\t85\nR003\t 樣本C \t'
        return f'''<label class="field-label" for="clean-input">三欄資料（Tab 分隔，第一列保留 ID、名稱、分數）</label><textarea id="clean-input" class="data-input" rows="7" spellcheck="false" aria-describedby="clean-hint">{h(sample)}</textarea><p class="small" id="clean-hint">可從 Excel 複製三欄貼上。分數可留空或填 0–100；不改寫數值、不自動補值。最多 100 筆資料。</p><div class="tool-actions"><button class="button" id="run-cleaner">整理看看 <span aria-hidden="true">↗</span></button><button class="button secondary" id="reset-cleaner">還原範例</button></div><p id="clean-status" class="tool-status" role="status"></p><div id="clean-output" hidden><div class="table-scroll"><table><caption>整理後的範例資料</caption><thead><tr><th scope="col">ID</th><th scope="col">名稱</th><th scope="col">分數</th></tr></thead><tbody id="clean-body"></tbody></table></div><p class="small">「缺漏」代表原欄位是空白；輸入內容僅在本頁處理，不會上傳。</p></div>'''
    if kind == 'storyboard':
        fields = [('message', '一句主訊息', '先統一欄位，再開始比對資料。', 60), ('context', '情境', '小組即將整合期末報告。', 120), ('finding', '發現', '不同檔案的欄位名稱與單位不一致。', 120), ('next', '下一步', '先做欄位對照表，確認單位後再分析。', 120)]
        controls = ''.join(f'<label class="field-label" for="story-{key}">{label}<textarea id="story-{key}" data-story="{key}" rows="2" maxlength="{limit}">{h(text)}</textarea></label>' for key, label, text, limit in fields)
        blocks = ''.join(f'<div><span>{label}</span><p id="preview-{key}"></p></div>' for key, label in [('context','01 情境'),('finding','02 發現'),('next','03 下一步')])
        return f'<div class="story-grid"><div>{controls}<button class="button secondary small-button" id="reset-story">還原範例</button></div><div class="story-preview"><span class="eyebrow">MY ONE-SLIDE STORY</span><h4 id="preview-message"></h4>{blocks}<small>自編教學情境 · 表達練習預覽</small></div></div>'
    return ''

def lesson_content(d, lessons):
    label, sublabel = CATEGORIES[d['category']]
    index = lessons.index(d)
    nav = [('goals','學習目標'),('concepts','核心觀念'),('steps','操作步驟'),('practice','動手練習'),('mistakes','常見誤解'),('quiz','小測驗'),('checklist','自我檢核'),('sources','參考來源')]
    aside = ''.join(f'<a href="#{key}">{name}</a>' for key, name in nav)
    goals = ''.join(f'<li><span aria-hidden="true">✓</span>{h(x)}</li>' for x in d['goals'])
    concepts = ''.join(f'<div class="concept"><h3>{h(x["term"])}</h3><p>{h(x["explanation"])}</p></div>' for x in d['concepts'])
    steps = ''.join(f'<li><span class="step-no">{i:02}</span><div><h3>{h(x["title"])}</h3><p>{h(x["description"])}</p></div></li>' for i, x in enumerate(d['steps'],1))
    demo = ''
    if d['demo']['type'] != 'none':
        demo = f'<div class="demo {h(d["category"])}"><span class="eyebrow">TRY IT YOURSELF</span><h3>{h(d["demo"]["title"])}</h3><p>{h(d["demo"]["description"])}</p>{render_demo(d)}</div>'
    mistakes = ''.join(f'<div class="mistake"><p><span>常見想法</span>{h(x["wrong"])}</p><p><span>試著這樣做</span>{h(x["better"])}</p></div>' for x in d['mistakes'])
    quizzes = ''
    for i, q in enumerate(d['quiz']):
        options = ''.join(f'<label class="quiz-choice"><input type="radio" name="q-{i}" value="{j}" required><span>{h(choice)}</span></label>' for j, choice in enumerate(q['choices']))
        quizzes += f'<form class="quiz-form" data-answer="{q["answer"]}" data-explanation="{h(q["explanation"])}"><fieldset><legend><span>Q{i+1:02}</span> {h(q["question"])}</legend>{options}</fieldset><button class="button secondary small-button" type="submit">確認答案</button><p class="quiz-feedback" role="status"></p></form>'
    checklist = ''.join(f'<label class="check-item"><input type="checkbox" data-self-check><span>{h(x)}</span></label>' for x in d['checklist'])
    sources = ''.join(f'<li><a href="{h(s["url"])}" target="_blank" rel="noopener noreferrer">{h(s["title"])} <span aria-hidden="true">↗</span></a><small>查閱：{h(s["accessed"])}</small></li>' for s in d['sources'])
    prevlink = f'<a href="../{lessons[index-1]["slug"]}/index.html"><small>← 上一堂小課</small><b>{h(lessons[index-1]["title"])}</b></a>' if index else '<a href="../../index.html#lessons"><small>← 回學習單元</small><b>挑選適合你的小課</b></a>'
    nextlink = f'<a href="../{lessons[index+1]["slug"]}/index.html"><small>下一堂小課 →</small><b>{h(lessons[index+1]["title"])}</b></a>' if index+1 < len(lessons) else '<a href="../../index.html#lessons"><small>回到小教室 →</small><b>看看自己的學習進度</b></a>'
    return f'''<div class="container"><a class="back-link" href="../../index.html#lessons">← 回到學習單元</a><header class="lesson-header {h(d['category'])}"><div class="lesson-eyebrow"><span class="category-tag">{h(label)} · {h(sublabel)}</span><span>LESSON {index+1:02} / {len(lessons):02}</span></div><h1>{h(d['title'])}</h1><p>{h(d['subtitle'])}</p><div class="lesson-details"><span>預估 {d['minutes']} 分鐘</span><span>內容查核 {h(d['updated'])}</span><span>入門 · 可動手練習</span></div></header><div class="lesson-layout"><aside class="lesson-aside"><span class="eyebrow">IN THIS LESSON</span><nav aria-label="本課章節">{aside}</nav><a class="aside-next" href="#checklist">替學習留個記號 ↘</a></aside><article class="lesson-article"><section class="lesson-section" id="goals"><p class="eyebrow">BEFORE WE START</p><h2>這堂課，你會學到</h2><ul class="goals">{goals}</ul><p>{h(d['intro'])}</p></section><section class="lesson-section" id="concepts"><p class="eyebrow">01 / UNDERSTAND</p><h2>先把觀念弄清楚</h2><div class="concepts">{concepts}</div></section><section class="lesson-section" id="steps"><p class="eyebrow">02 / FOLLOW ALONG</p><h2>一步一步，跟著做</h2><ol class="steps">{steps}</ol></section><section class="lesson-section" id="practice"><p class="eyebrow">03 / MAKE IT YOURS</p><h2>換你動手試試</h2>{demo}<div class="practice"><h3>把方法，用在自己的練習裡</h3><p>{h(d['practice']['task'])}</p><details><summary>看看參考做法</summary><p>{h(d['practice']['solution'])}</p></details></div></section><section class="lesson-section" id="mistakes"><p class="eyebrow">04 / LITTLE REMINDERS</p><h2>這幾個地方，容易卡住</h2>{mistakes}</section><section class="lesson-section" id="quiz"><p class="eyebrow">05 / CHECK YOUR UNDERSTANDING</p><h2>兩分鐘，確認自己懂了</h2><p>選一個答案，再看看理由。答錯也沒關係，可以重新試一次。</p>{quizzes}</section><section class="lesson-section completion" id="checklist"><p class="eyebrow">A LITTLE WIN FOR TODAY</p><h2>今天的你，又多學會一點。</h2><p>勾選你已經能完成的事，再替這堂課留下記號。</p>{checklist}<button class="button" id="complete-lesson" disabled>標記這堂課已完成 ✓</button><p id="completion-status" class="small" role="status">完成上面的自我檢核後，就可以標記完成。</p></section><section class="lesson-section sources" id="sources"><p class="eyebrow">KEEP EXPLORING</p><h2>想再多了解一點</h2><p>以下為官方說明。工具介面可能因版本、平台或語言略有不同。</p><ul>{sources}</ul></section></article></div><nav class="lesson-pagination" aria-label="前後課程">{prevlink}{nextlink}</nav></div>'''

def about_content(site, lessons):
    agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
    repo = f'<a class="button secondary" href="{h(site["repository"])}" target="_blank" rel="noopener noreferrer">GitHub 原始專案 ↗</a>' if site.get('repository') else ''
    return f'''<div class="container about-page"><a class="back-link" href="index.html">← 回到小教室</a><header class="about-heading"><p class="eyebrow">A NOTE FROM SELINA</p><h1>把學過的，<br><em>變成能繼續累積的方法。</em></h1><p>我是小魚 Selina。這裡整理研究生活中常用的工具技巧，讓每次的小卡關，都能成為下一次更順手的起點。</p></header><div class="about-grid"><section class="about-card"><span class="eyebrow">WHY THIS CLASSROOM</span><h2>從能用得上的事情開始</h2><p>這個小專案先從 Word、Excel 與簡報出發。每課都有觀念、步驟、練習、常見誤解、小測驗與自我檢核；先理解，再動手試。</p><p>教學情境與資料為自編範例，工具說明附官方來源。這是一份持續整理的學習資源。</p></section><section class="about-card green-card"><span class="eyebrow">BUILT TO KEEP GROWING</span><h2>讓下一堂課，有規則可循</h2><p>這也是第九週 AGENTS.md 作業：把內容格式、視覺風格、檔案位置與驗證方式寫清楚，讓 AI 能用同一套方法繼續新增教學。</p><p>課程內容與共用版型分開；新增一份內容檔後，首頁與課程導覽會一起更新。</p></section></div><section class="rules-section"><div class="section-heading"><div><p class="eyebrow">THE PROJECT PLAYBOOK</p><h2>小教室的製作規則</h2></div><a class="button secondary" href="AGENTS.md" download>下載 AGENTS.md ↓</a></div><div class="rule-steps"><div><span>01</span><h3>先寫清楚內容</h3><p>定義一個具體任務，查官方來源，完成固定章節。</p></div><div><span>02</span><h3>沿用同一套格式</h3><p>把內容放進課程 JSON，沿用共用版型與視覺。</p></div><div><span>03</span><h3>驗證，再加入網站</h3><p>檢查資料、連結與練習，讓新課程自動出現在首頁。</p></div></div><details class="agents-detail"><summary>展開閱讀完整 AGENTS.md</summary><pre>{h(agents)}</pre></details><div class="download-actions"><a class="text-link" href="lesson-template.json" download>下載新課程範本 ↘</a><a class="text-link" href="EXTENDING.md" download>閱讀擴充步驟 ↘</a>{repo}</div></section><section class="about-card progress-settings"><h2>你的學習記號</h2><p>完成狀態只儲存在目前的瀏覽器。練習工具的輸入不會上傳，也不會保存。</p><button class="button secondary" id="reset-progress">重設我的學習進度</button><p class="small" id="reset-status" role="status"></p></section><p class="small about-credit">AI 協作：使用 AI 協助規劃、程式實作與驗證；網站品牌、內容結構與教學情境依本專案設計。課堂網站作為架構參考。</p></div>'''

def main():
    lessons = load_lessons()
    site = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
    # Keep the output root inode stable for preview servers watching this folder.
    OUT.mkdir(exist_ok=True)
    for child in OUT.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    (OUT / 'lessons').mkdir(parents=True)
    shutil.copytree(ROOT / 'assets', OUT / 'assets')
    (OUT / 'index.html').write_text(page(site['title'], site['description'], home(lessons, site), lessons, body_class='home-page'), encoding='utf-8')
    (OUT / 'about.html').write_text(page('關於與規則｜' + site['title'], '認識小魚的工具小教室，以及讓 AI 持續擴充課程的 AGENTS.md。', about_content(site, lessons), lessons, body_class='about-view'), encoding='utf-8')
    for d in lessons:
        dest = OUT / 'lessons' / d['slug']
        dest.mkdir()
        (dest / 'index.html').write_text(page(d['title'] + '｜小魚的工具小教室', d['subtitle'], lesson_content(d, lessons), lessons, prefix='../../', body_class='lesson-page', slug=d['slug']), encoding='utf-8')
    for source, dest in [('AGENTS.md','AGENTS.md'), ('content/lesson-template.json','lesson-template.json'), ('docs/EXTENDING.md','EXTENDING.md')]:
        if (ROOT / source).exists():
            shutil.copyfile(ROOT / source, OUT / dest)
    (OUT / '.nojekyll').touch()
    print(f'Build OK: {len(lessons)} lessons, {len(lessons)+2} HTML pages → {OUT}')

if __name__ == '__main__':
    main()
