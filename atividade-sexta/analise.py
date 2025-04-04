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
        print('\nDeseja ver o que?\n1 - Titulo das colunas\n2 - Número de linhas e colunas\n3 - #ainda decidindo... ')
        op = int(input('- '))
        if op == 1:
            info = df.info()
        elif op == 2:
            print(f'\nNúmero de linhas:c {df.shape[0]} | Número de colunas: {df.shape[1]}\n')
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
            print('\nDigite qual continente deseja ver:\n1 - EU_Sales\2 - NA_Sales\n3 - JP_Sales\n4 - Others')
            op = int(input('- '))
            if op == 1:
                vendas = 'EU_Sales'
                decision = input('Deseja filtrar por vendas?\n (S/N): ')
                if decision == 'S'.lower():
                    valor_venda = float(input('\nDigite o valor da venda para poder filtrar: '))
                    print(f'Vendas filtradas por: {vendas} | {valor_venda}\n')
                    print(df[])


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