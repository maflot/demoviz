"""
German Disease Mortality Analysis with demoviz
=============================================

Analyzing mortality patterns by age, sex, and disease type using German health statistics.
Data source: Statistisches Bundesamt (Destatis) - Causes of death statistics 2023.

Key insights visualized:
- Disease burden across age groups
- Sex differences in mortality patterns  
- Leading causes of death by demographics
- Cancer vs infectious disease patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import demoviz as dv

# Set style for medical publication quality
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(42)

def load_mortality_data():
    """Load and process German mortality data."""
    
    # Create the mortality dataset from the provided data
    data = {
        'disease_code': ['TDU-01', 'TDU-011', 'TDU-012', 'TDU-013', 'TDU-014', 'TDU-02', 'TDU-021', 
                        'TDU-02101', 'TDU-02102', 'TDU-02103', 'TDU-02104'],
        'disease_name': [
            'Infectious and parasitic diseases',
            'Tuberculosis', 
            'Meningococcal infection',
            'Viral hepatitis',
            'HIV disease', 
            'Neoplasms (all)',
            'Malignant neoplasms',
            'Oral cavity cancers',
            'Esophageal cancer',
            'Stomach cancer', 
            'Colon cancer'
        ],
        'category': [
            'Infectious', 'Infectious', 'Infectious', 'Infectious', 'Infectious',
            'Cancer', 'Cancer', 'Cancer', 'Cancer', 'Cancer', 'Cancer'
        ]
    }
    
    # Age groups from the data
    age_groups = [
        'under 1 year', '1 to under 15 years', '15 to under 20 years', '20 to under 25 years',
        '25 to under 30 years', '30 to under 35 years', '35 to under 40 years', '40 to under 45 years',
        '45 to under 50 years', '50 to under 55 years', '55 to under 60 years', '60 to under 65 years',
        '65 to under 70 years', '70 to under 75 years', '75 to under 80 years', '80 to under 85 years',
        '85 years and over'
    ]
    
    # Sample mortality data (extracted from the table)
    # Male deaths by age group for selected diseases
    male_deaths = {
        'TDU-01': [12, 28, 6, 10, 18, 21, 55, 81, 144, 187, 379, 597, 772, 966, 1051, 1843, 2926],
        'TDU-014': [0, 0, 0, 0, 3, 7, 16, 13, 20, 34, 31, 32, 23, 15, 14, 14, 6],  # HIV
        'TDU-021': [0, 139, 65, 77, 133, 231, 366, 723, 1174, 3130, 6961, 11884, 15493, 18614, 17680, 23584, 23584],  # Malignant neoplasms
        'TDU-02104': [0, 0, 0, 0, 8, 15, 28, 55, 88, 210, 392, 628, 859, 1035, 1022, 1470, 1718]  # Colon cancer
    }
    
    # Female deaths by age group for selected diseases  
    female_deaths = {
        'TDU-01': [14, 36, 0, 5, 9, 17, 23, 30, 36, 102, 166, 294, 459, 720, 898, 1834, 4644],
        'TDU-014': [0, 0, 0, 0, 0, 0, 5, 3, 0, 9, 5, 5, 5, 0, 3, 0, 0],  # HIV
        'TDU-021': [4, 93, 34, 66, 106, 278, 537, 934, 1481, 3020, 5801, 9006, 11350, 13535, 13751, 20005, 26451],  # Malignant neoplasms
        'TDU-02104': [0, 0, 0, 0, 6, 11, 21, 58, 80, 136, 274, 436, 536, 756, 842, 1477, 2515]  # Colon cancer
    }
    
    # Convert age groups to numeric for plotting
    age_numeric = [0.5, 8, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 52.5, 57.5, 62.5, 67.5, 72.5, 77.5, 82.5, 90]
    
    # Create expanded dataset for scatter plotting
    rows = []
    
    selected_diseases = ['TDU-01', 'TDU-014', 'TDU-021', 'TDU-02104']
    disease_names_short = {
        'TDU-01': 'Infectious Diseases',
        'TDU-014': 'HIV Disease', 
        'TDU-021': 'Cancer (Malignant)',
        'TDU-02104': 'Colon Cancer'
    }
    
    for disease in selected_diseases:
        for i, age in enumerate(age_numeric):
            # Male data
            if male_deaths[disease][i] > 0:
                # Create multiple points for larger numbers (for visualization)
                n_points = min(int(np.sqrt(male_deaths[disease][i]) / 3), 50)  # Scale down for visualization
                for _ in range(max(1, n_points)):
                    rows.append({
                        'age': age + np.random.uniform(-1, 1),  # Add jitter
                        'deaths': male_deaths[disease][i],
                        'log_deaths': np.log10(max(1, male_deaths[disease][i])),
                        'sex': 'Male',
                        'disease': disease_names_short[disease],
                        'disease_code': disease,
                        'category': 'Infectious' if disease in ['TDU-01', 'TDU-014'] else 'Cancer'
                    })
            
            # Female data
            if female_deaths[disease][i] > 0:
                n_points = min(int(np.sqrt(female_deaths[disease][i]) / 3), 50)
                for _ in range(max(1, n_points)):
                    rows.append({
                        'age': age + np.random.uniform(-1, 1),
                        'deaths': female_deaths[disease][i], 
                        'log_deaths': np.log10(max(1, female_deaths[disease][i])),
                        'sex': 'Female',
                        'disease': disease_names_short[disease],
                        'disease_code': disease,
                        'category': 'Infectious' if disease in ['TDU-01', 'TDU-014'] else 'Cancer'
                    })
    
    df = pd.DataFrame(rows)
    
    # Save processed data
    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/german_mortality_2023.csv", index=False)
    
    return df

def create_disease_burden_plot(df):
    """Visualize disease burden across age groups and sexes."""
    print("Creating disease burden visualization...")
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Color palette for diseases
    disease_colors = {
        'Infectious Diseases': '#FF6B6B',  # Red
        'HIV Disease': '#4ECDC4',          # Teal  
        'Cancer (Malignant)': '#45B7D1',  # Blue
        'Colon Cancer': '#96CEB4'          # Green
    }
    
    # Map sex to demoviz format
    df['sex_code'] = df['sex'].map({'Male': 'M', 'Female': 'F'})
    
    # Create colors array
    colors = [disease_colors[disease] for disease in df['disease']]
    
    # Use demoviz for the scatter plot
    dv.scatter(df['age'], df['log_deaths'], 
              sex=df['sex_code'], c=colors,
              s=50, zoom=0.6, jitter=0.5, ax=ax)
    
    # Customize the plot
    ax.set_xlabel('Age (years)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Deaths (log scale)', fontsize=14, fontweight='bold')
    ax.set_title('German Mortality Patterns 2023: Disease Burden by Age and Sex', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Custom y-axis labels for log scale
    yticks = [0, 1, 2, 3, 4]
    yticklabels = ['1', '10', '100', '1K', '10K']
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    
    # Create custom legend for diseases
    from matplotlib.patches import Patch
    disease_legend = [Patch(facecolor=color, label=disease) 
                     for disease, color in disease_colors.items()]
    
    # Create sex legend  
    from matplotlib.lines import Line2D
    sex_legend = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#4A90E2', 
               markersize=10, label='Male', linestyle='None'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#E94B3C',
               markersize=10, label='Female', linestyle='None')
    ]
    
    # Add legends
    legend1 = ax.legend(handles=disease_legend, loc='upper left', title='Disease Type',
                       title_fontsize=12, fontsize=10)
    legend2 = ax.legend(handles=sex_legend, loc='upper right', title='Sex',
                       title_fontsize=12, fontsize=10)
    ax.add_artist(legend1)  # Keep both legends
    
    # Add annotations for key insights
    ax.annotate('Cancer burden\nincreases with age', 
               xy=(70, 4), xytext=(75, 3.5),
               arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
               fontsize=10, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    ax.annotate('HIV peaks in\nmiddle age', 
               xy=(40, 1.5), xytext=(25, 2.5),
               arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
               fontsize=10, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
    
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 95)
    ax.set_ylim(0, 4.5)
    
    plt.tight_layout()
    plt.savefig('plots/german_disease_burden_2023.png', dpi=300, bbox_inches='tight')
    return fig

def create_sex_comparison_plot(df):
    """Compare mortality patterns between sexes."""
    print("Creating sex comparison visualization...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    diseases = df['disease'].unique()
    disease_colors = {
        'Infectious Diseases': '#FF6B6B',
        'HIV Disease': '#4ECDC4', 
        'Cancer (Malignant)': '#45B7D1',
        'Colon Cancer': '#96CEB4'
    }
    
    for idx, disease in enumerate(diseases):
        ax = axes[idx]
        disease_data = df[df['disease'] == disease]
        
        # Separate by sex
        male_data = disease_data[disease_data['sex'] == 'Male']
        female_data = disease_data[disease_data['sex'] == 'Female']
        
        # Plot with demoviz
        if len(male_data) > 0:
            dv.scatter(male_data['age'], male_data['log_deaths'],
                      sex=['M'] * len(male_data), 
                      c=[disease_colors[disease]] * len(male_data),
                      s=40, zoom=0.4, alpha=0.7, ax=ax)
        
        if len(female_data) > 0:
            dv.scatter(female_data['age'], female_data['log_deaths'],
                      sex=['F'] * len(female_data),
                      c=[disease_colors[disease]] * len(female_data), 
                      s=40, zoom=0.4, alpha=0.7, ax=ax)
        
        ax.set_title(f'{disease}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Age (years)')
        ax.set_ylabel('Deaths (log scale)')
        ax.grid(True, alpha=0.3)
        
        # Set consistent y-axis
        ax.set_ylim(0, 4.5)
        yticks = [0, 1, 2, 3, 4]
        yticklabels = ['1', '10', '100', '1K', '10K']
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
    
    plt.suptitle('Disease-Specific Mortality Patterns by Sex and Age', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plots/german_disease_sex_comparison_2023.png', dpi=300, bbox_inches='tight')
    return fig

def create_cancer_vs_infectious_plot(df):
    """Compare cancer vs infectious disease patterns."""
    print("Creating cancer vs infectious disease comparison...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Separate by category
    infectious_data = df[df['category'] == 'Infectious']
    cancer_data = df[df['category'] == 'Cancer']
    
    # Plot infectious diseases
    if len(infectious_data) > 0:
        colors_inf = ['#FF6B6B' if d == 'Infectious Diseases' else '#4ECDC4' 
                     for d in infectious_data['disease']]
        dv.scatter(infectious_data['age'], infectious_data['log_deaths'],
                  sex=infectious_data['sex'].map({'Male': 'M', 'Female': 'F'}),
                  c=colors_inf, s=50, zoom=0.6, jitter=0.3, ax=ax1)
    
    ax1.set_title('Infectious Diseases', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Age (years)')
    ax1.set_ylabel('Deaths (log scale)')
    ax1.set_ylim(0, 4.5)
    ax1.grid(True, alpha=0.3)
    
    # Plot cancer diseases  
    if len(cancer_data) > 0:
        colors_cancer = ['#45B7D1' if d == 'Cancer (Malignant)' else '#96CEB4'
                        for d in cancer_data['disease']]
        dv.scatter(cancer_data['age'], cancer_data['log_deaths'],
                  sex=cancer_data['sex'].map({'Male': 'M', 'Female': 'F'}),
                  c=colors_cancer, s=50, zoom=0.6, jitter=0.3, ax=ax2)
    
    ax2.set_title('Cancer Diseases', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Age (years)')
    ax2.set_ylabel('Deaths (log scale)')
    ax2.set_ylim(0, 4.5)
    ax2.grid(True, alpha=0.3)
    
    # Common y-axis formatting
    for ax in [ax1, ax2]:
        yticks = [0, 1, 2, 3, 4]
        yticklabels = ['1', '10', '100', '1K', '10K'] 
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
    
    plt.suptitle('Infectious vs Cancer Mortality Patterns in Germany 2023', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plots/german_infectious_vs_cancer_2023.png', dpi=300, bbox_inches='tight')
    return fig

def create_age_mortality_heatmap(df):
    """Create age-based mortality heatmap using human icons."""
    print("Creating age-based mortality heatmap...")
    
    # Aggregate deaths by age decade and disease
    df['age_decade'] = (df['age'] // 10) * 10
    
    # Calculate total deaths by age decade, sex, and disease
    heatmap_data = df.groupby(['age_decade', 'sex', 'disease'])['deaths'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Create a scatter plot that mimics a heatmap
    diseases = heatmap_data['disease'].unique()
    age_decades = sorted(heatmap_data['age_decade'].unique())
    
    disease_colors = {
        'Infectious Diseases': '#FF6B6B',
        'HIV Disease': '#4ECDC4',
        'Cancer (Malignant)': '#45B7D1', 
        'Colon Cancer': '#96CEB4'
    }
    
    # Create grid positions
    y_pos = 0
    for disease in diseases:
        disease_data = heatmap_data[heatmap_data['disease'] == disease]
        
        for sex in ['Male', 'Female']:
            sex_data = disease_data[disease_data['sex'] == sex]
            
            for age_decade in age_decades:
                age_data = sex_data[sex_data['age_decade'] == age_decade]
                
                if len(age_data) > 0:
                    deaths = age_data['deaths'].iloc[0]
                    # Scale deaths for visualization
                    n_icons = min(int(np.sqrt(deaths) / 10), 20)
                    
                    if n_icons > 0:
                        # Create grid of icons
                        for i in range(n_icons):
                            x_offset = (i % 5) * 0.15 - 0.3
                            y_offset = (i // 5) * 0.08 - 0.2
                            
                            dv.scatter([age_decade + x_offset], [y_pos + y_offset],
                                     sex=[sex[0]], c=[disease_colors[disease]],
                                     s=30, zoom=0.3, ax=ax)
            
            y_pos += 1
    
    # Customize plot
    ax.set_xlabel('Age Decade', fontsize=14, fontweight='bold')
    ax.set_ylabel('Disease & Sex', fontsize=14, fontweight='bold')
    ax.set_title('Mortality Heat Map: Deaths by Age, Sex, and Disease Type', 
                fontsize=16, fontweight='bold')
    
    # Set y-axis labels
    y_labels = []
    for disease in diseases:
        y_labels.extend([f'{disease} (M)', f'{disease} (F)'])
    
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels, fontsize=10)
    ax.set_xticks(age_decades)
    ax.set_xticklabels([f'{int(age)}s' for age in age_decades])
    
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/german_mortality_heatmap_2023.png', dpi=300, bbox_inches='tight')
    return fig

def main():
    """Run the complete German disease mortality analysis."""
    print("🦠 German Disease Mortality Analysis with demoviz")
    print("=" * 55)
    
    # Load and process data
    df = load_mortality_data()
    print(f"Processed {len(df)} mortality data points")
    print(f"Diseases: {', '.join(df['disease'].unique())}")
    print(f"Age range: {df['age'].min():.1f} - {df['age'].max():.1f} years")
    
    # Create visualizations
    print("\nCreating medical visualizations...")
    
    try:
        fig1 = create_disease_burden_plot(df)
        print("✅ Disease burden plot created")
        
        fig2 = create_sex_comparison_plot(df)
        print("✅ Sex comparison plots created")
        
        fig3 = create_cancer_vs_infectious_plot(df)
        print("✅ Cancer vs infectious disease comparison created")
        
        fig4 = create_age_mortality_heatmap(df)
        print("✅ Age-based mortality heatmap created")
        
        print(f"\n🎉 All medical visualizations saved to 'data/' directory!")
        print("\nKey medical insights:")
        print("• Cancer mortality increases exponentially with age")
        print("• HIV shows distinct middle-age peak pattern")
        print("• Sex differences vary significantly by disease type")
        print("• Infectious diseases show different age patterns than cancers")
        print("• Elderly populations bear highest overall disease burden")
        
        # Show plots
        plt.show()
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()