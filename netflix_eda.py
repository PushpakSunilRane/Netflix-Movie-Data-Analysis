import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re

# Set style for better-looking plots
plt.style.use('ggplot')  # Using a built-in matplotlib style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Load the Netflix dataset
df = pd.read_csv('netflix_titles.csv')

# Data cleaning and preparation
# Handle date conversion with error handling
df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce')
# Create year and month columns only for valid dates
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# Clean country data by taking the first country if multiple countries are listed
df['primary_country'] = df['country'].str.split(',').str[0]

# Create a figure with subplots for the first four plots
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('Netflix Content Analysis', fontsize=16)

# 1. Countplot - Number of Movies vs TV Shows
sns.countplot(data=df, x='type', ax=axes[0, 0])
axes[0, 0].set_title('Content Type Distribution (Movies vs TV Shows)')
axes[0, 0].set_xlabel('Type')
axes[0, 0].set_ylabel('Count')

# 2. Line Plot - Content produced per year
content_per_year = df.groupby('release_year').size()
sns.lineplot(x=content_per_year.index, y=content_per_year.values, ax=axes[0, 1])
axes[0, 1].set_title('Content Produced Per Year')
axes[0, 1].set_xlabel('Year')
axes[0, 1].set_ylabel('Number of Titles')
axes[0, 1].grid(True)

# 3. Bar Plot - Top 10 countries producing Netflix content
top_countries = df['primary_country'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, ax=axes[1, 0])
axes[1, 0].set_title('Top 10 Countries by Content Production')
axes[1, 0].set_xlabel('Number of Titles')
axes[1, 0].set_ylabel('Country')

# 4. Pie Chart - Rating distribution
rating_counts = df['rating'].value_counts().head(8)  # Top 8 ratings
axes[1, 1].pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%')
axes[1, 1].set_title('Rating Distribution')

# Adjust layout for the first four plots
plt.tight_layout()
plt.savefig('netflix_analysis_part1.png')
plt.close()

# 5. Word Cloud - Frequent words in titles
# Combine all titles and clean the text
all_titles = ' '.join(df['title'].dropna())
# Remove special characters and convert to lowercase
all_titles = re.sub(r'[^\w\s]', '', all_titles.lower())

# Generate word cloud
wordcloud = WordCloud(width=1200, height=800, background_color='white',
                     min_font_size=10).generate(all_titles)

# Plot the word cloud
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Titles', fontsize=16)
plt.savefig('netflix_wordcloud.png')
plt.close()

# Print analysis results
print("\nPython Analysis Results:")
print("\n1. Content Type Distribution:")
print(df['type'].value_counts())

print("\n2. Release Year Statistics:")
print(df['release_year'].describe())

print("\n3. Top 10 Countries by Content Production:")
print(top_countries)

print("\n4. Rating Distribution:")
print(rating_counts)

# Additional insights
print("\nAdditional Insights:")
print(f"\nTotal number of titles: {len(df)}")
print(f"\nDate range of content: {df['release_year'].min()} to {df['release_year'].max()}")

# Data quality check
print("\nData Quality Check:")
print(f"\nNumber of missing dates: {df['date_added'].isna().sum()}")
print(f"\nNumber of missing countries: {df['country'].isna().sum()}")
print(f"\nNumber of missing ratings: {df['rating'].isna().sum()}") 