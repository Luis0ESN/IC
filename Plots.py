# -*- coding: utf-8 -*-

import os;
from urllib.request import urlretrieve
from urllib.request import urlopen
from datetime import datetime
import matplotlib.pyplot as plt;
from STEREO import stereo
import numpy
import pandas as pd
import zipfile
from moviepy.editor import *

'''
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
MAGENTA = "\033[35m"
REVERSE = "\033[;7m"

bpreto = '\033[40m'
bvermelho = '\033[41m'
bverde = '\033[42m'
bamarelo = '\033[43m'
bazul = '\033[44m'
bmagenta = '\033[45m'
bciano = '\033[46m'
bbranco = '\033[47m'
'''

### metodo para criar um caminho ###
def createFolder(caminho):
    try:
        if not os.path.exists(caminho):
            os.makedirs(caminho)
    except OSError:
        print ('Error: Creating directory. ' +  caminho)
        
### metodo que retorna o maior valor de um vetor, ignorando os valores nulos('nan')
def maior_valor(vet):
    maior = float(vet[0])
    
    for a in range(1, len(vet)-1):
            if float(maior) < vet[a] and str(vet[a])!='nan' or str(maior)=='nan':
                maior = vet[a]
    
    if str(maior)=='nan':
        return 10

    return maior

### metodo que retorna o menor valor de um vetor, ignorando os valores nulos('nan')
def menor_valor(vet):
    menor = float(vet[0])
    
    for a in range(1, len(vet)-1):
            if float(menor) > vet[a] and str(vet[a])!='nan' or str(menor)=='nan':
                menor = vet[a]
    
    if str(menor)=='nan':
        return 0

    return menor

