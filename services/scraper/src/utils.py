from playwright.async_api import async_playwright

async def get_html_with_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        html = await page.content()
        await browser.close()
        return html