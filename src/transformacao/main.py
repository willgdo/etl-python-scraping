import pandas as pd
import sqlite3
from datetime import datetime

# Ler os dados do arquivo JSON
jsonl_path = '../data/data.jsonl'
df = pd.read_json(jsonl_path, lines=True)

print(df.head())

# Adicionar a coluna source com o valor de onde os dados foram extraídos;
df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# Adicionar a coluna data_coleta com a data e hora atual;
df['_data_coleta'] = datetime.now()

# Alterar valores de colunas para o tipo Float:
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Alterar valores de colunas para o tipo Integer e Remover possíveis espaços
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

#Remover linhas que não possuem Marcas cadastradas (igual a null);
df.dropna(subset=['brand'], inplace=True)

# Criar coluna “old_price” -> Junção de coluna old_price_reais + old_price_centavos;
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100

#Criar coluna “new_price” -> Junção de coluna new_price_reais + new_price_centavos;
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remover colunas 'old_price_reais', 'old_price_centavos', 'new_price_reais' e  'new_price_centavos';
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Salvar o DataFrame no banco de dados SQLite
conn = sqlite3.connect('../data/quotes.db')
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)
conn.close()


# pd.options.display.max_columns = None
print(df.head())