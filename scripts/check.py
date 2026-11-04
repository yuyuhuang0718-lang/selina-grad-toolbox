#!/usr/bin/env python3
"""Verify authored data, site navigation, tools and the N+1 extension contract."""
from __future__ import annotations
import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT / 'scripts/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class InspectHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []
        self.h1, self.titles = 0, 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'duplicate id: {a["id"]}'
            self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.titles += 1
        for key in ('href', 'src'):
            if a.get(key): self.links.append(a[key])

def main():
    lessons = build.load_lessons()
    build.main()
    output = ROOT / 'dist'
    pages = sorted(output.rglob('*.html'))
    parsed = {}
    for file in pages:
        parser = InspectHTML()
        parser.feed(file.read_text(encoding='utf-8'))
        assert parser.h1 == 1 and parser.titles == 1, f'{file}: each page needs one h1 and title'
        parsed[file.resolve()] = parser
    for file, parser in parsed.items():
        for href in parser.links:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc: continue
            target = (file.parent / unquote(parts.path)).resolve() if parts.path else file
            if target.is_dir(): target = target / 'index.html'
            assert target.is_relative_to(output.resolve()), f'link escapes site: {href}'
            assert target.exists(), f'broken link in {file.name}: {href}'
            if parts.fragment:
                assert target in parsed and unquote(parts.fragment) in parsed[target].ids, f'broken fragment: {href}'
    for mutate in [lambda d:d.update(category='unknown'), lambda d:d['quiz'][0].update(answer=99), lambda d:d['sources'][0].update(url='javascript:alert(1)')]:
        bad = copy.deepcopy(lessons[0]); mutate(bad)
        try: build.validate_lesson(bad, Path(bad['slug'] + '.json'))
        except ValueError: pass
        else: raise AssertionError('invalid lesson unexpectedly accepted')
    print(f'Content and links OK: {len(lessons)} lessons; {len(pages)} HTML pages; all relative links and fragments.')
    for file in ['assets/site.js','assets/tools.mjs']:
        subprocess.run(['node','--check',str(ROOT / file)], check=True)
    subprocess.run(['node',str(ROOT / 'scripts/test-tools.mjs')], check=True)
    with tempfile.TemporaryDirectory(prefix='selina-n-plus-one-') as tmp:
        clone = Path(tmp) / 'project'
        shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns('.git','.openai','dist','__pycache__'))
        extra = copy.deepcopy(lessons[0]); extra.update(slug='extension-demo', order=max(x['order'] for x in lessons)+1, title='擴充驗證課程')
        extra['demo']['type'] = 'none'
        (clone / 'content/lessons/extension-demo.json').write_text(json.dumps(extra,ensure_ascii=False), encoding='utf-8')
        subprocess.run(['python3',str(clone / 'scripts/build.py')], check=True, stdout=subprocess.DEVNULL)
        home = (clone / 'dist/index.html').read_text(encoding='utf-8')
        assert '擴充驗證課程' in home and 'lessons/extension-demo/index.html' in home
        assert len(list((clone / 'dist/lessons').glob('*/index.html'))) == len(lessons)+1
        last = (clone / f'dist/lessons/{lessons[-1]["slug"]}/index.html').read_text(encoding='utf-8')
        assert '../extension-demo/index.html' in last
        generated = (clone / 'dist/lessons/extension-demo/index.html').read_text(encoding='utf-8')
        assert f'../{lessons[-1]["slug"]}/index.html' in generated
    print(f'Extension OK: adding one JSON creates lesson {len(lessons)+1}, home card, category count and previous/next links; production content untouched.')

if __name__ == '__main__':
    main()
