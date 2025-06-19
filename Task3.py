import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load dataset
df = pd.read_csv("clean_jobs.csv")

# Clean and format data
df = df.dropna(subset=['company', 'location', 'title', 'date_posted', 'source'])
df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
df = df.dropna(subset=['date_posted'])  # Remove invalid dates

# Prepare top companies data
top_companies = df['company'].value_counts().nlargest(10).reset_index()
top_companies.columns = ['company', 'count']

# Prepare top locations data
top_locations = df['location'].value_counts().nlargest(10).reset_index()
top_locations.columns = ['location', 'count']

# Prepare top job titles data
top_titles = df['title'].value_counts().nlargest(10).reset_index()
top_titles.columns = ['title', 'count']

# Initialize the Dash app
app = Dash(__name__)
app.title = "Job Listings Dashboard"

# Define app layout
app.layout = html.Div([
    html.H1("📊 Job Listings Dashboard", style={"textAlign": "center"}),

    dcc.Tabs([
        dcc.Tab(label='Jobs by Company', children=[
            dcc.Graph(
                figure=px.bar(
                    top_companies, x='company', y='count',
                    title='Top 10 Hiring Companies',
                    labels={'count': 'Number of Jobs'},
                    color='count'
                )
            )
        ]),
        dcc.Tab(label='Jobs by Location', children=[
            dcc.Graph(
                figure=px.bar(
                    top_locations, x='location', y='count',
                    title='Top 10 Job Locations',
                    labels={'count': 'Number of Jobs'},
                    color='count'
                )
            )
        ]),
        dcc.Tab(label='Jobs Over Time', children=[
            dcc.Graph(
                figure=px.histogram(
                    df, x='date_posted',
                    nbins=30,
                    title='Job Postings Over Time',
                    labels={'date_posted': 'Date Posted'}
                )
            )
        ]),
        dcc.Tab(label='Source of Jobs', children=[
            dcc.Graph(
                figure=px.pie(
                    df, names='source',
                    title='Job Sources Breakdown'
                )
            )
        ]),
        dcc.Tab(label='Top Job Titles', children=[
            dcc.Graph(
                figure=px.bar(
                    top_titles, x='title', y='count',
                    title='Top 10 Job Titles',
                    labels={'count': 'Number of Jobs'},
                    color='count'
                )
            )
        ]),
    ])
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
