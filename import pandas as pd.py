import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_top_batsmen(df, season='all', n=10):
    """
    Returns top N batsmen by runs.
    If season = 'all', returns for all seasons.
    Else returns for the specific season.
    """
    if season != 'all':
        season = int(season)
        if season not in df['season'].unique():
            raise ValueError(f"Season {season} not found in the data")
        df_season = df[df['season'] == season]
        top_batsmen = (
            df_season.groupby('batter')['batsman_runs'].sum()
            .sort_values(ascending=False).head(n).reset_index()
        )
        top_batsmen['season'] = season
        return top_batsmen
    else:
        all_seasons = []
        for yr in sorted(df['season'].unique()):
            df_yr = df[df['season'] == yr]
            top_batsmen = (
                df_yr.groupby('batter')['batsman_runs'].sum()
                .sort_values(ascending=False).head(n).reset_index()
            )
            top_batsmen['season'] = yr
            all_seasons.append(top_batsmen)
        return pd.concat(all_seasons, ignore_index=True)


def plot_top_batsmen(df, season='all', n=10):
    """
    Plots top batsmen for either a single season or all seasons.
    """
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Get data
    top_batsmen = get_top_batsmen(df, season, n)

    if season != 'all':
        # Plot for single season
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_batsmen, x='batter', y='batsman_runs', palette='Blues_d')
        plt.title(f"Top {n} Batsmen in Season {season}")
        plt.xlabel("Batsman")
        plt.ylabel("Runs")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        # Plot for all seasons using FacetGrid
        g = sns.FacetGrid(top_batsmen, col="season", col_wrap=4, height=4, sharex=False, sharey=False)
        g.map_dataframe(sns.barplot, x='batter', y='batsman_runs', hue='batter', palette='Blues_d', legend=False)
        g.set_titles("Season {col_name}")
        g.set_axis_labels("Batsman", "Runs")

        for ax in g.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(45)

        plt.tight_layout()
        plt.show()
