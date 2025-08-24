# Handled differently in real testing with get_module()
from tests_backend.widgets.button import ButtonProbe
from tests_backend.proxies.button_proxy import ButtonProxy

from pytest import approx, fixture

@fixture
def widget():
    return ButtonProxy()

@fixture
def probe(widget):
    return ButtonProbe(widget)

async def test_text_change(widget, probe):
    initial_height = probe.height

    widget.text = "new text"

    assert isinstance(widget.text, str)
    expected = str("new text").split("\n")[0]

    assert widget.text == expected
    assert probe.text == expected

    assert probe.height == approx(initial_height, abs=1)

# Second async test method to check that no errors occur
async def test_text_change2():
    widget = ButtonProxy()
    probe = ButtonProbe(widget)
    widget.text = "new text2"
    assert widget.text == probe.text

    
