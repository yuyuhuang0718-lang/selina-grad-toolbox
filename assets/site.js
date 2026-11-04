import { SAMPLE_TSV, cleanRows, buildOutline } from './tools.mjs';

const metadata = JSON.parse(document.getElementById('site-data').textContent);
const knownSlugs = new Set(metadata.slugs);
const STORAGE_KEY = 'selina-study-lab:v1:completed';
let completed = new Set();
let storageAvailable = true;
try {
  const probe = `${STORAGE_KEY}:probe`;
  localStorage.setItem(probe, '1');
  localStorage.removeItem(probe);
  const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  if (Array.isArray(stored)) completed = new Set(stored.filter(slug => knownSlugs.has(slug)));
} catch {
  storageAvailable = false;
  document.getElementById('storage-notice').hidden = false;
}
function saveProgress() {
  if (storageAvailable) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify([...completed])); }
    catch {
      storageAvailable = false;
      document.getElementById('storage-notice').hidden = false;
    }
  }
}
function updateProgress() {
  const counter = document.getElementById('progress-count');
  if (counter) {
    counter.textContent = `${completed.size} / ${metadata.slugs.length}`;
    document.getElementById('progress-fill').style.width = `${completed.size / metadata.slugs.length * 100}%`;
    document.querySelector('[role="progressbar"]').setAttribute('aria-valuenow', completed.size);
    document.getElementById('progress-title').textContent = completed.size ? (completed.size === metadata.slugs.length ? '每一個小練習，都累積成了自己的方法。' : '你已經替學習，留下一個小記號。') : '從一個小練習開始。';
    document.getElementById('progress-description').textContent = completed.size ? `已完成 ${completed.size} 堂課，照自己的步調繼續就好。` : '完成自我檢核，替今天的學習留下一個記號。';
    const next = metadata.slugs.find(slug => !completed.has(slug)) || metadata.slugs[0];
    const link = document.getElementById('continue-link');
    link.href = `lessons/${next}/index.html`;
    link.textContent = completed.size === metadata.slugs.length ? '再複習一次 →' : completed.size ? '繼續學習 →' : '開始學習 →';
  }
  document.querySelectorAll('[data-stamp]').forEach(stamp => { stamp.hidden = !completed.has(stamp.dataset.stamp); });
}
updateProgress();

const search = document.getElementById('course-search');
if (search) {
  let category = 'all';
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.lesson-card')];
  function filterCourses() {
    const query = search.value.trim().toLocaleLowerCase();
    const terms = query.split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const show = (category === 'all' || category === card.dataset.category) && terms.every(term => card.dataset.search.includes(term));
      card.hidden = !show;
      if (show) count++;
    });
    filters.forEach(button => {
      const active = button.dataset.filter === category;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    document.getElementById('result-count').textContent = `共 ${count} 個學習單元`;
    document.getElementById('empty-state').hidden = count > 0;
    document.getElementById('clear-search').hidden = query === '' && category === 'all';
  }
  function resetFilters() { category = 'all'; search.value = ''; filterCourses(); search.focus(); }
  filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filterCourses(); }));
  search.addEventListener('input', filterCourses);
  document.getElementById('clear-search').addEventListener('click', resetFilters);
  document.getElementById('reset-filters').addEventListener('click', resetFilters);
}

document.querySelectorAll('.quiz-form').forEach(form => {
  const feedback = form.querySelector('.quiz-feedback');
  form.addEventListener('submit', event => {
    event.preventDefault();
    const selected = form.querySelector('input:checked');
    if (!selected) { feedback.textContent = '先選一個答案，再看看理由。'; return; }
    const correct = Number(selected.value) === Number(form.dataset.answer);
    feedback.textContent = `${correct ? '答對了！' : '再想想看。'} ${form.dataset.explanation}`;
    feedback.classList.toggle('incorrect', !correct);
  });
  form.addEventListener('change', () => { feedback.textContent = ''; feedback.classList.remove('incorrect'); });
});

