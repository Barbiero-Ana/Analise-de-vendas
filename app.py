import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import io
import streamlit as st

st.set_page_config(page_title='Análise de vendas de games', layout='wide')

df = pd.read_csv('vgsales.csv')
column_names = df.columns
pd.set_option = ('display.max_rows', None)
pd.set_option = ('display.max_columns', None)
pd.set_option = ('display.expand_frame_repr', False)


# ainda alterar essas opções conforme o código se estender
op = st.sidebar.selectbox('Escolha a opção lhe atende', [
    'Informações sobre o arquivo',
    'Vendas',
    'Listar jogos',
    'Ocorrências'
])

st.title('Análise de venda de games')
st.markdown('Uma análise realizada com base em dados fornecidos pela CyberEdux')

def inf_arv(op):
    st.header('Informações sobre o arquivo')
    op = st.selectbox('Selecione uma opção:', ['Título das colunas', 'Número de linhas e colunas', 'Tipos de dados contidos no arquivo analisado', 'Lançamentos por ano'])
    match op:
        case 'Título das colunas':
            st.write('**Colunas disponiveis no arquivo:**')
            for i, col in enumerate(column_names, start=1):
                st.write(f'{i}. {col}')
        case 'Número de linhas e colunas':
            st.write(f'**Número de linhas: {df.shape[0]} | **Número de colunas:** {df.shape[1]}')
        case 'Tipos de dados contidos no arquivo analisado':
            st.write('**Tipos de dados contidos no arquivo:**')
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            st.text(f'\n{info_str}\n')
        case 'Lançamentos por ano':
            ano = st.number_input('Digite o ano para filtrar:', min_value=1980, max_value=2020, step=1)
            if st.button('Filtrar'):
                jogo_filter = df[df['Year'] == ano]
                st.write(f'**Jogos lançados no ano de: {ano}**')
                st.dataframe(jogo_filter[['Name', 'Rank', 'Year', 'Publisher', 'Genre']])
                st.write(f'**Total de vendas globais: {jogo_filter['Global_Sales'].sum():.2f} milhões')

def filtro_vendas(op):
    op = st.selectbox('Selecione uma opção:', [
        'Filtrar jogos por ano', 
        'Filtrar jogos por empresa',
        'Filtrar jogos por número de vendas',
        'Filtrar por continente',
        'Ver vendas globais',
        'Filtrar por jogos mais vendidos'
    ])
    