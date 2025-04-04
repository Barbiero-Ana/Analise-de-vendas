import pandas as pd

df = pd.read_csv('vgsales.csv') #abrindo e lendo o arquivo

column_names = df.columns
pd.set_option('display.max_rows', None)  # Mostra todas as linhas
pd.set_option('display.max_columns', None)  # Mostra todas as colunas
pd.set_option('display.expand_frame_repr', False) # deve mostrar todos os cabecalhos 



# if 3 -> dar opcao de escolher a quantia de jogos que quer listar

# if 2 -> dar a opcao de filtrar as vendas e deixar o usuário escolher o tipo do filtro

# if 4 -> Lancamento de jogos e deixar a pessoa poder escolher o filtro de quando foi lancado (ano)

# if 5 -> mostrar jogos publicados pela nintendo na (a pessoa escolhe eua ou EU sales) acima de 10 milhoes extra: deixar o usuario escolher se quer nintendo ou outra empresa

# if 6 -> pesquisar o jogo por genero

while True:

    print('\nDigite a opção que deseja:\n1 - Informações sobre o arquivo/dados\n2 - Vendas\n3 - Listar jogos\n4 - Ver lançamentos\n5 - Mostrar jogos publicados')

    op = int(input('- '))


    if op == 1:
        print('\nDeseja ver o que?\n1 - Titulo das colunas\n2 - Número de linhas e colunas\n3 - Ver tipos de dados do arquivo\n4 - #pensando ainda.... ')
        op = int(input('- '))
        if op == 1:
            info = df.info()
        elif op == 2:
            print(f'\nNúmero de linhas:c {df.shape[0]} | Número de colunas: {df.shape[1]}\n')

        elif op == 3:
            info = df.info()
            print(info)



    if op == 2:
        print('Como deseja ver?\n1 - Filtrar por ano\n2 - Filtrar por empresa\n3 - Filtrar por número de vendas\n4 - Filtrar por continente\n5 - ver vendas totais globais')
        op = int(input('- '))


        if op == 1:
            print('\nDigite o ano pelo qual deseja filtrar:')
            filtro = int(input('- '))
            jogo_filter = df[df['Year'] == filtro]
            print(f'\nJogos lançados em: {filtro}')
            print(f'{jogo_filter[['Name', 'Rank', 'Year', 'Publisher', 'Genre']]}\n')
            print(f'\nCom um total de vendas de: {df[df['Year'] == filtro]['Global_Sales'].sum()}')

        elif op == 2:
            name = input('\nDigite o nome da empresa: ')
            jogo_filter = df[df['Publisher'] == name]
            print(f'Jogos lançados por: {name}')
            print(f'{jogo_filter[['Name', 'Publisher']]}')


            # fazer o 3 ainda


        elif op == 4:
            print('\nDigite qual continente deseja ver:\n1 - EU_Sales\n2 - NA_Sales\n3 - JP_Sales\n4 - Others')
            op = int(input('- '))
            if op == 1:
                vendas = 'EU_Sales'
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
                vendas = 'NA_Sales'
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
                vendas = 'JP_Sales'
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
                vendas = 'Other_Sales'
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


    elif op == 3:
        print('\nDigite quantos jogos deseja listar:\n1 - Todos\n2 - inserir quantidade')
        op = int(input('- '))

        if op == 1:
            #inserir o código
            print()
        elif op == 2:
            filtro = int(input('Digite a quantidade de jogos que deseja listar: '))
            n = df['Name'].head(filtro)
            print(f'{n}\n')


        # fazer os outros ainda

    elif op == 5:
        total_vendas = df['Global_Sales'].sum()
        print('\nA venda global em forma total é de:')
        print(f'-> Global Sales: {total_vendas}\n')