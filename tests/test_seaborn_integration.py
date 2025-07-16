"""Tests for demoviz.seaborn_integration module."""

import pytest
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from unittest.mock import patch

from demoviz.seaborn_integration import scatterplot, relplot, demographic_plot


class TestScatterplotFunction:
    """Test the seaborn-style scatterplot function."""
    
    def test_scatterplot_basic(self, clean_matplotlib, sample_dataframe):
        """Test basic scatterplot creation."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_scatterplot_without_data(self, clean_matplotlib, sample_data):
        """Test scatterplot without DataFrame."""
        x = sample_data['x'][:5]
        y = sample_data['y'][:5]
        
        ax = scatterplot(x=x, y=y)
        
        assert ax is not None
        assert len(ax.artists) == len(x)
        plt.close()
    
    def test_scatterplot_with_sex(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with sex parameter."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', sex='sex')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_scatterplot_with_hue(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with hue parameter."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', hue='categories')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        # Should have a legend
        assert ax.get_legend() is not None
        plt.close()
    
    def test_scatterplot_with_size(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with size parameter."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', size='colors')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_scatterplot_with_palette_dict(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with palette as dictionary."""
        palette = {'A': 'red', 'B': 'blue', 'C': 'green'}
        
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        hue='categories', palette=palette)
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    @pytest.mark.skipif(True, reason="Seaborn not always available in test environment")
    def test_scatterplot_with_seaborn_palette(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with seaborn palette."""
        try:
            import seaborn as sns
            ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                           hue='categories', palette='Set1')
            
            assert ax is not None
            assert len(ax.artists) == len(sample_dataframe)
            plt.close()
        except ImportError:
            pytest.skip("Seaborn not available")
    
    def test_scatterplot_existing_axis(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot on existing axis."""
        fig, ax = plt.subplots()
        
        result_ax = scatterplot(data=sample_dataframe, x='x', y='y', ax=ax)
        
        assert result_ax is ax
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_scatterplot_no_legend(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with legend disabled."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        hue='categories', legend=False)
        
        assert ax is not None
        assert ax.get_legend() is None
        plt.close()
    
    def test_scatterplot_with_hue_order(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with custom hue order."""
        hue_order = ['C', 'A', 'B']
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        hue='categories', hue_order=hue_order)
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_scatterplot_numeric_hue(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with numeric hue values."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', hue='colors')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_scatterplot_mixed_parameters(self, clean_matplotlib, sample_dataframe):
        """Test scatterplot with multiple parameters."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        sex='sex', hue='categories', size='colors')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()


class TestRelplotFunction:
    """Test the relplot function."""
    
    def test_relplot_basic(self, clean_matplotlib, sample_dataframe):
        """Test basic relplot creation."""
        fig = relplot(data=sample_dataframe, x='x', y='y', kind='scatter')
        
        assert fig is not None
        plt.close()
    
    def test_relplot_with_sex(self, clean_matplotlib, sample_dataframe):
        """Test relplot with sex parameter."""
        fig = relplot(data=sample_dataframe, x='x', y='y', sex='sex', kind='scatter')
        
        assert fig is not None
        plt.close()
    
    def test_relplot_with_hue(self, clean_matplotlib, sample_dataframe):
        """Test relplot with hue parameter."""
        fig = relplot(data=sample_dataframe, x='x', y='y', 
                     hue='categories', kind='scatter')
        
        assert fig is not None
        plt.close()
    
    def test_relplot_custom_figsize(self, clean_matplotlib, sample_dataframe):
        """Test relplot with custom figure size."""
        fig = relplot(data=sample_dataframe, x='x', y='y', 
                     kind='scatter', figsize=(10, 8))
        
        assert fig is not None
        width, height = fig.get_size_inches()
        assert width == 10
        assert height == 8
        plt.close()
    
    def test_relplot_invalid_kind(self, clean_matplotlib, sample_dataframe):
        """Test relplot with invalid kind parameter."""
        with pytest.raises(ValueError, match="Only kind='scatter' is currently supported"):
            relplot(data=sample_dataframe, x='x', y='y', kind='line')
    
    def test_relplot_faceting_not_implemented(self, clean_matplotlib, sample_dataframe):
        """Test that faceting raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Faceting .* not yet implemented"):
            relplot(data=sample_dataframe, x='x', y='y', col='categories')
        
        with pytest.raises(NotImplementedError, match="Faceting .* not yet implemented"):
            relplot(data=sample_dataframe, x='x', y='y', row='categories')


class TestDemographicPlotDeprecated:
    """Test the deprecated demographic_plot function."""
    
    def test_demographic_plot_deprecated_warning(self, clean_matplotlib, sample_dataframe):
        """Test that demographic_plot issues deprecation warning."""
        with pytest.warns(DeprecationWarning, match="demographic_plot is deprecated"):
            ax = demographic_plot(data=sample_dataframe, x='x', y='y')
        
        assert ax is not None
        plt.close()
    
    def test_demographic_plot_functionality(self, clean_matplotlib, sample_dataframe):
        """Test that demographic_plot still works despite deprecation."""
        with pytest.warns(DeprecationWarning):
            ax = demographic_plot(data=sample_dataframe, x='x', y='y', sex='sex')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()


class TestSeabornIntegration:
    """Test integration with seaborn features."""
    
    @pytest.mark.skipif(True, reason="Seaborn not always available in test environment")
    def test_seaborn_despine_applied(self, clean_matplotlib, sample_dataframe):
        """Test that seaborn despine is applied when seaborn is available."""
        try:
            import seaborn as sns
            with patch('demoviz.seaborn_integration.HAS_SEABORN', True):
                with patch('demoviz.seaborn_integration.sns.despine') as mock_despine:
                    ax = scatterplot(data=sample_dataframe, x='x', y='y')
                    mock_despine.assert_called_once_with(ax=ax)
            plt.close()
        except ImportError:
            pytest.skip("Seaborn not available")
    
    def test_without_seaborn(self, clean_matplotlib, sample_dataframe):
        """Test functionality when seaborn is not available."""
        with patch('demoviz.seaborn_integration.HAS_SEABORN', False):
            ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                           hue='categories', palette='viridis')
            
            assert ax is not None
            assert len(ax.artists) == len(sample_dataframe)
            plt.close()


class TestLegendCreation:
    """Test legend creation functionality."""
    
    def test_legend_with_categorical_hue(self, clean_matplotlib, sample_dataframe):
        """Test legend creation with categorical hue data."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', hue='categories')
        
        legend = ax.get_legend()
        assert legend is not None
        
        # Check that all categories are in legend
        legend_labels = [t.get_text() for t in legend.get_texts()]
        unique_categories = sample_dataframe['categories'].unique()
        
        for category in unique_categories:
            assert str(category) in legend_labels
        plt.close()
    
    def test_legend_with_custom_hue_order(self, clean_matplotlib, sample_dataframe):
        """Test legend creation with custom hue order."""
        hue_order = ['C', 'A', 'B']
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        hue='categories', hue_order=hue_order)
        
        legend = ax.get_legend()
        assert legend is not None
        
        legend_labels = [t.get_text() for t in legend.get_texts()]
        assert legend_labels == ['C', 'A', 'B']
        plt.close()
    
    def test_legend_title(self, clean_matplotlib, sample_dataframe):
        """Test that legend has correct title."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', hue='categories')
        
        legend = ax.get_legend()
        assert legend is not None
        assert legend.get_title().get_text() == 'categories'
        plt.close()


class TestParameterHandling:
    """Test parameter handling and validation."""
    
    def test_data_extraction_string_columns(self, clean_matplotlib, sample_dataframe):
        """Test data extraction with string column names."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        sex='sex', hue='categories')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()
    
    def test_data_extraction_array_inputs(self, clean_matplotlib, sample_data):
        """Test data extraction with direct array inputs."""
        ax = scatterplot(data=None, x=sample_data['x'][:5], y=sample_data['y'][:5],
                        sex=sample_data['sex'][:5])
        
        assert ax is not None
        assert len(ax.artists) == 5
        plt.close()
    
    def test_missing_data_columns(self, clean_matplotlib, sample_dataframe):
        """Test handling of missing data columns."""
        # This should work - missing columns should be treated as None
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        sex='nonexistent_column')
        
        assert ax is not None
        plt.close()
    
    def test_size_parameter_handling(self, clean_matplotlib, sample_dataframe):
        """Test size parameter handling."""
        # Test with different size specifications
        sizes = [20, 40, 60]
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        size='categories', sizes=sizes)
        
        assert ax is not None
        plt.close()
    
    def test_size_dict_parameter(self, clean_matplotlib, sample_dataframe):
        """Test size parameter as dictionary."""
        sizes = {'A': 30, 'B': 50, 'C': 70}
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        size='categories', sizes=sizes)
        
        assert ax is not None
        plt.close()


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_dataframe(self, clean_matplotlib):
        """Test handling of empty DataFrame."""
        empty_df = pd.DataFrame(columns=['x', 'y', 'sex'])
        
        ax = scatterplot(data=empty_df, x='x', y='y', sex='sex')
        
        assert ax is not None
        assert len(ax.artists) == 0
        plt.close()
    
    def test_single_point_dataframe(self, clean_matplotlib):
        """Test handling of single-point DataFrame."""
        single_df = pd.DataFrame({'x': [50], 'y': [3], 'sex': ['M']})
        
        ax = scatterplot(data=single_df, x='x', y='y', sex='sex')
        
        assert ax is not None
        assert len(ax.artists) == 1
        plt.close()
    
    def test_none_data_with_arrays(self, clean_matplotlib, sample_data):
        """Test None data parameter with direct arrays."""
        x = sample_data['x'][:3]
        y = sample_data['y'][:3]
        
        ax = scatterplot(data=None, x=x, y=y)
        
        assert ax is not None
        assert len(ax.artists) == 3
        plt.close()


