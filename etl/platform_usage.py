"""
Script to generate platform usage data, including business logic for
opened tickets and feature usage based on customer plan.
"""
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Define the data path
DATA_PATH = Path('data/cleaned')
DATA_PATH.mkdir(parents=True, exist_ok=True)

# Load customers.csv to get the plan for each customer
try:
    # Assuming the main customers file is named 'customers.csv'
    # and has columns 'customer_id' and 'plan'
    customers_df = pd.read_csv(DATA_PATH / 'customers.csv')
except FileNotFoundError:
    print("Error: 'customers.csv' not found in 'data/cleaned/'. Please ensure the file exists.")
    exit()

customer_ids = customers_df['customer_id'].unique()

# --- Define Features per Plan ---
features_basic = ['Task Creation', 'Comments', 'Attachments', 'Project Creation']
features_pro = features_basic + ['Dashboards', 'Automations', 'Permission Control']
features_enterprise = features_pro + ['Advanced Reports', 'API Access', 'SSO', 'Audit Logs']

# --- Generate Platform Usage Data ---
NUM_EVENTS = 5000
usage_data = []

for _ in range(NUM_EVENTS):
    # Select a random customer
    customer_id = random.choice(customer_ids)

    # Get customer info (plan and contract date)
    customer_info = customers_df[customers_df['customer_id'] == customer_id].iloc[0]
    plan = customer_info['plan']
    contract_date_str = customer_info['contracting_date']

    contract_date = datetime.strptime(contract_date_str, '%Y-%m-%d') # Event happens within 3 years after the contract is signed
    event_date = contract_date + timedelta(days=random.randint(1, 365 * 3))

    # 1. num_opened_tickets
    opened_tickets = 0
    if plan == 'Enterprise':
        # Higher chance and volume of tickets
        if random.random() < 0.4:  # 40% chance of having an open ticket
            opened_tickets = random.randint(1, 5)
    elif plan == 'Pro':
        if random.random() < 0.15: # 15% chance
            opened_tickets = random.randint(1, 2)
    else:  # Basic
        if random.random() < 0.05: # 5% chance
            opened_tickets = 1

    # 2. most_used_features
    used_features_list = []
    if plan == 'Basic':
        # Focus on core usage
        used_features_list = random.sample(features_basic, k=random.randint(1, 3))
    elif plan == 'Pro':
        # Breadth of use: mix of core and pro features
        used_features_list = random.sample(features_basic, k=random.randint(1, 2))
        used_features_list += random.sample(['Dashboards', 'Automations', 'Permission Control'], k=random.randint(1, 2))
    elif plan == 'Enterprise':
        # Depth of use: advanced features plus core features (which might cause the tickets)
        used_features_list = random.sample(features_basic, k=random.randint(1, 2))
        used_features_list += random.sample(['Advanced Reports', 'API Access', 'SSO'], k=random.randint(1, 2))

    most_used_features = ', '.join(used_features_list)

    # Original metrics
    logins = random.randint(0, 50)
    projects = random.randint(0, 10)
    tasks = random.randint(0, 100)
    users = random.randint(1, 20)

    usage_data.append([
        customer_id,
        event_date.strftime('%Y-%m-%d'),
        logins,
        projects,
        tasks,
        users,
        opened_tickets,
        most_used_features
    ])

# Create a DataFrame and save it to a CSV file
usage_df = pd.DataFrame(
    usage_data,
    columns=[
        'customer_id',
        'event_date',
        'logins_last_week',
        'projects_created',
        'finished_tasks',
        'active_users',
        'num_opened_tickets',
        'most_used_features'
    ]
)
usage_df.to_csv(DATA_PATH / 'platform_usage.csv', index=False)

print("platform_usage.csv was successfully generated with all columns!")
