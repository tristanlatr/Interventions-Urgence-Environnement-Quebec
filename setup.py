#! /usr/bin/env python3
from setuptools import setup, find_packages
import sys
if sys.version_info[0] < 3: 
    raise RuntimeError("You must use Python 3")
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name='InterventionsUrgenceEnvironnementQuebec',
    description="InterventionsUrgenceEnvironnementQuebec generates an Excel file (also JSON) containing all information from the Registre des interventions d'Urgence-Environnement Québec.",
    url='https://github.com/tristanlatr/Interventions-Urgence-Environnement-Quebec',
    maintainer='tristanlatr',
    version='2.0.dev',
    packages=find_packages(),
    install_requires=[
          'pyasn1==0.4.8', 
          'scrapy-user-agents==0.1.1', 
          'scrapy==2.5.1', 
          'lxml==4.7.1', 
          'XlsxWriter==3.0.2', 
          'simplekml==1.3.6', 
          'geopy==2.2.0', 
          'ordered-set==4.1.0', 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    long_description=README,
    long_description_content_type="text/markdown"
)
