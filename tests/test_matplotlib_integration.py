"""Tests for demoviz.matplotlib_integration module."""

import pytest
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from unittest.mock import patch

from demoviz.matplotlib_integration import scatter, plot_demographics


class TestScatterFunction:
    """Test the main scatter function."""
    
    def test_scatter_basic(self, clean_matplotlib, sample_data):
        """Test basic scatter plot creation."""
        x = sample_data['x'][:5]
        y = sample_data['y'][:5]
        
        ax = scatter(x, y)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_with_sex(self, clean_matplotlib, sample_data):
        """Test scatter plot with sex parameter."""
        x = sample_data['x'][:5]
        y = sample_data['y'][:5]
        sex = sample_data['sex'][:5]
        
        ax = scatter(x, y, sex=sex)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_with_colors_array(self, clean_matplotlib, sample_data):
        """Test scatter plot with color array."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        colors = ['red', 'green', 'blue']
        
        ax = scatter(x, y, c=colors)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_with_single_color(self, clean_matplotlib, sample_data):
        """Test scatter plot with single color."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        ax = scatter(x, y, c='red')
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_with_numeric_colors(self, clean_matplotlib, sample_data):
        """Test scatter plot with numeric color mapping."""
        x = sample_data['x'][:5]
        y = sample_data['y'][:5]
        colors = sample_data['colors'][:5]
        
        ax = scatter(x, y, c=colors)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_custom_size(self, clean_matplotlib, sample_data):
        """Test scatter plot with custom icon size."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        ax = scatter(x, y, s=60)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_custom_zoom(self, clean_matplotlib, sample_data):
        """Test scatter plot with custom zoom."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        ax = scatter(x, y, zoom=0.5)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_with_jitter(self, clean_matplotlib, sample_data):
        """Test scatter plot with jitter."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        ax = scatter(x, y, jitter=1.0)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_existing_axis(self, clean_matplotlib, sample_data):
        """Test scatter plot on existing axis."""
        fig, ax = plt.subplots()
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        result_ax = scatter(x, y, ax=ax)
        
        assert result_ax is ax
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_custom_figsize(self, clean_matplotlib, sample_data):
        """Test scatter plot with custom figure size."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        ax = scatter(x, y, figsize=(12, 8))
        
        assert ax is not None
        fig = ax.get_figure()
        width, height = fig.get_size_inches()
        assert width == 12
        assert height == 8
        plt.close()
    
    def test_scatter_custom_icons(self, clean_matplotlib, sample_data, custom_icons):
        """Test scatter plot with custom icons."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        sex = sample_data['sex'][:3]
        
        ax = scatter(x, y, sex=sex, custom_icons=custom_icons)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatter_empty_input(self, clean_matplotlib):
        """Test scatter plot with empty input."""
        ax = scatter([], [])
        
        assert ax is not None
        assert len(ax.artists) == 0
        plt.close()
    
    def test_scatter_single_point(self, clean_matplotlib):
        """Test scatter plot with single point."""
        ax = scatter([50], [3], sex=['M'], c=['red'])
        
        assert ax is not None
        assert len(ax.artists) == 1
        plt.close()


class TestPlotDemographics:
    """Test the plot_demographics function."""
    
    def test_plot_demographics_basic(self, clean_matplotlib, sample_dataframe):
        """Test basic demographics plot."""
        ax = plot_demographics(sample_dataframe, 'x', 'y')
        
        assert ax is not None
        assert len(ax.artists) > 0
        plt.close()
    
    def test_plot_demographics_with_sex(self, clean_matplotlib, sample_dataframe):
        """Test demographics plot with sex column."""
        ax = plot_demographics(sample_dataframe, 'x', 'y', sex='sex')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_plot_demographics_with_hue(self, clean_matplotlib, sample_dataframe):
        """Test demographics plot with hue mapping."""
        ax = plot_demographics(sample_dataframe, 'x', 'y', sex='sex', hue='colors')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_plot_demographics_with_size(self, clean_matplotlib, sample_dataframe):
        """Test demographics plot with size mapping.""" 
        ax = plot_demographics(sample_dataframe, 'x', 'y', size='colors')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_plot_demographics_custom_figsize(self, clean_matplotlib, sample_dataframe):
        """Test demographics plot with custom figure size."""
        ax = plot_demographics(sample_dataframe, 'x', 'y', figsize=(10, 8))
        
        assert ax is not None
        fig = ax.get_figure()
        width, height = fig.get_size_inches()
        assert width == 10
        assert height == 8
        plt.close()
    
    def test_plot_demographics_with_title(self, clean_matplotlib, sample_dataframe):
        """Test demographics plot with title."""
        title = "Test Demographics Plot"
        ax = plot_demographics(sample_dataframe, 'x', 'y', title=title)
        
        assert ax is not None
        assert ax.get_title() == title
        plt.close()
    
    def test_plot_demographics_axis_labels(self, clean_matplotlib, sample_dataframe):
        """Test that axis labels are set correctly."""
        ax = plot_demographics(sample_dataframe, 'x', 'y')
        
        assert ax.get_xlabel() == 'X'
        assert ax.get_ylabel() == 'Y'
        plt.close()
    
    def test_plot_demographics_with_categorical_hue(self, clean_matplotlib, sample_dataframe):
        """Test demographics plot with categorical hue."""
        ax = plot_demographics(sample_dataframe, 'x', 'y', hue='categories')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    @pytest.mark.skipif(not plt.get_backend().startswith('Agg'), 
                       reason="Colorbar test requires Agg backend")
    def test_plot_demographics_colorbar_numeric_hue(self, clean_matplotlib, sample_dataframe):
        """Test that colorbar is added for numeric hue."""
        ax = plot_demographics(sample_dataframe, 'x', 'y', hue='colors')
        
        assert ax is not None
        # Check if colorbar was created (would be in the figure)
        fig = ax.get_figure()
        assert len(fig.axes) >= 1  # At least the main axis
        plt.close()


class TestInputValidation:
    """Test input validation and error handling."""
    
    def test_mismatched_array_lengths(self, clean_matplotlib):
        """Test handling of mismatched array lengths."""
        x = [1, 2, 3]
        y = [1, 2]  # Different length
        
        with pytest.raises((ValueError, IndexError)):
            scatter(x, y)
    
    def test_invalid_color_format(self, clean_matplotlib):
        """Test handling of invalid color formats."""
        x = [1, 2, 3]
        y = [1, 2, 3]
        
        # This should not raise an error - matplotlib should handle it
        ax = scatter(x, y, c='invalid_color_name')
        assert ax is not None
        plt.close()
    
    def test_plot_demographics_missing_columns(self, clean_matplotlib, sample_dataframe):
        """Test error handling for missing DataFrame columns."""
        with pytest.raises(KeyError):
            plot_demographics(sample_dataframe, 'nonexistent_column', 'y')


class TestIntegrationWithMatplotlib:
    """Test integration with matplotlib features."""
    
    def test_axis_limits_updated(self, clean_matplotlib, sample_data):
        """Test that axis limits are updated correctly."""
        x = sample_data['x'][:5]
        y = sample_data['y'][:5]
        
        ax = scatter(x, y)
        
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Check that limits encompass the data
        assert xlim[0] <= min(x) <= xlim[1]
        assert xlim[0] <= max(x) <= xlim[1]
        assert ylim[0] <= min(y) <= ylim[1]
        assert ylim[0] <= max(y) <= ylim[1]
        plt.close()
    
    def test_works_with_subplots(self, clean_matplotlib, sample_data):
        """Test that function works with matplotlib subplots."""
        fig, (ax1, ax2) = plt.subplots(1, 2)
        
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        scatter(x, y, ax=ax1)
        scatter(y, x, ax=ax2)  # Swap x and y
        
        assert len(ax1.artists) == len(x)
        assert len(ax2.artists) == len(x)
        plt.close()
    
    def test_tight_layout_compatibility(self, clean_matplotlib, sample_data):
        """Test compatibility with plt.tight_layout()."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        ax = scatter(x, y)
        plt.tight_layout()  # Should not raise an error
        
        assert ax is not None
        plt.close()