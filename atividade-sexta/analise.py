import pandas as pd
import io

df = pd.read_csv('vgsales.csv') #abrindo e lendo o arquivo
column_names = df.columns
pd.set_option('display.max_rows', None)  # mostra todas as linhas (tira os ... que o pandas resume)
pd.set_option('display.max_columns', None)  # mostra todas as colunas (tira os ... que o pandas resume)
pd.set_option('display.expand_frame_repr', False) # deve mostrar todos os cabecalhos (tira os ... que o pandas resume)

# -> Considerar ideia de trocar os if/else por match case
# if 4 -> Lancamento de jogos e deixar a pessoa poder escolher o filtro de quando foi lancado (ano)
# o global sales é a soma de todas as outras vendas (eu_sales, na_sales, jp_sales)




#-------- info do arqv op 1 ------------------------------------------
def info_arv():
        print('\nDeseja ver o que?\n1 - Titulo das colunas\n2 - Número de linhas e colunas\n3 - Ver tipos de dados do arquivo\n4 - #pensando ainda.... ')
        op = int(input('- '))
        if op == 1:
            print(f'\nColunas disponiveis no arquivo:')
            for i, col in enumerate(column_names, start= 1):
                print(f'{i}. {col}')
        elif op == 2:
            print(f'\nNúmero de linhas: {df.shape[0]} | Número de colunas: {df.shape[1]}\n')

        elif op == 3:
            # deixando o print mais bonitinho
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            print(f'\n{info_str}\n')



