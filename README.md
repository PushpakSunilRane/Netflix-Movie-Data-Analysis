# Netflix Content Analysis

This project performs an Exploratory Data Analysis (EDA) of Netflix's content library using Python for data analysis and visualization.

## Requirements

1. Python 3.8 or higher
2. Required Python packages:
   - pandas
   - numpy
   - matplotlib
   - seaborn

## Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the analysis script:
```bash
python netflix_eda.py
```

The script will:
1. Generate visualizations saved as 'netflix_analysis.png'
2. Print statistical analysis results to the console

## Analysis Includes

1. Content Type Distribution (Movies vs TV Shows)
2. Release Year Trends
3. Country-wise Production Analysis
4. Genre Distribution

## Note

The current analysis uses a sample dataset. To analyze your own Netflix dataset:
1. Replace the sample data in `netflix_eda.py` with your dataset
2. Ensure your dataset has the following columns:
   - show_id
   - type
   - title
   - release_year
   - country
   - genre
