from Grafo import GrafoListaAdj
from ArvoreGerMinima import ArvoreGerMinima
from toy_alterado import Instancia

def arvoreMinima(grafo):
    E = []

    G = GrafoListaAdj(orientado = False)

    for a in grafo.arestas:
        E.append((int(a.v1.id)+1, int(a.v2.id)+1, a.peso))

    G.DefinirN(len(grafo.vertices))

    for (u,v,w) in E:
        e = G.AdicionarAresta(u,v); e.w = w

    ET = ArvoreGerMinima(G)

    tree = []
    for i in ET:
        tree.append((i.v1-1,i.v2-1))

    counter1 = 0
    counter2 = 0

    final = []

    #print len(grafo.arestas)
    for i in grafo.arestas:
        counter1 += 1
        adj1 = (int(i.v1.id),int(i.v2.id)) 
        if tree.count(adj1)== 1:
            counter2 += 1
            final.append(i)
            #grafo.removeAresta(i)
        #else:
        #   grafo.removeAresta(i)

    #print counter1, counter2, len(final)
    #print tree, len(tree)
    #print [(a.v1.id, a.v2.id) for a in final]
    return final

"""
path = 'instancias/entradas_reais/v50_353.in'
instancia = Instancia(path)
grafo = instancia.grafo
arvoreMinima(grafo)
"""