#%%
# An order might have multiple items.
# Each item might be fulfilled by a distinct seller.
# All text identifying stores and partners where replaced by the names of Game of Thrones great houses.

# %% 

# Análises:
# preço do frete x distância
# quais os agrupamentos mais frequêntes de lojas de um mesmo pedido
# produtos e lojas com maior avaliação
# produtos mais vendidos, categorias mais vendidas
# distâncias médias. tempo de entrega por distância?
# perfil do consumidor pernambucano

#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
#%%


# %%

def rq(q):
    return pd.read_sql_query(q, con=engine)

# %% Listando colunas das tabelas do dataset e 
# 3 primeiras linhas de cada tabela

nomes_tabelas = rq(
    """SELECT name FROM sqlite_master WHERE type='table';"""
)

for name in nomes_tabelas.values:
    print(name, '\n', rq(f"PRAGMA table_info({name[0]})"))
    print(rq(f"SELECT * FROM {name[0]} LIMIT 3"))

# %% Informações obtidas com apenas 1 tabela por vez

# %% Para qual rating os usuários tendem mais a deixar comentários?

df = rq(
    """SELECT review_score FROM olist_order_reviews
    WHERE review_comment_title IS NOT NULL 
    OR review_comment_message IS NOT NULL"""
)
df.value_counts()

# clientes muito satisfeitos (5 stars)  usualmente deixam mais comentários,
# seguido de clientes muito insatisfeitos (1 star)

# %%

hst = df.value_counts()
ratings = [n[0] for n in hst.index] # desempacotando tuplas
plt.bar(ratings, hst.values )

# %% tamanho dos comentários está associado à ratings?

df = rq(
    """SELECT review_score,
    LENGTH(review_comment_message) AS length
    FROM olist_order_reviews
    WHERE review_comment_message IS NOT NULL
    ORDER BY review_score, length"""
)

# df['tamanho'] = df['review_comment_message'].apply(len)
df

# %%

fig, ax = plt.subplots(5, 1, figsize=(8,10))

for n in range(5):
    dfn = df[df['review_score'] == n+1]
    ax[n].scatter(dfn.index, dfn['length'])

# parece existir um limite de 200 caracteres. A curva parece indicar 
# menores comentários em avaliações positivas

# %%

fig, ax = plt.subplots(2, 3, figsize=(10,7))
ax = ax.flatten()
fig.delaxes(ax[-1])

for n in range(5):
    dfn = df[df['review_score'] == n+1]
    ax[n].set_title(f"Score {n+1}")
    ax[n].hist(dfn['length'], bins=np.arange(0, 200, 20))
    ax[n].set_xlim([0, 200])


# %% quais lojas foram mais frequentemente avaliadas com 5 estrelas

rq(
    """SELECT order_id FROM olist_order_reviews
    WHERE review_score = 5"""
)

# %% relação entre preço do produto e ratings


# %%

# %% qual o perfil do consumidor que escreve um comentário de avaliação?
# como se distribui por rating? por estados?

rq(
    """SELECT order_id FROM olist_order_reviews
    WHERE review_score = 5"""
)

# %% ratings positivos (medidos ao longo do tempo) incentivam a compra de determinado produto?
# avaliações em texto incentivam a compra de produtos?

# %% Lojas com entrega mais rápida conseguiram ter mais receita?


# %% Lojas que ivestiram mais em marketing obtiveram mais receita?