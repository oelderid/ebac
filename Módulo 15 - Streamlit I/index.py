import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.ioff()
sns.set_theme()

# função para gerar o gráfico e salvar em arquivo
def criar_grafico(value, index, ylabel, xlabel, func) -> None:
    table = pd.pivot_table(tabela, values=value, index=index, aggfunc=func).sort_values(value)
    
    if (type(index) == list):
        table = table.unstack()
        
    table.plot(figsize=[15, 5], ylabel=ylabel, xlabel=xlabel)

    # grava o gráfico
    st.pyplot(fig=plt)
    #plt.close()
    
    return None


# Configurações da página
st.set_page_config(
    page_title="SINASC Rondônia 2019", 
    layout="wide", 
    initial_sidebar_state="expanded"
)


# Leitura dos dados
base = pd.read_csv('input_M15_SINASC_RO_2019.csv')
base['DTNASC'] = pd.to_datetime(base['DTNASC'])


# Lista de cidades que serão exibidas no menu lateral
cidades = base['munResNome'].unique()
cidades = [cidade for cidade in cidades if 'ignorado' not in cidade]
cidades = np.sort(cidades)


# Adicionando o menu lateral
st.sidebar.title('Seleção de dados')
st.sidebar.divider()


# Adicionando no menu lateral a seleção das cidades
cidade_selecionada = st.sidebar.selectbox("Cidade:", cidades)


# Filtra as datas de nascimento de acordo com a cidade selecionada
df_data = base[base['munResNome'] == cidade_selecionada]
datas = df_data['DTNASC'].unique()
datas = np.sort(datas)


# Adicionando menu tipo "slider" para as datas de nascimento
st.sidebar.divider()
data_inicio, data_fim = st.sidebar.select_slider(
    'Data de nascimento',
    options=datas,
    value=(np.min(datas), np.max(datas)),
    format_func= lambda x: pd.to_datetime(x).strftime("%d/%m/%Y")
)


# Dados finais de acordo com a data de nascimento e cidade selecionados
tabela = df_data[(df_data['DTNASC'] >= data_inicio) & (df_data['DTNASC'] <= data_fim)]


# Colunas das tabela de dados que será exibida na página
colunas = {
    'IDADEMAE' : 'Idade',
    'ESCMAE' : 'Escolaridade',
    'GESTACAO' : 'Gestação',
    'PARTO' : 'Parto',
    'CONSULTAS' : 'Consulta',
    'APGAR1' : 'APGAR1',
    'APGAR5' : 'APGAR5',
    'PESO' : 'Peso'
}


# Criando a tabela para apresentação dos dados
apresentacao = tabela[colunas.keys()]
apresentacao.rename(columns=colunas, inplace=True)



# APGAR entre 7 e 10 serão destacados na cor verde (Bom)
# APGAR entre 4 e 6 serão destacados na cor amarelo (Moderado)
# APGAR entre 0 e 3 serão destacados na cor vermelha (Grave)
tabela_formatada = apresentacao.style \
        .highlight_between(subset='APGAR1', left=7, right=10, color='#D1FFD7') \
        .highlight_between(subset='APGAR1', left=4, right=6, color='#FFD800') \
        .highlight_between(subset='APGAR1', left=0, right=3, color='#FFB482') \
        .highlight_between(subset='APGAR5', left=7, right=10, color='#D1FFD7') \
        .highlight_between(subset='APGAR5', left=4, right=6, color='#FFD800') \
        .highlight_between(subset='APGAR5', left=0, right=3, color='#FFB482') \
        .format(subset='APGAR1', precision=0) \
        .format(subset='APGAR5', precision=0)


# Exibe a tabela de dados formatada e a contagem de registros abaixo
st.write(f'## SINASC Rondônia 2019: {cidade_selecionada}')
st.dataframe(tabela_formatada, use_container_width=True, hide_index=True)
st.write(f'Total de registros: **{tabela.shape[0]}**')


# Configuração dos gráficos que serão exibidos
config_graficos = [
    {
        'value': 'IDADEMAE', 
        'index': 'DTNASC', 
        'ylabel': 'Quantidade de nascimentos',
        'xlabel': 'Data de nascimento',
        'func': 'count', 
    },
    {
        'value': 'IDADEMAE', 
        'index': ['DTNASC', 'SEXO'],
        'ylabel': 'Média idade mãe',
        'xlabel': 'Data de nascimento',
        'func': 'mean', 
    },
    {
        'value': 'PESO', 
        'index': ['DTNASC', 'SEXO'],
        'ylabel': 'Média peso bebê',
        'xlabel': 'Data de nascimento',
        'func': 'mean', 
    },
    {
        'value': 'PESO', 
        'index': 'ESCMAE',
        'ylabel': 'Peso médio',
        'xlabel': 'Escolaridade mãe',
        'func': 'median', 
    },
    {
        'value': 'APGAR1', 
        'index': 'GESTACAO',
        'ylabel': 'APGAR1 médio',
        'xlabel': 'Gestação', 
        'func': 'mean', 
    },
    {
        'value': 'APGAR5', 
        'index': 'GESTACAO',
        'ylabel': 'APGAR5 médio',
        'xlabel': 'Gestação', 
        'func': 'mean',
    }
]

for grafico in config_graficos:
    st.write('<br>', unsafe_allow_html=True)
    st.subheader(f"\n\n{grafico['ylabel']} x {grafico['xlabel']}")
    criar_grafico(grafico['value'], grafico['index'], grafico['ylabel'], grafico['xlabel'], grafico['func'])