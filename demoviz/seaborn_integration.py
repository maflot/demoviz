"""
Seaborn-style integration for demoviz.
"""

import matplotlib.pyplot as plt
import numpy as np
from .matplotlib_integration import scatter as base_scatter

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False


def scatterplot(data=None, x=None, y=None, sex=None, hue=None, size=None, 
               style=None, palette=None, sizes=None, size_order=None,
               hue_order=None, legend='auto', ax=None, **kwargs):
    """
    Seaborn-style scatter plot with human icons.
    
    This function mimics seaborn.scatterplot() but uses human icons instead of
    regular markers.
    
    Parameters
    ----------
    data : pandas.DataFrame, optional
        Input data structure
    x, y : str or array-like
        Variables for x and y coordinates
    sex : str or array-like, optional
        Variable for icon type (male/female)
    hue : str or array-like, optional
        Variable for color mapping
    size : str or array-like, optional  
        Variable for size mapping
    style : str or array-like, optional
        Variable for icon style (currently same as sex)
    palette : palette name, list, or dict, optional
        Colors to use for hue levels
    sizes : list, dict, or tuple, optional
        Sizes to use for size levels
    size_order : list, optional
        Order for size levels
    hue_order : list, optional
        Order for hue levels
    legend : "auto", "brief", "full", or False
        How to draw the legend
    ax : matplotlib.axes.Axes, optional
        Target axis
    **kwargs
        Additional arguments passed to base scatter function
        
    Returns
    -------
    matplotlib.axes.Axes
        The plot axis
    """
    
    # Extract data if DataFrame provided
    if data is not None:
        x_data = data[x] if isinstance(x, str) else x
        y_data = data[y] if isinstance(y, str) else y
        sex_data = data[sex] if isinstance(sex, str) and sex in data.columns else sex
        hue_data = data[hue] if isinstance(hue, str) and hue in data.columns else hue
        size_data = data[size] if isinstance(size, str) and size in data.columns else size
        
        # Handle empty data
        if len(data) == 0:
            x_data = []
            y_data = []
            sex_data = []
            hue_data = []
            size_data = []
    else:
        x_data, y_data, sex_data, hue_data, size_data = x, y, sex, hue, size
    
    # Create figure if needed
    if ax is None:
        ax = plt.gca()
    
    # Handle color mapping
    colors = _process_hue_data(hue_data, palette, hue_order)
    
    # Handle size mapping  
    zoom = kwargs.pop('zoom', 0.3)
    if size_data is not None:
        zoom = _process_size_data(size_data, sizes, size_order, zoom)
    
    # Create the scatter plot
    base_scatter(x_data, y_data, sex=sex_data, c=colors, zoom=zoom, ax=ax, **kwargs)
    
    # Handle legend
    if legend and legend != False and hue_data is not None:
        _create_legend(ax, hue_data, colors, hue_order, hue)
    
    # Apply seaborn styling if available
    if HAS_SEABORN:
        sns.despine(ax=ax)
    
    return ax


def _process_hue_data(hue_data, palette, hue_order):
    """Process hue data to create color mapping."""
    if hue_data is None or len(hue_data) == 0:
        return None
    
    # Convert to list safely
    if hasattr(hue_data, 'tolist'):
        hue_list = hue_data.tolist()
    elif isinstance(hue_data, np.ndarray):
        hue_list = hue_data.tolist()
    else:
        hue_list = list(hue_data)
    
    if not hue_list:
        return None
    
    # Get unique values, handle mixed types
    unique_hues = list(set(hue_list))
    try:
        # Sort safely with mixed types
        unique_hues = sorted(unique_hues, key=lambda x: (x is None, str(x)))
    except (TypeError, AttributeError):
        pass  # Use unsorted if sorting fails
    
    if hue_order:
        unique_hues = hue_order
    
    # Create color mapping
    if palette is not None:
        if HAS_SEABORN and isinstance(palette, str):
            try:
                pal = sns.color_palette(palette, len(unique_hues))
                color_map = dict(zip(unique_hues, pal))
                return [color_map.get(h, (0.5, 0.5, 0.5, 1.0)) for h in hue_list]
            except Exception:
                pass
        
        if isinstance(palette, dict):
            return [palette.get(h, 'blue') for h in hue_list]
    
    # Default color mapping using matplotlib
    try:
        if len(unique_hues) > 0:
            cmap = plt.colormaps['tab10']
            color_map = {hue: cmap(i / max(len(unique_hues)-1, 1)) 
                        for i, hue in enumerate(unique_hues)}
            return [color_map.get(h, (0.5, 0.5, 0.5, 1.0)) for h in hue_list]
    except Exception:
        pass
    
    return hue_list  # Return original data as fallback


def _process_size_data(size_data, sizes, size_order, default_zoom):
    """Process size data to create zoom mapping."""
    if size_data is None:
        return default_zoom
    
    # Simple implementation - could be enhanced
    if sizes is not None:
        if isinstance(sizes, (list, tuple)) and len(sizes) > 0:
            return np.mean(sizes) / 100  # Convert to zoom range
        elif isinstance(sizes, dict):
            return np.mean(list(sizes.values())) / 100
    
    return default_zoom


def _create_legend(ax, hue_data, colors, hue_order, hue_name):
    """Create legend for hue mapping."""
    try:
        # Get unique hues
        if hasattr(hue_data, 'tolist'):
            hue_list = hue_data.tolist()
        else:
            hue_list = list(hue_data)
        
        unique_hues = list(set(hue_list))
        try:
            unique_hues = sorted(unique_hues, key=lambda x: (x is None, str(x)))
        except (TypeError, AttributeError):
            pass
        
        if hue_order:
            unique_hues = hue_order
        
        # Create legend elements
        legend_elements = []
        for hue_val in unique_hues:
            # Find color for this hue
            if colors and hasattr(colors, '__len__') and not isinstance(colors, str):
                hue_indices = [i for i, h in enumerate(hue_list) if h == hue_val]
                if hue_indices:
                    color = colors[hue_indices[0]]
                    if isinstance(color, np.ndarray):
                        color = color.tolist()
                else:
                    color = 'blue'
            else:
                color = 'blue'
            
            legend_elements.append(
                plt.Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor=color, markersize=8, label=str(hue_val))
            )
        
        title = hue_name if isinstance(hue_name, str) else 'Hue'
        ax.legend(handles=legend_elements, title=title)
    except Exception:
        pass  # Fail silently if legend creation fails


def relplot(data=None, x=None, y=None, sex=None, hue=None, size=None,
           col=None, row=None, kind='scatter', **kwargs):
    """
    Figure-level interface for drawing relational plots with human icons.
    
    This is a simplified version of seaborn.relplot() that supports human icons.
    Currently only supports kind='scatter'.
    """
    
    if kind != 'scatter':
        raise ValueError("Only kind='scatter' is currently supported")
    
    # Simple implementation - could be expanded for faceting
    if col is None and row is None:
        # Single plot
        fig, ax = plt.subplots(figsize=kwargs.pop('figsize', (8, 6)))
        scatterplot(data=data, x=x, y=y, sex=sex, hue=hue, size=size, ax=ax, **kwargs)
        return fig
    else:
        # Would need more complex faceting logic
        raise NotImplementedError("Faceting (col/row) not yet implemented")


def demographic_plot(*args, **kwargs):
    """Alias for scatterplot. Deprecated - use scatterplot instead."""
    import warnings
    warnings.warn("demographic_plot is deprecated, use scatterplot instead", 
                  DeprecationWarning, stacklevel=2)
    return scatterplot(*args, **kwargs)