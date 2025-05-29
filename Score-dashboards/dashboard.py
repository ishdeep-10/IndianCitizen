import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Transfer Rumors Dashboard",
    page_icon="⚽",
    layout="wide"
)

# Cache the data loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    """
    Load data from CSV file
    """
    try:
        df = pd.read_csv('transfer_rumours.csv')
        
        # Convert market value to numeric
        df['market_value_numeric'] = df['market_value'].apply(
            lambda x: float(str(x).replace('€', '').replace('m', '')) 
            if 'm' in str(x) 
            else float(str(x).replace('€', '').replace('k', ''))/1000 
            if 'k' in str(x) 
            else 0
        )
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load the data
df = load_data()

if df.empty:
    st.error("No data available. Please make sure transfer_rumours.csv exists in the app directory.")
    st.stop()

# Dashboard title with last update time
st.title("⚽ Transfer Rumors Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# Sidebar filters
st.sidebar.header("Filters")

# Position filter
positions = ['All'] + sorted(df['position'].unique().tolist())
selected_position = st.sidebar.selectbox('Select Position', positions)

# Market value range filter
max_value = float(df['market_value_numeric'].max())
min_value = float(df['market_value_numeric'].min())
market_value_range = st.sidebar.slider(
    'Market Value Range (€M)',
    min_value, max_value,
    (min_value, max_value)
)

# Club filters
clubs = ['All'] + sorted(df['current_club'].unique().tolist())
selected_club = st.sidebar.selectbox('Select Current Club', clubs)

# Apply filters
filtered_df = df.copy()
if selected_position != 'All':
    filtered_df = filtered_df[filtered_df['position'] == selected_position]
if selected_club != 'All':
    filtered_df = filtered_df[filtered_df['current_club'] == selected_club]
filtered_df = filtered_df[
    (filtered_df['market_value_numeric'] >= market_value_range[0]) &
    (filtered_df['market_value_numeric'] <= market_value_range[1])
]

# Display total number of rumors and total market value
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Rumors", len(filtered_df))
with col2:
    total_value = filtered_df['market_value_numeric'].sum()
    st.metric("Total Market Value", f"€{total_value:.1f}M")

# Create layout with columns
col1, col2 = st.columns(2)

# Top Players by Market Value
with col1:
    st.subheader("Top Players by Market Value")
    fig_market = px.bar(
        filtered_df.nlargest(10, 'market_value_numeric'),
        x='player_name',
        y='market_value_numeric',
        color='probability',
        text='market_value',
        title='Top 10 Players by Market Value',
        labels={'market_value_numeric': 'Market Value (€M)', 'player_name': 'Player'},
        color_continuous_scale='Viridis'
    )
    fig_market.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_market, use_container_width=True)

# Position Distribution
with col2:
    st.subheader("Rumors by Position")
    fig_position = px.pie(
        filtered_df,
        names='position',
        values='market_value_numeric',
        title='Market Value Distribution by Position',
        hole=0.4
    )
    st.plotly_chart(fig_position, use_container_width=True)

# Create second row of columns
col3, col4 = st.columns(2)

# Interested Clubs Analysis
with col3:
    st.subheader("Most Active Interested Clubs")
    club_activity = filtered_df.groupby('interested_club').agg({
        'player_name': 'count',
        'market_value_numeric': 'sum'
    }).reset_index()
    club_activity.columns = ['Club', 'Number of Targets', 'Total Market Value (€M)']
    fig_clubs = px.scatter(
        club_activity.nlargest(15, 'Total Market Value (€M)'),
        x='Number of Targets',
        y='Total Market Value (€M)',
        text='Club',
        size='Number of Targets',
        title='Club Transfer Activity'
    )
    fig_clubs.update_traces(textposition='top center')
    st.plotly_chart(fig_clubs, use_container_width=True)

# Age Distribution
with col4:
    st.subheader("Age Distribution")
    fig_age = px.histogram(
        filtered_df,
        x='age',
        nbins=20,
        title='Age Distribution of Transfer Targets',
        color='position'
    )
    st.plotly_chart(fig_age, use_container_width=True)

# Detailed Data Table
st.markdown("---")
st.subheader("Detailed Rumors Data")
st.dataframe(
    filtered_df[[
        'player_name', 'position', 'age', 'current_club',
        'interested_club', 'market_value', 'probability'
    ]].sort_values('probability', ascending=False),
    hide_index=True,
    width=1500
) 