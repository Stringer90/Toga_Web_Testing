# Handled differently in real testing with get_module()
from tests_backend.widgets.button import ButtonProbe
from tests_backend.proxies.button_proxy import ButtonProxy

from pytest import fixture

# will need to have to work as async - ie dealing with asyncio event loops

@fixture
def widget():
    return ButtonProxy()

@fixture
def probe(widget):
    return ButtonProbe(widget)

def test_text_change(widget, probe):
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



