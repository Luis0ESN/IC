# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:59:09 2019

@author: Carlos Nascimento
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:59:15 2019

@author: Carlos Nascimento
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:25:57 2019

@author: Carlos Nascimento
"""
#import Main_Methods
from Files import files;

arquivo1 = files()

############################################
                    #main()
############################################    
OP = int(-1); #opcao começa com para 2 para o while funcionar desde o inicio

# variavel que vai receber o texto que muda as cores
importante = {'inicio':'\033[4;31m',
            'fim': '\033[m'}

    # laço de repetição para que enquando o usúario não quiser fechar o programa ele continue aberto
while OP!=0:
    print('\n\nEscolha uma opcao!\n0 - SAIR!')
    print('1 - Plotar gráfico,  STA e STB separados.')
    print('2 - Plotar gráfico,  STA e STB juntos.')
    print('3 - Fazer download de dados.')
    print('4 - Fazer download da lista de eventos de um mes e seus respectivos dados.')
    print('5 - Plotar gráfico, STA e STB juntos, da lista de eventos,')
    print('6 - Plotar gráfico, STA e STB separados, da lista de eventos.')
    print('7 - Plotar histograma de frequência de shocks em um mes.')
    
    OP = int(input('Digite a opcao que voce deseja: ')); #Usúario escolhe uma opção
    
    if OP<0 or OP>7: #se diferente de 1 a opção é inválida e ele deve reescrever a opção
        print('\n\n {}Opcao invalida!{}'.format(importante['inicio'], importante['fim']))#, end='');
    
    
    if OP==1: #se igual a 2 o programa irá plotar os gráficos separados
        S_year = input('Digite o ano inicial: ')
        S_month = input('Digite o mes inicial: ')        
        S_day = input('Digite o dia inicial: ')
        E_year = input('Digite o ano final: ')
        E_month = input('Digite o mes final: ')        
        E_day = input('Digite o dia final: ')
        
        arquivo1.setDirectory("Arquivos")
        arquivo1.plot_and_subplot_somente1(S_year, S_month, S_day, E_year, E_month, E_day, {}, {})    
    
    
    elif OP== 2: #se igual a 2 o programa irá plotar os gráficos juntos
        S_year = input('Digite o ano inicial: ')
        S_month = input('Digite o mes inicial: ')        
        S_day = input('Digite o dia inicial: ')
        E_year = input('Digite o ano final: ')
        E_month = input('Digite o mes final: ')        
        E_day = input('Digite o dia final: ')
        
        arquivo1.setDirectory("Arquivos")
        arquivo1.plot_and_subplot(S_year, S_month, S_day, E_year, E_month, E_day, {}, {})
        
    elif OP==3: #se igual a 3 ele fara o download de dados de uma data específica
        S_year = input('Digite o ano inicial: ')
        S_month = input('Digite o mes inicial: ')        
        S_day = input('Digite o dia inicial: ')
        E_year = input('Digite o ano final: ')
        E_month = input('Digite o mes final: ')        
        E_day = input('Digite o dia final: ')
        
        #event_day=ano+mes+S_dia
        
        arquivo1.setDirectory("Arquivos")
        arquivo1.asciiDataDownload_2(S_year, S_month, S_day, E_year, E_month, E_day)
    if OP==4:
        ano = input('Digite o ano: ')
        mes = input('Digite o mes: ')        
        
        pastaAno = str(ano)
        
        if mes=='01':
            pastaMes = "Janeiro"
        if mes=='02':
            pastaMes = "Fevereiro"
        if mes=='03':
            pastaMes = "Marco"
        if mes=='04':
            pastaMes = "Abril"
        if mes=='05':
            pastaMes = "Maio"
        if mes=='06':
            pastaMes = "Junho"
        if mes=='07':
            pastaMes = "Julho"
        if mes=='08':
            pastaMes = "Agosto"
        if mes=='09':
            pastaMes = "Setembro"
        if mes=='10':
            pastaMes = "Outubro"
        if mes=='11':
            pastaMes = "Novembro"
        if mes=='12':
            pastaMes = "Dezembro"    
        
        arquivo1.setDirectory("Arquivos\EventDates\ ".strip() +pastaAno + '\ '.strip() + pastaMes)
        arquivo1.baixarEventList(ano, mes)
    if OP==5:
        ano = input('Digite o ano: ')
        mes = input('Digite o mes: ')        
        
        pastaAno = str(ano)
        
        if mes=='01':
            pastaMes = "Janeiro"
        if mes=='02':
            pastaMes = "Fevereiro"
        if mes=='03':
            pastaMes = "Marco"
        if mes=='04':
            pastaMes = "Abril"
        if mes=='05':
            pastaMes = "Maio"
        if mes=='06':
            pastaMes = "Junho"
        if mes=='07':
            pastaMes = "Julho"
        if mes=='08':
            pastaMes = "Agosto"
        if mes=='09':
            pastaMes = "Setembro"
        if mes=='10':
            pastaMes = "Outubro"
        if mes=='11':
            pastaMes = "Novembro"
        if mes=='12':
            pastaMes = "Dezembro" 
            
        arquivo1.setDirectory("Arquivos\EventDates\ ".strip() +pastaAno + '\ '.strip() + pastaMes)
        arquivo1.plotEventList(ano, mes)
    if OP==6:
        ano = input('Digite o ano: ')
        mes = input('Digite o mes: ')        
        
        pastaAno = str(ano)
        
        if mes=='01':
            pastaMes = "Janeiro"
        if mes=='02':
            pastaMes = "Fevereiro"
        if mes=='03':
            pastaMes = "Marco"
        if mes=='04':
            pastaMes = "Abril"
        if mes=='05':
            pastaMes = "Maio"
        if mes=='06':
            pastaMes = "Junho"
        if mes=='07':
            pastaMes = "Julho"
        if mes=='08':
            pastaMes = "Agosto"
        if mes=='09':
            pastaMes = "Setembro"
        if mes=='10':
            pastaMes = "Outubro"
        if mes=='11':
            pastaMes = "Novembro"
        if mes=='12':
            pastaMes = "Dezembro" 
            
        arquivo1.setDirectory("Arquivos\EventDates\ ".strip() +pastaAno + '\ '.strip() + pastaMes)
        arquivo1.plotEventList_somente1(ano, mes)
    if OP==7:            
        arquivo1.setDirectory("Arquivos\EventDates")
        arquivo1.criaHistograma()