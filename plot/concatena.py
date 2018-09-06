

if __name__ == "__main__":
    output = open("resultado_final","w")
    base = open("resultados_totais.txt")
    files = ["resultados_totais-11-20.txt","resultados_totais-21-30.txt"]
    base.readline()
    g = base.readlines()
    flag = True
    for f in files:
        arq = open(f)
        arq.readline()
        counter = 0
        for lines in arq:
            line = lines.rstrip("\r\n").split(";")
            if flag:
                g[counter] = g[counter].rstrip("\r\n") + ";" + ";".join(line[3:])
            else:
                g[counter] = g[counter].rstrip("\r\n") + ";" + ";".join(line[3:]) + "\r\n"
            counter += 1
        flag = False
    for i in g:
        print i
        output.write(i) 
