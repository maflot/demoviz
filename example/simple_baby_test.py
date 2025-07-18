#!/usr/bin/env python3
"""
Simple test script for baby icon - creates one plot at a time.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from demoviz import DemoScatter

def create_single_baby_plot():
    """Create a single baby plot and save it."""
    
    # Create simple data
    ages = [0, 6, 12, 18, 24]
    weights = [3.5, 7.0, 9.5, 11.0, 12.5]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Initialize DemoScatter
    demo = DemoScatter(icon_size=40, zoom=0.3)
    
    # Plot babies with baby icons
    demo.plot(ax, ages, weights, icon_type='baby', colors='lightblue')
    
    # Customize the plot
    ax.set_xlabel('Age (months)')
    ax.set_ylabel('Weight (kg)')
    ax.set_title('Baby Growth Milestones', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Save immediately
    fig.savefig('example/plots/single_baby_test.png', dpi=150, bbox_inches='tight')
    plt.close(fig)  # Close immediately
    
    print("✅ Single baby plot created and saved successfully!")

def test_baby_icon_availability():
    """Test that baby icon is available."""
    demo = DemoScatter()
    available_icons = demo.list_available_icons()
    
    print("Available icons:")
    for icon in available_icons:
        print(f"  - {icon}")
    
    if 'baby' in available_icons:
        print("✅ Baby icon is available!")
        return True
    else:
        print("❌ Baby icon not found!")
        return False

if __name__ == "__main__":
    print("Testing baby icon functionality...")
    
    # Test icon availability
    if test_baby_icon_availability():
        # Create single plot
        create_single_baby_plot()
        print("🎉 Baby icon test completed successfully!")
    else:
        print("❌ Baby icon test failed!") 