#====================
#       Library
#====================
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import requests

# tz = pytz.timezone('US/Eastern')



#====================
#     Titles
#====================
st.set_page_config(layout = 'wide', page_title='Incêndios Florestais no Brasil', page_icon='fire', initial_sidebar_state = 'expanded')
st.title('Incêndios Florestais no Brasil ')
st.subheader(' ')
# st.markdown('Neste app..')




#====================
#   Read Data
#====================
@st.cache(allow_output_mutation=True)




#====================
#  Get Data & Create Columns
#====================

# Get Data
def get_data(path):
    df = pd.read_csv('incendios.csv', encoding='latin1', thousands='.', decimal=',', dtype={'number': np.int64})
    df = df.drop(df[df['number'] == 0.0].index)
    df.drop_duplicates()

# Format type
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['year'].astype(int)

# Create new atributes
    df['bioma'] = df['state'].apply(lambda x:
                                    'Amazonia' if (
                                                x == 'Acre' or x == 'Amazonia' or x == 'Amapa' or x == 'Pará' or x == 'Roraima' or x == 'Rondonia' or x == 'Mato Grosso')
                                    else 'Cerrado' if (
                                                x == 'Maranhao' or x == 'Tocantins' or x == 'Goias' or x == 'Distrito Federal' or x == 'Minas Gerais')
                                    else 'Mata Atlantica' if (
                                                x == 'Rio' or x == 'Sao Paulo' or x == 'Espirito Santo' or x == 'Parana' or x == 'Santa Catarina')
                                    else 'Caatinga')
    df['regiao'] = df['state'].apply(lambda x:
                                     'Sudeste' if (
                                                 x == 'Sao Paulo' or x == 'Rio' or x == 'Espirito Santo' or x == 'Minas Gerais')
                                     else 'Sul' if (x == 'Santa Catarina')
                                     else 'Norte' if (
                                                 x == 'Acre' or x == 'Amapa' or x == 'Roraima' or x == 'Pará' or x == 'Amazonas' or x == 'Rondonia' or x == 'Tocantins')
                                     else 'Centro-Oeste' if (x == 'Goias' or x == 'Mato Grosso')
                                     else 'Nordeste')
    df['codigo'] = df['state'].apply(lambda x:
                                     '12' if (x == 'Acre')
                                     else '27' if (x == 'Alagoas')
                                     else '16' if (x == 'Amapa')
                                     else '13' if (x == 'Amazonas')
                                     else '29' if (x == 'Bahia')
                                     else '23' if (x == 'Ceara')
                                     else '53' if (x == 'Distrito Federal')
                                     else '32' if (x == 'Espirito Santo')
                                     else '52' if (x == 'Goias')
                                     else '21' if (x == 'Maranhao')
                                     else '51' if (x == 'Mato Grosso')
                                     else '31' if (x == 'Minas Gerais')
                                     else '15' if (x == 'Pará')
                                     else '25' if (x == 'Paraiba')
                                     else '26' if (x == 'Pernambuco')
                                     else '22' if (x == 'Piau')
                                     else '33' if (x == 'Rio')
                                     else '11' if (x == 'Rondonia')
                                     else '14' if (x == 'Roraima')
                                     else '42' if (x == 'Santa Catarina')
                                     else '35' if (x == 'Sao Paulo')
                                     else '28' if (x == 'Sergipe')
                                     else '17')
    df['codigo'] = df['codigo'].astype(str)

    return df




#====================
# Load Data & Define Global Variables
#====================
df = get_data('incendios.csv')

df1 = df[['year', 'number']].groupby('year').sum().reset_index()
fig1 = px.line(df1, x='year', y='number',
               title='FOCOS DE INCÊNDIO NO BRASIL AO LONGO DOS ANOS (1998 - 2017)',
               labels={
                   "number": " ",
                   "year": " "})
df2 = df[['month', 'number']].groupby('month', sort=False).sum().reset_index()
fig2 = px.line(df2, 'month', 'number',
               title='FOCOS DE INCÊNDIO NO BRASIL AO LONGO DOS MESES (1998 - 2017)',
               labels={
                   "number": " ",
                   "month": " "})
df3 = df[['number', 'regiao', 'year']].groupby(['regiao', 'year']).sum('number').reset_index()
fig3 = px.line(df3, x='year', y='number', color='regiao',
               title='FOCOS DE INCÊNDIO POR REGIÃO AO LONGO DOS ANOS (1998 - 2017)',
               labels={
                   "number": " ",
                   "regiao": "Região ",
                   "year": " "})
df4 = df[['number', 'regiao', 'month']].groupby(['regiao', 'month'], sort=False).sum('number').reset_index()
fig4 = px.line(df4, x='month', y='number', color='regiao',
               title='FOCOS DE INCÊNDIO POR REGIÃO AO LONGO DOS MESES (1998 - 2017)',
               labels={
                   "number": " ",
                   "regiao": "Região ",
                   "month": " "})
