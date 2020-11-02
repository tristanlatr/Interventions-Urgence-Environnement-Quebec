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
    description="InterventionsUrgenceEnvironnementQuebec fournis à toute personne intéressée un fichier Excel (et CSV) contenant toute les informations du registre des interventions d'Urgence-Environnement Québec. Le fichier est actualisé tous les jours",
    url='https://github.com/tristanlatr/InterventionsUrgenceEnvironnementQuebec',
    maintainer='tristanlatr',
    version='1.0',
    packages=find_packages(),
    install_requires=[
          'pyasn1', 'scrapy-user-agents', 'scrapy', 'bs4', 'XlsxWriter'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    long_description=README,
    long_description_content_type="text/markdown"
)