import requests
import pandas as pd
from dash import Dash, html
from dash import dash_table

# Fetch 10 random users
url = 'https://randomuser.me/api/?results=10'
response = requests.get(url)
data = response.json()['results']  # Make sure to access the 'results' key

# Initialize the Dash app
app = Dash(__name__)

# Convert data to a Pandas DataFrame for easier manipulation and display
df = pd.DataFrame(data)

def flatten_data(df, parent_key='', sep='_'):
    """
    Flatten nested dictionaries or lists within a DataFrame column into separate columns.

    Args:
    df (pd.DataFrame): The DataFrame to flatten.
    parent_key (str, optional): Concatenated key that will be used as a prefix for the new column names.
    sep (str, optional): Separator between the parent key and the child key.

    Returns:
    pd.DataFrame: A DataFrame with flattened column data.
    """
    original_columns = list(df.columns)
    for column in original_columns:
        # Check if the column contains dictionaries
        if isinstance(df.at[0, column], dict):
            expand_more = False
            for k, v in pd.json_normalize(df[column]).items():
                new_col_name = f"{parent_key}{sep}{k}" if parent_key else k
                df[new_col_name] = v
                if isinstance(df.at[0, new_col_name], dict) or isinstance(df.at[0, new_col_name], list):
                    expand_more = True
            df.drop(column, axis=1, inplace=True)
            if expand_more:
                df = flatten_data(df, parent_key=column, sep=sep)  # Recursively apply if more dictionaries/lists found
        # Check if the column contains lists
        elif isinstance(df.at[0, column], list):
            # Join list items into a single string (or handle otherwise as needed)
            df[column] = df[column].apply(lambda x: ', '.join(map(str, x)) if x else None)

    return df

# Apply the flattening function to the DataFrame
df = flatten_data(df)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Random User Dashboard"),
    dash_table.DataTable(
        # Create columns dynamically based on DataFrame columns
        columns=[{"name": col, "id": col} for col in df.columns],
        # Convert DataFrame to a list of dictionaries, suitable for the DataTable component
        data=df.to_dict('records'),
    )
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
