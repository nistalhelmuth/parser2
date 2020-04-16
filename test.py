letter = set('abcdefghijklmnopqrstuvwxyz')
digit = set('0123456789')
#ident = letter {letter | digit}.
'''
INICIO : A
ESTADOS : AB
TRANSICIONES : {'A': {'1': 'B'}, 'B': {'1': 'B'}}
SIMBOLOS : 1
ACEPTACION : ['A', 'B']
'''


f = open('test1.txt','r')
for line in f:
    words = line.split()
    print(words)
f.close()

f = open('test1.txt','r')
x = f
while True:
    c = x.read(1)
    if not c:
      print ("End of file")
      break
    print ("Read a character:", c)
print("asdf",f.read(1))
f.close()