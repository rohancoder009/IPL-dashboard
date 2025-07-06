import pandas as pd
import numpy as np

# ----------------------------------------------
#  BATTER FUNCTIONS
# ----------------------------------------------

def player_analysis(df, player_name, start_year=None, end_year=None):
    """
    Analyzes a player's batting performance across selected seasons.
    Returns matches played, total runs, average, strike rate, 50s, 100s.
    """
    if df.empty or 'batter' not in df.columns:
        return pd.DataFrame()

    min_year = df['season'].min()
    max_year = df['season'].max()

    if start_year is None:
        start_year = min_year
    if end_year is None:
        end_year = max_year

    # Ensure year bounds are valid
    if start_year < min_year or end_year > max_year:
        raise ValueError(f"Invalid year input. Data available from {min_year} to {max_year}")

    df = df[(df['season'] >= start_year) & (df['season'] <= end_year)]

    # Early exit if player is not in filtered data
    if player_name not in df['batter'].unique():
        return pd.DataFrame()

    player_df = df[df['batter'] == player_name]

    if player_df.empty:
        return pd.DataFrame()

    # Safe handling of outs
    dismissed_mask = player_df['player_dismissed'] == player_name
    outs = dismissed_mask.sum()

    total_runs = player_df['batsman_runs'].sum()
    balls_faced = player_df.shape[0]
    matches = player_df['match_id'].nunique()

    fours = (player_df['batsman_runs'] == 4).sum()
    sixes = (player_df['batsman_runs'] == 6).sum()

    avg = round(total_runs / outs, 2) if outs > 0 else 'NA'
    sr = round((total_runs / balls_faced) * 100, 2) if balls_faced > 0 else 0

    matchwise = player_df.groupby('match_id')['batsman_runs'].sum()
    fifties = matchwise[(matchwise >= 50) & (matchwise < 100)].count()
    hundreds = matchwise[matchwise >= 100].count()

    summary = {
        'Player': player_name,
        'Matches': matches,
        'Runs': total_runs,
        'Average': avg,
        'Strike Rate': sr,
        '50s': fifties,
        '100s': hundreds,
        'From': start_year,
        'To': end_year,
        '6s': sixes,
        '4s': fours
    }

    return pd.DataFrame([summary])


def top_batsmen_by_season(df, season='all',n=10):
    """
    Returns top n run-scorers for a given season or for full IPL .
    """
    if season!= 'all':
        season = int(season)
        if season not in df['season'].unique():
            raise ValueError (f"season {season} not found in the data")
        df = df[df['season'] == season]
        top_batsman = df.groupby('batter')['batsman_runs'].sum()
        top_batsman = top_batsman.sort_values(ascending=False).head(n)
        # top_batsman['season']=season
        return top_batsman.reset_index()
    else:
        all_season_stats = []
        for year in sorted(df['season'].unique()):
            df_season=df[df['season']==year]
            top_batsman=(
                df_season.groupby('batter')['batsman_runs'].sum()
                .sort_values(ascending = False)
                .head(n)
                .reset_index()
            )
            top_batsman['season']=year
            all_season_stats.append(top_batsman)
        return pd.concat(all_season_stats,ignore_index=True)

def batsman_growth_by_season(df,player_name):
    if player_name not in df['batter'].unique():
        raise ValueError(f"player {player_name} not found in data")
    df_player = df[df['batter']==player_name]
    result=[]
    for season in sorted(df['season'].unique()):
        season_df=df_player[df_player['season']==season]
        runs=season_df['batsman_runs'].sum()
        balls=season_df.shape[0]
        outs = season_df[season_df['player_dismissed']==player_name].shape[0]
        matches = season_df['match_id'].nunique()
        fours = df_player[df_player['batsman_runs']==4].shape[0]
        sixes= df_player[df_player['batsman_runs']==6].shape[0]
        strike_rate=round((runs/balls)*100,2) if balls else 0
        avg = round(runs/outs,2) if outs else 'NA'
        
        matchwise_runs=season_df.groupby('match_id')['batsman_runs'].sum()
        fifties = matchwise_runs[(matchwise_runs>= 50 )&(matchwise_runs<100)].count()
        hundreds= matchwise_runs[(matchwise_runs >= 100)].count()
        result.append({
            'player':player_name,
            'Season': season,
            'Runs': runs,
            'Matches': matches,
            'Average': avg,
            'Strike Rate': strike_rate,
            '50s': fifties,
            '100s': hundreds,
            '4s': fours,
            '6s':sixes,
        })
    return pd.DataFrame(result)
