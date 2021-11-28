# importando bibliotecas
from TwitterSearch import *
import pandas as pd
import os, json
import sqlalchemy

## lendo arquivo com autenticação

with open('token.txt', 'r') as tfile:
    consumer_key = tfile.readline().strip('\n')
    consumer_secret = tfile.readline().strip('\n')
    access_token = tfile.readline().strip('\n')
    access_token_secret = tfile.readline().strip('\n')
engine = sqlalchemy.create_engine('mysql+pymysql://root:Nebulosa@2022@localhost:3306/DATABASE_CRM')

# selecionando nome da linha com mais vendas no mês 12 de 2019
sqlQuery = """SELECT MAX(LINHA) as LINHA FROM `CONSOLIDADO_VENDAS_LINHA-ANO-MES` WHERE ANO = 2019 AND MES = 12"""
df_query = pd.read_sql_query(sqlQuery,engine)
linha = df_query['LINHA'].values[0]

# criando contador e lista de dicionario
contador = 0
list_dict = []

# usando TwitterSearch

try:

    ts = TwitterSearch(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    tso = TwitterSearchOrder()
    tso.set_keywords(['boticario', linha])
    tso.set_language('pt')
    tso.arguments.update({'tweet_mode': 'extended'})
    tso.set_count(50)

    for tweet in ts.search_tweets_iterable(tso):
        created_at = tweet['created_at']
        user = tweet['user']['screen_name']
        full_text = tweet['full_text']
        data = {"created_at": created_at, "user": user, "full_text": full_text}
        list_dict.append(data)
        contador = contador + 1
        if contador == 50:
            break

except TwitterSearchException as e:  # take care of all those ugly errors if there are some
    print(e)

# criando dataframe
df = pd.DataFrame(list_dict)

df.to_sql(
    name = 'TWEETS',
    con = engine,
    index = False,
    if_exists ='append'
)
