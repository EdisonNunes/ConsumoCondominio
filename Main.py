import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import locale

# ####  streamlit run Main.py

#from pyecharts import options as opts
#from pyecharts.charts import Line
#from streamlit_echarts import st_pyecharts

#st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.set_page_config(layout='centered')

@st.cache_data  # Coloca os dados no Cache
def gerar_df():
    df = pd.read_excel('ConsumoCond.xlsx')
    # df = pd.read_excel('ConsumoCondTeste.xlsx')
    df['ANO_NUM'] = df['Data'].dt.year
    df['ANO_NUM'] = df['ANO_NUM'].astype(str)
    df['MES_NUM'] = df['Data'].dt.month
    df['MES_STR'] = df['Data'].dt.strftime('%b') + '/' + df['Data'].dt.strftime('%y')
    df['Consumo'] = df['Consumo'].fillna(0.0).astype(int)
    return df

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
df = gerar_df()
df_last = df.sort_values(['Data'], ascending=[False])

st.title('Conjunto Residencial Jardim Sabará')

col1, col2 = st.columns(2, gap= 'small')

lista_anos = df['ANO_NUM'].unique()
lista_anos_invertida = lista_anos[::-1]
opcao =[]
opcao.append('Últimos 12 meses')
for i in range(0, len(lista_anos_invertida)):
    opcao.append(lista_anos_invertida[i])

with col1:
    fAno = st.selectbox('ANO/PERÍODO',
                        options=opcao,
                        index= 0)
    dadosAno = df.loc[(df['Data'] == fAno)]

with col2:
    fEmpresa = st.selectbox('EMPRESA',
                            options=df['Empresa'].unique()
                            )
    if fEmpresa == 'Sabesp':
        Unidade = 'm³'
    else:
        Unidade = 'kw'

    if fAno == 'Últimos 12 meses':
        dadosUsuario = df_last.loc[(df_last['Empresa'] == fEmpresa)][:12]
        dadosUsuario = dadosUsuario.sort_values(['Data'])
        st.header('Consumo nos últimos 12 meses em ' + Unidade)
        Texto = 'Consumo em 12 meses'
    else:
        dadosUsuario = df.loc[(df['Empresa'] == fEmpresa) & (df['ANO_NUM'] == fAno)]
        st.header('Consumo no ano de ' + fAno + ' em ' + Unidade)
        Texto = 'Consumo em ' + fAno


fig, ax = plt.subplots()

# Eixo X
x = list(dadosUsuario['MES_STR'])
# Eixo Y
y = list(dadosUsuario['Consumo'])
# Constroe lista com a Média do Ano
z = int(np.mean(dadosUsuario['Consumo']))
Media=[]
Ideal=[]
#Marcadores=[]
ConsumoIdeal= 12 * 36 # 12 m³ por apartamento
for i in y:
    Media.append(z)
    Ideal.append(ConsumoIdeal)
    #Marcadores.append('')
#print(Media)
#print(Ideal)
########## Imprime Gráfico
plt.rc('xtick', labelsize=8)
marcadores = np.where(y == np.min(y), '','')

for posicao, marcador in enumerate(marcadores):
    if marcador == '*':
        cor = 'red'
        tamanho = 80
    else:
        cor = 'blue'
        tamanho = 80
    plt.scatter(x[posicao], y[posicao], marker=marcador, s=tamanho, color=cor)
    # adicionando uma anotação para mostrar o menor valor em março
    plt.annotate(y[posicao],
                 color= cor,
                 xy=(x[posicao], y[posicao]),
                 xytext=(-5,5),
                 fontsize=8,
                 textcoords='offset points')
    # print('Posição: ', posicao,'  meses= ',x[posicao],'  vendas= ',y[posicao])


plt.plot(x, y, label=Texto, marker='*')

if fEmpresa == 'Sabesp':
    plt.plot(x, Ideal, label='Consumo ideal mensal ' + str(ConsumoIdeal) + Unidade, marker='*')
    plt.plot(x, Media, label='Média no período ' + str(z) + Unidade, marker='*')
else:
    plt.plot(x, Media, label='Consumo médio ' + str(z) + Unidade, marker='*')

# plt.xlabel('Meses do Ano')
plt.ylabel('Valor consumido em ' + Unidade)

plt.legend()
plt.grid(True)
st.pyplot(fig, clear_figure=True)
