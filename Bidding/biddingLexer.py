import ply.lex as lex


def theLexer():
    tokens = (
        'BY',
        'ONE_NO_TRUMP',
        'ONE_CLUB',
        'WEAK_TWO',
        'EQUAL',
        'NUMBER',
        'DISTRIBUTION',
        'MINUS',
        'TILDE',
        'TEAM'
     )
    
    t_EQUAL      = r'='
    t_MINUS      = r'-'
    t_TILDE      = r'~'
    t_ignore  = ' \t\n'

    literals = [';', 'N', 'E', 'S', 'W']
    
    
    def t_TEAM(t):
        r'(NS|EW)'
        return t

    def t_BY(t):
        'BY'
        return t
    
    def t_ONE_NO_TRUMP(t):
        '1NT'
        return t
    
    def t_ONE_CLUB(t):
        '1C'
        return t
    
    def t_WEAK_TWO(t):
        'W2'
        return t
    
    def t_DISTRIBUTION(t):
        r'[(][0-9x]{4}[)]'
        return t
    
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)    
        return t
     
    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
     
    # Build the lexer
    lexer = lex.lex(debug=False)
    return lexer, tokens