df5 = df[['state', 'year', 'number']].groupby(['state', 'year']).sum('number').reset_index()
fig5 = px.line(df5, x='year', y='number', color='state',
               title='FOCOS DE INCÊNDIO POR ESTADO AO LONGO DOS ANOS (1998 - 2017)',
               labels={
                   "number": " ",
                   "state": "Estados ",
                   "year": " "})
df6 = df[['state', 'month', 'number']].groupby(['state', 'month'], sort=False).sum('number').reset_index()
fig6 = px.line(df6, x='month', y='number', color='state',
               title='FOCOS DE INCÊNDIO POR ESTADO AO LONGO DOS MESES (1998 - 2017)',
               labels={
                   "number": " ",
                   "state": "Estados ",
                   "month": " "})

df_top_state = df[['state', 'number']].groupby('state').sum().sort_values('number', ascending=False).reset_index()
df_top_regiao = df[['regiao', 'number']].groupby('regiao').sum().sort_values('number', ascending=False).reset_index()
df_top_year = df[['year', 'number']].groupby('year').sum().sort_values('number', ascending=False).reset_index()
df_top_month = df[['month', 'number']].groupby('month', sort=False).sum().sort_values('number', ascending=False).reset_index()
df_top_bioma = df[['bioma', 'number']].groupby('bioma', sort=False).sum().sort_values('number', ascending=False).reset_index()



#====================
# Part 1
#====================

st.subheader('Total de incêndios em âmbito nacional')

# Filters
col1, col2 = st.columns(2)
with col1:
    eixo = st.radio(
        "Selecione a granularidade desejada",
        ('Ver de acordo com os estados', 'Ver de acordo com região'))
with col2:
    data_min = (int(df['year'].min()))
    data_max = (int(df['year'].max()))
    intervalo = st.slider("Selecione o intervalo desejado", data_min, data_max, (data_min, data_max))


# Request
response = requests.get(url='https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json')
if response.status_code == 200:  # O código 200 (OK) indica que a solicitação foi bem sucedida
    state_geo = response.json()

type(state_geo)


# Variables
df_map = df.loc[(df['year'] <= intervalo[1]) & (df['year'] >= intervalo[0])]
df_map = df_map[['number', 'state', 'codigo', 'year']]
df_map = df_map.groupby(['codigo', 'state']).sum().sort_values('number').reset_index()

dfa = df.loc[(df['year'] <= intervalo[1]) & (df['year'] >= intervalo[0])]
dfa = dfa.groupby('state').sum().sort_values('number').reset_index()
figa = px.bar(dfa, x='number', y='state', color='number',width=800, height=550,
              title='FOCOS DE INCÊNDIO POR ESTADO',
              labels={
                  "number": " ",
                  "state": " ",
                  "number": " "})
dfb = df.loc[(df['year'] <= intervalo[1]) & (df['year'] >= intervalo[0])]
dfb = dfb.groupby('regiao').sum().sort_values('number').reset_index()
figb = px.bar(dfb, 'number', 'regiao', color='number',
              title='FOCOS DE INCÊNDIO POR REGIÃO',
              labels={
                  "number": " ",
                  "regiao": " ",
                  "number": " "})


# Plot Charts
if eixo == 'Ver de acordo com os estados':
    st.plotly_chart(figa, use_container_width=True)
    df_top = df.loc[(df['year'] <= intervalo[1]) & (df['year'] >= intervalo[0])]
    df_top = df_top[['state', 'number']].groupby('state').sum().sort_values('number', ascending=False).reset_index()
elif eixo == 'Ver de acordo com região':
    st.plotly_chart(figb, use_container_width=True)
    df_top = df.loc[(df['year'] <= intervalo[1]) & (df['year'] >= intervalo[0])]
    df_top = df_top[['regiao', 'number']].groupby('regiao').sum().sort_values('number', ascending=False).reset_index()


# Plot Map
fig_map = px.choropleth(df_map, geojson=state_geo, color="number",
                        color_continuous_scale="burgyl",
                        locations="codigo",
                        featureidkey="properties.GEOCODIGO",
                        projection="mercator",
                        hover_name="state",
                        hover_data={"number": True, 'codigo': False},
                        labels={'number': 'Número de incêndios'},
                        )
fig_map.update_geos(fitbounds="geojson", visible=False)
fig_map.update_layout(title='FOCOS DE INCÊNDIO POR ESTADO',
                      height=500,
                      margin={"r": 0, "t": 40, "l": 0, "b": 0})
st.plotly_chart(fig_map)


# Button
gerar_rel = st.button("Gerar Relatório Geral", 1)
if gerar_rel:
    df_top
else:
    pass


st.subheader('  ')
st.subheader('  ')
st.subheader('  ')
st.subheader('  ')
#====================
# Part 2
#====================

st.subheader('Histórico anual de incêndios')

# Filter
anos = st.selectbox('Selecione o ano', df['year'].sort_values(ascending=False).unique())

