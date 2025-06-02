from playwright.async_api import async_playwright

async def get_html_with_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url)
        except Exception as e:
            print(f"Error al cargar la página {url}. Reintentando...")
            try:
                await page.goto(url, timeout=60000)
            except Exception as e:
                print(f"Error al cargar la página {url} después del reintento: {e}")
                await browser.close()
                return None
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        html = await page.content()
        await browser.close()
        return html