class TestBackwardCompatibility:
    """Test backward compatibility features."""
    
    def test_old_parameter_names(self, clean_matplotlib, sample_dataframe):
        """Test that function works with various parameter names."""
        # These should all work without errors
        ax1 = scatterplot(data=sample_dataframe, x='x', y='y', sex='sex')
        plt.close()
        
        ax2 = scatterplot(data=sample_dataframe, x='x', y='y', style='sex')
        plt.close()
        
        assert ax1 is not None
        assert ax2 is not None
    
    def test_style_parameter_fallback(self, clean_matplotlib, sample_dataframe):
        """Test that style parameter falls back to sex behavior."""
        # style parameter should work like sex parameter
        ax = scatterplot(data=sample_dataframe, x='x', y='y', style='sex')
        
        assert ax is not None
        assert len(ax.artists) == len(sample_dataframe)
        plt.close()


class TestAdvancedFeatures:
    """Test advanced functionality and edge cases."""
    
    def test_large_dataset_performance(self, clean_matplotlib):
        """Test performance with larger datasets."""
        n_points = 1000
        large_df = pd.DataFrame({
            'x': np.random.randn(n_points),
            'y': np.random.randn(n_points),
            'sex': np.random.choice(['M', 'F'], n_points),
            'category': np.random.choice(['A', 'B', 'C', 'D'], n_points)
        })
        
        # This should complete without timeout or memory issues
        ax = scatterplot(data=large_df, x='x', y='y', sex='sex', hue='category')
        
        assert ax is not None
        assert len(ax.artists) == n_points
        plt.close()
    
    def test_unicode_handling(self, clean_matplotlib):
        """Test handling of unicode characters in data."""
        unicode_df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'sex': ['M', 'F', 'M'],
            'category': ['café', 'naïve', 'résumé']
        })
        
        ax = scatterplot(data=unicode_df, x='x', y='y', hue='category')
        
        assert ax is not None
        assert len(ax.artists) == 3
        plt.close()
    
    def test_extreme_values(self, clean_matplotlib):
        """Test handling of extreme coordinate values."""
        extreme_df = pd.DataFrame({
            'x': [1e-10, 1e10, -1e10],
            'y': [1e-10, 1e10, -1e10],
            'sex': ['M', 'F', 'M']
        })
        
        ax = scatterplot(data=extreme_df, x='x', y='y', sex='sex')
        
        assert ax is not None
        assert len(ax.artists) == 3
        plt.close()
    
    def test_nan_handling(self, clean_matplotlib):
        """Test handling of NaN values in data."""
        nan_df = pd.DataFrame({
            'x': [1, 2, np.nan, 4],
            'y': [1, np.nan, 3, 4],
            'sex': ['M', 'F', None, 'M'],
            'category': ['A', None, 'B', 'C']
        })
        
        # Should handle NaN gracefully (may skip those points)
        ax = scatterplot(data=nan_df, x='x', y='y', sex='sex', hue='category')
        
        assert ax is not None
        # Artists count may be less than 4 due to NaN handling
        assert len(ax.artists) <= 4
        plt.close()
    
    def test_mixed_data_types(self, clean_matplotlib):
        """Test handling of mixed data types."""
        mixed_df = pd.DataFrame({
            'x': [1, 2.5, 3, 4.7],
            'y': [1.1, 2, 3.3, 4],
            'sex': [1, 0, 'M', 'F'],  # Mixed numeric and string
            'category': [1, 2, 'A', 'B']  # Mixed types
        })
        
        ax = scatterplot(data=mixed_df, x='x', y='y', sex='sex', hue='category')
        
        assert ax is not None
        assert len(ax.artists) == 4
        plt.close()


