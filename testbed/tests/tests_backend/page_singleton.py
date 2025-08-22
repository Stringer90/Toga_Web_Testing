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

import asyncio, threading
from typing import Any, Optional
from playwright.async_api import async_playwright


class BackgroundPage:
    _inst = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._inst is None:
                cls._inst = super().__new__(cls)
        return cls._inst

    @classmethod
    def get(cls) -> "BackgroundPage":
        return cls()

    def __init__(self):
        if getattr(self, "_init", False):
            return
        self._init = True
        self._mutex = threading.Lock()
        self._ready = threading.Event()
        self._bootstrap_err: Optional[Exception] = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread = threading.Thread(target=self._run, name="PageLoop", daemon=True)
        self._thread.start()
        self._ready.wait()
        if self._bootstrap_err is not None:
            raise RuntimeError(f"BackgroundPage failed to initialize: {self._bootstrap_err}") from self._bootstrap_err

    def eval_js(self, js: str, *args, timeout: Optional[float] = None) -> Any:
        if self._bootstrap_err is not None:
            raise RuntimeError(f"BackgroundPage not usable: {self._bootstrap_err}") from self._bootstrap_err
        with self._mutex:
            fut = asyncio.run_coroutine_threadsafe(self._eval(js, *args), self._loop)
            return fut.result(timeout=timeout)

    async def eval_js_async(self, js: str, *args, timeout: Optional[float] = None) -> Any:
        if self._bootstrap_err is not None:
            raise RuntimeError(f"BackgroundPage not usable: {self._bootstrap_err}") from self._bootstrap_err
        fut = asyncio.run_coroutine_threadsafe(self._eval(js, *args), self._loop)
        return await asyncio.wait_for(asyncio.wrap_future(fut), timeout=timeout)

    def _run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.create_task(self._bootstrap())
        self._loop.run_forever()
        self._loop.close()

    async def _bootstrap(self):
        try:
            self._play = await async_playwright().start()
            self._browser = await self._play.chromium.launch(headless=True)
            self._context = await self._browser.new_context()
            self._page = await self._context.new_page()

            await self._page.goto("http://localhost:8080")
            #await self._page.goto("http://localhost:8080", wait_until="load", timeout=30_000)
            await self._page.wait_for_timeout(5000)

            await self._page.evaluate("(code) => window.test_cmd(code)", "self.my_widgets = {}")

            self._alock = asyncio.Lock()
        except Exception as e:
            self._bootstrap_err = e
            self._alock = asyncio.Lock()
        finally:
            self._ready.set()

    async def _eval(self, js: str, *args):
        async with self._alock:
            return await self._page.evaluate(js, *args)

    def run_coro(self, coro_fn, *args, timeout=None, **kwargs):
        async def _runner():
            async with self._alock:
                return await coro_fn(self._page, *args, **kwargs)

        fut = asyncio.run_coroutine_threadsafe(_runner(), self._loop)
        return fut.result(timeout=timeout)

    async def run_coro_async(self, coro_fn, *args, timeout=None, **kwargs):
        async def _runner():
            async with self._alock:
                return await coro_fn(self._page, *args, **kwargs)

        fut = asyncio.run_coroutine_threadsafe(_runner(), self._loop)
        return await asyncio.wait_for(asyncio.wrap_future(fut), timeout=timeout)


"""
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
"""
