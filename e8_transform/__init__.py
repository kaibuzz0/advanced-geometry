"""
E8-Aligned Modular Transform
A framework for mapping complex functions onto the E8 root lattice.

This package provides tools to:
- Transform complex functions into E8-aligned coordinates
- Analyze emergent symmetries via the Weyl group
- Visualize hidden geometric patterns

Author: kaibuzz0
License: MIT
"""

__version__ = "0.1.0"
__author__ = "kaibuzz0"

from .core import E8Structure, E8Transform
from .analyzer import SymmetryAnalyzer

__all__ = [
    "E8Structure",
    "E8Transform", 
    "SymmetryAnalyzer",
]