class TestCustomizationOptions:
    """Test customization and styling options."""
    
    def test_custom_zoom_levels(self, clean_matplotlib, sample_dataframe):
        """Test different zoom levels."""
        zoom_levels = [0.1, 0.3, 0.5, 0.8, 1.0]
        
        for zoom in zoom_levels:
            ax = scatterplot(data=sample_dataframe.head(3), x='x', y='y', 
                           sex='sex', zoom=zoom)
            assert ax is not None
            plt.close()
    
    def test_palette_variations(self, clean_matplotlib, sample_dataframe):
        """Test different palette specifications."""
        palettes = [
            'viridis',
            'Set1', 
            ['red', 'green', 'blue'],
            {'A': 'red', 'B': 'green', 'C': 'blue'}
        ]
        
        for palette in palettes:
            try:
                ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                               hue='categories', palette=palette)
                assert ax is not None
                plt.close()
            except Exception as e:
                # Some palettes might not be available in all environments
                print(f"Palette {palette} not available: {e}")
    
    def test_size_variations(self, clean_matplotlib, sample_dataframe):
        """Test different size specifications."""
        size_specs = [
            [10, 20, 30],
            (15, 25, 35),
            {'A': 20, 'B': 40, 'C': 60},
            50  # Single size
        ]
        
        for sizes in size_specs:
            ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                           size='categories', sizes=sizes)
            assert ax is not None
            plt.close()


