# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
# -*- coding: utf-8 -*-


import sys, os


project = 'google_python_style'
copyright = '2021, zheng'
author = 'zheng'
master_doc = 'index'   


html_title = u'Google 开源项目风格指南'
htmlhelp_basename = 'zh-google-styleguide'
html_add_permalinks = ''


version = u''
release = u''

source_suffix = '.rst'
language = 'en_US'
exclude_patterns = ['_build']
extensions = ['sphinx.ext.imgmath']
pygments_style = 'sphinx'

# on_rtd is whether we are on readthedocs.org
import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


#Add sponsorship and project information to the template context.
context = {
    'MEDIA_URL': "/media/",
    'slug': 'google-styleguide',
    'name': u'Google 开源项目风格指南',
    'analytics_code': 'None',
}

html_context = context







# # -- Project information -----------------------------------------------------

# project = 'google_python_style'
# copyright = '2021, zheng'
# author = 'zheng'


# # -- General configuration ---------------------------------------------------

# # Add any Sphinx extension module names here, as strings. They can be
# # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# # ones.
# extensions = [
# ]

# # Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# # List of patterns, relative to source directory, that match files and
# # directories to ignore when looking for source files.
# # This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = []


# # -- Options for HTML output -------------------------------------------------

# # The theme to use for HTML and HTML Help pages.  See the documentation for
# # a list of builtin themes.
# #
# # html_theme = 'alabaster'
# html_theme = 'sphinx_rtd_theme'

# # Add any paths that contain custom static files (such as style sheets) here,
# # relative to this directory. They are copied after the builtin static files,
# # so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']