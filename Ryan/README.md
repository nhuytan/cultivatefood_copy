## Features

* **Poverty Rate Analysis**: Generates bar charts showing poverty rates by tract and detailed breakdowns by age and gender.
* **Food Category Distribution**: Calculates and visualizes the distribution of food categories in pounds (LBS), including:
    * Protein, Starch, Vegetables, Fruit, Baked Goods, Dairy, Grocery, and Individual Meals.

* **Automated Visualization**: Creates and saves high-quality charts as PNG files for reporting and presentations.
* **Data Aggregation**: Summarizes large datasets to provide clear insights into total food distribution weights.

## Prerequisites

To run this notebook, you will need the following Python libraries installed:

* **Pandas**: For data manipulation and analysis.
* **Matplotlib**: For creating static visualizations.
* **Seaborn**: For statistical data visualization.
* **Jupyter**: To execute the `.ipynb` file.

To run the dashboard, you will need the following Python libraries installed:

* **Dash**: For building interactive, data-driven web applications and dashboards
* **Dash-Bootstrap-Components**: Adds Bootstrap-themed layout and UI components
* **Plotly**: Provides a wide range of rich, web-based charts and visualizations

You can install the dependencies using pip:

```bash
pip install pandas matplotlib seaborn notebook dash dash-bootstrap-components plotly
```

## Data Sources

The notebook expects the following datasets in CSV format:
* `Elkhart_PovPercent_Transposed.csv`
* `Marhsall_PovPercent_Transposed.csv`
* `St_Joseph_PovPercent_Transposed.csv`
* `Outbound.csv`



## Generated Outputs

The notebook automatically exports the visualizations as `graph_name.png`



## Notebook Usage

1. Open the notebook in your Jupyter environment.
2. Ensure the source data files are in the same directory or update the file path in the data loading cell.
3. Run all cells to process the data and generate the visualization files.

## Dashboard.py Usage

1. Ensure Outbound.csv is in the same directory
2. Run the script in your terminal:  `python dashboard.py`
3. Open `locahost:8050` in your browser

