from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='etradebot',
    version='3.0.1',
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
    python_requires="==3.11",
    install_requires=[
        'cvxpy==1.3.0',
        'jupyterlab==3.6.1',
        'keyring==23.13.1',
        'matplotlib==3.7.1',
        'numpy==1.24.2',
        'pandas==1.5.3',
        'pyportfolioopt==1.5.5',
        'scikit-learn==1.2.2',
        'scipy==1.10.1',
        'selenium==4.8.2',
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
        ]
    },
    dependency_links=[
        'https://bcms.bloomberg.com/pip/simple/blpapi/',
        'git+https://github.com/PaulMest/tia.git#egg=tia'
    ]
)
