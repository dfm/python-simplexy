#!/usr/bin/env python

import os

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

if __name__ == "__main__":
    import sys
    import numpy

    # Publish the library to PyPI.
    if "publish" in sys.argv[-1]:
        os.system("python setup.py sdist upload")
        sys.exit()

    # Set up the C++-extension.
    libraries = []
    if os.name == "posix":
        libraries.append("m")

    # List all the required source files.
    AN_PATH = os.environ.get("ASTROMETRY_SRC", "an")
    sources = [os.path.join(AN_PATH, "util", fn) for fn in (
        # "main.c",
        "an-endian.c",
        "bl.c",
        "ctmf.c",
        "errors.c",
        "fitsioutils.c",
        "ioutils.c",
        "log.c",
        "resample.c",
        "simplexy.c",
        "dallpeaks.c",
        "permutedsort.c",
        "dcen3x3.c",
        "dpeaks.c",
        "dselip.c",
        "dsigma.c",
        "dsmooth.c",
        #"radix.c",
        "dfind.c",
        "dmedsmooth.c",
        "dobjects.c",
        "tic.c",
        "mathutil.c",
    )] + [os.path.join(AN_PATH, "qfits-an", fn) for fn in (
        "anqfits.c",
        "md5.c",
        "qfits_byteswap.c",
        "qfits_card.c",
        "qfits_convert.c",
        "qfits_error.c",
        "qfits_float.c",
        "qfits_header.c",
        "qfits_image.c",
        "qfits_md5.c",
        "qfits_memory.c",
        "qfits_rw.c",
        "qfits_table.c",
        "qfits_time.c",
        "qfits_tools.c",
    )]
    if not all(map(os.path.exists, sources)):
        raise RuntimeError("Please set the environment variable "
                           "ASTROMETRY_SRC to the location of your "
                           "astrometry.net installation")
    include_dirs = [
        os.path.join(AN_PATH, "include"),
        os.path.join(AN_PATH, "include", "astrometry"),
        numpy.get_include(),
    ]

    # Set up the extension.
    ext_fn = os.path.join("simplexy", "_simplexy")
    if os.path.exists(ext_fn + ".pyx"):
        from Cython.Build import cythonize
        ext_fn += ".pyx"
    else:
        ext_fn += ".c"
        cythonize = lambda x: x

    extensions = cythonize([
        Extension("simplexy._simplexy", sources=sources + [ext_fn],
                  include_dirs=include_dirs)
    ], language_level = "3")

    # Hackishly inject a constant into builtins to enable importing of the
    # package before the library is built.
    if sys.version_info[0] < 3:
        import __builtin__ as builtins
    else:
        import builtins
    builtins.__SIMPLEXY_SETUP__ = True
    import simplexy

    setup(
        name="simplexy",
        version=simplexy.__version__,
        author="Daniel Foreman-Mackey",
        author_email="danfm@nyu.edu",
        url="https://github.com/dfm/python-simplexy",
        license="MIT",
        packages=["simplexy", ],
        ext_modules=extensions,
        description="Python bindings to simplexy",
        long_description=open("README.rst").read(),
        package_data={"": ["README.rst", "LICENSE",
                           os.path.join("simplexy", "_simplexy.c"), ]},
        #include_package_data=True,
        classifiers=[
            # "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
        ],
    )
