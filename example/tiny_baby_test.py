#!/usr/bin/env python3
"""
Tiny baby icon test - using very small icon sizes.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from demoviz import DemoScatter

def create_tiny_baby_plot():
    """Create a baby plot with very small icons."""
    
    # Create simple data
    ages = [0, 6, 12, 18, 24]
    weights = [3.5, 7.0, 9.5, 11.0, 12.5]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Initialize DemoScatter with small icons but reasonable zoom
    demo = DemoScatter(icon_size=30, zoom=0.5)  # Smaller size but better zoom
    
    # Plot babies with baby icons
    demo.plot(ax, ages, weights, icon_type='baby', colors='lightblue')
    
    # Customize the plot
    ax.set_xlabel('Age (months)')
    ax.set_ylabel('Weight (kg)')
    ax.set_title('Baby Growth Milestones (Tiny Icons)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Save immediately
    fig.savefig('example/plots/tiny_baby_test.png', dpi=150, bbox_inches='tight')
    plt.close(fig)  # Close immediately
    
    print("✅ Tiny baby plot created and saved successfully!")

def create_minimal_baby_plot():
    """Create a minimal baby plot with just 3 points."""
    
    # Create minimal data
    ages = [6, 12, 18]
    weights = [7.0, 9.5, 11.0]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Initialize DemoScatter with minimal settings
    demo = DemoScatter(icon_size=25, zoom=0.4)  # Small but visible
    
    # Plot babies with baby icons
    demo.plot(ax, ages, weights, icon_type='baby', colors='lightblue')
    
    # Customize the plot
    ax.set_xlabel('Age (months)')
    ax.set_ylabel('Weight (kg)')
    ax.set_title('Minimal Baby Demo', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Save immediately
    fig.savefig('example/plots/minimal_baby_test.png', dpi=150, bbox_inches='tight')
    plt.close(fig)  # Close immediately
    
    print("✅ Minimal baby plot created and saved successfully!")

if __name__ == "__main__":
    print("Testing baby icon with tiny sizes...")
    
    # Test icon availability
    demo = DemoScatter()
    available_icons = demo.list_available_icons()
    
    if 'baby' in available_icons:
        print("✅ Baby icon is available!")
        
        # Create minimal plot first
        create_minimal_baby_plot()
        
        # Create tiny plot
        create_tiny_baby_plot()
        
        print("🎉 Tiny baby icon tests completed successfully!")
    else:
        print("❌ Baby icon not found!") 