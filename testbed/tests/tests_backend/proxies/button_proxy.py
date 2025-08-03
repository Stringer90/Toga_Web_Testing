
#Sync version
from ..page_singleton import PageSingleton
from playwright.sync_api import expect

class ButtonProxy:
    def __init__(self):
        self.id = self.setup()
        self.add_self_to_main_window()

    @property
    def text(self):
        page = PageSingleton.get()

        code = (
            f"result = self.my_widgets['{self.id}'].text"
        )

        result = page.evaluate("(code) => window.test_cmd(code)", code)
        return result
    
    @text.setter
    def text(self, value: str | None) -> None:
        
        # From core/button.py. Probably not needed yet
        #if value is None or value == "\u200b":
        #    value = ""
        #else:
        #    value = str(value).split("\n")[0]
        
        page = PageSingleton.get()

        code = (
            f"self.my_widgets['{self.id}'].text = '{value}'"
        )

        page.evaluate("(code) => window.test_cmd(code)", code)
    
    def setup(self):
        page = PageSingleton.get()

        code = (
            "new_widget = toga.Button('Hello')\n"
            "self.my_widgets[new_widget.id] = new_widget\n"
            "result = new_widget.id"
        )

        result = page.evaluate("(code) => window.test_cmd(code)", code)

        return result # ID of the widget in the remote web app
        
    def add_self_to_main_window(self):

        #- This method is for prototyping purposes only.
        #- Adding to main_window should be done in the probe fixture.
        #- This would require making a proxy for app, main_window and box, 
        #which has to be a ble to handle and child widgets at time of creation

        page = PageSingleton.get()

        code = (
            f"self.main_window.content.add(self.my_widgets['{self.id}'])"
        )

        page.evaluate("(code) => window.test_cmd(code)", code)
