import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO


# Opção de filtro "todos"
OPCAO_TODOS = 'Todos'


# configuuração do tema do seaborn
sns.set_theme(style="ticks", rc={
    "axes.spines.right": False,
    "axes.spines.top": False
})


# Função para ler os dados
@st.cache_data(show_spinner="Carregando os dados...")
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except:
        return pd.read_excel(file_data)


# Função para filtrar baseado na multiseleção de categorias
@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if OPCAO_TODOS in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)


# Função para converter o df para excel
@st.cache_data(show_spinner="Convertendo os dados para Excel...")
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    return output.getvalue()


# ao selecionar o arquivo, chama essa função para carregar o conteúdo
def carregar_conteudo_arquivo(arquivo):

    dados_originais = load_data(arquivo)
    df_dados = dados_originais.copy()

    st.write('## Antes dos filtros')
    st.write(dados_originais.head())

    with st.sidebar.form(key='my_form'):
        # tipo de gráfico
        graph_type = st.radio('Tipo de gráfico:', ('Barras', 'Pizza'))
    
        # idades
        max_age = int(df_dados.age.max())
        min_age = int(df_dados.age.min())
        idades = st.slider(
            label='Idade', 
            min_value = min_age,
            max_value = max_age, 
            value = (min_age, max_age),
            step = 1
        )

        # profissões
        jobs_list = df_dados.job.unique().tolist()
        jobs_list.append(OPCAO_TODOS)
        jobs_selected =  st.multiselect("Profissão", jobs_list, [OPCAO_TODOS])

        # estado civil
        marital_list = df_dados.marital.unique().tolist()
        marital_list.append(OPCAO_TODOS)
        marital_selected =  st.multiselect("Estado civil", marital_list, [OPCAO_TODOS])

        # default
        default_list = df_dados.default.unique().tolist()
        default_list.append(OPCAO_TODOS)
        default_selected =  st.multiselect("Default", default_list, [OPCAO_TODOS])
        
        # possui financiamento
        housing_list = df_dados.housing.unique().tolist()
        housing_list.append(OPCAO_TODOS)
        housing_selected =  st.multiselect("Possui financiamento", housing_list, [OPCAO_TODOS])
        
        # possui emprestimo
        loan_list = df_dados.loan.unique().tolist()
        loan_list.append(OPCAO_TODOS)
        loan_selected =  st.multiselect("Possui empréstimo", loan_list, [OPCAO_TODOS])
        
        # forma da contato
        contact_list = df_dados.contact.unique().tolist()
        contact_list.append(OPCAO_TODOS)
        contact_selected =  st.multiselect("Forma de contato", contact_list, [OPCAO_TODOS])
        
        # mês do contrato
        month_list = df_dados.month.unique().tolist()
        month_list.append(OPCAO_TODOS)
        month_selected =  st.multiselect("Mês do contato", month_list, [OPCAO_TODOS])
        
        # dia da semana
        day_of_week_list = df_dados.day_of_week.unique().tolist()
        day_of_week_list.append(OPCAO_TODOS)
        day_of_week_selected =  st.multiselect("Dia da semana", day_of_week_list, [OPCAO_TODOS])

        # todos os filtros ao mesmo tempo
        df_dados = (
            df_dados.query("age >= @idades[0] and age <= @idades[1]")
            .pipe(multiselect_filter, 'job', jobs_selected)
            .pipe(multiselect_filter, 'marital', marital_selected)
            .pipe(multiselect_filter, 'default', default_selected)
            .pipe(multiselect_filter, 'housing', housing_selected)
            .pipe(multiselect_filter, 'loan', loan_selected)
            .pipe(multiselect_filter, 'contact', contact_selected)
            .pipe(multiselect_filter, 'month', month_selected)
            .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
        )

        submit_button = st.form_submit_button(label='Aplicar')
    
    # Botões de download dos dados filtrados
    st.write('## Após os filtros')
    st.write(df_dados.head())
    
    df_xlsx = to_excel(df_dados)
    st.download_button(label='Baixar tabela em EXCEL', data=df_xlsx, file_name= 'dados_filtrados.xlsx')
    st.markdown("---")


    df_dados_percentual = dados_originais.y.value_counts(normalize = True).to_frame() * 100
    df_dados_percentual = df_dados_percentual.sort_index()

    df_dados_percentual_target = df_dados.y.value_counts(normalize = True).to_frame() * 100
    df_dados_percentual_target = df_dados_percentual_target.sort_index()
    
    # Botões de download dos dados dos gráficos
    col1, col2 = st.columns(2)

    df_xlsx = to_excel(df_dados_percentual)
    col1.write('### Proporção original')
    col1.write(df_dados_percentual)
    col1.download_button(label='Download', data=df_xlsx, file_name= 'proporcao_original.xlsx')
    
    df_xlsx = to_excel(df_dados_percentual_target)
    col2.write('### Proporção da tabela com filtros')
    col2.write(df_dados_percentual_target)
    col2.download_button(label='Download', data=df_xlsx, file_name= 'proporcao_com_filtros.xlsx')
    st.markdown("---")


    st.write('## Proporção de aceite')


    # gráficos    
    fig, ax = plt.subplots(1, 2, figsize = (5,3))

    if graph_type == 'Barras':
        sns.barplot(y = 'proportion', x = 'y', data = df_dados_percentual.reset_index(), ax = ax[0])
        ax[0].bar_label(ax[0].containers[0])
        ax[0].set_title('Dados brutos', fontweight ="bold")
        
        sns.barplot(y = 'proportion', x = 'y', data = df_dados_percentual_target.reset_index(), ax = ax[1])
        ax[1].bar_label(ax[1].containers[0])
        ax[1].set_title('Dados filtrados', fontweight ="bold")

    else:
        df_dados_percentual.reset_index().plot(kind='pie', autopct='%.2f', y='proportion', ax = ax[0])
        ax[0].set_title('Dados brutos', fontweight ="bold")
        
        df_dados_percentual_target.reset_index().plot(kind='pie', autopct='%.2f', y='proportion', ax = ax[1])
        ax[1].set_title('Dados filtrados', fontweight ="bold")

    st.pyplot(fig)



# Função principal da aplicação
def main():

    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title = 'Telemarketing analisys',
        page_icon = 'img/telmarketing_icon.png',
        layout="wide",
        initial_sidebar_state='expanded'
    )


    # Título principal da aplicação
    st.write('# Telemarketing analisys')
    st.markdown("---")

    
    # Apresenta a imagem na barra lateral da aplicação
    imagem = Image.open("img/bank-Branding.jpg")
    st.sidebar.image(imagem)


    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Upload do arquivo de dados")
    arquivo = st.sidebar.file_uploader("Arquivo com os dados", type = ['csv','xlsx'])


    # Se o arquivo foi selecionado pelo usuaário
    if (arquivo is not None):
        carregar_conteudo_arquivo(arquivo)


main()