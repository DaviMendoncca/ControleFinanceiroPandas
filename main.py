import pandas as pd
import locale


try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
    except locale.Error:
        print("Atenção: Locale não configurado. Os meses podem aparecer em Inglês.")


df = pd.read_csv('GastosReceitas.csv', #lê o csv no  utf-8
                 encoding='utf-8',
                 sep=';')

df = df.dropna(how='all') #apaga todas as linhas nulas
df['Valor'] = (df['Valor'].astype(str).str.replace('R$', '', regex=False) #trata o dataframe como str e substitui $ por nada
               .str.replace('.', '', regex=False) # substitui . por nada
               .str.replace(',', '.', regex=False)# substitui , por .
               .str.replace(' ', '', regex=False)# substitui espaço por nada
               .str.strip()) # apaga espaços desnecessários



df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce') # transforma a coluna Valor do dataframe em float


df['Data'] = pd.to_datetime(df['Data']) # transforma a coluna Data em DateTime
df = df.set_index('Data').sort_index() # declara a coluna Data como index para tratar o dataframe pela data

saldo_total = df['Valor'].sum() #soma todas as receitas e despesas
saldo_mensal = df['Valor'].resample('ME').sum().to_frame() # soma todos os valores no intervalode um mês e transforma saldo_mesal em df
saldo_mensal.columns = ['Saldo Mensal'] # adiciona um nome pra coluna dos valores



print("\n✅ DataFrame Após Limpeza e Conversão com Formato Brasileiro:")
saldo_mensal.index.name = None # oculta o nome do index data
print(df)
print(f'\nSaldo Total: {saldo_total}')
saldo_mensal.index = saldo_mensal.index.strftime('%b').str.capitalize() # troca a data pelo nome do mês no index
print(saldo_mensal)

    

