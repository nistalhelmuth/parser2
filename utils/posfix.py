precedence = {'*':3, '?':3, '&':3, '_':2, '|':1, ' ':2} 

def conversionToPostfix(expresion):
    def pop(top, array):
        if not top == -1:
            top -= 1
            return array.pop()
        else:
            return "$"
    
    def notGreater(i, array):
        try: 
            a = precedence[i] 
            b = precedence[array[-1]] 
            return True if a  <= b else False
        except KeyError:  
            return False

    top = -1
    array = []
    output = []
    #print(expresion)
    exp = '_'.join(expresion.split())
    #print(exp)
    i = 0
    while i < len(exp):
        if exp[i].isalnum() or exp[i] in ['#', '.', '+', '-', '"', "'"]:
            count = 0
            buff = exp[i]
            while i+count+1 < len(exp) and ( exp[i+count+1].isalnum() or exp[i+count+1].isalnum() in ['#', '"', "'"]):
                count += 1
                buff = buff + exp[i+count]
            output.append(buff) 
            i += count
        #if exp[i] in ['"', "'"]:

            
        elif exp[i] in ['(' ,'[' ,'{']: 
            top += 1
            array.append(exp[i])

        elif exp[i] == ')': 
            while((not top == -1) and array[-1]  != '('): 

                #a = pop(top, array) 
                if not top == -1:
                    top -= 1
                    a =  array.pop()
                else:
                    a = "$"

                output.append(a) 
            if (not top == -1 and array[-1]  != '('): 
                return -1
            elif not top == -1:
                    top -= 1
                    array.pop()
        
        elif exp[i] == ']': 
            while((not top == -1) and array[-1]  != '['): 

                #a = pop(top, array) 
                if not top == -1:
                    top -= 1
                    a =  array.pop()
                else:
                    a = "$"

                output.append(a) 
            output.append('?') 
            if (not top == -1 and array[-1]  != '['): 
                return -1
            elif not top == -1:
                    top -= 1
                    array.pop()
        
        elif exp[i] == '}': 
            while((not top == -1) and array[-1]  != '{'): 

                #a = pop(top, array) 
                if not top == -1:
                    top -= 1
                    a =  array.pop()
                else:
                    a = "$"

                output.append(a) 
            output.append('*') 
            if (not top == -1 and array[-1]  != '{'): 
                return -1
            elif not top == -1:
                    top -= 1
                    array.pop()
        
        else: 
            while(not top == -1 and notGreater(exp[i], array) and exp[i] != '*'): 
                top -= 1
                if exp[i] != '*':
                    count -= 1
                b = array.pop()
                output.append(b) 

            top += 1
            array.append(exp[i])
        i += 1
    while not top == -1: 
        if not top == -1:
            top -= 1
            c =  array.pop()
        else:
            c = "$"
        output.append(c) 
    #print(output)
    return output

#print(conversionToPostfix('.'.join(['letter','{letter|digit}'])))
#print(conversionToPostfix('abb*'))
#print(conversionToPostfix('.'.join(['a','b','b'])))
#print()
#print(conversionToPostfix('(a*|b*).c'))
#print(conversionToPostfix('.'.join(['(a*|b*)','c'])))
#print()
#print(conversionToPostfix('b*.a.b.b.(a|b)?'))
#print(conversionToPostfix('.'.join(['{b}','a','b','b','[a|b]'])))

