import string
from dfa import DFA

class Buffer():
    '''
        This is an auxiliary class that is used by the scanner (and possibly by 
        other classes) to read the source stream into a buffer and retrieve 
        portions of it:
    '''
    def __init__ (self, stream):
        self.file = open(stream, 'r')
        self.currentLine = self.file.readline().split()
        self.buffer = self.file
        self.line = 0
        self.word = 0

    def read(self):
        '''
            Read() returns the next character or 65536 if the input is exhausted
        '''
        
        word = ''
        if self.word < len(self.currentLine):
            word = self.currentLine[self.word]
            self.word += 1
        else:
            self.currentLine = self.file.readline().split()
            self.word = 0
            if self.currentLine != []:
                word = self.currentLine[self.word]
            self.word += 1
        return word

    def peek(self):
        '''
            Peek() allows the scanner to read characters ahead without consuming them
        '''

        word = None
        if self.word < len(self.currentLine) - 1:
            word = self.currentLine[self.word + 1]
        return word

    def getpos(self):
        return self.word, self.line
    
    def setpos(self, word, line):
        '''
            Pos allows the scanner to get or set the reading position, which is initially 0
        '''
        self.word = word
        self.line = line

    def getString(self, beginning, end):
        '''
            GetString(beg, end) can be used to retrieve the text interval 
            [beg..end[ from the input stream, where beg and end are byte positions.
        '''
        print('soon')

class Token():
    def __init__(self, code, val, pos=None, charPos=None, line=None, col=None):
        self.code = code                   # token code (EOF has the code 0)
        self.val = val                     # token value
        self.pos = pos                     # token position in the source text // (in bytes starting at 0)
        self.charPos = charPos             # token position in the source text // (in characters starting at 0)
        self.line = line                   # line number (starting at 1)
        self.col = col                     # column number (starting at 1)

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

        any_atr = set()
        hexdigit = set('0123456789').union(set('ABCDEF'))
        noApostrophe  = any_atr.difference("'")
        letter = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        digit = set('0123456789')
        nodigit  = any_atr.difference(digit)
        noQuote  = any_atr.difference('"')

        self.ident = DFA('letter {letter|digit}')
        #self.string =  DFA('" {noQuote} "')
        #self.number =  DFA('digit {digit}')
        #self.char =  DFA("'noApostrophe'")

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
        character = {}
        Char = superDFA('char | CHR(number)')
        BasicSet = superDFA(['string | indent | Char[".." Char]', ])
        Set = superDFA([BasicSet, DFA('{(+|-)BasicSet}')])
        Set = superDFA([ident, DFA('='), Set, DFA('.')])
        while SetDecl.check():
            name, value = SetDecl.get()
            if name != None:
                character[name] = value
            else: 
                print('KEYWORDS error')

        return character

    def KEYWORDS(self):
        '''
            ["KEYWORDS" {KeyworDecl}]
            KeywordDecl = ident '=' string '.'
        '''
        keywords = {}
        keywordDecl = superDFA([ident, DFA('='), string, DFA('.')])
        while keywordDecl.check():
            name, value = keywordDecl.get()
            if name != None:
                keywords[name] = value
            else: 
                print('KEYWORDS error')

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
            print(token.val)
            if (token.val == 'CHARACTERS'):
                print('CHARACTERS started')
                self.characters = self.CHARACTERS()
                token = self.scan()
            if (token.val == 'KEYWORDS'):
                print('KEYWORDS started')
                self.keywords = self.KEYWORDS()
                token = self.scan()
            if (token.val == 'TOKENS'):
                print('TOKENS started')
                self.tokens = self.TOKENS()
                token = self.scan()
            if (token.val == 'END'):
                token = self.scan()
                if(token.val == (name+'.')):
                    print("succesfully exit")
                else:
                    print("unexpected END")
        else:
            print("unexpected compiler name")
    

    def definition(self, value):
        code = None
        if value == '':
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
    
    def scan(self):
        '''
            The method Scan() is the actual scanner. The parser calls it whenever it needs 
            the next token. Once the input is exhausted Scan() returns the end-of-file token, 
            which has the token number 0. For invalid tokens (caused by illegal token syntax 
            or by invalid characters) Scan() returns a special token kind, which normally causes
            the parser to report an error.
        '''
        word = self.buffer.read()
        if word == '':
            return self.scan()
        return Token(self.definition(word),word)

        
    def peek(self, args):
        '''
            Peek() can be used to read one or several tokens ahead without removing them from
            the input stream. With every call of Scan() (i.e. every time a token has been 
            recognized) the peek position is set to the scan position so that the first Peek()
            after a Scan() returns the first yet unscanned token.
        '''
    
    def resetPeek(self, args):
        '''
            The method ResetPeek() can be used to reset the peek position to the scan position
            after several calls of Peek().
        '''

def main():
    scanner = Scanner("test1.txt")
    scanner.COMPILER()
    #args = scanner.start()
    

main()