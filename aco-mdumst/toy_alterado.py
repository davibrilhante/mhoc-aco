from grafo import Grafo, Vertice, Aresta

def encontraVertice(lista_vertices, nome_vertice):
    #print "A lista vertice de entrada do encontraVertice e: ", lista_vertices
    #print "O nome_vertice passado na encontraVertice e: ", nome_vertice
    for vertice in lista_vertices:
        #print "O nome_vertice no for do encontraVertice e: ", vertice.id
        if vertice.id == nome_vertice:
            #"O vertice de entrada ", nome_vertice, "foi encontrado e o objeto vertice e:", vertice, "com id: ", vertice.id
            return vertice
            

def lerInstancia(path, grafo):
    file = open(path, 'r')
    num_arestas = float("inf")
    num_vertices = float("inf")
    lista_vertices = []
    custo_upgrade_total = 0

    for num_linha, line in enumerate(file):
        #se quero ler a linha $linha o i tem que ser i = ($linha - 1)
        #print "O num_linha e: ", num_linha, "e o num_arestas e: ", num_arestas
        if num_linha == 0:
            num_vertices = int(line.split()[0])
            num_arestas = int(line.split()[1])
            #print "O numero de vertices e: ", num_vertices
            #print "O numero de arestas e: ", num_arestas
            
        elif num_linha > num_arestas:
            #print "O nome do vertice e: ",  str(num_linha-num_arestas-1)
            #print "O custo do vertice e: ", line.split()[0]
            vertice = Vertice(str(num_linha-num_arestas-1)) #Nomeia cada vertice pelo valor inteiro
            lista_vertices.append(vertice)
            vertice.custoUpgrade = float(line.split()[0])
            grafo.adicionaVertice(vertice)
            custo_upgrade_total = custo_upgrade_total + vertice.custoUpgrade
    file.close()
    
    file = open(path, 'r') #reabre o arquivo pois precisa ler primeiro todos os vertices para contabiliza-los e nomea-los
    
    for num_linha, line in enumerate(file):
        #print "O novo num_linha e: ", num_linha    
        if num_linha > 0 and num_linha <= num_arestas: #esta na parte do arquivo que le as arestas
            nome_vertice_endpoint_0 = line.split()[0]
            #print "O nome do vertice 0 e: ", nome_vertice_endpoint_0
            nome_vertice_endpoint_1 = line.split()[1]
            #print "O nome do vertice 1 e: ", nome_vertice_endpoint_1
            nome_aresta = nome_vertice_endpoint_0 + "-" + nome_vertice_endpoint_1
            #print "O nome da aresta e: ", nome_aresta
            aresta = Aresta(nome_aresta, encontraVertice(lista_vertices, nome_vertice_endpoint_0), encontraVertice(lista_vertices, nome_vertice_endpoint_1))
            #print "A aresta adicionada foi: ", nome_aresta
            aresta.setPeso(float(line.split()[2]))
            #print "O peso da aresta: ", nome_aresta, " foi: ", line.split()[2]
            aresta.setD1(float(line.split()[3]))
            #print "O D1 da aresta: ", nome_aresta, " foi: ", line.split()[3]
            aresta.setD2(float(line.split()[4]))
            #print "O D2 da aresta: ", nome_aresta, " foi: ", line.split()[4]
            
            grafo.adicionaAresta(aresta)
    
    file.close()
    
    return grafo, num_vertices, custo_upgrade_total

    
class Instancia(object):
    def __init__(self, path):
        file = open(path, 'r')
        nome = [valor_lido for valor_lido in file.readline().split()]
        file.close()
        self.nome = "D" + nome[0] + nome[1]
        ##print "O nome do grafo e: ", self.nome
        
        self.grafo, self.num_vertices, self.custo_upgrade_total = lerInstancia(path, Grafo(self.nome))