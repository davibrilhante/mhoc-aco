# Using the magic encoding
# -*- coding: utf-8 -*-

#####################################################
#                   COMO USAR                       #
#   Entre com 3 argumentos ao executar o script     #
#   O primeiro argumento eh a metrica de interesse  #
#   0 - Atraso 1 - Intervalo 2 - Custo 3 - Iteracao #
#                                                   #
#   O segundo eh o budget                           #
#   0 - 0.1     1 - 0.5      2 - 0.9                #
#                                                   #
#   O Terceiro eh o numero de vertices              #
#   0 - 10      1 - 50       2 - 100                #
#####################################################

import matplotlib.pyplot as plt
import numpy as np
import math
import sys

def intervalCalc(array,conf):
        dummy = 0
        mean = np.average(array)
        for i in array: dummy += (i - mean)**2
        stdDev = math.sqrt(dummy/len(array))

        barStart = mean - stdDev
        barEnd = mean +stdDev
        if conf == 90: z=1.645
        elif conf == 95: z=1.96
        elif conf == 98: z=2.326
        elif conf == 99: z=2.576
        else: "Confidence interval not specified.Try 90, 95, 98 or 99"
        return stdDev*z/math.sqrt(len(array))


if __name__ == "__main__":
    arq = open("Comparativo_Euclidiano_3.csv")
    arq.readline()
    budgets = [0.1, 0.2, 0.3]
    metr = int(sys.argv[1])
    custo = int(sys.argv[2])
    n_vertices = int(sys.argv[3])

    metricas = ["Atraso","Intervalo","Custo_Orcamentario","Iteracao_Saida"]
    nv = ['100','150','250','500']
    instances = [0 for x in range(10)]
    array_y = [0 for x in range(10)]
    erro = [0 for x in range(10)]
    counter = 0 #counter de instancia
    
    ### LE O ARQUIVO QUE CONTEM OS RESULTADOS DAS NOSSAS RODADAS
    for i in arq: 
        line = i.strip("\r\n").split(";")
        if line[0].count(nv[n_vertices])<>0:
            array_y[counter] = float(line[(4*(custo+1))-1])
            instances[counter] = line[0]
            counter += 1
            '''
            elif n_vertices == 1 and line[1].count('100')==0:
                nums = [float(x) for x in line[3:]]
                array_y[counter] = np.average(nums)
                instances[counter] = line[1].split("/")[2]
                erro[counter] = intervalCalc(nums,95)
                counter += 1
            elif line[1].count('100')<>0 and n_vertices == 2:
                nums = [float(x) for x in line[3:]]
                array_y[counter] = np.average(nums)
                instances[counter] = line[1].split("/")[2]
                erro[counter] = intervalCalc(nums,95)
                counter += 1
            '''    
    print array_y


    ### LE O ARQUIVO COM RESULTADOS ANTERIORES
    '''
    arq.close()
    arq = open("otimos&best_values - Sheet3.csv")
    arq.readline()
    comp_y = [0 for x in range(10)]
    counter = 0
    flagD = False
    if metr <> 3:
        for i in arq:
            line = i.strip("\n").strip("\r").split(",")
            if line[0]<>'': nome = line[0]

            if float(line[2])==budgets[custo]:
                try:
                    value = float(line[6-(1*metr)])
                except:
                    try:
                        value = float(line[4-(1*metr)])
                    except:
                        value = 0
                if metr == 2:
                    value = int(line[1])
                #print value
                if nome.count(nv[n_vertices])<>0:
                    #print line[0]
                    #if n_vertices == 0 and nome.count('100')==0:
                    print value,
                    #if nome.count('F')<>0: index = instances.index(nome)
                    #else: index = instances.index(nome+'.in')
                    index = instances.index(nome+'.in')
                    comp_y[index] = value
                    
                    elif n_vertices == 1 and nome.count('100')==0:
                        if nome.count('F')<>0: index = instances.index(nome)
                        else: index = instances.index(nome+'.in')
                        print value
                        comp_y[index] = value
                    elif n_vertices == 2 and len(nome)>6:
                        if nome.count('F')<>0: index = instances.index(nome)
                        else: index = instances.index(nome+'.in')
                        print value
                        comp_y[index] = value
                    '''
    font = {'family' : 'normal',
    'size'   : 18}
    plt.rc('font', **font)

    plt.bar(range(len(array_y)), array_y, 0.35, yerr=erro, edgecolor='none', facecolor='royalblue', error_kw={'elinewidth':3, 'ecolor':'black'}, label='ACO')
    '''
    if metr == 2:
        for i in range(len(comp_y)):
            plt.hlines(y=comp_y[i], xmin=i, xmax=i+1,linewidth=3.0, color='orange')
    else:
        1#plt.bar([x+0.35 for x in range(len(array_y))], comp_y, 0.35, edgecolor='none', facecolor='orange', label='Langrangeano')
    '''
    plt.xticks([x+0.35 for x in range(len(array_y))],instances,size='small', rotation=45)
    plt.ylim([min(array_y),max(array_y)*1.15])
    plt.ylabel("Gap [%]")
    #plt.legend(loc=7, fontsize=18) 
    plt.tight_layout()
    for i in range(len(array_y)):
        ajuste = 20 
        arredonda = 1 
        if max(array_y)<3: 
            ajuste = 0.01 
            arredonda = 3
        plt.text(i, array_y[i]+max(erro)+ajuste, str(round(array_y[i],arredonda)), size=12,rotation=45)
        #if comp_y[i] <> 0:
        #plt.text(i+0.4, comp_y[i]+max(erro)+ajuste, str(round(comp_y[i],arredonda)), size=12, rotation=45) 
    plt.title('Budget Percentual = '+str(budgets[custo]), fontsize='18')
    fig = plt.figure(1, figsize=(100,90))
    fig.savefig("comp"+metricas[metr]+nv[n_vertices]+"-"+str(budgets[custo])+'.png')

    plt.show()
