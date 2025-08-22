#from ..page_singleton import PageSingleton, BackgroundPage
from ..page_singleton import BackgroundPage
#from beeware_web_testing.web.tests_backend.page_singleton import PageSingleton

"""
Potential Improvements (more research/testing needed):
- Have the page singleton instance a class variable, so don't need to call get() in every method.
- In __init__, locate the button and store the located element as a class variable,
  ie 'self.button = page.locator(f"#{self.dom_id}")'.
  Won't need to keep locating it.
"""

class ButtonProbe:
    def __init__(self, widget):
        self.id = widget.id
        self.dom_id = f"toga_{self.id}"

    # Separated into 3 lines for readability
    # Sync version
    @property
    def text(self):

        """
        page = PageSingleton.get()
        button = page.locator(f"#{self.dom_id}")
        return button.inner_text()
        """
        w = BackgroundPage.get()
        return w.run_coro(lambda page: page.locator(f"#{self.dom_id}").inner_text())




