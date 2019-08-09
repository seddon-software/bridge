import ply.lex as lex
#import ply.yacc as yacc
import pandas as pd
#import os
import biddingLexer as bl
import biddingParser as bp

pd.set_option('display.width', None)        # None means all data displayed
pd.set_option('display.max_rows', None)


queriesAsString = '''E = 15-20 ; S = 5 - 13 ; 
          N = (5332);
'''
# queriesAsString = '''N = (5251);'''


def query(df, queries):
    for q in queries:
        df = df[eval(q)]
    return df


lexer, tokens = bl.theLexer()
parser = bp.theParser(lexer, tokens)

queries = parser.parse(queriesAsString)
df = pd.read_msgpack('bridge_results.msg')
df = query(df, queries)
print(df)
print(f"query: {queriesAsString.strip()}")
print(f"records found: {len(df)}")