def compare_batsman_growth(df,player1,player2):
    df1= batsman_growth_by_season(df,player1)
    df2= batsman_growth_by_season(df,player2)
    return pd.concat([df1,df2],ignore_index=True)

def most_runs_by_IPL(df, n=10):
    runs=df.groupby('batter')['batsman_runs'].sum().sort_values(ascending = False).head(n)
    return runs.reset_index().rename(columns={'batter':'player','batsman_runs':'player_runs'})
def player_against_teams(df,player_name,team_name,season='all'):
    if player_name not in df['batter'].unique():
        raise ValueError(f'Player "{player_name}" not found in data')

    if team_name not in df['bowling_team'].unique():
        raise ValueError(f'Team "{team_name}" not found in data')

    data = df[(df['batter'] == player_name) & (df['bowling_team'] == team_name)]

    if season != 'all':
        season = int(season)
        if season not in df['season'].unique():
            raise ValueError(f'Season {season} not found in data')
        data = data[data['season'] == season]

    if data.empty:
        return f"No data found for {player_name} vs {team_name} in season {season}"

    total_runs = data['batsman_runs'].sum()
    balls_faced = data.shape[0]
    outs = data[data['player_dismissed'] == player_name].shape[0]
    sr = (total_runs / balls_faced) * 100 if balls_faced else 0
    fours = data[data['batsman_runs'] == 4].shape[0]
    sixes = data[data['batsman_runs'] == 6].shape[0]

    result = {
        'Player': player_name,
        'Against Team': team_name,
        'Season': season,
        'Total Runs': total_runs,
        'Balls Faced': balls_faced,
        'Dismissals': outs,
        'Strike Rate': round(sr, 2),
        'Fours': fours,
        'Sixes': sixes,
    }

    return pd.DataFrame([result])

def player_head_to_head(df,player1,player2,start_year=None , end_year=None):
    df1=player_analysis(df,player1)
    df2=player_analysis(df,player2)
    return pd.concat([df1,df2],ignore_index=True)    
def most_strikerate_by_players(df, n =10, min_balls= 100):
    runs = df.groupby('batter')['batsman_runs'].sum()
    balls = df.groupby('batter').size()
    strike_rate_df=pd.DataFrame({
        'Runs':runs,
        'Balls Faced':balls
    })
    strike_rate_df = strike_rate_df[strike_rate_df['Balls Faced']>=min_balls]
    strike_rate_df['Strike Rate']=(strike_rate_df['Runs']/strike_rate_df['Balls Faced'])*100
    strike_rate_df['Strike Rate'] = strike_rate_df['Strike Rate'].round(2)
    return strike_rate_df.sort_values(by='Strike Rate',ascending= False).head(n)
def most_six_by_player(df,n=10):
    sixes =df[df['batsman_runs']==6]
    six_count = sixes.groupby('batter').size().sort_values(ascending = False)
    
    return six_count.head(n).reset_index(name='sixes')
def most_fours_by_player(df,n=10):
    fours =df[df['batsman_runs']==4]
    fours_count = fours.groupby('batter').size().sort_values(ascending = False)
    
    return fours_count.head(n).reset_index(name='fours')

# ----------------------------------------------
#  BOWLER FUNCTIONS
# ---------------------------------------`-------
def bowler_record(df,bowler_name,start_year =None,end_year = None):
    if bowler_name not in df['bowler'].unique():
        raise ValueError(f"bowler {bowler_name} not in the data ")
    min_year= df['season'].min()
    max_year= df['season'].max()
    start_year = start_year if start_year else min_year
    end_year = end_year if end_year else max_year
    df_bowler = df[(df['bowler']==bowler_name)&
                   (df['season']>= start_year)&
                   (df['season']<= end_year)]
    ball_bowled = df_bowler.shape[0]
    run_conceded = df_bowler['total_runs'].sum()
    wickets = df_bowler[df_bowler['player_dismissed'].notna()].shape[0]
    matches = df_bowler['match_id'].nunique()
    
    avg = round(run_conceded/wickets,2) if wickets else 'NA'
    eco = round((run_conceded/ball_bowled)*6,2) if ball_bowled else 0
    sr = round(ball_bowled/wickets,2) if wickets else 'NA'
    
    dot_balls = df_bowler[df_bowler['total_runs']==0].shape[0]
    fours = df_bowler[df_bowler['batsman_runs']==4].shape[0]
    sixes = df_bowler[df_bowler['batsman_runs']==6].shape[0]
    
    return pd.DataFrame([{
        'Bowler': bowler_name,
        'Matches': matches,
        'Balls Bowled': ball_bowled,
        'Runs': run_conceded,
        'Wickets': wickets,
        'Average': avg,
        'Economy': eco,
        'Strike Rate': sr,
        'Dots': dot_balls,
        'Fours': fours,
        'Sixes': sixes,
        'From': start_year,
        'To': end_year
    }]) 
