import pandas as pd
from jinja2 import Environment, FileSystemLoader

# 1. Load data
df = pd.read_excel('data/Long_format_poker_results.xlsx')

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

# 5. Write out to docs/
with open('docs/index.html', 'w') as f:
    f.write(html)
