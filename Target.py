from utils.dfa import DFA
from utils.evaluate import evaluate, Node

#CHARACTERS
upletter = DFA('I!C!B!F!M!L!E!S!X!V!Y!Z!W!G!P!Q!O!K!H!N!A!T!J!R!U!D')
downletter = DFA('y!o!v!t!d!m!x!l!r!h!n!z!g!j!c!s!e!q!p!a!u!w!b!i!f!k')
letter = DFA('I!C!B!F!M!L!E!S!X!V!Y!Z!W!G!P!Q!O!K!H!N!A!T!J!R!U!D')
digit = DFA('6!8!0!2!7!1!9!3!5!4')
hexdigit = DFA('6!A!E!C!B!F!8!0!2!7!1!9!3!5!4!D')
sign = DFA('-!+')

#KEYWORDS
keywords = {}
keywords["while"] = "while"
keywords["do"] = "do"
keywords["if"] = "if"
keywords["switch"] = "switch"

#TOKENS
digit = DFA('digit', {'digit': digit})
ident = DFA('letter{letter|digit}', {'letter': letter, 'digit': digit})
number = DFA('digit{digit}', {'digit': digit})
signnumber = DFA('[sign]digit{digit}', {'sign': sign, 'digit': digit})

tokens = {'digit': (digit, 'A', []),'ident': (ident, 'A', []),'number': (number, 'A', []),'signnumber': (signnumber, 'A', []),}
file = open('inputs/input1.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
evaluate(text, tokens)
