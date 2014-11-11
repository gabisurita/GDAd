#encoding: utf-8

Carga 	 = open("carga2s2014.txt", "r")
CargaCSV = open("carga2s2014.csv", "w")

Oferecimentos = []

for Of in Carga:
	try:
		Prof  = Of[ : (Of.find(" E"))]
		Sigla = Of[(Of.find(" E"))+1 : (Of.index(" E")+6)]
		Turma = Of[(Of.find(" E"))+7]
		
		CargaCSV.write(Sigla+","+Turma +","+Prof+	"\n")
		Oferecimentos.append([Sigla, Turma, Prof])
	
	except:
		CargaCSV.close()
		break


Header		= open("header.tex")
Footer 		= open("footer.tex")
Template  = open("template.tex")


Page = open("frontpages.tex", "w")
for i in Header:
	Page.write(i)

FullTemplate = ""

for i in Template:
	FullTemplate = FullTemplate + i
	
print FullTemplate.find("{1}")
	
i = 0

for Of in Oferecimentos:
	try:
		i += 1
		a = FullTemplate
		a = a.replace("{0}", Of[0])
		a = a.replace("{1}", Of[1])
		a = a.replace("{2}", Of[2])
		a = a.replace("{3}", str(i))
		
		Page.write(a)
	except:
		break
	
for i in Footer:
	Page.write(i)

Page.close()
