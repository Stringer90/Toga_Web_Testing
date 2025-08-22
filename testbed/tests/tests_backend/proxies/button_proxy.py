
#Sync version
#from ..page_singleton import PageSingleton, BackgroundPage
from ..page_singleton import BackgroundPage
from playwright.sync_api import expect
import asyncio
from concurrent.futures import Future

class ButtonProxy:
    def __init__(self):
        self.id = self.setup()
        self.add_self_to_main_window()

    """
    @property
    async def text(self):
        page = await PageSingleton.get()

        code = (
            f"result = self.my_widgets['{self.id}'].text"
        )

        result = await page.evaluate("(code) => window.test_cmd(code)", code)
        return result
    """
    
    @property
    def text(self):
        """
        async def _get(self):
            page = await PageSingleton.get()

            code = (
                f"result = self.my_widgets['{self.id}'].text"
            )
            return await page.evaluate("(code) => window.test_cmd(code)", code)
        
        #loop = asyncio.get_current_loop()
        loop = asyncio.get_event_loop()
        #loop = asyncio.get_running_loop()

        return loop.run_until_complete(_get())

        #future = asyncio.run_coroutine_threadsafe(_get(), loop)
        #return future.result()
        """
        
        w = BackgroundPage.get()
        code = (
            f"result = self.my_widgets['{self.id}'].text"
        )
        return w.eval_js("(code) => window.test_cmd(code)", code)


    @text.setter
    def text(self, value: str | None) -> None:
        
        #From core/button.py. Probably not needed yet
        """
        if value is None or value == "\u200b":
            value = ""
        else:
            value = str(value).split("\n")[0]
        """
        
        """
        page = PageSingleton.get()

        code = (
            f"self.my_widgets['{self.id}'].text = '{value}'"
        )

        await page.evaluate("(code) => window.test_cmd(code)", code)
        """

        """
        async def _set(self, code):
            page = await PageSingleton.get()
            await page.evaluate("(code) => window.test_cmd(code)", code)

        code = (
            f"self.my_widgets['{self.id}'].text = '{value}'"
        )

        #loop = asyncio.get_current_loop()
        loop = asyncio.get_event_loop()
        #loop = asyncio.get_running_loop()

        loop.run_until_complete(_set(self, code))

        #loop = asyncio.get_event_loop()
        #loop.create_task(self._set_text(code))
        """

        w = BackgroundPage.get()
        code = (
            f"self.my_widgets['{self.id}'].text = '{value}'"
        )
        #f"self.my_widgets[{self.id!r}].text = {value!r}\n"
        w.eval_js("(code) => window.test_cmd(code)", code)


    """
    async def _set_text(self, code):
        page = await PageSingleton.get()
        await page.evaluate("(code) => window.test_cmd(code)", code)
    """
        
    def setup(self):
        """
        page = await PageSingleton.get()

        code = (
            "new_widget = toga.Button('Hello')\n"
            "self.my_widgets[new_widget.id] = new_widget\n"
            "result = new_widget.id"
        )

        result = await page.evaluate("(code) => window.test_cmd(code)", code)

        return result # ID of the widget in the remote web app
        """

        """
        async def _setup(self):
            page = await PageSingleton.get()
            code = (
                "new_widget = toga.Button('Hello')\n"
                "self.my_widgets[new_widget.id] = new_widget\n"
                "result = new_widget.id"
            )
            result = await page.evaluate("(code) => window.test_cmd(code)", code)
            return result # ID of the widget in the remote web app

        #loop = asyncio.get_current_loop()
        loop = asyncio.get_event_loop()
        #loop = asyncio.get_running_loop()

        loop.run_until_complete(_setup(self))
        """
        
        w = BackgroundPage.get()
        code = (
            "new_widget = toga.Button('Hello')\n"
            "self.my_widgets[new_widget.id] = new_widget\n"
            "result = new_widget.id"
        )
        return w.eval_js("(code) => window.test_cmd(code)", code)

        
    def add_self_to_main_window(self):

        #- This method is for prototyping purposes only.
        #- Adding to main_window should be done in the probe fixture.
        #- This would require making a proxy for app, main_window and box, 
        #which has to be a ble to handle and child widgets at time of creation

        """
        page = await PageSingleton.get()

        code = (
            f"self.main_window.content.add(self.my_widgets['{self.id}'])"
        )

        await page.evaluate("(code) => window.test_cmd(code)", code)
        """

        """
        async def _add_self(self):
            page = await PageSingleton.get()
            code = (
                f"self.main_window.content.add(self.my_widgets['{self.id}'])"
            )
            result = await page.evaluate("(code) => window.test_cmd(code)", code)
            return result # ID of the widget in the remote web app

        #loop = asyncio.get_current_loop()
        loop = asyncio.get_event_loop()
        #loop = asyncio.get_running_loop()

        loop.run_until_complete(_add_self(self))
        """

        w = BackgroundPage.get()
        code = (
            f"self.main_window.content.add(self.my_widgets['{self.id}'])"
        )
        w.eval_js("(code) => window.test_cmd(code)", code)



