# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`conftest.py`
=============

Configuration file for pytest

# Author(s): Alec Delaney

"""

import sys
import socket
import importlib


MODULE_NAMES = [
    ("wifi", None, []),
    ("secrets", None, ["secrets"]),
    ("pwmio", None, ["PWMOut"]),
    ("audioio", None, ["AudioOut"]),
    ("adafruit_waveform", None, ["sine"]),
    ("microcontroller", None, ["Pin"]),
]

for name, parent, additionals in MODULE_NAMES:

    _spec = importlib.machinery.ModuleSpec(name, None)
    _module = importlib.util.module_from_spec(_spec)
    for additional in additionals:
        setattr(_module, additional, None)
    if parent:
        parent_path = parent.split(".")
        parent_module = sys.modules[parent_path[0]]
        for module_step in parent_path[1:]:
            parent_module = getattr(parent_module, module_step)
        setattr(parent_module, name, _module)

    sys.modules[name] = _module

sys.modules["socketpool"] = socket


def pytest_addoption(parser):
    """Add options for the pytest command line"""

    parser.addoption("--location", action="store")


def pytest_generate_tests(metafunc):
    """Generate pytest tests"""

    location = metafunc.config.option.location

    if "location" in metafunc.fixturenames and location is not None:
        metafunc.parametrize("location", [location])
