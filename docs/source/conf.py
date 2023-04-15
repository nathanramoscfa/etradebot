# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'etradebot'
copyright = '2023, Nathan Ramos, CFA®'
author = 'Nathan Ramos, CFA®'
version = '1.0.2'
release = '1.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'recommonmark',
]

templates_path = ['_templates']
exclude_patterns = []

# Configure the source suffix to include both 'bloomberg.rst' and '.md' file types
source_suffix = ['.rst', '.md']
source_encoding = 'utf-8'
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

extensions.append('sphinx_rtd_theme')
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