#metodo que cria o plot 
def plot_and_subplot(year, month, day):
        
    caminho = 'Arquivos'+'\ '.strip()+year+month+day
    createFolder(caminho)
        
    str_eventDate='{}/{}/{}'.format(year,month,day)
    eventDate = datetime.strptime(str_eventDate, '%Y/%m/%d')
    
    initialDate = eventDate.fromordinal(eventDate.toordinal()-2)
    S_year = initialDate.strftime('%Y')
    S_month = initialDate.strftime('%m')
    S_day = initialDate.strftime('%d')
    
    finalDate = eventDate.fromordinal(eventDate.toordinal()+2)
    E_year = finalDate.strftime('%Y')
    E_month = finalDate.strftime('%m')
    E_day = finalDate.strftime('%d')
    
    DADOS_STA = stereo('STA', S_year+'/'+S_month+'/'+S_day, E_year+'/'+E_month+'/'+E_day);
    DADOS_STB = stereo('STB', S_year+'/'+S_month+'/'+S_day, E_year+'/'+E_month+'/'+E_day);
    
    Y_LABEL = ['$N_p (1/cm^3)$', '$V_p$ (Km/s)', '$T_p k^o (10^6)$', '$Beta (Log_{10})$', '$P_T$ (nPa)', '$B_T (nT)$', '$B_x (nT)$', '$B_y (nT)$', '$B_z (nT)$']
    
    ###recebendo o maior e os menor valor de tempo
    if max(DADOS_STA.get_data('time')) > max(DADOS_STB.get_data('time')):
        maximo = max(DADOS_STA.get_data('time'))
    else:
        maximo = max(DADOS_STB.get_data('time'))
        
    if min(DADOS_STA.get_data('time')) > min(DADOS_STB.get_data('time')):
        minimo = min(DADOS_STA.get_data('time'))
    else:
        minimo = min(DADOS_STB.get_data('time'))
    ### fim da verificação
    
    
    ### para colocar os xsticks
    texto_data = []
    
    data_em_texto = '{}/{}/{}'.format(S_day, S_month, S_year)
    S_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
    
    data_em_texto = '{}/{}/{}'.format(E_day, E_month, E_year)
    E_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
    E_Day = datetime.fromordinal(E_Day.toordinal()+1)
    
    while S_Day != datetime.fromordinal(E_Day.toordinal()+1):
        texto_data.append(S_Day.strftime('%d/%m/%Y')) ### variavel que armazenará os Xsticks
        texto_data.append('')
        texto_data.append('')
        texto_data.append('')
        S_Day = datetime.fromordinal(S_Day.toordinal()+1)
    ### fim colocar Xsticks
    
    
    name='STA'
    fig = plt.figure()
    
    plt.subplots_adjust(left=0.125, bottom=0.1, right=1.15, top=2.4,
                        wspace=0.33, hspace=0.2)
    #plt.xscale('1')
    
    x1_plt = fig.add_subplot(9, 1, 1)
    x2_plt = fig.add_subplot(9, 1, 2)
    x3_plt = fig.add_subplot(9, 1, 3)
    x4_plt = fig.add_subplot(9, 1, 4)
    x5_plt = fig.add_subplot(9, 1, 5)
    x6_plt = fig.add_subplot(9, 1, 6)                
    x7_plt = fig.add_subplot(9, 1, 7)
    x8_plt = fig.add_subplot(9, 1, 8)
    x9_plt = fig.add_subplot(9, 1, 9)
    
    menor = menor_valor(DADOS_STA.get_data('np'))
    maior = maior_valor(DADOS_STA.get_data('np'))
    x1_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STA.get_data('speed'))
    maior = maior_valor(DADOS_STA.get_data('speed'))
    x2_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(numpy.true_divide(DADOS_STA.get_data('temperature'),10**6))
    maior = maior_valor(numpy.true_divide(DADOS_STA.get_data('temperature'),10**6))
    x3_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(numpy.log10(DADOS_STA.get_data('beta')))
    maior = maior_valor(numpy.log10(DADOS_STA.get_data('beta')))
    x4_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STA.get_data('total_pressure'))
    maior = maior_valor(DADOS_STA.get_data('total_pressure'))
    x5_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STA.get_data('btotal'))
    maior = maior_valor(DADOS_STA.get_data('btotal'))
    x6_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STA.get_data('bx'))
    maior = maior_valor(DADOS_STA.get_data('bx'))
    x7_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STA.get_data('by'))
    maior = maior_valor(DADOS_STA.get_data('by'))
    x8_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STA.get_data('bz'))
    maior = maior_valor(DADOS_STA.get_data('bz'))
    x9_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    
    
    x1_plt.plot(DADOS_STA.get_data('time'), DADOS_STA.get_data('np'), color='black', linewidth=1)
    x1_plt.set_title("STA")#('BTOTAL - BX - BY - BZ', fontsize=7, x=1, y=0)
    x1_plt.set_ylabel(Y_LABEL[0])
    start, end = x1_plt.get_xlim()
    x1_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x1_plt.set_xticklabels('')
    
    x2_plt.plot(DADOS_STA.get_data('time'), DADOS_STA.get_data('speed'), color='black', linewidth=1)
    x2_plt.set_ylabel(Y_LABEL[1])
    start, end = x2_plt.get_xlim()
    x2_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x2_plt.set_xticklabels('')
    
    x3_plt.plot(DADOS_STA.get_data('time'), numpy.true_divide(DADOS_STA.get_data('temperature'),10**6), color='black', linewidth=1)
    x3_plt.set_ylabel(Y_LABEL[2])
    start, end = x3_plt.get_xlim()
    x3_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x3_plt.set_xticklabels('')
    
    x4_plt.plot(DADOS_STA.get_data('time'), numpy.log10(DADOS_STA.get_data('beta')), color='black', linewidth=1)
    x4_plt.set_ylabel(Y_LABEL[3])
    start, end = x4_plt.get_xlim()
    x4_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x4_plt.set_xticklabels('')
    x4_plt.plot([start, end], [0,0])
    
    x5_plt.plot(DADOS_STA.get_data('time'), DADOS_STA.get_data('total_pressure'), color='black', linewidth=1)
    x5_plt.set_ylabel(Y_LABEL[4])
    start, end = x5_plt.get_xlim()
    x5_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x5_plt.set_xticklabels('')    
    
    x6_plt.plot(DADOS_STA.get_data('time'), DADOS_STA.get_data('btotal'), color='black', linewidth=1)
    x6_plt.set_ylabel(Y_LABEL[5])
    x6_plt.set_xlabel('')
    x6_plt.set_xticklabels('')
    start, end = x6_plt.get_xlim()
    x6_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    
    x7_plt.plot(DADOS_STA.get_data('time'), DADOS_STA.get_data('bx'), color='black', linewidth=1)
    x7_plt.set_ylabel(Y_LABEL[6])
    x7_plt.set_xlabel('')
    x7_plt.set_xticklabels('')
    start, end = x7_plt.get_xlim()
    x7_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x7_plt.plot([start, end], [0,0])
    
    x8_plt.plot(DADOS_STA.get_data('time'), DADOS_STA.get_data('by'), color='black', linewidth=1)
    x8_plt.set_ylabel(Y_LABEL[7])
    x8_plt.set_xlabel('')
    x8_plt.set_xticklabels('')
    start, end = x8_plt.get_xlim()
    x8_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x8_plt.plot([start, end], [0,0])
    
    x9_plt.plot(DADOS_STA.get_data('time'), DADOS_STA.get_data('bz'), color='black', linewidth=1)
    x9_plt.set_ylabel(Y_LABEL[8])
    x9_plt.set_xlabel('Dia')
    start, end = x9_plt.get_xlim()
    x9_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x9_plt.set_xticklabels(texto_data)
    x9_plt.plot([start, end], [0,0])
    
    ### encontrando os cortes de choques no gráficos ###
    shock_sta=[]                    
    data_em_texto = '{}/{}/{}'.format(S_day, S_month, S_year)
    datainic = datetime.strptime(data_em_texto, '%d/%m/%Y')
    data_em_texto = '{}/{}/{}'.format(E_day, E_month, E_year)
    datafim = datetime.strptime(data_em_texto, '%d/%m/%Y')
    for x in range(0, len(choques_graficos(datainic, datafim))):
        if choques_graficos(datainic, datafim)[x][0]=='STEREO A':
            shock_sta.append(choques_graficos(datainic, datafim)[x][1])
    
    ###plotando o corte no gráfico STA
    for z in range(0, len(shock_sta)):
        x1_plt.plot([shock_sta[z],shock_sta[z]], x1_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x2_plt.plot([shock_sta[z],shock_sta[z]], x2_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x3_plt.plot([shock_sta[z],shock_sta[z]], x3_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x4_plt.plot([shock_sta[z],shock_sta[z]], x4_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x5_plt.plot([shock_sta[z],shock_sta[z]], x5_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x6_plt.plot([shock_sta[z],shock_sta[z]], x6_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x7_plt.plot([shock_sta[z],shock_sta[z]], x7_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x8_plt.plot([shock_sta[z],shock_sta[z]], x8_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x9_plt.plot([shock_sta[z],shock_sta[z]], x9_plt.get_ylim(), 'b--', color='red', linewidth=1)
    
    
    fig.savefig(caminho+'/{}.png'.format(name), bbox_inches='tight', dpi=500 )
    try:
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    except:
        pass
    
    #plt.show()
    fig.clf()
    plt.clf()
    plt.close()
    
    name='STB'
    fig = plt.figure()    
    
    plt.subplots_adjust(left=0.125, bottom=0.1, right=1.15, top=2.4,
                        wspace=0.33, hspace=0.2)
    #plt.xscale('1')
    
    x1_plt = fig.add_subplot(9, 1, 1)
    x2_plt = fig.add_subplot(9, 1, 2)
    x3_plt = fig.add_subplot(9, 1, 3)
    x4_plt = fig.add_subplot(9, 1, 4)
    x5_plt = fig.add_subplot(9, 1, 5)
    x6_plt = fig.add_subplot(9, 1, 6)       
    x7_plt = fig.add_subplot(9, 1, 7)
    x8_plt = fig.add_subplot(9, 1, 8)
    x9_plt = fig.add_subplot(9, 1, 9)
    
    menor = menor_valor(DADOS_STB.get_data('np'))
    maior = maior_valor(DADOS_STB.get_data('np'))
    x1_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STB.get_data('speed'))
    maior = maior_valor(DADOS_STB.get_data('speed'))
    x2_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(numpy.true_divide(DADOS_STB.get_data('temperature'),10**6))
    maior = maior_valor(numpy.true_divide(DADOS_STB.get_data('temperature'),10**6))
    x3_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(numpy.log10(DADOS_STB.get_data('beta')))
    maior = maior_valor(numpy.log10(DADOS_STB.get_data('beta')))
    x4_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STB.get_data('total_pressure'))
    maior = maior_valor(DADOS_STB.get_data('total_pressure'))
    x5_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STB.get_data('btotal'))
    maior = maior_valor(DADOS_STB.get_data('btotal'))
    x6_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STB.get_data('bx'))
    maior = maior_valor(DADOS_STB.get_data('bx'))
    x7_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STB.get_data('by'))
    maior = maior_valor(DADOS_STB.get_data('by'))
    x8_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    menor = menor_valor(DADOS_STB.get_data('bz'))
    maior = maior_valor(DADOS_STB.get_data('bz'))
    x9_plt.axis((minimo, maximo, menor - 0.1*abs(menor), maior + 0.1*abs(maior)))
    
    
    x1_plt.plot(DADOS_STB.get_data('time'), DADOS_STB.get_data('np'), color='black', linewidth=1)
    x1_plt.set_title("STB")#('BTOTAL - BX - BY - BZ', fontsize=7, x=1, y=0)
    x1_plt.set_ylabel(Y_LABEL[0])
    start, end = x1_plt.get_xlim()
    x1_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x1_plt.set_xticklabels('')
    
    x2_plt.plot(DADOS_STB.get_data('time'), DADOS_STB.get_data('speed'), color='black', linewidth=1)
    x2_plt.set_ylabel(Y_LABEL[1])
    start, end = x2_plt.get_xlim()
    x2_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x2_plt.set_xticklabels('')
    
    x3_plt.plot(DADOS_STB.get_data('time'), numpy.true_divide(DADOS_STB.get_data('temperature'),10**6), color='black', linewidth=1)
    x3_plt.set_ylabel(Y_LABEL[2])
    start, end = x3_plt.get_xlim()
    x3_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x3_plt.set_xticklabels('')
    
    x4_plt.plot(DADOS_STB.get_data('time'), numpy.log10(DADOS_STB.get_data('beta')), color='black', linewidth=1)
    x4_plt.set_ylabel(Y_LABEL[3])
    start, end = x4_plt.get_xlim()
    x4_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x4_plt.set_xticklabels('')
    x4_plt.plot([start, end], [0,0])
    
    x5_plt.plot(DADOS_STB.get_data('time'), DADOS_STB.get_data('total_pressure'), color='black', linewidth=1)
    x5_plt.set_ylabel(Y_LABEL[4])
    start, end = x5_plt.get_xlim()
    x5_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x5_plt.set_xticklabels('')   
    
    x6_plt.plot(DADOS_STB.get_data('time'), DADOS_STB.get_data('btotal'), color='black', linewidth=1)
    x6_plt.set_ylabel(Y_LABEL[5])
    x6_plt.set_xlabel('')
    start, end = x6_plt.get_xlim()
    x6_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x6_plt.set_xticklabels('')
    
    x7_plt.plot(DADOS_STB.get_data('time'), DADOS_STB.get_data('bx'), color='black', linewidth=1)
    x7_plt.set_ylabel(Y_LABEL[6])
    x7_plt.set_xlabel('')
    start, end = x7_plt.get_xlim()
    x7_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x7_plt.set_xticklabels('')   
    x7_plt.plot([start, end], [0,0])
    
    x8_plt.plot(DADOS_STB.get_data('time'), DADOS_STB.get_data('by'), color='black', linewidth=1)
    x8_plt.set_ylabel(Y_LABEL[7])
    x8_plt.set_xlabel('')
    start, end = x8_plt.get_xlim()
    x8_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x8_plt.set_xticklabels('')   
    x8_plt.plot([start, end], [0,0])
    
    x9_plt.plot(DADOS_STB.get_data('time'), DADOS_STB.get_data('bz'), color='black', linewidth=1)
    x9_plt.set_ylabel(Y_LABEL[8])
    x9_plt.set_xlabel('Dia')
    start, end = x9_plt.get_xlim()
    x9_plt.xaxis.set_ticks(numpy.arange(start, end, 0.25))
    x9_plt.set_xticklabels(texto_data)
    x9_plt.plot([start, end], [0,0])
    
    
    ### encontrando os cortes de choques no gráficos ###
    shock_stb=[]
    data_em_texto = '{}/{}/{}'.format(S_day, S_month, S_year)
    datainic = datetime.strptime(data_em_texto, '%d/%m/%Y')
    data_em_texto = '{}/{}/{}'.format(E_day, E_month, E_year)
    datafim = datetime.strptime(data_em_texto, '%d/%m/%Y')
    for x in range(0, len(choques_graficos(datainic, datafim))):
        if choques_graficos(datainic, datafim)[x][0]=='STEREO B':
            shock_stb.append(choques_graficos(datainic, datafim)[x][1])
    
    
    ###plotando o corte no gráfico STB
    for z in range(0, len(shock_stb)):
        x1_plt.plot([shock_stb[z],shock_stb[z]], x1_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x2_plt.plot([shock_stb[z],shock_stb[z]], x2_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x3_plt.plot([shock_stb[z],shock_stb[z]], x3_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x4_plt.plot([shock_stb[z],shock_stb[z]], x4_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x5_plt.plot([shock_stb[z],shock_stb[z]], x5_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x6_plt.plot([shock_stb[z],shock_stb[z]], x6_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x7_plt.plot([shock_stb[z],shock_stb[z]], x7_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x8_plt.plot([shock_stb[z],shock_stb[z]], x8_plt.get_ylim(), 'b--', color='red', linewidth=1)
        x9_plt.plot([shock_stb[z],shock_stb[z]], x9_plt.get_ylim(), 'b--', color='red', linewidth=1)
    
    
    fig.savefig(caminho+'/{}.png'.format(name), bbox_inches='tight', dpi=500)
    
    try:
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    except:
        pass
    
    #plt.show()
    fig.clf()
    plt.clf()
    plt.close()
    
#metodo que cria o plot para todos os eventos.
def plotEventList(): 
    file = pd.read_excel('Lista de choques.xlsx')
    file.dropna(inplace=True)
    dataset = file.loc[(file.Type == 'FF')]
    
    selData = numpy.array(dataset[['Year','Month','Day']])
    
    #encontrando dias repetidos
    datas_repetidas = []
    for item in selData:
        str_date = '{}/{}/{}'.format(item[0], item[1], item[2])
        datas_repetidas.append(datetime.strptime(str_date, '%Y/%m/%d'))
        
    #deletando o dias repetidos do vetor
    data = []
    for i in datas_repetidas:
        if i not in data:
            data.append(i)
    data.sort()
    
    i = int(0) #variavel int que vai receber o número da linha atual
    for i in range(0, len(data)): #vai repetir enquando houver linhas no texto de datas não repetidas                
        year = data[i].strftime('%Y')
        month = data[i].strftime('%m')
        day = data[i].strftime('%d')
        
        plot_and_subplot(year, month, day)
        ImagesZipDownload(year, month, day)
        makeVideo(year, month, day)

#retorna os choques que ocorreram num determinado período [Stereo A/Stereo B; datetime]
def choques_graficos(datainic, datafim): 
    vet = []
    
    file = pd.read_excel('Lista de choques.xlsx')
    file.dropna(inplace=True)
    dataset = file.loc[(file.Type == 'FF')]
    
    selData = numpy.array(dataset[['Spacecraft','Year','Month','Day','Hour','Minute','Sec']])
    
    for item in selData:
        str_date = '{}/{}/{} {}:{}:{}.000'.format(item[1], item[2], item[3], item[4], item[5], item[6])
        if datetime.strptime(str_date, '%Y/%m/%d %H:%M:%S.%f') > datainic and datetime.strptime(str_date, '%Y/%m/%d %H:%M:%S.%f') < datafim:
            if item[0] == 'STA':
                aux = ["STEREO A", datetime.strptime(str_date, '%Y/%m/%d %H:%M:%S.%f')]
                vet.append(aux)
                    
            if item[0] == 'STB':
                aux = ["STEREO B", datetime.strptime(str_date, '%Y/%m/%d %H:%M:%S.%f')]
                vet.append(aux)
    return vet


###########################
#####criação de videos#####
###########################

#método que faz o vídeo 
def makeVideo(year, month, day): 
    missions = ['EUVI_B', 'COR2_A', 'COR2_B', 'EUVI_A']
    euvi_B = []
    cor2_B = []
    euvi_A = []
    cor2_A = []
    
    data_em_texto = '{}/{}/{}'.format(year, month, day)
    eventDate = datetime.strptime(data_em_texto, '%Y/%m/%d')
    
    str_eventDate = eventDate.strftime('%Y') + eventDate.strftime('%m') + eventDate.strftime('%d')
    
    print( '\n Event occurred on the day:', eventDate.strftime('%Y/%m/%d'))
    #print(BLUE, '\n Event occurred on the day:', GREEN, eventDate[0:5] + eventDate[5:7] + eventDate[7:9])
    
    try:
        if not os.path.exists('Arquivos'+'\ '.strip()+str_eventDate):
            os.makedirs('Arquivos'+'\ '.strip()+str_eventDate)
    except OSError:
        print ('Error: Creating directory. ' +  'Arquivos'+'\ '.strip()+str_eventDate)
    
    for mission in missions:
        print('Mission: '+mission)
        zip_Path = 'Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip()+mission+'/ '.strip()+mission+'.zip'                    
        with zipfile.ZipFile(zip_Path, 'r') as z:
            z.extractall(path='Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip()+mission)
            imagesNames = z.namelist()
            imagesNames.reverse()
            for filename in imagesNames:
                img_path = 'Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip() + mission + '/ '.strip() + filename
                if mission == 'EUVI_B':
                    euvi_B.append(plt.imread(img_path))
                    video1 = ImageSequenceClip(euvi_B, fps=5)
                    
                if mission == 'EUVI_A':
                    euvi_A.append(plt.imread(img_path))
                    video2 = ImageSequenceClip(euvi_A, fps=5)
                    
                if mission == 'COR2_B':
                    cor2_B.append(plt.imread(img_path))
                    video3 = ImageSequenceClip(cor2_B, fps=5)
                    
                if mission == 'COR2_A':
                    cor2_A.append(plt.imread(img_path))
                    video4 = ImageSequenceClip(cor2_A, fps=5)
            
        ## finalizando a adicão das imagens em um clipe de imagens
        #será feito um vídeo com esse clipe
    
    #fim leitura de imagens e criação de sequencia de imagens
    final_clip = clips_array([[video4, video3],
                              [video2, video1]])
    
    
    final_clip.write_videofile('Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip() +'video.mp4')


def ImagesZipDownload(year, month, day): #baixa o zip de imagens de um perido
    data_em_texto = '{}/{}/{}'.format(year, month, day)
    eventDate = datetime.strptime(data_em_texto, '%Y/%m/%d')
    
    str_eventDate = eventDate.strftime('%Y') + eventDate.strftime('%m') + eventDate.strftime('%d')
    
    ###baixando a imagem Where is stereo
    page_link ="https://stereo-ssc.nascom.nasa.gov/cgi-bin/make_where_gif?day={}&month={}&year={}&hour=12&minute=00&field=&background=".format(eventDate.strftime('%d'), eventDate.strftime('%m'), eventDate.strftime('%Y'))
    WebPage = urlopen(page_link)
    html = str(WebPage.readlines())
    print('input url: '+page_link)
    print("\nReading webpage's HTML\n")
    linkStart = html.find("SRC='")
    linkStart+=5
    linkEnd = html.find('\'></P>')
    image_link=html[linkStart:linkEnd]
    #print(partialLink)
    imageLink = "https://stereo-ssc.nascom.nasa.gov"+str(image_link)
    print('Downloading from: ', imageLink)
    
    try:
        urlretrieve(imageLink, 'Arquivos\ '.strip()+str_eventDate+'\ '.strip()+'Where is stereo.png')
    except FileNotFoundError:
        createFolder('Arquivos\ '.strip()+str_eventDate)
        urlretrieve(imageLink, 'Arquivos\ '.strip()+str_eventDate+'\ '.strip()+'Where is stereo.png')
    else:
        urlretrieve(imageLink, 'Arquivos\ '.strip()+str_eventDate+'\ '.strip()+'Where is stereo.png')
    ###
    
    ###baixando os arquivos .zip
    print( '\n Event occurred on the day:', eventDate.strftime('%Y/%m/%d'))
    #print(BLUE, '\n Event occurred on the day:', GREEN, eventDate[0:5] + eventDate[5:7] + eventDate[7:9])
    
    initialDate = datetime.fromordinal(eventDate.toordinal()-5)
    str_initialDate = initialDate.strftime('%Y')+initialDate.strftime('%m')+initialDate.strftime('%d')
    finalDate = datetime.fromordinal(eventDate.toordinal()-3)
    str_finalDate = finalDate.strftime('%Y')+finalDate.strftime('%m')+finalDate.strftime('%d')
    
    missions = ['EUVI_B', 'COR2_A', 'COR2_B', 'EUVI_A']
    for mission in missions:
        #downloadChoice=input("Download data from "+mission+"?")
        #if downloadChoice=="y":
        '''https://stereo-ssc.nascom.nasa.gov/cgi-bin/images?frame=Displaying+1+of+573&fstart=1&fstop=573&Download=Download+all+Behind+COR2&Session=Display&Start=20120720&Finish=20120724&Resolution=512&NumImg=0&Sample=1'''
        if mission == 'EUVI_B':
            eventUrl = "http://stereo-ssc.nascom.nasa.gov/cgi-bin/images?Detectors=behindXeuviX195&frame=Displaying+1+of+573&fstart=1&fstop=573&Download=Download+all+Behind+EUVI+195&Session=Display&Start={}&Finish={}&Resolution=512&NumImg=0&Sample=hour".format(str_initialDate,str_finalDate)
        if mission == 'COR2_A':
            eventUrl = "http://stereo-ssc.nascom.nasa.gov/cgi-bin/images?Detectors=aheadXcor2&frame=Displaying+1+of+573&fstart=1&fstop=573&Download=Download+all+Ahead+COR2&Session=Display&Start={}&Finish={}&Resolution=512&NumImg=0&Sample=hour".format(str_initialDate,str_finalDate)
        if mission == 'COR2_B':
            eventUrl = "http://stereo-ssc.nascom.nasa.gov/cgi-bin/images?Detectors=behindXcor2&frame=Displaying+1+of+573&fstart=1&fstop=573&Download=Download+all+Behind+COR2&Session=Display&Start={}&Finish={}&Resolution=512&NumImg=0&Sample=hour".format(str_initialDate,str_finalDate)
        if mission == 'EUVI_A':
            eventUrl = "http://stereo-ssc.nascom.nasa.gov/cgi-bin/images?Detectors=aheadXeuviX195&frame=Displaying+1+of+573&fstart=1&fstop=573&Download=Download+all+Ahead+EUVI+195&Session=Display&Start={}&Finish={}&Resolution=512&NumImg=0&Sample=hour".format(str_initialDate,str_finalDate)
        try:
            if not os.path.exists('Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip()+mission):
                os.makedirs('Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip()+mission)
        except OSError:
            print ('Error: Creating directory. ' +  'Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip()+mission)
        
        try:
            print('\n\nDownloading .zip files from: '+eventUrl)
            #urlretrieve(eventUrl, eventDate+'/'+mission+'/images'+eventDate+'.zip')
            urlretrieve(eventUrl, 'Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip()+mission+'/ '.strip()+mission+'.zip')
            print('\n\n.zip Saved on: Arquivos'+'\ '.strip()+str_eventDate+'\ '.strip()+mission+'/ '.strip()+mission+'.zip')
        except:
            print("\n\-->wget \""+eventUrl+"\" -O "+'Arquivos'+'\ '.strip()+str_eventDate+"/"+mission+".zip")
