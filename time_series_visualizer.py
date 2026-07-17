import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data and set index
df_raw = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data with your exact quantile thresholds
df = df_raw[(df_raw['value'] >= df_raw['value'].quantile(0.025)) & (df_raw['value'] <= df_raw['value'].quantile(0.975))].copy()

# Part 1: Line Plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return figure
    fig.savefig('line_plot.png')
    return fig

# Part 2: Bar Plot
def draw_bar_plot():
    df_bar = df.copy()
    
    df_bar['Years'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month_name()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['Months'] = pd.Categorical(df_bar['Months'], categories=month_order, ordered=True)
    
    df_grouped = df_bar.groupby(['Years', 'Months'], observed=False)['value'].mean().unstack()
    
    fig = df_grouped.plot(kind='bar', figsize=(16, 8)).get_figure()
    
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=month_order)

    # Save image and return figure
    fig.savefig('bar_plot.png')
    return fig

# Part 3: Box Plots
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    fig, ax = plt.subplots(1, 2, figsize=(25, 12))
    
    # Left Plot: Year-wise Trend
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0], hue='year', legend=False, palette=['blue','orange','green','red'])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    
    # Right Plot: Month-wise Seasonality
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], hue='month', legend=False)
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')

    # Save image and return figure
    fig.savefig('box_plot.png')
    return fig
