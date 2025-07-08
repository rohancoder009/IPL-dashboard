import seaborn  as sns
import matplotlib.pyplot as plt
import analysis as an
import pandas as pd
import plotly.graph_objects as go
import numpy as np
def normalize_dataframe(df, exclude_cols=None):
    """
    Normalize numeric columns in the DataFrame between 0 and 1.
    
    Parameters:
    - df: DataFrame to normalize
    - exclude_cols: list of column names to exclude from normalization (e.g., ['Player', 'Team'])

    Returns:
    - A new DataFrame with normalized numeric columns
    """
    df_norm = df.copy()
    exclude_cols = exclude_cols if exclude_cols else []

    for col in df.columns:
        if col in exclude_cols or df[col].dtype == 'object':
            continue

        col_min = df[col].min()
        col_max = df[col].max()
        if col_max != col_min:
            df_norm[col] = (df[col] - col_min) / (col_max - col_min)
        else:
            df_norm[col] = 0  

    return df_norm
def top_batsmen_by_season(df,season='all',n=10):
    """
    Plots top batsmen for either a single season or all seasons.
    """
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Get data
    top_batsmen = an.top_batsmen_by_season(df, season)

    if season != 'all':
        # Plot for single season
        fig ,ax = plt.subplots(figsize=(12,8))
        sns.barplot(data=top_batsmen, x='batter', y='batsman_runs', palette='Blues_d')
        ax.set_title(f"Top {n} Batsmen in Season {season}")
        ax.set_xlabel("Batsman")
        ax.set_ylabel("Runs")
        ax.tick_params(axis='x',rotation = 45)
        fig.tight_layout()
        return fig
    else:
        # Plot for all seasons 
        g = sns.FacetGrid(top_batsmen, col="season", col_wrap=4, height=4, sharex=False, sharey=False)
        g.map_dataframe(sns.barplot, x='batter', y='batsman_runs', hue='batter', palette='Blues_d', legend=False)
        g.set_titles("Season {col_name}")
        g.set_axis_labels("Batsman", "Runs")

        for ax in g.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(45)

        g.tight_layout()
        return g
def plot_team_wins_season(df):
    win_mat = an.team_win_by_season(df)

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(win_mat, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)

    ax.set_title("Matches won by Team across Seasons", fontsize=16)
    ax.set_xlabel("Season")
    ax.set_ylabel("Team")
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)

    fig.tight_layout()
    return fig
def plot_team_vs_opponents(stats_dict,team_name):
    team_name = team_name.title()
    data = stats_dict[team_name]['Against Opponents']
    
    df = pd.DataFrame(data).T.reset_index().rename(columns={"index":'Opponent'})
    plt.figure(figsize=(12,6))
    
    sns.barplot(data=df.melt(id_vars='Opponent',value_vars=['Wins','Losses']),x='Opponent',y='value',hue='variable')
    plt.title(f"{team_name} - wins and losses Vs each opponent")
    plt.ylabel('Count')
    plt.xlabel('Opponent Teams')
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.show()  
def plot_win_percentage_against_Opponents(stats_dict, team_name):
    team_name=team_name.title()
    data = stats_dict[team_name]['Against Opponents']
    df = pd.DataFrame(data).T.reset_index().rename(columns={'index':'Opponent'})
    
    plt.figure(figsize=(10,5))
    sns.lineplot(data=df,x='Opponent',y='Win %',markers='o',color='g')
    plt.title(f"{team_name}-win percentage vs each opponent ")
    plt.ylabel('Win %')
    plt.xlabel('opponent teams')
    plt.xticks(rotation=85)
    plt.ylim(0,100)
    plt.tight_layout()
    plt.show()
def plot_highest_run_by_team(df,team_name,n=5):
    highest = an.highest_scores_by_team(df,team_name)
    fig , ax =plt.subplots(figsize=(12,8))
    
    sns.barplot(data=highest,x='Against',y='score')
    ax.set_title(f"{team_name}- highest score against opponents")
    ax.set_xlabel('teams')
    ax.set_ylabel('scores')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    fig.tight_layout()
    return fig
def plot_highest_chase_by_team(df,team_name,n=5):
    highest = an.highest_chase_by_team(df,team_name)
    plt.figure(figsize=(12,8))
    
    sns.barplot(data=highest,x='Against',y='score',palette='viridis')
    plt.title(f"{team_name}- highest score chase against opponents")
    plt.xlabel('teams')
    plt.ylabel('scores')
    plt.xticks(rotation =65)
    plt.tight_layout()
    plt.show()
def plot_growth_of_batsman_overtime(df, player_name):
    growth = an.batsman_growth_by_season(df,player_name)
    fig ,ax= plt.subplots(figsize=(12,8))
    sns.lineplot(data=growth,x='Season',y='Runs',markers='o',label='Runs')
    sns.lineplot(data=growth,x='Season',y='Strike Rate',markers='s',label='Strike Rate')
    ax.set_title(f"player {player_name} growth over season")
    ax.set_xlabel('sesaon ')
    ax.set_ylabel('scores')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


def compare_growth(df, player1, player2):
    growth = an.compare_batsman_growth(df, player1, player2)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.lineplot(data=growth, x='Season', y='Runs', hue='player', marker='o', ax=ax)
    ax.set_title(f"{player1} vs {player2} - Runs over Seasons")
    ax.set_xlabel("Season")
    ax.set_ylabel("Runs")
    ax.grid(True)
    fig.tight_layout()
    return fig

