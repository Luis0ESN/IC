from datetime import datetime
from urllib.request import urlopen
import numpy

class stereo(object):
    ###   começo da iniciação  ###
    def __init__(self, spacecraft, date_start, date_end):
        
        if spacecraft!='STA' and spacecraft!='STB':
            print('spacecraft invalido!')
        
        self.date_start = datetime.strptime(date_start, '%Y/%m/%d')
        
        self.date_end = datetime.strptime(date_end, '%Y/%m/%d')
        
        self.spacecraft = spacecraft
        
        Sday = datetime.strftime(self.date_start, '%d')
        Smonth = datetime.strftime(self.date_start, '%m')
        Syear = datetime.strftime(self.date_start, '%Y')
        
        Eday = datetime.strftime(self.date_end, '%d')
        Emonth = datetime.strftime(self.date_end, '%m')
        Eyear = datetime.strftime(self.date_end, '%Y')
        
        if spacecraft == 'STB':
            self.link = 'https://cdaweb.gsfc.nasa.gov/cgi-bin/eval3.cgi?dataset=+STB_L2_MAGPLASMA_1M&start={}%2F{}%2F{}+00%3A00%3A00.000&stop={}%2F{}%2F{}+23%3A59%3A00.000&bin_value=15&time_unit=min&missval=fillval&spike_opt=none&index=sp_phys&nobin_spike_opt=light&spinner=1&autoChecking=on&action=list&var=STB_L2_MAGPLASMA_1M+BFIELDRTN&var=STB_L2_MAGPLASMA_1M+BTOTAL&var=STB_L2_MAGPLASMA_1M+Np&var=STB_L2_MAGPLASMA_1M+Vp&var=STB_L2_MAGPLASMA_1M+Tp&var=STB_L2_MAGPLASMA_1M+Vp_RTN&var=STB_L2_MAGPLASMA_1M+Beta&var=STB_L2_MAGPLASMA_1M+Total_Pressure&png=1'.format(Syear,Smonth,Sday,Eyear,Emonth,Eday)
        
        elif spacecraft == 'STA':
            self.link = 'https://cdaweb.gsfc.nasa.gov/cgi-bin/eval3.cgi?dataset=+STA_L2_MAGPLASMA_1M&start={}%2F{}%2F{}+00%3A00%3A00.000&stop={}%2F{}%2F{}+23%3A59%3A00.000&bin_value=15&time_unit=min&missval=fillval&spike_opt=none&index=sp_phys&nobin_spike_opt=light&spinner=1&autoChecking=on&action=list&var=STA_L2_MAGPLASMA_1M+BFIELDRTN&var=STA_L2_MAGPLASMA_1M+BTOTAL&var=STA_L2_MAGPLASMA_1M+Np&var=STA_L2_MAGPLASMA_1M+Vp&var=STA_L2_MAGPLASMA_1M+Tp&var=STA_L2_MAGPLASMA_1M+Vp_RTN&var=STA_L2_MAGPLASMA_1M+Beta&var=STA_L2_MAGPLASMA_1M+Total_Pressure&png=1'.format(Syear,Smonth,Sday,Eyear,Emonth,Eday)
        
        ###parametros
        self.btotal = list()
        self.np = list()
        self.speed = list()
        self.temperature = list()
        self.beta = list()
        self.total_pressure = list()
        self.bx = list()
        self.by = list()
        self.bz = list()
        self.time = list() #todos os valores de tempo no periodo lido no arquivo
        #fim parametros
        
        if spacecraft=='STA' or spacecraft=='STB':        
            try: #acessa a página que fica arquivo com os dados
                webpage = urlopen(self.link)
            except:
                print("Site não encontrado.")
            else:
                print('input url: '+self.link)
                
                webpageHtml = webpage.readlines()
                print("Reading webpage's html...\n")
                
                linkEnd = str(webpageHtml).find('">{}_L2_MAGPLASMA_1M_'.format(self.spacecraft))
                linkStart = str(webpageHtml).find('href="/tmp/')+6
                
                dataLink = 'https://cdaweb.gsfc.nasa.gov/'+ str(webpageHtml)[linkStart:linkEnd]
                #recebe o link do arquivo com os dados
            webpage.close()
            
            try: #abre o link que contém o arquivo
                arquivo = urlopen(dataLink)
            except:
                print('Algo de errado nao está certo.')
            else:        
                ##inicia leitura
                aux = list()
    
                texto = arquivo.readlines(); #texto recebe todas as linhas com valores
                
                i = int(0) #variavel int que vai receber o número da linha atual
                for i in range(0, len(texto)): #vai repetir enquando houver linhas no texto        
                    Linha = texto[i] #linha é a linha atual do texto    
                    Linha = Linha.decode('utf-8')
                    if Linha[0] != '#': #removendo linhas indesejadas do arquivo
                        Linha = Linha.strip()
                        aux.append(Linha)
                    
                del aux[2]
                del aux[1]
                del aux[0]
                
                for i in range(0,len(aux)):
                    linha = aux[i];
                    linha = linha.replace('-1.00000E+30', '  nan  ')
                    #print(linha)
                    data_texto = linha.split()[0]+ ' ' + linha.split()[1]
                    
                    self.btotal.append(float(linha.split()[2]));
                    self.np.append(float(linha.split()[3]));
                    self.beta.append(float(linha.split()[7]));
                    self.total_pressure.append(float(linha.split()[8]));
                    self.speed.append(float(linha.split()[4]));
                    self.temperature.append(float(linha.split()[5]));
                    self.bx.append(float(linha.split()[9]));
                    self.by.append(float(linha.split()[10]));
                    self.bz.append(float(linha.split()[11]));
                    self.time.append(datetime.strptime(data_texto, '%d-%m-%Y %H:%M:%S.%f'))
                
                arquivo.close()
            ##finaliza leitura
        else:
            print('Spacecraft inválido')
    ###   fim da iniciação   ###
    
    def get_data(self, data):#data values == 'btotal' or 'np' or 'beta' or 'total_pressure' or 'speed' or 'temperature' or 'bx' or 'by' or bz' or 'time'
        if data=='btotal':
            return numpy.array(self.btotal)
        
        elif data=='np':
            return numpy.array(self.np)
        
        elif data=='beta':
            return numpy.array(self.beta)
        
        elif data=='total_pressure':
            return numpy.array(self.total_pressure)
        
        elif data=='speed':
            return numpy.array(self.speed)
        
        elif data=='temperature':
            return numpy.array(self.temperature)
        
        elif data=='bx':
            return numpy.array(self.bx)
        
        elif data=='by':
            return numpy.array(self.by)
        
        elif data=='bz':
            return numpy.array(self.bz)
        
        elif data=='time':
            return numpy.array(self.time)
        
        else:
            print('data not found')
    
    ###   início do método reiniciar o objeto com um novo período   ###
    def new_date(self, start_date, end_date):
        self.__new__(stereo)
        self.__init__(self.spacecraft, start_date, end_date)
    ###   fim do método reiniciar o objeto com um novo período   ###