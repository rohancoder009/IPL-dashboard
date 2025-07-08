import  streamlit as st
import data_loader as dl
import analysis as an
import visualize as vv
import pandas as pd
import llmutil as ai
def load_data():
    return dl.load_ipl()

df = load_data()


# Player Summary Prompt

# ---------------- Player Prompts ----------------
def generate_player_summary_prompt(df, player_name, start_year=None, end_year=None):
    from analysis import player_analysis
    summary_df = player_analysis(df, player_name, start_year, end_year)
    if summary_df.empty:
        return None
    stats = summary_df.iloc[0].to_dict()
    prompt = (
        f"Summarize the IPL batting performance of {stats['Player']} from {stats['From']} to {stats['To']}:\n"
        f"- Matches: {stats['Matches']}\n"
        f"- Runs: {stats['Runs']}\n"
        f"- Average: {stats['Average']}\n"
        f"- Strike Rate: {stats['Strike Rate']}\n"
        f"- 50s: {stats['50s']}\n"
        f"- 100s: {stats['100s']}\n"
        f"- 4s: {stats['4s']}\n"
        f"- 6s: {stats['6s']}\n"
        f"Write a short 3-4 line paragraph summarizing the player's performance."
    )
    return prompt

def genrate_top_batsman_prompt(season, n=10):
    return f"Summarize the top {n} batsmen of IPL season {season}. Highlight their performance and key stats."

def genrate_growth_of_batsman(player_name):
    return f"Summarize the performance growth of IPL player {player_name} across seasons based on runs scored."

# ---------------- Bowler Prompts ----------------
def genrate_bowler(player_name, start_year, end_year):
    return f"Summarize the bowling performance of {player_name} in IPL from {start_year} to {end_year}. Include wickets, economy, strike rate, and match count."

def genrate_bowler_comparison_prompt(bowler1, bowler2, start_year, end_year):
    return f"Compare the IPL bowling performance of {bowler1} and {bowler2} from {start_year} to {end_year}. Mention who performed better in wickets, economy, matches."

def genrate_economy_summary_prompt(bowler_name, economy, team_name):
    return f"{bowler_name} has the best economy rate ({economy}) for {team_name} in IPL. Summarize their performance and effectiveness in limiting runs."

# ---------------- Team Prompts ----------------
def genrate_team_season_summary_prompt(team_name, df):
    wins = df["Wins"].sum() if "Wins" in df.columns else "N/A"
    years = df["Season"].tolist() if "Season" in df.columns else []
    return (
        f"Summarize the season-wise IPL performance of {team_name} across years {years}. "
        f"Total wins: {wins if wins != 'N/A' else 'unknown'}. Highlight performance trends."
    )

def genrate_head_to_head_summary_prompt(team1, team2, df):
    matches = df["Matches"].sum() if "Matches" in df.columns else "N/A"
    return (
        f"Summarize the IPL head-to-head performance between {team1} and {team2}. "
        f"Total matches: {matches}. Highlight which team dominated overall and in recent years."
    )

def genrate_team_record_summary_prompt(team_name, df):
    opponents = df["Opponent"].tolist() if "Opponent" in df.columns else []
    return (
        f"Summarize the IPL record of {team_name} against opponents like {', '.join(opponents[:5])}. "
        f"Highlight major wins, struggles, and any trends."
    )

def genrate_highest_scores_prompt(team_name, df):
    top_score = df["Score"].max() if "Score" in df.columns else "N/A"
    return (
        f"Summarize the highest IPL scores made by {team_name}. "
        f"Their top score is {top_score}. Mention how often they scored over 180+ runs."
    )

def genrate_highest_chases_prompt(team_name, df):
    chases = df["Chased"].tolist() if "Chased" in df.columns else []
    return (
        f"Summarize the successful IPL run chases by {team_name}. "
        f"Mention their biggest chases and consistency in chasing high totals."
    )
