"""
Script to generate customer service interactions data
"""
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

# Carrega clientes.csv para garantir a consistência do customer_id
path = Path('data/cleaned')
customers_df = pd.read_csv(path / 'customers.csv')
customer_ids = customers_df['customer_id'].unique()

# Gera dados para interacoes_cs.csv
NUM_INTERACTIONS = 2000  # Aproximadamente 2 interações por cliente
interaction_types = ['Reunião QBR', 'Suporte Técnico', 'Email de Acompanhamento']
interactions_data = []
for _ in range(NUM_INTERACTIONS):
    cid = random.choice(customer_ids)
    # Garante que a data da interação é posterior à data de contratação
    contracting_date_str = customers_df[
        customers_df['customer_id'] == cid
    ]['contracting_date'].iloc[0]
    contracting_date = datetime.strptime(contracting_date_str, '%Y-%m-%d')
    interaction_date = contracting_date + timedelta(days=random.randint(1, 365*3))

    int_type = random.choice(interaction_types)
    nps = random.choice([random.randint(0, 10), np.nan])  # Adiciona a possibilidade de NPS vazio
    interactions_data.append([cid, interaction_date.strftime('%Y-%m-%d'), int_type, nps])

interactions_df = pd.DataFrame(
    interactions_data,
    columns=['customer_id', 'interaction_date',
             'interaction_type', 'nps_last_research']
)
interactions_df.to_csv(path / 'cs_interactions.csv', index=False)

print("interactions.csv gerado com sucesso!")
