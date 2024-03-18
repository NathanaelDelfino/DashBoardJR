import streamlit as st
import pandas as pd
import plotly.express as px
import math

def is_number(value):
    return isinstance(value, (int, float))

st.set_page_config(layout='wide')
st.title('Clientes JRPDV')




df = pd.read_csv('empresa.csv', sep=';', decimal=',')
df['Data'] = pd.to_datetime(df['Data'])
df = df.sort_values('Data')

df['Month'] = df['Data'].apply(lambda x: str(x.year) + '-' + str(x.month))


listaDeMeses = df['Month'].unique().tolist()
listaDeMeses.insert(0,'Todos')
months = st.sidebar.selectbox("Mês", listaDeMeses)

listaDeClientes = df['Cidade'].unique().tolist()
listaDeClientes.insert(0,'Todas')
cidades = st.sidebar.selectbox("Cidade", listaDeClientes)

listaDeRegimes = df['Regime'].unique().tolist()
listaDeRegimes.insert(0,'Todos')
regime = st.sidebar.selectbox("Regime", listaDeRegimes)


df_filtered = df

if(regime != 'Todos'):
    df_filtered = df[df['Regime'] == regime]

if(months != 'Todos'):
    df_filtered = df_filtered[df_filtered['Month'] == months]

if(cidades != 'Todas'):
    df_filtered = df_filtered[df_filtered['Cidade'] == cidades]
    
    
df_filtered

col1, col2 = st.columns(2)
col3, col4, col5= st.columns(3)


# Crie uma cópia do DataFrame
df_copy = df_filtered.copy()

# Calcule a contagem de cada cidade
counts = df_copy['Cidade'].value_counts()

# Crie uma nova coluna 'Cidade Agrupada' que substitui as cidades com contagem <= 1 por 'Outros'
df_copy['Cidade Agrupada'] = df_copy['Cidade'].apply(lambda x: x if counts.get(x, 0) > 10 else 'Outros')

# Agrupe novamente por 'Cidade Agrupada'
clientes_por_cidade_agrupada = df_copy.groupby('Cidade Agrupada').count().reset_index()

# Crie o gráfico de pizza
fig_clientes_por_cidade_agrupada = px.pie(clientes_por_cidade_agrupada, values='Data', names='Cidade Agrupada', title='Clientes por Cidade', hole=0.5)
col1.plotly_chart(fig_clientes_por_cidade_agrupada, use_container_width=True)

