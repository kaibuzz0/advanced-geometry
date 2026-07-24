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
        """Compute the 8 simple roots of E8 using the Dynkin diagram structure."""
        roots = np.zeros((8, 8))
        # A7 subchain: e_i - e_{i+1} for i = 0,...,6
        for i in range(7):
            roots[i, i] = 1
            roots[i, i+1] = -1
        # Additional root connecting to the A7 chain: 1/2*(sum of first 6 with -, then +1/2, +1/2)
        roots[7] = np.array([-0.5] * 6 + [0.5, 0.5])
        return roots
    
    def _compute_root_lattice(self) -> np.ndarray:
        """
        Generate the 240 roots of E8 lattice.
        
        E8 roots come in two types:
        1. 112 roots: (±1, ±1, 0, 0, 0, 0, 0, 0) and permutations
        2. 128 roots: (±1/2, ±1/2, ..., ±1/2) with an even number of minus signs
        """
        roots = []
        from itertools import product, permutations
        
        # Type 1: 112 roots (±1, ±1, 0, 0, 0, 0, 0, 0)
        # All permutations of positions of the two non-zero entries
        for i in range(8):
            for j in range(i+1, 8):
                for s1 in [1, -1]:
                    for s2 in [1, -1]:
                        root = np.zeros(8)
                        root[i] = s1
                        root[j] = s2
                        roots.append(root)
        
        # Type 2: 128 roots (±1/2, ..., ±1/2) with EVEN number of minus signs
        for signs in product([1, -1], repeat=8):
            # Count minus signs - must be even
            if sum(1 for s in signs if s == -1) % 2 == 0:
                root = np.array(signs) * 0.5
                roots.append(root)
        
        result = np.array(roots)
        
        # Verification: should have exactly 240 unique roots
        assert len(result) == 240, f"Expected 240 roots, got {len(result)}"
        
        return result
    
    @property
    def simple_roots(self) -> np.ndarray:
        return self._simple_roots
    
    @property
    def root_lattice(self) -> np.ndarray:
        return self._root_lattice
    
    def verify_roots(self) -> dict:
        """Verify root system properties. Returns verification report."""
        roots = self.root_lattice
        report = {
            "total_roots": len(roots),
            "expected_roots": 240,
            "unique_roots": len(np.unique(roots, axis=0)),
            "norms": np.unique(np.round([np.dot(r, r) for r in roots], 6)),
        }
        # All E8 roots should have norm squared = 2
        norms = [np.dot(r, r) for r in roots]
        report["all_norms_equal_2"] = all(abs(n - 2.0) < 1e-10 for n in norms)
        return report


class E8Transform:
    """Transform complex functions onto E8-aligned coordinates."""
    
    def __init__(self, e8: Optional['E8Structure'] = None):
        self.e8 = e8 or E8Structure()
        self._projection_matrix = self._compute_projection()
    
    def _compute_projection(self) -> np.ndarray:
        """
        Compute projection from 2D complex plane to 8D E8 space.
        
        Uses the first 8 roots as a basis, orthonormalized via Gram-Schmidt.
        """
        basis = self.e8.root_lattice[:8].astype(float)
        
        # Gram-Schmidt orthonormalization
        ortho_basis = []
        for i, vec in enumerate(basis):
            w = vec.copy()
            for j in range(len(ortho_basis)):
                proj = np.dot(vec, ortho_basis[j]) * ortho_basis[j]
                w = w - proj
            norm = np.linalg.norm(w)
            if norm > 1e-10:
                ortho_basis.append(w / norm)
        
        return np.array(ortho_basis[:2]).T  # Project to 2 orthonormal directions
    
    def complex_to_e8(self, z: complex) -> np.ndarray:
        """
        Map a complex number to 8D E8-aligned coordinates.
        
        Uses a symplectic-inspired mapping preserving phase structure.
        """
        x, y = z.real, z.imag
        
        # Create 8D vector with complex structure embedded
        # Pattern: [x, y, -x, -y, x, y, -x, -y] creates natural symmetry
        base = np.array([x, y, -x, -y, x, y, -x, -y])
        
        # Apply orthogonal projection onto E8-aligned subspace
        projected = np.dot(base[:2], self._projection_matrix[:2, :].T)
        
        # Embed back into 8D with the projection structure
        coords = np.zeros(8)
        coords[:len(projected)] = projected
        
        return coords
    
    def e8_to_complex(self, v: np.ndarray) -> complex:
        """
        Approximate inverse: map 8D E8 vector back to complex plane.
        """
        # Project back to the 2D subspace
        proj_2d = np.dot(v[:2], self._projection_matrix[:2, :])
        return complex(proj_2d[0], proj_2d[1]) if len(proj_2d) > 1 else complex(proj_2d[0], 0)
    
    def align_function(
        self, 
        f: Callable[[complex], complex], 
        domain: List[complex],
    ) -> np.ndarray:
        """Transform a complex function's output onto E8-aligned coordinates."""
        results = []
        for z in domain:
            try:
                result = self.complex_to_e8(f(z))
                results.append(result)
            except (OverflowError, ValueError):
                # Skip points that cause numerical issues
                continue
        return np.array(results) if results else np.zeros((0, 8))
    
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
    
    # Verify roots
    verification = e8.verify_roots()
    print(f"\nVerification:")
    for key, val in verification.items():
        print(f"  {key}: {val}")
    
    print("\nE8 Transform Test")
    transform = E8Transform(e8)
    z = 1 + 2j
    e8_coords = transform.complex_to_e8(z)
    print(f"  Input: {z}")
    print(f"  E8 coords shape: {e8_coords.shape}")
    print(f"  E8 coords: {e8_coords}")
    
    z_back = transform.e8_to_complex(e8_coords)
    print(f"  Recovered: {z_back}")
    print(f"  Round-trip error: {abs(z - z_back)}")
