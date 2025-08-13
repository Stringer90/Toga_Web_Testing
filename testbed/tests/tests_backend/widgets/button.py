from ..page_singleton import PageSingleton
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
        object.__setattr__(self, "id", widget.id)
        object.__setattr__(self, "dom_id", f"toga_{widget.id}")

    def _locator(self):
        page = PageSingleton.get()
        return page.locator(f"#{self.dom_id}")

    def __getattr__(self, name):
        locator = self._locator()

        match name:
            case "text":
                return locator.inner_text()
            case "height":
                box = locator.bounding_box()
                return None if box is None else box["height"]

        return "No match"


    """
    # Separated into 3 lines for readability
    # Sync version
    @property
    def text(self):
        page = PageSingleton.get()
        button = page.locator(f"#{self.dom_id}")
        return button.inner_text()
    """