# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import sys


def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, '../../__version__.py'), encoding='utf-8') as f:
        version_file_contents = f.read()
    # Use regular expression to extract version string
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file_contents, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'etradebot'
copyright = '2024, Nathan Ramos, CFA®'
author = 'Nathan Ramos, CFA®'
version = get_version()
release = get_version()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'recommonmark',
]

templates_path = ['_templates']
exclude_patterns = []

# Configure the source suffix to include both 'data.rst' and '.md' file types
source_suffix = ['.rst', '.md']
source_encoding = 'utf-8'
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

extensions.append('sphinx_rtd_theme')
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
