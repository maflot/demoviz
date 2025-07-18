#!/usr/bin/env python3
"""
Demo script showing how to use the baby icon in demographic visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
from demoviz import DemoScatter

def create_baby_demo():
    """Create a demo plot showing baby icons in a demographic context."""
    
    # Create sample data for babies
    np.random.seed(42)
    n_babies = 25  # Reduced from 50 to avoid memory issues
    
    # Simulate baby data (age in months, weight in kg)
    ages = np.random.uniform(0, 24, n_babies)  # 0-24 months
    weights = np.random.normal(8, 2, n_babies)  # Average weight around 8kg
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Initialize DemoScatter with baby icons
    demo = DemoScatter(icon_size=35, zoom=0.4)  # Reasonable size and zoom
    
    # Plot babies with baby icons
    demo.plot(ax, ages, weights, icon_type='baby', colors='lightblue', jitter=0.3)
    
    # Customize the plot
    ax.set_xlabel('Age (months)')
    ax.set_ylabel('Weight (kg)')
    ax.set_title('Baby Growth Chart\nUsing Baby Icons', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add some reference lines
    ax.axhline(y=8, color='gray', linestyle='--', alpha=0.5, label='Average weight')
    ax.axvline(x=12, color='gray', linestyle='--', alpha=0.5, label='1 year')
    
    ax.legend()
    
    # Use a more conservative layout approach
    try:
        plt.tight_layout()
    except:
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    return fig

def create_mixed_demographic_demo():
    """Create a demo showing different age groups with appropriate icons."""
    
    np.random.seed(42)
    
    # Create data for different age groups
    n_points = 15  # Reduced from 30 to avoid memory issues
    
    # Adults (male/female)
    adult_ages = np.random.uniform(25, 65, n_points)
    adult_heights = np.random.normal(170, 10, n_points)
    adult_genders = np.random.choice(['male', 'female'], n_points)
    
    # Babies
    baby_ages = np.random.uniform(0, 2, n_points//2)
    baby_heights = np.random.normal(75, 10, n_points//2)
    
    # Combine data
    all_ages = np.concatenate([adult_ages, baby_ages])
    all_heights = np.concatenate([adult_heights, baby_heights])
    all_icons = np.concatenate([adult_genders, ['baby'] * (n_points//2)])
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    demo = DemoScatter(icon_size=30, zoom=0.35)  # Reasonable size and zoom
    
    # Plot with different icons for different age groups
    demo.plot(ax, all_ages, all_heights, icon_type=all_icons, 
              colors=['red' if icon == 'female' else 'blue' if icon == 'male' else 'lightgreen' 
                     for icon in all_icons], jitter=0.2)
    
    # Customize the plot
    ax.set_xlabel('Age (years)')
    ax.set_ylabel('Height (cm)')
    ax.set_title('Demographic Height Distribution\nMixed Age Groups', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Female'),
        Patch(facecolor='blue', label='Male'),
        Patch(facecolor='lightgreen', label='Baby')
    ]
    ax.legend(handles=legend_elements)
    
    # Use a more conservative layout approach
    try:
        plt.tight_layout()
    except:
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    return fig

def create_simple_baby_demo():
    """Create a very simple demo with just a few baby icons."""
    
    np.random.seed(42)
    
    # Create simple data
    ages = [0, 6, 12, 18, 24]  # Specific ages
    weights = [3.5, 7.0, 9.5, 11.0, 12.5]  # Typical weights
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    demo = DemoScatter(icon_size=30, zoom=0.25)
    
    # Plot babies with baby icons
    demo.plot(ax, ages, weights, icon_type='baby', colors='lightblue')
    
    # Customize the plot
    ax.set_xlabel('Age (months)')
    ax.set_ylabel('Weight (kg)')
    ax.set_title('Baby Growth Milestones', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(ages, weights, 1)
    p = np.poly1d(z)
    ax.plot(ages, p(ages), "r--", alpha=0.8, label='Growth trend')
    
    ax.legend()
    
    # Use a more conservative layout approach
    try:
        plt.tight_layout()
    except:
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    return fig

def list_available_icons():
    """Show what icons are available in the package."""
    demo = DemoScatter()
    available_icons = demo.list_available_icons()
    print("Available icons in demoviz:")
    for icon in available_icons:
        print(f"  - {icon}")
    return available_icons

if __name__ == "__main__":
    print("Creating baby demo plots...")
    
    # List available icons
    print("\n" + "="*50)
    list_available_icons()
    
    # Create simple baby demo first
    print("\n" + "="*50)
    print("Creating simple baby demo...")
    try:
        fig1 = create_simple_baby_demo()
        fig1.savefig('example/plots/simple_baby_demo.png', dpi=300, bbox_inches='tight')
        print("Saved: example/plots/simple_baby_demo.png")
        plt.close(fig1)  # Close to free memory
    except Exception as e:
        print(f"Error creating simple demo: {e}")
    
    # Create baby growth chart
    print("\n" + "="*50)
    print("Creating baby growth chart...")
    try:
        fig2 = create_baby_demo()
        fig2.savefig('example/plots/baby_growth_chart.png', dpi=300, bbox_inches='tight')
        print("Saved: example/plots/baby_growth_chart.png")
        plt.close(fig2)  # Close to free memory
    except Exception as e:
        print(f"Error creating growth chart: {e}")
    
    # Create mixed demographic demo
    print("\n" + "="*50)
    print("Creating mixed demographic demo...")
    try:
        fig3 = create_mixed_demographic_demo()
        fig3.savefig('example/plots/mixed_demographic_demo.png', dpi=300, bbox_inches='tight')
        print("Saved: example/plots/mixed_demographic_demo.png")
        plt.close(fig3)  # Close to free memory
    except Exception as e:
        print(f"Error creating mixed demo: {e}")
    
    print("\nDemo completed!") 