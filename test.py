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
        if 1 < len(words):
            self.next = Node(words[1:])
        

class Buffer():
    '''
        This is an auxiliary class that is used by the scanner (and possibly by 
        other classes) to read the source stream into a buffer and retrieve 
        portions of it:
    '''
    def __init__ (self, stream):
        file = open(stream, 'r')
        words = [word for line in file.readlines() for word in line.split()]
        print(words)
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
        elif value == 'EXCEPT':
            code = 80
        elif value == 'KEYWORDS':
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

        any_atr = set(string.printable)
        hexdigit = set('0123456789').union(set('ABCDEF'))
        noApostrophe  = any_atr.difference(set("'"))
        letter = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        digit = set('0123456789')
        nodigit  = any_atr.difference(digit)
        noQuote  = any_atr.difference(set('"'))

        self.ident = DFA('letter {letter|digit}')
        self.string =  DFA('" {noQuote} "')
        self.number =  DFA('digit {digit}')
        self.char =  DFA("' noApostrophe '")
        self.equal =  DFA("=")
        self.period =  DFA(".")

        '''
        symbolTable = {'letter': letter, 'digit': digit, 'ident': ident}
        '''
        
    def CHARACTERS(self):
        '''
            ["CHARACTERS" {SetDecl}]
            SetDecl = ident '=' Set.
            Set = BasicSet { ('+'|'-') BasicSet }.
            BasicSet = string | ident | Char [".." Char].
            Char = char | "CHR" '(' number ')'.
            ident = Set.
            Set = (string | ident | char | "CHR" '(' number ')' [".." char | "CHR" '(' number ')']) { ('+'|'-') BasicSet }.
        '''
        characters = {}
        token = self.peek()
        state = 0
        while token.code < 50 and state != -1:
            if state == 0 and self.ident.check(token.val):
                name = token.val
                state += 1
                token = self.peek()
            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()
            elif state == 3 and self.string.check(token.val):
                value = token.val
                state += 1
                token = self.peek()
            elif state == 4 and self.period.check(token.val):
                keywords[name] = value
                for i in range(state):
                    self.scan()
                state = 0
            else: 
                state = -1
                self.resetPeek()
                print('KEYWORDS error', token.value, token.code)

        return characters

    def KEYWORDS(self):
        '''
            ["KEYWORDS" {KeyworDecl}]
            KeywordDecl = ident '=' string '.'
        '''
        keywords = {}
        token = self.peek()
        state = 0
        while token.code < 50 and state != -1:
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
                print("KEYWORD ", value, "ADDED")
                for i in range(state+1):
                    self.scan()
                token = self.peek()
                state = 0
            else: 
                self.resetPeek()
                print('KEYWORDS error', token.val, token.code, state)
                state = -1
        
        print(keywords)
        return keywords
    
    def TOKENS(self):
        '''
            ["TOKENS" {TokenDecl}]
            TokenDecl = ident ['=' TokenExpr ] ["EXCEPT KEYWORDS"] '.'.
            TokenExpr = TokenTerm {'|' TokenTerm }.
            TokenTerm = TokenFactor {TokenFactor}
            TokenFactor = Symbol | '(' TokenExpr ')' | '[' TokenExpr ']' | '{' TokenExpr '}'.
            Symbol = ident | string | char
        '''
        return
        tokens = {}

        Symbol = superDFA('ident | string | char')

        TokenDecl = superDFA([ident, DFA('[= TokenExpr]'), DFA('[EXCEPT KEYWORDS].')])
        while TokenDecl.check():
            name, value = TokenDecl.get()
            if name != None:
                tokens[name] = value
            else: 
                print('KEYWORDS error')

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
                token = self.scan()
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
    


def main():
    scanner = Scanner("./tests/test1.txt")
    scanner.COMPILER()
    #args = scanner.start()
    

main()