import generatePbnDataframe as g
import pandas as pd

def main():
    try:
        #df = g.getDataframe("reading_2018*.pbn")
        df = g.getDataframe("*.pbn")
        
#         for name in list(df):
#             print(name)
        
        def analyseNT(level):
            df2 = df[ (df['NS_BEST_SUIT'] == "NT") & (df['NS_MAX_TRICKS'] == level) ]
            df3 = df2.loc[:, 'NS_PTS']
            print( f"{level} NT with: {df3.mean(axis=0):.1f} pts, {len(df3)}" )
        
        def analyse(n, fits):
            for fit in fits:
                df2 = df[ (df['NS_MAX_TRICKS'] == n) & (df['NS_DOUBLE_DUMMY'] == fit) ]
                df3 = df2.loc[:, 'NS_PTS']
                print( f"{n} tricks with {fit}: {df3.mean(axis=0):.1f} pts, {len(df3)}" )
        
#         for n in range(7,14):
#             analyseNT(n)
#         g.display(df, ['NS_MAX_TRICKS', 'NS_DOUBLE_DUMMY'])
        df2 = df[['N_PTS', 'N_DISTRIBUTION']]
        df2 = df2[ (df2['N_PTS'] >= 3) & (df2['N_PTS'] <= 10)]
        df2['SORTED_DISTRIBUTION'] = df2.apply(lambda row: sorted(row.loc['N_DISTRIBUTION'])[2:4]==[5,6], axis=1)
        df3 = df2.groupby('SORTED_DISTRIBUTION').count()
        print(df3)
#        g.display(df2, ['N_PTS', 'N_DISTRIBUTION', 'SORTED_DISTRIBUTION'])
        
        
    except Exception as e:
        print(e)

main()

# BOARD
# DEALER
# VULNERABLE
# DEAL
# OPTIMUM_SCORE
# DOUBLE_DUMMY_TRICKS
# OPTIMUM_RESULT_TABLE
# SCORE_TABLE
# SCORING
# NS_DOUBLE_DUMMY
# EW_DOUBLE_DUMMY
# N_PTS
# E_PTS
# S_PTS
# W_PTS
# NS_PTS
# EW_PTS
# N_DISTRIBUTION
# E_DISTRIBUTION
# S_DISTRIBUTION
                                  # W_DISTRIBUTION
# NS_DISTRIBUTION
# EW_DISTRIBUTION
# NS_BEST_SUIT
# NS_MAX_TRICKS
# EW_BEST_SUIT
# EW_MAX_TRICKS

# 7 tricks in NT with: 20.2 pts, 275
# 8 tricks in NT with: 21.9 pts, 387
# 9 tricks in NT with: 23.9 pts, 455
# 10 tricks in NT with: 25.5 pts, 433
# 11 tricks in NT with: 27.5 pts, 352
# 12 tricks in NT with: 29.3 pts, 295
# 13 tricks in NT with: 30.8 pts, 161

# 8 card fits:
#      7 tricks => 17.4 pts
#      8 tricks => 19.4 pts
#      9 tricks => 21.3 pts
#     10 tricks => 23.0 pts
#     11 tricks => 25.1 pts
#     12 tricks => 26.4 pts
#     13 tricks => 28.4 pts

# 7 tricks with 4-4: 17.5 pts, 460
# 7 tricks with 5-3: 17.5 pts, 345
# 7 tricks with 6-2: 16.6 pts, 114
# 7 tricks with 7-1: 15.6 pts, 17
# 7 tricks with 8-0: nan pts, 0
# 
# 8 tricks with 4-4: 19.4 pts, 526
# 8 tricks with 5-3: 19.5 pts, 343
# 8 tricks with 6-2: 19.0 pts, 136
# 8 tricks with 7-1: 18.6 pts, 25
# 8 tricks with 8-0: 19.5 pts, 2
# 
# 9 tricks with 4-4: 21.3 pts, 486
# 9 tricks with 5-3: 21.3 pts, 341
# 9 tricks with 6-2: 21.2 pts, 116
# 9 tricks with 7-1: 20.2 pts, 16
# 9 tricks with 8-0: 20.3 pts, 3
# 
# 10 tricks with 4-4: 23.1 pts, 393
# 10 tricks with 5-3: 23.0 pts, 229
# 10 tricks with 6-2: 22.9 pts, 83
# 10 tricks with 7-1: 23.1 pts, 18
# 10 tricks with 8-0: nan pts, 0
# 
# 11 tricks with 4-4: 25.1 pts, 227
# 11 tricks with 5-3: 25.0 pts, 144
# 11 tricks with 6-2: 25.1 pts, 63
# 11 tricks with 7-1: 25.2 pts, 13
# 11 tricks with 8-0: 24.0 pts, 2
# 
# 12 tricks with 4-4: 26.6 pts, 106
# 12 tricks with 5-3: 26.6 pts, 56
# 12 tricks with 6-2: 25.5 pts, 15
# 12 tricks with 7-1: 24.7 pts, 6
# 12 tricks with 8-0: nan pts, 0
# 
# 13 tricks with 4-4: 28.6 pts, 21
# 13 tricks with 5-3: 28.7 pts, 6
# 13 tricks with 6-2: 28.0 pts, 5
# 13 tricks with 7-1: 25.0 pts, 1
# 13 tricks with 8-0: 29.0 pts, 1
