import pandas as pd
import os
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

    # FIXED: Don't convert column names to lowercase - keep original case
    # The template expects 'WeightedScore' and 'Player', not 'weightedscore' and 'player'
    # ranking.columns = ranking.columns.str.lower()  # REMOVED THIS LINE

    # Create output directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)

    # 3. Render HTML
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('index.html')
    html = tmpl.render(rankings=ranking.to_dict(orient='records'))

    # 4. Save the HTML file
    with open('docs/index.html', 'w') as f:
        f.write(html)

    print("\nHTML file successfully created at docs/index.html")
    print("\nFinal rankings:")
    print(ranking)

except Exception as e:
    print(f"\nError occurred: {str(e)}")
    if 'df' in locals():
        print("\nDataFrame info:")
        print(df.info())
    else:
        print("No DataFrame was created - check if the Excel file exists")
    raise