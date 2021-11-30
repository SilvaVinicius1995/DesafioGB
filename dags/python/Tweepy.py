# importando bibliotecas
import pandas as pd
import tweepy as tw
import os
import sqlalchemy
from airflow.hooks.base import BaseHook

## lendo arquivo com autenticação

with open('/mnt/c/Users/virodrig/PycharmProjects/pythonProject/dags/python/token.txt', 'r') as tfile:
    consumer_key = tfile.readline().strip('\n')
    consumer_secret = tfile.readline().strip('\n')
    access_token = tfile.readline().strip('\n')
    access_token_secret = tfile.readline().strip('\n')

conn = BaseHook.get_connection('db_mysql_local')
conn_string =  str(conn.host)
password= str(conn.password)
username= str(conn.login)
schema= str(conn.schema)
engineMysql =("mysql+pymysql://"+username+":"+password+"@localhost:3306/"+schema+"")
engine = sqlalchemy.create_engine(engineMysql)

# selecionando nome da linha com mais vendas no mês 12 de 2019
sqlQuery = """SELECT LINHA FROM `CONSOLIDADO_VENDAS_LINHA-ANO-MES` 
WHERE QTD_VENDA = 
(SELECT MAX(QTD_VENDA) FROM `CONSOLIDADO_VENDAS_LINHA-ANO-MES` 
WHERE ANO = 2019 AND MES = 12)
AND ANO = 2019 AND MES = 12"""

df_query = pd.read_sql_query(sqlQuery,engine)
linha = df_query['LINHA'].values[0]

# usando tweepy
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

# buscando palavras
query = "boticario", linha

# Collect tweets
cursor_tweet = tw.Cursor(api.search_tweets,q=query,lang='pt',tweet_mode="extended",result_type="recent").items(50)

# criando dicionario
tweets_dict = {}
tweets_dict = tweets_dict.fromkeys(['id','created_at',  'full_text', 'user'])
list_dict = []

# Executando cursor
for tweet in cursor_tweet:
    for key in tweets_dict.keys():
        id = tweet._json['id']
        created_at = tweet._json['created_at']
        user = tweet._json['user']['screen_name']
        full_text = tweet._json['full_text']
        data = {"id": id,"created_at": created_at, "user": user, "full_text": full_text}
        list_dict.append(data)

# criando dataframe
df = pd.DataFrame(list_dict)
df = df.drop_duplicates()

# inserindo na tabela

df.to_sql(
    name = 'TWEETS',
    con = engine,
    index = True,
    if_exists ='append'
)