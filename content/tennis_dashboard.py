import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
import datetime


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
     # Convert rows_raw to a list of dictionaries    
    df = pd.DataFrame(rows)
    return df

st.write("""# Tennis Match Dashboard""")

with st.expander("Project Description"):
    st.write("""
    Displaying some simple statistics for ATP tennis matches in 2024.
    Overall it seems that Jannik Sinner had an awesome year. 
    Data was pulled from GitHub and is stored, transformed and served via Google BigQuery.
    ## Technologies
    - Storage: Google BigQuery
    - Data Visualization: Streamlit & Plotly
    """)


st.divider()

with st.container(border=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        top_players_cnt = st.slider("Show Top", 0, 100, 10)

    with col2:
        start_date = st.date_input("Start Date", datetime.date(2023, 1, 1))
    
    with col3:
        end_date = st.date_input("End Date", datetime.date.today())


df = run_query(f"""
select player_name
     , count(1) as matches_cnt
     , countif(player_is_winner) as matches_won
     , countif(not player_is_winner) as matches_lost
  from `streamlit-demo-db.tennis.match_history`
 where tourney_date between '{start_date}' and '{end_date}'
 group by 1
 order by 2 desc
""")

df_size = df.shape[0]

if df_size == 0: 
    st.write("Please change parameters, no results are returned.")
else:
    df = df.head(top_players_cnt)
    st.write(f"Showing the {df_size} best male Tennis players from {start_date} to {end_date}.")

    # Create scatter plot
    fig = px.scatter(
        df,
        x='matches_won',
        y='matches_lost',
        #color='win_lose_ratio', 
        hover_data=['player_name'],
        text="player_name"
    )

    # Customize the text position and size of points
    fig.update_traces(
        textposition='top center',  # Position the text labels
        marker=dict(size=10)  # Set a constant size for scatter points
    )

    # Display in Streamlit
    st.plotly_chart(fig)


# Print results.
with st.expander("Detail data"):
    st.table(df)