import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config with a light theme
st.set_page_config(
    page_title="Netflix Content Analysis Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for light theme
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    .stMetric {
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 10px;
    }
    .css-1d391kg {
        background-color: #F0F2F6;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
    }
    h2 {
        color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# Set style for plots
plt.style.use('seaborn')
sns.set_style("whitegrid")
sns.set_palette("husl")

# Title with emoji
st.title("🎬 Netflix Content Analysis Dashboard")

# Load data with caching
@st.cache
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    # Data cleaning
    df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['primary_country'] = df['country'].str.split(',').str[0]
    return df

df = load_data()

# Sidebar with a nice header
st.sidebar.markdown("## 🎯 Filters")
st.sidebar.markdown("---")

# Sidebar filters with emojis
content_type = st.sidebar.multiselect(
    "🎥 Select Content Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

year_range = st.sidebar.slider(
    "📅 Select Year Range",
    min_value=int(df['release_year'].min()),
    max_value=int(df['release_year'].max()),
    value=(int(df['release_year'].min()), int(df['release_year'].max()))
)

# Filter data based on selections
filtered_df = df[
    (df['type'].isin(content_type)) &
    (df['release_year'].between(year_range[0], year_range[1]))
]

# Main content with better spacing
st.markdown("---")

# Key metrics with emojis and better styling
st.markdown("### 📊 Content Overview")
metric1, metric2, metric3 = st.columns(3)
with metric1:
    st.metric("🎬 Total Titles", len(filtered_df))
with metric2:
    st.metric("🎥 Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
with metric3:
    st.metric("📺 TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

# First row of visualizations
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Content Type Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=filtered_df, x='type', ax=ax)
    ax.set_title('Content Type Distribution', color='#333333')
    ax.set_xlabel('Type', color='#333333')
    ax.set_ylabel('Count', color='#333333')
    ax.tick_params(colors='#333333')
    st.pyplot(fig)

with col2:
    st.markdown("### 📉 Content Production Trend")
    fig, ax = plt.subplots(figsize=(10, 6))
    content_per_year = filtered_df.groupby('release_year').size()
    sns.lineplot(x=content_per_year.index, y=content_per_year.values, ax=ax)
    ax.set_title('Content Produced Per Year', color='#333333')
    ax.set_xlabel('Year', color='#333333')
    ax.set_ylabel('Number of Titles', color='#333333')
    ax.tick_params(colors='#333333')
    st.pyplot(fig)

# Second row of visualizations
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🌍 Top 10 Countries")
    fig, ax = plt.subplots(figsize=(10, 6))
    top_countries = filtered_df['primary_country'].value_counts().head(10)
    sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax)
    ax.set_title('Top 10 Countries by Content Production', color='#333333')
    ax.set_xlabel('Number of Titles', color='#333333')
    ax.set_ylabel('Country', color='#333333')
    ax.tick_params(colors='#333333')
    st.pyplot(fig)

with col4:
    st.markdown("### ⭐ Rating Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    rating_counts = filtered_df['rating'].value_counts().head(8)
    ax.pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%')
    ax.set_title('Rating Distribution', color='#333333')
    st.pyplot(fig)

# Additional Insights with better formatting
st.markdown("---")
st.markdown("### 📌 Additional Insights")
insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("#### 📊 Content Statistics")
    st.markdown(f"- 📅 Date range: {filtered_df['release_year'].min()} to {filtered_df['release_year'].max()}")
    st.markdown(f"- ⭐ Most common rating: {filtered_df['rating'].mode().iloc[0]}")
    
with insight_col2:
    st.markdown("#### 🔍 Data Quality")
    st.markdown(f"- ❌ Missing dates: {filtered_df['date_added'].isna().sum()}")
    st.markdown(f"- ❌ Missing countries: {filtered_df['country'].isna().sum()}")
    st.markdown(f"- ❌ Missing ratings: {filtered_df['rating'].isna().sum()}")

# Sample data table with a nice header
st.markdown("---")
st.markdown("### 📋 Sample Data")
st.dataframe(filtered_df.head(10), use_container_width=True) 