class Pilha():
    def __init__(self):
        self.dados = []
 
    def empilha(self, elemento):
        self.dados.append(elemento)
 
    def desempilha(self):
        if not self.vazia():
            return self.dados.pop(-1)
 
    def vazia(self):
        return len(self.dados) == 0
    
    def existeV(self, vertice):
        for w in self.dados:
            if (str(vertice.id) == str(w.id)):
                return True
        return False
    
    def saoConsecutivos(self, v, w):
        indexv, indexw = -100, -100
        if self.existeV(v):
            indexv = self.dados.index(v)
        if self.existeV(w):
            indexw = self.dados.index(w)
        if abs(indexv - indexw) == 1:
            return True
        return False