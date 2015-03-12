import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="rpi_dots",
    version="0.2.2",
    author="Ben Nuttall",
    author_email="ben@raspberrypi.org",
    description="Software for the DOTS board for the Raspberry Pi",
    long_description=read('README.rst'),
    license="BSD",
    keywords=[
        "raspberrypi",
        "dots",
        "dots board",
        "connect the dots",
        "bare conductive",
        "conductive paint",
    ],
    url="https://github.com/raspberrypilearning/dots",
    packages=find_packages(),
    scripts=['scripts/rpi_dots'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
    ],
)
