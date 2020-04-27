import string
from utils.dfa import DFA

class Token():
    def __init__(self, code, val, pos=None, charPos=None, line=None, col=None):
        self.code = code                   # token code (EOF has the code 0)
        self.val = val                     # token value
        self.pos = pos                     # token position in the source text // (in bytes starting at 0)
        self.charPos = charPos             # token position in the source text // (in characters starting at 0)
        self.line = line                   # line number (starting at 1)
        self.col = col                     # column number (starting at 1)


class Node():
    def __init__(self, words):
        if len(words) == 0:
            return
        self.value = words[0]
        self.next = None
        self.next = Node(words[1:])
        

class Buffer():
    '''
        This is an auxiliary class that is used by the scanner (and possibly by 
        other classes) to read the source stream into a buffer and retrieve 
        portions of it:
    '''
    def __init__ (self, stream):
        def clean(word):
            if word.isalnum():
                return [word]
            i = 0
            words = []
            buff = ''
            ignore = False
            while i < len(word):
                if word[i] in ['"', "'"]:
                    if ignore:
                        words.append(buff+word[i])
                        buff = ''
                    else:
                        buff = buff + word[i]
                    ignore = not ignore
                elif not ignore and i < len(word)-1 and word[i] == '.' and word[i+1] == '.':
                    if len(buff) > 0:
                        words.append(buff)
                    words.append(word[i] + word[i+1])
                    buff = ''
                    i += 1
                elif not ignore and word[i] in ['=','+','-','.','{', '}', '[' ,']']:
                    if len(buff) > 0:
                        words.append(buff)
                    words.append(word[i])
                    buff = ''
                else:
                    buff = buff + word[i]
                    
                i += 1
            return words

        file = open(stream, 'r')
        words = []
        for text in file.readlines():
            line = text.split()
            new_line = []
            for i in range(len(line)):
                new_line = new_line + clean(line[i])
            #print(new_line)
            words = words + new_line
        #input()
        file.close()
        self.currentWord =  Node(words)
        self.nextWord = self.currentWord
    
    def definition(self, value):
        code = None
        if value == '':
            code = 0
        if value == '.':
            code = 0
        if value == '=':
            code = 0
        if value == '+':
            code = 0
        if value == '-':
            code = 0
        elif value == 'COMPILER':
            code = 50
        elif value == 'CHARACTERS':
            code = 60
        elif value == 'KEYWORDS':
            code = 70
        elif value == 'TOKENS':
            code = 80
        elif value == 'END':
            code = 90
        else:
            code = -1
        return code

    def read(self):
        '''
            Read() returns the next character or 65536 if the input is exhausted
        '''
        
        word = self.currentWord.value
        self.currentWord = self.currentWord.next
        self.nextWord = self.currentWord
        return Token(self.definition(word), word)

    def peek(self):
        '''
            Peek() allows the scanner to read characters ahead without consuming them
        '''

        word = self.nextWord.value
        self.nextWord = self.nextWord.next
        return Token(self.definition(word), word)
    
    def resetPeek(self):
        self.nextWord = self.currentWord


