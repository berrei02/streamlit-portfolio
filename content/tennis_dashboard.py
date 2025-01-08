import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import plotly.express as px


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

st.write("""
# Tennis Match Dashboard
Displaying some simple statistics for ATP tennis matches in 2024.
Overall it seems that Jannik Sinner had an awesome year. 
Data was pulled from GitHub and is stored, transformed and served via Google BigQuery.
## Technologies
- Storage: Google BigQuery
- Data Visualization: Streamlit & Plotly
""")


top_players_cnt = st.slider("Show Top", 0, 100, 10)
st.write(f"Showing the {top_players_cnt} best male Tennis players in 2024.")

df_100 = run_query("select *, case when lost_matches = 0 then null else round(won_matches / lost_matches, 2) end as win_lose_ratio from `streamlit-demo-db.tennis.atp_stats` LIMIT 100")

df = df_100.head(top_players_cnt)

# Create scatter plot
fig = px.scatter(
    df,
    x='won_matches',
    y='lost_matches',
    color='win_lose_ratio', 
    hover_data=['player_name']
)

# Display in Streamlit
st.plotly_chart(fig)


# Print results.
with st.expander("Detail data"):
    st.table(df)