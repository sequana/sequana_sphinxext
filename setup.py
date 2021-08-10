from setuptools import setup, find_packages


_MAJOR = 0
_MINOR = 1
_MICRO = 0
version = f"{_MAJOR}.{_MINOR}.{_MICRO}"
release = f"{_MAJOR}.{_MINOR}"

metainfo = {
    "authors": {"main": ("Thomas Cokelaer", "thomas.cokelaer@pasteur.fr")},
    "maintainer": {"main": ("Thomas Cokelaer", "thomas.cokelaer@pasteur.fr")},
    "version": version,
    "license": "new BSD",
    "url": "http://github.com/sequana/sequana_sphinxext",
    "description": "A set of standalone application and pipelines dedicated to NGS (new generation sequencing) analysis",
    "platforms": ["Linux", "Unix", "MacOsX", "Windows"],
    "keywords": ["NGS", "snakemake"],
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
}


setup(
    name="sequana_sphinxext",
    version=version,
    maintainer=metainfo["authors"]["main"][0],
    maintainer_email=metainfo["authors"]["main"][1],
    author=metainfo["authors"]["main"][0],
    author_email=metainfo["authors"]["main"][1],
    long_description=open("README.rst").read(),
    keywords=metainfo["keywords"],
    description=metainfo["description"],
    license=metainfo["license"],
    platforms=metainfo["platforms"],
    url=metainfo["url"],
    classifiers=metainfo["classifiers"],
    # package installation
    packages=find_packages(exclude=["tests*"]),
    install_requires=open("requirements.txt", "r").read(),
    tests_require=["pytest", "coverage", "pytest-cov"],
    # This is recursive include of data files
    exclude_package_data={"": ["__pycache__"]},
    zip_safe=False,
)
