from pilha import Pilha


class Grafo(object):
    def __init__(self, id):
        self.nome = id
        #self.numVertices = m
        #self.numArestas = n
        self.arestas = []
        self.vertices = []
        self.pilha = Pilha()
        self.ciclo = False

    
    def adicionaVertice(self, vertice):
        """ Cria uma lista com todos os vertives
        """
        self.vertices.append(vertice)

    def verticeEstaNaVizinhanca(self, vertice, vizinhos=list):
        for e in vizinhos:
            if (str(e.id) == str(vertice.id)):
                return True
        return False

    def adicionaAresta(self, aresta):
        #aresta.v1.vizinhos.append(aresta.v2)
        #aresta.v2.vizinhos.append(aresta.v1)

        #if (self.verticeEstaNaVizinhanca(aresta.v2, aresta.v1.vizinhos) == False):
        #    aresta.v1.vizinhos.append(aresta.v2)
        
        #if (self.verticeEstaNaVizinhanca(aresta.v1, aresta.v2.vizinhos) == False):
        #    aresta.v2.vizinhos.append(aresta.v1)

        self.arestas.append(aresta)
    
    def removeAresta(self, aresta):
        aresta.v1.vizinhos.remove(aresta.v2)
        aresta.v2.vizinhos.remove(aresta.v1)
        self.arestas.remove(aresta)


    def arvoreMinima(self):
        T = Grafo("MST")
        # Considerando G um grafo conexo, T tem pelo menos os mesmos vertices de G
        # Fazendo uma copia deles...
        for v in self.vertices:
            vertice = Vertice(v.id)
            vertice.custoUpgrade = v.custoUpgrade
            T.adicionaVertice(vertice)
        
        self.arestas.sort(key=lambda aresta: aresta.peso)

        for a in self.arestas:
            for v in T.vertices:
                if v.id == a.v1.id:
                    v1 = v

            for v in T.vertices:
                if v.id == a.v2.id:
                    v2 = v

            aresta = Aresta(a.id, v1, v2)
            aresta.setPeso(a.peso)
            T.adicionaAresta(aresta)

            #print ("--Adicionando a aresta", aresta.id)

            T.possuiCiclo()
            if T.ciclo:
                #print ("PossuiCiclo!!!")
                T.removeAresta(aresta)
                T.ciclo = False
        return T


    def possuiCiclo(self):
        for v in self.vertices:
            #print(v.id)
            #print(v.marcado)
            self.P(v)
            for ver in self.vertices: ver.marcado = False
    
    def P(self, v):
        v.marcado = True
        self.pilha.empilha(v)
        for w in v.vizinhos:
            if (w.marcado == False):
                #print("aresta de arvore!")
                self.P(w)
            else:
                if (self.pilha.existeV(w)) and (self.pilha.saoConsecutivos(v, w) == False):
                    #print("aresta de retorno!")
                    #print("POSSUI CICLO!")
                    self.ciclo = True
                    
        self.pilha.desempilha()

    def atualizaVertice(self, v = []):
        """ Recebe uma lista de vertices para serem atualizados no grafo
        """

        #reseta as arestas para d0
        #for a in self.arestas:
        #    a.peso = a.d0

        for vertice in v:
            for a in self.arestas:
                if (vertice.id == a.v1.id):
                    #print ("atualiza aresta", a.id)
                    if (a.v2.atualizado):
                        a.peso = a.d2
                    else:
                        a.peso = a.d1


                if (vertice.id == a.v2.id):
                    #print ("atualiza aresta", a.id)
                    if (a.v1.atualizado):
                        a.peso = a.d2
                    else:
                        a.peso = a.d1
            
            vertice.atualizado = True
        
        for vertice in v:
            vertice.atualizado = False


    
class Vertice(object):
    """ Elemento vertice do grafo
    """
    def __init__(self, id):
        self.id = id
        self.marcado = False
        self.atualizado = False
        self.vizinhos = []
        self.custoUpgrade = 0
        self.feromonio = 1
    
    def __str__(self):
        return "Vertice: ", str(self.id)

class Aresta(object):
    """ Elemento aresta de um grafo
    """
    def __init__(self, id, v1=Vertice(None), v2=Vertice(None)):
        self.id = id
        self.v1 = v1
        self.v1.vizinhos.append(v2)

        self.v2 = v2
        self.v2.vizinhos.append(v1)
        self.peso = None
        self.d0 = 0
        self.d1 = 0
        self.d2 = 0
    
    def __str__(self):
        return "Aresta: ", str(self.id)
    
    def setPeso(self, peso):
        self.peso = peso

    def setD0(self, d0):
        self.d0 = d0

    def setD1(self, d1):
        self.d1 = d1
    
    def setD2(self, d2):
        self.d2 = d2