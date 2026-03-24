import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQHK2bFmd-RTAoK0YKU1KLO8hAe5MMMAjMqSN_p15zRYYwiUl-Ncvk5xaaWtof5FHW7Tqez1hADZ3gT/pub?output=csv"

st.set_page_config(layout="wide")
try:
    df = pd.read_csv(url, #lê o csv no  utf-8
                    encoding='utf-8',
                    sep=',')

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



except Exception as ex:
    print("Erro ao ler o arquivo CSV. Verifique se o arquivo 'GastosReceitas.csv' existe e está no formato correto.", ex)

ordem_meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


st.title("Controle Financeiro com Pandas")
st.text("Este é um exemplo de controle financeiro usando Pandas e Streamlit." \
" Os dados são lidos de um arquivo CSV hospedado no Google Sheets," \
" processados e exibidos em um formato amigável.")

col_esquerda, col_central_direita = st.columns([1, 2])

with col_central_direita:
    st.text(f"Saldo Atual: {saldo_total}")

    st.dataframe(df, width=2000,column_config={
                "Data": st.column_config.DateColumn(
                    "Data",
                    format="DD/MM/YYYY",
                    )
                },)
    st.dataframe(saldo_mensal)
with col_esquerda:
    df_gastos = df[df['Valor'] < 0].copy()
    df_gastos['Valor'] = df_gastos['Valor'].abs()
    print(df_gastos)
    gastos_por_categoria = df_gastos.groupby('Categoria')['Valor'].sum().reset_index()
    pizza = px.pie(gastos_por_categoria, values='Valor', names = 'Categoria', title='Gastos por Categoria')
    st.plotly_chart(pizza)


    saldo_mensal = saldo_mensal.sort_index()
    saldo_mensal['Mês'] = saldo_mensal.index.strftime('%b/%y').str.capitalize()
    df_plot = saldo_mensal.reset_index()
    chart = alt.Chart(df_plot).mark_bar().encode(
    x=alt.X('Mês', sort=None), # O sort=None é o segredo
        y='Saldo Mensal',
        color=alt.condition(
            alt.datum['Saldo Mensal'] > 0,
            alt.value('steelblue'),  # Cor para valores positivos
            alt.value('darkred')     # Cor para valores negativos
        ),
        tooltip=['Mês', 'Saldo Mensal']
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

    saldo_mensal.index = saldo_mensal.index.strftime('%b/%y').str.capitalize() # troca a data pelo nome do mês no index
    saldo_mensal = saldo_mensal.drop('Mês', axis=1) # apaga a coluna mês do df para não ter repetição de dados
    





