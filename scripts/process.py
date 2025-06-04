import pandas as pd
import numpy as np
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

    # Ensure 'FinishScore' is numeric, coercing errors to NaN
    df['FinishScore'] = pd.to_numeric(df['FinishScore'], errors='coerce')
    
    # IMPORTANT ASSUMPTION: The data in 'Long_format_poker_results.xlsx' is assumed to be sorted chronologically
    # for each player (oldest game first, newest game last) for the 'last 6 games' logic to work correctly.
    # If not, a 'GameDate' or 'GameID' column should be added and used for sorting before this step.

    # 2. Calculate player scores based on best 3 finishes in last 6 games
    def calculate_player_score(player_games):
        # player_games is already sorted if the main df was sorted by date/game_id per player
        # For now, we assume it's sorted as per the file's current order for that player.
        recent_games = player_games.tail(6) # Get last 6 games (or fewer if less than 6 played)
        
        finish_scores = recent_games['FinishScore'].dropna().sort_values(ascending=False) # Higher FinishScore is better
        
        num_recent_games_considered = len(recent_games)
        num_valid_finishes_in_recent = len(finish_scores)
        
        if num_valid_finishes_in_recent == 0:
            power_score = np.nan
            num_finishes_used = 0
        else:
            best_finishes = finish_scores.head(3) # Get best 3 (or fewer)
            power_score = best_finishes.mean()
            num_finishes_used = len(best_finishes)
            
        return pd.Series({
            'PowerScore': power_score,
            'NumRecentGamesConsidered': num_recent_games_considered,
            'NumFinishesUsed': num_finishes_used
        })

    ranking = df.groupby('Player').apply(calculate_player_score).reset_index()
    
    # Rename PowerScore to WeightedScore to match the template
    ranking = ranking.rename(columns={'PowerScore': 'WeightedScore'})
    
    # Sort by WeightedScore (higher is better), NaN scores will be at the bottom
    ranking = ranking.sort_values('WeightedScore', ascending=False, na_position='last')

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