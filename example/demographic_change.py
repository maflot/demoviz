"""
Germany Demographic Change Visualization with demoviz
====================================================

This example showcases Germany's population change from 1950-2024 using creative
human icon visualizations. Data source: Statistisches Bundesamt (Destatis).

Key insights visualized:
- German reunification impact (1990)
- Population growth and decline phases
- Recent immigration waves
- Demographic transitions over 75 years
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import demoviz as dv

# Set style for publication-quality plots
np.random.seed(42)

def load_germany_data():
    """Load and clean German population data."""
    try:
        # Try to load from data directory
        data_path = Path("data/germany_population.csv")
        if not data_path.exists():
            # Create the data from the provided information
            create_germany_dataset()
        
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return create_germany_dataset()

def create_germany_dataset():
    """Create the German population dataset from the provided data."""
    # Population data from Statistisches Bundesamt
    population_data = [
        ("1950-12-31", 50958125), ("1951-12-31", 51434777), ("1952-12-31", 51863761),
        ("1953-12-31", 52453806), ("1954-12-31", 52943295), ("1955-12-31", 53517683),
        ("1956-12-31", 53339626), ("1957-12-31", 54064365), ("1958-12-31", 54719159),
        ("1959-12-31", 55257088), ("1960-12-31", 55958321), ("1961-12-31", 56589148),
        ("1962-12-31", 57247246), ("1963-12-31", 57864509), ("1964-12-31", 58587451),
        ("1965-12-31", 59296591), ("1966-12-31", 59792934), ("1967-12-31", 59948474),
        ("1968-12-31", 60463033), ("1969-12-31", 61194591), ("1970-12-31", 61001164),
        ("1971-12-31", 61502503), ("1972-12-31", 61809378), ("1973-12-31", 62101369),
        ("1974-12-31", 61991475), ("1975-12-31", 61644624), ("1976-12-31", 61441996),
        ("1977-12-31", 61352745), ("1978-12-31", 61321663), ("1979-12-31", 61439342),
        ("1980-12-31", 61657945), ("1981-12-31", 61712689), ("1982-12-31", 61546101),
        ("1983-12-31", 61306669), ("1984-12-31", 61049256), ("1985-12-31", 61020474),
        ("1986-12-31", 61140461), ("1987-12-31", 61238079), ("1988-12-31", 61715103),
        ("1989-12-31", 62679035), ("1990-12-31", 79753227), ("1991-12-31", 80274564),
        ("1992-12-31", 80974632), ("1993-12-31", 81338093), ("1994-12-31", 81538603),
        ("1995-12-31", 81817499), ("1996-12-31", 82012162), ("1997-12-31", 82057379),
        ("1998-12-31", 82037011), ("1999-12-31", 82163475), ("2000-12-31", 82259540),
        ("2001-12-31", 82440309), ("2002-12-31", 82536680), ("2003-12-31", 82531671),
        ("2004-12-31", 82500849), ("2005-12-31", 82437995), ("2006-12-31", 82314906),
        ("2007-12-31", 82217837), ("2008-12-31", 82002356), ("2009-12-31", 81802257),
        ("2010-12-31", 81751602), ("2011-12-31", 80327900), ("2012-12-31", 80523746),
        ("2013-12-31", 80767463), ("2014-12-31", 81197537), ("2015-12-31", 82175684),
        ("2016-12-31", 82521653), ("2017-12-31", 82792351), ("2018-12-31", 83019213),
        ("2019-12-31", 83166711), ("2020-12-31", 83155031), ("2021-12-31", 83237124),
        ("2022-12-31", 83118501), ("2023-12-31", 83456045), ("2024-12-31", 83577140)
    ]
    
    df = pd.DataFrame(population_data, columns=['date', 'population'])
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    
    # Add demographic phases
    df['phase'] = df['year'].apply(lambda x: 
        'Post-War Growth' if x < 1961 else
        'Baby Boom Era' if x < 1973 else
        'Stagnation' if x < 1990 else
        'Reunification Boom' if x < 2005 else
        'Decline Period' if x < 2015 else
        'Immigration Wave'
    )
    
    # Add population change
    df['pop_change'] = df['population'].diff()
    df['pop_change_pct'] = df['population'].pct_change() * 100
    
    # Add milestone markers
    df['milestone'] = ''
    df.loc[df['year'] == 1961, 'milestone'] = 'Berlin Wall Built'
    df.loc[df['year'] == 1989, 'milestone'] = 'Fall of Berlin Wall'
    df.loc[df['year'] == 1990, 'milestone'] = 'German Reunification'
    df.loc[df['year'] == 2015, 'milestone'] = 'Refugee Crisis'
    
    # Save to CSV for future use
    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/germany_population.csv", index=False)
    
    return df

def create_reunification_impact_plot(df):
    """Visualize the dramatic impact of German reunification."""
    print("Creating reunification impact visualization...")
    
    # Focus on years around reunification
    reunification_data = df[(df['year'] >= 1985) & (df['year'] <= 1995)].copy()
    
    # Create simulated regional data (West vs East Germany metaphor)
    n_points = len(reunification_data)
    
    # Pre-1990: Only "West" people, Post-1990: Mix of "West" and "East"
    reunification_data['region'] = reunification_data['year'].apply(
        lambda x: 'West Germany' if x < 1990 else 'Unified Germany'
    )
    
    # Create symbolic population representation
    reunification_data['symbolic_pop'] = reunification_data['population'] / 1_000_000  # In millions
    reunification_data['growth_rate'] = reunification_data['pop_change_pct']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Top plot: The dramatic jump
    years = reunification_data['year']
    pop_millions = reunification_data['symbolic_pop']
    
    # Use traditional scatter for the line, then human icons for key points
    ax1.plot(years, pop_millions, 'o-', linewidth=3, markersize=8, 
             color='#000000', alpha=0.3, label='Population Trend')
    
    # Highlight reunification with human icons
    key_years = [1989, 1990, 1991]
    for year in key_years:
        year_data = reunification_data[reunification_data['year'] == year]
        if not year_data.empty:
            x_pos = year
            y_pos = year_data['symbolic_pop'].iloc[0]
            color = '#FF0000' if year == 1990 else '#FFD700'  # Red for reunification, gold for others
            
            # Use demoviz for symbolic representation
            dv.scatter([x_pos], [y_pos], sex=['M'], c=[color], s=60, zoom=0.4, ax=ax1)
    
    ax1.axvline(x=1990, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax1.text(1990.2, 75, 'German\nReunification\nOct 3, 1990', 
             fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population (Millions)')
    ax1.set_title('The Reunification Shock: Germany\'s Population Jump', fontsize=16, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Bottom plot: Growth rate with human icons showing East vs West metaphor
    ax2.bar(years, reunification_data['growth_rate'], 
            color=['#1f77b4' if x < 1990 else '#ff7f0e' for x in years],
            alpha=0.7, width=0.8)
    
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax2.axvline(x=1990, color='red', linestyle='--', alpha=0.7, linewidth=2)
    
    # Add human icons for dramatic growth
    max_growth_year = reunification_data.loc[reunification_data['growth_rate'].idxmax(), 'year']
    max_growth_rate = reunification_data['growth_rate'].max()
    
    dv.scatter([max_growth_year], [max_growth_rate + 5], 
               sex=['M'], c=['#00FF00'], s=80, zoom=0.5, ax=ax2)
    ax2.text(max_growth_year, max_growth_rate + 8, f'+{max_growth_rate:.1f}%\nPeak Growth', 
             ha='center', fontsize=9, fontweight='bold')
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Population Growth Rate (%)')
    ax2.set_title('Annual Population Change: The Reunification Effect', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/germany_reunification_impact.png', dpi=300, bbox_inches='tight')
    return fig

def create_demographic_phases_plot(df):
    """Create a comprehensive view of Germany's demographic phases."""
    print("Creating demographic phases visualization...")
    
    # Sample data points for visualization (every 5 years + key years)
    key_years = [1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1989, 1990, 
                1995, 2000, 2005, 2010, 2015, 2020, 2024]
    
    plot_data = df[df['year'].isin(key_years)].copy()
    
    # Create age structure simulation (metaphorical)
    plot_data['elderly_ratio'] = np.linspace(0.1, 0.3, len(plot_data))  # Aging society
    plot_data['young_ratio'] = np.linspace(0.3, 0.15, len(plot_data))   # Declining birth rate
    
    # Assign sex for demographic representation
    np.random.seed(42)
    plot_data['demo_sex'] = np.random.choice(['M', 'F'], len(plot_data))
    
    fig, ax = plt.subplots(figsize=(20, 12))
    
    # Create the main scatter plot with human icons
    x_pos = plot_data['year']
    y_pos = plot_data['population'] / 1_000_000  # Convert to millions
    
    # Color by demographic phase
    phase_colors = {
        'Post-War Growth': '#2E8B57',      # Sea Green
        'Baby Boom Era': '#FFD700',        # Gold  
        'Stagnation': '#B22222',           # Fire Brick
        'Reunification Boom': '#FF6347',   # Tomato
        'Decline Period': '#4682B4',       # Steel Blue
        'Immigration Wave': '#9370DB'       # Medium Purple
    }
    
    colors = [phase_colors[phase] for phase in plot_data['phase']]
    
    # Use demoviz for the main visualization
    dv.scatter(x_pos, y_pos, sex=plot_data['demo_sex'], c=colors, 
               s=60, zoom=0.8, jitter=0.5, ax=ax)
    
    # Add trend line
    ax.plot(x_pos, y_pos, '--', color='gray', alpha=0.5, linewidth=2, zorder=0)
    
    # Highlight major events
    events = [
        (1961, 'Berlin Wall Built'),
        (1989, 'Fall of Berlin Wall'),
        (1990, 'German Reunification'),
        (2015, 'Refugee Crisis')
    ]
    
    for year, event in events:
        if year in plot_data['year'].values:
            y_event = plot_data[plot_data['year'] == year]['population'].iloc[0] / 1_000_000
            ax.annotate(event, xy=(year, y_event), xytext=(year, y_event + 5),
                       arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                       fontsize=10, ha='center', fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Customize the plot
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Population (Millions)', fontsize=14)
    ax.set_title('Germany\'s Demographic Journey: 75 Years of Change (1950-2024)', 
                fontsize=18, fontweight='bold', pad=20)
    
    # Add phase legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=phase) 
                      for phase, color in phase_colors.items()]
    ax.legend(handles=legend_elements, loc='upper left', title='Demographic Phases', 
             title_fontsize=12, fontsize=10)
    
    # Set axis limits and formatting
    ax.set_xlim(1945, 2030)
    ax.set_ylim(45, 90)
    ax.grid(True, alpha=0.3)
    
    # Add annotations for key insights
    ax.text(0.02, 0.98, 
           'Key Insights:\n'
           '• 1990: +27% population jump from reunification\n'
           '• 2005-2015: Demographic decline period\n'
           '• 2015+: Immigration-driven recovery\n'
           '• 75 years: +32.6 million people (+64%)',
           transform=ax.transAxes, fontsize=11,
           verticalalignment='top',
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('plots/germany_demographic_phases.png', dpi=300, bbox_inches='tight')
    return fig

def create_population_pyramid_evolution(df):
    """Create a creative population pyramid evolution using human icons."""
    print("Creating population pyramid evolution...")
    
    # Select key years for comparison
    key_years = [1960, 1990, 2024]
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    
    for idx, year in enumerate(key_years):
        ax = axes[idx]
        
        # Get population for this year
        year_pop = df[df['year'] == year]['population'].iloc[0]
        
        # Simulate age structure (creative representation)
        age_groups = ['0-14', '15-29', '30-44', '45-59', '60-74', '75+']
        
        # Different age distributions for different years
        if year == 1960:  # Post-war baby boom
            male_pct = [15, 18, 16, 14, 12, 8]
            female_pct = [14, 17, 15, 13, 11, 7]
        elif year == 1990:  # Reunification era
            male_pct = [8, 15, 18, 16, 12, 6]
            female_pct = [7, 14, 17, 15, 11, 8]
        else:  # 2024: Aging society
            male_pct = [6, 12, 14, 16, 18, 12]
            female_pct = [5, 11, 13, 15, 17, 15]
        
        # Create the pyramid
        y_positions = np.arange(len(age_groups))
        
        # Male side (left)
        for i, (age_group, male_p) in enumerate(zip(age_groups, male_pct)):
            n_icons = max(1, int(male_p / 3))  # Scale down for visualization
            x_positions = np.linspace(-male_p, -1, n_icons)
            dv.scatter(x_positions, [i] * n_icons, sex=['M'] * n_icons,
                      c=['#4A90E2'] * n_icons, s=40, zoom=0.3, ax=ax)
        
        # Female side (right)
        for i, (age_group, female_p) in enumerate(zip(age_groups, female_pct)):
            n_icons = max(1, int(female_p / 3))
            x_positions = np.linspace(1, female_p, n_icons)
            dv.scatter(x_positions, [i] * n_icons, sex=['F'] * n_icons,
                      c=['#E94B3C'] * n_icons, s=40, zoom=0.3, ax=ax)
        
        # Customize each subplot
        ax.set_yticks(y_positions)
        ax.set_yticklabels(age_groups)
        ax.set_xlim(-20, 20)
        ax.set_xlabel('Population %')
        ax.set_title(f'{year}\nPop: {year_pop/1_000_000:.1f}M', fontsize=14, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
        ax.grid(True, alpha=0.3)
        
        # Add male/female labels
        ax.text(-15, -0.8, 'Male', ha='center', fontweight='bold', color='#4A90E2')
        ax.text(15, -0.8, 'Female', ha='center', fontweight='bold', color='#E94B3C')
    
    plt.suptitle('Evolution of Germany\'s Age Structure: From Baby Boom to Aging Society', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plots/germany_population_pyramid_evolution.png', dpi=300, bbox_inches='tight')
    return fig

def create_interactive_timeline(df):
    """Create an interactive-style timeline of German demographic milestones."""
    print("Creating demographic timeline...")
    
    # Select milestone years
    milestones = [
        (1955, "Post-war economic miracle begins", "Economic Growth"),
        (1961, "Berlin Wall built", "Division"),
        (1973, "Oil crisis & demographic transition", "Crisis"),
        (1989, "Fall of Berlin Wall", "Liberation"),
        (1990, "German Reunification", "Unity"),
        (2005, "Population peak reached", "Peak"),
        (2015, "Refugee crisis & immigration wave", "Immigration"),
        (2024, "Modern Germany", "Present")
    ]
    
    fig, ax = plt.subplots(figsize=(18, 10))
    
    # Create timeline base
    years = [m[0] for m in milestones]
    populations = [df[df['year'] == year]['population'].iloc[0] / 1_000_000 
                  for year in years]
    
    # Color coding by event type
    event_colors = {
        "Economic Growth": "#228B22",
        "Division": "#DC143C", 
        "Crisis": "#FF8C00",
        "Liberation": "#FFD700",
        "Unity": "#32CD32",
        "Peak": "#4169E1",
        "Immigration": "#9370DB",
        "Present": "#FF1493"
    }
    
    colors = [event_colors[m[2]] for m in milestones]
    
    # Use demoviz for timeline points
    dv.scatter(years, populations, sex=['M', 'F'] * 4, c=colors, 
               s=80, zoom=1.0, jitter=0, ax=ax)
    
    # Connect with timeline
    ax.plot(years, populations, '--', color='gray', alpha=0.6, linewidth=3, zorder=0)
    
    # Add milestone annotations
    for i, (year, event, event_type) in enumerate(milestones):
        pop = populations[i]
        
        # Alternate annotation positions
        offset = 8 if i % 2 == 0 else -8
        va = 'bottom' if i % 2 == 0 else 'top'
        
        ax.annotate(f'{year}\n{event}', 
                   xy=(year, pop), xytext=(year, pop + offset),
                   ha='center', va=va, fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[i], alpha=0.3),
                   arrowprops=dict(arrowstyle='->', color=colors[i], alpha=0.7))
    
    # Customize plot
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Population (Millions)', fontsize=14)
    ax.set_title('Germany\'s Demographic Milestones: A Human Story in Data', 
                fontsize=16, fontweight='bold')
    
    # Add legend for event types
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=event_type) 
                      for event_type, color in event_colors.items()]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5),
             title='Event Types', title_fontsize=12)
    
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1950, 2030)
    
    plt.tight_layout()
    plt.savefig('plots/germany_demographic_timeline.png', dpi=300, bbox_inches='tight')
    return fig

def main():
    """Run the complete Germany demographic visualization showcase."""
    print("🇩🇪 Germany Demographic Change Visualization with demoviz")
    print("=" * 60)
    
    # Load data
    df = load_germany_data()
    print(f"Loaded data: {len(df)} years from {df['year'].min()}-{df['year'].max()}")
    print(f"Population change: {df['population'].iloc[0]/1e6:.1f}M → {df['population'].iloc[-1]/1e6:.1f}M")
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    try:
        fig1 = create_reunification_impact_plot(df)
        print("✅ Reunification impact plot created")
        
        fig2 = create_demographic_phases_plot(df)
        print("✅ Demographic phases plot created")
        
        fig3 = create_population_pyramid_evolution(df)
        print("✅ Population pyramid evolution created")
        
        fig4 = create_interactive_timeline(df)
        print("✅ Interactive timeline created")
        
        print(f"\n🎉 All visualizations saved to 'data/' directory!")
        print("\nKey insights from the data:")
        print("• German reunification caused a +27% population jump in 1990")
        print("• Population peaked around 2005, then declined until 2015")
        print("• Recent immigration has driven population recovery")
        print("• 75 years of change: +32.6 million people (+64% growth)")
        
        # Show plots
        plt.show()
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()