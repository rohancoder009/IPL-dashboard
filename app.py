import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

import data_loader as dl
import analysis as an
import visualize as vv
import llmutil as ai
import prompts as pm


# --------------------------------------------------
# Title & API Setup
# --------------------------------------------------
st.title("🏏 IPL Data Analysis Dashboard")
st.write("Welcome to the IPL Analysis UI built with Streamlit")

load_dotenv()
api_key = st.secrets.get("API_KEY", os.getenv("API_KEY"))

if not api_key:
    st.error("API key not found. Please set it in .env or secrets.toml")
else:
    ai.setup_gemini(api_key)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return dl.load_ipl()

df = load_data()

# --------------------------------------------------
# Sidebar Menu
# --------------------------------------------------
st.sidebar.title("🏏 IPL Dashboard Menu")
option = st.sidebar.selectbox("Choose Analysis Type", [
    "Team Analysis", 
    "Player Analysis", 
    "Bowler Analysis"
])

players = pd.unique(pd.concat([
        df['batter'], df['bowler'], df['player_dismissed']
        ]).dropna())

years = sorted(df['season'].unique())
# --------------------------------------------------
# Team Analysis
# --------------------------------------------------
if option == "Team Analysis":
    st.header("Team Analysis")

    teams = sorted(df['batting_team'].unique())
    

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Team Season Performance", 
        "Head to Head", 
        "Team Wins by Season", 
        "Team Record", 
        "Highest Scores", 
        "Highest Chases"
    ])

    with tab1:
        team_name = st.selectbox("Select Team", teams)
        result_df = an.team_season_performance(df, team_name)
        
        if st.button("Show"):
            st.dataframe(result_df)
        if st.button("Visualize"):
            fig = vv.plot_team_season_performance(df, team_name)
            st.pyplot(fig)

    with tab2:
        team1 = st.selectbox("Team 1", teams)
        team2 = st.selectbox("Team 2", teams)
        start_year = st.selectbox("Start Year", years, index=0)
        end_year = st.selectbox("End Year", years, index=len(years)-1)

        if st.button("Compare"):
            if team1 == team2:
                st.warning("Please select two different teams")
            else:
                result_df = an.head_to_head(df, team1, team2, start_year, end_year)
                st.subheader(f"{team1} vs {team2} from {start_year} to {end_year}")
                st.dataframe(result_df)

        if st.button("Visualize Head to Head"):
            if team1 != team2:
                fig = vv.plot_team_head_to_head(df, team1, team2, start_year, end_year)
                st.pyplot(fig)

    with tab3:
        teamname = st.selectbox("Select Team", teams)
        result_df = an.team_season_performance(df, teamname)

        if st.button("Show Data"):
            st.dataframe(result_df)
        if st.button("Visualize Team Performance"):
            fig = vv.plot_team_season_performance(df, teamname)
            st.pyplot(fig)

    with tab4:
        team_name_record = st.selectbox("Select Team", teams)
        team_record_solo, team_record_opponent = an.team_record(df, team_name_record)

        if st.button("Show Overall"):
            st.dataframe(team_record_solo)
        if st.button("Against Opponents"):
            st.dataframe(team_record_opponent)

    with tab5:
        team_nameruns = st.selectbox("Select Team", teams)
        highest_runs = an.highest_scores_by_team(df, team_nameruns)

        if st.button("Show Highest Scores"):
            st.dataframe(highest_runs)
        if st.button("Visualize Highest Scores"):
            fig = vv.plot_highest_run_by_team(df, team_nameruns)
            st.pyplot(fig)

    with tab6:
        team_namechase = st.selectbox("Select Team", teams)
        highest_chase = an.highest_chase_by_team(df, team_namechase)

        if st.button("Show Highest Chases"):
            st.dataframe(highest_chase)
        if st.button("Visualize Highest Chases"):
            fig = vv.plot_highest_chase_by_team(df, team_namechase)
            st.pyplot(fig)


