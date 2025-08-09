# Singleton to hold page object

# Sync version
"""
from playwright.sync_api import sync_playwright

class PageSingleton:
    _playwright = None
    _browser = None
    _page = None
    _url = "http://localhost:8080" 

    @classmethod
    def get(cls):
        if cls._page is None:
            cls._playwright = sync_playwright().start()
            cls._browser = cls._playwright.chromium.launch(headless=True)
            cls._page = cls._browser.new_page()
            cls._page.goto(cls._url)

            # Let page load
            cls._page.wait_for_timeout(5000)

            # Initially create dictionary of widgets that will be created during testing
            code = (
                "self.my_widgets = {}"
            )
            cls._page.evaluate("(code) => window.test_cmd(code)", code)

        return cls._page

    # Even needed? Will be destroyed after program ends anyway (right?)
    @classmethod
    def close(cls):
        if cls._browser:
            cls._browser.close()
            cls._playwright.stop()
            cls._browser = None
            cls._playwright = None
            cls._page = None
"""

# Async version

import asyncio
from playwright.async_api import async_playwright

class PageSingleton:
    _playwright = None
    _browser = None
    _page = None
    _url = "http://localhost:8080"

    @classmethod
    async def get(cls):
        if cls._page is None:
            cls._playwright = await async_playwright().start()
            cls._browser = await cls._playwright.chromium.launch(headless=True)
            cls._page = await cls._browser.new_page()
            await cls._page.goto(cls._url)

            # Let page load
            await cls._page.wait_for_timeout(5000)

            # Create initial dictionary of widgets
            code = (
                "self.my_widgets = {}"
            )
            await cls._page.evaluate("(code) => window.test_cmd(code)", code)

        return cls._page

    @classmethod
    async def close(cls):
        if cls._browser is not None:
            await cls._browser.close()
            await cls._playwright.stop()
            cls._playwright = None
            cls._browser = None
            cls._page = None

