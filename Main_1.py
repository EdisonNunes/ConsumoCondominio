import streamlit as st
import pandas as pd

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import locale

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

@st.cache_data  # Coloca os dados no Cache
def gerar_df():
    df = pd.read_excel(
        io='ConsumoCond.xlsx',
        engine='openpyxl',
        sheet_name='Consumo',
        usecols='A:C',
        nrows= 208
    )

    df['ANO_NUM'] = df['Data'].dt.year
    df['ANO_NUM'] = df['ANO_NUM'].astype(str)
    df['MES_NUM'] = df['Data'].dt.month
    df['MES_STR'] = df['Data'].dt.strftime('%b')
    df['Consumo'] = df['Consumo'].fillna(0.0).astype(int)
    return df


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
df = gerar_df()

# Side bar
with st.sidebar:
    st.subheader('Conjunto Residencial Jardim Sabará')
    logo = Image.open('Logo.jpg')
    #st.image(logo, use_column_width=True)
    st.image(logo)

    st.subheader('SELEÇÃO DE FILTROS')
    fAno = st.selectbox('ANO',
                        options=df['ANO_NUM'].unique(),
                        index= 8)

    dadosAno = df.loc[(
        df['Data'] == fAno
    )]
    fEmpresa = st.selectbox('EMPRESA',
                            options=df['Empresa'].unique()
                            )

    dadosUsuario = df.loc[(
        df['Empresa'] == fEmpresa) & (df['ANO_NUM'] == fAno)
    ]


updateDatas = dadosUsuario['Data'].dt.strftime('%Y/%b')
dadosUsuario['Data']= updateDatas[0:]

updateAno = dadosAno['Data'].dt.strftime('%Y')
dadosAno = updateAno[0:]

if fEmpresa == 'Sabesp':
    Unidade = 'm³'
else:
    Unidade = 'kw'
st.header('TOTAIS CONSUMIDOS EM '+ fAno + ' [' + Unidade + ']')
st.markdown('**Empresa selecionada:** '+ fEmpresa)

#
#grafico = alt.Chart(dadosUsuario).mark_line(
#    point=alt.OverlayMarkDef(color='red', size=20)
#).encode(
#    x= 'MES_STR:N',   # x= 'ANO_NUM:T',
#    #x= 'Data',
#    y= 'Consumo',
#    strokeWidth = alt.value(3)

#).properties(
#    height = 700,
#    width = 500 #1500
#
#)

#print(grafico.to_json())
#st.altair_chart(grafico)

#fig, ax = plt.subplots(figsize=(15, 10))
fig, ax = plt.subplots()

x = dadosUsuario['MES_STR']
y = dadosUsuario['Consumo']

barras = plt.barh(x,y)

plt.bar_label(barras, labels=dadosUsuario['Consumo'], padding=3, fontsize=10, fontweight='bold')
plt.ylabel('Meses do Ano')
plt.xlabel('Valor consumido em ' + Unidade)
#plt.show()

st.pyplot(fig)