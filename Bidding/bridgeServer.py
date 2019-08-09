from flask import Flask, request
from flask import jsonify
import pandas as pd
import urllib.parse
import biddingLexer as bl
import biddingParser as bp

pd.set_option('display.width', None)        # None means all data displayed
pd.set_option('display.max_rows', None)

app = Flask(__name__, static_url_path='')
lexer, tokens = bl.theLexer()
parser = bp.theParser(lexer, tokens)


def queryDataframe(queries):
    global data
    df = pd.read_msgpack('bridge_results.msg')
    for q in queries:
        df = eval(q)
    print(df[-10:])
    df = df[['BOARD', 'DEALER', 'VULNERABLE', 'SCORE_TABLE', 'DEAL']]
    data = df.values.tolist()

@app.route("/")
def root():
    return app.send_static_file('bridge.html')

df = pd.read_msgpack('bridge_results.msg')
df = df[['BOARD', 'DEALER', 'VULNERABLE', 'SCORE_TABLE', 'DEAL']]
data = df.values.tolist()
currentHand = data.pop()
data = []

def dealer(df, by):
    values = df.apply(lambda row: row['DEALER'] == by, axis=1).values
    df = df.assign(NEW_DEALER=values)
    df = df[df['NEW_DEALER']==True]
    return df
        
def vulnerable(df, by):
    values = df.apply(lambda row: row['VULNERABLE'] == by, axis=1).values
    df = df.assign(NEW_VULNERABLE=values)
    df = df[df['NEW_VULNERABLE']==True]
    return df
        
def weakTwo(df, by):
    def select(row):
        return (row[f'{by}_DISTRIBUTION'][0]==6 or 
                row[f'{by}_DISTRIBUTION'][1]==6) and (
                row[f'{by}_PTS'] >= 5 and row[f'{by}_PTS'] <= 9)
    values = df.apply(select, axis=1).values
    df = df.assign(WEAK_TWO=values)
    df = df[df['WEAK_TWO']==True]
    return df

def exact_distribution(df, by, d):
    def select(row):
        target = row[f'{by}_DISTRIBUTION']
        query = tuple([c for c in d[1:-1]])
        comparison = [str(t)==q for t, q in zip(target, query) if 'x' not in q]
        return False not in comparison

    values = df.apply(select, axis=1).values
    df = df.assign(NEW_EXACT_DISTRIBUTION=values)
    df = df[df['NEW_EXACT_DISTRIBUTION']==True]
    return df
    
def unordered_distribution(df, by, d):
    def select(row):
        target = list(row[f'{by}_DISTRIBUTION']) 
        query = [int(c) for c in d if c not in '()x']
        result = True
        try:
            for n in query:
                target.remove(n)
        except ValueError as e:
            result = False
        return result

    values = df.apply(select, axis=1).values
    df = df.assign(NEW_UNORDERED_DISTRIBUTION=values)
    df = df[df['NEW_UNORDERED_DISTRIBUTION']==True]
    return df
    
    
def send(item):
    message = jsonify({
                    'board'      : item[0],
                    'dealer'     : item[1],
                    'vulnerable' : item[2],
                    'scoreTable' : item[3],
                    'deal'       : item[4],
                    'record'     : len(data)
                    })
    print(message)
    return message
    
@app.route('/resend')
def resendHands():
    global currentHand
    return send(currentHand)

import random

@app.route('/hands')
def getHands():
    global currentHand
    
    print(f"Hand No: {len(data)}")
    if data:         
        currentHand  = data.pop()
    return send(currentHand)

@app.route('/query')
def get_query():
    queriesAsBytes = request.query_string
    queriesAsString = queriesAsBytes.decode()
    queriesAsString = urllib.parse.unquote(queriesAsString)
    queries = parser.parse(queriesAsString)
    if not queries:
        return "syntax error in query", 406
    
    queryDataframe(queries)
    print(queries)
    if data: 
        random.shuffle(data)
    print(len(data))
#    return f'{len(data)}'
    return getHands()
    
if __name__ == "__main__":
    print("serving on localhost, port 5000")
    app.debug = True
    app.run(host='192.168.0.89',port=7003)