def bowler_headtohead(df,player1,player2,start_year,end_year):
    df1=bowler_record(df,player1,start_year,end_year)
    df2=bowler_record(df,player2,start_year,end_year)
    return pd.concat([df1,df2],ignore_index= True)

    
def economy_rate(df, team_name):
    """
    Returns the bowler with the lowest economy rate (minimum 50 balls bowled) from a given team.
    """
    df = df[df['bowling_team'] == team_name]
    total_runs = df.groupby('bowler')['total_runs'].sum()
    total_balls = df.groupby('bowler')['iswicket'].count()

    valid_bowlers = total_balls[total_balls >= 50]
    economy_rate = total_runs[valid_bowlers.index] / (valid_bowlers / 6)

    best_bowler = economy_rate.sort_values().head(1)
    return best_bowler

#4 bowler 
# ----------------------------------------------
#  TEAM FUNCTIONS
# ----------------------------------------------

def head_to_head(df, team1, team2, start_year=None, end_year=None):
    """
    Returns head-to-head stats between two teams including wins, tosses, ties, etc.
    """
    min_year = df['season'].min()
    max_year = df['season'].max()
    if start_year is None:
        start_year = min_year
    if end_year is None:
        end_year = max_year
    if start_year < min_year or end_year > max_year:
        raise ValueError(f"Invalid year input. Data available from {min_year} to {max_year}")

    team1 = team1.strip().lower()
    team2 = team2.strip().lower()

    df = df[(df['season'] >= start_year) & (df['season'] <= end_year)]
    h2h_df = df[
        ((df['team1'].str.lower() == team1) & (df['team2'].str.lower() == team2)) |
        ((df['team2'].str.lower() == team1) & (df['team1'].str.lower() == team2))
    ]

    if h2h_df.empty:
        raise ValueError(f"No matches found between {team1} and {team2}")

    total_matches = h2h_df.shape[0]

    win_counts = h2h_df['winner'].str.lower().value_counts()
    team1_wins = win_counts.get(team1, 0)
    team2_wins = win_counts.get(team2, 0)
    ties_cancelled = total_matches - (team1_wins + team2_wins)

    toss_counts = h2h_df['toss_winner'].str.lower().value_counts()
    team1_toss = toss_counts.get(team1, 0)
    team2_toss = toss_counts.get(team2, 0)

    return {
        'Total Matches': total_matches,
        f'{team1.title()} Wins': team1_wins,
        f'{team2.title()} Wins': team2_wins,
        'Ties/No Results': ties_cancelled,
        f'{team1.title()} Toss Wins': team1_toss,
        f'{team2.title()} Toss Wins': team2_toss
    }


def team_season_performance(df, team_name):
    """
    Returns per-season stats for a team: matches played, matches won, and win percentage.
    """
    # Standardize relevant columns
    columns_to_clean = ['team1', 'team2', 'winner', 'toss_winner', 'batter', 'player_dismissed']
    for col in columns_to_clean:
      df.loc[:, col] = df[col].astype(str).str.lower().str.strip()

    team_name = team_name.strip().lower()
    df['season'] = df['season'].astype(int)

    if team_name not in df['team1'].unique() and team_name not in df['team2'].unique():
        raise ValueError(f"No match data found for team '{team_name}'")

    team_matches = df[(df['team1'] == team_name) | (df['team2'] == team_name)]

    matches_per_season = team_matches.groupby('season')['id'].count()
    wins_per_season = team_matches[team_matches['winner'] == team_name].groupby('season')['id'].count()

    result_df = pd.DataFrame({
        'Matches Played': matches_per_season,
        'Matches Won': wins_per_season
    })

    result_df['Matches Won'] = result_df['Matches Won'].fillna(0).astype(int)
    result_df['win %'] = (result_df['Matches Won'] / result_df['Matches Played'].replace(0, float('nan')) * 100).round(2)

    return result_df

