from utils.dfa import DFA
from utils.evaluate import evaluate, Node

#CHARACTERS
upletter = DFA('U!C!Z!E!A!F!P!D!H!W!R!J!L!N!V!T!Q!G!B!X!M!I!Y!K!O!S')
downletter = DFA('o!q!s!j!h!a!r!g!b!y!w!x!p!z!i!l!t!n!m!f!u!v!c!d!e!k')
letter = DFA('U!C!Z!E!A!F!P!D!H!W!R!J!L!N!V!T!Q!G!B!X!M!I!Y!K!O!S')
digit = DFA('1!8!6!7!5!2!0!4!3!9')
hexdigit = DFA('1!8!6!C!7!E!A!F!5!2!0!4!D!3!9!B')
sign = DFA('+!-')

#KEYWORDS
keywords = {}
keywords["while"] = "while"
keywords["do"] = "do"
keywords["if"] = "if"
keywords["switch"] = "switch"

#TOKENS
digits = DFA('digit{digit}', {'digit': digit})
letters = DFA('letter', {'letter': downletter})
ident = DFA('letter{letter|digit}', {'letter': letter, 'digit': digit})
number = DFA('digit{digit}', {'digit': digit})
signnumber = DFA('[sign]digit{digit}', {'sign': sign, 'digit': digit})

file = open('inputs/input1.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()

tokens = {'digit': (digits, 'A', []), 'letter': (letters, 'A', [])}

evaluate(text, tokens)
'''
start = copy.deepcopy(tokens)
currentValue = text
nextValue = text
last = {}
pull = []
while currentValue.next != None:
    for name in tokens.keys():
        token = tokens[name]
        newState, accepted = token[0].slowCheck(nextValue.value, token[1])
        if newState != None:
            token[2].append(nextValue.value)
            tokens[name] = (token[0], newState, copy.deepcopy(token[2]))
            if accepted:
                test = nextValue.value
                last = {
                    'name': name,
                    'text': copy.deepcopy(token[2]),
                    'token': (token[0], newState, token[2])
                }
        else:
            pull.append(name)

    for name in pull:
        del tokens[name]
        pull = []

    
    if len(tokens) == 0:
        if last != {}:
            test = ''
            for value in last['text']:
                if value == currentValue.value:
                    currentValue = currentValue.next
                    test = test + value
            print('TOKEN FOUND', last)
            last = {}
        else:
            print('ERORR WITH', currentValue.value)
            currentValue = currentValue.next
        tokens = copy.deepcopy(start)
        nextValue = currentValue
    else:
        nextValue = nextValue.next
'''