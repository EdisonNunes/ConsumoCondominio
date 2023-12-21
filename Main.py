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
                        # options=df['ANO_NUM'].unique(),
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



#updateDatas = dadosUsuario['Data'].dt.strftime('%Y/%b')
#dadosUsuario['Data']= updateDatas[0:]

#updateAno = dadosAno['Data'].dt.strftime('%Y')
#dadosAno = updateAno[0:]



fig, ax = plt.subplots()

# Eixo X
x = dadosUsuario['MES_STR']
# Eixo Y
y = dadosUsuario['Consumo']

# Constroe lista com a Média do Ano
z = int(np.mean(dadosUsuario['Consumo']))
Media=[]
for i in y:
    Media.append(z)

########## Imprime Gráfico
plt.rc('xtick', labelsize=8)

plt.plot(x , y, label=Texto, marker='*')
plt.plot(x , Media, label= 'Consumo médio '+ str(z) + Unidade, color='r')
# plt.xlabel('Meses do Ano')
plt.ylabel('Valor consumido em ' + Unidade)

plt.legend()
plt.grid(True)
st.pyplot(fig, clear_figure=True)
#
#    df_lista = dadosUsuario[['MES_STR', 'Consumo']]
#    df_lista = df_lista.rename(columns={'MES_STR':'MÊS'})
#    st.dataframe(df_lista, hide_index=True, use_container_width=True, height=460)

#b = (
#    Line()
#    .add_xaxis(x)
#    .add_yaxis(Texto,y)
#    .add_yaxis(Texto,Media)
#    .set_global_opts(title_opts=opts.TitleOpts(title="Titulo"))
#    )
#st_pyecharts(b)