
f = open("paths",'r')
flag = False
root = 0
for l in f:
	if l== "./C-conv:\n" or l == "./Euclidean:\n":
		root = l.strip(':\n')
		flag = True
	elif flag == True:
		path2file = root + "/" + l.strip('\n')
		if path2file == './C-conv/': 
			continue		
		outfile = l.strip(".dat\n") + ".in"
		output = open(outfile,'w')
		instance = open(path2file)
		vertex = 0
		edge = 0
		flag2 = False
		for k in instance:
			line = k.split()
			if line == []:
				continue
			elif line[0] == 'Nodes':
				vertex = int(line[1])
			elif line[0] == 'Edges':
				edge = int(line[1])
			elif line[0] == 'E' and flag2 == False:
				output.write(str(vertex)+' '+str(edge)+'\n')
				output.write(line[1]+" "+line[2]+" "+line[3]+" "+line[4]+" "+line[5]+"\n")				
				flag2 = True
			elif line[0] == 'END' or line[0]=='EOF' or line[0]=='EOL':
				flag2 = False
			elif line[0] == 'E' and flag2 == True:
				output.write(line[1]+" "+line[2]+" "+line[3]+" "+line[4]+" "+line[5]+"\n")
			elif line[0]=='T':
				output.write(line[2]+"\n")
		output.close()
		instance.close()
	elif l=='\n':
		flag = False
