"""
Matplotlib integration for demoviz.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .core import DemoScatter


def scatter(x, y, sex=None, c=None, s=40, zoom=0.3, jitter=0, 
           ax=None, figsize=None, custom_icons=None, **kwargs):
    """
    Create a scatter plot with human icons.
    
    This is the main high-level function for creating demographic scatter plots.
    
    Parameters
    ----------
    x, y : array-like
        Data coordinates
    sex : array-like, optional
        Sex/gender for each point. Accepts 'M'/'F', 'male'/'female', 1/0, etc.
        If None, uses generic person icons.
    c : color or array-like, optional
        Colors for icons. Can be single color, array of colors, or values to map.
    s : float, default 40
        Icon size in pixels
    zoom : float, default 0.3
        Icon zoom factor (affects visual size)
    jitter : float, default 0
        Random position jitter to avoid overlapping
    ax : matplotlib.axes.Axes, optional
        Target axis. Creates new figure if None.
    figsize : tuple, optional
        Figure size (width, height) if creating new figure
    custom_icons : dict, optional
        Custom icon paths {'male': path, 'female': path}
    **kwargs
        Additional keyword arguments passed to axis setup
        
    Returns
    -------
    matplotlib.axes.Axes
        The plot axis
        
    Examples
    --------
    Basic usage:
    >>> import demoviz as dv
    >>> ages = [45, 67, 23, 89, 34]
    >>> scores = [2, 5, 1, 6, 3] 
    >>> sexes = ['M', 'F', 'M', 'F', 'M']
    >>> ax = dv.scatter(ages, scores, sex=sexes)
    
    With custom colors:
    >>> colors = ['red', 'blue', 'green', 'purple', 'orange']
    >>> ax = dv.scatter(ages, scores, sex=sexes, c=colors)
    
    With continuous color mapping:
    >>> severity = [0.2, 0.8, 0.1, 0.9, 0.4]
    >>> ax = dv.scatter(ages, scores, sex=sexes, c=severity)
    """
    
    # Create figure/axis if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    
    # Handle color mapping for continuous data
    if c is not None and not isinstance(c, str):
        c = np.asarray(c)
        # Check if it's numeric data that can be mapped to colors
        if len(c) > 0 and c.dtype.kind in 'biufc':  # numeric data
            # Map to colormap
            cmap = kwargs.pop('cmap', 'viridis')
            norm = plt.Normalize(vmin=c.min(), vmax=c.max())
            colors = plt.colormaps[cmap](norm(c))  # Use modern API
        elif len(c) > 0:
            # For categorical data, create a color mapping
            try:
                unique_vals = np.unique(c[~pd.isna(c)] if hasattr(c, 'dtype') else c)
                if len(unique_vals) <= 10:  # Reasonable number of categories
                    cmap = kwargs.pop('cmap', 'tab10')
                    color_palette = plt.colormaps[cmap]
                    color_map = {val: color_palette(i / max(len(unique_vals)-1, 1)) 
                               for i, val in enumerate(unique_vals)}
                    colors = [color_map.get(val, (0.5, 0.5, 0.5, 1.0)) for val in c]
                else:
                    colors = c  # Let the core handle it
            except Exception:
                colors = c  # Let the core handle it
        else:
            colors = None  # Empty data
    else:
        colors = c
    
    # Create scatter plot
    demo_scatter = DemoScatter(icon_size=s, zoom=zoom, custom_icons=custom_icons)
    demo_scatter.plot(ax, x, y, icon_type=sex, colors=colors, jitter=jitter)
    
    # Update data limits
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    
    return ax


def plot_demographics(data, x, y, sex=None, hue=None, size=None, 
                     figsize=(10, 6), title=None, **kwargs):
    """
    Create a demographic plot from a DataFrame.
    
    Parameters
    ----------
    data : pandas.DataFrame
        Input data
    x, y : str
        Column names for x and y coordinates
    sex : str, optional
        Column name for sex/gender
    hue : str, optional  
        Column name for color mapping
    size : str, optional
        Column name for size mapping (affects zoom)
    figsize : tuple, default (10, 6)
        Figure size
    title : str, optional
        Plot title
    **kwargs
        Additional arguments passed to scatter()
        
    Returns
    -------
    matplotlib.axes.Axes
        The plot axis
        
    Examples
    --------
    >>> import pandas as pd
    >>> import demoviz as dv
    >>> df = pd.DataFrame({
    ...     'age': [45, 67, 23, 89],
    ...     'score': [2, 5, 1, 6],
    ...     'sex': ['M', 'F', 'M', 'F'],
    ...     'severity': [0.2, 0.8, 0.1, 0.9]
    ... })
    >>> ax = dv.plot_demographics(df, 'age', 'score', sex='sex', hue='severity')
    """
    
    # Extract data
    x_data = data[x]
    y_data = data[y]
    sex_data = data[sex] if sex else None
    hue_data = data[hue] if hue else None
    size_data = data[size] if size else None
    
    # Handle size mapping
    if size_data is not None:
        # Normalize size to reasonable zoom range
        size_norm = (size_data - size_data.min()) / (size_data.max() - size_data.min())
        zoom_values = 0.2 + size_norm * 0.4  # Range from 0.2 to 0.6
        # For now, we'll use average zoom (could be enhanced to support per-point sizing)
        zoom = zoom_values.mean()
        kwargs.setdefault('zoom', zoom)
    
    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    scatter(x_data, y_data, sex=sex_data, c=hue_data, ax=ax, **kwargs)
    
    # Styling
    ax.set_xlabel(x.title().replace('_', ' '))
    ax.set_ylabel(y.title().replace('_', ' '))
    
    if title:
        ax.set_title(title)
    
    # Add colorbar if using continuous hue
    if hue_data is not None and np.issubdtype(hue_data.dtype, np.number):
        import matplotlib.cm as cm
        cmap = kwargs.get('cmap', 'viridis')
        norm = plt.Normalize(vmin=hue_data.min(), vmax=hue_data.max())
        sm = cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label(hue.title().replace('_', ' '))
    
    plt.tight_layout()
    return ax