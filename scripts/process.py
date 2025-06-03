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
    
    # Convert column names to lowercase to match Excel's case-insensitive nature
    df.columns = df.columns.str.lower()
    
    # 2. Compute weighted score using lowercase column names
    df['score'] = 0.7 * df['finishscore'] + 0.3 * df['winscore']

    # 3. Aggregate per player (mean or sum as you choose)
    ranking = (df
        .groupby('player')['score']
        .mean()
        .reset_index()
        .sort_values('score', ascending=False)
    )

    # 4. Render HTML
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('index.html')
    html = tmpl.render(rankings=ranking.to_dict(orient='records'))

    # Save the HTML file
    with open('docs/index.html', 'w') as f:
        f.write(html)

    print("\nFinal rankings:")
    print(ranking)

except Exception as e:
    print(f"\nError occurred: {str(e)}")
    print(f"DataFrame info: {df.info() if 'df' in locals() else 'No DataFrame created'}")
    raise
