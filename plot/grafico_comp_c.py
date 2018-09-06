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
#   O Terceiro eh o inicio do plot                  #
#   0 - 1 a 10      1 - 11 a 20                     #
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
    arq = open("resultados-c")
    budgets = [0.1, 0.2, 0.3]
    metr = int(sys.argv[1])
    custo = int(sys.argv[2])

    metricas = ["Atraso","Intervalo","Custo_Orcamentario","Iteracao_Saida"]
    #nv = ['100','150','250','500']
    if sys.argv[3] == '0':  nv = ['c0'+str(x)+'.in' for x in range(1,10)]+['c10.in']
    elif sys.argv[3] == '1':nv = ['c1'+str(x)+'.in' for x in range(1,10)]+['c20.in']
 
    instances = [0 for x in range(10)]
    array_y = [0 for x in range(10)]
    erro = [0 for x in range(10)]
    counter = 0 #counter de instancia
    
    ### LE O ARQUIVO QUE CONTEM OS RESULTADOS DAS NOSSAS RODADAS
    for i in arq: 
        line = i.strip("\r\n").split(";")
        if line[0] == metricas[metr] and int(line[2]) == custo:
            print line[1].split("/")[2]
            if nv.count(line[1].split('/')[2])<>0:
                nums = [float(x) for x in line[3:]]
                array_y[counter] = np.average(nums)
                instances[counter] = line[1].split("/")[2]
                erro[counter] = intervalCalc(nums,95)
                counter += 1
    print array_y


    ### LE O ARQUIVO COM RESULTADOS ANTERIORES
    arq.close()
    arq = open("otimos&best_values - Sheet2.csv")
    arq.readline()
    comp_y = [0 for x in range(10)]
    counter = 0
    flagD = False
    if metr <> 3:
        for i in arq:
            line = i.strip("\n").strip("\r").split(",")
            if line[0]<>'': nome = line[0]+'.in'

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
                ###print value
                #if nome.count(nv[n_vertices])<>0:
                if nv.count(nome)<>0:
                    ###print line[0]
                    ###if n_vertices == 0 and nome.count('100')==0:
                    print value,
                    ###if nome.count('F')<>0: index = instances.index(nome)
                    ###else: index = instances.index(nome+'.in')
                    #index = instances.index(nome+'.in')
                    index = instances.index(nome)
                    comp_y[index] = value
    ### LE O ARQUIVO COM RESULTADOS ANTERIORES
    arq.close()
    arq = open("otimos&best_values - Sheet2.csv")
    arq.readline()
    comp_z = [0 for x in range(10)]
    counter = 0
    flagD = False
    if metr <> 3:
        for i in arq:
            line = i.strip("\n").strip("\r").split(",")
            if line[0]<>'': nome = line[0]+'.in'

            if float(line[2])==budgets[custo]:
                try:
                    value = float(line[4-(1*metr)])
                except:
                    try:
                        value = float(line[6-(1*metr)])
                    except:
                        value = 0
                if metr == 2:
                    value = int(line[1])
                ###print value
                #if nome.count(nv[n_vertices])<>0:
                if nv.count(nome)<>0:
                    ###print line[0]
                    ###if n_vertices == 0 and nome.count('100')==0:
                    print value,
                    ###if nome.count('F')<>0: index = instances.index(nome)
                    ###else: index = instances.index(nome+'.in')
                    #index = instances.index(nome+'.in')
                    index = instances.index(nome)
                    comp_z[index] = value

    font = {'family' : 'normal',
    'size'   : 18}
    plt.rc('font', **font)

    lag = [(x/y-1.0)*100 for x, y in zip(array_y, comp_y)]
    bb = [(x/y-1.0)*100 for x, y in zip(array_y, comp_z)]

    plt.bar(range(len(array_y)), lag, 0.35, edgecolor='none', facecolor='royalblue', label='lagrangeano')
    plt.bar([x+0.35 for x in range(len(array_y))], bb, 0.35, edgecolor='none', facecolor='green',label='B&B')

    plt.xticks([x+0.35 for x in range(len(array_y))],instances,size='small', rotation=45)
    plt.ylabel("Gap [%]")
    plt.legend(loc=7, fontsize=18) 
    plt.tight_layout()
    '''
    for i in range(len(array_y)):
        ajuste = 2 
        arredonda = 1 
        plt.text(i, lag[i]+ajuste, str(round(lag[i],arredonda)), size=12,rotation=45)
        if comp_y[i] <> 0:
            plt.text(i+0.4, bb[i]+ajuste, str(round(bb[i],arredonda)), size=12, rotation=45) 
    '''
    plt.title('Budget Percentual = '+str(budgets[custo]), fontsize='18')
    fig = plt.figure(1, figsize=(100,90))
    fig.savefig("c1-10-gap-bb-"+str(budgets[custo])+'.png')

    plt.show()