class Scanner():
    '''
        The main class of the compiler (see Section 3.5) has to create a scanner 
        object and pass it either an input stream or the name of a file from where 
        the tokens should be read. The scanner's input buffer is exported in the 
        field buffer. It can be used to access the input text at random addresses 
        (see Section 3.4.3).
    '''

    def __init__(self, file):
        self.buffer = Buffer(file)

        #any_atr = set(string.printable)
        #self.any_atr = DFA('!'.join(list(any_atr)))
        self.hexdigit = DFA('!'.join(list(set('0123456789').union(set('ABCDEF')))))
        #self.noApostrophe  = DFA('!'.join(list(any_atr.difference(set("'")))))
        self.letter = DFA('a!b!c!d!e!f!g!h!i!j!k!l!m!n!o!p!q!r!s!t!u!v!w!x!y!z!A!B!C!D!E!F!G!H!I!J!K!L!M!N!O!P!Q!R!S!T!U!V!W!X!Y!Z')
        self.digit = DFA('0!1!2!3!4!5!6!7!8!9')
        #self.noQuote  = DFA('!'.join(list(any_atr.difference(set('"')))))

        self.ident = DFA('letter {letter!digit}', {'letter': self.letter, 'digit': self.digit})
        self.string =  DFA('" {noQuote} "')
        self.number =  DFA('digit {digit}', {'digit': self.digit})
        self.char =  DFA("' noApostrophe '")
        self.equal =  DFA("=")
        self.period =  DFA(".")
        self.plus =  DFA("+")
        self.minus =  DFA("-")
        test = DFA('CHR(digit)')
        test.get_core()

    def CHARACTERS(self):
        '''
            ["CHARACTERS" {SetDecl}]
            SetDecl = ident '=' Set.
            Set = BasicSet { ('+'!'-') BasicSet }.
            BasicSet = string ! ident ! Char [".." Char].
            Char = char ! "CHR" '(' number ')'.
        '''
        characters = {}
        token = self.peek()
        state = 0

        char = DFA("char!CHR'('number')'")
        char = self.char
        basicset = DFA('string!ident', {'string': self.string, 'ident': self.ident, 'char':self.char})
        mySet = DFA('BasicSet {(+!-) BasicSet}',{'BasicSet': basicset})

        M = {
            'S': [(self.string, ['B', "S'"]), (self.ident, ['B',"S'"]), (char, ['B',"S'"])], 
            'B': [(self.string, ['s']), (self.ident, ['i']), (char, ['c'])], 
            "S'": [(self.plus, ['+', 'B']), (self.minus, ['-', 'B']), (self.period, [])]
        }
        while token.code < 50:
            token = self.scan()
            
            if state == 0 and self.ident.check(token.val):
                name = token.val
                state += 1
                token = self.peek()
                values = []
            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()            
            elif state == 2 and self.period.check(token.val):
                '''
                a = the first symbol of w
                x = the top stack symbol
                while stack no empty
                    if x = a pop the stack and let a be the next symbol of w
                    else if x is terminal error
                    else if m[x,a] is not an entry error
                    else if m[x,a] = x--> y
                        output the production
                        pop stack
                        push y ont the stack with y1 on top
                    let x be the top stack
                '''
                inputs = values + ['.']
                a = inputs[0]
                stack = ['S', '.']
                x = stack[0]
                error = True
                character = []
                while 0 < len(stack) and error:
                    if x in ['i', 's', 'c', '+', '-']:
                        terminal = stack.pop(0)
                        value = inputs.pop(0)
                        character = character + [value]
                        #if x == 'i':
                        #    character = character + characters[value]
                        #if x == 's':
                        #    character = character + [value]
                        # print('match', x)
                        a = inputs[0]
                    elif x in M.keys():
                        for option in M[x]:
                            if option[0].check(a):
                                stack.pop(0)
                                stack = option[1] + stack
                                break
                    else:
                        error = False
                    x = stack[0]

                if error:
                    print("error")
                else:
                    characters[name] = character
                    print("CHARACTER ", name, "ADDED")
                state = 0
                token = self.peek()
            elif state == 2 :
                values.append(token.val)
                token = self.peek()
            else: 
                errors = {0:'ident', 1:'equal', 2:'set', 3:'period'}
                print('CHARACTERS error: read', token.val, 'expected ', errors[state])
                state = 0
        print(characters)
        return characters

    def KEYWORDS(self):
        '''
            ["KEYWORDS" {KeyworDecl}]
            KeywordDecl = ident '=' string '.'
            KeywordDecl = DFA('ident = string .', {'ident': self.ident, 'string': self.string})
        '''
        keywords = {}
        token = self.peek()
        state = 0
        while token.code < 50:
            token = self.scan()
            if state == 0 and self.ident.check(token.val):
                name = token.val
                state += 1
                token = self.peek()
            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()
            elif state == 2 and self.string.check(token.val):
                value = token.val
                state += 1
                token = self.peek()
            elif state == 3 and self.period.check(token.val):
                keywords[name] = value[1:-1]
                print("KEYWORD ", name, "ADDED")
                state = 0
                token = self.peek()
            else: 
                errors = {0:'ident', 1:'equal', 2:'string', 3:'period'}
                print('KEYWORDS error: read', token.val, 'expected ', errors[state])
                state = 0
        
        print(keywords)
        return keywords
    
    def TOKENS(self):
        '''
            ["TOKENS" {TokenDecl}]
            TokenDecl = ident ['=' TokenExpr ] ["EXCEPT KEYWORDS"] '.'.
            TokenExpr = TokenTerm {| TokenTerm }.
            TokenTerm = TokenFactor {TokenFactor}
            TokenFactor = Symbol ! ( TokenExpr ) ! [ TokenExpr ] ! { TokenExpr }.
            Symbol = ident ! string ! char
        '''
        tokens = {}
        token = self.peek()
        state = 0
        parentesisA = DFA("(")
        parentesisC = DFA(")")
        corchetesA = DFA("[")
        corchetesC = DFA("]")
        llaveA = DFA("{")
        llaveC = DFA("}")
        orDFA = DFA("|") 
        excep = DFA("EXCEPT")
        keys = DFA("KEYWORDS")

        M = {
            'E': [(self.string, ['T',"E'"]), (self.ident, ['T',"E'"]), (self.char, ['T',"E'"]), (llaveA, ['T',"E'"]), (parentesisA, ['T',"E'"]), (corchetesA, ['T',"E'"]), (parentesisC, ['T',"E'"]), (corchetesC, ['T',"E'"]), (llaveC, ['T',"E'"])], 
            "E'": [(orDFA, ['|','T',"E'"]), (parentesisC, []), (corchetesC, []), (llaveC, []), (self.period, [])], 
            'T': [(self.string, ['F', "T'"]), (self.ident, ['F', "T'"]), (self.char, ['F', "T'"]), (llaveA, ['F', "T'"]), (parentesisA, ['F', "T'"]), (corchetesA, ['F', "T'"])], 
            "T'": [(self.string, ['F', "T'"]), (self.ident, ['F', "T'"]), (self.char, ['F', "T'"]), (llaveA, ['F', "T'"]), (parentesisA, ['F', "T'"]), (corchetesA, ['F', "T'"]), (parentesisC, []), (corchetesC, []), (llaveC, []), (self.period, [])], 
            'F': [(self.string, ['S']), (self.ident, ['S']), (self.char, ['S']), (parentesisA, ['(', 'E', ')']), (corchetesA, ['[', 'E', ']']), (llaveA, ['{', 'E', '}'])],
            'S': [(self.string, ['s']), (self.ident, ['i']), (self.char, ['c'])],
        }

        while token.code < 50:
            token = self.scan()
            if state == 0 and self.ident.check(token.val):
                name = token.val
                state += 1
                token = self.peek()
                values = []
                flag = False
            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()
            elif state == 2 and excep.check([token.val]):
                token = self.peek()
                if keys.check([token.val]):
                    self.scan()
                    flag = True
                token = self.peek()
            elif state == 2 and self.period.check(token.val):
                '''
                a = the first symbol of w
                x = the top stack symbol
                while stack no empty
                    if x = a pop the stack and let a be the next symbol of w
                    else if x is terminal error
                    else if m[x,a] is not an entry error
                    else if m[x,a] = x--> y
                        output the production
                        pop stack
                        push y ont the stack with y1 on top
                    let x be the top stack
                '''
                inputs = values + ['.']
                a = inputs[0]
                stack = ['E', '.']
                x = stack[0]
                error = True
                token = []
                while 0 < len(stack) and error:
                    if x in ['i', 's', 'c', '|', '(', ')', '[', ']', '{', '}']:
                        terminal = stack.pop(0)
                        value = inputs.pop(0)
                        token = token + [value]
                        a = inputs [0]
                    elif x in M.keys():
                        for option in M[x]:
                            if option[0].check(a):
                                stack.pop(0)
                                stack = option[1] + stack
                                break
                    else:
                        error = False
                    x = stack[0]
                
                if error:
                    print("error")
                else:
                    tokens[name] = (flag, token)
                    print("KEYWORD ", name, "ADDED")

                state = 0
                token = self.peek()
            elif state == 2:
                values.append(token.val)
                token = self.peek()
            else: 
                self.resetPeek()
                print('TOKEN error', token.val, token.code, state)
                state = 0
        print(tokens)
        return tokens

    def COMPILER(self):
        token = self.scan()
        if token.val != 'COMPILER':
            print("expected compiler")
            return
        token = self.scan()
        if (self.ident.check(token.val)):
            print('COMPILER started')
            name = token.val
            token = self.scan()
            if (token.val == 'CHARACTERS'):
                print('CHARACTERS started')
                self.characters = self.CHARACTERS()
                token = self.scan()
                print('CHARACTERS ended')
            if (token.val == 'KEYWORDS'):
                print('KEYWORDS started')
                self.keywords = self.KEYWORDS()
                token = self.scan()
                print('KEYWORDS ended')
            if (token.val == 'TOKENS'):
                print('TOKENS started')
                self.tokens = self.TOKENS()
                print('TOKENS ended')
            if (token.val == 'END'):
                token = self.scan()
                if(token.val == (name+'.')):
                    print("succesfully exit")
                else:
                    print("unexpected END")
            print('COMPILER ended')
        else:
            print("unexpected compiler name")
    
    def scan(self):
        '''
            The method Scan() is the actual scanner. The parser calls it whenever it needs 
            the next token. Once the input is exhausted Scan() returns the end-of-file token, 
            which has the token number 0. For invalid tokens (caused by illegal token syntax 
            or by invalid characters) Scan() returns a special token kind, which normally causes
            the parser to report an error.
        '''
        token = self.buffer.read()
        #print('token read: ', token.code, token.val)
        return token

        
    def peek(self):
        '''
            Peek() can be used to read one or several tokens ahead without removing them from
            the input stream. With every call of Scan() (i.e. every time a token has been 
            recognized) the peek position is set to the scan position so that the first Peek()
            after a Scan() returns the first yet unscanned token.
        '''
        return self.buffer.peek()
    
    def resetPeek(self):
        self.buffer.resetPeek()
    
    def test(self, file):
        print('')
    


def main():
    scanner = Scanner("./tests/Aritmetica.ATG")
    #scanner.COMPILER()
    #scanner.test('./inputs/input1.txt')
    #args = scanner.start()
    

main()