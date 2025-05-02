import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import io
import streamlit as st

st.set_page_config(page_title='Análise de vendas de games', layout='wide')

# Load the dataset
df = pd.read_csv('vgsales.csv')
column_names = df.columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Sidebar menu
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
            st.write('**Colunas disponíveis no arquivo:**')
            for i, col in enumerate(column_names, start=1):
                st.write(f'{i}. {col}')
        case 'Número de linhas e colunas':
            st.write(f'**Número de linhas:** {df.shape[0]} | **Número de colunas:** {df.shape[1]}')
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
                st.write(f'**Total de vendas globais:** {jogo_filter['Global_Sales'].sum():.2f} milhões')

def filtro_vendas(op):
    st.header('Filtros de Vendas')
    op = st.selectbox('Selecione uma opção:', [
        'Filtrar jogos por ano',
        'Filtrar jogos por empresa',
        'Filtrar jogos por número de vendas',
        'Filtrar por continente',
        'Ver vendas globais',
        'Filtrar por jogos mais vendidos',
        'Filtrar por nome do jogo'
    ])

    match op:
        case 'Filtrar jogos por ano':
            ano = st.number_input('Digite o ano:', min_value=1980, max_value=2020, step=1)
            if st.button('Filtrar', key='filter_year'):
                jogo_filter = df[df['Year'] == ano]
                if not jogo_filter.empty:
                    st.write(f'**Jogos lançados em {ano}:**')
                    st.dataframe(jogo_filter[['Name', 'Rank', 'Year', 'Publisher', 'Genre']])
                    st.write(f'**Total de vendas globais:** {jogo_filter['Global_Sales'].sum():.2f} milhões')
                else:
                    st.write(f'Nenhum jogo encontrado para o ano {ano}.')
        case 'Filtrar jogos por empresa':
            empresa = st.text_input('Digite o nome da empresa:')
            if st.button('Filtrar', key='filter_company'):
                jogo_filter = df[df['Publisher'].str.contains(empresa, case=False, na=False)]
                if not jogo_filter.empty:
                    st.write(f'**Jogos lançados por {empresa}:**')
                    st.dataframe(jogo_filter[['Name', 'Publisher']])
                else:
                    st.write(f'Nenhuma empresa encontrada com o nome {empresa}.')
        case 'Filtrar jogos por número de vendas':
            valor_venda = st.number_input('Digite o valor mínimo de vendas (em milhões):', min_value=0.0, step=0.1)
            if st.button('Filtrar', key='filter_sales'):
                regioes = ['JP_Sales', 'EU_Sales', 'NA_Sales', 'Other_Sales']
                filtro = df[df[regioes].gt(valor_venda).any(axis=1)]
                if not filtro.empty:
                    st.write('**Jogos com vendas acima do valor especificado:**')
                    for _, linha in filtro.iterrows():
                        st.write(f'**Jogo:** {linha['Name']} | **Empresa:** {linha['Publisher']}')
                        for coluna in regioes:
                            st.write(f'{coluna}: {linha[coluna]} milhões')
                else:
                    st.write(f'Nenhum jogo encontrado com vendas acima de {valor_venda} milhões.')
        case 'Filtrar por continente':
            continente = st.selectbox('Selecione o continente:', ['EU_Sales', 'NA_Sales', 'JP_Sales', 'Other_Sales'])
            empresa = st.text_input('Digite o nome da empresa:')
            filtrar_vendas = st.checkbox('Filtrar por valor de vendas?')
            if filtrar_vendas:
                valor_venda = st.number_input('Digite o valor mínimo de vendas (em milhões):', min_value=0.0, step=0.1)
            if st.button('Filtrar', key='filter_continent'):
                filtro = df[df['Publisher'].str.contains(empresa, case=False, na=False)]
                if filtrar_vendas:
                    filtro = filtro[filtro[continente] > valor_venda]
                    st.write(f'**Vendas de {empresa} em {continente} acima de {valor_venda} milhões:**')
                else:
                    st.write(f'**Vendas de {empresa} em {continente}:**')
                if not filtro.empty:
                    st.dataframe(filtro[['Name', 'Publisher', continente]])
                else:
                    st.write(f'Nenhum jogo encontrado para {empresa} em {continente}.')
        case 'Ver vendas globais':
            filtrar = st.checkbox('Filtrar por valor de vendas?')
            if filtrar:
                valor = st.number_input('Digite o valor mínimo de vendas globais (em milhões):', min_value=0.0, step=0.1)
                if st.button('Filtrar', key='filter_global'):
                    filtro = df[df['Global_Sales'] > valor]
                    if not filtro.empty:
                        st.write(f'**Vendas globais acima de {valor} milhões:**')
                        st.dataframe(filtro[['Name', 'Publisher', 'Global_Sales']])
                    else:
                        st.write(f'Nenhum jogo encontrado com vendas globais acima de {valor} milhões.')
            else:
                total_vendas = df['Global_Sales'].sum()
                st.write(f'**Total de vendas globais:** {total_vendas:.2f} milhões')
        case 'Filtrar por jogos mais vendidos':
            filtrar_qtd = st.checkbox('Filtrar por quantidade específica?')
            if filtrar_qtd:
                qtd = st.number_input('Digite a quantidade de jogos:', min_value=1, step=1)
                if st.button('Filtrar', key='filter_top_sales'):
                    big_vendas = df.sort_values(by='Global_Sales', ascending=False).head(qtd)
                    st.write(f'**Top {qtd} jogos mais vendidos:**')
                    st.dataframe(big_vendas[['Name', 'Publisher', 'Global_Sales']])
                    # Note: Plotly import was missing in original code, omitting chart for now
            else:
                big_venda = df.loc[df['Global_Sales'].idxmax()]
                st.write(f'**Jogo mais vendido:** {big_venda['Name']} | **Empresa:** {big_venda['Publisher']} | **Vendas:** {big_venda['Global_Sales']:.2f} milhões')
        case 'Filtrar por nome do jogo':
            jogo = st.selectbox('Selecione o nome do jogo:', df['Name'].sort_values().unique())
            if st.button('Filtrar', key='filter_game_name'):
                jogo_filter = df[df['Name'] == jogo]
                if not jogo_filter.empty:
                    st.write(f'**Detalhes do jogo: {jogo}**')
                    for _, linha in jogo_filter.iterrows():
                        st.write(f'**Rank:** {linha['Rank']}')
                        st.write(f'**Empresa:** {linha['Publisher']}')
                        st.write(f'**Vendas Globais:** {linha['Global_Sales']:.2f} milhões')
                        st.write(f'**Vendas NA:** {linha['NA_Sales']:.2f} milhões')
                        st.write(f'**Vendas EU:** {linha['EU_Sales']:.2f} milhões')
                        st.write(f'**Vendas JP:** {linha['JP_Sales']:.2f} milhões')
                        st.write(f'**Vendas Outros:** {linha['Other_Sales']:.2f} milhões')
                else:
                    st.write(f'Jogo {jogo} não encontrado.')

def listar_games(op):
    op = st.selectbox('Selecione uma opção:', [
        'Todos os jogos',
        'Quantidade de jogos em específico'
    ])

    match op:
        case 'Todos os jogos':
            st.write('**Lista de todos os jogos:**')
            st.dataframe(df[['Name']])
        case 'Quantidade de jogos em específico':
            qtd = st.number_input('Digite a quantidade de jogos:', min_value=1, step=1)
            if st.button('Filtrar', key='filter_qty_games'):
                jogos = df[['Name']].head(qtd)
                st.write(f'**Primeiros {qtd} jogos:**')
                st.dataframe(jogos)

# Main logic
if op == 'Informações sobre o arquivo':
    inf_arv(op)
elif op == 'Vendas':
    filtro_vendas(op)
elif op == 'Listar jogos':
    listar_games(op)
elif op == 'Ocorrências':
    st.write('Funcionalidade de Ocorrências ainda não implementada.')