def top_runs_by_player(df, n=10):
    runs = an.most_runs_by_IPL(df)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='player', y='player_runs', data=runs.head(n), ax=ax)
    ax.set_title('Most Runs by Player in IPL')
    ax.set_xlabel('Player Name')
    ax.set_ylabel('Runs')
    plt.xticks(rotation=80)
    fig.tight_layout()
    return fig

def plot_player_against_team(df, player_name, team_name, season='all'):
    stats_df = an.player_against_teams(df, player_name, team_name)
    metrics = ['Total Runs', 'Balls Faced', 'Dismissals', 'Strike Rate', 'Fours', 'Sixes']
    values = [stats_df.at[0, metric] for metric in metrics]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(metrics, values, color='skyblue')
    ax.set_xlabel('Value')
    ax.set_title(f"{stats_df.at[0, 'Player']} vs {stats_df.at[0, 'Against Team']} ({stats_df.at[0, 'Season']})")

    for bar in bars:
        ax.text(bar.get_width(), bar.get_y() + 0.25, f'{bar.get_width():.1f}', va='center')

    fig.tight_layout()
    return fig

def plot_player_head_to_head(df, player1, player2, start_year=None, end_year=None):
    df_summary = an.player_head_to_head(df, player1, player2)
    categories = ['Runs', 'Average', '6s', '4s', '50s', '100s', 'Strike Rate']
    player1, player2 = df_summary['Player'].values
    values1 = [df_summary.iloc[0][cat] if df_summary.iloc[0][cat] != 'NA' else 0 for cat in categories]
    values2 = [df_summary.iloc[1][cat] if df_summary.iloc[1][cat] != 'NA' else 0 for cat in categories]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width / 2, values1, width, label=player1, color='steelblue')
    bars2 = ax.bar(x + width / 2, values2, width, label=player2, color='orange')

    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    ax.set_ylabel('Value')
    ax.set_title('Player Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()
    return fig
def plot_most_Strike_rate_in_IPL(df,n=10):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Player", y="Strike Rate", data=result_df, ax=ax, palette="viridis")
    ax.set_title("Top Strike Rates in IPL")
    ax.set_ylabel("Strike Rate")
    ax.set_xlabel("Player")
    plt.xticks(rotation=45)
    return fig
def plot_most_six_in_IPL(df, n=10):
    data = an.most_six_by_player(df, n)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='batter', y='sixes', data=data, ax=ax)
    ax.set_title('Most 6s by Player in IPL')
    ax.set_xlabel('Player Name')
    ax.set_ylabel('6s')
    ax.tick_params(axis='x', rotation=80)
    fig.tight_layout()
    return fig

def plot_most_four_in_IPL(df, n=10):
    data = an.most_fours_by_player(df, n)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='batter', y='fours', data=data, ax=ax)
    ax.set_title('Most 4s by Player in IPL')
    ax.set_xlabel('Player Name')
    ax.set_ylabel('4s')
    ax.tick_params(axis='x', rotation=80)
    fig.tight_layout()
    return fig

import plotly.graph_objects as go

def plot_bowler_headtohead(df, player1, player2, start_year=None, end_year=None):
    df = an.bowler_headtohead(df, player1, player2, start_year, end_year)
    df_copy = df.copy()
    df = normalize_dataframe(df)
    metrices = [col for col in df.columns if col != 'Bowler' and df[col].dtype != 'object']

    fig = go.Figure()

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for i, (_, row) in enumerate(df.iterrows()):
        values = [row[m] for m in metrices]
        values.append(values[0])  
        color = colors[i % len(colors)]  
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrices + [metrices[0]],
            fill='toself',
            name=row['Bowler'],
            line=dict(color=color),
            fillcolor=color,
            opacity=0.6
        ))

    fig.update_layout(
        title='Bowler vs Bowler – Normalized Radar Comparison',
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True
    )

    return fig

def plot_team_season_performance(df,teamname):
    result_df=an.team_season_performance(df,teamname)

    fig, ax = plt.subplots(figsize=(12, 8))  
    sns.lineplot(x='season', y='win %', data=result_df, ax=ax)
    ax.set_title("Team Performance Season-wise")
    ax.set_xlabel("Season / Years")
    ax.set_ylabel("Winning Rate")
    fig.tight_layout()

    return fig 
def plot_team_head_to_head(df,team_name1,team_name2,start_year=None,end_year=None):
    result=an.head_to_head(df,team_name1,team_name2,start_year,end_year)
    keys = [f'{team_name1.title()} Wins', f'{team_name2.title()} Wins']
    values = [result.get(keys[0], 0), result.get(keys[1], 0)]

    
    data = pd.DataFrame({
        'Team': keys,
        'Wins': values
    })
    
    fig , ax= plt.subplots(figsize=(12,8))
    sns.barplot(x='Team',y='Wins',data=data,ax=ax, palette='Set2')
    ax.set_title(f"{team_name1} Vs {team_name2} ")
    ax.set_xlabel("teams")
    ax.set_ylabel("Number of wins")
    ax.bar_label(ax.containers[0],fmt='%d')
    fig.tight_layout()
    return fig 
