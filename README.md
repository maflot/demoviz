# Demoviz - demographic visualization

> **note**
> Fell free to fork or use it as a template for your own project with other icons.

## Installation
``` bash
pip install demoviz
```

## Demoviz

Demoviz is a library for creating demographic visualizations.
Using human vector icons, it can create scatter plots of demographic data, coloring the icons by the demographic data.
and highlight the icons by the demographic data.

# Acknowledgments
the icons have been retrieved from wikimedia commons.
``` bash
# female icon
wget https://upload.wikimedia.org/wikipedia/commons/f/f9/Woman_%28958542%29_-_The_Noun_Project.svg
# male icon
wget https://upload.wikimedia.org/wikipedia/commons/d/d8/Person_icon_BLACK-01.svg
```

## Example
See readme in example directory for more details, but her in short:
Open access by the german federal statistical office is used some age-based data visualization.
``` bash
cd example  
python demographic_change.py
python disease_analysis.py
```
The data displayed is from 2023 and beatifully visualized the fall of the berlin wall and the reunification of germany.
![demographic_change](example/plots/germany_demographic_timeline.png)

But also the disease burden and the sex-specific disease burden are visualized.
![disease_analysis](example/plots/german_infectious_vs_cancer_2023.png)

In any case, if you ever need to plot some human icons or icons in general, you can use the `demoviz` library.

## Demoviz

Demoviz is a library for creating demographic visualizations.
