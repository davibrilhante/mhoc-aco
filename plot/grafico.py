#####################################################
#                   COMO USAR                       #
#   Entre com 2 argumentos ao executar o script     #
#   O primeiro argumento eh a metrica de interesse  #
#   0 - Atraso 1 - Intervalo 2 - Custo 3 - Iteracao #
#                                                   #
#   O segundo eh o budget                           #
#   0 - 0.1     1 - 0.5      2 - 0.9                #
#                                                   #
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
    arq = open("resultado_final")
    budgets = [0.1, 0.5, 0.9]
    metr = int(sys.argv[1])
    custo = int(sys.argv[2])
    metricas = ["Atraso","Intervalo","Custo_Orcamentario","Iteracao_Saida"]
    instances = [0 for x in range(13)]
    array_y = [0 for x in range(13)]
    erro = [0 for x in range(13)]
    counter = 0 #counter de instancia
    
    ### LE O ARQUIVO QUE CONTEM OS RESULTADOS DAS NOSSAS RODADAS
    for i in arq: 
        line = i.strip("\r\n").split(";")
        if line[0] == metricas[metr] and int(line[2]) == custo and line[1].count('D')==0:
            nums = [float(x) for x in line[3:]]
            array_y[counter] = np.average(nums)
            instances[counter] = line[1].split("/")[2]
            erro[counter] = intervalCalc(nums,95)
            counter += 1
    #print instances


    ### LE O ARQUIVO COM RESULTADOS ANTERIORES
    arq.close()
    arq = open("otimos&best_values - Sheet1.csv")
    arq.readline()
    comp_y = [0 for x in range(13)]
    counter = 0
    for i in arq:
        line = i.strip("\n").strip("\r").split(",")
        if line[0]<>'' and line[0].count('D')==0:
            counter = 0
            if line[0].count('F')<>0:
                index = instances.index(line[0])
            else:
                index = instances.index(line[0]+".in")
        try: 
            value = float(line[6])
        except:
            try:
                value = float(line[4])
            except:
                value = 0
        if counter == custo: comp_y[index] = value
        counter += 1

    plt.errorbar(range(len(array_y)),array_y,yerr=erro)
    plt.plot(range(len(array_y)), array_y)
    plt.plot(range(len(array_y)), comp_y)
    plt.xticks(range(len(instances)),instances,size='small')
    plt.ylabel(metricas[metr])
    plt.tight_layout()
    plt.show()
