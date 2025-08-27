# Handled differently in real testing with get_module()
from ..tests_backend.widgets.button import ButtonProbe
from ..tests_backend.proxies.button_proxy import ButtonProxy

from pytest import approx, fixture

@fixture
def widget():
    return ButtonProxy()

async def test_text_change(widget, probe):
    initial_height = probe.height

    widget.text = "new text"

    assert isinstance(widget.text, str)
    expected = str("new text").split("\n")[0]

    assert widget.text == expected
    assert probe.text == expected

    assert probe.height == approx(initial_height, abs=1)
