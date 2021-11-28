# biblioteca
import sqlalchemy
import pandas as pd

## conexao
engine = sqlalchemy.create_engine('mysql+pymysql://root:Nebulosa@2022@localhost:3306/DATABASE_CRM')

##queries

tabela1 = '''
select  DATE_FORMAT(DATA_VENDA,'%%Y') as ANO, DATE_FORMAT(DATA_VENDA,'%%m') as MES, sum(QTD_VENDA)as QTD_VENDA from vendas v 
group by ANO,MES
order by ANO,MES asc;
'''

tabela2 = '''
select sum(QTD_VENDA)as QTD_VENDA , MARCA , LINHA, sum(QTD_VENDA)as QTD_VENDA from vendas v 
group by  MARCA , LINHA
order by MARCA , LINHA  asc;
'''

tabela3 = '''
select MARCA, DATE_FORMAT(DATA_VENDA,'%%Y') as ANO, DATE_FORMAT(DATA_VENDA,'%%m') as MES, sum(QTD_VENDA)as QTD_VENDA  from vendas v 
group by MARCA,ANO,MES
order by ANO,MES asc;
'''

tabela4 = '''
select  LINHA, DATE_FORMAT(DATA_VENDA,'%%Y') as ANO, DATE_FORMAT(DATA_VENDA,'%%m') as MES, sum(QTD_VENDA)as QTD_VENDA from vendas v 
group by LINHA,ANO,MES
order by ANO,MES asc;
'''

## Criandos os dataframes
df_tabela1 = pd.read_sql_query(tabela1,engine)
df_tabela2 = pd.read_sql_query(tabela2,engine)
df_tabela3 = pd.read_sql_query(tabela3,engine)
df_tabela4 = pd.read_sql_query(tabela4,engine)

# função de remover caracteres
def remove_accents(marca):
    marca = marca.replace('BOTIC�RIO', 'BOTICARIO')
    return marca

# limpando caracteres dos dataframes

df_tabela2['MARCA'] = df_tabela2['MARCA'].apply(remove_accents)
df_tabela3['MARCA'] = df_tabela3['MARCA'].apply(remove_accents)

# Salvando dataframes na banco

df_tabela1.to_sql(
    name = 'CONSOLIDADO_VENDAS_ANO-MES',
    con = engine,
    index = False,
    if_exists ='append'
)

df_tabela2.to_sql(
    name = 'CONSOLIDADO_VENDAS_MARCA-LINHA',
    con = engine,
    index = False,
    if_exists ='append'
)

df_tabela3.to_sql(
    name = 'CONSOLIDADO_VENDAS_MARCA-ANO-MES',
    con = engine,
    index = False,
    if_exists ='append'
)

df_tabela4.to_sql(
    name = 'CONSOLIDADO_VENDAS_LINHA-ANO-MES',
    con = engine,
    index = False,
    if_exists ='append'
)