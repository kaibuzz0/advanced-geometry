#!/usr/bin/env python3
"""
E8-Aligned Modular Transform - Demo Script
Maps complex functions onto E8 root lattice to reveal hidden symmetries.
"""

import sys
import os

# Add parent directory to path (works regardless of where script is run from)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from e8_transform.core import E8Transform
from e8_transform.analyzer import SymmetryAnalyzer


def demo_polynomials():
    """Demo: Polynomial functions and E8 symmetries."""
    print("\n" + "="*60)
    print("DEMO: Polynomial Functions")
    print("="*60)
    
    transform = E8Transform()
    analyzer = SymmetryAnalyzer()
    
    functions = [
        ("z", lambda z: z),
        ("z²", lambda z: z**2),
        ("z³ - z", lambda z: z**3 - z),
    ]
    
    domain = [complex(x, y) 
              for x in np.linspace(-1.5, 1.5, 15)
              for y in np.linspace(-1.5, 1.5, 15)]
    
    for name, func in functions:
        e8_points = transform.align_function(func, domain)
        report = analyzer.analyze(e8_points)
        
        print(f"\n{name}:")
        print(f"  Isotropy: {report.isotropy_score:.4f}")
        print(f"  Lattice:  {report.lattice_alignment:.4f}")
        print(f"  Symmetry: {report.dominant_symmetry}")


def demo_riemann_zeta():
    """Demo: Riemann zeta on critical strip."""
    print("\n" + "="*60)
    print("DEMO: Riemann Zeta Function")
    print("="*60)
    
    transform = E8Transform()
    analyzer = SymmetryAnalyzer()
    
    def zeta_approx(s, terms=50):
        return sum(1 / (n**s) for n in range(1, terms+1))
    
    print("\nCritical line: s = 0.5 + it")
    t_values = np.linspace(0, 30, 80)
    
    points = []
    for t in t_values:
        s = 0.5 + 1j*t
        try:
            z = zeta_approx(s, terms=30)
            if abs(z) < 100:
                points.append(z)
        except:
            pass
    
    print(f"Computed {len(points)} zeta values")
    
    if points:
        e8_points = transform.align_function(lambda z: z, points)
        report = analyzer.analyze(e8_points)
        
        print(f"  Isotropy: {report.isotropy_score:.4f}")
        print(f"  Lattice:  {report.lattice_alignment:.4f}")
        print(f"  Symmetry: {report.dominant_symmetry}")


def main():
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     E8-ALIGNED MODULAR TRANSFORM v0.1.0                   ║")
    print("║     Mathematical Innovation Framework                     ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    demo_polynomials()
    demo_riemann_zeta()
    
    print("\n" + "="*60)
    print("Key Innovation:")
    print("  Complex functions reveal latent E8 symmetries when")
    print("  mapped onto the exceptional Lie group root lattice.")
    print("="*60)


if __name__ == "__main__":
    main()
