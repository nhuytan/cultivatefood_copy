import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# 1. LOAD AND CLEAN DATA
def load_data():
    df = pd.read_csv('Outbound.csv')
    
    # Clean numeric columns
    num_cols = ['Protein LBS', 'Starch LBS', 'Veg LBS', 'Fruit LBS', 
                'Baked Goods LBS', 'Dairy LBS', 'Grocery LBS', 'Total Pounds']
    for col in num_cols:
        # Remove commas and non-numeric chars, convert to float
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

    # Parse Dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    
    # Extract Year/Month
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    # Clean County Names
    df['County'] = df['County'].astype(str).str.strip().str.upper()
    df['County'] = df['County'].replace('NAN', 'UNKNOWN') # Handle missing county data

    # FILTER: Keep only 2023, 2024, 2025
    df = df[df['Year'].isin([2023, 2024, 2025])]
    
    return df

df = load_data()

# 2. APP SETUP
# Pick a theme here, I chose FLATLY for "Basic Modern" look
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server  # Expose server 

# 3. APP LAYOUT
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H1("Food Distribution Dashboard", className="text-center text-primary mb-4"), width=12)
    ], className="mt-4"),

    # Filters Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Filter by County:", className="fw-bold"),
                    dcc.Dropdown(
                        id='county-dropdown',
                        options=[{'label': 'All Counties', 'value': 'ALL'}] + 
                                [{'label': c, 'value': c} for c in sorted(df['County'].unique())],
                        value='ALL',
                        clearable=False
                    )
                ])
            ], className="mb-4 shadow-sm")
        ], width=12)
    ]),

    # Row 1: 
        # Distribution Trend & Categories
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Distribution Trend (Year-over-Year)"),
                dbc.CardBody(dcc.Graph(id='trend-chart'))
            ], className="mb-4 shadow-sm")
        ], md=6),

        # Food Categories
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Food Category Breakdown"),
                dbc.CardBody(dcc.Graph(id='category-chart'))
            ], className="mb-4 shadow-sm")
        ], md=6),
    ]),

    # Row 2:
        # County Context
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Total Volume by County (Top 10)"),
                dbc.CardBody(dcc.Graph(id='county-chart')) # This chart shows all counties always to provide context. Does not change with dropdown change
            ], className="mb-4 shadow-sm")
        ], md=6),
        
        # Top 10 Vendors
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 10 Vendor Partners (2025 Focus)"),
                dbc.CardBody(dcc.Graph(id='vendor-chart'))
            ], className="mb-4 shadow-sm")
        ], md=6),
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col(html.P("Data Source: Outbound.csv (2023-2025)", className="text-muted text-center"), width=12)
    ])

], fluid=True)


# 4. CALLBACKS (Interactivity)
@app.callback(
    [Output('trend-chart', 'figure'),
     Output('category-chart', 'figure'),
     Output('county-chart', 'figure'),
     Output('vendor-chart', 'figure')],
    [Input('county-dropdown', 'value')]
)
def update_charts(selected_county):
    # Base Filter logic
    if selected_county == 'ALL':
        filtered_df = df
        title_suffix = "(All Counties)"
    else:
        filtered_df = df[df['County'] == selected_county]
        title_suffix = f"({selected_county})"

    # 1. Monthly Trend Chart
    monthly_data = filtered_df.groupby(['Year', 'Month'])['Total Pounds'].sum().reset_index()
    fig_trend = px.line(monthly_data, x='Month', y='Total Pounds', color='Year', 
                        markers=True, title=f"Monthly Volume {title_suffix}")
    fig_trend.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))

    # 2. Category Chart
    cat_cols = ['Protein LBS', 'Starch LBS', 'Veg LBS', 'Fruit LBS', 'Dairy LBS', 'Grocery LBS']
    # Melt data for bar chart
    cat_data = filtered_df.groupby('Year')[cat_cols].sum().reset_index().melt(id_vars='Year', var_name='Category', value_name='Pounds')
    cat_data['Category'] = cat_data['Category'].str.replace(' LBS', '')
    
    fig_cat = px.bar(cat_data, x='Category', y='Pounds', color='Year', barmode='group',
                     title=f"Food Type Mix {title_suffix}")

    # 3. County Chart
    # I intentionally kept this showing ALL counties so users can compare the selected one vs others
    # I can change it to highlight the selected county if wanted. For now, standard bar chart.
    county_sums = df.groupby(['County', 'Year'])['Total Pounds'].sum().reset_index()
    # Get top 10 counties by total volume
    top_counties = df.groupby('County')['Total Pounds'].sum().sort_values(ascending=False).head(10).index
    county_sums = county_sums[county_sums['County'].isin(top_counties)]
    
    fig_county = px.bar(county_sums, x='County', y='Total Pounds', color='Year', 
                        title="Regional Distribution (Global View)")

    # 4. Vendor Chart Top 10
    # Filtered for 2025 specifically to see "Current Partners" view, can use all years if preferred.
    vendor_sums = filtered_df.groupby('Vendor')['Total Pounds'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_vendor = px.bar(vendor_sums, x='Total Pounds', y='Vendor', orientation='h',
                        title=f"Top Partners {title_suffix}", color_discrete_sequence=["#50C2E5"])
    fig_vendor.update_layout(yaxis={'categoryorder':'total ascending'})

    return fig_trend, fig_cat, fig_county, fig_vendor

# 5. RUN SERVER
if __name__ == '__main__':
    app.run(debug=True, port=8050)