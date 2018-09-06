from itertools import permutations
from toy_alterado import Instancia
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import threading
import time
from conversor import arvoreMinima
import csv

#global threadLock
#threadLock = threading.Lock()
NUMERO_RODADAS= 1
MAX_ITERACOES = 20
LIMITE_ITERACOES_ESTAGNACAO = 10
CSV_PARAMETERS_SETTINGS = 'parameter_settings.txt'
CSV_CONFIGURACOES = 'configuracoes_alfa_beta_taxa.txt'
CSV_RESULTADOS = 'resultados_totais.txt'
TAXA_FORMIGAS_EM_RELACAO_A_VERTICES = 0.1
INTERVALO_ENTRE_RODADAS = 5
TAXAS_DE_ORCAMENTO = [0.1, 0.2, 0.3]
ALFAS = [1]
BETAS = [0.1]

class myThread(threading.Thread):
   def __init__(self, threadID, nome, path, grafoOriginal, orcamento):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.nome = nome
      self.path = path
      self.grafoOriginal = grafoOriginal
      self.orcamento = orcamento
      self.custo = float('inf')
      
   def run(self):
      #print "Starting " + self.name
      #print_time(self.name, self.counter, 3)
      # Get lock to synchronize threads
      #threadLock.acquire()
      
      instancia = Instancia(self.path)
      grafo = instancia.grafo
      inicio_obtencao_solucao_candidata = time.time()
        
      #********************************************************************************
      self.solucaoCandidata = obterSolucaoCandidata(grafo, self.grafoOriginal, self.orcamento, self.nome)
      fim_da_obtencao_solucao_candidata = time.time()
      #print self.nome, ": Obtencao da solucao candidata demorando: ", fim_da_obtencao_solucao_candidata - inicio_obtencao_solucao_candidata
      #time.sleep(2)
      #print self.nome, ": Entrando na atualizacao do grafo"
      grafo.atualizaVertice(self.solucaoCandidata)
      #print self.nome, ": Calculando arvoreMinima"
      arestasArvore = arvoreMinima(grafo)
      T0 = grafo#grafo.arvoreMinima()
      T0.arestas = arestasArvore
      T0.vertices = grafo.vertices
      custo = 0
      
      #print self.nome, ": Calculando custos da arvore T0"
      for a in T0.arestas:
        custo = custo + a.peso
        
      self.custo = custo
      #print self.nome, ": Custo da arvore T0 e:", self.custo
      # Free lock to release next thread
      #threadLock.release()
      


def obterSolucaoCandidata(grafo, grafoOriginal, orcamento, nomeThread):
    vertices = grafo.vertices
    pVertice = []
    verticesOrig = grafoOriginal.vertices

    # atualiza a info de feromonio dos vertices
    for vOrig in verticesOrig:
        for v in vertices:
            if (vOrig.id == v.id):
                v.feromonio = vOrig.feromonio
   
    fero = [] # vetor de feromonios
    heu = []
    for v in vertices:
        #print(nomeThread, ": v.feromonio: ", v.feromonio)
        fero.append(v.feromonio)
        heu.append(v.custoUpgrade)
    
    #print nomeThread, ": Lista heu: ", heu
    #print nomeThread, ": Lista fero: ", heu
    fero_mod = np.power(fero, alfa) # calcula fero elevado a alfa
    heu_mod = np.power(heu, beta) # calcula info heu elevado a beta

    vProduto = []
    R = 0
    for i in range(len(vertices)):
        R = R + (fero_mod[i] * heu_mod[i])
        vProduto.append(fero_mod[i] * heu_mod[i])

    for i in range(len(vertices)):
        pVertice.append(vProduto[i]/R)
    
    custoDeUpgrade = 0
    #'''    
    while (True):
        tamanhoSolucao = random.randint(1, len(vertices))  # Escolhe aleatoriamente um tamanho de solucao entre 1 e a quantidade de vertices (inclusive)
        solucaoCandidata = []

        #solucaoCandidata = random.sample(vertices, tamanhoSolucao)  # seleciona aleatoriamente n = tamanhoSolucao vertices
        solucaoCandidata = np.random.choice(vertices, tamanhoSolucao, False, pVertice)
        #print nomeThread, ": Solucao candidata: ", solucaoCandidata
       
        custoDeUpgrade = 0
        for v in solucaoCandidata:
                #print nomeThread, ": Vertice da solucaoCandidata:", v.id
                custoDeUpgrade = custoDeUpgrade + v.custoUpgrade
        
        if (custoDeUpgrade <= orcamento):
            #for v in solucaoCandidata:
            #    print("-----------------------------> ", v.id)
            break

    return solucaoCandidata
    '''
    savings = 0
    tentativas = 0
    tamanhoSolucao = random.randint(1, len(vertices))  # Escolhe aleatoriamente um tamanho de solucao entre 1 e a quantidade de vertices (inclusive)
    solucaoCandidata = []
    while len(solucaoCandidata) < tamanhoSolucao:
        candidato = np.random.choice(vertices, 1, False, pVertice)[0]
        tentativas+=1
        #print "savings", savings, "candidato", candidato.custoUpgrade 
        if (savings + candidato.custoUpgrade < orcamento) and (solucaoCandidata.count(candidato) == 0):
            solucaoCandidata.append(candidato)
            savings += candidato.custoUpgrade
        if tentativas == len(vertices):
            break
    return solucaoCandidata
    '''
