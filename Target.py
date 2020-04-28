from utils.dfa import DFA
from utils.evaluate import evaluate, Node

#CHARACTERS
letter = DFA('n!F!m!q!z!M!A!P!b!B!t!c!E!l!y!j!V!h!p!O!r!u!U!H!w!Y!G!f!e!N!R!K!C!J!Q!i!D!a!d!x!W!o!S!Z!g!I!k!T!v!X!L!s')
digit = DFA('6!7!1!2!0!5!8!9!3!4')
tab = DFA(chr(9))
eol = DFA(chr(10))

#KEYWORDS
keywords = {}
keywords["while"] = "while"
keywords["do"] = "do"
keywords["if"] = "if"

#TOKENS
ident = DFA('letter{letter|digit}', {'letter': letter, 'digit': digit})
number = DFA('digit{digit}', {'digit': digit})

tokens = {'ident': (ident, 'A', [], True),'number': (number, 'A', [], False),}
file = open('./inputs/input1.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
evaluate(text, tokens, keywords)
