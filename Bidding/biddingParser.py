import ply.yacc as yacc

'''
Examples of queries (spaces ignored):
    WEAK_TWO BY N;
    S = 10-15;
    W = (5323);    # 5 spades, 3 hearts, 2 diamonds and 3 clubs
    W = (53xx);    # 5 spades and 3 hearts
    E ~ (52xx);    # 5-2 in any suits
'''

def theParser(lexer, tokens): 
    pts = {'N':'N_PTS', 'E':'E_PTS', 'S':'S_PTS', 'W':'W_PTS'}
    
    def p_queries(p):
        '''queries : queries query
                   | query'''
        if len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = [p[1]]
    
    def p_query(p):
        '''query : point_range
                 | exact_distribution 
                 | unordered_distribution 
                 | dealer
                 | vulnerable
                 | weak_two
                 | one_no_trump
                 | one_club'''
        p[0] = p[1]
    
#    weakTwo(df, "W")
    def p_unordered_distribution(p):
        '''unordered_distribution : player TILDE DISTRIBUTION ';' '''
        p[0] = f"unordered_distribution(df, '{p[1]}', '{p[3]}')"
        
    def p_exact_distribution(p):
        '''exact_distribution : player EQUAL DISTRIBUTION ';' '''
        p[0] = f"exact_distribution(df, '{p[1]}', '{p[3]}')"
    
    def p_one_no_trump(p):
        '''one_no_trump : ONE_NO_TRUMP BY player ';' '''
        p[0] = f"oneNoTrump(df, '{p[3]}')"
        
    def p_one_club(p):
        '''one_club : ONE_CLUB BY player ';' '''
        p[0] = f"oneClub(df, '{p[3]}')"
        
    def p_weak_two(p):
        '''weak_two : WEAK_TWO BY player ';' '''
        p[0] = f"weakTwo(df, '{p[3]}')"
    
    def p_dealer(p):
        '''dealer : player ';' '''
        p[0] = f"dealer(df, '{p[1]}')"
        
    def p_vulnerable(p):
        '''vulnerable : TEAM ';' '''
        p[0] = f"vulnerable(df, '{p[1]}')"
        
    def p_point_range(p):
        '''point_range : player EQUAL range ';' '''
        player = p[1]
        range_ = p[3]
        p[0] = f"df[(df['{pts[player]}'] >= {range_[0]}) & (df['{pts[player]}'] <= {range_[1]})]"
    
    def p_range(p):
        'range : NUMBER MINUS NUMBER'
        p[0] = [p[1], p[3]]  
    
    def p_player(p):
        '''player : 'N' 
                  | 'E' 
                  | 'S' 
                  | 'W' '''
        p[0] = p[1]
              
    def p_error(p):
        print("Syntax error in input!")
    
    parser = yacc.yacc(debug=False)
    return parser