#-------- Filtro de vendas op 2 -------------------------------------
def filtro_vendas():
            print('Como deseja ver?\n1 - Filtrar por ano\n2 - Filtrar por empresa\n3 - Filtrar por número de vendas\n4 - Filtrar por continente\n5 - ver vendas globais\n6 - Jogos mais vendidos\n#pensando ainda...')
            op = int(input('- '))

            # por ano
            if op == 1:
                print('\nDigite o ano pelo qual deseja filtrar:')
                filtro = int(input('- '))
                jogo_filter = df[df['Year'] == filtro]
                print(f'\nJogos lançados em: {filtro}')
                print(f'{jogo_filter[['Name', 'Rank', 'Year', 'Publisher', 'Genre']]}\n')
                print(f'\nCom um total de vendas de: {df[df['Year'] == filtro]['Global_Sales'].sum()}')

            # por empresa
            elif op == 2:
                name = input('\nDigite o nome da empresa: ')
                jogo_filter = df[df['Publisher'] == name]
                print(f'Jogos lançados por: {name}')
                print(f'{jogo_filter[['Name', 'Publisher']]}')

            #por valor de venda
            elif op == 3:
                valor_venda = float(input('\nDigite o valor da venda para poder filtrar: '))
                regioes = ['JP_Sales', 'EU_Sales', 'NA_Sales', 'Other_Sales']
                filter = df[df[regioes].gt(valor_venda).any(axis=1)]

                for _, linha in filter.iterrows():
                    print(f'Jogo: {linha['Name']}\nEmpresa: {linha['Publisher']}\nNº de vendas:')
                    for coluna in regioes:
                        print(f'{coluna} : {linha[coluna]} milhões\n')

            # continente
            elif op == 4:
                print('\nDigite qual continente deseja ver:\n1 - EU_Sales\n2 - NA_Sales\n3 - JP_Sales\n4 - Others')
                op = int(input('- '))
                if op == 1:
                    # vendas = 'EU_Sales'
                    decision = input('Deseja filtrar por vendas?\n (S/N): ')
                    if decision == 'S'.lower():
                        valor_venda = float(input('\nDigite o valor da venda para poder filtrar: '))
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        filter_vendas = df[(df['Publisher'] == empresa) & (df['EU_Sales'] > valor_venda)]
                        print(f'\nVendas da empresa: {empresa} na Europa com valores acima de: {valor_venda} milhões')
                        print(filter_vendas[['Name', 'Publisher' ,'EU_Sales']])
                    elif decision == 'N'.lower():
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        filter_vendas = df[df['Publisher'] == empresa]
                        print(f'\nVendas da empresa: {empresa} na Europa')
                        print(filter_vendas[['Name', 'Publisher' ,'EU_Sales']])

                elif op == 2:
                    # vendas = 'NA_Sales'
                    decision = input('Deseja filtrar por vendas?\n (S/N): ')
                    if decision == 'S'.lower():
                        valor_venda = float(input('\nDigite o valor da venda para poder filtrar: '))
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        filter_vendas = df[(df['Publisher'] == empresa) & (df['NA_Sales'] > valor_venda)]
                        print(f'\nVendas da empresa: {empresa} na América do norte com valores acima de: {valor_venda} milhões')
                        print(filter_vendas[['Name', 'Publisher' ,'NA_Sales']])
                    elif decision == 'N'.lower():
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        filter_vendas = df[df['Publisher'] == empresa]
                        print(f'\nVendas da empresa: {empresa} na América do norte')
                        print(filter_vendas[['Name', 'Publisher' ,'NA_Sales']])
                
                elif op == 3:
                    # vendas = 'JP_Sales'
                    decision = input('Deseja filtrar por vendas?\n (S/N): ')

                    if decision.lower() == 's'.lower():
                        valor_venda = float(input('\nDigite o valor da venda para poder filtrar: '))
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        
                        filter_vendas = df[(df['Publisher'] == empresa) & (df['JP_Sales'] > valor_venda)]
                        
                        print(f'\nVendas da empresa: {empresa} no Japão com valores acima de: {valor_venda} milhões')
                        print(filter_vendas[['Name', 'Publisher', 'JP_Sales']])
                        
                    elif decision.lower() == 'n'.lower():
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        
                        filter_vendas = df[df['Publisher'] == empresa]
                        
                        print(f'\nTodas as vendas da empresa: {empresa} no Japão')
                        print(filter_vendas[['Name', 'Publisher', 'JP_Sales']])


                elif op == 4:
                    # vendas = 'Other_Sales'
                    decision = input('Deseja filtrar por vendas?\n (S/N): ')
                    if decision == 'S'.lower():
                        valor_venda = float(input('\nDigite o valor da venda para poder filtrar: '))
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        filter_vendas = df[(df['Publisher'] == empresa) & (df['Other_Sales'] > valor_venda)]
                        print(f'\nVendas da empresa: {empresa} em Outras vendas com valores acima de: {valor_venda} milhões')
                        print(filter_vendas[['Name', 'Publisher' ,'Other_Sales']])
                    elif decision == 'N'.lower():
                        empresa = input('Digite o nome da empresa pela qual deseja filtrar: ')
                        filter_vendas = df[df['Publisher'] == empresa]
                        print(f'\nVendas da empresa: {empresa} em outras vendas')
                        print(filter_vendas[['Name', 'Publisher' ,'Other_Sales']])

            elif op == 5:
                print('Deseja filtrar por venda?')
                decisao = input('S/N - ')

                if decisao == 'S'.lower():
                    print('\nDigite o valor pelo qual deseja filtrar as vendas globais:')
                    filtro = float(input('- '))
                    filter_vendas = df[(df['Global_Sales'] > filtro)]
                    print(f'\nVendas globais com valores acima de: {filtro}')
                    print(filter_vendas[['Name', 'Publisher' ,'Global_Sales']])
                    

                elif decisao == 'N'.lower():
                    total_vendas = df['Global_Sales'].sum()
                    print('\nA venda global em forma total é de:')
                    print(f'-> Global Sales: {total_vendas}\n')

            # filtrando por jogos mais vendidos
            elif op == 6:
                print('\nDeseja escolher uma quantia em especifico ou apenas o jogo que mais aparece?')
                op = input('S/N - ')
                if op == 'S'.lower():
                    qtd = int(input('Digite a quantidade que deseja ver: '))
                    big_vendas = df.sort_values(by='Global_Sales', ascending=False).head(qtd)
                    for i, row in enumerate(big_vendas.itertuples(), start=1):
                        print(f'\n{i}º {row.Name} | Empresa: {row.Publisher} | Número de vendas: {row.Global_Sales:.2f} milhões\n')
                if op == 'N'.lower():
                    big_venda = df.loc[df['Global_Sales'].idxmax()]
                    print(f'Segue o jogo mais vendido:\nNome: {big_venda['Name']} | Empresa: {big_venda['Publisher']} | Número de vendas: {big_venda['Global_Sales']:.2f} milhões')

            # # global sales (quest 15)
            # elif op == 7:
            #     print('Deseja filtrar por venda?')
            #     decisao = input('S/N - ')

            #     if decisao == 'S'.lower():
            #         print('\nDigite o valor pelo qual deseja filtrar as vendas globais:')
            #         filtro = float(input('- '))
            #         filter_vendas = df[(df['Global_Sales'] > filtro)]
            #         print(f'\nVendas globais com valores acima de: {filtro}')
            #         print(filter_vendas[['Name', 'Publisher' ,'Global_Sales']])
                    

            #     elif decisao == 'N'.lower():
            #         total_vendas = df['Global_Sales'].sum()
            #         print('\nA venda global em forma total é de:')
            #         print(f'-> Global Sales: {total_vendas}\n')



#-------- listar os jogs op 3 ---------------------------------------------
def listar_games():
        print('\nDigite quantos jogos deseja listar:\n1 - Todos\n2 - inserir quantidade')
        op = int(input('- '))

        if op == 1:
            n = df['Name']
            print(n)
        elif op == 2:
            filtro = int(input('Digite a quantidade de jogos que deseja listar: '))
            n = df['Name'].head(filtro)
            print(f'{n}\n')
        # fazer os outros ainda


