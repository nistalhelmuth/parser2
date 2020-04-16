class Scanner():
    '''
        The main class of the compiler (see Section 3.5) has to create a scanner 
        object and pass it either an input stream or the name of a file from where 
        the tokens should be read. The scanner's input buffer is exported in the 
        field buffer. It can be used to access the input text at random addresses 
        (see Section 3.4.3).
    '''

    def __init__(self, args):
        self.buffer = Buffer()
        self.file = open('test1.txt','3')
        any_atr = set(string.printable)
        letter = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        digit = set('0123456789')
        hexdigit = set('0123456789').union(set('ABCDEF'))
        nodigit  = any_atr.difference(digit)

        #ident = letter {letter | digit}.       l.(l|d)*    DFA("letter{letter|digit}")
        #number = digit {digit}.                d.d         DFA("digit.digit") 
        #string = '"' {anyButQuote} '"'.        ".q*."      DFA('"{'+any_atr.difference(set('""'))+'}"')
        #char = '\'' anyButApostrophe '\''.     '.a.'       DFA("'"+any_atr.difference(set("'"))+"'")
        
        token = self.scan()
        if(token.val == 'COMPILER'):
            
            '''
                "COMPILER" ident
                scanner specification
            '''
            token = self.scan()
            if (not ident.check(token.val)):
                self.file.close()
                print("error line:", pointer)
                break;

                token = self.scan()
            if(token.val == 'CHARACTERS'):
                '''
                    ["CHARACTERS" {SetDecl}]
                    SetDecl = ident '=' Set.
                    Set = BasicSet { ('+'|'-') BasicSet }.
                    BasicSet = string | ident | Char [".." Char].
                    Char = char | "CHR" '(' number ')'.
                '''
                token = self.scan()
            if(token.val == 'KEYWORDS'):
                '''
                    ["KEYWORDS" {KeyworDecl}]
                    KeywordDecl = ident '=' string '.'
                '''
                #ident.check(token)
                #token == '='
                #string.check(token)
                token = self.scan()
            if(token.val == 'TOKENS'):
                '''
                    ["TOKENS" {TokenDecl}]
                    TokenDecl = ident ['=' TokenExpr ] ["EXCEPT KEYWORDS"] '.'.
                    TokenExpr = TokenTerm {'|' TokenTerm }.
                    TokenTerm = TokenFactor {TokenFactor}
                    TokenFactor = Symbol
                    | '(' TokenExpr ')'
                    | '[' TokenExpr ']'
                    | '{' TokenExpr '}'.
                    Symbol = ident | string | char
                '''
                token = self.scan()
            if(token.val == 'END'):
                '''
                    "END" ident '.'.
                '''
                token = self.scan()
                token = self.scan()

        self.file.close()
    
    def scan(self, args):
        '''
            The method Scan() is the actual scanner. The parser calls it whenever it needs 
            the next token. Once the input is exhausted Scan() returns the end-of-file token, 
            which has the token number 0. For invalid tokens (caused by illegal token syntax 
            or by invalid characters) Scan() returns a special token kind, which normally causes
            the parser to report an error.
        '''
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

class Token():
    def __init__(self, name, val, pos=None, charPos=None, line=None, col=None):
        self.name = name                    # token code (EOF has the code 0)
        self.val = val                     # token value
        self.pos = pos                     # token position in the source text // (in bytes starting at 0)
        self.charPos = charPos                 # token position in the source text // (in characters starting at 0)
        self.line = line                    # line number (starting at 1)
        self.col = col                     # column number (starting at 1)

class Buffer():
    '''
        This is an auxiliary class that is used by the scanner (and possibly by 
        other classes) to read the source stream into a buffer and retrieve 
        portions of it:
    '''
    def __init__ (self, stream):
        self.EOF = char.MaxValue + 1;
    #int
    def Read():
    '''
        Read() returns the next character or 65536 if the input is exhausted
    '''

    #int
    def Peek():
    '''
        Peek() allows the scanner to read characters ahead without consuming them
    '''

    #int
    def Getpos():

    def Setpos():
    '''
        Pos allows the scanner to get or set the reading position, which is initially 0
    '''
    #string
    def GetString(int beg, int end):
    '''
        GetString(beg, end) can be used to retrieve the text interval 
        [beg..end[ from the input stream, where beg and end are byte positions.
    '''

#class Parser():
#class Errors():

def main():
    scanner = Scanner("archivo")
    #parser = Parser(scanner)
    #parser.Parse():
    #print("errors")