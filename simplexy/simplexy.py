# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["simplexy"]

import numpy as np

from ._simplexy import simplexy as run_simplexy


_dtype = np.dtype([("x", np.float32), ("y", np.float32),
                   ("flux", np.float32), ("bkg", np.float32)])


def simplexy(img, **kwargs):
    r = run_simplexy(np.ascontiguousarray(img.T, dtype=np.float32),
                     **kwargs).T
    return np.array(list(zip(*r)), dtype=_dtype)