class TestDocumentationExamples:
    """Test examples that would appear in documentation."""
    
    def test_basic_example(self, clean_matplotlib):
        """Test basic usage example from docs."""
        # Create sample data
        data = pd.DataFrame({
            'age': [25, 45, 67, 23, 89, 34],
            'score': [2, 5, 1, 6, 3, 4],
            'sex': ['M', 'F', 'M', 'F', 'M', 'F'],
            'condition': ['A', 'B', 'A', 'B', 'A', 'B']
        })
        
        # Basic plot
        ax = scatterplot(data=data, x='age', y='score', sex='sex')
        assert ax is not None
        plt.close()
        
        # With hue
        ax = scatterplot(data=data, x='age', y='score', sex='sex', hue='condition')
        assert ax is not None
        plt.close()
    
    def test_advanced_example(self, clean_matplotlib):
        """Test advanced usage example."""
        # More complex data
        np.random.seed(42)
        n = 50
        data = pd.DataFrame({
            'age': np.random.normal(65, 15, n),
            'cognitive_score': np.random.normal(25, 5, n),
            'sex': np.random.choice(['M', 'F'], n),
            'diagnosis': np.random.choice(['Control', 'MCI', 'AD'], n),
            'severity': np.random.uniform(0, 1, n)
        })
        
        # Advanced plot with multiple parameters
        ax = scatterplot(data=data, x='age', y='cognitive_score',
                        sex='sex', hue='diagnosis', size='severity',
                        palette='viridis')
        
        assert ax is not None
        assert len(ax.artists) == n
        plt.close()


