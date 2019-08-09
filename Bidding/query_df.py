import pandas as pd
#import generatePbnDataframe as pdb
import os
pd.set_option('display.width', None)        # None means all data displayed
pd.set_option('display.max_rows', None)

def query(df, condition=None):
    return df[condition]

df = pd.read_msgpack('bridge_results.msg')
print(list(df))



# z = query(df, df['VULNERABLE'] == 'NS')
# print(type(z))
t = (5, 3, 3, 2)
z = query(df, df['N_DISTRIBUTION'] == t)
print(z)
# print( query(df, df['DEALER'] == 'S'))
# print( query(df, (df['N_PTS'] > 14) & (df['N_PTS'] < 16) ))
# def reduceScoreTable(row):
#     scoreTable = row['SCORE_TABLE'].strip()
#     scores = scoreTable.split('\n')
#     scores.pop(0)   # remove headings
#     scoreTable = []
#     for score in scores:
#         score = score.split()
#         score.pop(0)    # pop NS pair number
#         score.pop(0)    # pop EW pair number
#         scoreTable.append(score)
#     return scoreTable
#     
# df['SCORE_TABLE'] = df.apply(reduceScoreTable, axis=1)

#print(df['SCORE_TABLE'])

