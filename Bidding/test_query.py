import pandas as pd

pd.set_option('display.width', None)        # None means all data displayed
pd.set_option('display.max_rows', None)

d = ('5512',)
l = [c for c in d[0]]
x = tuple(l)

def weakTwo(df, by):
    def select(row):
        return (row[f'{by}_DISTRIBUTION'][0]==6 or 
                row[f'{by}_DISTRIBUTION'][1]==6) and (
                row[f'{by}_PTS'] >= 5 and row[f'{by}_PTS'] <= 9)
    values = df.apply(select, axis=1).values
    df = df.assign(WEAK_TWO=values)
    df = df[df['WEAK_TWO']==True]
    return df

def f():
    df = pd.read_msgpack('bridge_results.msg')
    df = eval('weakTwo(df, "W")')
    print(df)
f()

# def f():
#     df = pd.read_msgpack('bridge_results.msg')
#     q = '''df.assign(z=eval("df.apply(lambda row: (row['W_DISTRIBUTION'][0])==6 or (row['W_DISTRIBUTION'][1])==6, axis=1)").values)'''
#     df = eval(q)
#    #df = df[df['z']==True][-10:]
#     df = eval(q)[eval(q)['z']==True]
#     print(df)
# f()