def ConstroiSolucaoFormiga(grafoOriginal, nFormigas, path, orcamento):
    solucao_local = []  # armazena a solucao otima local dentre todas as formigas
    mst_otimo = float('inf') # armazena otimo da iteracao das n formigas
    threads = []
    #threadLock = threading.Lock()
    
    for formiga in range(nFormigas):
        #print("Formiga ", formiga)

        thread = myThread(formiga, 'Thread-'+str(formiga), path, grafoOriginal, orcamento)
        thread.start()
        threads.append(thread)
        
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    for t in threads:
        if t.custo <= mst_otimo:
            mst_otimo = t.custo
            solucao_local = t.solucaoCandidata

    print("menor custo tsp: ", mst_otimo)
    return (solucao_local, mst_otimo)

    
def AtualizaFeromonio(grafo, solucao):
    for v in grafo.vertices:
        v.feromonio = (1-taxaEvaporacao) * v.feromonio

    for s in solucao[0]:
        for v in grafo.vertices:
            if (s.id == v.id):
                v.feromonio = v.feromonio + (Q/solucao[1])

                
def ExecutaSolucaoBaseadaParametros(path, taxa_de_orcamento, custo_otimo, maxIteracoes, Q, alfa, beta, taxaEvaporacao, numero_figura, contador_instancia):
    iteracao = 0
    iteracao_saida = None
    ts_leitura_inicial = time.time()
    print contador_instancia, ".1.1. Leitura iniciada as: ", ts_leitura_inicial  
    instancia = Instancia(path)
    ts_leitura_final = time.time()
    print contador_instancia, ".1.2. Leitura finalizada as: ", ts_leitura_final
    print contador_instancia, ".1.3. Intervalo de leitura: ", ts_leitura_final - ts_leitura_inicial
    
    print "O numero de vertices/formigas e:", instancia.num_vertices
    if instancia.num_vertices > 50:
        nFormigas = int (instancia.num_vertices * TAXA_FORMIGAS_EM_RELACAO_A_VERTICES)
    else:
        nFormigas = instancia.num_vertices
    orcamento = taxa_de_orcamento * instancia.custo_upgrade_total
    print 'Orcamento disponivel:', orcamento
    grafo = instancia.grafo

    #inicialmente o feronomio recebe valor 1
    for v in grafo.vertices:
        v.feromonio = 1

    mst_otimo = float('inf') # armazena otimmo global
    sol_otima = []
    solucoes = []
    limiteEstagnacao = LIMITE_ITERACOES_ESTAGNACAO
    estagnacao = 0
    while (iteracao < maxIteracoes):
        #print ("Iteracao: ", iteracao)
        iteracao = iteracao + 1
        estagnacao += 1
        #print("--Construindo solucoes de formigas")

        # retorna uma lista com duas posicoes: na posicao 0 uma lista com os vertices da solucao, e na pos 1 o custo da mst
        solucao = ConstroiSolucaoFormiga(grafo, nFormigas, path, orcamento)

        #print 'SOLUCAO', solucao
        if solucao[1] <= mst_otimo:
            solucoes.append(solucao)
            mst_otimo = solucao[1]
            sol_otima = solucao
            estagnacao = 0
        else:
            solucoes.append([[], mst_otimo])
        #print("--Aplicando a busca local")

        AtualizaFeromonio(grafo, solucao)
        #print("--Atualiza feromonio")
        if estagnacao == limiteEstagnacao:
            iteracao_saida = iteracao
            break


    ts_calculo_final = time.time()
    print contador_instancia, ".1.4. Calculo finalizado as: ", ts_calculo_final
    print contador_instancia, ".1.5. Intervalo de calculo: ", ts_calculo_final - ts_leitura_final
    #print 'SOL_OTIMA',sol_otima
    """
    for v in sol_otima[0]:
        print ("vertice otimo: ", v.id)
    print ("mst otimo: ", sol_otima[1])
    """
    custo_orcamentario = 0
    for v in sol_otima[0]:
        custo_orcamentario = custo_orcamentario + v.custoUpgrade
        
    mmst = []
    for sol in range(len(solucoes)):
        mmst.append(solucoes[sol][1])
        
    if iteracao_saida == None:
        iteracao_saida == iteracao - 1 # Caso em que para no numero maximo de iteracoes
    
    plt.figure(num=numero_figura)
    plt.plot(mmst)
    plt.ylabel('custo mst')
    plt.xlabel('n iteracoes')
    titulo = instancia.nome + "\nn formigas: " + str (nFormigas)
    plt.title(titulo)
    plt.show()
    plt.savefig(instancia.nome+'alfa'+str(alfa)+'beta'+str(beta)+'taxasEvaporacao'+str(taxaEvaporacao)+'.png')
    print("menor custo tsp: ", mst_otimo)

    return mst_otimo, ts_calculo_final - ts_leitura_final, custo_orcamentario, iteracao_saida
                
                
