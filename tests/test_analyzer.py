"""
Tests for SymmetryAnalyzer.
"""

import numpy as np
from e8_transform.core import E8Transform
from e8_transform.analyzer import SymmetryAnalyzer, SymmetryReport


class TestSymmetryAnalyzer:
    """Tests for symmetry analysis functionality."""
    
    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly."""
        analyzer = SymmetryAnalyzer()
        assert analyzer.e8 is not None
    
    def test_analyze_returns_report(self):
        """Test that analyze returns a SymmetryReport."""
        analyzer = SymmetryAnalyzer()
        transform = E8Transform()
        
        domain = [complex(x, y) for x in np.linspace(-1, 1, 5) 
                  for y in np.linspace(-1, 1, 5)]
        points = transform.align_function(lambda z: z**2, domain)
        
        report = analyzer.analyze(points)
        assert isinstance(report, SymmetryReport)
    
    def test_report_attributes(self):
        """Test that report has all expected attributes."""
        analyzer = SymmetryAnalyzer()
        transform = E8Transform()
        
        domain = [complex(x, y) for x in np.linspace(-1, 1, 3) 
                  for y in np.linspace(-1, 1, 3)]
        points = transform.align_function(lambda z: z, domain)
        
        report = analyzer.analyze(points)
        
        assert hasattr(report, 'num_points')
        assert hasattr(report, 'dimension')
        assert hasattr(report, 'isotropy_score')
        assert hasattr(report, 'lattice_alignment')
        assert hasattr(report, 'weyl_invariance')
        assert hasattr(report, 'dominant_symmetry')
    
    def test_scores_in_valid_range(self):
        """Test that all scores are in [0, 1] range."""
        analyzer = SymmetryAnalyzer()
        transform = E8Transform()
        
        domain = [complex(x, y) for x in np.linspace(-1, 1, 5) 
                  for y in np.linspace(-1, 1, 5)]
        points = transform.align_function(lambda z: z**2, domain)
        
        report = analyzer.analyze(points)
        
        assert 0.0 <= report.isotropy_score <= 1.0
        assert 0.0 <= report.lattice_alignment <= 1.0
        assert 0.0 <= report.weyl_invariance <= 1.0
