
""" 
TODO: 
Need to get this working with remote proxy classes. Otherwise manually.
Requires proxy objects 'replacing' toga objects dynamically if web.

from importlib import import_module

def get_probe(widget):
    name = type(widget).__name__
    module = import_module(f"tests_backend.widgets.{name.lower()}")
    return getattr(module, f"{name}Probe")(widget)
"""
from importlib import import_module

def get_probe(widget):
    name = type(widget).__name__          # e.g. "ButtonProxy"
    base = name.removesuffix("Proxy")     # -> "Button"
    module = import_module(f"tests.tests_backend.widgets.{base.lower()}")  # -> tests/tests_backend/widgets/button.py
    return getattr(module, f"{base}Probe")(widget)
