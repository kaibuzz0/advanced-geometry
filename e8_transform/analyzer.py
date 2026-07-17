"""
Symmetry Analyzer for E8-aligned transforms.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class SymmetryReport:
    """Report of symmetry analysis on E8-transformed data."""
    num_points: int
    dimension: int
    isotropy_score: float
    lattice_alignment: float
    weyl_invariance: float
    dominant_symmetry: str
    symmetry_multiplicity: int
    eigenvalues: np.ndarray
    centroid: np.ndarray
    invariants: Dict[str, float]


class SymmetryAnalyzer:
    """Analyze E8-transformed functions for hidden symmetries."""
    
    def __init__(self, e8_structure=None):
        from .core import E8Structure
        self.e8 = e8_structure or E8Structure()
        self._weyl_samples = 100
    
    def analyze(self, e8_points: np.ndarray) -> SymmetryReport:
        """Perform comprehensive symmetry analysis on E8-transformed points."""
        if e8_points.ndim == 1:
            e8_points = e8_points.reshape(1, -1)
        
        n_points, dim = e8_points.shape
        centroid = np.mean(e8_points, axis=0)
        centered = e8_points - centroid
        
        if n_points > 1:
            cov = np.cov(centered.T)
            eigenvalues, eigenvectors = np.linalg.eigh(cov)
        else:
            eigenvalues = np.ones(dim)
            eigenvectors = np.eye(dim)
        
        ev_normalized = eigenvalues / (np.sum(eigenvalues) + 1e-10)
        isotropy = 1 - np.std(ev_normalized)
        
        lattice_align = self._compute_lattice_alignment(e8_points)
        weyl_inv = self._compute_weyl_invariance(e8_points)
        
        dominant_sym, multiplicity = self._classify_symmetry(
            isotropy, lattice_align, weyl_inv, eigenvalues
        )
        
        invariants = self._compute_invariants(e8_points)
        
        return SymmetryReport(
            num_points=n_points,
            dimension=dim,
            isotropy_score=isotropy,
            lattice_alignment=lattice_align,
            weyl_invariance=weyl_inv,
            dominant_symmetry=dominant_sym,
            symmetry_multiplicity=multiplicity,
            eigenvalues=eigenvalues,
            centroid=centroid,
            invariants=invariants,
        )
    
    def _compute_lattice_alignment(self, points: np.ndarray) -> float:
        """Measure how well points align to the E8 root lattice."""
        if len(points) == 0:
            return 0.0
        
        roots = self.e8.root_lattice
        total_alignment = 0.0
        
        for point in points:
            distances = np.linalg.norm(roots - point, axis=1)
            min_dist = np.min(distances)
            alignment = np.exp(-min_dist / 2.0)
            total_alignment += alignment
        
        return total_alignment / len(points)
    
    def _compute_weyl_invariance(self, points: np.ndarray) -> float:
        """Test invariance under Weyl group reflections."""
        if len(points) == 0:
            return 0.0
        
        sample_size = min(self._weyl_samples, len(points))
        indices = np.random.choice(len(points), sample_size, replace=False)
        
        invariance_scores = []
        
        for simple_root_idx in range(min(4, len(self.e8.simple_roots))):
            reflector = self.e8.simple_roots[simple_root_idx]
            
            for idx in indices:
                point = points[idx]
                dot = np.dot(point, reflector)
                norm_sq = np.dot(reflector, reflector)
                reflected = point - 2 * dot / norm_sq * reflector
                
                distances = np.linalg.norm(points - reflected, axis=1)
                if np.min(distances) < 0.1:
                    invariance_scores.append(1.0)
                else:
                    invariance_scores.append(0.0)
        
        return float(np.mean(invariance_scores)) if invariance_scores else 0.0
    
    def _classify_symmetry(self, isotropy, lattice_align, weyl_inv, eigenvalues) -> Tuple[str, int]:
        """Classify the dominant symmetry type."""
        scores = {
            "E8": weyl_inv * lattice_align,
            "A7": isotropy * (1 - weyl_inv) * 0.8,
            "D8": isotropy * (1 - weyl_inv) * 0.6,
            "SO(8)": isotropy * 0.5,
            "Trivial": 0.1,
        }
        
        dominant = max(scores, key=scores.get)
        multiplicity = sum(1 for v in scores.values() if v > 0.3)
        
        return dominant, multiplicity
    
    def _compute_invariants(self, points: np.ndarray) -> Dict[str, float]:
        """Compute algebraic invariants of the point set."""
        invariants = {}
        centroid = np.mean(points, axis=0)
        centered = points - centroid
        
        invariants["trace_moment"] = np.trace(np.cov(centered.T)) if len(points) > 1 else 0.0
        
        radii = np.linalg.norm(centered, axis=1)
        invariants["mean_radius"] = np.mean(radii)
        invariants["radius_variance"] = np.var(radii)
        
        return invariants


if __name__ == "__main__":
    from .core import E8Transform
    
    print("Symmetry Analyzer Test")
    analyzer = SymmetryAnalyzer()
    transform = E8Transform()
    
    domain = [complex(x, y) for x in np.linspace(-1, 1, 5) for y in np.linspace(-1, 1, 5)]
    pts = transform.align_function(lambda z: z**2 + 1, domain)
    
    report = analyzer.analyze(pts)
    print(f"  Isotropy: {report.isotropy_score:.4f}")
    print(f"  Dominant: {report.dominant_symmetry}")
