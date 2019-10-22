import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "equity-correlation-python",
    version = "0.0.1",
    author = "Aaron Tan",
    author_email = "aarontanzk@gmail.com",
    description = ("Equity Correlation In Python "),
    license = "BSD",
    keywords = "risk",
    url = "http://nil.com",
    packages=[
        "package"
    ],
    long_description=open('README.txt').read(),
    install_requires=[
       "alpha_vantage",
       "pandas",
       "sqlalchemy",
       "pyodbc",
       "matplotlib"
    ],
)