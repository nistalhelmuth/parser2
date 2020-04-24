import sys
import string as strDefinition
from .draw import drawPrettyGraph
from .posfix import conversionToPostfix

class Node():
    def __init__(self,  label, left=None,right=None):
        self.left = left
        self.right = right
        self.label = label
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = None
        self.nullable = None
        self.position = None
    
    def setPositions(self, positions=[]):
        if self.label == '*':
            self.left.setPositions(positions)
            return positions
        elif self.label == '|' or self.label == '_':
            new_positions = self.left.setPositions(positions)
            self.right.setPositions(new_positions)
            return positions
        elif self.label !='#':
            if len(positions) > 0 :
                self.position = len(positions)
            else:
                self.position = 0
            positions.append((self.label, self.position))
            return positions
        return positions

    def setNullable(self):
        if self.label == '|':
            self.nullable = self.left.setNullable() or self.right.setNullable()
        elif self.label == '_':
            A = self.left.setNullable()
            B = self.right.setNullable()
            self.nullable = A and B
        elif self.label == '*':
            self.left.setNullable()
            self.nullable = True
        elif self.label == '#':
            self.nullable = True
        else:
            self.nullable = False
        
        return self.nullable
    
    def setFirstPos(self):
        if self.label == '|':
            A = self.left.setFirstPos()
            B = self.right.setFirstPos()
            self.firstpos = A.union(B)
        elif self.label == '_':
            A = self.left.setFirstPos()
            B = self.right.setFirstPos()
            if self.left.nullable:
                self.firstpos = B.union(A)
            else:
                self.firstpos = A
        elif self.label == '*':
            self.firstpos = self.left.setFirstPos()
        elif self.label != '#':
            self.firstpos.add(self.position)

        return self.firstpos

    def setLastPos(self):
        if self.label == '|':
            A = self.left.setLastPos()
            B = self.right.setLastPos()
            self.lastpos = A.union(B)
        elif self.label == '_':
            A = self.left.setLastPos()
            B = self.right.setLastPos()
            if self.right.nullable:
                self.lastpos = A.union(B)
            else:
                self.lastpos = B
        elif self.label == '*':
            self.lastpos = self.left.setLastPos()
        elif self.label != '#':
            self.lastpos.add(self.position)   
       
        return self.lastpos
    
    def setFollowPos(self, table, dic):
        if self.label == '_':
            for i in self.left.lastpos:
                table[(dic[i], i)] = table[(dic[i], i)].union(self.right.firstpos)
            table = self.left.setFollowPos(table, dic)
            table = self.right.setFollowPos(table, dic)
        elif self.label == '|':
            table = self.left.setFollowPos(table, dic)
            table = self.right.setFollowPos(table, dic)
        elif self.label == '*':
            for i in self.lastpos:
                table[(dic[i], i)] = table[(dic[i], i)].union(self.firstpos)
            table = self.left.setFollowPos(table, dic)
        return table

        

    def evaluate(self, followtable, language):
        transitions = {}
        Dstates = [self.firstpos]
        letters = 'ABCDEFGHI'
        count = 0
        while count < len(Dstates):
            S = Dstates[count]
            for letter in language:
                U = set()
                for p in S:
                    if (letter, p) in followtable.keys():
                        A = followtable[(letter, p)]
                        U = U.union(A)
                #if len(U) == 0:
                #    continue
                if U not in Dstates:
                    Dstates.append(U)

                if letters[count] in transitions.keys():
                    transitions[letters[count]][letter] =  letters[Dstates.index(U)]
                else:
                    transitions[letters[count]] = {letter: letters[Dstates.index(U)]}
            count += 1
        return transitions, Dstates, letters[:count]

    def show(self):
        if self.left != None:
            self.left.show()
        if self.right != None:
            self.right.show()
              
        if self.right != None and self.left != None:
            #print(self.nullable, (self.left.label, self.label, self.right.label), self.position, self.firstpos, self.lastpos, self.followpos)
            print((self.left.label, self.label, self.right.label), self.position, self.followpos)
        elif self.label == '*':
            #print(self.nullable, (self.left.label, self.label), self.position, self.firstpos, self.lastpos, self.followpos)
            print((self.left.label, self.label), self.position, self.followpos)
        else:
            #print(self.nullable, (self.label), self.position, self.firstpos, self.lastpos, self.followpos)
            print((self.label), self.position, self.followpos)
        
        #if self.label not in '.|*':
        #    print((self.label), self.position, self.followpos)
        

class DFA:

    def __init__(self, exp):
        # Genera el arbol
        expre = conversionToPostfix(exp)
        self.stack = []
        for ch in expre:
            if ch == '*':
                node_A = self.stack.pop()
                self.stack.append(Node(left=node_A,label='*'))
            elif ch == '_' or ch =='|':
                node_A = self.stack.pop()
                node_B = self.stack.pop()
                self.stack.append(Node(left=node_B, label=ch, right=node_A))
            elif ch == '+': #rr+
                node_A = self.stack.pop()
                node_B = Node(left=node_A, label='*')
                self.stack.append(Node(left=node_A, label='_', right=node_B))
            elif ch == '?': #r|ɛ
                node_A = self.stack.pop()
                node_B = Node(label='#')
                self.stack.append(Node(left=node_A, label='|', right=node_B))
            else:
                self.stack.append(Node(label=ch))
        node_A = self.stack.pop()
        node_B = Node(label='Z')
        self.stack.append(Node(left=node_A, label='_', right=node_B))

        core = self.stack.pop()
        # Encuentra el lenguaje
        self.language = []
        for letter in expre:
            if letter not in self.language and letter not in '*|_#?+':
                self.language.append(letter)
        positions = core.setPositions()
        core.setNullable()
        core.setFirstPos()
        core.setLastPos()
        table = {}
        dic = {}
        for position in positions:
            table[position] = set()
            dic[position[1]] = position[0]
        followtable = core.setFollowPos(table=table, dic=dic)
        transitions, groups, states = core.evaluate(followtable = followtable, language = self.language)
        self.accept = []
        for i in range(len(groups)):
            #esto es para saber cuál es el posicion del utlimo caracter (Z/#)
            if len(dic.keys())-1 in groups[i]:
                self.accept.append(states[i])
        self.transitions = transitions
        self.groups = groups
        self.states = states
        self.start = states[0]
    
    def get_core(self):
        drawPrettyGraph([self.start], self.states, self.transitions, self.accept, 'dfa2')
        return self.start, self.states, self.language, self.transitions, self.accept, self.groups
    
    def check(self, expre):
        def move(state, transitions, value):
            if value in transitions[state].keys():
                return transitions[state][value]
            return -1
            
        def new_move(state, transitions, value):
            any_atr = set(strDefinition.printable)
            table = {'digit': set('0123456789'), 'letter': set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'noQuote': set(strDefinition.printable).difference(set('"'))}
            if value in transitions[state].keys():
                return transitions[state][value]

            for key in transitions[state].keys():
                if key in table.keys() and value in table[key]:
                    return transitions[state][key]
            return -1

        
        s = self.start
        for letter in expre:
            s = new_move(s, self.transitions, letter)
            if s == -1:
                break
        if s in self.accept:
            return True
        return False


#ident = 'letter {letter|digit}'
#string = '" {noQuote} "'
#dfa = DFA(".")
#dfa_core = dfa.get_core()
#test = '.'

#print(dfa.check(test))