import os
import numpy
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt;
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def reg_linear(y_str, x_str):

        #para as piores regressões simples
        try:
            if not os.path.exists('regressoes_simples/ruins'):
                os.makedirs('regressoes_simples/ruins')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_simples/ruins')


        #para regressões simples medianas
        try:
            if not os.path.exists('regressoes_simples/medianas'):
                os.makedirs('regressoes_simples/medianas')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_simples/medianas')

        #para as melhores regressões simples
        try:
            if not os.path.exists('regressoes_simples/melhores'):
                os.makedirs('regressoes_simples/melhores')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_simples/melhores')
        

        #para as melhores regressões multiplas
        try:
            if not os.path.exists('regressoes_multiplas/melhores'):
                os.makedirs('regressoes_multiplas/melhores')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_multiplas/melhores')

        #para regressões multiplas medianas
        try:
            if not os.path.exists('regressoes_multiplas/medianas'):
                os.makedirs('regressoes_multiplas/medianas')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_multiplas/medianas')

        #para as piores regressões multiplas
        try:
            if not os.path.exists('regressoes_multiplas/ruins'):
                os.makedirs('regressoes_multiplas/ruins')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_multiplas/ruins')

        
        file = pd.read_excel('reduzido.xlsx')
        file.dropna(inplace=True)

        dataset = file.loc[(file.Type == 'FF')]
        
        B_up = dataset[['B_up']]
        Bx_up = dataset[['Bx_up']]
        By_up = dataset[['By_up']]
        Bz_up = dataset[['Bz_up']]
        B_down = dataset[['B_down']]
        Bx_down = dataset[['Bx_down']]
        By_down = dataset[['By_down']]
        Bz_down = dataset[['Bz_down']]
        V_up = dataset[['V_up']]
        V_down = dataset[['V_down']]
        Np_up = dataset[['Np_up']]
        Np_down = dataset[['Np_down']]
        Tp_up = dataset[['Tp_up (10^4)']]
        Tp_down = dataset[['Tp_down (10^4)']]
        Cs_up = dataset[['Cs_up']]
        Va_up = dataset[['Va_up']]
        Vms_up = dataset[['Vms_up']]
        Beta_up = dataset[['Beta_up']]
        Theta = dataset[['Theta']]
        Vsh = dataset[['Vsh']]
        M_A = dataset[['M_A']]
        Mms = dataset[['Mms']]


        dic_labels = {'B_up':'B_up (nT)', 'Bx_up':'Bx_up (nT)', 'By_up':'By_up (nT)', 'Bz_up':'Bz_up (nT)',
                'B_down':'B_down (nT)', 'Bx_down':'Bx_down (nT)', 'By_down':'By_down (nT)', 'Bz_down':'Bz_down (nT)',
                'V_up':'V_up (Km/s)', 'V_down':'V_down (Km/s)', 'Np_up':'Np_up $(1/m^3)$', 'Np_down':'Np_down $(1/cm^3)$',
                'Tp_up':'Tp_up $(K^o)*(10^6)$', 'Tp_down':'Tp_down $(K^o)*(10^4)$', 'Cs_up':'Cs_up (Km/s)',
                'Va_up':'Va_up (Km/s)', 'Vms_up':'Vms_up (Km/s)', 'Beta_up':'Beta_up', 'Theta':'Theta (\u03B8)',
                'Vsh':'Vsh (Km/s)', 'M_A':'M_A', 'Mms':'Mms'}


        dic_str = {'B_up':'B_up', 'Bx_up':'Bx_up', 'By_up':'By_up', 'Bz_up':'Bz_up',
                'B_down':'B_down', 'Bx_down':'Bx_down', 'By_down':'By_down', 'Bz_down':'Bz_down',
                'V_up':'V_up', 'V_down':'V_down', 'Np_up':'Np_up', 'Np_down':'Np_down',
                'Tp_up':'Tp_up', 'Tp_down':'Tp_down', 'Cs_up':'Cs_up',
                'Va_up':'Va_up', 'Vms_up':'Vms_up', 'Beta_up':'Beta_up', 'Theta':'Theta',
                'Vsh':'Vsh', 'M_A':'M_A', 'Mms':'Mms'}


        
        dic = {'B_up':B_up, 'Bx_up':Bx_up, 'By_up':By_up, 'Bz_up':Bz_up,
               'B_down':B_down, 'Bx_down':Bx_down, 'By_down':By_down,
               'Bz_down':Bz_down, 'V_up':V_up, 'V_down':V_down, 'Np_up':Np_up,
               'Np_down':Np_down, 'Tp_up':Tp_up, 'Tp_down':Tp_down, 'Cs_up':Cs_up,
               'Va_up':Va_up, 'Vms_up':Vms_up, 'Beta_up':Beta_up, 'Theta':Theta,
               'Vsh':Vsh, 'M_A':M_A, 'Mms':Mms}
        
        dic_aux = {}
        dic_aux.update(dic)
        del dic_aux[y_str]


        y = numpy.array(dic[y_str]) #recebendo o valor de Y


        ##recebendo o valor de X
        #para regressao simples
        if len(x_str.split(','))==1:
                regression_simple = True
                x = numpy.array(dic_aux[x_str]).reshape(-1,1)

        # para regressão multipla
        elif len(x_str.split(','))>1:
                x =list()
                regression_simple = False
                n_vetores = len(x_str.split(','))

                aux = list()
                aux_str = ''
                for item in x_str.split(','):
                        aux.append(numpy.array(dic_aux[item]))
                
                for j in range(0,len(aux[0])):
                        aux_str = ''
                        for i in range(0,len(aux)):
                                aux_str = aux_str + ' ' + str(aux[i][j][0])

                        x.append(aux_str.split())
                        
                
                x = numpy.array(x, dtype='float').reshape(-1,n_vetores)
        ##fim do recebimento do valor de X
        
        model = LinearRegression()
        model.fit(x, y)

        if numpy.sqrt(model.score(x,y))<0.5:
                caminho = 'ruins'
        if numpy.sqrt(model.score(x,y))>=0.5 and numpy.sqrt(model.score(x,y))<0.75:
                caminho = 'medianas'
        if numpy.sqrt(model.score(x,y))>=0.75:
                caminho = 'melhores'

        legenda = 'R = {:.3f}\nY = '.format(numpy.sqrt(model.score(x,y)))
        for i in range(0,len(model.coef_[0])):
                if i==0:
                        legenda = legenda + '{:.3f}*{} '.format(model.coef_[0][i], dic_str[x_str.split(',')[i]])
                else:
                        if model.coef_[0][i]<0:
                                legenda = legenda + '{:.3f}*{} '.format(model.coef_[0][i], dic_str[x_str.split(',')[i]])
                        else:
                                legenda = legenda + '+ {:.3f}*{} '.format(model.coef_[0][i], dic_str[x_str.split(',')[i]])
        if model.intercept_<0:
                legenda = legenda + '{:.3f} '.format(model.intercept_[0])
        else:
                legenda = legenda + '+ {:.3f} '.format(model.intercept_[0])
        
                       
        print(legenda)
        reg = model.predict(x)
        if regression_simple:
            
            fig = plt.figure()            
            
            plt.scatter(x, y)
            plt.plot(x, reg, color='red')
            plt.ylabel(dic_labels[y_str])
            plt.xlabel(dic_labels[x_str])
            
            x_min, x_max = plt.xlim()
            y_min, y_max = plt.ylim()
            
            plt.annotate(legenda, xycoords='data', xy=(x_min, y_max),
                             xytext=(+0, +10), textcoords='offset points', fontsize=12)
            
            #plt.show()
            plt.close()
            
            try:
                figManager = plt.get_current_fig_manager()
                figManager.window.showMaximized()
            except:
                pass
            fig.savefig('regressoes_simples/'+caminho+'/{} por {}.png'.format(y_str, x_str), bbox_inches='tight')
        else:
            if n_vetores == 2:
                fig = plt.figure()
                
                '''
                fig.subplots_adjust(left=0, bottom=0, right=1.15, top=2,
                                        wspace=0.33, hspace=0.2)
                '''
                
                ax = fig.gca(projection='3d')
                
                x_plt = numpy.array(dic[x_str.split(',')[0]])
                z_plt = numpy.array(dic[x_str.split(',')[1]])
                
                ax.scatter(x_plt, z_plt, y)

                
                ax.set_xlabel(dic_labels[x_str.split(',')[0]])
                ax.set_ylabel(dic_labels[x_str.split(',')[1]])
                ax.set_zlabel(dic_labels[y_str])
                #ax.view_init(30, 50)
                
                x_min, x_max = ax.get_xlim()
                y_min, y_max = ax.get_ylim()
                z_min, z_max = ax.get_zlim()
                
                vet_X = numpy.array([x_min, x_max, x_min, x_max])
                vet_Y = numpy.array([y_min, y_min, y_max, y_max])
                vet_Z = model.coef_[0][0]*vet_X + model.coef_[0][1]*vet_Y + model.intercept_[0]
                
                ax.plot_trisurf(vet_X, vet_Y, vet_Z, linewidth=0.2, antialiased=True, alpha=0.35, color='green')
                
                font_1 = {'family':'serif','color':'black','fontsize':'small'}
                ax.text2D(0, -0.11, legenda, fontdict=font_1, verticalalignment='top')

                
                try:
                    figManager = plt.get_current_fig_manager()
                    figManager.window.showMaximized()
                except:
                    pass
                fig.savefig('regressoes_multiplas/'+caminho+'/{} por {}.png'.format(y_str, x_str), bbox_inches='tight', dp=500)
                
                #plt.show()
                plt.close()

                
            if n_vetores >2: #se tiver mais de 2 X.
                fig = plt.figure()
                
                fig.subplots_adjust(left=-2, bottom=-2, right=1.15, top=2.4,
                                        wspace=0.33, hspace=0.2)
                
                
                for i in range(0,n_vetores):
                    item = x_str.split(',')[i]
                    x_aux = numpy.array(dic[item]).reshape(-1,1)
                    
                    axs = fig.add_subplot(n_vetores,1,i+1)
                    axs.scatter(x_aux, y)
                    axs.scatter(x_aux, reg, color='red')
                    axs.set_ylabel(dic_labels[y_str])
                    axs.set_xlabel(dic_labels[x_str])
                    
                    x_min, x_max = axs.get_xlim()
                    y_min, y_max = axs.get_ylim()
                    
                    if i==0:
                        axs.annotate(legenda, xycoords='data', xy=(x_min, y_max),
                                 xytext=(+0, +10), textcoords='offset points', fontsize=12)
                try:
                    figManager = plt.get_current_fig_manager()
                    figManager.window.showMaximized()
                except:
                    pass
                #plt.show()
                plt.close()
                fig.savefig('regressoes_multiplas/'+caminho+'/{} por {}.png'.format(y_str, x_str), bbox_inches='tight')