# Variables
df_base = df.loc[df['year'] == anos]
df7 = df_base.groupby('month', sort=False).sum().reset_index()
df_bio = df_base[['bioma', 'number']].groupby('bioma').sum().sort_values('number').reset_index()

# Metrics
metric1 = df7.sort_values('number', ascending=False).reset_index(drop=True)
metric1 = metric1.loc[0, 'month']
metric2 = df_base['number'].sum()
metric3 = df_base[['number', 'state']].groupby('state').sum().sort_values('number', ascending=False).reset_index()
metric3 = metric3.loc[0, 'state']
metric4 = df[['bioma', 'number']].groupby('bioma').sum().reset_index()
metric4 = metric4.loc[0, 'bioma']

st.subheader('  ')

col1, col2 = st.columns(2)
with col1:
    st.metric("Mês com maior quantidade de incêndios", metric1)
    st.metric("Número de incêndios no ano", metric2)
with col2:
    st.metric("Estado com maior quantidade de incêndios", metric3)
    st.metric("Bioma mais atingido", metric4)

# Plot Charts
fig7 = px.line(df7, x='month', y='number',
           title=f'FOCOS DE INCÊNDIO NO ANO DE {anos}',
           labels={
               "number": " ",
               "month": " "})
st.plotly_chart(fig7, use_container_width=True)

fig_bio = px.bar(df_bio, x='number', y='bioma', color='number',
             title=f'FOCOS DE INCÊNDIO POR BIOMA NO ANO DE {anos}',
             labels={
                 "number": " ",
                 "bioma": " ",
                 "number": " "
                 })
st.plotly_chart(fig_bio, use_container_width=True)




st.subheader('  ')
st.subheader('  ')
#====================
# Part 3
#====================
st.subheader('Distribuição de incêndios ao longo dos anos')

# Filter
eixo = st.radio(
    "Selecione o modo de visualização",
    ('Ver ano-a-ano', 'Ver reta média'))

# Variables
if eixo == 'Ver ano-a-ano':
    fig1 = fig1
    fig2 = fig2
    fig3 = fig3
elif eixo == 'Ver reta média':
    fig1 = px.scatter(df1, x='year', y='number', trendline="ols",
                   title='FOCOS DE INCÊNDIO NO BRASIL AO LONGO DOS ANOS (1998 - 2017)',
                   labels={
                       "number": " ",
                       "year": " "})
    fig3 = px.scatter(df3, x='year', y='number', color='regiao', trendline="ols",
                   title='FOCOS DE INCÊNDIO POR REGIÃO AO LONGO DOS ANOS (1998 - 2017)',
                   labels={
                       "number": " ",
                       "regiao": "Região ",
                       "year": " "})
    fig5 = px.scatter(df5, x='year', y='number', color='state', trendline="ols",
                   title='FOCOS DE INCÊNDIO POR ESTADO AO LONGO DOS ANOS (1998 - 2017)',
                   labels={
                       "number": " ",
                       "state": "Estados ",
                       "year": " "})

# Plot Charts
tab1, tab2, tab3 = st.tabs(['Brasil', 'Região', 'Estado'])
with tab1:
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    st.plotly_chart(fig3, use_container_width=True)
with tab3:
    st.plotly_chart(fig5, use_container_width=True)

# Button
gerar_rel_2 = st.button("Gerar Relatório Anual", 2)
if gerar_rel_2:
    df_top_year
else:
    pass



st.subheader('  ')
st.subheader('  ')
st.subheader('  ')
st.subheader('  ')
#====================
# Part 3
#====================
st.subheader('Distribuição de incêndios ao longo dos meses')

# Plot Charts
tab1, tab2, tab3 = st.tabs(['Brasil', 'Região', 'Estado'])
with tab1:
    st.plotly_chart(fig2, use_container_width=True)
with tab2:
    st.plotly_chart(fig4, use_container_width=True)
with tab3:
    st.plotly_chart(fig6, use_container_width=True)

# Button
gerar_rel_3 = st.button("Gerar Relatório Mensal", 2)
if gerar_rel_3:
    df_top_month
else:
    pass




#====================
# SideBar
#====================

with st.sidebar:
    estado_max = df_top_state.loc[0, 'state']
    ano_max = df_top_year.loc[0, 'year']
    month_max = df_top_month.loc[0, 'month']
    bioma_max = df_top_bioma.loc[0, 'bioma']

    st.title('Panorama Geral')

    st.subheader(f" \U0001F4CC" "O Estado com maior quantidade de incêndios é:")
    st.write(estado_max)

    st.subheader(f" \U0001F4C5" "O ano com maior quantidade de incêndios é:")
    st.write(ano_max)

    st.subheader(" \U0001F5D3" "O mês com maior quantidade de incêndios é:")
    st.write(month_max)

    st.subheader(" \U0001F333" "O bioma com maior quantidade de incêndios é:")
    st.write(bioma_max)

