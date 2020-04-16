operands = '{}|+'

precedence = {'.':1} 

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
        if i.isalnum() or i == '#': 
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

    while not top == -1: 
        if not top == -1:
            top -= 1
            c =  array.pop()
        else:
            c = "$"
        output.append(c) 

    return "".join(output)


print(conversionToPostfix('c.i.e.i'))
'''
# Class to convert the expression 
class Conversion: 
      
    # Constructor to initialize the class variables 
    def __init__(self, capacity): 
        self.top = -1 
        self.capacity = capacity 
        # This array is used a stack  
        self.array = [] 
        # Precedence setting 
        self.output = [] 
        self.precedence = {'*':3, '?':3, '+':3, '.':2, '|':1} 
      
    # Pop the element from the stack 
    def pop(self): 
        if not self.top == -1: 
            self.top -= 1
            return self.array.pop() 
        else: 
            return "$"
  
    # Check if the precedence of operator is strictly 
    # less than top of stack or not 
    def notGreater(self, i): 
        try: 
            a = self.precedence[i] 
            b = self.precedence[self.array[-1] ] 
            return True if a  <= b else False
        except KeyError:  
            return False
              
    # The main function that converts given infix expression 
    # to postfix expression 
    def infixToPostfix(self, exp): 
          
        # Iterate over the expression for conversion 
        for i in exp: 
            # If the character is an operand,  
            # add it to output 
            if i.isalpha(): 
                self.output.append(i) 
              
            # If the character is an '(', push it to stack 
            elif i  == '(': 
                self.top += 1
                self.array.append(i)
  
            # If the scanned character is an ')', pop and  
            # output from the stack until and '(' is found 
            elif i == ')': 
                while( (not self.top == -1) and self.array[-1]  != '('): 
                    a = self.pop() 
                    self.output.append(a) 
                if (not self.top == -1 and self.array[-1]  != '('): 
                    return -1
                else: 
                    self.pop() 
  
            # An operator is encountered 
            else: 
                while(not self.top == -1 and self.notGreater(i) and i != '*'): 
                    self.output.append(self.pop()) 
                self.top += 1
                self.array.append(i)
  
        # pop all the operator from the stack 
        while not self.top == -1: 
            self.output.append(self.pop()) 
  
        return 
        print ("".join(self.output) )
  
# Driver program to test above function 
#exp = "(a|b)*.a.b.b.c"
#exp = "b*.a.b|#"
#exp = "b*.a.b?" #
#exp = "((a|b)*)*.#.((a|b)|#)*"
exp = "(a|b)*.((a|(b.b))*.#))"
obj = Conversion(len(exp)) 
obj.infixToPostfix(exp) 
  
# This code is contributed by Nikhil Kumar Singh(nickzuck_007) 
'''