def reg_expo(y_str, x_str):

        #para as piores regressões exponenciais
        try:
            if not os.path.exists('regressoes_exponenciais/ruins'):
                os.makedirs('regressoes_exponenciais/ruins')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_exponenciais/ruins')

        #para regressões exponenciais medianas
        try:
            if not os.path.exists('regressoes_exponenciais/medianas'):
                os.makedirs('regressoes_exponenciais/medianas')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_exponenciais/medianas')

        #para as melhores regressões exponenciais
        try:
            if not os.path.exists('regressoes_exponenciais/melhores'):
                os.makedirs('regressoes_exponenciais/melhores')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_exponenciais/melhores')
        
        
        file = pd.read_excel('reduzido.xlsx')
        file.dropna(inplace=True)

        dataset = file.loc[(file.Type == 'FF')]
        
        B_up = dataset[['B_up']]
        Bx_up = dataset[['Bx_up']]
        By_up = dataset[['By_up']]
        Bz_up = dataset[['Bz_up']]
        B_down = dataset[['B_down']]
        Bx_down = dataset[['Bx_down']]
        By_down = dataset[['By_down']]
        Bz_down = dataset[['Bz_down']]
        V_up = dataset[['V_up']]
        V_down = dataset[['V_down']]
        Np_up = dataset[['Np_up']]
        Np_down = dataset[['Np_down']]
        Tp_up = dataset[['Tp_up (10^4)']]
        Tp_down = dataset[['Tp_down (10^4)']]
        Cs_up = dataset[['Cs_up']]
        Va_up = dataset[['Va_up']]
        Vms_up = dataset[['Vms_up']]
        Beta_up = dataset[['Beta_up']]
        Theta = dataset[['Theta']]
        Vsh = dataset[['Vsh']]
        M_A = dataset[['M_A']]
        Mms = dataset[['Mms']]


        dic_labels = {'B_up':'B_up (nT)', 'Bx_up':'Bx_up (nT)', 'By_up':'By_up (nT)', 'Bz_up':'Bz_up (nT)',
                'B_down':'B_down (nT)', 'Bx_down':'Bx_down (nT)', 'By_down':'By_down (nT)', 'Bz_down':'Bz_down (nT)',
                'V_up':'V_up (Km/s)', 'V_down':'V_down (Km/s)', 'Np_up':'Np_up $(1/m^3)$', 'Np_down':'Np_down $(1/cm^3)$',
                'Tp_up':'Tp_up $(K^o)*(10^6)$', 'Tp_down':'Tp_down $(K^o)*(10^6)$', 'Cs_up':'Cs_up (Km/s)',
                'Va_up':'Va_up (Km/s)', 'Vms_up':'Vms_up (Km/s)', 'Beta_up':'Beta_up', 'Theta':'Theta (\u03B8)',
                'Vsh':'Vsh (Km/s)', 'M_A':'M_A', 'Mms':'Mms'}


        dic_str = {'B_up':'B_up', 'Bx_up':'Bx_up', 'By_up':'By_up', 'Bz_up':'Bz_up',
                'B_down':'B_down', 'Bx_down':'Bx_down', 'By_down':'By_down', 'Bz_down':'Bz_down',
                'V_up':'V_up', 'V_down':'V_down', 'Np_up':'Np_up', 'Np_down':'Np_down',
                'Tp_up':'Tp_up', 'Tp_down':'Tp_down', 'Cs_up':'Cs_up',
                'Va_up':'Va_up', 'Vms_up':'Vms_up', 'Beta_up':'Beta_up', 'Theta':'Theta',
                'Vsh':'Vsh', 'M_A':'M_A', 'Mms':'Mms'}


        dic = {'B_up':B_up, 'Bx_up':Bx_up, 'By_up':By_up, 'Bz_up':Bz_up,
               'B_down':B_down, 'Bx_down':Bx_down, 'By_down':By_down,
               'Bz_down':Bz_down, 'V_up':V_up, 'V_down':V_down, 'Np_up':Np_up,
               'Np_down':Np_down, 'Tp_up':Tp_up, 'Tp_down':Tp_down, 'Cs_up':Cs_up,
               'Va_up':Va_up, 'Vms_up':Vms_up, 'Beta_up':Beta_up, 'Theta':Theta,
               'Vsh':Vsh, 'M_A':M_A, 'Mms':Mms}
        
        dic_aux = {}
        dic_aux.update(dic)
        del dic_aux[y_str]

        y = numpy.array(dic[y_str]) #recebendo o valor de Y
        
        ##recebendo o valor de X
        #para regressao simples
        if len(x_str.split(','))==1:
                regression_simple = True
                x = numpy.array(dic_aux[x_str]).reshape(-1,1)

        if regression_simple:
            try:
                model = LinearRegression()
                model.fit(x, numpy.log(y))


                if numpy.sqrt(model.score(x,numpy.log(y)))<0.5:
                    caminho = 'ruins'
                if numpy.sqrt(model.score(x,numpy.log(y)))>=0.5 and numpy.sqrt(model.score(x,numpy.log(y)))<0.75:
                    caminho = 'medianas'
                if numpy.sqrt(model.score(x,numpy.log(y)))>=0.75:
                    caminho = 'melhores'
                
                function = 'R = {:.3f}\nY = {:.4f}*e^({}*{:.4f})'.format(numpy.sqrt(model.score(x,numpy.log(y))), numpy.exp(model.intercept_[0]),dic_str[x_str], model.coef_[0][0])
                print(function)
                fig = plt.figure()
                plt.scatter(x, y)
                
                x_min, x_max = plt.xlim()
                
                
                x_aux = numpy.linspace(min(x),max(x), len(x))
                x_aux = numpy.array(x_aux).reshape(-1,1)
                
                reg = numpy.exp(model.intercept_[0])*numpy.exp(x_aux*model.coef_[0][0])
                
                
                plt.plot(x_aux, reg, color='red')
                plt.ylabel(dic_labels[y_str])
                plt.xlabel(dic_labels[x_str])
                
                x_min, x_max = plt.xlim()
                y_min, y_max = plt.ylim()
                
                plt.annotate(function, xycoords='data', xy=(x_min, y_max),
                                 xytext=(+0, +10), textcoords='offset points', fontsize=12)
                try:
                    figManager = plt.get_current_fig_manager()
                    figManager.window.showMaximized()
                except:
                    pass
                #plt.show()
                plt.close()
                fig.savefig('regressoes_exponenciais/'+caminho+'/exponencial - {} por {}.png'.format(y_str, x_str), bbox_inches='tight')
            except:
                print('erro')


