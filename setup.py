"""
PyAnime4Up
~~~~~~~~~
:Copyright: (c) 2021 By Amine Soukara <https://github.com/AmineSoukara>.
:License: MIT, See LICENSE For More Details.
:Description: A Selenium-less Python Anime4Up Library
"""

from setuptools import find_packages, setup

AUTHOR = "AmineSoukara"
EMAIL = "AmineSoukara@gmail.com"
URL = "https://github.com/AmineSoukara/PyAnime4Up"


# Get the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


VERSION = input("Input The New Version Number You Are Going To Use: ")

setup(
    name="PyAnime4Up",
    version=VERSION,
    description="A Selenium-less Python Anime4Up Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license="MIT",
    packages=find_packages(),
    keywords="Anime Anime4Up Scrapper Python",
    project_urls={
        "Source": "https://github.com/AmineSoukara/PyAnime4Up",
        "Documentation": "https://github.com/AmineSoukara/PyAnime4Up#readme",
        "Tracker": "https://github.com/AmineSoukara/PyAnime4Up/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
    ],
    python_requires=">=3.6",
    install_requires=["aiohttp", "urllib3", "bs4", "requests"],
)
