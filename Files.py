# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:45:44 2019

@author: Carlos Nascimento
"""
import os;
import xlrd
from urllib.request import urlopen
from urllib.request import urlretrieve
from datetime import datetime
import matplotlib.pyplot as plt;
import matplotlib.pyplot as plt_stereo;
import PIL as img
from Dados import dados;
import numpy as np
import math as math

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




class files:
    '''
    ###   começo da iniciação  ###
    def _init_(self, directory):
        self.directory = directory;
        
        aux = directory.split("\ ".strip())
        caminho = aux[0]
        
        if len(aux) == 1:
            self.createFolder(caminho)
            
        else:
            for i in range(0, len(aux)):
                if i==0:
                    self.createFolder(caminho)
                else:
                    caminho = caminho+"\ ".sprit() + aux[i]
                    self.createFolder(caminho)
    ###   fim da iniciação   ###
    '''
    
    
    def setDirectory(self, directory):
        self.directory = str(directory);
        
    def getDirectory(self):
        return self.directory;
    
    
    ### metodo createFolder ###
    def createFolder(self, caminho):
        try:
            if not os.path.exists(caminho):
                os.makedirs(caminho)
        except OSError:
            print (RED+'Error: Creating directory. ' +  caminho)
    
    
    ### metodo verificar_arquivo
    def verificar_arquivo(self, name, S_year, S_month, S_day, E_year, E_month, E_day):    
        existe = True;
        
        caminho = self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day+'/'+name+'.txt'
        
        if not os.path.exists(caminho):
            return False
        else:
            return True
        return existe
    
    
    ### metodo para selecionar o arquivo a ser usado
    def selecionar_arquivo(self, name, S_year, S_month, S_day, E_year, E_month, E_day):    
        caminho = self.getDirectory()+'\S_'.strip(' ')+S_year+S_month+S_day+' E_'+E_year+E_month+E_day
        #arquivo = caminho + '/STA.txt'
        arquivo = caminho + '/{}.txt'.format(name)
        #'/STA_L2_MAGPLASMA_1M_8737.txt'
        
        if not os.path.exists(caminho):
            #os.makedirs(caminho)
            print('Essa pasta nao existe')
            
            
        if not os.path.exists(arquivo):
            #open(arquivo, 'w')
            print('Esse arquivo nao existe')
            
        return arquivo;
    
    
    ### metodo que separa as variaveis que serão usadas no plot
    def separar_dados(self, name, S_year, S_month, S_day, E_year, E_month, E_day):
        texto = [];
        STEREO = [];
        aux = [];    
        
        arquivo = self.selecionar_arquivo('{}'.format(name), S_year, S_month, S_day, E_year, E_month, E_day);
        
        
        try:
            arq = open(arquivo);
        except FileNotFoundError:
            print('Algo de errado nao esta certo.')
        else:        
            texto = arq.readlines(); #texto recebe todas as linhas com valores
            
            i = int(0) #variavel int que vai receber o número da linha atual
            for i in range(0, len(texto)): #vai repetir enquando houver linhas no texto        
                Linha = texto[i] #linha é a linha atual do texto    
                if Linha[0] != '#': #removendo linhas indesejadas do arquivo
                    Linha = Linha.strip()
                    aux.append(Linha)
            
            del aux[2]
            del aux[1]
            del aux[0]
            
            for i in range(0,len(aux)):
                linha = aux[i];
                STEREO.append(dados());    
                STEREO[i].setDay(linha[0:2]);
                STEREO[i].setMonth(linha[3:5]);
                STEREO[i].setYear(linha[6:10]);
                STEREO[i].setHour(linha[11:13]);
                STEREO[i].setMinute(linha[14:16])
                STEREO[i].setSecund(linha[17:19]);
                STEREO[i].setMs(linha[20:23]);
                STEREO[i].setBTOTAL(linha.split()[2]);
                STEREO[i].setNP(linha.split()[3]);
                STEREO[i].setBETA(linha.split()[5]);
                STEREO[i].setTOTAL_PRESSURE(linha.split()[6]);
                STEREO[i].setSpeed(linha.split()[7]);
                STEREO[i].setTemperature(linha.split()[8]);
        
                
                
                STEREO[i].setBX(linha.split()[9]);
                STEREO[i].setBY(linha.split()[10]);
                STEREO[i].setBZ(linha.split()[11]);
                
            arq.close();
            
            return STEREO;
    
    
    ### metodo que retorna o maior valor entre dois vetores
    def maior_valor(self, vet1, vet2):
        maior1= vet1[0]
        maior2= vet2[0]
        #print('{},{}'.format(str(maior1),str(maior2)))
        for a in range(0, len(vet1)):
            if float(maior1) < vet1[a] and str(vet1[a])!='nan' or str(maior1)=='nan':
                maior1 = vet1[a]
                
        for a in range(0, len(vet2)):
            if float(maior2) < vet2[a] and str(vet2[a])!='nan' or str(maior2)=='nan':
                maior2 = vet2[a]
        
        if str(maior1)=='nan' and str(maior2)=='nan':
            return 10
        
        if maior1 > maior2 or str(maior2)=='nan':
            return maior1
        
        return maior2

    ### metodo que retorna o menor valor entre dois vetores
    def menor_valor(self, vet1, vet2):
        menor1= vet1[0]
        menor2= vet2[0]
        #print('{},{}'.format(str(maior1),str(maior2)))
        for a in range(0, len(vet1)):
            if float(menor1) > vet1[a] and str(vet1[a])!='nan' or str(menor1)=='nan':
                menor1 = vet1[a]
        for a in range(0, len(vet2)):
            if float(menor2) > vet2[a] and str(vet2[a])!='nan' or str(menor2)=='nan':
                menor2 = vet2[a]
        
        
        if str(menor1)=='nan' and str(menor2)=='nan':
            return 0
        
        if menor1 < menor2 or str(menor2)=='nan':
            return menor1
        
        return menor2
    

    ### metodo usado para criar os vetores que serão usados no plots
    def dados_plt(self, Stereo_name):
        btotal = []
        np = []
        speed = []
        temperature = []
        beta = []
        total_pressure = []
        bx = []
        by = []
        bz = []
        time = []
        
        '''
        ### para receber da data inicial
        data_em_texto = '{}/{}/{}'.format(Stereo_name[0].getDay(), Stereo_name[0].getMonth(), Stereo_name[0].getYear())
        SDay = datetime.strptime(data_em_texto, '%d/%m/%Y')
        '''
        
        ### para descobrir o ultimo dia do mes da data inicial
        dia = '01'
        data_em_texto = '{}/{}/{}'.format(dia, Stereo_name[0].getMonth(), Stereo_name[0].getYear())
        
        Day1 = datetime.strptime(data_em_texto, '%d/%m/%Y') # primeiro dia do primeiro mes
        
        Day1 = datetime.fromordinal(Day1.toordinal()+32) #avança para o mes seguinde
        data_em_texto = '{}/{}/{}'.format(dia, Day1.month, Day1.year) #primeiro dia do mes seguinde
        
        Day1 = datetime.strptime(data_em_texto, '%d/%m/%Y') # day1 recebe a data do primeiro dia do mes seguinde
        
        Day1 = datetime.fromordinal(Day1.toordinal()-1) #retrocede para o ultimo dia do mes anterior
        
        ### auxiliares
        S_month = Stereo_name[0].getMonth() ### mes inicial
        E_day = Day1.day ### ultimo dia do mes inicial
        
        ### recebendo vetores
        for z in range(0,len(Stereo_name)):
            
            month = Stereo_name[z].getMonth() #se o mes atual é igual ao inicial
            if S_month == month:         # tempo vai receber o tempo corrido do referente dia
                tempo = float(Stereo_name[z].getDay()) + (float(Stereo_name[z].getHour())*60 + float(Stereo_name[z].getMinute()))/1440
            else: #se não tempo vai receber o valor do dia final mais a soma do dia corrido atual, ps:na mudança de mes o dia corrido atual vai reiniciar no 1
                tempo = float(E_day) + float(Stereo_name[z].getDay()) + (float(Stereo_name[z].getHour())*60 + float(Stereo_name[z].getMinute()))/1440
            
            time.append(tempo)
            np.append(Stereo_name[z].getNP())
            speed.append(Stereo_name[z].getSpeed())
            temperature.append(Stereo_name[z].getTemperature())
            beta.append(Stereo_name[z].getBETA())
            total_pressure.append(Stereo_name[z].getTOTAL_PRESSURE())
            btotal.append(Stereo_name[z].getBTOTAL())
            bx.append(Stereo_name[z].getBX())
            by.append(Stereo_name[z].getBY())
            bz.append(Stereo_name[z].getBZ())
        ###
           
        # retornando vetor de vetores
        AUX = [np, speed, temperature, beta, total_pressure, btotal, bx, by, bz, time]
        return AUX;
    
    
    
    
    ### metodo que baixa os arquivos
    def asciiDataDownload_2(self, S_year, S_month, S_day, E_year, E_month, E_day, verbose=True):
        
        aux = str(self.getDirectory()).split("\ ".strip())
        caminho = str(aux[0])
        #print(len(aux))
        
        if len(aux) == 1:
            self.createFolder(caminho)
        else:
            for i in range(0, len(aux)):
                if i==0:
                    self.createFolder(caminho)
                else:
                    caminho = caminho+"\ ".strip() + aux[i]
                    self.createFolder(caminho)
            
        # verifica se ambos os arquivos existem, se sim pergunta se quer substituí-los
        if(self.verificar_arquivo('STA', S_year, S_month, S_day, E_year, E_month, E_day)==True and self.verificar_arquivo('STB', S_year, S_month, S_day, E_year, E_month, E_day)==True):
            print('Ambos os arquivos existem!')
            print('Digite: S para sim ou N para nao')
            baixar = input('Deseja substituir esses arquivos?').upper()
            
            if baixar=='S' or baixar=='SIM':
                try:
                    webpage = urlopen("https://cdaweb.gsfc.nasa.gov/cgi-bin/eval3.cgi?dataset=STA_L2_MAGPLASMA1M%20STB_L2_MAGPLASMA_1M&select=custom&start={}%2F{}%2F{}+00%3A00%3A00.000&stop={}%2F{}%2F{}+23%3A59%3A00.000&index=istp_public&action=list&var=STA_L2_MAGPLASMA_1M+BTOTAL&var=STB_L2_MAGPLASMA_1M+BTOTAL&var=STA_L2_MAGPLASMA_1M+Np&var=STB_L2_MAGPLASMA_1M+Np&var=STA_L2_MAGPLASMA_1M+BFIELDRTN&var=STB_L2_MAGPLASMA_1M+BFIELDRTN&var=STA_L2_MAGPLASMA_1M+Vp_RTN&var=STB_L2_MAGPLASMA_1M+Vp_RTN&var=STA_L2_MAGPLASMA_1M+Beta&var=STB_L2_MAGPLASMA_1M+Beta&var=STA_L2_MAGPLASMA_1M+Total_Pressure&var=STB_L2_MAGPLASMA_1M+Total_Pressure&var=STA_L2_MAGPLASMA_1M+Vp&var=STB_L2_MAGPLASMA_1M+Vp&var=STA_L2_MAGPLASMA_1M+Tp&var=STB_L2_MAGPLASMA_1M+Tp".format(S_year, S_month, S_day, E_year, E_month, E_day))
                except:
                    print("Site não encontrado.")
                else:
                    print('input url: '+'https://cdaweb.gsfc.nasa.gov/cgi-bin/eval3.cgi?dataset=STA_L2_MAGPLASMA1M%20STB_L2_MAGPLASMA_1M&select=custom&start={}%2F{}%2F{}+00%3A00%3A00.000&stop={}%2F{}%2F{}+23%3A59%3A00.000&index=istp_public&action=list&var=STA_L2_MAGPLASMA_1M+BTOTAL&var=STB_L2_MAGPLASMA_1M+BTOTAL&var=STA_L2_MAGPLASMA_1M+Np&var=STB_L2_MAGPLASMA_1M+Np&var=STA_L2_MAGPLASMA_1M+BFIELDRTN&var=STB_L2_MAGPLASMA_1M+BFIELDRTN&var=STA_L2_MAGPLASMA_1M+Vp_RTN&var=STB_L2_MAGPLASMA_1M+Vp_RTN&var=STA_L2_MAGPLASMA_1M+Beta&var=STB_L2_MAGPLASMA_1M+Beta&var=STA_L2_MAGPLASMA_1M+Total_Pressure&var=STB_L2_MAGPLASMA_1M+Total_Pressure&var=STA_L2_MAGPLASMA_1M+Vp&var=STB_L2_MAGPLASMA_1M+Vp&var=STA_L2_MAGPLASMA_1M+Tp&var=STB_L2_MAGPLASMA_1M+Tp\n'.format(S_year, S_month, S_day, E_year, E_month, E_day))
                    
                    webpageHtml = webpage.readlines()
                    print(BOLD+GREEN+"Reading webpage's html...\n"+RESET)
                    
                    
                    caminho=self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day #verifica e se necessário cria a pasta referente ao periodo de tempo
                    self.createFolder(caminho)
                    
                    
                    ###  pegando o arquivo STA  ###        
                    linkEnd = str(webpageHtml).find("\">STA_L2_MAGPLASMA_1M_")
                    linkStart = str(webpageHtml).find("href=\"/tmp/STA_L2")+6
                    dataLink = 'https://cdaweb.gsfc.nasa.gov/'+ str(webpageHtml)[linkStart:linkEnd]
                    
                    try:
                        urlretrieve(dataLink)
                    except FileNotFoundError:
                        print('Algo de errado nao está certo.')
                    else:
                        urlretrieve(dataLink, self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day+'/STA.txt')
                        
                    
                    ###  pegando arquivo STB  ###
                    linkEnd = str(webpageHtml).find("\">STB_L2_MAGPLASMA_1M_")
                    linkStart = str(webpageHtml).find("href=\"/tmp/STB_L2")+6
                    dataLink = 'https://cdaweb.gsfc.nasa.gov/'+ str(webpageHtml)[linkStart:linkEnd]
                    
                    try:
                        urlretrieve(dataLink)
                    except FileNotFoundError:
                        print('Algo de errado nao está certo.')
                    else:
                        urlretrieve(dataLink, self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day+'/STB.txt')
                
        # se nao, seja que exista apenas 1 ou nenhum
        else:
            baixar_STA='S'
            baixar_STB='S'
            
            try:
                webpage = urlopen("https://cdaweb.gsfc.nasa.gov/cgi-bin/eval3.cgi?dataset=STA_L2_MAGPLASMA1M%20STB_L2_MAGPLASMA_1M&select=custom&start={}%2F{}%2F{}+00%3A00%3A00.000&stop={}%2F{}%2F{}+23%3A59%3A00.000&index=istp_public&action=list&var=STA_L2_MAGPLASMA_1M+BTOTAL&var=STB_L2_MAGPLASMA_1M+BTOTAL&var=STA_L2_MAGPLASMA_1M+Np&var=STB_L2_MAGPLASMA_1M+Np&var=STA_L2_MAGPLASMA_1M+BFIELDRTN&var=STB_L2_MAGPLASMA_1M+BFIELDRTN&var=STA_L2_MAGPLASMA_1M+Vp_RTN&var=STB_L2_MAGPLASMA_1M+Vp_RTN&var=STA_L2_MAGPLASMA_1M+Beta&var=STB_L2_MAGPLASMA_1M+Beta&var=STA_L2_MAGPLASMA_1M+Total_Pressure&var=STB_L2_MAGPLASMA_1M+Total_Pressure&var=STA_L2_MAGPLASMA_1M+Vp&var=STB_L2_MAGPLASMA_1M+Vp&var=STA_L2_MAGPLASMA_1M+Tp&var=STB_L2_MAGPLASMA_1M+Tp".format(S_year, S_month, S_day, E_year, E_month, E_day))
            except:
                print("Site não encontrado.")
            else:
                print('input url: '+'https://cdaweb.gsfc.nasa.gov/cgi-bin/eval3.cgi?dataset=STA_L2_MAGPLASMA1M%20STB_L2_MAGPLASMA_1M&select=custom&start={}%2F{}%2F{}+00%3A00%3A00.000&stop={}%2F{}%2F{}+23%3A59%3A00.000&index=istp_public&action=list&var=STA_L2_MAGPLASMA_1M+BTOTAL&var=STB_L2_MAGPLASMA_1M+BTOTAL&var=STA_L2_MAGPLASMA_1M+Np&var=STB_L2_MAGPLASMA_1M+Np&var=STA_L2_MAGPLASMA_1M+BFIELDRTN&var=STB_L2_MAGPLASMA_1M+BFIELDRTN&var=STA_L2_MAGPLASMA_1M+Vp_RTN&var=STB_L2_MAGPLASMA_1M+Vp_RTN&var=STA_L2_MAGPLASMA_1M+Beta&var=STB_L2_MAGPLASMA_1M+Beta&var=STA_L2_MAGPLASMA_1M+Total_Pressure&var=STB_L2_MAGPLASMA_1M+Total_Pressure&var=STA_L2_MAGPLASMA_1M+Vp&var=STB_L2_MAGPLASMA_1M+Vp&var=STA_L2_MAGPLASMA_1M+Tp&var=STB_L2_MAGPLASMA_1M+Tp\n'.format(S_year, S_month, S_day, E_year, E_month, E_day))
                
                webpageHtml = webpage.readlines()
                print(BOLD+GREEN+"Reading webpage's html...\n"+RESET)
                
                caminho=self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day #verifica e se necessário cria a pasta referente ao periodo de tempo
                self.createFolder(caminho)
                
                ###  pegando o arquivo STA  ###       
                if(self.verificar_arquivo('STA', S_year, S_month, S_day, E_year, E_month, E_day)==True): #verifica se o apenas STA existe, se sim 
                                                                        #pergunta se quer baixar, alterando assim o 
                                                                        #baixar que vai definir se vai baixar ou não.
                                                                        #PS:ele inicia com sim, caso o arquivo 
                                                                        #não exista ele vai baixa-lo, sem 
                                                                        #ter que passar pela pergunta
                                                                        
                    
                    print('O arquivo STA existe!')
                    print('Digite: S para sim ou N para nao')
                    baixar_STA = input('Deseja substituir esses arquivos?').upper()
                    
                if baixar_STA=='S' or baixar_STA=='SIM':
                    linkEnd = str(webpageHtml).find("\">STA_L2_MAGPLASMA_1M_")
                    linkStart = str(webpageHtml).find("href=\"/tmp/STA_L2")+6
                    dataLink = 'https://cdaweb.gsfc.nasa.gov/'+ str(webpageHtml)[linkStart:linkEnd]
                    
                    try:
                        urlretrieve(dataLink)
                    except FileNotFoundError:
                        print('Algo de errado nao está certo.')
                    else:
                        urlretrieve(dataLink, self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day+'/STA.txt')
                
                ###  pegando arquivo STB  ###
                if(self.verificar_arquivo('STB', S_year, S_month, S_day, E_year, E_month, E_day)==True): #verifica se o apenas STB existe, se sim 
                                                                        #pergunta se quer baixar, alterando assim o 
                                                                        #baixar que vai definir se vai baixar ou não.
                                                                        #PS:ele inicia com sim, caso o arquivo 
                                                                        #não exista ele vai baixa-lo, sem 
                                                                        #ter que passar pela pergunta
                                                                        
                    
                    print('O arquivo STB existe!')
                    print('Digite: S para sim ou N para nao')
                    baixar_STB = input('Deseja substituir esses arquivos?').upper()
                    
                if baixar_STB=='S' or baixar_STB=='SIM':
                    linkEnd = str(webpageHtml).find("\">STB_L2_MAGPLASMA_1M_")
                    linkStart = str(webpageHtml).find("href=\"/tmp/STB_L2")+6
                    dataLink = 'https://cdaweb.gsfc.nasa.gov/'+ str(webpageHtml)[linkStart:linkEnd]
                    
                    try:
                        urlretrieve(dataLink)
                    except FileNotFoundError:
                        print('Algo de errado nao está certo.')
                    else:
                        urlretrieve(dataLink, self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day+'/STB.txt')       

#caminho='Arquivos\S_'.strip(' ')+year+month+S_day+' E_'+year+month+E_day
    ### metodo que cria o plot
    def plot_and_subplot(self, S_year, S_month, S_day, E_year, E_month, E_day, shock_sta, shock_stb):
        
        caminho=self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day
        Rplot='S'
        
        ### verifica se a imagem já existe ###
        if os.path.exists(caminho+'/STA-STB.png'):
            print('A imagem ja existe.')
            Rplot=input('Deseja replotar a imagem?').upper()
            
            if Rplot=="N" or Rplot=="NAO":
                im = img.Image.open(caminho+'/STA-STB.png')
                im.show()
                im.close()
        ### termino da verificação ###
        
        
        ### se ela não existe ou se o úsuario optou por replota-la
        if Rplot=='S' or Rplot=='SIM':
        
            ### verificando a existência dos arquivos necessários para que o gráfico possa ser gerado.
            if self.verificar_arquivo('STA', S_year, S_month, S_day, E_year, E_month, E_day)==False or self.verificar_arquivo('STB', S_year, S_month, S_day, E_year, E_month, E_day)==False:
                print('Um ou ambos os arquivos não existem. Deseja baixá-los?')
                baixar = input('Digite S para sim ou N para nao.').upper()
                
                if baixar=='S' or baixar=='SIM':
                    #event_day=year+month+S_day
                    self.asciiDataDownload_2(S_year, S_month, S_day, E_year, E_month, E_day)
                    
                else:
                    Rplot='N'
            ### fim da verificação
            
            
            
            ### se ambos os arquivos existem ou se o úsuario optou por baixar
                        ### os que não existem
            if Rplot=='S' or Rplot=='SIM':
                
                fig = plt.figure()
                plt.subplots_adjust(left=-2, bottom=-2, right=1.15, top=2.4,
                                    wspace=0.33, hspace=0.2)
                
                
                #plt.subplots_adjust(left=0.125, bottom=0.1, right=1.15, top=2.4,
                 #                   wspace=0.33, hspace=0.2)
                
                
                x1_plt = fig.add_subplot(9, 2, 1)
                x2_plt = fig.add_subplot(9, 2, 3)
                x3_plt = fig.add_subplot(9, 2, 5)
                x4_plt = fig.add_subplot(9, 2, 7)
                x5_plt = fig.add_subplot(9, 2, 9)
                x6_plt = fig.add_subplot(9, 2, 11)
                x7_plt = fig.add_subplot(9, 2, 13)
                x8_plt = fig.add_subplot(9, 2, 15)
                x9_plt = fig.add_subplot(9, 2, 17)
                
                x11_plt = fig.add_subplot(9, 2, 2)
                x12_plt = fig.add_subplot(9, 2, 4)
                x13_plt = fig.add_subplot(9, 2, 6)
                x14_plt = fig.add_subplot(9, 2, 8)
                x15_plt = fig.add_subplot(9, 2, 10)
                x16_plt = fig.add_subplot(9, 2, 12)
                x17_plt = fig.add_subplot(9, 2, 14)
                x18_plt = fig.add_subplot(9, 2, 16)
                x19_plt = fig.add_subplot(9, 2, 18)
                
                STA = [dados()]; #inicializando a variavel com os valores de STA
                STB = [dados()]; #inicializando a variavel com os valores de STA
                
                STA = self.separar_dados('STA', S_year, S_month, S_day, E_year, E_month, E_day);
                STB = self.separar_dados('STB', S_year, S_month, S_day, E_year, E_month, E_day);
                
                DADOS_STA = self.dados_plt(STA);
                DADOS_STB = self.dados_plt(STB);
                
                #titulo = ['$N_p (1/cm^3)$', '$V_p$ (Km/s)', '$T_p (\deg(k))$', '$\beta$', '$P_T$ (nPa)', 'nT']
                titulo = ['$N_p (1/cm^3)$', '$V_p$ (Km/s)', '$T_p k^o$', '$Beta (Log)$', '$P_T$ (nPa)', '$B_T (nT)$', '$B_x (nT)$', '$B_y (nT)$', '$B_z (nT)$']
                #Y_LABEL = ['NP', 'Speed', 'Temperature', 'Beta', 'Total Pressure', 'BTotal', 'Bx', 'By', 'Bz']
                
                ### para colocar os Xsticks
                minimo = min(DADOS_STA[9])
                maximo = max(DADOS_STA[9])
                x = []
                for z in range(int(minimo), int(maximo)+1, 1):
                    x.append(z)
                #print(x)
                
                texto_data = []
                
                data_em_texto = '{}/{}/{}'.format(S_day, S_month, S_year)
                S_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
                
                data_em_texto = '{}/{}/{}'.format(E_day, E_month, E_year)
                E_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
                E_Day = datetime.fromordinal(E_Day.toordinal()+1)
                
                
                while S_Day != datetime.fromordinal(E_Day.toordinal()+1):
                    texto_data.append(S_Day.strftime('%d/%m/%Y'))
                    texto_data.append('')
                    texto_data.append('')
                    texto_data.append('')
                    S_Day = datetime.fromordinal(S_Day.toordinal()+1)
                    
                
                
                ### obtendo o valor de beta em log de base 10 para STA
                beta_sta = []
                for a in range(0, len(DADOS_STA[3])):
                    beta_sta.append(math.log(DADOS_STA[3][a],10))
                    
                    
                ### obtendo o valor de beta em log de base 10 para STB
                beta_stb = []
                for a in range(0, len(DADOS_STB[3])):
                    beta_stb.append(math.log(DADOS_STB[3][a],10))
                
                
                
                
                
                
                
                
                
                x1_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[0],DADOS_STB[0]) - 0.1*abs(self.menor_valor(DADOS_STA[0],DADOS_STB[0])), self.maior_valor(DADOS_STA[0],DADOS_STB[0]) + 0.1*abs(self.maior_valor(DADOS_STA[0],DADOS_STB[0]))))
                x11_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[0],DADOS_STB[0]) - 0.1*abs(self.menor_valor(DADOS_STA[0],DADOS_STB[0])), self.maior_valor(DADOS_STA[0],DADOS_STB[0]) + 0.1*abs(self.maior_valor(DADOS_STA[0],DADOS_STB[0]))))     
                
                x2_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[1],DADOS_STB[1]) - 0.1*abs(self.menor_valor(DADOS_STA[1],DADOS_STB[1])), self.maior_valor(DADOS_STA[1],DADOS_STB[1]) + 0.1*abs(self.maior_valor(DADOS_STA[1],DADOS_STB[1]))))
                x12_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[1],DADOS_STB[1]) - 0.1*abs(self.menor_valor(DADOS_STA[1],DADOS_STB[1])), self.maior_valor(DADOS_STA[1],DADOS_STB[1]) + 0.1*abs(self.maior_valor(DADOS_STA[1],DADOS_STB[1]))))
                
                x3_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[2],DADOS_STB[2]) - 0.1*abs(self.menor_valor(DADOS_STA[2],DADOS_STB[2])), self.maior_valor(DADOS_STA[2],DADOS_STB[2]) + 0.1*abs(self.maior_valor(DADOS_STA[2],DADOS_STB[2]))))
                x13_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[2],DADOS_STB[2]) - 0.1*abs(self.menor_valor(DADOS_STA[2],DADOS_STB[2])), self.maior_valor(DADOS_STA[2],DADOS_STB[2]) + 0.1*abs(self.maior_valor(DADOS_STA[2],DADOS_STB[2]))))
                
                x4_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(beta_sta,beta_stb) - 0.1*abs(self.menor_valor(beta_sta,beta_stb)), self.maior_valor(beta_sta,beta_stb) + 0.1*abs(self.maior_valor(beta_sta,beta_stb))))
                x14_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(beta_sta,beta_stb) - 0.1*abs(self.menor_valor(beta_sta,beta_stb)), self.maior_valor(beta_sta,beta_stb) + 0.1*abs(self.maior_valor(beta_sta,beta_stb))))
                
                x5_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[4],DADOS_STB[4]) - 0.1*abs(self.menor_valor(DADOS_STA[4],DADOS_STB[4])), self.maior_valor(DADOS_STA[4],DADOS_STB[4]) + 0.1*abs(self.maior_valor(DADOS_STA[4],DADOS_STB[4]))))
                x15_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[4],DADOS_STB[4]) - 0.1*abs(self.menor_valor(DADOS_STA[4],DADOS_STB[4])), self.maior_valor(DADOS_STA[4],DADOS_STB[4]) + 0.1*abs(self.maior_valor(DADOS_STA[4],DADOS_STB[4]))))               
                
                x6_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[5],DADOS_STB[5])-0.1*abs(self.menor_valor(DADOS_STA[5],DADOS_STB[5])), self.maior_valor(DADOS_STA[5],DADOS_STB[5]) + 0.1*abs(self.maior_valor(DADOS_STA[5],DADOS_STB[5]))))
                x16_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[5],DADOS_STB[5])-0.1*abs(self.menor_valor(DADOS_STA[5],DADOS_STB[5])), self.maior_valor(DADOS_STA[5],DADOS_STB[5]) + 0.1*abs(self.maior_valor(DADOS_STA[5],DADOS_STB[5]))))
                
                x7_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[6],DADOS_STB[6])-0.1*abs(self.menor_valor(DADOS_STA[6],DADOS_STB[6])), self.maior_valor(DADOS_STA[6],DADOS_STB[6]) + 0.1*abs(self.maior_valor(DADOS_STA[6],DADOS_STB[6]))))
                x17_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[6],DADOS_STB[6])-0.1*abs(self.menor_valor(DADOS_STA[6],DADOS_STB[6])), self.maior_valor(DADOS_STA[6],DADOS_STB[6]) + 0.1*abs(self.maior_valor(DADOS_STA[6],DADOS_STB[6]))))
                
                x8_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[7],DADOS_STB[7])-0.1*abs(self.menor_valor(DADOS_STA[7],DADOS_STB[7])), self.maior_valor(DADOS_STA[7],DADOS_STB[7]) + 0.1*abs(self.maior_valor(DADOS_STA[7],DADOS_STB[7]))))
                x18_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[7],DADOS_STB[7])-0.1*abs(self.menor_valor(DADOS_STA[7],DADOS_STB[7])), self.maior_valor(DADOS_STA[7],DADOS_STB[7]) + 0.1*abs(self.maior_valor(DADOS_STA[7],DADOS_STB[7]))))
                
                x9_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[8],DADOS_STB[8])-0.1*abs(self.menor_valor(DADOS_STA[8],DADOS_STB[8])), self.maior_valor(DADOS_STA[8],DADOS_STB[8]) + 0.1*abs(self.maior_valor(DADOS_STA[8],DADOS_STB[8]))))
                x19_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[8],DADOS_STB[8])-0.1*abs(self.menor_valor(DADOS_STA[8],DADOS_STB[8])), self.maior_valor(DADOS_STA[8],DADOS_STB[8]) + 0.1*abs(self.maior_valor(DADOS_STA[8],DADOS_STB[8]))))
                
                
                x1_plt.plot(DADOS_STA[9], DADOS_STA[0], color='black', linewidth=1)
                x1_plt.set_title("STA")#('BTOTAL - BX - BY - BZ', fontsize=7, x=1, y=0)
                x1_plt.set_ylabel(titulo[0])
                x1_plt.set_xticklabels('')
                start, end = x1_plt.get_xlim()
                x1_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x2_plt.plot(DADOS_STA[9], DADOS_STA[1], color='black', linewidth=1)
                x2_plt.set_ylabel(titulo[1])
                x2_plt.set_xticklabels('')
                start, end = x2_plt.get_xlim()
                x2_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x3_plt.plot(DADOS_STA[9], DADOS_STA[2], color='black', linewidth=1)
                x3_plt.set_ylabel(titulo[2])
                x3_plt.set_xticklabels('')
                start, end = x3_plt.get_xlim()
                x3_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    
                x4_plt.plot(DADOS_STA[9], beta_sta, color='black', linewidth=1)
                x4_plt.set_ylabel(titulo[3])
                x4_plt.set_xticklabels('')
                start, end = x4_plt.get_xlim()
                x4_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x4_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                x5_plt.plot(DADOS_STA[9], DADOS_STA[4], color='black', linewidth=1)
                x5_plt.set_ylabel(titulo[4])
                x5_plt.set_xticklabels('')   
                start, end = x5_plt.get_xlim()
                x5_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x6_plt.plot(DADOS_STA[9], DADOS_STA[5], color='black', linewidth=1)
                x6_plt.set_ylabel(titulo[5])
                x6_plt.set_xticklabels('')
                start, end = x6_plt.get_xlim()
                x6_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x7_plt.plot(DADOS_STA[9], DADOS_STA[6], color='black', linewidth=1)
                x7_plt.set_ylabel(titulo[6])
                x7_plt.set_xticklabels('')
                start, end = x7_plt.get_xlim()
                x7_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x7_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                x8_plt.plot(DADOS_STA[9], DADOS_STA[7], color='black', linewidth=1)
                x8_plt.set_ylabel(titulo[7])
                x8_plt.set_xticklabels('')
                start, end = x8_plt.get_xlim()
                x8_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x8_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                x9_plt.plot(DADOS_STA[9], DADOS_STA[8], color='black', linewidth=1)
                x9_plt.set_ylabel(titulo[8])
                x9_plt.set_xlabel('Dia')
                start, end = x9_plt.get_xlim()
                x9_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x9_plt.set_xticklabels(texto_data)
                x9_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                            
                x11_plt.plot(DADOS_STB[9], DADOS_STB[0], color='black', linewidth=1, label='')
                x11_plt.set_title("STB")#('BTOTAL - BX - BY - BZ', fontsize=7, x=1, y=0)
                x11_plt.set_ylabel(titulo[0])
                x11_plt.set_xticklabels('')
                start, end = x11_plt.get_xlim()
                x11_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x12_plt.plot(DADOS_STB[9], DADOS_STB[1], color='black', linewidth=1, label='')
                x12_plt.set_ylabel(titulo[1])
                x12_plt.set_xticklabels('')
                start, end = x12_plt.get_xlim()
                x12_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x13_plt.plot(DADOS_STB[9], DADOS_STB[2], color='black', linewidth=1, label='')
                x13_plt.set_ylabel(titulo[2])
                x13_plt.set_xticklabels('')
                start, end = x13_plt.get_xlim()
                x13_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x14_plt.plot(DADOS_STB[9], beta_stb, color='black', linewidth=1, label='')
                x14_plt.set_ylabel(titulo[3])
                x14_plt.set_xticklabels('')
                start, end = x14_plt.get_xlim()
                x14_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x14_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                x15_plt.plot(DADOS_STB[9], DADOS_STB[4], color='black', linewidth=1, label='')
                x15_plt.set_ylabel(titulo[4])
                x15_plt.set_xticklabels('')
                start, end = x15_plt.get_xlim()
                x15_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x16_plt.plot(DADOS_STB[9], DADOS_STB[5], color='black', linewidth=1)
                x16_plt.set_ylabel(titulo[5])
                x16_plt.set_xlabel('')
                x16_plt.set_xticklabels('')
                start, end = x16_plt.get_xlim()
                x16_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                
                x17_plt.plot(DADOS_STB[9], DADOS_STB[6], color='black', linewidth=1)
                x17_plt.set_ylabel(titulo[6])
                x17_plt.set_xlabel('')
                x17_plt.set_xticklabels('')
                start, end = x17_plt.get_xlim()
                x17_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x17_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                x18_plt.plot(DADOS_STB[9], DADOS_STB[7], color='black', linewidth=1)
                x18_plt.set_ylabel(titulo[7])
                x18_plt.set_xlabel('')
                x18_plt.set_xticklabels('')
                start, end = x18_plt.get_xlim()
                x18_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x18_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                x19_plt.plot(DADOS_STB[9], DADOS_STB[8], color='black', linewidth=1)
                x19_plt.set_ylabel(titulo[8])
                x19_plt.set_xlabel('Dia')
                start, end = x19_plt.get_xlim()
                x19_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                x19_plt.set_xticklabels(texto_data)
                x19_plt.plot([self.menor_valor(DADOS_STA[9],DADOS_STB[9]),self.maior_valor(DADOS_STA[9],DADOS_STB[9])], [0,0])
                
                
                ###plotando o corte no gráfico STA
                for z in range(0, len(shock_sta)):
                    x1_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[0],DADOS_STB[0]) - 0.1*abs(self.menor_valor(DADOS_STA[0],DADOS_STB[0])), self.maior_valor(DADOS_STA[0],DADOS_STB[0]) + 0.1*abs(self.maior_valor(DADOS_STA[0],DADOS_STB[0]))], 'b--', color='red', linewidth=1)
                    x2_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[1],DADOS_STB[1]) - 0.1*abs(self.menor_valor(DADOS_STA[1],DADOS_STB[1])), self.maior_valor(DADOS_STA[1],DADOS_STB[1]) + 0.1*abs(self.maior_valor(DADOS_STA[1],DADOS_STB[1]))], 'b--', color='red', linewidth=1)
                    x3_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[2],DADOS_STB[2]) - 0.1*abs(self.menor_valor(DADOS_STA[2],DADOS_STB[2])), self.maior_valor(DADOS_STA[2],DADOS_STB[2]) + 0.1*abs(self.maior_valor(DADOS_STA[2],DADOS_STB[2]))], 'b--', color='red', linewidth=1)
                    x4_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(beta_sta,beta_stb) - 0.1*abs(self.menor_valor(beta_sta,beta_stb)), self.maior_valor(beta_sta,beta_stb) + 0.1*abs(self.maior_valor(beta_sta,beta_stb))], 'b--', color='red', linewidth=1)
                    x5_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[4],DADOS_STB[4]) - 0.1*abs(self.menor_valor(DADOS_STA[4],DADOS_STB[4])), self.maior_valor(DADOS_STA[4],DADOS_STB[4]) + 0.1*abs(self.maior_valor(DADOS_STA[4],DADOS_STB[4]))], 'b--', color='red', linewidth=1)
                    x6_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[5],DADOS_STB[5]) - 0.1*abs(self.menor_valor(DADOS_STA[5],DADOS_STB[5])), self.maior_valor(DADOS_STA[5],DADOS_STB[5]) + 0.1*abs(self.maior_valor(DADOS_STA[5],DADOS_STB[5]))], 'b--', color='red', linewidth=1)
                    x7_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[6],DADOS_STB[6]) - 0.1*abs(self.menor_valor(DADOS_STA[6],DADOS_STB[6])), self.maior_valor(DADOS_STA[6],DADOS_STB[6]) + 0.1*abs(self.maior_valor(DADOS_STA[6],DADOS_STB[6]))], 'b--', color='red', linewidth=1)
                    x8_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[7],DADOS_STB[7]) - 0.1*abs(self.menor_valor(DADOS_STA[7],DADOS_STB[7])), self.maior_valor(DADOS_STA[7],DADOS_STB[7]) + 0.1*abs(self.maior_valor(DADOS_STA[7],DADOS_STB[7]))], 'b--', color='red', linewidth=1)
                    x9_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[8],DADOS_STB[8]) - 0.1*abs(self.menor_valor(DADOS_STA[8],DADOS_STB[8])), self.maior_valor(DADOS_STA[8],DADOS_STB[8]) + 0.1*abs(self.maior_valor(DADOS_STA[8],DADOS_STB[8]))], 'b--', color='red', linewidth=1)
                
                ###plotando o corte no gráfico STB
                for y in range(0, len(shock_stb)):
                    x11_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[0],DADOS_STB[0]) - 0.1*abs(self.menor_valor(DADOS_STA[0],DADOS_STB[0])), self.maior_valor(DADOS_STA[0],DADOS_STB[0]) + 0.1*abs(self.maior_valor(DADOS_STA[0],DADOS_STB[0]))], 'b--', color='red', linewidth=1)
                    x12_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[1],DADOS_STB[1]) - 0.1*abs(self.menor_valor(DADOS_STA[1],DADOS_STB[1])), self.maior_valor(DADOS_STA[1],DADOS_STB[1]) + 0.1*abs(self.maior_valor(DADOS_STA[1],DADOS_STB[1]))], 'b--', color='red', linewidth=1)
                    x13_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[2],DADOS_STB[2]) - 0.1*abs(self.menor_valor(DADOS_STA[2],DADOS_STB[2])), self.maior_valor(DADOS_STA[2],DADOS_STB[2]) + 0.1*abs(self.maior_valor(DADOS_STA[2],DADOS_STB[2]))], 'b--', color='red', linewidth=1)
                    x14_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(beta_sta,beta_stb) - 0.1*abs(self.menor_valor(beta_sta,beta_stb)), self.maior_valor(beta_sta,beta_stb) + 0.1*abs(self.maior_valor(beta_sta,beta_stb))], 'b--', color='red', linewidth=1)
                    x15_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[4],DADOS_STB[4]) - 0.1*abs(self.menor_valor(DADOS_STA[4],DADOS_STB[4])), self.maior_valor(DADOS_STA[4],DADOS_STB[4]) + 0.1*abs(self.maior_valor(DADOS_STA[4],DADOS_STB[4]))], 'b--', color='red', linewidth=1)
                    x16_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[5],DADOS_STB[5]) - 0.1*abs(self.menor_valor(DADOS_STA[5],DADOS_STB[5])), self.maior_valor(DADOS_STA[5],DADOS_STB[5]) + 0.1*abs(self.maior_valor(DADOS_STA[5],DADOS_STB[5]))], 'b--', color='red', linewidth=1)
                    x17_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[6],DADOS_STB[6]) - 0.1*abs(self.menor_valor(DADOS_STA[6],DADOS_STB[6])), self.maior_valor(DADOS_STA[6],DADOS_STB[6]) + 0.1*abs(self.maior_valor(DADOS_STA[6],DADOS_STB[6]))], 'b--', color='red', linewidth=1)
                    x18_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[7],DADOS_STB[7]) - 0.1*abs(self.menor_valor(DADOS_STA[7],DADOS_STB[7])), self.maior_valor(DADOS_STA[7],DADOS_STB[7]) + 0.1*abs(self.maior_valor(DADOS_STA[7],DADOS_STB[7]))], 'b--', color='red', linewidth=1)
                    x19_plt.plot([shock_stb[y],shock_stb[y]], [self.menor_valor(DADOS_STA[8],DADOS_STB[8]) - 0.1*abs(self.menor_valor(DADOS_STA[8],DADOS_STB[8])), self.maior_valor(DADOS_STA[8],DADOS_STB[8]) + 0.1*abs(self.maior_valor(DADOS_STA[8],DADOS_STB[8]))], 'b--', color='red', linewidth=1)
                    
                fig.savefig(caminho+'/STA-STB.png', bbox_inches='tight')
                
                try:
                    figManager = plt.get_current_fig_manager()
                    figManager.window.showMaximized()
                except:
                    pass
                plt.show()
                
        if not os.path.exists(caminho+'/STA-STB.png') and Rplot=='N':
            print('OK. Entao nao ha como exibir nada.')
            
    def plot_and_subplot_somente1(self, S_year, S_month, S_day, E_year, E_month, E_day, shock_sta, shock_stb):
        
        caminho=self.getDirectory()+'\S_'+S_year+S_month+S_day+' E_'+E_year+E_month+E_day #verifica e se necessário cria a pasta referente ao periodo de tempo
                
        Rplot='S'
        ### verifica se a imagem já existe ###
        if os.path.exists(caminho+'/{}.png'.format('STA')) and os.path.exists(caminho+'/{}.png'.format('STB')):
            print('A imagem ja existe.')
            Rplot=input('Deseja replotar a imagem?').upper()
            
            if Rplot=="N" or Rplot=="NAO":
                im = img.Image.open(caminho+'/{}.png'.format('STA'))
                im.show()
                im.close()
                
                im = img.Image.open(caminho+'/{}.png'.format('STA'))
                im.show()
                im.close()
        ### termino da verificação ###
        
    
    ### se ela não existe ou se o úsuario optou por replota-la
        if Rplot=='S' or Rplot=='SIM':
        
            ### verificando a existência dos arquivos necessários para que o gráfico possa ser gerado.
            if self.verificar_arquivo('STA', S_year, S_month, S_day, E_year, E_month, E_day)==False or self.verificar_arquivo('STB', S_year, S_month, S_day, E_year, E_month, E_day)==False:
                print('Um ou ambos os arquivos não existem. Deseja baixá-los?')
                baixar = input('Digite S para sim ou N para nao.').upper()
                
                if baixar=='S' or baixar=='SIM':
                    #event_day=year+month+S_day
                    self.asciiDataDownload_2(S_year, S_month, S_day, E_year, E_month, E_day)
                    
                else:
                    Rplot='N'
            ### fim da verificação
            
            
            
            ### se ambos os arquivos existem ou se o úsuario optou por baixar
            ### os que não existem
            if Rplot=='S' or Rplot=='SIM':
                
                STA = [dados()]; #inicializando a variavel com os valores de STA
                STB = [dados()]; #inicializando a variavel com os valores de STA
                
                STA = self.separar_dados('STA', S_year, S_month, S_day, E_year, E_month, E_day);
                STB = self.separar_dados('STB', S_year, S_month, S_day, E_year, E_month, E_day);
                
                DADOS_STA = self.dados_plt(STA);
                DADOS_STB = self.dados_plt(STB);
                
                #titulo = ['$N_p (1/cm^3)$', '$V_p$ (Km/s)', '$T_p (\deg(k))$', '$\beta$', '$P_T$ (nPa)', 'nT']
                titulo = ['$N_p (1/cm^3)$', '$V_p$ (Km/s)', '$T_p k^o$', '$Beta (Log)$', '$P_T$ (nPa)', '$B_T (nT)$', '$B_x (nT)$', '$B_y (nT)$', '$B_z (nT)$']
                #Y_LABEL = ['NP', 'Speed', 'Temperature', 'Beta', 'Total Pressure', 'BTotal', 'Bx', 'By', 'Bz']
                
                
                ### obtendo o valor de beta em log de base 10 para STA
                beta_sta = []
                for a in range(0, len(DADOS_STA[3])):
                    beta_sta.append(math.log(DADOS_STA[3][a],10))
                    
                    
                ### obtendo o valor de beta em log de base 10 para STB
                beta_stb = []
                for a in range(0, len(DADOS_STB[3])):
                    beta_stb.append(math.log(DADOS_STB[3][a],10))
                
                name='STA'
                if(name=='STA'):
                    fig = plt_stereo.figure()
                    #plt_stereo.subplots_adjust(left=-2, bottom=-2, right=1.15, top=2.4,
                    #                   wspace=0.33, hspace=0.2)
                    
                    
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
                    
                    ### para colocar os Xsticks
                    minimo = min(DADOS_STA[9])
                    maximo = max(DADOS_STA[9])
                    x = []
                    for z in range(int(minimo), int(maximo)+1, 1):
                        x.append(z)
                    #print(x)
                    
                    texto_data = []
                    
                    data_em_texto = '{}/{}/{}'.format(S_day, S_month, S_year)
                    S_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
                    
                    data_em_texto = '{}/{}/{}'.format(E_day, E_month, E_year)
                    E_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
                    E_Day = datetime.fromordinal(E_Day.toordinal()+1)
                    
                    while S_Day != datetime.fromordinal(E_Day.toordinal()+1):
                        texto_data.append(S_Day.strftime('%d/%m/%Y'))
                        texto_data.append('')
                        texto_data.append('')
                        texto_data.append('')
                        S_Day = datetime.fromordinal(S_Day.toordinal()+1)
                        
                    #plt.xticks(x, texto_data)
                    ###
                    
                    '''
                    print(texto_data)
                    labels = [item.get_text() for item in x7_plt.get_xticklabels()]
                    #for j in range(0, len(x)):
                    labels[0] = texto_data[0]
                    labels[2] = texto_data[1]
                    labels[4] = texto_data[2]
                    labels[5] = texto_data[3]
                    '''                   
                    
                    x1_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[0],DADOS_STA[0]) - 0.1*abs(self.menor_valor(DADOS_STA[0],DADOS_STA[0])), self.maior_valor(DADOS_STA[0],DADOS_STA[0]) + 0.1*abs(self.maior_valor(DADOS_STA[0],DADOS_STA[0]))))
                    
                    x2_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[1],DADOS_STA[1]) - 0.1*abs(self.menor_valor(DADOS_STA[1],DADOS_STA[1])), self.maior_valor(DADOS_STA[1],DADOS_STA[1]) + 0.1*abs(self.maior_valor(DADOS_STA[1],DADOS_STA[1]))))
                    
                    x3_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[2],DADOS_STA[2]) - 0.1*abs(self.menor_valor(DADOS_STA[2],DADOS_STA[2])), self.maior_valor(DADOS_STA[2],DADOS_STA[2]) + 0.1*abs(self.maior_valor(DADOS_STA[2],DADOS_STA[2]))))
                    
                    x4_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(beta_sta,beta_sta) - 0.1*abs(self.menor_valor(beta_sta,beta_sta)), self.maior_valor(beta_sta,beta_sta) + 0.1*abs(self.maior_valor(beta_sta,beta_sta))))
                    
                    x5_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[4],DADOS_STA[4]) - 0.1*abs(self.menor_valor(DADOS_STA[4],DADOS_STA[4])), self.maior_valor(DADOS_STA[4],DADOS_STA[4]) + 0.1*abs(self.maior_valor(DADOS_STA[4],DADOS_STA[4]))))
                    
                    x6_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[5],DADOS_STA[5]) - 0.1*abs(self.menor_valor(DADOS_STA[5],DADOS_STA[5])), self.maior_valor(DADOS_STA[5],DADOS_STA[5]) + 0.1*abs(self.maior_valor(DADOS_STA[5],DADOS_STA[5]))))
                    
                    x7_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[6],DADOS_STA[6]) - 0.1*abs(self.menor_valor(DADOS_STA[6],DADOS_STA[6])), self.maior_valor(DADOS_STA[6],DADOS_STA[6]) + 0.1*abs(self.maior_valor(DADOS_STA[6],DADOS_STA[6]))))
                    
                    x8_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[7],DADOS_STA[7]) - 0.1*abs(self.menor_valor(DADOS_STA[7],DADOS_STA[7])), self.maior_valor(DADOS_STA[7],DADOS_STA[7]) + 0.1*abs(self.maior_valor(DADOS_STA[7],DADOS_STA[7]))))
                    
                    x9_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STA[8],DADOS_STA[8]) - 0.1*abs(self.menor_valor(DADOS_STA[8],DADOS_STA[8])), self.maior_valor(DADOS_STA[8],DADOS_STA[8]) + 0.1*abs(self.maior_valor(DADOS_STA[8],DADOS_STA[8]))))

                    
                    x1_plt.plot(DADOS_STA[9], DADOS_STA[0], color='black', linewidth=1)
                    x1_plt.set_title("STA")#('BTOTAL - BX - BY - BZ', fontsize=7, x=1, y=0)
                    x1_plt.set_ylabel(titulo[0])
                    start, end = x1_plt.get_xlim()
                    x1_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x1_plt.set_xticklabels('')
                    
                    x2_plt.plot(DADOS_STA[9], DADOS_STA[1], color='black', linewidth=1)
                    x2_plt.set_ylabel(titulo[1])
                    start, end = x2_plt.get_xlim()
                    x2_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x2_plt.set_xticklabels('')
                        
                    x3_plt.plot(DADOS_STA[9], DADOS_STA[2], color='black', linewidth=1)
                    x3_plt.set_ylabel(titulo[2])
                    start, end = x3_plt.get_xlim()
                    x3_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x3_plt.set_xticklabels('')
                                        
                    x4_plt.plot(DADOS_STA[9], beta_sta, color='black', linewidth=1)
                    x4_plt.set_ylabel(titulo[3])
                    start, end = x4_plt.get_xlim()
                    x4_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x4_plt.set_xticklabels('')
                    x4_plt.plot([min(DADOS_STA[9]),max(DADOS_STA[9])], [0,0])
                    
                    x5_plt.plot(DADOS_STA[9], DADOS_STA[4], color='black', linewidth=1)
                    x5_plt.set_ylabel(titulo[4])
                    start, end = x5_plt.get_xlim()
                    x5_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x5_plt.set_xticklabels('')    
                    
                    x6_plt.plot(DADOS_STA[9], DADOS_STA[5], color='black', linewidth=1)
                    x6_plt.set_ylabel(titulo[5])
                    x6_plt.set_xlabel('')
                    x6_plt.set_xticklabels('')
                    start, end = x6_plt.get_xlim()
                    x6_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    
                    x7_plt.plot(DADOS_STA[9], DADOS_STA[6], color='black', linewidth=1)
                    x7_plt.set_ylabel(titulo[6])
                    x7_plt.set_xlabel('')
                    x7_plt.set_xticklabels('')
                    start, end = x7_plt.get_xlim()
                    x7_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x7_plt.plot([min(DADOS_STA[9]),max(DADOS_STA[9])], [0,0])
                    
                    x8_plt.plot(DADOS_STA[9], DADOS_STA[7], color='black', linewidth=1)
                    x8_plt.set_ylabel(titulo[7])
                    x8_plt.set_xlabel('')
                    x8_plt.set_xticklabels('')
                    start, end = x8_plt.get_xlim()
                    x8_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x8_plt.plot([min(DADOS_STA[9]),max(DADOS_STA[9])], [0,0])
                    
                    x9_plt.plot(DADOS_STA[9], DADOS_STA[8], color='black', linewidth=1)
                    x9_plt.set_ylabel(titulo[8])
                    x9_plt.set_xlabel('Dia')
                    start, end = x9_plt.get_xlim()
                    x9_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x9_plt.set_xticklabels(texto_data)
                    x9_plt.plot([min(DADOS_STA[9]),max(DADOS_STA[9])], [0,0])
                    
                    ###plotando o corte no gráfico STA
                    for z in range(0, len(shock_sta)):
                        x1_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[0],DADOS_STB[0]) - 0.1*abs(self.menor_valor(DADOS_STA[0],DADOS_STB[0])), self.maior_valor(DADOS_STA[0],DADOS_STB[0]) + 0.1*abs(self.maior_valor(DADOS_STA[0],DADOS_STB[0]))], 'b--', color='red', linewidth=1)
                        x2_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[1],DADOS_STB[1]) - 0.1*abs(self.menor_valor(DADOS_STA[1],DADOS_STB[1])), self.maior_valor(DADOS_STA[1],DADOS_STB[1]) + 0.1*abs(self.maior_valor(DADOS_STA[1],DADOS_STB[1]))], 'b--', color='red', linewidth=1)
                        x3_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[2],DADOS_STB[2]) - 0.1*abs(self.menor_valor(DADOS_STA[2],DADOS_STB[2])), self.maior_valor(DADOS_STA[2],DADOS_STB[2]) + 0.1*abs(self.maior_valor(DADOS_STA[2],DADOS_STB[2]))], 'b--', color='red', linewidth=1)
                        x4_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(beta_sta,beta_sta) - 0.1*abs(self.menor_valor(beta_sta,beta_sta)), self.maior_valor(beta_sta,beta_sta) + 0.1*abs(self.maior_valor(beta_sta,beta_sta))], 'b--', color='red', linewidth=1)
                        x5_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[4],DADOS_STB[4]) - 0.1*abs(self.menor_valor(DADOS_STA[4],DADOS_STB[4])), self.maior_valor(DADOS_STA[4],DADOS_STB[4]) + 0.1*abs(self.maior_valor(DADOS_STA[4],DADOS_STB[4]))], 'b--', color='red', linewidth=1)
                        x6_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[5],DADOS_STB[5]) - 0.1*abs(self.menor_valor(DADOS_STA[5],DADOS_STB[5])), self.maior_valor(DADOS_STA[5],DADOS_STB[5]) + 0.1*abs(self.maior_valor(DADOS_STA[5],DADOS_STB[5]))], 'b--', color='red', linewidth=1)
                        x7_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[6],DADOS_STB[6]) - 0.1*abs(self.menor_valor(DADOS_STA[6],DADOS_STB[6])), self.maior_valor(DADOS_STA[6],DADOS_STB[6]) + 0.1*abs(self.maior_valor(DADOS_STA[6],DADOS_STB[6]))], 'b--', color='red', linewidth=1)
                        x8_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[7],DADOS_STB[7]) - 0.1*abs(self.menor_valor(DADOS_STA[7],DADOS_STB[7])), self.maior_valor(DADOS_STA[7],DADOS_STB[7]) + 0.1*abs(self.maior_valor(DADOS_STA[7],DADOS_STB[7]))], 'b--', color='red', linewidth=1)
                        x9_plt.plot([shock_sta[z],shock_sta[z]], [self.menor_valor(DADOS_STA[8],DADOS_STB[8]) - 0.1*abs(self.menor_valor(DADOS_STA[8],DADOS_STB[8])), self.maior_valor(DADOS_STA[8],DADOS_STB[8]) + 0.1*abs(self.maior_valor(DADOS_STA[8],DADOS_STB[8]))], 'b--', color='red', linewidth=1)
                    
                    
                    fig.savefig(caminho+'/{}.png'.format(name), bbox_inches='tight')
            
                    try:
                        figManager = plt.get_current_fig_manager()
                        figManager.window.showMaximized()
                    except:
                        pass
                    
                    
                    plt.show()
                    fig.clf()
                    plt.clf()
                    plt.close()
                
                name='STB'
                if(name=='STB'):
                    fig = plt_stereo.figure()
                    #plt_stereo.subplots_adjust(left=-2, bottom=-2, right=1.15, top=2.4,
                    #                   wspace=0.33, hspace=0.2)
                    
                    
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
                    
                    ### para colocar os Xsticks
                    minimo = min(DADOS_STA[9])
                    maximo = max(DADOS_STA[9])
                    x = []
                    for z in range(int(minimo), int(maximo)+1, 1):
                        x.append(z)
                    #print(x)
                    
                    texto_data = []
                    
                    data_em_texto = '{}/{}/{}'.format(S_day, S_month, S_year)
                    S_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
                    
                    data_em_texto = '{}/{}/{}'.format(E_day, E_month, E_year)
                    E_Day = datetime.strptime(data_em_texto, '%d/%m/%Y')
                    E_Day = datetime.fromordinal(E_Day.toordinal()+1)
                    
                    while S_Day != datetime.fromordinal(E_Day.toordinal()+1):
                        texto_data.append(S_Day.strftime('%d/%m/%Y'))
                        texto_data.append('')
                        texto_data.append('')
                        texto_data.append('')
                        S_Day = datetime.fromordinal(S_Day.toordinal()+1)
                        
                    #plt.xticks(x, texto_data)
                    ###
                    
                    x1_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[0],DADOS_STB[0]) - 0.1*abs(self.menor_valor(DADOS_STB[0],DADOS_STB[0])), self.maior_valor(DADOS_STB[0],DADOS_STB[0]) + 0.1*abs(self.maior_valor(DADOS_STB[0],DADOS_STB[0]))))
                    
                    x2_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[1],DADOS_STB[1]) - 0.1*abs(self.menor_valor(DADOS_STB[1],DADOS_STB[1])), self.maior_valor(DADOS_STB[1],DADOS_STB[1]) + 0.1*abs(self.maior_valor(DADOS_STB[1],DADOS_STB[1]))))
                    
                    x3_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[2],DADOS_STB[2]) - 0.1*abs(self.menor_valor(DADOS_STB[2],DADOS_STB[2])), self.maior_valor(DADOS_STB[2],DADOS_STB[2]) + 0.1*abs(self.maior_valor(DADOS_STB[2],DADOS_STB[2]))))
                    
                    x4_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(beta_stb,beta_stb) - 0.1*abs(self.menor_valor(beta_stb,beta_stb)), self.maior_valor(beta_stb,beta_stb) + 0.1*abs(self.maior_valor(beta_stb,beta_stb))))
                    
                    x5_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[4],DADOS_STB[4]) - 0.1*abs(self.menor_valor(DADOS_STB[4],DADOS_STB[4])), self.maior_valor(DADOS_STB[4],DADOS_STB[4]) + 0.1*abs(self.maior_valor(DADOS_STB[4],DADOS_STB[4]))))
                    
                    x6_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[5],DADOS_STB[5]) - 0.1*abs(self.menor_valor(DADOS_STB[5],DADOS_STB[5])), self.maior_valor(DADOS_STB[5],DADOS_STB[5]) + 0.1*abs(self.maior_valor(DADOS_STB[5],DADOS_STB[5]))))
                    
                    x7_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[6],DADOS_STB[6]) - 0.1*abs(self.menor_valor(DADOS_STB[6],DADOS_STB[6])), self.maior_valor(DADOS_STB[6],DADOS_STB[6]) + 0.1*abs(self.maior_valor(DADOS_STB[6],DADOS_STB[6]))))
                    
                    x8_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[7],DADOS_STB[7]) - 0.1*abs(self.menor_valor(DADOS_STB[7],DADOS_STB[7])), self.maior_valor(DADOS_STB[7],DADOS_STB[7]) + 0.1*abs(self.maior_valor(DADOS_STB[7],DADOS_STB[7]))))
                    
                    x9_plt.axis((min(DADOS_STA[9]), max(DADOS_STA[9]), self.menor_valor(DADOS_STB[8],DADOS_STB[8]) - 0.1*abs(self.menor_valor(DADOS_STB[8],DADOS_STB[8])), self.maior_valor(DADOS_STB[8],DADOS_STB[8]) + 0.1*abs(self.maior_valor(DADOS_STB[8],DADOS_STB[8]))))
                    
                    
                    x1_plt.plot(DADOS_STB[9], DADOS_STB[0], color='black', linewidth=1)
                    x1_plt.set_title("STB")#('BTOTAL - BX - BY - BZ', fontsize=7, x=1, y=0)
                    x1_plt.set_ylabel(titulo[0])
                    start, end = x1_plt.get_xlim()
                    x1_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x1_plt.set_xticklabels('')
                    
                    x2_plt.plot(DADOS_STB[9], DADOS_STB[1], color='black', linewidth=1)
                    x2_plt.set_ylabel(titulo[1])
                    start, end = x2_plt.get_xlim()
                    x2_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x2_plt.set_xticklabels('')
                
                    x3_plt.plot(DADOS_STB[9], DADOS_STB[2], color='black', linewidth=1)
                    x3_plt.set_ylabel(titulo[2])
                    start, end = x3_plt.get_xlim()
                    x3_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x3_plt.set_xticklabels('')
                                        
                    x4_plt.plot(DADOS_STB[9], beta_stb, color='black', linewidth=1)
                    x4_plt.set_ylabel(titulo[3])
                    start, end = x4_plt.get_xlim()
                    x4_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x4_plt.set_xticklabels('')
                    x4_plt.plot([min(DADOS_STB[9]),max(DADOS_STB[9])], [0,0])
                    
                    x5_plt.plot(DADOS_STB[9], DADOS_STB[4], color='black', linewidth=1)
                    x5_plt.set_ylabel(titulo[4])
                    start, end = x5_plt.get_xlim()
                    x5_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x5_plt.set_xticklabels('')   
                    
                    x6_plt.plot(DADOS_STB[9], DADOS_STB[5], color='black', linewidth=1)
                    x6_plt.set_ylabel(titulo[5])
                    x6_plt.set_xlabel('')
                    start, end = x6_plt.get_xlim()
                    x6_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x6_plt.set_xticklabels('')
                    
                    x7_plt.plot(DADOS_STB[9], DADOS_STB[6], color='black', linewidth=1)
                    x7_plt.set_ylabel(titulo[6])
                    x7_plt.set_xlabel('')
                    start, end = x7_plt.get_xlim()
                    x7_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x7_plt.set_xticklabels('')   
                    x7_plt.plot([min(DADOS_STA[9]),max(DADOS_STA[9])], [0,0])
                    
                    x8_plt.plot(DADOS_STB[9], DADOS_STB[7], color='black', linewidth=1)
                    x8_plt.set_ylabel(titulo[7])
                    x8_plt.set_xlabel('')
                    start, end = x8_plt.get_xlim()
                    x8_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x8_plt.set_xticklabels('')   
                    x8_plt.plot([min(DADOS_STA[9]),max(DADOS_STA[9])], [0,0])
                    
                    x9_plt.plot(DADOS_STB[9], DADOS_STB[8], color='black', linewidth=1)
                    x9_plt.set_ylabel(titulo[8])
                    x9_plt.set_xlabel('Dia')
                    start, end = x9_plt.get_xlim()
                    x9_plt.xaxis.set_ticks(np.arange(start, end+0.25, 0.25))
                    x9_plt.set_xticklabels(texto_data)
                    x9_plt.plot([min(DADOS_STA[9]),max(DADOS_STA[9])], [0,0])
                    
                    ###plotando o corte no gráfico STB
                    for z in range(0, len(shock_stb)):
                        x1_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[0],DADOS_STB[0]) - 0.1*abs(self.menor_valor(DADOS_STA[0],DADOS_STB[0])), self.maior_valor(DADOS_STA[0],DADOS_STB[0]) + 0.1*abs(self.maior_valor(DADOS_STA[0],DADOS_STB[0]))], 'b--', color='red', linewidth=1)
                        x2_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[1],DADOS_STB[1]) - 0.1*abs(self.menor_valor(DADOS_STA[1],DADOS_STB[1])), self.maior_valor(DADOS_STA[1],DADOS_STB[1]) + 0.1*abs(self.maior_valor(DADOS_STA[1],DADOS_STB[1]))], 'b--', color='red', linewidth=1)
                        x3_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[2],DADOS_STB[2]) - 0.1*abs(self.menor_valor(DADOS_STA[2],DADOS_STB[2])), self.maior_valor(DADOS_STA[2],DADOS_STB[2]) + 0.1*abs(self.maior_valor(DADOS_STA[2],DADOS_STB[2]))], 'b--', color='red', linewidth=1)
                        x4_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(beta_stb,beta_stb) - 0.1*abs(self.menor_valor(beta_stb,beta_stb)), self.maior_valor(beta_stb,beta_stb) + 0.1*abs(self.maior_valor(beta_stb,beta_stb))], 'b--', color='red', linewidth=1)
                        x5_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[4],DADOS_STB[4]) - 0.1*abs(self.menor_valor(DADOS_STA[4],DADOS_STB[4])), self.maior_valor(DADOS_STA[4],DADOS_STB[4]) + 0.1*abs(self.maior_valor(DADOS_STA[4],DADOS_STB[4]))], 'b--', color='red', linewidth=1)
                        x6_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[5],DADOS_STB[5]) - 0.1*abs(self.menor_valor(DADOS_STA[5],DADOS_STB[5])), self.maior_valor(DADOS_STA[5],DADOS_STB[5]) + 0.1*abs(self.maior_valor(DADOS_STA[5],DADOS_STB[5]))], 'b--', color='red', linewidth=1)
                        x7_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[6],DADOS_STB[6]) - 0.1*abs(self.menor_valor(DADOS_STA[6],DADOS_STB[6])), self.maior_valor(DADOS_STA[6],DADOS_STB[6]) + 0.1*abs(self.maior_valor(DADOS_STA[6],DADOS_STB[6]))], 'b--', color='red', linewidth=1)
                        x8_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[7],DADOS_STB[7]) - 0.1*abs(self.menor_valor(DADOS_STA[7],DADOS_STB[7])), self.maior_valor(DADOS_STA[7],DADOS_STB[7]) + 0.1*abs(self.maior_valor(DADOS_STA[7],DADOS_STB[7]))], 'b--', color='red', linewidth=1)
                        x9_plt.plot([shock_stb[z],shock_stb[z]], [self.menor_valor(DADOS_STA[8],DADOS_STB[8]) - 0.1*abs(self.menor_valor(DADOS_STA[8],DADOS_STB[8])), self.maior_valor(DADOS_STA[8],DADOS_STB[8]) + 0.1*abs(self.maior_valor(DADOS_STA[8],DADOS_STB[8]))], 'b--', color='red', linewidth=1)
                    
                    
                    fig.savefig(caminho+'/{}.png'.format(name), bbox_inches='tight')
                        
                    try:
                        figManager = plt.get_current_fig_manager()
                        figManager.window.showMaximized()
                    except:
                        pass
                        
                    plt.show()
                    fig.clf()
                    plt.clf()
                    plt.close()
                
            if (not os.path.exists(caminho+'/{}.png'.format('STA')) or not os.path.exists(caminho+'/{}.png'.format('STA')))  and Rplot=='N':
                print('OK. Entao nao ha como exibir nada.')   
                
    def shocks(self, data, vet_sta):
        STA_shock = []        
        for i in range(0, len(vet_sta)):
            if vet_sta[i][0] >= datetime.fromordinal(data.toordinal()-2) and vet_sta[i][0] <= datetime.fromordinal(data.toordinal()+2):
                STA_shock.append(vet_sta[i][1])
        return STA_shock
    
    def shocks_stb(self, data, vet_stb):
        STB_shock = []        
        for i in range(0, len(vet_stb)):
            if vet_stb[i][0] == data:
                STB_shock.append(vet_stb[i][1])
        return STB_shock
    
    def plotEventList(self, year, month):
        texto = self.arqxlsx(year, month)
        
        shock_STA = []
        shock_STB = []
        #AUX_shock = []
        #encontrando dias repetidos
        datas_repetidas = []
        for j in range(0, len(texto)):
            ano_atual = str(int(texto[j][1]))
            mes_atual = str(int(texto[j][2]))
            dia_atual = str(int(texto[j][3]))
            datas_repetidas.append(ano_atual+' '+mes_atual+' '+dia_atual)
            
            #encontrando o momento dos shocks
            ### para descobrir o ultimo dia do mes da data inicial
            data_em_texto = '{}/{}/{}'.format(dia_atual, mes_atual, ano_atual)
            data_atual = datetime.strptime(data_em_texto, '%d/%m/%Y')
        
            aux_D = datetime.fromordinal(data_atual.toordinal()-2)
            
            dia = '01'
            data_em_texto = '{}/{}/{}'.format(dia, aux_D.month, aux_D.year)
            
            aux_D = datetime.strptime(data_em_texto, '%d/%m/%Y') # primeiro dia do primeiro mes
            
            aux_D = datetime.fromordinal(aux_D.toordinal()+32) #avança para o mes seguinde
            data_em_texto = '{}/{}/{}'.format(dia, aux_D.month, aux_D.year) #primeiro dia do mes seguinde
            
            aux_D = datetime.strptime(data_em_texto, '%d/%m/%Y') # day1 recebe a data do primeiro dia do mes seguinde
            
            aux_D = datetime.fromordinal(aux_D.toordinal()-1) #retrocede para o ultimo dia do mes anterior
            
            ### auxiliares
            S_month = str(int(aux_D.strftime('%m'))) ### mes inicial
            E_day = aux_D.day ### ultimo dia do mes inicial
            
            # calculando o tempo corrido
            hora_atual = texto[j][4]
            minuto_atual = texto[j][5]
            
            #se o mes atual é igual ao inicial
            if S_month == mes_atual:         # tempo vai receber o tempo corrido do referente dia
                tempo = float(dia_atual) + (float(hora_atual)*60 + float(minuto_atual))/1440
            else: #se não tempo vai receber o valor do dia final mais a soma do dia corrido atual, ps:na mudança de mes o dia corrido atual vai reiniciar no 1
                tempo = float(E_day) + float(dia_atual) + (float(hora_atual)*60 + float(minuto_atual))/1440
            
            AUX_shock = [data_atual, tempo]
            #print(AUX_shock)
            #print('\n\n')
            
            '''
            #AUX_shock.append(data_atual.strftime('%d/%m/%Y'), tempo)
            #AUX_shock.append(data_atual.strftime('%d/%m/%Y'))
            #AUX_shock.append(tempo)
            
            #print(AUX_shock)
            '''
            
            if texto[j][0] == 'STEREO A':
                shock_STA.append(AUX_shock)
            
            if texto[j][0] == 'STEREO B':
                shock_STB.append(AUX_shock)
                
            #del AUX_shock[0]  
            #del AUX_shock[0]
            #del AUX_shock[0]
            #AUX_shock.clear()
        
         #deletando o dias repetidos do vetor
        #print(shock_STB)
        data = []
        for i in datas_repetidas:
            if i not in data:
                data.append(i)
        data.sort()
        
        #print(data)
                
        i = int(0) #variavel int que vai receber o número da linha atual
        for i in range(0, len(data)): #vai repetir enquando houver linhas no texto de datas não repetidas              
            splitado = str(data[i]).split()
            
            year = splitado[0]
            month = splitado[1]
            day = splitado[2]
            
            data_em_texto = '{}/{}/{}'.format(day, month, year)
            Day1 = datetime.strptime(data_em_texto, '%d/%m/%Y')
        
            S_Day = datetime.fromordinal(Day1.toordinal()-2)
            E_Day = datetime.fromordinal(Day1.toordinal()+2)
                
            S_year = S_Day.strftime('%Y')
        
            S_month = S_Day.strftime('%m')
            S_day = S_Day.strftime('%d')
            
            E_year = E_Day.strftime('%Y')
            E_month = E_Day.strftime('%m')
            E_day = E_Day.strftime('%d')
            
            '''
            print('shock separados')
            print(shock_STA)
            print('\n\n')
            print(shock_STB) 
            print('\n\n')
            '''
            
            shock_sta = self.shocks(Day1, shock_STA)
            shock_stb = self.shocks(Day1, shock_STB)
            
            '''
            print('shocks do dia: ' +Day1.strftime('%d/%m/%Y'))
            print('STA ---> {}'.format(shock_sta))
            print('\n\n')
            print('STB ---> {}'.format(shock_stb))
            print('\n\n')
            '''
            
            #print(shock_sta)
            #print('\n\n')
            #print(shock_stb)
            
            self.plot_and_subplot(S_year, S_month, S_day, E_year, E_month, E_day, shock_sta, shock_stb)
        
    def plotEventList_somente1(self, year, month):
        texto = self.arqxlsx(year, month)
        
        shock_STA = []
        shock_STB = []
        #AUX_shock = []
        #encontrando dias repetidos
        datas_repetidas = []
        for j in range(0, len(texto)):
            ano_atual = str(int(texto[j][1]))
            mes_atual = str(int(texto[j][2]))
            dia_atual = str(int(texto[j][3]))
            datas_repetidas.append(ano_atual+' '+mes_atual+' '+dia_atual)
            
            #encontrando o momento dos shocks
            ### para descobrir o ultimo dia do mes da data inicial
            data_em_texto = '{}/{}/{}'.format(dia_atual, mes_atual, ano_atual)
            data_atual = datetime.strptime(data_em_texto, '%d/%m/%Y')
        
            aux_D = datetime.fromordinal(data_atual.toordinal()-2)
            
            dia = '01'
            data_em_texto = '{}/{}/{}'.format(dia, aux_D.month, aux_D.year)
            
            aux_D = datetime.strptime(data_em_texto, '%d/%m/%Y') # primeiro dia do primeiro mes
            
            aux_D = datetime.fromordinal(aux_D.toordinal()+32) #avança para o mes seguinde
            data_em_texto = '{}/{}/{}'.format(dia, aux_D.month, aux_D.year) #primeiro dia do mes seguinde
            
            aux_D = datetime.strptime(data_em_texto, '%d/%m/%Y') # day1 recebe a data do primeiro dia do mes seguinde
            
            aux_D = datetime.fromordinal(aux_D.toordinal()-1) #retrocede para o ultimo dia do mes anterior
            
            ### auxiliares
            S_month = str(int(aux_D.strftime('%m'))) ### mes inicial
            E_day = aux_D.day ### ultimo dia do mes inicial
            
            # calculando o tempo corrido
            hora_atual = texto[j][4]
            minuto_atual = texto[j][5]
            
            #se o mes atual é igual ao inicial
            if S_month == mes_atual:         # tempo vai receber o tempo corrido do referente dia
                tempo = float(dia_atual) + (float(hora_atual)*60 + float(minuto_atual))/1440
            else: #se não tempo vai receber o valor do dia final mais a soma do dia corrido atual, ps:na mudança de mes o dia corrido atual vai reiniciar no 1
                tempo = float(E_day) + float(dia_atual) + (float(hora_atual)*60 + float(minuto_atual))/1440
            
            AUX_shock = [data_atual, tempo]
            #print(AUX_shock)
            #print('\n\n')
            
            '''
            #AUX_shock.append(data_atual.strftime('%d/%m/%Y'), tempo)
            #AUX_shock.append(data_atual.strftime('%d/%m/%Y'))
            #AUX_shock.append(tempo)
            
            #print(AUX_shock)
            '''
            
            if texto[j][0] == 'STEREO A':
                shock_STA.append(AUX_shock)
            
            if texto[j][0] == 'STEREO B':
                shock_STB.append(AUX_shock)
                
            #del AUX_shock[0]  
            #del AUX_shock[0]
            #del AUX_shock[0]
            #AUX_shock.clear()
        
         #deletando o dias repetidos do vetor
        #print(shock_STB)
        data = []
        for i in datas_repetidas:
            if i not in data:
                data.append(i)
        data.sort()
        
        #print(data)
                
        i = int(0) #variavel int que vai receber o número da linha atual
        for i in range(0, len(data)): #vai repetir enquando houver linhas no texto de datas não repetidas              
            splitado = str(data[i]).split()
            
            year = splitado[0]
            month = splitado[1]
            day = splitado[2]
            
            data_em_texto = '{}/{}/{}'.format(day, month, year)
            Day1 = datetime.strptime(data_em_texto, '%d/%m/%Y')
        
            S_Day = datetime.fromordinal(Day1.toordinal()-2)
            E_Day = datetime.fromordinal(Day1.toordinal()+2)
                
            S_year = S_Day.strftime('%Y')
        
            S_month = S_Day.strftime('%m')
            S_day = S_Day.strftime('%d')
            
            E_year = E_Day.strftime('%Y')
            E_month = E_Day.strftime('%m')
            E_day = E_Day.strftime('%d')
            
            '''
            print('shock separados')
            print(shock_STA)
            print('\n\n')
            print(shock_STB) 
            print('\n\n')
            '''
            
            shock_sta = self.shocks(Day1, shock_STA)
            shock_stb = self.shocks(Day1, shock_STB)
            
            '''
            print('shocks do dia: ' +Day1.strftime('%d/%m/%Y'))
            print('STA ---> {}'.format(shock_sta))
            print('\n\n')
            print('STB ---> {}'.format(shock_stb))
            print('\n\n')
            '''
            
            #print(shock_sta)
            #print('\n\n')
            #print(shock_stb)
            
            self.plot_and_subplot_somente1(S_year, S_month, S_day, E_year, E_month, E_day, shock_sta, shock_stb)
        
    
    
    def xlread(self):
        #abre arquivo
        xls = xlrd.open_workbook("STEREO_Level3_Shock.xlsx")
        #pega a primeira linha
        plan = xls.sheets()[0]
        
        #para i de zero ao numero de linhasda planilha
        for i in range(plan.nrows):
            #le os valores nas linhas da planilha
            yield plan.row_values(i)
    
    def arqxlsx(self, year, month):
        vet = []

        recebeSTA = True
        for linha in self.xlread():
            if str(linha[0]) == "Interplanetary  Shocks  at  STEREO B":
                recebeSTA = False;
                
            if linha[1] == float(year) and linha[2] == float(month) and str(linha[12]).count("ICME") == 1 and recebeSTA == True:
                linha[0] = "STEREO A"
                vet.append(linha)
                #print(linha)
                #print("")
                
            if linha[1] == float(year) and linha[2] == float(month) and str(linha[12]).count("ICME") == 1 and recebeSTA == False:
                linha[0] = "STEREO B"
                vet.append(linha)
                #print(linha)
                #print("")
        
        
        return vet
    
    def sta_stb_qtdEvent(self):
        vet = []

        recebeSTA = True
        for linha in self.xlread():
                
            if str(linha[0]) == "Interplanetary  Shocks  at  STEREO B":
                recebeSTA = False;

            if str(linha[12]).count("ICME") == 1 and recebeSTA == True and linha[1] < int(2015):
                linha[0] = "STEREO A"
                vet.append(linha)
                #print(linha)
                #print("")
                    
            if str(linha[12]).count("ICME") == 1 and recebeSTA == False and linha[1] < int(2015):
                linha[0] = "STEREO B"
                vet.append(linha)
                #print(linha)
                #print("")
                
        return vet
    
    def baixarEventList(self, year, month):
        baixar='S'
        
        aux = str(self.getDirectory()).split("\ ".strip())
        caminho = str(aux[0])
        #print(len(aux))
        
        if len(aux) == 1:
            self.createFolder(caminho)
        else:
            for i in range(0, len(aux)):
                if i==0:
                    self.createFolder(caminho)
                else:
                    caminho = caminho+"\ ".strip() + aux[i]
                    self.createFolder(caminho)
        
        # verifica se o arquivo existe, se sim pergunta se quer substituí-los
        if os.path.exists(self.getDirectory()+'STEREO_Level3_Shock.xlsx'):
            print('O arquivo nao existe!')
            print('Digite: S para sim ou N para nao')
            baixar = input('Deseja substituir o arquivo?').upper()
            
        # se baixar é igual a sim, independente se eles já existem ou não
        if baixar=='S' or baixar=='SIM':           
            try:
                webpage = urlopen("http://www-ssc.igpp.ucla.edu/forms/stereo/stereo_level_3.html")
            except:
                print("Site não encontrado.")
            else:
                print('http://www-ssc.igpp.ucla.edu/forms/stereo/stereo_level_3.html')
                    
            webpageHtml = str(webpage.readlines())
                
            start = webpageHtml.find("http://www-ssc.igpp.ucla.edu/~jlan/STEREO/Level3/STEREO_Level3_Shock.xls")
            end = webpageHtml.find('">Shock list in excel format')
                
            print(webpageHtml[start:end])
            datalink = str(webpageHtml)[start:end]
            #datalink = Linha[start:end+1]
            try:
                urlretrieve(datalink)
            except FileNotFoundError:
                print('Algo de errado nao está certo.')
            else:
                urlretrieve(datalink, "STEREO_Level3_Shock.xlsx")

                texto = self.arqxlsx(year, month)                               
                #encontrando dias repetidos
                datas_repetidas = []
                for j in range(0, len(texto)):
                    ano_atual = str(int(texto[j][1]))
                    mes_atual = str(int(texto[j][2]))
                    dia_atual = str(int(texto[j][3]))
                    datas_repetidas.append(ano_atual+' '+mes_atual+' '+dia_atual)
                 
                #deletando o dias repetidos do vetor
                data = []
                for i in datas_repetidas:
                    if i not in data:
                        data.append(i)
                data.sort()
                
                i = int(0) #variavel int que vai receber o número da linha atual
                for i in range(0, len(data)): #vai repetir enquando houver linhas no texto                
                    splitado = str(data[i]).split()
                    
                    year = splitado[0]
                    month = splitado[1]
                    day = splitado[2]
                    
                    data_em_texto = '{}/{}/{}'.format(day, month, year)
                    Day1 = datetime.strptime(data_em_texto, '%d/%m/%Y')
                
                    S_Day = datetime.fromordinal(Day1.toordinal()-2)
                    E_Day = datetime.fromordinal(Day1.toordinal()+2)
                        
                    S_year = S_Day.strftime('%Y')
                
                    S_month = S_Day.strftime('%m')
                    S_day = S_Day.strftime('%d')
                    
                    E_year = E_Day.strftime('%Y')
                    E_month = E_Day.strftime('%m')
                    E_day = E_Day.strftime('%d')
                        
                        
                    self.asciiDataDownload_2(S_year, S_month, S_day, E_year, E_month, E_day)

    def criaHistograma(self):       
                
        datalink = "https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-indices/sunspot-numbers/american/tables/table_aavso-arssn_monthly.txt"
            #datalink = Linha[start:end+1]
        try:
            urlretrieve(datalink)
        except FileNotFoundError:
            print('Algo de errado nao está certo.')
        else:
            urlretrieve(datalink, "table_aavso-arssn_monthly.txt")
            
        
        plt_eixo_x = []
        plt_eixo_y = []
        try:
            arq = open("table_aavso-arssn_monthly.txt");
        except FileNotFoundError:
            print('Algo de errado nao esta certo.')
        else:        
            texto = arq.readlines(); #texto recebe todas as linhas com valores
            
            del texto[3]
            del texto[2]
            del texto[1]
            del texto[0]
            
            i = int(0) #variavel int que vai receber o número da linha atual
            for i in range(0, len(texto)): #vai repetir enquando houver linhas no texto        
                    
                if len(str(texto[i]).split()) > 0 and str(texto[i][0]) != "-" and int(str(texto[i]).split()[0]) >= 2007 and int(str(texto[i]).split()[0]) <= 2014:
                    Linha = str(texto[i]).split() #linha é a linha atual do texto 
                    for i in range(1, len(Linha)):
                        plt_eixo_y.append(float(Linha[i]))
                    
                    for i in range(1, 13):
                        plt_eixo_x.append(float(Linha[0]) + i*1/13)
            
            
            #print(plt_eixo_y)
            #print('\n\n')
            #print(plt_eixo_x)
        '''
        dia = "01"
        month = "01"
        year = "2007"
        data_em_texto = '{}/{}/{}'.format(dia, month, year)
        data_inic = datetime.strptime(data_em_texto, '%d/%m/%Y')
        
        dia = "01"
        month = "01"
        year = "2015"
        data_em_texto = '{}/{}/{}'.format(dia, month, year)
        data_fim = datetime.strptime(data_em_texto, '%d/%m/%Y')
        data_fim = datetime.fromordinal(data_fim.toordinal()-1)
        '''
        caminho = self.getDirectory()
        texto = self.sta_stb_qtdEvent()
        sta = []
        stb = []
        
        
        i = int(0)
        for i in range(0,len(texto)):
            if texto[i][0] == "STEREO A":
                sta.append(texto[i][1])
            if texto[i][0] == "STEREO B":
                stb.append(texto[i][1])       
        
        texto_xticks = []
        for i in range(2007, 2016):
            texto_xticks.append(i)
            texto_xticks.append("")        
        
        
        fig = plt_stereo.figure()
        plt.subplots_adjust(left=0.125, bottom=0.1, right=1.15, top=2.4,
                                        wspace=0.33, hspace=0.2)
        
        plt_hist = fig.add_subplot(1, 1, 1)
        plt_plote = fig.add_subplot(1, 1, 1)
        
        plt.axis((2007, 2015, 0, 100))
        #plt.grid()
        
        
        plt_hist.hist([sta, stb], color=['orange', 'green'], stacked=True, rwidth=1.0, bins=range(2007, 2016,1))
        plt.xlabel("Year")
        plt_hist.set_ylabel("Number of shocks")
        plt_hist.legend(["STA", "STB"])
        start, end = plt_hist.get_ylim()
        plt_hist.yaxis.set_ticks(np.arange(start, end+1, 5))
        plt_hist.grid(axis='y', linestyle='-')
        
        plt_plote.set_ylabel("Sunspot number")
        plt_plote.plot(plt_eixo_x, plt_eixo_y, color='black', linewidth=1)
        plt_plote.legend("MONTHLY MEAN")
        start, end = plt_plote.get_xlim()
        plt_plote.xaxis.set_ticks(np.arange(start, end+0.5, 0.5))
        #plt_plote.set_xticklabels(texto_xticks, rotation = (45), fontsize = 10, va='bottom', ha='left')
        
        plt_plote.set_xticklabels(texto_xticks)
        plt_plote.xaxis.set_tick_params(rotation=45)
        #plt_plote.set_yticklabels('')
        
        
        fig.savefig(caminho+'/histograma.png', bbox_inches='tight')
            
        try:
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
        except:
            pass
                    
                    
        plt.show()