def reg_log(y_str, x_str):
        
        #para as piores regressões logaritmicas
        try:
            if not os.path.exists('regressoes_logaritmicas/ruins'):
                os.makedirs('regressoes_logaritmicas/ruins')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_logaritmicas/ruins')

        #para regressões logaritmicas medianas
        try:
            if not os.path.exists('regressoes_logaritmicas/medianas'):
                os.makedirs('regressoes_logaritmicas/medianas')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_logaritmicas/medianas')

        #para as melhores regressões logaritmicas
        try:
            if not os.path.exists('regressoes_logaritmicas/melhores'):
                os.makedirs('regressoes_logaritmicas/melhores')
        except OSError:
            print ('Error: Creating directory. ' +  'regressoes_logaritmicas/melhores')
        
        
        file = pd.read_excel('reduzido.xlsx')
        file.dropna(inplace=True)

        dataset = file.loc[(file.Type == 'FF')]

        B_up = dataset[['B_up']]
        Bx_up = dataset[['Bx_up']]
        By_up = dataset[['By_up']]
        Bz_up = dataset[['Bz_up']]
        B_down = dataset[['B_down']]
        Bx_down = dataset[['Bx_down']]
        By_down = dataset[['By_down']]
        Bz_down = dataset[['Bz_down']]
        V_up = dataset[['V_up']]
        V_down = dataset[['V_down']]
        Np_up = dataset[['Np_up']]
        Np_down = dataset[['Np_down']]
        Tp_up = dataset[['Tp_up (10^4)']]
        Tp_down = dataset[['Tp_down (10^4)']]
        Cs_up = dataset[['Cs_up']]
        Va_up = dataset[['Va_up']]
        Vms_up = dataset[['Vms_up']]
        Beta_up = dataset[['Beta_up']]
        Theta = dataset[['Theta']]
        Vsh = dataset[['Vsh']]
        M_A = dataset[['M_A']]
        Mms = dataset[['Mms']]

        dic_labels = {'B_up':'B_up (nT)', 'Bx_up':'Bx_up (nT)', 'By_up':'By_up (nT)', 'Bz_up':'Bz_up (nT)',
                'B_down':'B_down (nT)', 'Bx_down':'Bx_down (nT)', 'By_down':'By_down (nT)', 'Bz_down':'Bz_down (nT)',
                'V_up':'V_up (Km/s)', 'V_down':'V_down (Km/s)', 'Np_up':'Np_up $(1/m^3)$', 'Np_down':'Np_down $(1/cm^3)$',
                'Tp_up':'Tp_up $(K^o)*(10^6)$', 'Tp_down':'Tp_down $(K^o)*(10^6)$', 'Cs_up':'Cs_up (Km/s)',
                'Va_up':'Va_up (Km/s)', 'Vms_up':'Vms_up (Km/s)', 'Beta_up':'Beta_up', 'Theta':'Theta (\u03B8)',
                'Vsh':'Vsh (Km/s)', 'M_A':'M_A', 'Mms':'Mms'}


        dic_str = {'B_up':'B_up', 'Bx_up':'Bx_up', 'By_up':'By_up', 'Bz_up':'Bz_up',
                'B_down':'B_down', 'Bx_down':'Bx_down', 'By_down':'By_down', 'Bz_down':'Bz_down',
                'V_up':'V_up', 'V_down':'V_down', 'Np_up':'Np_up', 'Np_down':'Np_down',
                'Tp_up':'Tp_up', 'Tp_down':'Tp_down', 'Cs_up':'Cs_up',
                'Va_up':'Va_up', 'Vms_up':'Vms_up', 'Beta_up':'Beta_up', 'Theta':'Theta',
                'Vsh':'Vsh', 'M_A':'M_A', 'Mms':'Mms'}
        
        
        dic = {'B_up':B_up, 'Bx_up':Bx_up, 'By_up':By_up, 'Bz_up':Bz_up,
               'B_down':B_down, 'Bx_down':Bx_down, 'By_down':By_down,
               'Bz_down':Bz_down, 'V_up':V_up, 'V_down':V_down, 'Np_up':Np_up,
               'Np_down':Np_down, 'Tp_up':Tp_up, 'Tp_down':Tp_down, 'Cs_up':Cs_up,
               'Va_up':Va_up, 'Vms_up':Vms_up, 'Beta_up':Beta_up, 'Theta':Theta,
               'Vsh':Vsh, 'M_A':M_A, 'Mms':Mms}
        
        
        dic_aux = {}
        dic_aux.update(dic)
        del dic_aux[y_str]

        y = numpy.array(dic[y_str]) #recebendo o valor de Y
        
        ##recebendo o valor de X
        #para regressao simples
        if len(x_str.split(','))==1:
                regression_simple = True
                x = numpy.array(dic_aux[x_str]).reshape(-1,1)
        
        if regression_simple:            
            model = LinearRegression()
            try:
                model.fit(numpy.log(x), y)

                if numpy.sqrt(model.score(numpy.log(x),y))<0.5:
                    caminho = 'ruins'
                if numpy.sqrt(model.score(numpy.log(x),y))>=0.5 and numpy.sqrt(model.score(numpy.log(x),y))<0.75:
                    caminho = 'medianas'
                if numpy.sqrt(model.score(numpy.log(x),y))>=0.75:
                    caminho = 'melhores'

                
                if model.intercept_<0:
                    function = 'R = {:.3f}\nY = {:.3f}*ln({}) {:.3f}'.format(numpy.sqrt(model.score(numpy.log(x),y)), model.coef_[0][0], dic_str[x_str], model.intercept_[0])
                else:
                    function = 'R = {:.3f}\nY = {:.3f}*ln({}) + {:.3f}'.format(numpy.sqrt(model.score(numpy.log(x),y)), model.coef_[0][0], dic_str[x_str], model.intercept_[0])
                print(function)
                fig = plt.figure()
                plt.scatter(x, y)
                
                x_min, x_max = plt.xlim()
                
                
                x_aux = numpy.linspace(min(x),max(x), len(x))
                x_aux = numpy.array(x_aux).reshape(-1,1)
                reg = model.predict(numpy.log(x_aux))
                
                plt.plot(x_aux, reg, color='red')
                plt.ylabel(dic_labels[y_str])
                plt.xlabel(dic_labels[x_str])
                
                x_min, x_max = plt.xlim()
                y_min, y_max = plt.ylim()
                
                plt.annotate(function, xycoords='data', xy=(x_min, y_max),
                                 xytext=(+0, +10), textcoords='offset points', fontsize=12)
                try:
                    figManager = plt.get_current_fig_manager()
                    figManager.window.showMaximized()
                except:
                    pass
                #plt.show()
                plt.close()
                fig.savefig('regressoes_logaritmicas/'+caminho+'/logaritmica - {} por {}.png'.format(y_str, x_str), bbox_inches='tight')
            except:
                print('erro')


dicionario = ['B_down', 'B_up', 'Bx_down', 'Bx_up', 'By_down', 'By_up', 'Bz_down', 'Bz_up',
              'V_down', 'V_up', 'Np_down', 'Np_up', 'Tp_down', 'Tp_up', 'Cs_up', 'Va_up',
              'Vms_up', 'Beta_up', 'Theta', 'Vsh', 'M_A', 'Mms']


#para regressões simples
for i in range(0,len(dicionario)-1):
        print('\n\nCalculando com y sendo {}\n\n'.format(dicionario[i]))
        for j in range(i+1,len(dicionario)):
                #reg_linear(dicionario[i], dicionario[j])
                #reg_expo(dicionario[i], dicionario[j])
                reg_log(dicionario[i], dicionario[j])

'''
#para regressões multipla de 2 variaveis independentes
for i in range(0,len(dicionario)-2):
        print('\n\nCalculando com y sendo {}\n\n'.format(dicionario[i]))
        for j in range(i+1,len(dicionario)-1):
                for k in range(j+1,len(dicionario)):
                        x_str = dicionario[j]+','+dicionario[k]
                        reg_linear(dicionario[i], x_str)
'''