#-------- filtrar por genero op 4 ------------------------------------
def filtr_genero():
        generos = sorted(df['Genre'].unique())
        print('\nGêneros disponiveis:')
        for genero in generos:
            print(f'- {genero}')
        filtro = input('\nDigite o gênero que deseja buscar (favor, digitar igual está na tabela): ')
        filter_games = df[df['Genre'] == filtro]
        print(f'\nJogos do gênero: {filtro}:')
        print(filter_games[['Genre','Name', 'Publisher' ]])


# --------- Ocorrencias op 5 ---------------------------------------
def filtr_ocorren():

    # na op 2 -> colocar uma funcao para que o usuário possa escolher de qual continente ele quer escolher e qual a quantia de jogos com maiores vendas

        print('Qual ocorrência deseja verificar:\n1 - Qual editora mais aparece no documento\n2 - Quais são os jogos com maiores vendas (por continente e/ou globais)\n3 - Diferença de venda entre continentes\n4 - Qual gênero tem o maior total de vendas globais\n5 - ')

        op = int(input('- '))

        if op == 1:
            print('\nDeseja escolher uma quantia em especifico ou apenas o que de fato mais aparece?')
            op = input('S/N - ')

            if op == 'S'.lower():
                n = int(input('Deseja ver quantas editoras que mais aparecem no documento: '))
                m_freq = df['Publisher'].value_counts().head(n) 
                qtd = df['Publisher'].value_counts().max()
                for i, (Publisher, qtd) in enumerate(m_freq.items(), start=1):
                    print(f'{i}º {Publisher} | Apareceu: {qtd} vezes')

            elif op == 'N'.lower():
                m_freq = df['Publisher'].value_counts().idxmax() #o id max retorna o indice de maior valor -> quem mais apareceu
                qtd = df['Publisher'].value_counts().max()
                print(f'A editora/ empresa que mais aparece é: {m_freq} | Apareceu: {qtd} vezes')

        elif op == 2:
            print('Deseja ver maiores vendas por:\n1 - continente\n2 - global')
            op = int(input('- '))
            if op == 1: # continente
                print('Deseja filtrar por:\n1 - valor\n2 - maior ocorrencia de vendas')
                op = int(input('- '))

                if op == 1: # com filtro de valor
                    n = float(input('Digite qual o valor que deseja filtrar a busca: '))
                    continente = {
                        'EU_Sales' : 'Europa',
                        'NA_Sales' : 'América do norte',
                        'JP_Sales' : 'Japão',
                        'Other_Sales' : 'Outros países'
                    }

                    for coluna, nome in continente.items():
                        filter = df[df[coluna] > n][['Name', coluna]]
                        print(f'\nJogos com vendas acima de: {n} em {nome}\n')

                        if filter.empty:
                            print('Nenhum jogo encontrado')
                        else:
                            for i, row in filter.iterrows():
                                print(f'- {row['Name']} | {coluna}: {row[coluna]}')

                elif op == 2: # sem filtro de valor                    
                    continente = {
                        'EU_Sales' : 'Europa',
                        'NA_Sales' : 'América do norte',
                        'JP_Sales' : 'Japão',
                        'Other_Sales' : 'Outros países'
                    }
                    for coluna, nome in continente.items():
                        vendas = df.loc[df[coluna].idxmax()] # pega a linha com maior venda 
                        print(f'\nJogo com maiore número de vendas em: {nome}')
                        print(f'- {vendas['Name']} | {coluna} : {vendas[coluna]}')

            elif op == 2: #global
            # -> apenas por pela maior ocorrencia no ocumento, pois na opcao de vendas já existe a funcao de filtrar por valor 
                continente = {
                            'Vendas globais' : 'Global_Sales'
                        }
                for nome, col in continente.items():
                    top_venda = df.loc[df[col].idxmax()]
                    print(f'\n{nome}\nJogo mais vendido: {top_venda['Name']} | Empresa: {top_venda['Publisher']} | Nº de vendas em escala global: {top_venda[col]} milhões')

        elif op == 3:
            #fazer a dif entre continentes
            print()

        elif op == 4:
            # ver qual dos continentes detem o maior numero de vendas globais 
            print()


# ----- MAIN --------------------------------------------------------
def main():
    while True:

        print('\nDigite a opção que deseja:\n1 - Informações sobre o arquivo/dados\n2 - Vendas\n3 - Listar jogos\n4 - Filtrar jogos por genero\n5 - Ver ocorrências')

        op = int(input('- '))

        if op == 1:
            info_arv()
        elif op == 2:
            filtro_vendas()
        elif op == 3:
            listar_games()
        elif op == 4:
            filtr_genero()
        elif op == 5:
            filtr_ocorren()
        

main()