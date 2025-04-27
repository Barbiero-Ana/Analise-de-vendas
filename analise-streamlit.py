import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# --- Carregando o dataset ---
df = pd.read_csv('vgsales.csv')

# Ajustes no dataset
df.dropna(subset=['Year'], inplace=True)
df['Year'] = df['Year'].astype(int)

# --- Sidebar para navegação ---
st.sidebar.title('Menu de Navegação')
menu = st.sidebar.radio('Selecione uma seção:', [
    'Métricas Gerais',
    'Top Jogos por Vendas',
    'Distribuição de Vendas por Região',
    'Popularidade de Gêneros',
    'Tendências Temporais',
    'Busca de Jogos'
])

# --- Funções auxiliares ---
def vendas_por_decada(ano):
    if ano < 1990:
        return 'Antes de 1990'
    elif ano <= 2000:
        return '1991-2000'
    elif ano <= 2010:
        return '2001-2010'
    else:
        return '2011-2020'

df['Década'] = df['Year'].apply(vendas_por_decada)

# --- Métricas Gerais ---
if menu == 'Métricas Gerais':
    st.title('Métricas Gerais')
    
    total_jogos = df['Name'].nunique()
    ano_mais_antigo = df['Year'].min()
    ano_mais_recente = df['Year'].max()
    media_vendas_global = df['Global_Sales'].mean()
    editora_top = df['Publisher'].value_counts().idxmax()

    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total de Jogos Únicos', total_jogos)
        st.metric('Ano mais Antigo', ano_mais_antigo)
    with col2:
        st.metric('Ano mais Recente', ano_mais_recente)
        st.metric('Média Global de Vendas por Jogo (M)', f"{media_vendas_global:.2f}")
    
    st.info(f'**Editora com mais jogos publicados:** {editora_top}')

# --- Top Jogos por Vendas ---
elif menu == 'Top Jogos por Vendas':
    st.title('Top Jogos por Vendas')

    num_jogos = st.selectbox('Número de jogos para exibir:', [5, 10, 20])
    tipo_venda = st.selectbox('Tipo de Venda:', ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales'])

    plataforma = st.multiselect('Filtrar por Plataforma:', df['Platform'].unique())
    genero = st.multiselect('Filtrar por Gênero:', df['Genre'].unique())
    editora = st.multiselect('Filtrar por Editora:', df['Publisher'].unique())

    df_filtrado = df.copy()

    if plataforma:
        df_filtrado = df_filtrado[df_filtrado['Platform'].isin(plataforma)]
    if genero:
        df_filtrado = df_filtrado[df_filtrado['Genre'].isin(genero)]
    if editora:
        df_filtrado = df_filtrado[df_filtrado['Publisher'].isin(editora)]

    top_jogos = df_filtrado.sort_values(by=tipo_venda, ascending=False).head(num_jogos)

    fig = px.bar(
        top_jogos,
        x=tipo_venda,
        y='Name',
        orientation='h',
        hover_data=['Platform', 'Year'],
        labels={tipo_venda: 'Vendas (Milhões)', 'Name': 'Nome do Jogo'}
    )
    st.plotly_chart(fig)

# --- Distribuição de Vendas por Região ---
elif menu == 'Distribuição de Vendas por Região':
    st.title('Distribuição de Vendas por Região')

    decada = st.selectbox('Filtrar por Década:', df['Década'].unique())

    df_decada = df[df['Década'] == decada]

    regioes = {
        'América do Norte': df_decada['NA_Sales'].sum(),
        'Europa': df_decada['EU_Sales'].sum(),
        'Japão': df_decada['JP_Sales'].sum(),
        'Outros': df_decada['Other_Sales'].sum()
    }

    fig = px.pie(
        names=regioes.keys(),
        values=regioes.values(),
        title=f'Distribuição de Vendas - {decada}',
        hole=0.4
    )
    st.plotly_chart(fig)

# --- Popularidade de Gêneros ---
elif menu == 'Popularidade de Gêneros':
    st.title('Popularidade de Gêneros')

    ano_range = st.slider('Selecionar intervalo de anos:', int(df['Year'].min()), int(df['Year'].max()), (2000, 2010))

    df_genero = df[(df['Year'] >= ano_range[0]) & (df['Year'] <= ano_range[1])]
    vendas_genero = df_genero.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum()

    vendas_genero = vendas_genero.reset_index()

    fig = px.bar(
        vendas_genero,
        x='Genre',
        y=['NA_Sales', 'EU_Sales', 'JP_Sales'],
        labels={'value': 'Vendas (Milhões)', 'Genre': 'Gênero'},
        title='Popularidade de Gêneros por Região',
        barmode='stack'
    )
    st.plotly_chart(fig)

# --- Tendências Temporais ---
elif menu == 'Tendências Temporais':
    st.title('Tendências Temporais de Vendas Globais')

    vendas_ano = df.groupby('Year')['Global_Sales'].sum().reset_index()

    fig = px.line(
        vendas_ano,
        x='Year',
        y='Global_Sales',
        labels={'Global_Sales': 'Vendas Globais (Milhões)', 'Year': 'Ano'},
        title='Tendência de Vendas Globais por Ano'
    )
    st.plotly_chart(fig)

# --- Busca de Jogos ---
elif menu == 'Busca de Jogos':
    st.title('Busca de Jogos')

    busca = st.text_input('Digite o nome do jogo:')
    
    if busca:
        df_busca = df[df['Name'].str.contains(busca, case=False, na=False)]

        if not df_busca.empty:
            st.dataframe(df_busca)

            vendas_regiao = {
                'NA': df_busca['NA_Sales'].sum(),
                'EU': df_busca['EU_Sales'].sum(),
                'JP': df_busca['JP_Sales'].sum(),
                'Other': df_busca['Other_Sales'].sum()
            }

            fig = px.pie(
                names=vendas_regiao.keys(),
                values=vendas_regiao.values(),
                title=f'Vendas por Região para "{busca}"',
                hole=0.4
            )
            st.plotly_chart(fig)
        else:
            st.warning('Nenhum jogo encontrado com esse nome.')
