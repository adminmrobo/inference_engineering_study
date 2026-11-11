# -*- coding: utf-8 -*-
"""페이지 점검: 콘솔 오류, 390px 가로 넘침, 스크린샷. 사용: python3 check.py page.html [shot_prefix]"""
import sys, asyncio
from playwright.async_api import async_playwright

async def main(path, shot):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for w in (1280, 390):
            pg = await b.new_page(viewport={'width': w, 'height': 900})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'fonts' not in m.text and 'ERR_' not in m.text else None)
            await pg.goto('file://' + path)
            await pg.wait_for_timeout(800)
            for sel in ['.reveal', '[data-reveal]', '.quiz .bt', '[data-zip]']:
                for el in (await pg.query_selector_all(sel))[:6]:
                    try: await el.click(timeout=1000)
                    except Exception: pass
            await pg.wait_for_timeout(500)
            if shot and w == 1280:
                d = await pg.query_selector('#duelBox')
                if d: await d.screenshot(path=shot + '_duel.png')
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            print(w, 'scrollWidth', sw, 'errors', errs[:5])
            if shot:
                await pg.screenshot(path='%s_%d.png' % (shot, w), full_page=False)
                if w == 1280:
                    h = await pg.evaluate('document.documentElement.scrollHeight')
                    print('height', h)
            await pg.close()
        await b.close()

asyncio.run(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
