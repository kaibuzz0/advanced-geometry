"""
Core E8 mathematical structures and transformation engine.
"""

import numpy as np
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class E8Structure:
    """
    E8 Exceptional Lie Group - The most symmetric structure in mathematics.
    
    Properties:
    - Rank: 8 (number of independent Cartan generators)
    - Dimension: 248 (number of group elements/Lie algebra dimension)
    - Weyl Group Order: 696,729,600 (symmetries of root system)
    - Root Count: 240 (vectors in 8D space)
    """
    RANK: int = 8
    DIMENSION: int = 248
    WEYL_ORDER: int = 696729600
    ROOT_COUNT: int = 240
    COXETER_NUMBER: int = 30
    
    def __post_init__(self):
        object.__setattr__(self, '_simple_roots', self._compute_simple_roots())
        object.__setattr__(self, '_root_lattice', self._compute_root_lattice())
    
    def _compute_simple_roots(self) -> np.ndarray:
        """Compute the 8 simple roots of E8."""
        roots = np.zeros((8, 8))
        for i in range(7):
            roots[i, i] = 1
            roots[i, i+1] = -1
        roots[7] = np.array([-0.5] * 6 + [0.5, 0.5])
        return roots
    
    def _compute_root_lattice(self) -> np.ndarray:
        """Generate the 240 roots of E8 lattice."""
        roots = []
        from itertools import product
        
        # Type 1: 112 roots (±1, ±1, 0, 0, 0, 0, 0, 0)
        for i in range(8):
            for j in range(i+1, 8):
                for s1 in [1, -1]:
                    for s2 in [1, -1]:
                        root = np.zeros(8)
                        root[i] = s1
                        root[j] = s2
                        roots.append(root)
        
        # Type 2: 128 roots (±1/2, ..., ±1/2) with even minus signs
        for signs in product([1, -1], repeat=8):
            if np.prod(signs) == 1:
                root = np.array(signs) * 0.5
                roots.append(root)
        
        return np.array(roots)
    
    @property
    def simple_roots(self) -> np.ndarray:
        return self._simple_roots
    
    @property
    def root_lattice(self) -> np.ndarray:
        return self._root_lattice


class E8Transform:
    """Transform complex functions onto E8-aligned coordinates."""
    
    def __init__(self, e8: Optional['E8Structure'] = None):
        self.e8 = e8 or E8Structure()
        self._projection_matrix = self._compute_projection()
    
    def _compute_projection(self) -> np.ndarray:
        """Compute projection from 2D complex plane to 8D E8 space."""
        basis = self.e8.root_lattice[:8]
        norms = np.linalg.norm(basis, axis=1, keepdims=True)
        return basis / norms
    
    def complex_to_e8(self, z: complex) -> np.ndarray:
        """Map a complex number to 8D E8-aligned coordinates."""
        x, y = z.real, z.imag
        
        phase_factors = np.array([
            [1, 0], [0, 1], [-1, 0], [0, -1],
        ])
        
        coords = np.array([
            x * phase_factors[0, 0] + y * phase_factors[0, 1],
            x * phase_factors[0, 1] - y * phase_factors[0, 0],
            x * phase_factors[1, 0] + y * phase_factors[1, 1],
            x * phase_factors[1, 1] - y * phase_factors[1, 0],
            x * phase_factors[2, 0] + y * phase_factors[2, 1],
            x * phase_factors[2, 1] - y * phase_factors[2, 0],
            x * phase_factors[3, 0] + y * phase_factors[3, 1],
            x * phase_factors[3, 1] - y * phase_factors[3, 0],
        ])
        
        return np.dot(coords, self._projection_matrix)
    
    def e8_to_complex(self, v: np.ndarray) -> complex:
        """Approximate inverse: map 8D E8 vector back to complex plane."""
        inv_proj = np.linalg.pinv(self._projection_matrix)
        coords = np.dot(v, inv_proj.T)
        return complex(coords[0], coords[1])
    
    def align_function(
        self, 
        f: Callable[[complex], complex], 
        domain: List[complex],
    ) -> np.ndarray:
        """Transform a complex function's output onto E8-aligned coordinates."""
        results = []
        for z in domain:
            results.append(self.complex_to_e8(f(z)))
        return np.array(results)
    
    def compute_symmetry_score(self, values: np.ndarray) -> float:
        """Measure how symmetric a set of E8-aligned values is."""
        if len(values) < 2:
            return 0.0
        centered = values - np.mean(values, axis=0)
        cov = np.cov(centered.T)
        eigenvalues = np.linalg.eigvalsh(cov)
        if eigenvalues[-1] == 0:
            return 0.0
        return float(np.min(eigenvalues) / np.max(eigenvalues))


if __name__ == "__main__":
    print("E8 Structure Test")
    e8 = E8Structure()
    print(f"  Rank: {e8.RANK}")
    print(f"  Dimension: {e8.DIMENSION}")
    print(f"  Root count: {len(e8.root_lattice)}")
    
    print("\nE8 Transform Test")
    transform = E8Transform(e8)
    z = 1 + 2j
    e8_coords = transform.complex_to_e8(z)
    print(f"  Input: {z}")
    print(f"  E8 coords shape: {e8_coords.shape}")
    
    z_back = transform.e8_to_complex(e8_coords)
    print(f"  Recovered: {z_back}")
