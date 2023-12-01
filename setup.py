import setuptools

with open("README.md") as readme:
    long_description = readme.read()

with open("requirements.txt") as req:
    packages = req.read().splitlines()

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
    include_package_data=True,
    entry_points={"console_scripts": ["grab=grab"]},
    python_requires=">=3.11",
)
