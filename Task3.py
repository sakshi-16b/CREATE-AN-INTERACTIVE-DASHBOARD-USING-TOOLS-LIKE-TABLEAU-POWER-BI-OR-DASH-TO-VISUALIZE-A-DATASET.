import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load dataset
df = pd.read_csv("software_companies.csv")

# Clean and format data
# Drop the 'Unnamed' columns which seem to be empty or contain irrelevant data
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Rename columns to match desired names for the dashboard tabs
df = df.rename(columns={
    'Company Name': 'company',
    'Address': 'location',
    'Specialization': 'specialization' # Using specialization as a category equivalent
})

# Drop rows where essential columns for this dashboard are missing
df = df.dropna(subset=['company', 'location', 'specialization'])

# Prepare top companies data
top_companies = df['company'].value_counts().nlargest(10).reset_index()
top_companies.columns = ['company', 'count']

# Prepare top locations data
top_locations = df['location'].value_counts().nlargest(10).reset_index()
top_locations.columns = ['location', 'count']

# Prepare top specializations data
# Note: 'specialization' column might contain comma-separated values,
# but for simplicity, we are counting unique string entries as is.
top_specializations = df['specialization'].value_counts().nlargest(10).reset_index()
top_specializations.columns = ['specialization', 'count']

# Initialize the Dash app
app = Dash(__name__)
app.title = "Software Companies Dashboard"

# Define app layout
app.layout = html.Div([
    html.H1("📊 Software Companies Dashboard", style={"textAlign": "center"}),

    dcc.Tabs([
        dcc.Tab(label='Companies by Count', children=[
            dcc.Graph(
                figure=px.bar(
                    top_companies, x='company', y='count',
                    title='Top 10 Companies by Entry Count',
                    labels={'count': 'Number of Entries'},
                    color='count'
                )
            )
        ]),
        dcc.Tab(label='Locations by Company Count', children=[
            dcc.Graph(
                figure=px.bar(
                    top_locations, x='location', y='count',
                    title='Top 10 Locations by Company Count',
                    labels={'count': 'Number of Companies'},
                    color='count'
                )
            )
        ]),
        dcc.Tab(label='Top Specializations', children=[
            dcc.Graph(
                figure=px.bar(
                    top_specializations, x='specialization', y='count',
                    title='Top 10 Company Specializations',
                    labels={'count': 'Number of Companies'},
                    color='count'
                )
            )
        ]),
    ])
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
