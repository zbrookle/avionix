from distutils.core import setup
import os
from pathlib import Path

from setuptools import find_packages

import versioneer

CODE_DIRECTORY = Path(__file__).parent


def read_file(filename):
    """Source the contents of a file"""
    with open(
        os.path.join(os.path.dirname(__file__), filename), encoding="utf-8"
    ) as file:
        return file.read()


setup(
    name="avionix",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    long_description="Coming soon...",
    maintainer="Varun Rao and Zach Brookler",
    maintainer_email="zachb1996@yahoo.com",
    description="A package for soldifying kubernetes structure and development by "
    "using objects and code rather than yaml",
    python_requires=">=3.6.1",
    install_requires=["pyyaml==5.3.1"],
    project_urls={
        "Source Code": "https://github.com/zbrookle/avionix",
        "Documentation": "https://github.com/zbrookle/avionix",
        "Bug Tracker": "https://github.com/zbrookle/avionix/issues",
    },
    url="https://github.com/zbrookle/avionix",
    download_url="https://github.com/zbrookle/avionix/archive/master.zip",
    keywords=["kuberenetes", "helm", "yaml", "docker", "infrastructure"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Typing :: Typed",
        "Operating System :: OS Independent",
    ],
    long_description_content_type="text/markdown",
    include_package_data=True,
)
