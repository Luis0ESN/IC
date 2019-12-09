# -*- coding: utf-8 -*-

from urllib.request import urlopen #abrir uma pagina web
import pandas as pd
import numpy
import matplotlib.pyplot as plt;

###########################
###criação de histograma###
###########################

#cria um histograma de frequência dos eventos e da quantidade de manchas solares identificadas
def criaHistograma(): 
    datalink = "https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-indices/sunspot-numbers/american/tables/table_aavso-arssn_monthly.txt"

    plt_eixo_x = []
    plt_eixo_y = []
    try: #abre o link que contém o arquivo
        arq = urlopen(datalink)
    except:
        print('Algo de errado nao está certo.')
    else:
        print('input url: '+datalink)
        print("Reading webpage's html...\n")
        texto = arq.readlines(); #texto recebe todas as linhas com valores
        
        del texto[3]
        del texto[2]
        del texto[1]
        del texto[0]
        
        for i in range(0, len(texto)): #vai repetir enquando houver linhas no texto 
            texto[i] = texto[i].decode('utf-8')
            if len(str(texto[i]).split()) > 0 and str(texto[i][0]) != "-" and int(str(texto[i]).split()[0]) >= 2007 and int(str(texto[i]).split()[0]) <= 2014:
                Linha = str(texto[i]).split() #linha é a linha atual do texto 
                
                for i in range(1, len(Linha)):
                    plt_eixo_y.append(float(Linha[i])) #média de cada mês do ano
                
                for i in range(1, 13):
                    plt_eixo_x.append(float(Linha[0]) + i/13) #ano + fração referente ao mês
        
    sta = list()
    stb = list()
    
    file = pd.read_excel('Lista de choques.xlsx')
    dataset = file.loc[(file.Type == 'FF')]
    
    selData = numpy.array(dataset[['Spacecraft','Year','Month']])
    
    for item in selData:
        if item[0] == "STA":
            sta.append(item[1])
        if item[0] == "STB":
            stb.append(item[1])       
    
    texto_xticks = []
    #texto_xticks.append("")
    for i in range(2007, 2015):
        texto_xticks.append(i)


    for i in range(2007, 2016, 1):
        print(i)
    
    fig = plt.figure()
    plt.subplots_adjust(left=0.125, bottom=0.1, right=1.15, top=2.4,
                        wspace=0.33, hspace=0.2)
    
    plt_hist = fig.add_subplot(1, 1, 1)
    #plt_plote = fig.add_subplot(1, 1, 1)    
    
    plt_hist.axis((2007, 2015, 0, max([len(sta), len(stb), max(plt_eixo_y)])))
    plt_hist.hist([sta, stb], color=['orange', 'green'], edgecolor='black', stacked=True, rwidth=1.0, bins=range(2007, 2016,1))
    plt_hist.set_xlabel("Year")
    plt_hist.set_ylabel("Number of shocks")
    plt_hist.legend(["STA", "STB"], bbox_to_anchor=(1.3, 1))
    #start, end = plt_hist.get_ylim()
    #plt_hist.yaxis.set_ticks(numpy.arange(start, end+1, 5))
    plt_hist.grid(axis='y', linestyle='-')
    
    plt_plote = plt_hist.twinx();
    plt_plote.axis((2007, 2015, 0, max([len(sta), len(stb), max(plt_eixo_y)])))
    plt_plote.set_ylabel("Sunspot number")
    plt_plote.plot(plt_eixo_x, plt_eixo_y, color='black', linewidth=1)
    plt_plote.legend(["MONTHLY MEAN"], bbox_to_anchor=(1.3, 0.9))
    start, end = plt_plote.get_xlim()
    plt_plote.xaxis.set_ticks(numpy.arange(start+0.5, end, 1))
    plt_plote.set_xticklabels(texto_xticks)
    
    fig.savefig('Arquivos/histograma.png', bbox_inches='tight')
    
    try:
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    except:
        pass


criaHistograma()