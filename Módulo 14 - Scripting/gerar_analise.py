# imports
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys


# configuração dos meses para os quais devemos criar os gráficos
meses = sys.argv[1:]


# configurações
plt.ioff()
sns.set_theme()
data = None


# função para gerar o gráfico e salvar em arquivo
def criar_grafico(value, index, ylabel, xlabel, func) -> None:
    table = pd.pivot_table(data, values=value, index=index, aggfunc=func).sort_values(value)
    
    if (type(index) == list):
        table = table.unstack()
        
    table.plot(figsize=[15, 5], ylabel=ylabel, xlabel=xlabel)
    
    # cria o diretório
    ano_mes = data['DTNASC'].max()[:7]
    diretorio = f'./graficos/{ano_mes}'
    os.makedirs(diretorio, exist_ok=True)
    
    # cria o nome do arquivo baseado nas labels
    nome_arquivo = f'{xlabel}__{ylabel}'.replace(' ', '_')
    nome_arquivo = f'{diretorio}/{nome_arquivo}.png'
    
    # grava o gráfico
    plt.savefig(nome_arquivo)
    plt.close()
    
    return None


# configurações dos gráficos que devem ser gerados
config_graficos = [
    {
        'value': 'IDADEMAE', 
        'index': 'DTNASC', 
        'ylabel': 'quantidade de nascimento',
        'xlabel': 'data de nascimento',
        'func': 'count', 
    },
    {
        'value': 'IDADEMAE', 
        'index': ['DTNASC', 'SEXO'],
        'ylabel': 'media idade mae',
        'xlabel': 'data de nascimento',
        'func': 'mean', 
    },
    {
        'value': 'PESO', 
        'index': ['DTNASC', 'SEXO'],
        'ylabel': 'media peso bebe',
        'xlabel': 'data de nascimento',
        'func': 'mean', 
    },
    {
        'value': 'PESO', 
        'index': 'ESCMAE',
        'ylabel': 'apgar1 medio',
        'xlabel': 'gestacao',
        'func': 'median', 
    },
    {
        'value': 'APGAR1', 
        'index': 'GESTACAO',
        'ylabel': 'apgar1 medio',
        'xlabel': 'gestacao', 
        'func': 'mean', 
    },
    {
        'value': 'APGAR5', 
        'index': 'GESTACAO',
        'ylabel': 'apgar5 medio',
        'xlabel': 'gestacao', 
        'func': 'mean',
    }
]


for mes in meses:
    data = pd.read_csv(f'./input/SINASC_RO_2019_{mes}.csv')
    data.dropna(inplace=True)
    
    for grafico in config_graficos:
        criar_grafico(grafico['value'], grafico['index'], grafico['ylabel'], grafico['xlabel'], grafico['func'])