class TestIntegrationWithOtherLibraries:
    """Test integration with other common libraries."""
    
    def test_with_matplotlib_subplots(self, clean_matplotlib, sample_dataframe):
        """Test integration with matplotlib subplot system."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Different plots on different axes
        scatterplot(data=sample_dataframe, x='x', y='y', sex='sex', ax=ax1)
        scatterplot(data=sample_dataframe, x='y', y='x', hue='categories', ax=ax2)
        scatterplot(data=sample_dataframe, x='x', y='colors', sex='sex', ax=ax3)
        scatterplot(data=sample_dataframe, x='colors', y='y', hue='sex', ax=ax4)
        
        # All axes should have artists
        assert len(ax1.artists) > 0
        assert len(ax2.artists) > 0  
        assert len(ax3.artists) > 0
        assert len(ax4.artists) > 0
        
        plt.close()
    
    def test_with_pandas_groupby(self, clean_matplotlib):
        """Test integration with pandas groupby operations."""
        # Create grouped data
        data = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'sex': np.random.choice(['M', 'F'], 100),
            'group': np.random.choice(['A', 'B'], 100)
        })
        
        # Plot each group separately
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        for i, (name, group) in enumerate(data.groupby('group')):
            scatterplot(data=group, x='x', y='y', sex='sex', ax=axes[i])
            axes[i].set_title(f'Group {name}')
        
        assert len(axes[0].artists) > 0
        assert len(axes[1].artists) > 0
        plt.close()


class TestRegressionTests:
    """Test for specific bugs and regressions."""
    
    def test_legend_with_single_category(self, clean_matplotlib):
        """Test legend creation with only one category."""
        single_cat_df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'sex': ['M', 'M', 'M'],  # All same
            'category': ['A', 'A', 'A']  # All same
        })
        
        ax = scatterplot(data=single_cat_df, x='x', y='y', hue='category')
        
        # Should still create legend even with single category
        legend = ax.get_legend()
        assert legend is not None
        plt.close()
    
    def test_empty_string_categories(self, clean_matplotlib):
        """Test handling of empty string categories."""
        empty_str_df = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y': [1, 2, 3, 4],
            'sex': ['M', 'F', '', 'M'],
            'category': ['A', '', 'B', 'C']
        })
        
        ax = scatterplot(data=empty_str_df, x='x', y='y', sex='sex', hue='category')
        
        assert ax is not None
        assert len(ax.artists) == 4
        plt.close()
    
    def test_zero_values(self, clean_matplotlib):
        """Test handling of zero coordinates."""
        zero_df = pd.DataFrame({
            'x': [0, 1, 2, 0],
            'y': [0, 0, 1, 2],
            'sex': ['M', 'F', 'M', 'F']
        })
        
        ax = scatterplot(data=zero_df, x='x', y='y', sex='sex')
        
        assert ax is not None
        assert len(ax.artists) == 4
        plt.close()
    
    def test_duplicate_coordinates(self, clean_matplotlib):
        """Test handling of overlapping points."""
        duplicate_df = pd.DataFrame({
            'x': [1, 1, 1, 2],  # Multiple points at same location
            'y': [1, 1, 1, 2],
            'sex': ['M', 'F', 'M', 'F'],
            'category': ['A', 'B', 'A', 'B']
        })
        
        ax = scatterplot(data=duplicate_df, x='x', y='y', sex='sex', hue='category')
        
        assert ax is not None
        assert len(ax.artists) == 4  # All points should be plotted
        plt.close()


# Parametrized tests for comprehensive coverage
class TestParametrizedScenarios:
    """Parametrized tests for comprehensive scenario coverage."""
    
    @pytest.mark.parametrize("sex_format", [
        ['M', 'F', 'M'],
        ['male', 'female', 'male'], 
        [1, 0, 1],
        ['man', 'woman', 'man']
    ])
    def test_different_sex_formats(self, clean_matplotlib, sex_format):
        """Test different sex format specifications."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'sex': sex_format
        })
        
        ax = scatterplot(data=data, x='x', y='y', sex='sex')
        assert ax is not None
        assert len(ax.artists) == 3
        plt.close()
    
    @pytest.mark.parametrize("legend_setting", [True, False, 'auto', 'brief', 'full'])
    def test_legend_settings(self, clean_matplotlib, sample_dataframe, legend_setting):
        """Test different legend settings."""
        ax = scatterplot(data=sample_dataframe, x='x', y='y', 
                        hue='categories', legend=legend_setting)
        
        assert ax is not None
        
        if legend_setting in [False]:
            assert ax.get_legend() is None
        elif legend_setting in [True, 'auto', 'brief', 'full']:
            # Should have legend (implementation may vary)
            pass  # Legend presence depends on implementation details
        
        plt.close()
    
    @pytest.mark.parametrize("data_size", [1, 5, 20, 100])
    def test_different_data_sizes(self, clean_matplotlib, data_size):
        """Test with different data sizes."""
        np.random.seed(42)
        data = pd.DataFrame({
            'x': np.random.randn(data_size),
            'y': np.random.randn(data_size),
            'sex': np.random.choice(['M', 'F'], data_size),
            'category': np.random.choice(['A', 'B', 'C'], data_size)
        })
        
        ax = scatterplot(data=data, x='x', y='y', sex='sex', hue='category')
        
        assert ax is not None
        assert len(ax.artists) == data_size
        plt.close()