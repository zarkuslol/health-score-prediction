"""
Script to generate customers data
"""
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

path = Path('data/cleaned')

NUM_CUSTOMERS = 1000
customer_ids = range(1, NUM_CUSTOMERS + 1)
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)
plans = ['Basic', 'Pro', 'Enterprise']
segments = ['SMB', 'Mid-Market', 'Enterprise']

customers_data = []
for cid in customer_ids:
    contracting_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    plan = random.choice(plans)
    if plan == 'Basic':
        mrr = round(random.uniform(20, 100), 2)
    elif plan == 'Pro':
        mrr = round(random.uniform(100, 500), 2)
    else:
        mrr = round(random.uniform(500, 2000), 2)
    segment = random.choice(segments)
    customers_data.append([cid, contracting_date.strftime('%Y-%m-%d'), plan, mrr, segment])

customers_df = pd.DataFrame(
    customers_data,
    columns=['customer_id', 'contracting_date', 'plan', 'mrr', 'segment']
)
customers_df.to_csv(path / 'customers.csv', index=False)

print("customers.csv gerado com sucesso!")
