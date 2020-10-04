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


# -- Project information -----------------------------------------------------
"""
isort:skip_file
"""

from pathlib import Path
import sys

module_path = str(Path(__file__).parents[2].resolve()) + "/"
sys.path.insert(0, module_path)

import avionix

project = "Avionix"
copyright = "2020, Zach Brookler"
author = "Zach Brookler"
version = avionix.__version__

# The full version, including alpha/beta/rc tags
release = "0.3.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
autosummary_generate = True
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Add any links that may be too long to add in a docstring
extlinks = {
    "kubernetes_service_networking": (
        "https://kubernetes.io/docs/concepts/services-networking/%s",
        "https://kubernetes.io/docs/concepts/services-networking/",
    ),
    "kubernetes_access_application_cluster": (
        "https://kubernetes.io/docs/tasks/access-application-cluster/%s",
        "https://kubernetes.io/docs/tasks/access-application-cluster/",
    ),
    "kubernetes_controllers": (
        "https://kubernetes.io/docs/concepts/workloads/controllers/%s",
        "https://kubernetes.io/docs/concepts/workloads/controllers/",
    ),
    "kubernetes_working_with_objects": (
        "https://kubernetes.io/docs/concepts/overview/working-with-objects/%s",
        "https://kubernetes.io/docs/concepts/overview/working-with-objects/",
    ),
    "kubernetes_api_conventions": (
        "https://git.k8s.io/community/contributors/devel/sig-architecture/api"
        "-conventions.md#%s",
        "https://git.k8s.io/community/contributors/devel/sig-architecture/api"
        "-conventions.md#",
    ),
}
