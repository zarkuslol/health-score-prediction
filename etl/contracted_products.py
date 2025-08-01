"""
Script to extract most used products by customer from platform_usage
"""
from pathlib import Path
import pandas as pd

DATA_PATH = Path('data/')
INPUT_FILE = DATA_PATH / 'raw' / 'platform_usage.csv'
OUTPUT_FILE = DATA_PATH / 'trusted' / 'features_normalized.csv'

def normalize_features_data(input_path, output_path):
    """
    Lê os dados de uso da plataforma, normaliza a coluna de features
    e salva o resultado em um novo arquivo CSV.
    """
    try:
        # 1. Carregar o arquivo CSV
        print(f"Carregando dados de '{input_path}'...")
        df = pd.read_csv(input_path)
        print("Dados carregados com sucesso. Amostra inicial:")
        print(df.head())
        
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{input_path}' não foi encontrado.")
        print("Por favor, certifique-se de que o script que gera esse arquivo foi executado primeiro.")
        return

    # 2. Extrair cada produto (feature)
    df.dropna(subset=['most_used_features'], inplace=True)
    df['most_used_features'] = df['most_used_features'].str.split(',')
    
    # 3. Criar uma nova linha para cada produto
    print("\nProcessando: criando uma linha para cada feature usada...")
    df_normalized = df.explode('most_used_features')
    
    # 4. Fazer um trim na coluna para limpeza
    df_normalized['most_used_features'] = df_normalized['most_used_features'].str.strip()
    
    df_normalized.rename(columns={'most_used_features': 'feature'}, inplace=True)

    df_normalized = df_normalized[['customer_id', 'feature']]

    # 5. Salvar o resultado em um novo CSV
    print(f"Salvando dados normalizados em '{output_path}'...")
    df_normalized.to_csv(output_path, index=False)
    
    print("\nProcesso concluído com sucesso!")
    print("Amostra do resultado final:")
    print(df_normalized.head())

# Executa a função
if __name__ == "__main__":
    normalize_features_data(INPUT_FILE, OUTPUT_FILE)
