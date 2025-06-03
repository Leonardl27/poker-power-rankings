import pandas as pd
from jinja2 import Environment, FileSystemLoader

# 1. Load data with explicit column names and better handling
df = pd.read_excel('data/Long_format_poker_results.xlsx')
print("\nColumns in DataFrame:", df.columns.tolist())
print("\nFirst few rows of data:")
print(df.head())

# 2. Compute weighted score
df['Score'] = 0.7 * df['FinishScore'] + 0.3 * df['WinScore']

# 3. Aggregate per player (mean or sum as you choose)
ranking = (df
  .groupby('Player')['Score']
  .mean()
  .reset_index()
  .sort_values('Score', ascending=False)
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

# 5. Write out to docs/
with open('docs/index.html', 'w') as f:
    f.write(html)
