import pandas as pd
import streamlit as st

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQHK2bFmd-RTAoK0YKU1KLO8hAe5MMMAjMqSN_p15zRYYwiUl-Ncvk5xaaWtof5FHW7Tqez1hADZ3gT/pub?output=csv"

try:
    df = pd.read_csv(url, #lê o csv no  utf-8
                    encoding='utf-8',
                    sep=',')

    df = df.dropna(how='all') #apaga todas as linhas nulas
    print(df['Valor'])
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
    saldo_mensal.index.name = 'Mês' # oculta o nome do index data
    print(df)
    print(f'\nSaldo Total: {saldo_total}')
    saldo_mensal.index = saldo_mensal.index.strftime('%b').str.capitalize() # troca a data pelo nome do mês no index
    print(saldo_mensal)
except Exception as ex:
    print("Erro ao ler o arquivo CSV. Verifique se o arquivo 'GastosReceitas.csv' existe e está no formato correto.", ex)

ordem_meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


st.title("Controle Financeiro com Pandas")
st.text("Este é um exemplo de controle financeiro usando Pandas e Streamlit. Os dados são lidos de um arquivo CSV hospedado no Google Sheets, processados e exibidos em um formato amigável.")


st.text(f"Saldo Total: {saldo_total}")

st.dataframe(saldo_mensal)

st.dataframe(df,column_config={
            "Data": st.column_config.DateColumn(
                "Data",
                format="DD/MM/YYYY",
                )
            },)

saldo_mensal.index = pd.Categorical(saldo_mensal.index, categories=ordem_meses, ordered=True)
saldo_mensal = saldo_mensal.sort_index()
#st.bar_chart(saldo_mensal)
