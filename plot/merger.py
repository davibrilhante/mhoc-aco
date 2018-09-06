reader = open('reader')
output = open('resultados-c','w')
for i in reader:
    filename = i.strip('\r').strip('\n')
    arq = open(filename)
    arq.readline()
    for j in arq:
        output.write(j)
    arq.close()
