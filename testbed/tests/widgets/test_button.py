# Handled differently in real testing with get_module()
from tests_backend.widgets.button import ButtonProbe
from tests_backend.proxies.button_proxy import ButtonProxy

from pytest import approx, fixture

# will need to have to work as async - ie dealing with asyncio event loops

@fixture
def widget():
    return ButtonProxy()

@fixture
def probe(widget):
    return ButtonProbe(widget)

def test_text_change(widget, probe):

    initial_height = probe.height

    widget.text = "new text"
    #await probe.redraw(f"Button text should be {text}")

    # Text after a newline will be stripped.
    #assert isinstance(widget.text, str)
    #expected = str("new text").split("\n")[0]
    expected = "new text"

    assert widget.text == expected
    assert probe.text == expected
    # GTK rendering can result in a very minor change in button height
    assert probe.height == approx(initial_height, abs=1)



    """
    #widget = ButtonProxy()
    #probe = ButtonProbe(widget)

    print(f"widget id: {widget.id}")
    print(f"widget text: {widget.text}")

    print(f"probe text: {probe.text}")

    widget.text = "new text"
    print("changed widget text to 'new text'")

    widget_text = widget.text
    probe_text = probe.text

    print(f"widget text: {widget.text}")
    print(f"probe text: {probe.text}")

    assert widget_text == probe_text
    """


