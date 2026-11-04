export const SAMPLE_TSV = 'ID\t名稱\t分數\nR001\t 樣本A \t85\nR002\t樣本B\t90\nR001\t樣本A\t85\nR003\t 樣本C \t';

// Match Excel TRIM's ASCII-space behavior; preserve all other Unicode spaces.
export function trimAscii(value) {
  return String(value).replace(/^ +| +$/g, '').replace(/ {2,}/g, ' ');
}

export function cleanRows(text) {
  if (typeof text !== 'string' || text.trim() === '') throw new Error('先貼上三欄資料，再試一次。');
  if (text.length > 20000) throw new Error('資料太長了，請使用最多 100 筆的小範例。');
  const lines = text.replace(/\r\n?/g, '\n').split('\n');
  while (lines.length && lines.at(-1) === '') lines.pop();
  const header = lines.shift().split('\t').map(trimAscii);
  if (header.length !== 3 || header.join('\t') !== 'ID\t名稱\t分數') throw new Error('第一列需為 ID、名稱、分數，並以 Tab 分隔三欄。可按「還原範例」參考。');
  if (!lines.length) throw new Error('表頭下至少需要一筆資料。');
  if (lines.length > 100) throw new Error('這張練習桌最多處理 100 筆資料。');
  const rows = [], seen = new Set(), ids = new Map(), conflicts = new Set();
  let duplicateCount = 0, missing = 0;
  for (const [index, line] of lines.entries()) {
    const row = line.split('\t').map(trimAscii);
    if (row.length !== 3) throw new Error(`第 ${index + 2} 列不是三欄，請確認使用 Tab 分隔；空白列也請移除。`);
    if (row[2] !== '' && (!/^\d+(?:\.\d+)?$/.test(row[2]) || Number(row[2]) > 100)) throw new Error(`第 ${index + 2} 列的分數請留空或填 0–100 的數字。`);
    const key = JSON.stringify(row);
    if (seen.has(key)) { duplicateCount++; continue; }
    seen.add(key);
    missing += row.filter(value => value === '').length;
    if (row[0] !== '') {
      if (ids.has(row[0]) && ids.get(row[0]) !== key) conflicts.add(row[0]);
      ids.set(row[0], key);
    }
    rows.push(row);
  }
  return { rows, inputCount: lines.length, duplicateCount, missing, conflicts: [...conflicts] };
}

export function buildOutline(items) {
  let parentSeen = false;
  return items.filter(item => item.level === 1 || item.level === 2).map(item => {
    const orphan = item.level === 2 && !parentSeen;
    if (item.level === 1) parentSeen = true;
    return { text: String(item.text), level: item.level, orphan };
  });
}
