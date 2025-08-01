"""
Script to create master dataset
"""
from datetime import datetime
from pathlib import Path
import pandas as pd

# Loading data
def read_data_from_layer(layer: str, file_path: str) -> pd.DataFrame:
    """Read all data from any layer"""
    path = Path('data/')
    return pd.read_csv(path / layer / file_path)

interactions = read_data_from_layer('raw', 'cs_interactions.csv')
customers = read_data_from_layer('raw', 'customers.csv')
usage = read_data_from_layer('raw', 'platform_usage.csv')
features = read_data_from_layer('trusted', 'features_normalized.csv')

# Adjusting features
features.loc[:, 'is_active'] = True

features = features.pivot_table(
    index='customer_id',
    columns='feature',
    values='is_active',
    fill_value=0
).rename_axis(None, axis=1).reset_index()

# Creating "mega" dataset
df = pd.merge(
    customers,
    interactions,
    how='left',
    on='customer_id'
)

df = df.merge(
    usage,
    how='left',
    on='customer_id'
)

df = df.merge(
    features,
    how='left',
    on='customer_id'
)

# Preparing dataset
df = df.groupby('customer_id') \
    .agg({
        'mrr': 'last',
        'plan': 'last',
        'contracting_date': 'min',
        'segment': 'last',
        'interaction_date': 'max', # Last interaction
        'interaction_type': 'last', # Last activity
        'nps_last_research': 'last',
        'event_date': 'max', # Last usage data collection
        'logins_last_week': 'mean', # Historic logins
        'finished_tasks': 'mean', # Historic finished tasks
        'active_users': 'mean', # Average users (they can be higher or lower)
        'num_opened_tickets': 'mean', # Historical opened tickets
        'API Access': 'max', 
        'Advanced Reports': 'max', 
        'Attachments': 'max',
        'Automations': 'max', 
        'Comments': 'max', 
        'Dashboards': 'max', 
        'Permission Control': 'max',
        'Project Creation': 'max', 
        'SSO': 'max', 
        'Task Creation': 'max'
    }) \
    .reset_index()

# Feature engineering
def calculate_tenure_in_years(start_date, end_date):
    """
    Calcula o tempo de contrato em anos, respeitando a regra de negócio
    de 365/366 dias para anos normais/bissextos.
    """
    total_days_in_period = 0
    for year in range(start_date.year, end_date.year + 1):
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        total_days_in_period += 366 if is_leap else 365

    # Se não completou um ano inteiro, o cálculo pode ser impreciso,
    # então retornamos a proporção dos dias.
    if total_days_in_period == 0:
        return 0

    # tenure_in_days já calculado
    tenure_in_days = (end_date - start_date).days
    
    # A "idade" do cliente em anos é a proporção de dias que ele viveu
    # pelo total de dias no período que ele atravessou.
    return tenure_in_days / (total_days_in_period / (end_date.year - start_date.year + 1))

now = datetime(2026, 12, 1)

df.loc[:, 'weeks_since_last_interaction'] = (
    now - pd.to_datetime(df['interaction_date'])
).dt.days // 7

df.loc[:, 'tenure_in_years'] = df.apply(
    lambda row: calculate_tenure_in_years(pd.to_datetime(row['contracting_date']), now),
    axis=1
)

df.loc[:, 'weeks_since_last_usage_extraction'] = (
    now - pd.to_datetime(df['event_date'])
).dt.days // 7

# Save dataset into analytics
df.to_csv(Path('data/analytics') / 'master_dataset.csv', index=False)
print('master_dataset.csv saved to Analytics successfully!')
