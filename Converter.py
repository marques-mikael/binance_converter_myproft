# Importando as Bibliotecas Necessárias
import pandas as pd
import re
from datetime import datetime

# Carregando os Dados da Planilha Original
# Substitua 'dados_originais.xlsx' pelo nome do seu arquivo
df = pd.read_excel('Transações 12-10-2023 a 31-12-202.xlsx')

# Criando uma Nova Coluna para a Corretora
df['Corretora'] = 'Binance'

# Convertendo a Data para o Formato Desejado
df['Data'] = pd.to_datetime(df['Date(UTC)']).dt.strftime('%d/%m/%Y %H:%M')

# Convertendo a Operação
def converter_operacao(row):
    if row['Side'] == 'BUY':
        return 'Permuta Compra'
    else:
        return 'Permuta Venda'

df['Operação'] = df.apply(converter_operacao, axis=1)

# Calculando a Quantidade e o Preço
"""Calcula a quantidade e o preço de uma operação, considerando o tipo de operação (compra ou venda) e as taxas.
    """
def calcular_quantidade_e_preco(row):
    executed = row['Executed'].strip()
    fee = row['Fee'].strip()
    amount = row['Amount'].strip()

    if row['Side'] == 'BUY':
        quantidade = pd.to_numeric(re.sub(r'[^\d.]', '', executed), errors='coerce') - pd.to_numeric(re.sub(r'[^\d.]', '', fee), errors='coerce')
        preco = pd.to_numeric(re.sub(r'[^\d.]', '', amount), errors='coerce') / quantidade
    else:
        quantidade = pd.to_numeric(re.sub(r'[^\d.]', '', executed), errors='coerce')
        preco = (pd.to_numeric(re.sub(r'[^\d.]', '', amount), errors='coerce') - pd.to_numeric(re.sub(r'[^\d.]', '', fee), errors='coerce')) / quantidade

    return quantidade, preco

df[['Quantidade', 'Preço']] = df.apply(calcular_quantidade_e_preco, axis=1, result_type='expand')

# Selecionando as colunas na ordem desejada
df_novo = df[['Data', 'Corretora', 'Operação', 'Pair', 'Quantidade', 'Preço']]

# Salvando em um novo arquivo Excel
df_novo.to_excel('dados_convertidos.xlsx', index=False)