const completionButton = document.getElementById('complete-lesson');
if (completionButton) {
  const checks = [...document.querySelectorAll('[data-self-check]')];
  const status = document.getElementById('completion-status');
  if (completed.has(metadata.current)) checks.forEach(check => { check.checked = true; });
  function refreshCompletion() {
    const done = completed.has(metadata.current);
    const allChecked = checks.every(check => check.checked);
    completionButton.disabled = !done && !allChecked;
    completionButton.textContent = done ? '已完成這堂課 ✓ · 取消標記' : '標記這堂課已完成 ✓';
    status.textContent = done ? '這個小進步，已經記下來了。回首頁看看學習進度吧。' : allChecked ? '準備好了，就按下按鈕，替今天的學習留個記號。' : '完成上面的自我檢核後，就可以標記完成。';
  }
  checks.forEach(check => check.addEventListener('change', () => {
    if (completed.has(metadata.current) && !checks.every(c => c.checked)) { completed.delete(metadata.current); saveProgress(); }
    refreshCompletion();
  }));
  completionButton.addEventListener('click', () => {
    if (completed.has(metadata.current)) completed.delete(metadata.current);
    else if (checks.every(check => check.checked)) completed.add(metadata.current);
    saveProgress(); updateProgress(); refreshCompletion();
  });
  refreshCompletion();
}

document.getElementById('reset-progress')?.addEventListener('click', () => {
  completed.clear(); saveProgress(); updateProgress();
  document.getElementById('reset-status').textContent = '進度已重設，隨時都能從一個小練習重新開始。';
});

const outlineControls = [...document.querySelectorAll('[data-outline-text]')];
if (outlineControls.length) {
  const initial = outlineControls.map(control => control.value);
  function refreshOutline() {
    const output = document.getElementById('outline-preview');
    output.replaceChildren();
    const items = buildOutline(outlineControls.map(control => ({ text: control.dataset.outlineText, level: Number(control.value) })));
    if (!items.length) {
      const empty = document.createElement('li'); empty.className = 'no-heading'; empty.textContent = '還沒有標題，先替左側文字套用樣式。'; output.append(empty);
    }
    items.forEach(item => {
      const line = document.createElement('li');
      if (item.level === 2) line.className = 'level-two';
      line.textContent = item.text + (item.orphan ? '（前面尚無標題 1）' : '');
      output.append(line);
    });
  }
  outlineControls.forEach(control => control.addEventListener('change', refreshOutline));
  document.getElementById('reset-outline').addEventListener('click', () => { outlineControls.forEach((control, index) => { control.value = initial[index]; }); refreshOutline(); });
  refreshOutline();
}

const cleanInput = document.getElementById('clean-input');
if (cleanInput) {
  const status = document.getElementById('clean-status');
  const output = document.getElementById('clean-output');
  const body = document.getElementById('clean-body');
  document.getElementById('run-cleaner').addEventListener('click', () => {
    body.replaceChildren(); output.hidden = true; status.classList.remove('error');
    try {
      const result = cleanRows(cleanInput.value);
      for (const row of result.rows) {
        const tr = document.createElement('tr');
        for (const value of row) {
          const td = document.createElement('td');
          td.textContent = value === '' ? '缺漏' : value;
          if (value === '') td.className = 'missing';
          tr.append(td);
        }
        body.append(tr);
      }
      status.textContent = `原有 ${result.inputCount} 筆 → 保留 ${result.rows.length} 筆；移除 ${result.duplicateCount} 筆完全重複，保留 ${result.missing} 個缺漏欄位。` + (result.conflicts.length ? ` 提醒：${result.conflicts.join('、')} 的 ID 相同但內容不同，已保留各筆，請另外確認。` : '');
      output.hidden = false;
    } catch (error) { status.textContent = error.message; status.classList.add('error'); }
  });
  cleanInput.addEventListener('input', () => { output.hidden = true; status.textContent = '資料已修改，按「整理看看」重新計算。'; status.classList.remove('error'); });
  document.getElementById('reset-cleaner').addEventListener('click', () => { cleanInput.value = SAMPLE_TSV; output.hidden = true; body.replaceChildren(); status.textContent = '範例已還原，可以先猜猜整理後會剩幾筆。'; status.classList.remove('error'); });
}

const storyInputs = [...document.querySelectorAll('[data-story]')];
if (storyInputs.length) {
  const original = storyInputs.map(input => input.value);
  function refreshStory() {
    storyInputs.forEach(input => {
      const text = input.value.trim();
      document.getElementById(`preview-${input.dataset.story}`).textContent = text || (input.dataset.story === 'message' ? '先寫下一句，你最想說的話。' : '這一段，留給你的想法。');
    });
  }
  storyInputs.forEach(input => input.addEventListener('input', refreshStory));
  document.getElementById('reset-story').addEventListener('click', () => { storyInputs.forEach((input, index) => { input.value = original[index]; }); refreshStory(); });
  refreshStory();
}
