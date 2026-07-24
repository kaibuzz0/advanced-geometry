"""
E8-Aligned Modular Transform
A mathematical framework for mapping complex functions onto the E8 root lattice.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="e8-transform",
    version="0.1.0",
    author="kaibuzz0",
    description="A mathematical innovation framework mapping complex functions onto E8 root lattice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaibuzz0/advanced-geometry",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "plotly>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "e8-demo=demo:main",
        ],
    },
)
