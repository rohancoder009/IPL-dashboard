import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

import data_loader as dl
import analysis as an
import visualize as vv
import llmutil as ai
import prompts as pm

# Title & API Setup
st.title("IPL Data Analysis Dashboard")
st.write("Welcome to the IPL Analysis UI built with Streamlit")

load_dotenv()
api_key = st.secrets.get("API_KEY", os.getenv("API_KEY"))

if not api_key:
    st.error("API key not found. Please set it in .env or secrets.toml")
else:
    ai.setup_gemini(api_key)

# Load Data
@st.cache_data
def load_data():
    return dl.load_ipl()

df = load_data()
players = pd.unique(pd.concat([df['batter'], df['bowler'], df['player_dismissed']]).dropna())
years = sorted(df['season'].unique())

# Sidebar Menu
st.sidebar.title("IPL Dashboard Menu")
option = st.sidebar.selectbox("Choose Analysis Type", [
    "Team Analysis", 
    "Player Analysis", 
    "Bowler Analysis"
])

# Team Analysis Section
if option == "Team Analysis":
    st.header("Team Analysis")
    all_teams = sorted(df['batting_team'].unique())

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Team Season Performance", 
        "Head to Head", 
        "Team Wins by Season", 
        "Team Record", 
        "Highest Scores", 
        "Highest Chases"
    ])

    with tab1:
        selected_team = st.selectbox("Select Team", all_teams)
        result_df = an.team_season_performance(df, selected_team)
        if st.button("Show Season Performance"):
            st.session_state.team_season_df = result_df
            st.dataframe(result_df)
        if "team_season_df" in st.session_state:
            if st.button("Summarize Team Season Performance"):
                prompt = pm.genrate_team_season_summary_prompt(selected_team, st.session_state.team_season_df)
                summary = ai.summarize_stats(prompt)
                st.markdown("Summary")
                st.success(summary)
        if st.button("Visualize Season Performance"):
            fig = vv.plot_team_season_performance(df, selected_team)
            st.pyplot(fig)

    with tab2:
        team1 = st.selectbox("Team 1", all_teams)
        team2 = st.selectbox("Team 2", all_teams)
        start = st.selectbox("Start Year", years, index=0)
        end = st.selectbox("End Year", years, index=len(years)-1)

        if st.button("Compare Teams"):
            if team1 == team2:
                st.warning("Please select two different teams")
            else:
                comparison_df = an.head_to_head(df, team1, team2, start, end)
                st.session_state.head_to_head_df = comparison_df
                st.dataframe(comparison_df)

        if "head_to_head_df" in st.session_state:
            if st.button("Summarize Head to Head"):
                prompt = pm.genrate_head_to_head_summary_prompt(team1, team2, st.session_state.head_to_head_df)
                summary = ai.summarize_stats(prompt)
                st.markdown("Summary")
                st.success(summary)

        if st.button("Visualize Head to Head"):
            if team1 != team2:
                fig = vv.plot_team_head_to_head(df, team1, team2, start, end)
                st.pyplot(fig)

    with tab3:
        wins_team = st.selectbox("Select Team", all_teams)
        wins_df = an.team_season_performance(df, wins_team)
        if st.button("Show Team Wins"):
            st.dataframe(wins_df)
        if st.button("Visualize Team Wins"):
            fig = vv.plot_team_season_performance(df, wins_team)
            st.pyplot(fig)

    with tab4:
        record_team = st.selectbox("Select Team", all_teams)
        team_solo, team_vs_opponent = an.team_record(df, record_team)
        if st.button("Show Team Record"):
            st.session_state.team_record_df = team_vs_opponent
            st.dataframe(team_solo)
        if st.button("Show Opponent Record"):
            st.dataframe(team_vs_opponent)
        if "team_record_df" in st.session_state:
            if st.button("Summarize Team Record"):
                prompt = pm.genrate_team_record_summary_prompt(record_team, st.session_state.team_record_df)
                summary = ai.summarize_stats(prompt)
                st.markdown("Summary")
                st.success(summary)

    with tab5:
        team_for_runs = st.selectbox("Select Team", all_teams)
        highest_scores_df = an.highest_scores_by_team(df, team_for_runs)
        if st.button("Show Highest Scores"):
            st.session_state.highest_scores_df = highest_scores_df
            st.dataframe(highest_scores_df)
        if st.button("Visualize Highest Scores"):
            fig = vv.plot_highest_run_by_team(df, team_for_runs)
            st.pyplot(fig)
        if "highest_scores_df" in st.session_state:
            if st.button("Summarize Highest Scores"):
                prompt = pm.genrate_highest_scores_prompt(team_for_runs, st.session_state.highest_scores_df)
                summary = ai.summarize_stats(prompt)
                st.markdown("Summary")
                st.success(summary)

    with tab6:
        team_for_chase = st.selectbox("Select Team", all_teams)
        highest_chase_df = an.highest_chase_by_team(df, team_for_chase)
        if st.button("Show Highest Chases"):
            st.session_state.highest_chase_df = highest_chase_df
            st.dataframe(highest_chase_df)
        if st.button("Visualize Highest Chases"):
            fig = vv.plot_highest_chase_by_team(df, team_for_chase)
            st.pyplot(fig)
        if "highest_chase_df" in st.session_state:
            if st.button("Summarize Highest Chases"):
                prompt = pm.genrate_highest_chases_prompt(team_for_chase, st.session_state.highest_chase_df)
                summary = ai.summarize_stats(prompt)
                st.markdown("Summary")
                st.success(summary)

