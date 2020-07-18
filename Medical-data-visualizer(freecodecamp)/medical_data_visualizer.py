import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
BMI = df['weight']/ ((df['height']/100) ** 2)
df['overweight'] = pd.Series(np.where(BMI > 25, 1, 0))


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = pd.Series(np.where(df['cholesterol'] == 1, 0, 1))
df['gluc'] = pd.Series(np.where(df['gluc'] == 1, 0, 1))

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], id_vars = ['cardio'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df_cat.sort_values(['variable'])

    # Draw the catplot with 'sns.catplot()'
    fig1 = sns.catplot(x = 'variable', col = 'cardio', hue= 'value', data= df_cat, kind ="count")
    fig1.set(ylabel = "total")
    fig = fig1.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height']
    <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) &
    (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10,10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, fmt ='.1f', mask = mask, vmin = -0.08, vmax = 0.24, center = 0, annot=True)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
