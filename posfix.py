operands = '{}|+'

precedence = {'*':3, '?':3, '+':3, '.':2, '|':1, ' ':2} 

def conversionToPostfix(exp):
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
    
    for i in exp: 
        if i.isalnum() or i == '#' or i == '"' or i == "'": 
            output.append(i) 
            
        elif i  == '(': 
            top += 1
            array.append(i)

        elif i == ')': 
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
            else: 

                if not top == -1:
                    top -= 1
                    array.pop()

        else: 
            while(not top == -1 and notGreater(i, array) and i != '*'): 
                top -= 1
                b = array.pop()
                output.append(b) 

            top += 1
            array.append(i)
    print(output, array, top)
    while not top == -1: 
        if not top == -1:
            top -= 1
            c =  array.pop()
        else:
            c = "$"
        output.append(c) 

    return output


print(conversionToPostfix('l (l|d)*'))
print(conversionToPostfix(['digit','.','digit','*']))