# Player Analysis Section

# Bowler Analysis Section
elif option == "Bowler Analysis":
    st.header("Bowler Stats and Comparison")
    all_bowlers = sorted(df["bowler"].unique())
    all_bowling_teams = sorted(df['bowling_team'].unique())

    tab1, tab2, tab3 = st.tabs([
        "Bowler Record",
        "Head-to-Head Comparison",
        "Best Economy (By Team)"
    ])

    # ---------------- Bowler Record ----------------
    with tab1:
        selected_bowler = st.selectbox("Select Bowler", all_bowlers)
        start_yr = st.selectbox("Start Year", years, index=0)
        end_yr = st.selectbox("End Year", years, index=len(years) - 1)

        if st.button("Show Bowler Record"):
            try:
                bowler_df = an.bowler_record(df, selected_bowler, start_yr, end_yr)
                st.session_state.bowler_record_df = bowler_df
                st.dataframe(bowler_df)
            except Exception as e:
                st.warning(str(e))

        if "bowler_record_df" in st.session_state and not st.session_state.bowler_record_df.empty:
            if st.button("Summarize Bowler Stats"):
                prompt = pm.genrate_bowler(selected_bowler, start_yr, end_yr)
                if prompt:
                    summary = ai.summarize_stats(prompt)
                    st.markdown("Summary")
                    st.success(summary)
                else:
                    st.warning("Prompt was empty")

    # ---------------- Head-to-Head ----------------
    with tab2:
        bowler1 = st.selectbox("Bowler 1", all_bowlers, key="bow1")
        bowler2 = st.selectbox("Bowler 2", all_bowlers, key="bow2")
        h2h_start = st.selectbox("Start Year", years, index=0, key="head2head_start")
        h2h_end = st.selectbox("End Year", years, index=len(years) - 1, key="head2head_end")

        if bowler1 == bowler2:
            st.warning("Please select two different bowlers.")
        elif st.button("Compare Bowlers"):
            try:
                h2h_df = an.bowler_headtohead(df, bowler1, bowler2, h2h_start, h2h_end)
                st.session_state.bowler_h2h_df = h2h_df
                st.dataframe(h2h_df)
            except Exception as e:
                st.error(str(e))

        if "bowler_h2h_df" in st.session_state and not st.session_state.bowler_h2h_df.empty:
            if st.button("Summarize Comparison"):
                try:
                    prompt = pm.genrate_bowler_comparison_prompt(bowler1, bowler2, h2h_start, h2h_end)
                    if prompt:
                        summary = ai.summarize_stats(prompt)
                        st.markdown("Summary")
                        st.success(summary)
                    else:
                        st.warning("Prompt generation failed")
                except Exception as e:
                    st.warning(str(e))
        if st.button("visualize Head to head of bowler"):
            fig = vv.plot_bowler_headtohead(df,bowler1,bowler2,h2h_start,h2h_end)
            st.plotly_chart(fig, use_container_width=True)
    # ---------------- Economy Rate ----------------
    with tab3:
        econ_team = st.selectbox("Select Bowling Team", all_bowling_teams)
        if st.button("Show Best Economy Bowler"):
            econ_df = an.economy_rate(df, econ_team)
            st.session_state.economy_df = econ_df
            st.dataframe(econ_df)

        if "economy_df" in st.session_state:
            if st.button("Summarize Economy Bowler"):
                bowler_name = st.session_state.economy_df.index[0]
                eco = round(st.session_state.economy_df.iloc[0], 2)
                try:
                    prompt = pm.genrate_economy_summary_prompt(bowler_name, eco, econ_team)
                    if prompt:
                        summary = ai.summarize_stats(prompt)
                        st.markdown("Summary")
                        st.success(summary)
                    else:
                        st.warning("Prompt failed to generate.")
                except Exception as e:
                    st.error(str(e))
