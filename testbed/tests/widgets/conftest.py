import pytest
import toga
from .probe import get_probe
from ..tests_backend.proxies.box_proxy import BoxProxy

""" TODO: Don't enable until below is implemented.
@pytest.fixture
async def widget():
    raise NotImplementedError("test modules must define a `widget` fixture")
"""

""" TODO: Implement. atm: manually in each widget test file.
@pytest.fixture
async def probe(main_window, widget):
    old_content = main_window.content

    box = toga.Box(children=[widget])
    main_window.content = box
    probe = get_probe(widget)
    await probe.redraw(f"\nConstructing {widget.__class__.__name__} probe")
    probe.assert_container(box)
    yield probe

    main_window.content = old_content
"""
#sync ver
@pytest.fixture
def probe(main_window, widget):
    old_content = main_window.content
    box = BoxProxy(children=[widget])
    main_window.content = box
    probe = get_probe(widget)
    yield probe
    main_window.content = old_content