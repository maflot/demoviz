"""Tests for demoviz.core module."""

import pytest
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from unittest.mock import patch, MagicMock

import demoviz
from demoviz.core import DemoScatter, svg_to_colored_image


class TestSvgToColoredImage:
    """Test SVG processing functionality."""
    
    def test_svg_to_colored_image_no_cairosvg(self):
        """Test that ImportError is raised when cairosvg is not available."""
        with patch('demoviz.core.HAS_CAIROSVG', False):
            with pytest.raises(ImportError, match="cairosvg is required"):
                svg_to_colored_image("dummy.svg", (1, 0, 0, 1))
    
    @pytest.mark.skipif(not hasattr(demoviz.core, 'cairosvg'), 
                       reason="cairosvg not available")
    def test_svg_to_colored_image_success(self, custom_icons):
        """Test successful SVG to image conversion."""
        color = (1.0, 0.0, 0.0, 1.0)  # Red
        result = svg_to_colored_image(custom_icons['male'], color, size=(50, 50))
        
        assert isinstance(result, Image.Image)
        assert result.size == (50, 50)
        assert result.mode == 'RGBA'


class TestDemoScatter:
    """Test DemoScatter class."""
    
    def test_init_default(self):
        """Test DemoScatter initialization with defaults."""
        scatter = DemoScatter()
        
        assert scatter.icon_size == 40
        assert scatter.zoom == 0.3
        assert scatter.icon_cache == {}
        assert isinstance(scatter.icon_paths, dict)
    
    def test_init_custom_params(self, custom_icons):
        """Test DemoScatter initialization with custom parameters."""
        scatter = DemoScatter(icon_size=60, zoom=0.5, custom_icons=custom_icons)
        
        assert scatter.icon_size == 60
        assert scatter.zoom == 0.5
        assert scatter.icon_paths == custom_icons
    
    def test_normalize_icon_type(self):
        """Test icon type normalization."""
        scatter = DemoScatter()
        
        # Test various inputs
        assert scatter._normalize_icon_type('M') == 'male'
        assert scatter._normalize_icon_type('F') == 'female'
        assert scatter._normalize_icon_type(1) == 'male'
        assert scatter._normalize_icon_type(0) == 'female'
        assert scatter._normalize_icon_type('male') == 'male'
        assert scatter._normalize_icon_type('FEMALE') == 'female'
        assert scatter._normalize_icon_type('custom') == 'custom'
    
    def test_create_fallback_icon(self):
        """Test fallback icon creation."""
        scatter = DemoScatter()
        color = (1.0, 0.0, 0.0, 0.8)
        size = 50
        
        icon = scatter._create_fallback_icon(color, size)
        
        assert isinstance(icon, Image.Image)
        assert icon.size == (size, size)
        assert icon.mode == 'RGBA'
    
    def test_get_icon_image_fallback(self):
        """Test getting icon image with fallback."""
        scatter = DemoScatter(custom_icons={})  # No icons available
        color = (0.0, 1.0, 0.0, 1.0)
        
        icon = scatter._get_icon_image('male', color)
        
        assert isinstance(icon, Image.Image)
        assert icon.size == (scatter.icon_size, scatter.icon_size)
    
    def test_get_icon_image_caching(self):
        """Test that icon images are cached properly."""
        scatter = DemoScatter(custom_icons={})
        color = (0.0, 0.0, 1.0, 1.0)
        
        # First call
        icon1 = scatter._get_icon_image('male', color)
        cache_size_1 = len(scatter.icon_cache)
        
        # Second call with same parameters
        icon2 = scatter._get_icon_image('male', color)
        cache_size_2 = len(scatter.icon_cache)
        
        # Cache should not grow
        assert cache_size_1 == cache_size_2
        # Should be same object (from cache)
        assert icon1 is icon2
    
    def test_plot_basic(self, clean_matplotlib, sample_data):
        """Test basic plotting functionality."""
        scatter = DemoScatter()
        fig, ax = plt.subplots()
        
        x = sample_data['x'][:5]
        y = sample_data['y'][:5] 
        sex = sample_data['sex'][:5]
        
        result_ax = scatter.plot(ax, x, y, icon_type=sex)
        
        assert result_ax is ax
        # Check that artists were added
        assert len(ax.artists) == len(x)
    
    def test_plot_with_colors(self, clean_matplotlib, sample_data):
        """Test plotting with color array."""
        scatter = DemoScatter()
        fig, ax = plt.subplots()
        
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        colors = ['red', 'green', 'blue']
        
        scatter.plot(ax, x, y, colors=colors)
        
        assert len(ax.artists) == len(x)
    
    def test_plot_with_jitter(self, clean_matplotlib, sample_data):
        """Test plotting with position jitter."""
        scatter = DemoScatter()
        fig, ax = plt.subplots()
        
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        scatter.plot(ax, x, y, jitter=1.0)
        
        assert len(ax.artists) == len(x)
    
    def test_plot_single_values(self, clean_matplotlib):
        """Test plotting with single x, y values."""
        scatter = DemoScatter()
        fig, ax = plt.subplots()
        
        scatter.plot(ax, [50], [3], icon_type='male', colors='red')
        
        assert len(ax.artists) == 1
    
    def test_plot_no_icon_type(self, clean_matplotlib, sample_data):
        """Test plotting without specifying icon type."""
        scatter = DemoScatter()
        fig, ax = plt.subplots()
        
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        scatter.plot(ax, x, y)  # No icon_type specified
        
        assert len(ax.artists) == len(x)
    
    def test_clear_cache(self):
        """Test cache clearing functionality."""
        scatter = DemoScatter()
        
        # Add something to cache
        scatter._get_icon_image('male', (1, 0, 0, 1))
        assert len(scatter.icon_cache) > 0
        
        # Clear cache
        scatter.clear_cache()
        assert len(scatter.icon_cache) == 0
    
    def test_list_available_icons(self, custom_icons):
        """Test listing available icons."""
        scatter = DemoScatter(custom_icons=custom_icons)
        
        available = scatter.list_available_icons()
        
        assert 'male' in available
        assert 'female' in available
        assert isinstance(available, list)
    
    def test_color_format_handling(self, clean_matplotlib):
        """Test different color format inputs."""
        scatter = DemoScatter()
        fig, ax = plt.subplots()
        
        # Test different color formats
        test_cases = [
            'red',                    # Named color
            '#FF0000',               # Hex color
            (1.0, 0.0, 0.0),        # RGB tuple
            (1.0, 0.0, 0.0, 0.5),   # RGBA tuple
        ]
        
        for i, color in enumerate(test_cases):
            ax.clear()
            scatter.plot(ax, [i], [i], colors=color)
            assert len(ax.artists) == 1
    
    def test_array_input_validation(self, clean_matplotlib):
        """Test that function handles array inputs correctly."""
        scatter = DemoScatter()
        fig, ax = plt.subplots()
        
        # Test with numpy arrays
        x = np.array([1, 2, 3])
        y = np.array([1, 2, 3])
        sex = np.array(['M', 'F', 'M'])
        colors = np.array(['red', 'green', 'blue'])
        
        scatter.plot(ax, x, y, icon_type=sex, colors=colors)
        
        assert len(ax.artists) == 3


class TestModuleImports:
    """Test module-level imports and exports."""
    
    def test_main_imports(self):
        """Test that main functions are importable."""
        from demoviz import DemoScatter, scatter, scatterplot, svg_to_colored_image
        
        assert callable(DemoScatter)
        assert callable(scatter)
        assert callable(scatterplot)
        assert callable(svg_to_colored_image)
    
    def test_version_exists(self):
        """Test that version is defined."""
        assert hasattr(demoviz, '__version__')
        assert isinstance(demoviz.__version__, str)
    
    def test_all_exports(self):
        """Test __all__ exports."""
        assert hasattr(demoviz, '__all__')
        
        for name in demoviz.__all__:
            assert hasattr(demoviz, name)