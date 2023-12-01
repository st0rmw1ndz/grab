from pathlib import Path

import setuptools

with Path.open("README.md", mode="r") as f:
    long_description = f.read()

with Path.open("requirements.txt", mode="r") as f:
    packages = f.read().splitlines()

setuptools.setup(
    name="grab",
    version="1.0.0",
    author="st0rm",
    author_email="inthishouseofcards@gmail.com",
    description="simple paste system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/st0rmw1ndz/grab",
    packages=setuptools.find_packages(),
    install_requires=packages,
    entry_points={"console_scripts": ["grab=grab:main"]},
    python_requires=">=3.11",
)
