"""
demoviz: Demographic data visualization with human icons
=====================================================

A matplotlib extension for creating scatter plots with human figure icons,
perfect for demographic and biomedical data visualization.

Basic usage:
    >>> import demoviz as dv
    >>> dv.scatter(ages, scores, sex=['M', 'F', 'M'], colors=colors)

Main functions:
    - scatter: Create scatter plot with human icons
    - scatterplot: Seaborn-style interface
    - DemoScatter: Core class for advanced usage
"""

from .core import DemoScatter, svg_to_colored_image
from .matplotlib_integration import scatter
from .seaborn_integration import scatterplot

__version__ = "0.1.0"
__author__ = "Matthias Flotho"
__email__ = "matthias.flotho@ccb.uni-saarland.de"

__all__ = [
    "DemoScatter",
    "scatter", 
    "scatterplot",
    "svg_to_colored_image"
]