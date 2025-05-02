import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Configuração da página
st.set_page_config(page_title='Análise de Vendas de Games', layout='wide')

# Verifica se o arquivo existe
csv_file = 'vgsales.csv'
if not os.path.exists(csv_file):
    st.error(f"Arquivo {csv_file} não encontrado. Certifique-se de que o arquivo está no diretório correto.")
    st.stop()

# Carrega o dataset
df = pd.read_csv(csv_file)
# Garante que a coluna 'Year' seja tratada como inteiros, lidando com valores nulos
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
column_names = df.columns

# Configurações de exibição do pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Menu lateral
op = st.sidebar.selectbox('Escolha a opção que lhe atende', [
    'Informações sobre o arquivo',
    'Vendas',
    'Listar jogos',
    'Ocorrências',
    'Métricas Avançadas'
], key='main_menu')

st.title('Análise de Venda de Games')
st.markdown('Uma análise realizada com base em dados fornecidos pela CyberEdux')

# CSS personalizado para cartões de métricas e detalhes de jogos
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #4F1C51 0%, #6B2D6D 100%);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 10px;
        color: white;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 1.2em;
        color: #FFFFFF;
    }
    .metric-card p {
        margin: 5px 0 0;
        font-size: 1.5em;
        font-weight: bold;
    }
    .game-card {
        background: linear-gradient(135deg, #4F1C51 0%, #6B2D6D 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
        color: white;
        animation: fadeIn 0.5s ease-in;
    }
    .game-card h2 {
        margin: 0 0 10px;
        font-size: 1.8em;
        color: #FFFFFF;
    }
    .game-card p {
        margin: 5px 0;
        font-size: 1.1em;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

def inf_arv():
    st.header('Informações sobre o arquivo')
    op = st.sidebar.selectbox('Selecione uma opção:', [
        'Título das colunas',
        'Número de linhas e colunas',
        'Tipos de dados contidos no arquivo analisado',
        'Lançamentos por ano'
    ], key='inf_option')
    
    if op == 'Título das colunas':
        st.subheader('Colunas do Arquivo')
        st.markdown('Lista de todas as colunas disponíveis no conjunto de dados.')
        columns_df = pd.DataFrame({
            'Índice': range(1, len(column_names) + 1),
            'Nome da Coluna': column_names
        })
        styled_df = columns_df.style.set_properties(**{
            'background-color': '#4F1C51',
            'color': 'white',
            'text-align': 'left',
            'border-color': '#d3d3d3',
            'border-style': 'solid',
            'border-width': '1px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
        ])
        st.dataframe(styled_df, use_container_width=True)
    
    elif op == 'Número de linhas e colunas':
        st.subheader('Dimensões do Arquivo')
        st.markdown('Informações sobre o tamanho do conjunto de dados.')
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Número de Linhas", value=f"{df.shape[0]:,}")
        with col2:
            st.metric(label="Número de Colunas", value=df.shape[1])
    
    elif op == 'Tipos de dados contidos no arquivo analisado':
        st.subheader('Tipos de Dados')
        st.markdown('Detalhes sobre os tipos de dados e valores não nulos em cada coluna.')
        dtypes_df = pd.DataFrame({
            'Coluna': df.columns,
            'Tipo de Dado': [str(dtype) for dtype in df.dtypes],
            'Valores Não Nulos': [df[col].notnull().sum() for col in df.columns]
        })
        styled_dtypes = dtypes_df.style.set_properties(**{
            'background-color': '#4F1C51',
            'color': 'white',
            'text-align': 'center',
            'border-color': '#d3d3d3',
            'border-style': 'solid',
            'border-width': '1px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#2196F3'), ('color', 'white'), ('font-weight', 'bold')]}
        ]).highlight_max(subset=['Valores Não Nulos'], color='#e6f3e6')
        st.dataframe(styled_dtypes, use_container_width=True)
    
    elif op == 'Lançamentos por ano':
        st.subheader('Lançamentos por Ano')
        st.markdown('Filtre os jogos lançados em um ano específico e veja os detalhes.')
        ano = st.sidebar.slider('Selecione o ano para filtrar:', min_value=1980, max_value=2020, value=1980, step=1, key='inf_year')
        if st.sidebar.button('Filtrar', key='inf_filter_year'):
            jogo_filter = df[df['Year'] == ano]
            if not jogo_filter.empty:
                st.write(f'**Jogos lançados em {ano}**')
                styled_filter = jogo_filter[['Name', 'Rank', 'Year', 'Publisher', 'Genre']].style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#FF5722'), ('color', 'white'), ('font-weight', 'bold')]}
                ])
                st.dataframe(styled_filter, use_container_width=True)
                total_sales = jogo_filter['Global_Sales'].sum()
                st.metric(label="Total de Vendas Globais", value=f"{total_sales:.2f} milhões")
                releases_per_year = df['Year'].value_counts().sort_index()
                avg_releases = releases_per_year.mean()
                plot_data = pd.DataFrame({
                    'Ano': [str(ano), 'Média Anual'],
                    'Número de Lançamentos': [len(jogo_filter), avg_releases]
                })
                fig = px.bar(
                    plot_data,
                    x='Ano',
                    y='Número de Lançamentos',
                    title=f'Lançamentos em {ano} vs Média Anual',
                    labels={'Número de Lançamentos': 'Número de Lançamentos', 'Ano': 'Ano'},
                    text='Número de Lançamentos',
                    color='Ano',
                    color_discrete_map={str(ano): '#FF5722', 'Média Anual': '#4CAF50'}
                )
                fig.update_traces(texttemplate='%{text:.0f}', textposition='auto')
                fig.update_layout(
                    xaxis_title='Ano',
                    yaxis_title='Número de Lançamentos',
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f'Nenhum jogo encontrado para o ano {ano}.')

