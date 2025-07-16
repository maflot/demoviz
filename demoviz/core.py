"""
Core functionality for demoviz package.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageDraw
import io
from pathlib import Path
try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False

try:
    from importlib import resources
    HAS_IMPORTLIB_RESOURCES = True
except ImportError:
    try:
        import pkg_resources
        HAS_IMPORTLIB_RESOURCES = False
    except ImportError:
        HAS_IMPORTLIB_RESOURCES = None


def svg_to_colored_image(svg_path, color, size=(100, 100)):
    """
    Convert SVG to a colored raster image.
    
    Parameters
    ----------
    svg_path : str or Path
        Path to SVG file
    color : tuple
        RGBA color tuple (values 0-1)
    size : tuple, default (100, 100)
        Output image size (width, height)
        
    Returns
    -------
    PIL.Image
        Colored image
        
    Raises
    ------
    ImportError
        If cairosvg is not installed
    """
    if not HAS_CAIROSVG:
        raise ImportError(
            "cairosvg is required for SVG processing. "
            "Install with: pip install cairosvg"
        )
    
    png_data = cairosvg.svg2png(
        url=str(svg_path), 
        output_width=size[0], 
        output_height=size[1]
    )
    img = Image.open(io.BytesIO(png_data)).convert('RGBA')
    
    img_array = np.array(img).astype(float) / 255.0
    alpha = img_array[:, :, 3]
    
    colored_array = np.zeros_like(img_array)
    colored_array[:, :, 0] = color[0]
    colored_array[:, :, 1] = color[1]
    colored_array[:, :, 2] = color[2]
    colored_array[:, :, 3] = alpha
    
    return Image.fromarray((colored_array * 255).astype(np.uint8), 'RGBA')


class DemoScatter:
    """
    Core class for creating demographic scatter plots with human icons.
    
    Parameters
    ----------
    icon_size : int, default 40
        Size of icons in pixels
    zoom : float, default 0.3
        Zoom factor for displaying icons
    custom_icons : dict, optional
        Custom icon paths {'male': path, 'female': path}
    """
    
    # Default icon mappings
    ICON_ALIASES = {
        # Sex/Gender
        'M': 'male', 'F': 'female',
        'male': 'male', 'female': 'female',
        'man': 'male', 'woman': 'female',
        1: 'male', 0: 'female',  # Common numeric coding
        # Add more aliases as needed
    }
    
    def __init__(self, icon_size=40, zoom=0.3, custom_icons=None):
        self.icon_size = icon_size
        self.zoom = zoom
        self.icon_cache = {}
        self.icon_paths = self._get_icon_paths(custom_icons)
    
    def _get_icon_paths(self, custom_icons=None):
        """Get paths to icon files."""
        if custom_icons:
            return custom_icons
            
        try:
            # Try modern importlib.resources first
            if HAS_IMPORTLIB_RESOURCES:
                from importlib import resources
                icon_dir = resources.files('demoviz') / 'icons'
            else:
                # Fallback to pkg_resources
                import pkg_resources
                icon_dir = Path(pkg_resources.resource_filename('demoviz', 'icons'))
            
            paths = {}
            # Look for your specific icon files
            person_file = icon_dir / 'Person_icon_BLACK-01.svg'
            woman_file = icon_dir / 'Woman_(958542)_-_The_Noun_Project.svg'
            
            if person_file.exists():
                paths['male'] = person_file
                paths['person'] = person_file
            if woman_file.exists():
                paths['female'] = woman_file
                paths['woman'] = woman_file
                
            return paths
            
        except Exception as e:
            print(f"Warning: Could not load bundled icons: {e}")
            return {}
    
    def _normalize_icon_type(self, icon_type):
        """Convert various icon type formats to standard names."""
        if icon_type in self.ICON_ALIASES:
            return self.ICON_ALIASES[icon_type]
        return str(icon_type).lower()
    
    def _create_fallback_icon(self, color, size):
        """Create a simple colored circle as fallback icon."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Convert color to proper format
        if isinstance(color, np.ndarray):
            color = color.tolist()
        elif not isinstance(color, (list, tuple)):
            color = [color, color, color, 1.0]  # Convert scalar to RGBA
        
        # Ensure we have RGB values
        if len(color) >= 3:
            rgb_color = tuple(int(float(c) * 255) for c in color[:3])
            alpha = int(float(color[3]) * 255) if len(color) > 3 else 255
        else:
            # Fallback for invalid color
            rgb_color = (128, 128, 128)  # Gray
            alpha = 255
            
        fill_color = rgb_color + (alpha,)
        
        margin = size // 10
        draw.ellipse([margin, margin, size - margin, size - margin], fill=fill_color)
        
        return img
    
    def _get_icon_image(self, icon_type, color):
        """Get colored icon image, with caching."""
        icon_type = self._normalize_icon_type(icon_type)
        
        # Convert color to RGBA tuple first
        if isinstance(color, str):
            # Handle hex colors, named colors, etc.
            from matplotlib.colors import to_rgba
            try:
                color = to_rgba(color)
            except ValueError:
                # If color conversion fails, use default blue
                color = (0.2, 0.2, 0.8, 0.8)
        elif isinstance(color, np.ndarray):
            # Convert numpy array to tuple
            color = tuple(color.tolist())
            if len(color) == 3:
                color = tuple(color) + (1.0,)
        elif hasattr(color, '__iter__') and not isinstance(color, str):
            color = tuple(color)
            if len(color) == 3:
                color = tuple(color) + (1.0,)
        else:
            # Fallback for any other case
            color = (0.2, 0.2, 0.8, 0.8)
        
        # Ensure all values are floats between 0 and 1
        try:
            color = tuple(float(c) for c in color)
            # Clamp values to 0-1 range
            color = tuple(max(0.0, min(1.0, c)) for c in color)
        except (ValueError, TypeError):
            color = (0.2, 0.2, 0.8, 0.8)  # Default fallback
        
        # Create cache key
        try:
            cache_key = f"{icon_type}_{hash(color)}"
        except (TypeError, ValueError):
            # Fallback for unhashable types
            cache_key = f"{icon_type}_{id(color)}"
        
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
        
        # Try to create icon from SVG
        if icon_type in self.icon_paths and HAS_CAIROSVG:
            try:
                img = svg_to_colored_image(
                    self.icon_paths[icon_type], 
                    color, 
                    size=(self.icon_size, self.icon_size)
                )
                self.icon_cache[cache_key] = img
                return img
            except Exception as e:
                print(f"Warning: SVG processing failed for {icon_type}: {e}")
        
        # Fallback to simple shape
        img = self._create_fallback_icon(color, self.icon_size)
        self.icon_cache[cache_key] = img
        return img
    
    def plot(self, ax, x, y, icon_type=None, colors=None, jitter=0, **kwargs):
        """
        Add human icons to matplotlib axis.
        
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Target axis
        x, y : array-like
            Data coordinates
        icon_type : str, array-like, or None
            Icon type for each point. If None, uses 'person'
        colors : color or array-like
            Colors for each icon
        jitter : float, default 0
            Random jitter to add to positions
        **kwargs
            Additional arguments (currently unused)
            
        Returns
        -------
        matplotlib.axes.Axes
            The modified axis
        """
        x = np.asarray(x)
        y = np.asarray(y)
        n_points = len(x)
        
        # Handle icon types
        if icon_type is None:
            icon_types = ['person'] * n_points
        elif np.isscalar(icon_type):
            icon_types = [icon_type] * n_points
        else:
            icon_types = np.asarray(icon_type)
        
        # Handle colors
        if colors is None:
            colors = [(0.2, 0.2, 0.8, 0.8)] * n_points  # Default blue
        elif isinstance(colors, str):
            # Single string color - don't multiply strings!
            colors = [colors] * n_points
        elif np.isscalar(colors):
            # Single scalar color
            colors = [colors] * n_points
        elif isinstance(colors, (list, tuple, np.ndarray)):
            colors = list(colors)
            # Check if it's a single color (RGB or RGBA tuple)
            if len(colors) in [3, 4] and all(isinstance(x, (int, float)) for x in colors):
                # Single color tuple
                colors = [colors] * n_points
            elif len(colors) != n_points:
                if len(colors) == 1:
                    colors = colors * n_points  # This is safe for lists
                else:
                    # Cycle through available colors
                    colors = [colors[i % len(colors)] for i in range(n_points)]
        else:
            # Convert to list and ensure right length
            colors = [colors] * n_points
        
        # Add jitter if requested
        if jitter > 0:
            np.random.seed(42)  # For reproducibility
            x_jitter = x + np.random.uniform(-jitter, jitter, len(x))
            y_jitter = y + np.random.uniform(-jitter, jitter, len(y))
        else:
            x_jitter, y_jitter = x, y
        
        # Plot each point
        for i in range(n_points):
            icon = icon_types[i] if hasattr(icon_types, '__len__') and len(icon_types) > 1 else icon_types[0] if hasattr(icon_types, '__len__') else icon_types
            
            # Handle color selection
            if hasattr(colors, '__len__') and len(colors) > 1 and not isinstance(colors[0], str):
                color = colors[i] if i < len(colors) else colors[0]
            elif hasattr(colors, '__len__') and len(colors) == 1:
                color = colors[0]
            else:
                color = colors
            
            img = self._get_icon_image(icon, color)
            imagebox = OffsetImage(img, zoom=self.zoom)
            ab = AnnotationBbox(imagebox, (x_jitter[i], y_jitter[i]), frameon=False, pad=0)
            ax.add_artist(ab)
        
        return ax
    
    def clear_cache(self):
        """Clear the icon cache."""
        self.icon_cache.clear()
    
    def list_available_icons(self):
        """List available icon types."""
        return list(self.icon_paths.keys())