# --------------------------------------------------
# Player Analysis
# --------------------------------------------------
elif option == "Player Analysis":
    st.header("Player Performance Analysis")

    list_ana = [
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

    ana_type = st.selectbox("What do you want to analyze?", list_ana)

    if ana_type == "player_analysis":
        
        selected_player = st.selectbox("Select a Player", sorted(players))
        years = sorted(df['season'].unique())
        start_year = st.selectbox("Start Year", years, index=0)
        end_year = st.selectbox("End Year", years, index=len(years) - 1)

    #  Store in session_state if not already
        if "player_data" not in st.session_state:
            st.session_state.player_data = pd.DataFrame()

    #  Show Stats Button
        if st.button("Show Stats"):
            st.session_state.player_data = an.player_analysis(df, selected_player, start_year, end_year)

    #  Display if available
        if not st.session_state.player_data.empty:
            st.subheader(f"Performance of {selected_player}")
            st.dataframe(st.session_state.player_data)

        #  Gemini Summary Button
            if st.button("Summarize Performance"):
                st.subheader("🔍 Prompt + Gemini Debug")

                try:
                    prompt = pm.generate_player_summary_prompt(df, selected_player, start_year, end_year)

                    if prompt:
                        summary = ai.summarize_stats(prompt)
                        st.markdown("###  Summary")
                        st.success(summary)
                    else:
                        st.warning("Prompt was empty or failed to generate.")

                except Exception as e:
                    st.error(f"🔥 Gemini Error: {e}")

    if ana_type == 'top_batsmen_by_season':
        years = ['All'] + sorted(df['season'].unique())
        season = st.selectbox("Select a season (select 'All' for overall)", years, key="season")
        number = st.number_input("Enter number of top batsmen", min_value=1, max_value=10, step=1, format="%d")
    
        if st.button("Show Top Batsmen"):
            selected_season = 'all' if season == 'All' else season
            st.session_state.top_batsman = an.top_batsmen_by_season(df, season=selected_season, n=number)
    
        if "top_batsman" in st.session_state and not st.session_state.top_batsman.empty:
            st.subheader(f"TOP {number} Batsmen for {'all seasons' if season == 'All' else f'season {season}'}")
            st.dataframe(st.session_state.top_batsman)

        if st.button("Summarize Top Batsmen"):
            st.subheader("Summarizing performance...")
            try:
                prompt = pm.genrate_top_batsman_prompt(season,number)
                if prompt:
                    summary = ai.summarize_stats(prompt)
                    st.markdown("### Summary")
                    st.success(summary)
                else:
                    st.warning("Prompt was empty or failed to generate.")
            except Exception as e:
                st.warning(f"Summary generation failed: {e}")
        
        if st.button("Visualize Top Batsmen"):
            fig = vv.top_batsmen_by_season(df, season if season != 'All' else 'all', number)
            st.pyplot(fig)
    
    
    if ana_type == "batsman_growth_by_season":
        player_growth = st.selectbox("Enter the player name",players,key="player_growth")
        
        if st.button("show growth"):
            st.session_state.growth_data = an.batsman_growth_by_season(df,player_growth)
            if not st.session_state.growth_data.empty:
                st.write(f"Growth of player {player_growth} ")
                st.dataframe(st.session_state.growth_data)
                if("show summary"):
                    prompt = pm.genrate_growth_of_batsman(player_growth)
                    if prompt:
                        st.write("summarizing")
                        summary = ai.summarize_stats(prompt)
                        st.markdown(" summary")
                        st.success(summary)
        
        if st.button("visualize growth "):
            fig = vv.plot_growth_of_batsman_overtime(df,player_growth)
            st.pyplot(fig)
        
    if ana_type == "compare_batsman_growth":
        player1 = st.selectbox("Select Player 1", sorted(players), key="cg1")
        player2 = st.selectbox("Select Player 2", sorted(players), key="cg2")

        if player1 == player2:
            st.warning("Please select two different players")
        elif st.button("Compare Growth"):
            result_df = an.compare_batsman_growth(df, player1, player2)
            st.subheader(f"Season-wise Run Comparison: {player1} vs {player2}")
            st.dataframe(result_df)

        if st.button("Visualize Growth"):
            fig = vv.compare_growth(df, player1, player2)
            st.pyplot(fig)

    if ana_type == "player_against_teams":
        player = st.selectbox("Select Player", sorted(players), key="pat1")
        teams = sorted(df['bowling_team'].unique())
        team = st.selectbox("Select Against Team", teams, key="pat2")

        if st.button("Show Performance"):
            result_df = an.player_against_teams(df, player, team)
            st.subheader(f"{player} vs {team}")
            st.dataframe(result_df)

        if st.button("Visualize vs Team"):
            fig = vv.plot_player_against_team(df, player, team)
            st.pyplot(fig)

    if ana_type == "player_head_to_head":
        player1 = st.selectbox("Player 1", sorted(players), key="ph1")
        player2 = st.selectbox("Player 2", sorted(players), key="ph2")

        if player1 == player2:
            st.warning("Please select two different players")
        elif st.button("Compare Head-to-Head"):
            result_df = an.player_head_to_head(df, player1, player2)
            st.subheader(f"{player1} vs {player2} Head-to-Head")
            st.dataframe(result_df)

        if st.button("Visualize Head-to-Head"):
            fig = vv.plot_player_head_to_head(df, player1, player2)
            st.pyplot(fig)
    
    
    if ana_type == "most_runs_by_IPL":
        number = st.slider("Select number of top run scorers", min_value=5, max_value=20, value=10)

        if st.button("Show Top Run Scorers"):
            result_df = an.most_runs_by_IPL(df).head(number)
            st.subheader(f"Top {number} Players by Total Runs in IPL")
            st.dataframe(result_df)

        if st.button("Visualize Top Run Scorers"):
            fig = vv.top_runs_by_player(df, number)
            st.pyplot(fig)
        if ana_type == "most_strikerate_by_players":
            number = st.slider("Number of top players", 5, 20, 10)
            min_balls = st.slider("Minimum balls faced", 30, 300, 100, step=10)

        if st.button("Show Top Strike Rates"):
            result_df = an.most_strikerate_by_players(df, n=number, min_balls=min_balls)
            st.subheader(f"Top {number} Players with Highest Strike Rates (Min {min_balls} Balls)")
            st.dataframe(result_df)

        if st.button("Visualize Strike Rate"):
            fig = vv.plot_most_Strike_rate_in_IPL
            st.pyplot(fig)
    
    
    if ana_type == "most_six_by_player":
        number = st.slider("Number of top players", 5, 20, 10)

        if st.button("Show Six Hitters"):
            result_df = an.most_six_by_player(df, n=number)
            st.subheader(f"Top {number} Players with Most Sixes in IPL")
            st.dataframe(result_df)

        if st.button("Visualize Sixes"):
            fig = vv.plot_most_six_in_IPL(df, number)
            st.pyplot(fig)

    if ana_type == "most_fours_by_player":
        number = st.slider("Number of top players", 5, 20, 10)

        if st.button("Show Four Hitters"):
            result_df = an.most_fours_by_player(df, n=number)
            st.subheader(f"Top {number} Players with Most Fours in IPL")
            st.dataframe(result_df)

        if st.button("Visualize Fours"):
            fig = vv.plot_most_four_in_IPL(df, number)
            st.pyplot(fig)




        

    
# --------------------------------------------------
# Bowler Analysis
# --------------------------------------------------
elif option == "Bowler Analysis":
    bowlers= df["bowler"].unique()
    st.header("Bowler Stats and Comparison")

    tab1, tab2, tab3= st.tabs([
        "bowler_record",
        "bowler_headtohead",
        "economy rate"])
    with tab1:
        bowler_name = st.selectbox("select the player name",bowlers,key="bowler_name")
        
        start_year = st.selectbox("Start Year", years, index=0)
        end_year = st.selectbox("End Year", years, index=len(years)-1)

        
        st.session_state.data_df = an.bowler_record(df,bowler_name,start_year,end_year)
        if st.button("show"):
            if not st.session_state.data_df.empty:
                st.subheader(f"Bowler{bowler_name} data ")
                st.dataframe(st.session_state.data_df)
            else:
                st.warning("no data for the bowler")
        if st.button("show summary"):
                prompt = pm.genrate_bowler(bowler_name,start_year,end_year)
                if prompt:
                    st.write("summarizing")
                    summary = ai.summarize_stats(prompt)
                    st.markdown(" summary")
                    st.success(summary)
                else :
                    st.warning("No prompt got")
        