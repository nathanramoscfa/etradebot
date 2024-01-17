import os
import re
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Function to extract the version from __version__.py
def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, '__version__.py'), encoding='utf-8') as f:
        version_file_contents = f.read()
    # Use regular expression to extract version string
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file_contents, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='etradebot',
    version=get_version(),
    url='https://github.com/nathanramoscfa/etradebot',
    license='MIT',
    author='Nathan Ramos, CFA®',
    author_email='nathan.ramos.github@gmail.com',
    description='A Python-based trading bot for the E-Trade platform',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11, <3.12",
    install_requires=[
        'cvxpy==1.3.0',
        'dicttoxml==1.7.16',
        'jupyterlab==3.6.1',
        'keyring==23.13.1',
        'matplotlib==3.7.1',
        'numpy==1.24.2',
        'pandas>=2.0.3',
        'pyportfolioopt==1.5.5',
        'pytz==2022.7.1',
        'recommonmark',
        'requests==2.31.0',
        'scikit-learn==1.2.2',
        'scipy==1.10.1',
        'selenium==4.8.2',
        'setuptools<=64.0.2',
        'sphinx==6.1.3',
        'sphinx_rtd_theme',
        'statsmodels==0.13.5',
        'tqdm==4.65.0',
        'xmltodict==0.13.0',
        'yahooquery==2.3.6',
        'yfinance==0.2.12'
    ],
    extras_require={
        'bloomberg': [
            'blpapi==3.19.1',
            'tia'
        ],
        'github_forks': [
            'pyetrade==1.4.1',
            'pandas_market_calendars==4.3.3'
        ],
    },
    dependency_links=[
        'https://bcms.bloomberg.com/pip/simple/blpapi/',
        'git+https://github.com/PaulMest/tia.git#egg=tia',
        'git+https://github.com/nathanramoscfa/pyetrade.git#egg=pyetrade',
        'git+https://github.com/nathanramoscfa/pandas_market_calendars.git#egg=pandas-market-calendars'
    ]
)
