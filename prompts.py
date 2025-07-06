import  streamlit as st
import data_loader as dl
import analysis as an
import visualize as vv
import pandas as pd
import llmutil as ai
def load_data():
    return dl.load_ipl()

df = load_data()


def generate_player_summary_prompt(df, player_name, start_year=None, end_year=None):
    summary_df = an.player_analysis(df, player_name, start_year, end_year)
    if summary_df.empty:
        return None  # Or return "No data available for player"

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

def genrate_top_batsman_prompt(season,n=10):
        return f"top {n}performers OF IPL {season} "


def genrate_growth_of_batsman(player_name):
        return f"growth of  {player_name} of all past  season to according to  Runs"
def genrate_bowler(player_name,start_year,end_year):
    return f" performance of bowler {player_name} from {start_year} to {end_year}"
