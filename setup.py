from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-unsafe-expose-env",
    description="Datasette plugin to expose some environment variables at /-/env for debugging",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-unsafe-expose-env",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-unsafe-expose-env/issues",
        "CI": "https://github.com/simonw/datasette-unsafe-expose-env/actions",
        "Changelog": "https://github.com/simonw/datasette-unsafe-expose-env/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_unsafe_expose_env"],
    entry_points={"datasette": ["unsafe_expose_env = datasette_unsafe_expose_env"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    tests_require=["datasette-unsafe-expose-env[test]"],
    python_requires=">=3.6",
)
