#  Copyright (c) 2023 frosty.
#
#  This file is released under the "MIT License". Please see the LICENSE file that should have
#  been included as part of this package for more information.

from setuptools import find_packages, setup

setup(
    name="grab",
    version="1.1.0",
    py_modules=["grab"],
    install_requires=["Click", "pyperclip", "PyYAML"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "grab = grab.__main__:cli",
        ],
    },
)
