from utils.dfa import DFA

#CHARACTERS
upletter = DFA('Z!J!K!T!C!N!D!G!M!U!Q!F!Y!S!I!R!H!L!P!O!V!B!E!W!X!A')
downletter = DFA('b!l!u!x!s!z!a!j!g!q!k!r!p!i!m!d!w!e!f!t!o!y!h!n!v!c')
letter = DFA('Z!J!K!T!C!N!D!G!M!U!Q!F!Y!S!I!R!H!L!P!O!V!B!E!W!X!A')
digit = DFA('1!0!4!2!5!9!8!3!7!6')
hexdigit = DFA('1!0!B!E!4!2!5!9!8!C!A!3!7!D!6!F')
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

