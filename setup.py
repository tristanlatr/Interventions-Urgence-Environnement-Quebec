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

REQUIREMENTS = """
    ordered-set==4.1.0
    geopy==2.2.0
    simplekml==1.3.6
    XlsxWriter==3.0.2
    lxml==4.7.1
    Scrapy==2.5.1
    scrapy-user-agents==0.1.1
    pyasn1==0.4.8
    geographiclib==1.52
    zope.interface==5.4.0
    w3lib==1.22.0
    service-identity==21.1.0
    queuelib==1.6.2
    pyOpenSSL==21.0.0
    Protego==0.1.16
    parsel==1.6.0
    itemloaders==1.0.4
    itemadapter==0.4.0
    h2==3.2.0
    cssselect==1.1.0
    cryptography==36.0.1
    Twisted==22.1.0rc1
    PyDispatcher==2.0.5
    user-agents==2.2.0
    six==1.16.0
    pyasn1-modules==0.2.8
    attrs==21.4.0
    jmespath==0.10.0
    hyperframe==5.2.0
    hpack==3.0.0
    cffi==1.15.0
    priority==1.3.0
    typing-extensions==4.0.1
    incremental==21.3.0
    hyperlink==21.0.0
    constantly==15.1.0
    Automat==20.2.0
    ua-parser==0.10.0
    pycparser==2.21
    idna==3.3
    setuptools==56.0.0
    """

setup(
    name='InterventionsUrgenceEnvironnementQuebec',
    description="InterventionsUrgenceEnvironnementQuebec generates an Excel file (also JSON) containing all information from the Registre des interventions d'Urgence-Environnement Québec.",
    url='https://github.com/tristanlatr/Interventions-Urgence-Environnement-Quebec',
    maintainer='tristanlatr',
    version='2.0.dev',
    packages=find_packages(),
    install_requires=[r.strip() for r in REQUIREMENTS.splitlines() if r.strip()],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    long_description=README,
    long_description_content_type="text/markdown"
)
