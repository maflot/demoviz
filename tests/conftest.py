"""Pytest configuration and fixtures."""

import pytest
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from pathlib import Path
import tempfile

@pytest.fixture
def clean_matplotlib():
    """Clean matplotlib state before/after tests."""
    plt.close('all')
    plt.clf()
    plt.cla()
    yield
    plt.close('all')
    plt.clf()
    plt.cla()

@pytest.fixture
def sample_data():
    """Sample demographic data for testing."""
    np.random.seed(42)
    n = 20
    return {
        'x': np.random.uniform(20, 80, n),  # ages
        'y': np.random.uniform(0, 6, n),    # scores  
        'sex': np.random.choice(['M', 'F'], n),
        'colors': np.random.uniform(0, 1, n),
        'categories': np.random.choice(['A', 'B', 'C'], n)
    }

@pytest.fixture
def sample_dataframe(sample_data):
    """Sample DataFrame for testing."""
    return pd.DataFrame(sample_data)

@pytest.fixture
def test_icon_dir():
    """Create temporary directory with test SVG icons."""
    with tempfile.TemporaryDirectory() as tmpdir:
        icon_dir = Path(tmpdir)
        
        # Create simple test SVGs
        male_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="30" r="15" fill="black"/>
    <rect x="40" y="45" width="20" height="40" fill="black"/>
</svg>'''
        
        female_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="30" r="15" fill="black"/>
    <polygon points="40,45 60,45 70,85 30,85" fill="black"/>
</svg>'''
        
        # Write SVG files
        (icon_dir / 'test_male.svg').write_text(male_svg)
        (icon_dir / 'test_female.svg').write_text(female_svg)
        (icon_dir / 'Person_icon_BLACK-01.svg').write_text(male_svg)
        (icon_dir / 'Woman_(958542)_-_The_Noun_Project.svg').write_text(female_svg)
        
        yield {
            'male': icon_dir / 'test_male.svg',
            'female': icon_dir / 'test_female.svg',
            'person': icon_dir / 'Person_icon_BLACK-01.svg'
        }

@pytest.fixture
def custom_icons(test_icon_dir):
    """Custom icon paths for testing."""
    return test_icon_dir