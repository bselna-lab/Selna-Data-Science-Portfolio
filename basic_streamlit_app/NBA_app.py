import streamlit as st
import pandas as pd

df = pd.read_csv("NBA_app_data.csv")

st.title("🏀 NBA Player Stats Compared!")
st.subheader("By: Bridget Selna 💓")
st.write(
    "This app lets you explore and compare 2 NBA players statistics.  "
    "Pick a team, then a player from that team, and use the slider feature to zero in on one specific year to compare "
    "Finally, view the results in the table and charts below."
)
st.write("Explore NBA player information and statistics from 1996 to 2022.")
#create 2 columns
col1, col2 = st.columns(2)

# player 1 column
with col1:
    st.subheader("Player 1🏀")
#select a team
    teams1 = sorted(df["team_abbreviation"].dropna().unique())

    team1 = st.selectbox("Select a team:", teams1, key="team1_select")

# Filter the data by team
    team1_data = df[df["team_abbreviation"] == team1]

# Select a player
    players1 = sorted(team1_data["player_name"].dropna().unique())

    player1 = st.selectbox("Select a player:", players1, key="player1_select")


# Filter the data by player and sort by season
    player1_data = team1_data[team1_data["player_name"] == player1].sort_values("season")

#slider for specific season
    seasons1 = sorted(player1_data['season'].dropna().unique())
    if len(seasons1) > 1:
        start_s1, end_s1 = st.select_slider("Select Seasons:", options=seasons1,value=(seasons1[0], seasons1[-1]), key=f"slider1_{player1}")
        player1_filtered = player1_data[player1_data["season"].between(start_s1, end_s1)]
#filter rows for range
    elif len(seasons1) == 1:
        st.infof("Only 1 season available for {player1}: {seasons1[0]}")
        player1_filtered = player1_data
    else:
        player1_filtered = pd.DataFrame()
# Display player information
    st.header("Player 1 Information")
    if not player1_filtered.empty:
        st.dataframe(
            player1_filtered[
            [
                "season",
                "player_name",
                "team_abbreviation",
                "age",
                "player_height",
                "player_weight",
                "college",
                "country",
                "draft_year",
                "draft_round",
                "draft_number"
            ]
        ]
    )

# Display statistics
    st.header("Player 1 Statistics")
    if not player1_filtered.empty:
        st.metric("Games Played (Total)", int(player1_filtered["gp"].sum()))
        st.metric("Points (Avg)", f"{player1_filtered['pts'].mean():.1f}")
        st.metric("Rebounds (Avg)", f"{player1_filtered['reb'].mean():.1f}")
        st.metric("Assists (Avg)", f"{player1_filtered['ast'].mean():.1f}")

# Display a chart
    st.header("Player 1 Statistics Chart")
    if not player1_filtered.empty:
        stats1 = (
            player1_filtered.groupby("season", as_index=False)[["pts", "reb", "ast"]]
            .mean()
            .sort_values("season")
        )
        st.bar_chart(
            stats1,
            x="season",
            y=["pts", "reb", "ast"])

   


    # player 1 column
with col2:
    st.subheader("Player 2🏀")
#select a team
    teams2 = sorted(df["team_abbreviation"].dropna().unique())

    team2 = st.selectbox("Select a team:", teams2, key="team2_select")


# Filter the data by team
    team2_data = df[df["team_abbreviation"] == team2]

# Select a player
    players2 = sorted(team2_data["player_name"].dropna().unique())

    player2 = st.selectbox("Select a player:", players2, key="player2_select")

# Filter the data by player
    player2_data = team2_data[team2_data["player_name"] == player2]
#slider for specific season
    seasons2 = sorted(player2_data['season'].dropna().unique())
    if len(seasons1) > 1:
        start_s2, end_s2 = st.select_slider("Select Seasons:", options=seasons2,value=(seasons2[0], seasons2[-1]), key=f"slider2_{player2}")
        player2_filtered = player2_data[player2_data["season"].between(start_s2, end_s2)]
#filter rows for range
    elif len(seasons2) == 2:
        st.infof("Only 1 season available for {player2}: {seasons2[0]}")
        player2_filtered = player2_data
    else:
        player2_filtered = pd.DataFrame()
# Display player information
    st.header("Player 2 Information")
    if not player2_filtered.empty:
        st.dataframe(
            player2_filtered[
            [
                "season",
                "player_name",
                "team_abbreviation",
                "age",
                "player_height",
                "player_weight",
                "college",
                "country",
                "draft_year",
                "draft_round",
                "draft_number"
            ]
        ]
    )

# Display statistics
    st.header("Player 2 Statistics")
    if not player2_filtered.empty:
        st.metric("Games Played (Total)", int(player2_filtered["gp"].sum()))
        st.metric("Points (Avg)", f"{player2_filtered['pts'].mean():.1f}")
        st.metric("Rebounds (Avg)", f"{player2_filtered['reb'].mean():.1f}")
        st.metric("Assists (Avg)", f"{player2_filtered['ast'].mean():.1f}")
# Display a chart
    st.header("Player 2 Statistics Chart")
    if not player2_filtered.empty:
        stats2 = (
            player2_filtered.groupby("season", as_index=False)[["pts", "reb", "ast"]]
            .mean()
            .sort_values("season")
        )
        st.bar_chart(
            stats2,
            x="season",
            y=["pts", "reb", "ast"])