def filtro_vendas():
    st.header('Filtros de Vendas')
    op = st.sidebar.selectbox('Selecione uma opção:', [
        'Filtrar jogos por ano',
        'Filtrar jogos por empresa',
        'Filtrar jogos por número de vendas',
        'Filtrar por continente',
        'Ver vendas globais',
        'Filtrar por jogos mais vendidos',
        'Filtrar por nome do jogo',
        'Ver métricas'
    ], key='vendas_option')

    if op == 'Filtrar jogos por ano':
        ano = st.sidebar.slider('Selecione o ano:', min_value=1980, max_value=2020, value=1980, step=1, key='vendas_year')
        if st.sidebar.button('Filtrar', key='vendas_filter_year'):
            jogo_filter = df[df['Year'] == ano]
            if not jogo_filter.empty:
                st.write(f'**Jogos lançados em {ano}:**')
                styled_filter = jogo_filter[['Name', 'Rank', 'Year', 'Publisher', 'Genre']].style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#FF5722'), ('color', 'white'), ('font-weight', 'bold')]}
                ])
                st.dataframe(styled_filter, use_container_width=True)
                st.write(f'**Total de vendas globais:** {jogo_filter['Global_Sales'].sum():.2f} milhões')
            else:
                st.warning(f'Nenhum jogo encontrado para o ano {ano}.')
    
    elif op == 'Filtrar jogos por empresa':
        empresa = st.sidebar.selectbox('Selecione a empresa:', sorted(df['Publisher'].dropna().unique()), key='vendas_company')
        if st.sidebar.button('Filtrar', key='vendas_filter_company'):
            jogo_filter = df[df['Publisher'] == empresa]
            if not jogo_filter.empty:
                st.write(f'**Jogos lançados por {empresa}:**')
                styled_filter = jogo_filter[['Name', 'Publisher']].style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
                ])
                st.dataframe(styled_filter, use_container_width=True)
            else:
                st.warning(f'Nenhuma empresa encontrada com o nome {empresa}.')
    
    elif op == 'Filtrar jogos por número de vendas':
        max_sales = df[['JP_Sales', 'EU_Sales', 'NA_Sales', 'Other_Sales']].max().max()
        valor_venda = st.sidebar.slider(
            'Selecione o valor mínimo de vendas (em milhões):',
            min_value=0.0,
            max_value=float(max_sales),
            value=0.0,
            step=0.1,
            key='vendas_sales'
        )
        regioes = ['JP_Sales', 'EU_Sales', 'NA_Sales', 'Other_Sales']
        filtro = df[df[regioes].gt(valor_venda).any(axis=1)]
        if not filtro.empty:
            st.write(f'**Jogos com vendas acima de {valor_venda} milhões em pelo menos uma região:**')
            styled_filter = filtro[['Name', 'Publisher'] + regioes].style.set_properties(**{
                'background-color': '#4F1C51',
                'color': 'white',
                'text-align': 'left',
                'border-color': '#d3d3d3',
                'border-style': 'solid',
                'border-width': '1px'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#2196F3'), ('color', 'white'), ('font-weight', 'bold')]}
            ]).format({col: '{:.2f}' for col in regioes})
            st.dataframe(styled_filter, use_container_width=True)
        else:
            st.warning(f'Nenhum jogo encontrado com vendas acima de {valor_venda} milhões.')
    
    elif op == 'Filtrar por continente':
        continente = st.sidebar.selectbox('Selecione o continente:', ['EU_Sales', 'NA_Sales', 'JP_Sales', 'Other_Sales'], key='vendas_continent')
        empresa = st.sidebar.selectbox('Selecione a empresa:', sorted(df['Publisher'].dropna().unique()), key='vendas_continent_company')
        filtrar_vendas = st.sidebar.checkbox('Filtrar por valor de vendas?', key='vendas_continent_checkbox')
        if filtrar_vendas:
            valor_venda = st.sidebar.number_input('Digite o valor mínimo de vendas (em milhões):', min_value=0.0, step=0.1, key='vendas_continent_sales')
        if st.sidebar.button('Filtrar', key='vendas_filter_continent'):
            filtro = df[df['Publisher'] == empresa]
            if filtrar_vendas:
                filtro = filtro[filtro[continente] > valor_venda]
                st.write(f'**Vendas de {empresa} em {continente} acima de {valor_venda} milhões:**')
            else:
                st.write(f'**Vendas de {empresa} em {continente}:**')
            if not filtro.empty:
                styled_filter = filtro[['Name', 'Publisher', continente]].style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#FF5722'), ('color', 'white'), ('font-weight', 'bold')]}
                ])
                st.dataframe(styled_filter, use_container_width=True)
            else:
                st.warning(f'Nenhum jogo encontrado para {empresa} em {continente}.')
    
    elif op == 'Ver vendas globais':
        filtrar = st.sidebar.checkbox('Filtrar por valor de vendas?', key='vendas_global_checkbox')
        if filtrar:
            valor = st.sidebar.number_input('Digite o valor mínimo de vendas globais (em milhões):', min_value=0.0, step=0.1, key='vendas_global_sales')
            if st.sidebar.button('Filtrar', key='vendas_filter_global'):
                filtro = df[df['Global_Sales'] > valor]
                if not filtro.empty:
                    st.write(f'**Vendas globais acima de {valor} milhões:**')
                    styled_filter = filtro[['Name', 'Publisher', 'Global_Sales']].style.set_properties(**{
                        'background-color': '#4F1C51',
                        'color': 'white',
                        'text-align': 'left',
                        'border-color': '#d3d3d3',
                        'border-style': 'solid',
                        'border-width': '1px'
                    }).set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
                    ]).format({'Global_Sales': '{:.2f}'})
                    st.dataframe(styled_filter, use_container_width=True)
                else:
                    st.warning(f'Nenhum jogo encontrado com vendas globais acima de {valor} milhões.')
        else:
            total_vendas = df['Global_Sales'].sum()
            avg_sales_per_game = df['Global_Sales'].mean()
            st.markdown(f"""
                <div class="metric-card">
                    <h3>🌍 Total de Vendas Globais</h3>
                    <p>{total_vendas:.2f} milhões</p>
                </div>
            """, unsafe_allow_html=True)
            st.metric(
                label="Total de Vendas Globais",
                value=f"{total_vendas:.2f} milhões",
                delta=f"{total_vendas - avg_sales_per_game * df.shape[0]:+.2f} milhões vs. média esperada",
                delta_color="normal"
            )
    
    elif op == 'Filtrar por jogos mais vendidos':
        filtrar_qtd = st.sidebar.checkbox('Filtrar por quantidade específica?', key='vendas_top_sales_checkbox')
        if filtrar_qtd:
            qtd = st.sidebar.slider('Selecione a quantidade de jogos:', min_value=1, max_value=50, value=10, step=1, key='vendas_top_sales_qty')
            if st.sidebar.button('Filtrar', key='vendas_filter_top_sales'):
                big_vendas = df.sort_values(by='Global_Sales', ascending=False).head(qtd)
                st.write(f'**Top {qtd} jogos mais vendidos:**')
                styled_vendas = big_vendas[['Name', 'Publisher', 'Global_Sales']].style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#2196F3'), ('color', 'white'), ('font-weight', 'bold')]}
                ]).format({'Global_Sales': '{:.2f}'})
                st.dataframe(styled_vendas, use_container_width=True)
                fig = px.bar(big_vendas, x='Name', y='Global_Sales', title='Top Jogos por Vendas Globais')
                st.plotly_chart(fig, use_container_width=True)
        else:
            big_venda = df.loc[df['Global_Sales'].idxmax()]
            st.markdown(f"""
                <div class="metric-card">
                    <h3>🏆 Jogo Mais Vendido</h3>
                    <p>{big_venda['Name']}</p>
                    <p>Empresa: {big_venda['Publisher']}</p>
                    <p>Vendas: {big_venda['Global_Sales']:.2f} milhões</p>
                </div>
            """, unsafe_allow_html=True)
    
    elif op == 'Filtrar por nome do jogo':
        jogo = st.sidebar.selectbox('Selecione o nome do jogo:', sorted(df['Name'].dropna().unique()), key='vendas_game_name')
        if st.sidebar.button('Filtrar', key='vendas_filter_game_name'):
            jogo_filter = df[df['Name'] == jogo].groupby('Name').agg({
                'Rank': 'min',
                'Publisher': 'first',
                'Global_Sales': 'sum',
                'NA_Sales': 'sum',
                'EU_Sales': 'sum',
                'JP_Sales': 'sum',
                'Other_Sales': 'sum',
                'Year': 'first',
                'Genre': 'first',
                'Platform': 'first'
            }).reset_index()
            if not jogo_filter.empty:
                linha = jogo_filter.iloc[0]
                st.write(f'**Detalhes do jogo: {jogo}**')
                st.write(f'**Rank:** {linha['Rank']}')
                st.write(f'**Empresa:** {linha['Publisher']}')
                st.write(f'**Ano:** {int(linha['Year']) if pd.notnull(linha['Year']) else 'Desconhecido'}')
                st.write(f'**Gênero:** {linha['Genre']}')
                st.write(f'**Plataforma:** {linha['Platform']}')
                st.write(f'**Vendas Globais:** {linha['Global_Sales']:.2f} milhões')
                st.write(f'**Vendas NA:** {linha['NA_Sales']:.2f} milhões')
                st.write(f'**Vendas EU:** {linha['EU_Sales']:.2f} milhões')
                st.write(f'**Vendas JP:** {linha['JP_Sales']:.2f} milhões')
                st.write(f'**Vendas Outros:** {linha['Other_Sales']:.2f} milhões')
            else:
                st.warning(f'Jogo {jogo} não encontrado.')
    
    elif op == 'Ver métricas':
        genres = st.sidebar.multiselect(
            'Selecione os gêneros:', 
            sorted(df['Genre'].dropna().unique()),
            key='vendas_metrics_genres'
        )
        plot_type = st.sidebar.selectbox(
            'Selecione o tipo de gráfico:',
            ['Barplot', 'Lineplot', 'Histogram', 'Scatter Plot'],
            key='vendas_metrics_plot_type'
        )
        if st.sidebar.button('Gerar métricas', key='vendas_metrics_button'):
            if genres:
                filtered_df = df[df['Genre'].isin(genres)]
                sales_data = filtered_df.groupby('Genre').agg({
                    'Global_Sales': 'sum',
                    'NA_Sales': 'sum',
                    'EU_Sales': 'sum',
                    'JP_Sales': 'sum',
                    'Other_Sales': 'sum'
                }).reset_index()
                plot_data = []
                for _, row in sales_data.iterrows():
                    for region in ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']:
                        plot_data.append({
                            'Gênero': row['Genre'],
                            'Região': region.replace('_Sales', ''),
                            'Vendas (milhões)': row[region]
                        })
                plot_df = pd.DataFrame(plot_data)
                st.write('**Resumo de vendas por gênero:**')
                styled_sales = sales_data.rename(columns={
                    'Genre': 'Gênero',
                    'Global_Sales': 'Global',
                    'NA_Sales': 'NA',
                    'EU_Sales': 'EU',
                    'JP_Sales': 'JP',
                    'Other_Sales': 'Outros'
                }).style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
                ]).format({col: '{:.2f}' for col in ['Global', 'NA', 'EU', 'JP', 'Outros']})
                st.dataframe(styled_sales, use_container_width=True)
                if plot_type == 'Barplot':
                    fig = px.bar(
                        plot_df,
                        x='Região',
                        y='Vendas (milhões)',
                        color='Gênero',
                        barmode='group',
                        title='Vendas por Gênero e Região',
                        labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                        text='Vendas (milhões)'
                    )
                    fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                elif plot_type == 'Lineplot':
                    fig = px.line(
                        plot_df,
                        x='Região',
                        y='Vendas (milhões)',
                        color='Gênero',
                        title='Vendas por Gênero e Região',
                        labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                        markers=True
                    )
                elif plot_type == 'Histogram':
                    fig = px.histogram(
                        plot_df,
                        x='Região',
                        y='Vendas (milhões)',
                        color='Gênero',
                        barmode='group',
                        title='Vendas por Gênero e Região',
                        labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                        histfunc='sum'
                    )
                elif plot_type == 'Scatter Plot':
                    fig = px.scatter(
                        plot_df,
                        x='Região',
                        y='Vendas (milhões)',
                        color='Gênero',
                        title='Vendas por Gênero e Região',
                        labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                        size='Vendas (milhões)',
                        size_max=20
                    )
                fig.update_layout(
                    xaxis_title='Região',
                    yaxis_title='Vendas (milhões)',
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info('Por favor, selecione pelo menos um gênero.')

def listar_games():
    st.header('Listar Jogos')
    op = st.sidebar.selectbox('Selecione uma opção:', [
        'Todos os jogos',
        'Quantidade de jogos em específico'
    ], key='listar_option')

    if op == 'Todos os jogos':
        st.subheader('Lista de Todos os Jogos')
        st.markdown('Selecione um jogo para ver detalhes e visualizar gráficos de vendas.')
        styled_df = df[['Name']].style.set_properties(**{
            'background-color': '#4F1C51',
            'color': 'white',
            'text-align': 'left',
            'border-color': '#d3d3d3',
            'border-style': 'solid',
            'border-width': '1px',
            'font-size': '14px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
        ])
        selected = st.dataframe(
            styled_df,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            key='listar_game_select',
            height=400
        )
        plot_type = st.sidebar.selectbox(
            'Selecione o tipo de gráfico:',
            ['Barplot', 'Lineplot', 'Histogram', 'Scatter Plot'],
            key='plot_type_select'
        )
        if selected['selection']['rows']:
            selected_index = selected['selection']['rows'][0]
            selected_game = df.iloc[selected_index]
            st.markdown(f"""
                <div class="game-card">
                    <h2>{selected_game["Name"]}</h2>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="flex: 1;">
                            <p><strong>Empresa:</strong> {selected_game["Publisher"]}</p>
                            <p><strong>Ano:</strong> {int(selected_game["Year"]) if pd.notnull(selected_game["Year"]) else "Desconhecido"}</p>
                        </div>
                        <div style="flex: 1;">
                            <p><strong>Gênero:</strong> {selected_game["Genre"]}</p>
                            <p><strong>Plataforma:</strong> {selected_game["Platform"]}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("Detalhes de Vendas"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Vendas Globais", value=f"{selected_game['Global_Sales']:.2f} milhões")
                    st.metric(label="Vendas NA", value=f"{selected_game['NA_Sales']:.2f} milhões")
                with col2:
                    st.metric(label="Vendas EU", value=f"{selected_game['EU_Sales']:.2f} milhões")
                    st.metric(label="Vendas JP", value=f"{selected_game['JP_Sales']:.2f} milhões")
                with col3:
                    st.metric(label="Vendas Outros", value=f"{selected_game['Other_Sales']:.2f} milhões")
            sales_data = {
                'Região': ['Global', 'NA', 'EU', 'JP', 'Outros'],
                'Vendas (milhões)': [
                    selected_game['Global_Sales'],
                    selected_game['NA_Sales'],
                    selected_game['EU_Sales'],
                    selected_game['JP_Sales'],
                    selected_game['Other_Sales']
                ]
            }
            plot_df = pd.DataFrame(sales_data)
            color_map = {
                'Global': '#4CAF50',
                'NA': '#2196F3',
                'EU': '#FF5722',
                'JP': '#FFC107',
                'Outros': '#9C27B0'
            }
            if plot_type == 'Barplot':
                fig = px.bar(
                    plot_df,
                    x='Região',
                    y='Vendas (milhões)',
                    title=f'Vendas de {selected_game["Name"]}',
                    labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                    text='Vendas (milhões)',
                    color='Região',
                    color_discrete_map=color_map
                )
                fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
            elif plot_type == 'Lineplot':
                fig = px.line(
                    plot_df,
                    x='Região',
                    y='Vendas (milhões)',
                    title=f'Vendas de {selected_game["Name"]}',
                    labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                    markers=True,
                    color='Região',
                    color_discrete_map=color_map
                )
            elif plot_type == 'Histogram':
                fig = px.histogram(
                    plot_df,
                    x='Região',
                    y='Vendas (milhões)',
                    title=f'Vendas de {selected_game["Name"]}',
                    labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                    histfunc='sum',
                    color='Região',
                    color_discrete_map=color_map
                )
            elif plot_type == 'Scatter Plot':
                fig = px.scatter(
                    plot_df,
                    x='Região',
                    y='Vendas (milhões)',
                    title=f'Vendas de {selected_game["Name"]}',
                    labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                    size='Vendas (milhões)',
                    size_max=20,
                    color='Região',
                    color_discrete_map=color_map
                )
            fig.update_layout(
                xaxis_title='Região',
                yaxis_title='Vendas (milhões)',
                showlegend=True,
                height=500,
                hovermode='x unified'
            )
            fig.update_traces(
                hovertemplate='%{x}<br>Vendas: %{y:.2f} milhões'
            )
            st.plotly_chart(fig, use_container_width=True)

    elif op == 'Quantidade de jogos em específico':
        qtd = st.sidebar.slider('Selecione a quantidade de jogos:', min_value=1, max_value=50, value=10, step=1, key='listar_qty')
        if st.sidebar.button('Filtrar', key='listar_filter_qty_games'):
            jogos = df[['Name']].head(qtd)
            st.write(f'**Primeiros {qtd} jogos:**')
            styled_jogos = jogos.style.set_properties(**{
                'background-color': '#4F1C51',
                'color': 'white',
                'text-align': 'left',
                'border-color': '#d3d3d3',
                'border-style': 'solid',
                'border-width': '1px'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#2196F3'), ('color', 'white'), ('font-weight', 'bold')]}
            ])
            st.dataframe(styled_jogos, use_container_width=True)

def ocorrencias():
    st.header('Análise de Ocorrências')
    op = st.sidebar.selectbox('Selecione uma opção:', [
        'Contagem de jogos por gênero',
        'Contagem de jogos por plataforma',
        'Contagem de jogos por empresa',
        'Distribuição de lançamentos por ano'
    ], key='ocorrencias_option')

    if op == 'Contagem de jogos por gênero':
        st.markdown('Selecione os gêneros para visualizar a contagem de jogos.')
        genres = st.sidebar.multiselect(
            'Selecione os gêneros:',
            sorted(df['Genre'].dropna().unique()),
            key='ocorrencias_genre_select'
        )
        if st.sidebar.button('Filtrar', key='ocorrencias_genre_button'):
            if genres:
                filtered_df = df[df['Genre'].isin(genres)]
                genre_counts = filtered_df['Genre'].value_counts()
                st.write('**Contagem de jogos por gênero selecionado:**')
                styled_genres = genre_counts.reset_index().rename(columns={'index': 'Gênero', 'Genre': 'Quantidade'}).style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
                ])
                st.dataframe(styled_genres, use_container_width=True)
                plot_data = pd.DataFrame({
                    'Gênero': genre_counts.index,
                    'Quantidade': genre_counts.values
                })
                fig = px.bar(
                    plot_data,
                    x='Quantidade',
                    y='Gênero',
                    orientation='h',
                    title='Contagem de Jogos por Gênero',
                    labels={'Quantidade': 'Número de Jogos', 'Gênero': 'Gênero'},
                    text='Quantidade',
                    color_discrete_sequence=['#4CAF50']
                )
                fig.update_traces(texttemplate='%{text:.0f}', textposition='auto')
                fig.update_layout(
                    xaxis_title='Número de Jogos',
                    yaxis_title='Gênero',
                    height=max(400, len(genre_counts) * 30),
                    showlegend=False,
                    font=dict(size=12),
                    hovermode='y unified'
                )
                fig.update_traces(hovertemplate='%{y}<br>Jogos: %{x}')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info('Por favor, selecione pelo menos um gênero.')
    
    elif op == 'Contagem de jogos por plataforma':
        st.markdown('Selecione as plataformas para visualizar a contagem de jogos.')
        platforms = st.sidebar.multiselect(
            'Selecione as plataformas:',
            sorted(df['Platform'].dropna().unique()),
            key='ocorrencias_platform_select'
        )
        if st.sidebar.button('Filtrar', key='ocorrencias_platform_button'):
            if platforms:
                filtered_df = df[df['Platform'].isin(platforms)]
                platform_counts = filtered_df['Platform'].value_counts()
            else:
                filtered_df = df
                platform_counts = df['Platform'].value_counts()
            if not platform_counts.empty:
                st.write('**Contagem de jogos por plataforma selecionada:**')
                styled_platforms = platform_counts.reset_index().rename(columns={'index': 'Plataforma', 'Platform': 'Quantidade'}).style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#2196F3'), ('color', 'white'), ('font-weight', 'bold')]}
                ])
                st.dataframe(styled_platforms, use_container_width=True)
                plot_data = pd.DataFrame({
                    'Plataforma': platform_counts.index,
                    'Quantidade': platform_counts.values
                })
                fig = px.bar(
                    plot_data,
                    x='Quantidade',
                    y='Plataforma',
                    orientation='h',
                    title='Contagem de Jogos por Plataforma',
                    labels={'Quantidade': 'Número de Jogos', 'Plataforma': 'Plataforma'},
                    text='Quantidade',
                    color_discrete_sequence=['#2196F3']
                )
                fig.update_traces(texttemplate='%{text:.0f}', textposition='auto')
                fig.update_layout(
                    xaxis_title='Número de Jogos',
                    yaxis_title='Plataforma',
                    height=max(400, len(platform_counts) * 30),
                    showlegend=False,
                    font=dict(size=12),
                    hovermode='y unified'
                )
                fig.update_traces(hovertemplate='%{y}<br>Jogos: %{x}')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Nenhuma plataforma encontrada com os filtros selecionados.')
        else:
            if not platforms:
                st.info('Por favor, selecione pelo menos uma plataforma ou clique em "Filtrar" para ver todas.')
    
    elif op == 'Contagem de jogos por empresa':
        max_count = st.sidebar.slider(
            'Selecione o número máximo de jogos por empresa:',
            min_value=1,
            max_value=500,
            value=100,
            step=10,
            key='ocorrencias_publisher_count'
        )
        publisher_counts = df['Publisher'].value_counts()
        filtered_publishers = publisher_counts[publisher_counts <= max_count].head(10)
        if not filtered_publishers.empty:
            st.write(f'**Contagem de jogos por empresa (máximo {max_count} jogos, top 10):**')
            styled_publishers = filtered_publishers.reset_index().rename(columns={'index': 'Empresa', 'Publisher': 'Quantidade'}).style.set_properties(**{
                'background-color': '#4F1C51',
                'color': 'white',
                'text-align': 'left',
                'border-color': '#d3d3d3',
                'border-style': 'solid',
                'border-width': '1px'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#FF5722'), ('color', 'white'), ('font-weight', 'bold')]}
            ])
            st.dataframe(styled_publishers, use_container_width=True)
            plot_data = pd.DataFrame({
                'Empresa': filtered_publishers.index,
                'Quantidade': filtered_publishers.values
            })
            fig = px.bar(
                plot_data,
                x='Quantidade',
                y='Empresa',
                orientation='h',
                title='Contagem de Jogos por Empresa (Top 10)',
                labels={'Quantidade': 'Número de Jogos', 'Empresa': 'Empresa'},
                text='Quantidade',
                color_discrete_sequence=['#FF5722']
            )
            fig.update_traces(texttemplate='%{text:.0f}', textposition='auto')
            fig.update_layout(
                xaxis_title='Número de Jogos',
                yaxis_title='Empresa',
                height=400,
                showlegend=False,
                font=dict(size=12),
                hovermode='y unified'
            )
            fig.update_traces(hovertemplate='%{y}<br>Jogos: %{x}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f'Nenhuma empresa encontrada com até {max_count} jogos. Tente aumentar o valor.')
    
    elif op == 'Distribuição de lançamentos por ano':
        year_range = st.sidebar.slider('Selecione o intervalo de anos:', min_value=1980, max_value=2020, value=(1980, 2020), step=1, key='ocorrencias_year_range')
        if st.sidebar.button('Analisar', key='ocorrencias_year'):
            year_counts = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]['Year'].value_counts().sort_index()
            if not year_counts.empty:
                st.write(f'**Distribuição de lançamentos por ano ({year_range[0]} a {year_range[1]}):**')
                styled_years = year_counts.reset_index().rename(columns={'index': 'Ano', 'Year': 'Quantidade'}).style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
                ])
                st.dataframe(styled_years, use_container_width=True)
                plt.figure(figsize=(10, 6))
                sns.lineplot(x=year_counts.index, y=year_counts.values)
                plt.title('Distribuição de Lançamentos por Ano')
                plt.xlabel('Ano')
                plt.ylabel('Quantidade de Jogos')
                plt.grid(True)
                plt.tight_layout()
                plt.savefig('year_distribution.png')
                st.image('year_distribution.png')
                plt.close()
            else:
                st.warning(f'Nenhum jogo encontrado entre {year_range[0]} e {year_range[1]}.')

def metricas_avancadas():
    st.header('Métricas Avançadas')
    op = st.sidebar.selectbox('Selecione uma métrica:', [
        'Métricas Gerais',
        'Top Jogos por Vendas',
        'Distribuição de Vendas por Região',
        'Popularidade de Gêneros',
        'Tendências Temporais',
        'Busca de Jogos'
    ], key='metricas_option')

    if op == 'Métricas Gerais':
        st.subheader('Métricas Gerais do Conjunto de Dados')
        st.markdown('Resumo estatístico dos dados de vendas de jogos, filtrado por década.')
        year_range = st.sidebar.slider(
            'Selecione o intervalo de anos:',
            min_value=1980,
            max_value=2020,
            value=(1980, 2020),
            step=1,
            key='metrics_year_range'
        )
        chart_type = st.sidebar.selectbox(
            'Selecione o tipo de gráfico:',
            ['Pie Chart', 'Donut Chart', 'Bar Chart'],
            key='metrics_chart_type'
        )
        filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        total_games = filtered_df['Name'].nunique()
        total_games_all = df['Name'].nunique()
        oldest_year = int(filtered_df['Year'].min()) if pd.notnull(filtered_df['Year'].min()) else "Desconhecido"
        recent_year = int(filtered_df['Year'].max()) if pd.notnull(filtered_df['Year'].max()) else "Desconhecido"
        avg_sales = filtered_df['Global_Sales'].mean()
        avg_sales_all = df['Global_Sales'].mean()
        publisher, count = (filtered_df['Publisher'].value_counts().idxmax(), 
                          filtered_df['Publisher'].value_counts().max()) if not filtered_df['Publisher'].value_counts().empty else ("N/A", 0)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>🎮 Total de Jogos Únicos</h3>
                    <p>{total_games:,}</p>
                </div>
            """, unsafe_allow_html=True)
            st.metric(
                label="Total de Jogos Únicos",
                value=f"{total_games:,}",
                delta=f"{total_games - total_games_all:+,}" if total_games != total_games_all else None,
                delta_color="inverse"
            )
            st.markdown(f"""
                <div class="metric-card">
                    <h3>💰 Média Global de Vendas</h3>
                    <p>{avg_sales:.2f} milhões</p>
                </div>
            """, unsafe_allow_html=True)
            st.metric(
                label="Média Global de Vendas por Jogo",
                value=f"{avg_sales:.2f} milhões",
                delta=f"{avg_sales - avg_sales_all:+.2f} milhões" if avg_sales != avg_sales_all else None,
                delta_color="normal"
            )
            max_avg_sales = df.groupby(df['Year'] // 10 * 10)['Global_Sales'].mean().max()
            progress = min(avg_sales / max_avg_sales, 1.0) if max_avg_sales > 0 else 0
            st.progress(progress)
            st.caption(f"Comparação com a média máxima por década: {avg_sales:.2f}/{max_avg_sales:.2f} milhões")
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>📅 Anos de Lançamento</h3>
                    <p>{oldest_year} - {recent_year}</p>
                </div>
            """, unsafe_allow_html=True)
            st.metric(
                label="Intervalo de Anos",
                value=f"{oldest_year} - {recent_year}",
                delta=None
            )
            st.markdown(f"""
                <div class="metric-card">
                    <h3>🏢 Editora com Mais Jogos</h3>
                    <p>{publisher} ({count} jogos)</p>
                </div>
            """, unsafe_allow_html=True)
            st.metric(
                label="Editora com Mais Jogos",
                value=f"{publisher} ({count} jogos)",
                delta=None
            )
        st.write("**Resumo das Métricas**")
        summary_data = {
            'Métrica': ['Total de Jogos Únicos', 'Média Global de Vendas', 'Ano Mais Antigo', 'Ano Mais Recente', 'Editora com Mais Jogos'],
            'Valor': [
                f"{total_games:,}",
                f"{avg_sales:.2f} milhões",
                str(oldest_year),
                str(recent_year),
                f"{publisher} ({count} jogos)"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        styled_summary = summary_df.style.set_properties(**{
            'background-color': '#4F1C51',
            'color': 'white',
            'text-align': 'left',
            'border-color': '#d3d3d3',
            'border-style': 'solid',
            'border-width': '1px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
        ])
        st.dataframe(styled_summary, use_container_width=True)
        if not filtered_df.empty:
            publisher_counts = filtered_df['Publisher'].value_counts().head(5)
            publisher_df = pd.DataFrame({
                'Editora': publisher_counts.index,
                'Quantidade': publisher_counts.values
            })
            if chart_type == 'Pie Chart':
                fig = px.pie(
                    publisher_df,
                    names='Editora',
                    values='Quantidade',
                    title='Distribuição dos Top 5 Editores',
                    color_discrete_sequence=['#4CAF50', '#2196F3', '#FF5722', '#FFC107', '#9C27B0']
                )
                fig.update_traces(textinfo='percent+label', textposition='inside')
            elif chart_type == 'Donut Chart':
                fig = px.pie(
                    publisher_df,
                    names='Editora',
                    values='Quantidade',
                    title='Distribuição dos Top 5 Editores',
                    hole=0.4,
                    color_discrete_sequence=['#4CAF50', '#2196F3', '#FF5722', '#FFC107', '#9C27B0']
                )
                fig.update_traces(textinfo='percent+label', textposition='inside')
            else:
                fig = px.bar(
                    publisher_df,
                    x='Editora',
                    y='Quantidade',
                    title='Distribuição dos Top 5 Editores',
                    color='Editora',
                    color_discrete_sequence=['#4CAF50', '#2196F3', '#FF5722', '#FFC107', '#9C27B0'],
                    text='Quantidade'
                )
                fig.update_traces(texttemplate='%{text:.0f}', textposition='auto')
            fig.update_layout(
                height=400,
                showlegend=True,
                xaxis_title='Editora',
                yaxis_title='Quantidade de Jogos'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado disponível para o intervalo selecionado.")
    
    elif op == 'Top Jogos por Vendas':
        st.subheader('Top Jogos por Vendas')
        st.markdown('Visualize os jogos mais vendidos com filtros personalizados.')
        sales_type = st.sidebar.selectbox(
            'Selecione o tipo de vendas:',
            ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
            key='top_sales_type'
        )
        n_games = st.sidebar.slider(
            'Selecione o número de jogos a exibir:',
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            key='top_n_games'
        )
        platforms = st.sidebar.multiselect(
            'Filtrar por plataforma:',
            sorted(df['Platform'].dropna().unique()),
            key='top_platform_filter'
        )
        genres = st.sidebar.multiselect(
            'Filtrar por gênero:',
            sorted(df['Genre'].dropna().unique()),
            key='top_genre_filter'
        )
        publishers = st.sidebar.multiselect(
            'Filtrar por editora:',
            sorted(df['Publisher'].dropna().unique()),
            key='top_publisher_filter'
        )
        if st.sidebar.button('Filtrar', key='top_filter_button'):
            filtered_df = df.copy()
            if platforms:
                filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
            if genres:
                filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]
            if publishers:
                filtered_df = filtered_df[filtered_df['Publisher'].isin(publishers)]
            if not filtered_df.empty:
                top_games = filtered_df.sort_values(by=sales_type, ascending=False).head(n_games)
                st.write(f'**Top {n_games} jogos por {sales_type.replace("_Sales", "")}**')
                styled_top = top_games[['Name', 'Platform', 'Year', sales_type]].style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#FF5722'), ('color', 'white'), ('font-weight', 'bold')]}
                ]).format({sales_type: '{:.2f}'})
                st.dataframe(styled_top, use_container_width=True)
                fig = px.bar(
                    top_games,
                    y='Name',
                    x=sales_type,
                    orientation='h',
                    title=f'Top {n_games} Jogos por {sales_type.replace("_Sales", "")}',
                    labels={sales_type: 'Vendas (milhões)', 'Name': 'Jogo'},
                    hover_data=['Name', 'Platform', 'Year'],
                    text=sales_type
                )
                fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                fig.update_layout(
                    yaxis_title='Jogo',
                    xaxis_title='Vendas (milhões)',
                    height=600,
                    yaxis={'autorange': 'reversed'}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Nenhum jogo encontrado com os filtros selecionados.')
    
    elif op == 'Distribuição de Vendas por Região':
        st.subheader('Distribuição de Vendas por Região')
        st.markdown('Veja como as vendas são distribuídas entre as regiões.')
        chart_type = st.sidebar.selectbox(
            'Selecione o tipo de gráfico:',
            ['Pie Chart', 'Treemap'],
            key='region_chart_type'
        )
        decade = st.sidebar.selectbox(
            'Filtrar por década:',
            ['Todas', '1980-1990', '1991-2000', '2001-2010', '2011-2020'],
            key='region_decade'
        )
        if st.sidebar.button('Gerar', key='region_generate_button'):
            filtered_df = df.copy()
            if decade != 'Todas':
                start_year, end_year = map(int, decade.split('-'))
                filtered_df = filtered_df[(filtered_df['Year'] >= start_year) & (filtered_df['Year'] <= end_year)]
            sales_data = {
                'Região': ['NA', 'EU', 'JP', 'Outros'],
                'Vendas (milhões)': [
                    filtered_df['NA_Sales'].sum(),
                    filtered_df['EU_Sales'].sum(),
                    filtered_df['JP_Sales'].sum(),
                    filtered_df['Other_Sales'].sum()
                ]
            }
            total_sales = sum(sales_data['Vendas (milhões)'])
            sales_data['Percentual'] = [100 * sales / total_sales if total_sales > 0 else 0 for sales in sales_data['Vendas (milhões)']]
            sales_df = pd.DataFrame(sales_data)
            st.write('**Resumo de vendas por região:**')
            styled_sales = sales_df.style.set_properties(**{
                'background-color': '#4F1C51',
                'color': 'white',
                'text-align': 'center',
                'border-color': '#d3d3d3',
                'border-style': 'solid',
                'border-width': '1px'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#2196F3'), ('color', 'white'), ('font-weight', 'bold')]}
            ]).format({'Vendas (milhões)': '{:.2f}', 'Percentual': '{:.2f}%'})
            st.dataframe(styled_sales, use_container_width=True)
            if chart_type == 'Pie Chart':
                fig = px.pie(
                    sales_df,
                    names='Região',
                    values='Vendas (milhões)',
                    title='Distribuição de Vendas por Região',
                    labels={'Vendas (milhões)': 'Vendas (milhões)'},
                    hover_data=['Percentual']
                )
                fig.update_traces(textinfo='percent+label', textposition='inside')
            else:
                fig = px.treemap(
                    sales_df,
                    path=['Região'],
                    values='Vendas (milhões)',
                    title='Distribuição de Vendas por Região',
                    labels={'Vendas (milhões)': 'Vendas (milhões)'},
                    hover_data=['Percentual']
                )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    elif op == 'Popularidade de Gêneros':
        st.subheader('Popularidade de Gêneros')
        st.markdown('Compare as vendas de gêneros entre regiões em um intervalo de anos.')
        regions = st.sidebar.multiselect(
            'Selecione as regiões:',
            ['NA_Sales', 'EU_Sales', 'JP_Sales'],
            default=['NA_Sales', 'EU_Sales', 'JP_Sales'],
            key='genre_regions'
        )
        year_range = st.sidebar.slider(
            'Selecione o intervalo de anos:',
            min_value=1980,
            max_value=2020,
            value=(1980, 2020),
            step=1,
            key='genre_year_range'
        )
        if st.sidebar.button('Gerar', key='genre_generate_button'):
            if regions:
                filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
                sales_data = filtered_df.groupby('Genre').agg({region: 'sum' for region in regions}).reset_index()
                plot_data = []
                for _, row in sales_data.iterrows():
                    for region in regions:
                        plot_data.append({
                            'Gênero': row['Genre'],
                            'Região': region.replace('_Sales', ''),
                            'Vendas (milhões)': row[region]
                        })
                plot_df = pd.DataFrame(plot_data)
                st.write('**Vendas por gênero e região:**')
                styled_sales = sales_data.rename(columns={region: region.replace('_Sales', '') for region in regions}).style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
                ]).format({region.replace('_Sales', ''): '{:.2f}' for region in regions})
                st.dataframe(styled_sales, use_container_width=True)
                fig = px.bar(
                    plot_df,
                    x='Gênero',
                    y='Vendas (milhões)',
                    color='Região',
                    barmode='stack',
                    title='Vendas por Gênero e Região',
                    labels={'Vendas (milhões)': 'Vendas (milhões)', 'Gênero': 'Gênero'},
                    text='Vendas (milhões)'
                )
                fig.update_traces(texttemplate='%{text:.2f}', textposition='inside')
                fig.update_layout(
                    xaxis_title='Gênero',
                    yaxis_title='Vendas (milhões)',
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info('Por favor, selecione pelo menos uma região.')
    
    elif op == 'Tendências Temporais':
        st.subheader('Tendências Temporais')
        st.markdown('Visualize a evolução das vendas globais ao longo dos anos.')
        sales_by_year = df.groupby('Year')['Global_Sales'].sum().reset_index()
        sales_by_year = sales_by_year[sales_by_year['Year'].notnull()]
        fig = px.line(
            sales_by_year,
            x='Year',
            y='Global_Sales',
            title='Vendas Globais por Ano',
            labels={'Global_Sales': 'Vendas Globais (milhões)', 'Year': 'Ano'},
            markers=True
        )
        fig.update_layout(
            xaxis_title='Ano',
            yaxis_title='Vendas Globais (milhões)',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif op == 'Busca de Jogos':
        st.subheader('Busca de Jogos')
        st.markdown('Digite o nome do jogo para ver detalhes e análise de vendas.')
        search_query = st.sidebar.text_input('Digite o nome do jogo:', key='search_game')
        chart_type = st.sidebar.selectbox(
            'Selecione o tipo de gráfico:',
            ['Bar Chart', 'Pie Chart'],
            key='search_chart_type'
        )
        if search_query:
            filtered_df = df[df['Name'].str.contains(search_query, case=False, na=False)]
            if not filtered_df.empty:
                st.write(f'**Resultados para: {search_query}**')
                styled_results = filtered_df[['Name', 'Rank', 'Year', 'Publisher', 'Genre', 'Platform', 'Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].style.set_properties(**{
                    'background-color': '#4F1C51',
                    'color': 'white',
                    'text-align': 'left',
                    'border-color': '#d3d3d3',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#FF5722'), ('color', 'white'), ('font-weight', 'bold')]}
                ]).format({
                    'Global_Sales': '{:.2f}',
                    'NA_Sales': '{:.2f}',
                    'EU_Sales': '{:.2f}',
                    'JP_Sales': '{:.2f}',
                    'Other_Sales': '{:.2f}'
                })
                st.dataframe(styled_results, use_container_width=True)
                sales_data = {
                    'Região': ['Global', 'NA', 'EU', 'JP', 'Outros'],
                    'Vendas (milhões)': [
                        filtered_df['Global_Sales'].sum(),
                        filtered_df['NA_Sales'].sum(),
                        filtered_df['EU_Sales'].sum(),
                        filtered_df['JP_Sales'].sum(),
                        filtered_df['Other_Sales'].sum()
                    ]
                }
                sales_df = pd.DataFrame(sales_data)
                if chart_type == 'Bar Chart':
                    fig = px.bar(
                        sales_df,
                        x='Região',
                        y='Vendas (milhões)',
                        title=f'Vendas de Jogos Correspondentes a "{search_query}"',
                        labels={'Vendas (milhões)': 'Vendas (milhões)', 'Região': 'Região'},
                        text='Vendas (milhões)'
                    )
                    fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                else:
                    fig = px.pie(
                        sales_df,
                        names='Região',
                        values='Vendas (milhões)',
                        title=f'Vendas de Jogos Correspondentes a "{search_query}"',
                        labels={'Vendas (milhões)': 'Vendas (milhões)'}
                    )
                    fig.update_traces(textinfo='percent+label', textposition='inside')
                fig.update_layout(
                    xaxis_title='Região',
                    yaxis_title='Vendas (milhões)',
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f'Nenhum jogo encontrado para "{search_query}".')

# Lógica principal
if op == 'Informações sobre o arquivo':
    inf_arv()
elif op == 'Vendas':
    filtro_vendas()
elif op == 'Listar jogos':
    listar_games()
elif op == 'Ocorrências':
    ocorrencias()
elif op == 'Métricas Avançadas':
    metricas_avancadas()