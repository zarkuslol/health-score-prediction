"""
Script to generate platform usage data
"""
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Carrega clientes.csv para garantir a consistência do customer_id
path = Path('data/cleaned')
customers_df = pd.read_csv(path / 'customers.csv')
customer_ids = customers_df['customer_id'].unique()

# Gera dados para uso_plataforma.csv
NUM_EVENTS = 5000  # Aproximadamente 5 eventos por cliente
usage_data = []
for _ in range(NUM_EVENTS):
    cid = random.choice(customer_ids)
    # Garante que a data do evento é posterior à data de contratação
    contracting_date_str = customers_df[
        customers_df['customer_id'] == cid
    ]['contracting_date'].iloc[0]
    contracting_date = datetime.strptime(contracting_date_str, '%Y-%m-%d')
    event_date = contracting_date + timedelta(days=random.randint(1, 365*3))

    logins = random.randint(0, 50)
    projects = random.randint(0, 10)
    tasks = random.randint(0, 100)
    users = random.randint(1, 20)
    usage_data.append([cid, event_date.strftime('%Y-%m-%d'), logins, projects, tasks, users])

usage_df = pd.DataFrame(
    usage_data,
    columns=['customer_id', 'event_date',
             'logins_last_week', 'projects_created', 
             'finished_tasks', 'active_users']
)
usage_df.to_csv(path / 'platform_usage.csv', index=False)

print("platform_usage.csv gerado com sucesso!")
