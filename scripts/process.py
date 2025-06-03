import pandas as pd
from jinja2 import Environment, FileSystemLoader

try:
    # 1. Load data from Excel with explicit parameters
    df = pd.read_excel(
        'data/Long_format_poker_results.xlsx',
        sheet_name='Sheet1',  # Specify the sheet name if needed
        dtype={
            'Player': str,
            'FinishScore': float,
            'WinScore': float
        }
    )
    
    # Print detailed information about the DataFrame
    print("\nColumns in DataFrame:", df.columns.tolist())
    print("\nFirst few rows of data:")
    print(df.head())
    print("\nDataFrame info:")
    print(df.info())
    
    # 2. Aggregate per player using WeightedScore
    ranking = (df
        .groupby('Player')['WeightedScore']
        .mean()
        .reset_index()
        .sort_values('WeightedScore', ascending=False)
    )

    # Convert column names to lowercase for consistency
    ranking.columns = ranking.columns.str.lower()

    # 3. Render HTML
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('index.html')
    html = tmpl.render(rankings=ranking.to_dict(orient='records'))

    # 4. Save the HTML file
    with open('docs/index.html', 'w') as f:
        f.write(html)

    print("\nFinal rankings:")
    print(ranking)

except Exception as e:
    print(f"\nError occurred: {str(e)}")
    print(f"DataFrame info: {df.info() if 'df' in locals() else 'No DataFrame created'}")
    raise