def parse_team_record_to_df(team_dict):
    team_name= list(team_dict.keys())[0]
    overall_stats=team_dict[team_name]['Overall']
    opponent_stats=team_dict[team_name]['Against Opponents']
    overall_df=pd.DataFrame([overall_stats])
    overall_df.insert(0,'Team',team_name)
    
    vs_opponents=pd.DataFrame(opponent_stats).T.reset_index()
    vs_opponents.rename(columns={'index':'opponent'},inplace=True)
    vs_opponents.insert(0,'Team',team_name)
    return overall_df,vs_opponents
def team_win_by_season(df):
    """
    Returns pivot table: each team’s number of wins across all seasons.
    """
    win_counts = df.groupby(['season', 'winner']).size().reset_index(name='wins')
    pivot = win_counts.pivot(index='winner', columns='season', values='wins').fillna(0)
    return pivot
def team_record(df, team):
    team = team.strip().lower()

    # Filter only those matches where the team participated
    temp_df = df[(df['team1'].str.lower() == team) | (df['team2'].str.lower() == team)].copy()

    # Basic stats
    total_matches = temp_df.shape[0]
    total_wins = (temp_df['winner'].str.lower() == team).sum()
    total_draws = temp_df['winner'].isnull().sum()
    total_loss = ((temp_df['winner'].str.lower() != team) & temp_df['winner'].notna()).sum()
    win_percentage = (total_wins / total_matches) * 100 if total_matches > 0 else 0

    # Titles won: assuming a column named 'match_type' marks 'Final'
    if 'match_type' in temp_df.columns:
        titles_won = temp_df[(temp_df['winner'].str.lower() == team) & 
                             (temp_df['match_type'].str.lower() == 'final')].shape[0]
    else:
        titles_won = 'Data Not Available'

    # Unique opponent teams
    opponents = pd.concat([temp_df['team1'], temp_df['team2']]).str.lower().unique()

    # Dictionary to store per-opponent stats
    opponent_stats = {}

    for opp in opponents:
        if opp != team:
            # Matches against that opponent
            opp_df = temp_df[(temp_df['team1'].str.lower() == opp) | 
                             (temp_df['team2'].str.lower() == opp)]
            total_vs = opp_df.shape[0]
            won_vs = (opp_df['winner'].str.lower() == team).sum()
            lost_vs = (opp_df['winner'].str.lower() == opp).sum()
            draw_vs = opp_df['winner'].isnull().sum()
            win_perc_vs = (won_vs / total_vs) * 100 if total_vs > 0 else 0

            opponent_stats[opp.title()] = {
                'Matches': total_vs,
                'Wins': won_vs,
                'Losses': lost_vs,
                'Draws': draw_vs,
                'Win %': round(win_perc_vs, 2)
            }

    # Final structured dictionary output
    result= {
        team.title(): {
            'Overall': {
                'Matches Played': total_matches,
                'Wins': total_wins,
                'Losses': total_loss,
                'Draws': total_draws,
                'Win %': round(win_percentage, 2),
                'Titles Won': titles_won
            },
            'Against Opponents': opponent_stats
        }
    }
    team_solo,team_opp=parse_team_record_to_df(result)
    return team_solo,team_opp
    
    

def highest_scores_by_team(df,team_name,n=5):
    team_df=df[df['batting_team']==team_name]
    if team_df.empty:
        raise ValueError(f"team {team_name} not in data ")
    scores = (team_df.groupby(['match_id','season','venue','bowling_team'])['total_runs'].sum()
        .reset_index()
        .sort_values(by='total_runs',ascending=False)
        .head(n)           
    )    
    scores.rename(columns={'total_runs':'score','bowling_team':'Against'},inplace=True)
    return scores
def highest_chase_by_team(df,team_name,n=5):
    team_df=df[df['bowling_team']==team_name]
    if team_df.empty:
        raise ValueError(f"team {team_name} not in data ")
    chase =(team_df.groupby(['match_id','season','venue','batting_team'])['total_runs'].sum()
            .reset_index()
            .sort_values(by='total_runs',ascending=False)
            .head(n)
        )
    chase.rename(columns={'total_runs':'score','batting_team':'Against'},inplace=True)
    return chase
