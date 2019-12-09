# -*- coding: utf-8 -*-

import Plots;

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
    print('1 - Plotar gráficos e fazer o video para um evento')
    print('2 - Plotar gráficos e fazer os videos para os eventos da lista.')
    
    OP = int(input('Digite a opcao que voce deseja: ')); #Usúario escolhe uma opção
    
    if OP<0 or OP>2: #verificando se a opção escolhida é válida
        print('\n\n {}Opcao invalida!{}'.format(importante['inicio'], importante['fim']))#, end='');
    
    elif OP==1: #se igual a 2 o programa irá plotar os gráficos separados
        year = input('Digite o ano: ')
        month = input('Digite o mes: ')        
        day = input('Digite o dia: ')
        
        Plots.plot_and_subplot(year, month, day)
        Plots.ImagesZipDownload(year, month, day)
        Plots.makeVideo(year, month, day)

    elif OP==2:
        Plots.plotEventList()
    
    elif OP==3:            
        Plots.criaHistograma()
