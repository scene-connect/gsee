#!/usr/bin/env python

from setuptools import Extension, setup

# Numpy headers are always required for compliation, but to allow
# `python setup.py egg_info` to work on install in a clean environment,
# the numpy import must be wrapped in a try-except block.
try:
    import numpy as np

    numpy_include = [np.get_include()]
except ImportError:
    numpy_include = []

setup(
    ext_modules=[
        Extension(
            "gsee.climatedata_interface.kt_h_sinusfunc",
            ["gsee/climatedata_interface/kt_h_sinusfunc.pyx"],
            include_dirs=numpy_include,
        )
    ],
)
