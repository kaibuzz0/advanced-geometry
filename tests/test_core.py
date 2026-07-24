"""
Tests for E8 core mathematical structures.
"""

import numpy as np
import pytest
from e8_transform.core import E8Structure, E8Transform


class TestE8Structure:
    """Tests for the E8 Lie group structure."""
    
    def test_basic_properties(self):
        """Test that E8 has the correct mathematical properties."""
        e8 = E8Structure()
        assert e8.RANK == 8
        assert e8.DIMENSION == 248
        assert e8.WEYL_ORDER == 696729600
        assert e8.ROOT_COUNT == 240
        assert e8.COXETER_NUMBER == 30
    
    def test_simple_roots_shape(self):
        """Test that simple roots have correct shape."""
        e8 = E8Structure()
        assert e8.simple_roots.shape == (8, 8)
    
    def test_root_lattice_count(self):
        """Test that root lattice has exactly 240 roots."""
        e8 = E8Structure()
        assert len(e8.root_lattice) == 240
    
    def test_root_lattice_unique(self):
        """Test that all roots are unique."""
        e8 = E8Structure()
        unique_roots = np.unique(e8.root_lattice, axis=0)
        assert len(unique_roots) == 240
    
    def test_roots_have_norm_squared_2(self):
        """Test that all roots have norm squared = 2."""
        e8 = E8Structure()
        for root in e8.root_lattice:
            norm_sq = np.dot(root, root)
            assert abs(norm_sq - 2.0) < 1e-10
    
    def test_verification_report(self):
        """Test that verification produces correct report."""
        e8 = E8Structure()
        report = e8.verify_roots()
        assert report["total_roots"] == 240
        assert report["expected_roots"] == 240
        assert report["unique_roots"] == 240
        assert report["all_norms_equal_2"] is True


class TestE8Transform:
    """Tests for the E8 transformation engine."""
    
    def test_transform_initialization(self):
        """Test that transform initializes correctly."""
        transform = E8Transform()
        assert transform.e8 is not None
    
    def test_complex_to_e8_shape(self):
        """Test that complex number maps to 8D vector."""
        transform = E8Transform()
        z = 1 + 2j
        result = transform.complex_to_e8(z)
        assert result.shape == (8,)
    
    def test_complex_to_e8_type(self):
        """Test that output is numpy array."""
        transform = E8Transform()
        z = 1 + 2j
        result = transform.complex_to_e8(z)
        assert isinstance(result, np.ndarray)
    
    def test_roundtrip_approximation(self):
        """Test that round-trip approximately recovers original value."""
        transform = E8Transform()
        z = 1 + 2j
        e8_coords = transform.complex_to_e8(z)
        z_back = transform.e8_to_complex(e8_coords)
        assert abs(z - z_back) < 1.0
    
    def test_align_function(self):
        """Test aligning a function over a domain."""
        transform = E8Transform()
        domain = [complex(x, y) for x in range(-2, 3) for y in range(-2, 3)]
        result = transform.align_function(lambda z: z**2, domain)
        assert result.shape == (25, 8)
    
    def test_align_function_empty_domain(self):
        """Test align with empty domain."""
        transform = E8Transform()
        result = transform.align_function(lambda z: z**2, [])
        assert result.shape == (0, 8)


class TestE8EdgeCases:
    """Edge case tests."""
    
    def test_zero_complex(self):
        """Test mapping zero complex number."""
        transform = E8Transform()
        result = transform.complex_to_e8(0j)
        assert result.shape == (8,)
        assert not np.any(np.isnan(result))
    
    def test_large_complex(self):
        """Test mapping large complex number."""
        transform = E8Transform()
        z = 1e6 + 1e6j
        result = transform.complex_to_e8(z)
        assert result.shape == (8,)
        assert not np.any(np.isnan(result))