if __name__ == "__main__":
    path_diretorio = 'instancias/entradas_reais/'
    #path_diretorio = 'instancias/toys/'
    onlyfiles = [f for f in listdir(path_diretorio) if isfile(join(path_diretorio, f))]
    print "Arquivos: ", onlyfiles
    #onlyfiles = ['r10.in']
    numero_rodadas = NUMERO_RODADAS
    
    paths =[]
    for nome_arquivo in onlyfiles:
        paths.append(path_diretorio + nome_arquivo)
    
    print "O paths e: ", paths
    
    #path = 'instancias/toys/D57.in'
    #paths = ['instancias/toys/D57.in', 'instancias/toys/D69.in']
    
    # configuracao de parametros
    #orcamento = 23 # orcamento pra upgrade
    #taxa_de_orcamento = 0.3 #0.1 0.5 0.9
    custo_otimo = float('inf') # valor do custo nas arestas de MST
    maxIteracoes = MAX_ITERACOES # num max de iteracoes
    Q = 1 # quantidade de feroemonio
    #nFormigas = len(grafo.vertices) # Quantidade de formigas tem que ser igual a quantidade de vertices
    #nFormigas = 5
    #alfas = [1.0]  # parametriza a influencia do feromonio
    #alfas = [0.05, 0.1, 0.5, 1, 2]
    #alfas = ALFAS
    #alfas = [0.25, 1]
    #betas = [1.0] # parametriza a influencia da info metaheuristica
    #betas = [0.1, 0.5, 1, 2, 5]
    #betas = [0.25, 1]
    #betas = BETAS
    taxasEvaporacao = [0.5]
    #taxasEvaporacao = [0.1, 0.2, 0.5, 0.7, 0.9]
    #taxasEvaporacao = [0.1, 0.9]
    solucao = [] # as melhores solucoes de cada iteracao
    #inicialmente a info heuristica recebe valor 1
    #infoHeuristica = 1
    
    #with open(CSV_PARAMETERS_SETTINGS, 'wb') as csvfile:
    
    csvfile1 = open(CSV_PARAMETERS_SETTINGS, 'wb')
    spamwriter1 = csv.writer(csvfile1, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)
    spamwriter1.writerow(['Instancia', 'Taxa de Orcamento', 'Melhor Alfa', 'Melhor Beta', 'Melhor Taxa Evaporacao', 'Melhor Atraso da Arvore', 'Tempo do Melhor Atraso', 'Custo Orcamentario do Melhor Atraso', 'Mediana dos Atrasos das Rodadas Para Melhores Alfa, Beta e Taxa', 'Media dos Atrasos das Rodadas Para Melhores Alfa, Beta e Taxa', 'Desvio dos Atrasos das Rodadas Para Melhores Alfa, Beta e Taxa', 'Mediana dos Intervalos das Rodadas Para Melhores Alfa, Beta e Taxa', 'Media dos Intervalos das Rodadas Para Melhores Alfa, Beta e Taxa', 'Desvio dos Intervalos das Rodadas Para Melhores Alfa, Beta e Taxa', 'Mediana dos Custos Orcamentarios das Rodadas Para Melhores Alfa, Beta e Taxa', 'Media dos Custos Orcamentarios das Rodadas Para Melhores Alfa, Beta e Taxa', 'Desvio dos Custos Orcamentarios das Rodadas Para Melhores Alfa, Beta e Taxa', 'Melhor Atraso Medio', 'Melhor Intervalo Medio', 'Melhor Custo Orcamentario Medio' ,'Alfa Para Melhor Atraso Medio', 'Beta Para Melhor Atraso Medio', 'Taxa Para Melhor Atraso Medio'])
    
    csvfile2 = open(CSV_CONFIGURACOES, 'wb')
    spamwriter2 = csv.writer(csvfile2, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)
    spamwriter2.writerow(['Instancia', 'Numero da Configuracao', 'Taxa de Orcamento', 'Alfa', 'Beta', 'Taxa'])
    
    csvfile3 = open(CSV_RESULTADOS, 'wb')
    spamwriter3 = csv.writer(csvfile3, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)
    spamwriter3.writerow(['Tipo Resultado', 'Instancia', 'Numero Configuracao', 'Rodadas'])
    
    contador_instancia = 1 #Utilizado para exibicao dos resultados no console
    numero_figura = 0
    
    for path in paths:
        print contador_instancia, ". Instancia: ", path
        melhor_mst_otimo = float('inf')
        melhor_alfa = None
        melhor_beta = None
        melhor_taxa = None
        melhor_intervalo = None
        melhor_lista_mst_otimo = None
        melhor_lista_intervalo = None
        melhor_configuracao = None
        melhor_custo_orcamentario = None
        lista_de_listas_mst_otimo = []
        lista_de_listas_intervalos = []
        lista_de_listas_custos_orcamentario = []
        lista_de_configuracoes = []
        numeracao_configuracao = -1
        for taxa_de_orcamento in TAXAS_DE_ORCAMENTO:
            for alfa in ALFAS:
                for beta in BETAS:
                    for taxaEvaporacao in taxasEvaporacao:
                        lista_mst_otimo = []
                        lista_intervalo = []
                        lista_custo_orcamentario = []
                        lista_iteracao_saida = []
                        numeracao_configuracao = numeracao_configuracao + 1
                        lista_de_configuracoes.append({'alfa': alfa, 'beta': beta, 'taxa': taxaEvaporacao})
                        spamwriter2.writerow([path, numeracao_configuracao, taxa_de_orcamento, alfa, beta, taxaEvaporacao])
                        
                        for rodada in range(numero_rodadas):
                            print contador_instancia, ".1. Executando rodada #", rodada, "para Taxa de Orcamento: ", taxa_de_orcamento, " para:  Alfa = ", alfa, "Beta = ", beta, "taxaEvaporacao = ", taxaEvaporacao 
                            random.seed(rodada)
                            np.random.seed(rodada)
                            numero_figura = numero_figura + 1
                            mst_otimo, intervalo_calculo, custo_orcamentario_solucao, iteracao_saida = ExecutaSolucaoBaseadaParametros(path, taxa_de_orcamento, custo_otimo, maxIteracoes, Q, alfa, beta, taxaEvaporacao, numero_figura, contador_instancia)
                            print contador_instancia, ".1. Executando rodada #", rodada, " melhor atraso foi: ", mst_otimo 
                            lista_mst_otimo.append(mst_otimo)
                            lista_intervalo.append(intervalo_calculo)
                            lista_custo_orcamentario.append(custo_orcamentario_solucao)
                            lista_iteracao_saida.append(iteracao_saida)
                                                    
                            if mst_otimo < melhor_mst_otimo:
                                melhor_configuracao = numeracao_configuracao
                                melhor_mst_otimo = mst_otimo
                                melhor_alfa = alfa
                                melhor_beta = beta
                                melhor_taxa = taxaEvaporacao
                                melhor_intervalo = intervalo_calculo
                                melhor_custo_orcamentario = custo_orcamentario_solucao
                            
                            time.sleep(INTERVALO_ENTRE_RODADAS)
                        
                        linha_a_ser_escrita_arquivo_atrasos = ['Atraso', path, numeracao_configuracao] + lista_mst_otimo
                        linha_a_ser_escrita_arquivo_intervalos = ['Intervalo', path, numeracao_configuracao] + lista_intervalo
                        linha_a_ser_escrita_arquivo_custos_orcamentario = ['Custo_Orcamentario', path, numeracao_configuracao] + lista_custo_orcamentario
                        linha_a_ser_escrita_arquivo_iteracao_saida = ['Iteraca_Saida', path, numeracao_configuracao] + lista_iteracao_saida
                        spamwriter3.writerow(linha_a_ser_escrita_arquivo_atrasos)
                        spamwriter3.writerow(linha_a_ser_escrita_arquivo_intervalos)
                        spamwriter3.writerow(linha_a_ser_escrita_arquivo_custos_orcamentario)
                        spamwriter3.writerow(linha_a_ser_escrita_arquivo_iteracao_saida)
                        
                        #Lista de listas que contem os resultados de todas as configuracoes para todas as rodadas                    
                        lista_de_listas_mst_otimo.append(lista_mst_otimo)
                        lista_de_listas_intervalos.append(lista_intervalo)
                        lista_de_listas_custos_orcamentario.append(lista_custo_orcamentario)
        
        lista_melhor_configuracao_mst_otimo = lista_de_listas_mst_otimo[melhor_configuracao]
        lista_melhor_configuracao_intervalos = lista_de_listas_intervalos[melhor_configuracao]
        lista_melhor_configuracao_custos_orcamentario = lista_de_listas_custos_orcamentario[melhor_configuracao]
        
        media_mst_otimo = np.mean(lista_melhor_configuracao_mst_otimo)
        mediana_mst_otimo = np.median(lista_melhor_configuracao_mst_otimo)
        desvio_mst_otimo = np.std(lista_melhor_configuracao_mst_otimo)
        
        media_intervalo_melhor_configuracao = np.mean(lista_melhor_configuracao_intervalos)
        mediana_intervalo_melhor_configuracao = np.median(lista_melhor_configuracao_intervalos)
        desvio_intervalo_melhor_configuracao = np.std(lista_melhor_configuracao_intervalos)
        
        media_custo_orcamentario_melhor_configuracao = np.mean(lista_melhor_configuracao_custos_orcamentario)
        mediana_custo_orcamentario_melhor_configuracao = np.median(lista_melhor_configuracao_custos_orcamentario)
        desvio_custo_orcamentario_melhor_configuracao = np.std(lista_melhor_configuracao_custos_orcamentario)
        
        melhor_media_mst = float('inf')
        melhor_media_intervalos = None
        melhor_media_alfa = None
        melhor_media_beta = None
        melhor_media_taxa = None
        contador_configuracoes = 0
        
        for lista_de_mst_otimo in lista_de_listas_mst_otimo:
            media_mst = np.mean(lista_de_mst_otimo)
            mediana_mst = np.median(lista_de_mst_otimo)
            desvio_mst_otimo = np.std(lista_de_mst_otimo)
            
            if media_mst < melhor_media_mst:
                melhor_media_mst = media_mst
                melhor_media_intervalos = np.mean(lista_de_listas_intervalos[contador_configuracoes])
                melhor_media_custos_orcamentario = np.mean(lista_de_listas_custos_orcamentario[contador_configuracoes])
                melhor_media_alfa = lista_de_configuracoes[contador_configuracoes]['alfa']
                melhor_media_beta = lista_de_configuracoes[contador_configuracoes]['beta']
                melhor_media_taxa = lista_de_configuracoes[contador_configuracoes]['taxa']
            
            contador_configuracoes = contador_configuracoes + 1
            
        #with open(CSV_PARAMETERS_SETTINGS, 'w') as csvfile:
        #    spamwriter = csv.writer(csvfile, delimiter=',',
        #                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter1.writerow([path, taxa_de_orcamento, melhor_alfa, melhor_beta, melhor_taxa, melhor_mst_otimo, melhor_intervalo, melhor_custo_orcamentario, mediana_mst_otimo, media_mst_otimo, desvio_mst_otimo, mediana_intervalo_melhor_configuracao, media_intervalo_melhor_configuracao, desvio_intervalo_melhor_configuracao, mediana_custo_orcamentario_melhor_configuracao, media_custo_orcamentario_melhor_configuracao, desvio_custo_orcamentario_melhor_configuracao, melhor_media_mst, melhor_media_intervalos, melhor_custo_orcamentario, melhor_media_alfa, melhor_media_beta, melhor_media_taxa])
                        
        contador_instancia = contador_instancia + 1
    
    csvfile1.close()
    csvfile2.close()
    csvfile3.close()
    
    exit(0)
