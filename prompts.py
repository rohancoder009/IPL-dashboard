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
def generate_player_summary_prompt(df, player_name, start_year=None, end_year=None):
    summary_df = an.player_analysis(df, player_name, start_year, end_year)
    if summary_df.empty:
        return None

    stats = summary_df.iloc[0].to_dict()

    prompt = (
        f"Generate a performance summary for the IPL player {stats['Player']} "
        f"from {stats['From']} to {stats['To']}:\n"
        f"- Matches Played: {stats['Matches']}\n"
        f"- Total Runs: {stats['Runs']}\n"
        f"- Average: {stats['Average']}\n"
        f"- Strike Rate: {stats['Strike Rate']}\n"
        f"- 50s: {stats['50s']}\n"
        f"- 100s: {stats['100s']}\n"
        f"- 4s: {stats['4s']}\n"
        f"- 6s: {stats['6s']}\n"
        f"Write a short paragraph highlighting this performance."
    )
    return prompt


# Top Batsman Prompt
def genrate_top_batsman_prompt(season, n=10):
    return f"Generate a summary of top {n} batsmen of IPL {season}. Mention their consistency, performance, and key achievements."


# Batsman Growth Prompt
def genrate_growth_of_batsman(player_name):
    return f"Describe the performance growth of {player_name} across all IPL seasons based on runs scored. Highlight key years of improvement or drop."


# Bowler Performance Prompt
def genrate_bowler(player_name, start_year, end_year):
    return (
        f"Summarize the performance of bowler {player_name} from IPL {start_year} to {end_year}. "
        f"Include number of matches, wickets, economy, strike rate, average, and key contributions."
    )


# Bowler Comparison Prompt
def genrate_bowler_comparison_prompt(bowler1, bowler2, start, end):
    return (
        f"Compare the IPL performance of {bowler1} and {bowler2} from {start} to {end}. "
        f"Evaluate based on matches, wickets, economy, average, strike rate, and highlight who performed better."
    )


# Economy Bowler Prompt
def genrate_economy_summary_prompt(bowler_name, economy_rate, team_name):
    return (
        f"In team {team_name}, {bowler_name} had the best economy rate of {round(economy_rate, 2)} in the IPL. "
        f"Explain what makes this performance significant and how it could impact the team's bowling strategy."
    )

