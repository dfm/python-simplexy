# -*- coding: utf-8 -*-

__version__ = "0.0.1"

try:
    __SIMPLEXY_SETUP__
except NameError:
    __SIMPLEXY_SETUP__ = False

if not __SIMPLEXY_SETUP__:
    __all__ = ["simplexy"]

    from .simplexy import simplexy
