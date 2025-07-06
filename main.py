# main.py
from data_loader import load_ipl,load_matches
from analysis import *
import visualize as vv
import pandas as pd
# def normalize_columns(df):
#     cols_to_normalize = ['team1', 'team2', 'winner', 'toss_winner', 'batter', 'player_dismissed']
#     for col in cols_to_normalize:
#         df[col] = df[col].astype(str).str.strip().str.lower()
#     return df

df = load_ipl()
# result = player_analysis(df, 'V Kohli', 2018, 2023)
match_stats=head_to_head(df,'Chennai Super Kings','Mumbai Indians',2008,2023)
#print(pd.DataFrame([result]))
print(pd.DataFrame([match_stats]))
# df = normalize_columns(df)

# team_perf = team_season_performance(df,'Mumbai Indians')
# print(team_perf)
# print(df.columns.tolist())

# top_batsmen = top_batsmen_by_season(df,2018)
# vv.top_batsmen_by_season(df,'2018')
# print(top_batsmen)
mdf=load_matches()
# team_win=team_win_by_season(mdf)
# print(team_win)
# vv.plot_team_wins_season(mdf)

# team_r = team_record(mdf, 'Mumbai Indians')
# vv.plot_team_vs_opponents(team_r,'Mumbai Indians')
# vv.plot_win_percentage_against_Opponents(team_r,'Mumbai Indians')
#highest_scores = highest_scores_by_team(df,'Mumbai Indians')
# print(highest_scores)
# vv.plot_highest_run_by_team(df,'Mumbai Indians')
# highest_chase = highest_chase_by_team(df,'Mumbai Indians')
# print(highest_chase)
# vv.plot_highest_chase_by_team(df,'Mumbai Indians')

# vv.plot_growth_of_batsman_overtime(df,'v kohli')
# vv.compare_growth(df,'v kohli','ss iyer')
# df2=compare_batsman_growth(df,'v kohli','ss iyer')
# print(df2)
# vv.top_runs_by_player(df,10)

# df2=player_against_teams(df,'v kohli','Mumbai Indians')
# print(df2)
# vv.plot_player_against_team(df,'v kohli','Mumbai Indians') 
# df2=player_head_to_head(df,'v kohli','ra jadeja')
# print(df2)
# vv.plot_player_head_to_head(df,'v kohli','ra jadeja')
# df2 = most_fours_by_player(df)
# print(df2)
# vv.plot_most_six_in_IPL(df)
# vv.plot_most_four_in_IPL(df)
# print(bowler_record(df, 'GJ Maxwell', end_year=2023))

# vv.plot_bowler_headtohead(df, 'GJ Maxwell','MR Marsh')