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
            st.dataframe(result_df)
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
                st.dataframe(comparison_df)

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
            st.dataframe(team_solo)
        if st.button("Show Opponent Record"):
            st.dataframe(team_vs_opponent)

    with tab5:
        team_for_runs = st.selectbox("Select Team", all_teams)
        highest_scores_df = an.highest_scores_by_team(df, team_for_runs)
        if st.button("Show Highest Scores"):
            st.dataframe(highest_scores_df)
        if st.button("Visualize Highest Scores"):
            fig = vv.plot_highest_run_by_team(df, team_for_runs)
            st.pyplot(fig)

    with tab6:
        team_for_chase = st.selectbox("Select Team", all_teams)
        highest_chase_df = an.highest_chase_by_team(df, team_for_chase)
        if st.button("Show Highest Chases"):
            st.dataframe(highest_chase_df)
        if st.button("Visualize Highest Chases"):
            fig = vv.plot_highest_chase_by_team(df, team_for_chase)
            st.pyplot(fig)

# Player Analysis Section
elif option == "Player Analysis":
    st.header("Player Performance Analysis")

    analysis_options = [
        "player_analysis",
        "top_batsmen_by_season",
        "batsman_growth_by_season",
        "compare_batsman_growth",
        "most_runs_by_IPL",
        "player_against_teams",
        "player_head_to_head",
        "most_strikerate_by_players",
        "most_six_by_player",
        "most_fours_by_player"
    ]

    selected_analysis = st.selectbox("Choose Analysis Type", analysis_options)

    if selected_analysis == "player_analysis":
        selected_player = st.selectbox("Select Player", sorted(players))
        start_year = st.selectbox("Start Year", years, index=0)
        end_year = st.selectbox("End Year", years, index=len(years)-1)

        if st.button("Show Player Stats"):
            st.session_state.player_stats = an.player_analysis(df, selected_player, start_year, end_year)

        if "player_stats" in st.session_state:
            st.subheader(f"Performance of {selected_player}")
            st.dataframe(st.session_state.player_stats)

            if st.button("Summarize Performance"):
                prompt = pm.generate_player_summary_prompt(df, selected_player, start_year, end_year)
                if prompt:
                    summary = ai.summarize_stats(prompt)
                    st.markdown("Summary")
                    st.success(summary)

    if selected_analysis == "top_batsmen_by_season":
        season_choice = st.selectbox("Select Season", ["All"] + years)
        top_n = st.number_input("Number of Players", 1, 10, 5)
        selected_season = "all" if season_choice == "All" else season_choice

        if st.button("Show Top Batsmen"):
            top_batsman_df = an.top_batsmen_by_season(df, season=selected_season, n=top_n)
            st.dataframe(top_batsman_df)

        if st.button("Summarize Top Batsmen"):
            prompt = pm.genrate_top_batsman_prompt(season_choice, top_n)
            summary = ai.summarize_stats(prompt)
            st.markdown("Summary")
            st.success(summary)

        if st.button("Visualize Top Batsmen"):
            fig = vv.top_batsmen_by_season(df, selected_season, top_n)
            st.pyplot(fig)

    if selected_analysis == "batsman_growth_by_season":
        growth_player = st.selectbox("Select Player", sorted(players))
        if st.button("Show Growth"):
            growth_df = an.batsman_growth_by_season(df, growth_player)
            st.dataframe(growth_df)
        if st.button("Visualize Growth"):
            fig = vv.plot_growth_of_batsman_overtime(df, growth_player)
            st.pyplot(fig)

    if selected_analysis == "compare_batsman_growth":
        player1 = st.selectbox("Player 1", sorted(players))
        player2 = st.selectbox("Player 2", sorted(players))
        if player1 != player2:
            if st.button("Compare"):
                compare_df = an.compare_batsman_growth(df, player1, player2)
                st.dataframe(compare_df)
            if st.button("Visualize Comparison"):
                fig = vv.compare_growth(df, player1, player2)
                st.pyplot(fig)
        else:
            st.warning("Please select different players")

    if selected_analysis == "player_against_teams":
        pat_player = st.selectbox("Select Player", sorted(players))
        opponent_team = st.selectbox("Select Opponent Team", sorted(df['bowling_team'].unique()))
        if st.button("Show Performance vs Team"):
            pat_df = an.player_against_teams(df, pat_player, opponent_team)
            st.dataframe(pat_df)
        if st.button("Visualize vs Team"):
            fig = vv.plot_player_against_team(df, pat_player, opponent_team)
            st.pyplot(fig)

    if selected_analysis == "player_head_to_head":
        ph_player1 = st.selectbox("Player 1", sorted(players))
        ph_player2 = st.selectbox("Player 2", sorted(players))
        if ph_player1 != ph_player2:
            if st.button("Compare Head-to-Head"):
                h2h_df = an.player_head_to_head(df, ph_player1, ph_player2)
                st.dataframe(h2h_df)
            if st.button("Visualize Head-to-Head"):
                fig = vv.plot_player_head_to_head(df, ph_player1, ph_player2)
                st.pyplot(fig)
        else:
            st.warning("Please select different players")

    if selected_analysis == "most_runs_by_IPL":
        top_run_count = st.slider("Number of Players", 5, 20, 10)
        if st.button("Show Top Run Scorers"):
            runs_df = an.most_runs_by_IPL(df).head(top_run_count)
            st.dataframe(runs_df)
        if st.button("Visualize Runs"):
            fig = vv.top_runs_by_player(df, top_run_count)
            st.pyplot(fig)

    if selected_analysis == "most_strikerate_by_players":
        top_strike_n = st.slider("Number of Players", 5, 20, 10)
        min_balls = st.slider("Minimum Balls Faced", 30, 300, 100)
        if st.button("Show Strike Rates"):
            strike_df = an.most_strikerate_by_players(df, n=top_strike_n, min_balls=min_balls)
            st.dataframe(strike_df)
        if st.button("Visualize Strike Rates"):
            fig = vv.plot_most_Strike_rate_in_IPL(df, top_strike_n, min_balls)
            st.pyplot(fig)

    if selected_analysis == "most_six_by_player":
        six_count = st.slider("Number of Players", 5, 20, 10)
        if st.button("Show Most Sixes"):
            six_df = an.most_six_by_player(df, n=six_count)
            st.dataframe(six_df)
        if st.button("Visualize Sixes"):
            fig = vv.plot_most_six_in_IPL(df, six_count)
            st.pyplot(fig)

    if selected_analysis == "most_fours_by_player":
        four_count = st.slider("Number of Players", 5, 20, 10)
        if st.button("Show Most Fours"):
            four_df = an.most_fours_by_player(df, n=four_count)
            st.dataframe(four_df)
        if st.button("Visualize Fours"):
            fig = vv.plot_most_four_in_IPL(df, four_count)
            st.pyplot(fig)

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
                st.dataframe(bowler_df)
                st.session_state.bowler_record_df = bowler_df
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
                st.dataframe(h2h_df)
                st.session_state.bowler_h2h_df = h2h_df
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

    # ---------------- Economy Rate ----------------
    with tab3:
        econ_team = st.selectbox("Select Bowling Team", all_bowling_teams)
        if st.button("Show Best Economy Bowler"):
            econ_df = an.economy_rate(df, econ_team)
            st.dataframe(econ_df)

            if st.button("Summarize Economy Bowler"):
                bowler_name = econ_df.index[0]
                eco = round(econ_df.iloc[0], 2)
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
