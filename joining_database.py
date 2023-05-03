#%%

import pandas as pd
import numpy as np
import os

#%% Criando dataframes

fnames = os.listdir('csv')
print(fnames)

# dicionário com os dataframes
frames = {}
for file in fnames:
    chave = file.replace('.csv','').replace('_dataset','')
    arquivo = os.path.join('csv', file)
    frames[chave] = pd.read_csv(arquivo)

#%% Descrever colunas

# %% Criando banco de dados
from sqlalchemy import create_engine
# cria uma conexão com um banco de dados SQLite em memória
# sqlalchemy cria o banco em memória
engine = create_engine('sqlite://', echo=False)

for chave, df in frames.items():
    df.to_sql(chave, con=engine)

#%% Testando queries simples

query = """
SELECT name FROM sqlite_master WHERE type='table';
"""

df_query = pd.read_sql_query(query, con=engine)
df_query

# %%

query = '''
Select * from olist_customers
limit 10
'''

df_query = pd.read_sql_query(query, con=engine)
df_query