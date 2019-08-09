import re, glob, os
import calendar
from collections import deque
import pandas as pd
from functools import partial
import scores

pd.set_option('display.width', None)        # None means all data displayed
pd.set_option('display.max_rows', None)

os.chdir("results")

BOARD = r'Board\s+["](\d+)["]'
DEALER = r'Dealer\s+["](.*)?["]'
VULNERABLE = r'Vulnerable\s+["](.*)?["]'
DEAL = r'Deal\s+["][NESW]:(.*)?["]'
OPTIMUM_SCORE = r'OptimumScore\s+["](.*)["]'
DOUBLE_DUMMY_TRICKS = r'DoubleDummyTricks\s+["](.*)["]'
OPTIMUM_RESULT_TABLE = r'OptimumResultTable([\s\S]*)'
SCORE_TABLE = r'ScoreTable([\s\S]*)'
SCORING = r'Scoring[^"]*["]([^"]*)["]'

def getData(fileName):
    allLines = []
    try:
        with open(fileName, "r") as f:
            allLines = f.readlines()
    except IOError as e:
        print(f"1: {fileName}: {e}")
    except UnicodeDecodeError as e:
        print(f"2: {fileName}: {e}")
    finally:
        return allLines
    
def extractData(df, data, fileName):
    # deal has hands with dealer first; hands need to be rotated to make North first
    def rotateDeal(hands, dealer):
        i = "NESW".find(dealer)
        d = deque(hands)
        d.rotate(i)
        return list(d)

    def appendToDf(h):
        nonlocal df
        keys = list(h.keys())
        values = list(h.values())
        row = {k:v for k,v in zip(keys, values)}
        if df is None:
            df = pd.DataFrame(columns=keys)
        df = df.append(row, ignore_index=True)

    def search(key):
        pattern = f"{eval(f'{key}')}"
        result = re.search(pattern, item, re.RegexFlag.MULTILINE)
        if result:
            h[key] = result.group(1)

    dataAsString = "".join(data)
    dataAsList = dataAsString.split("[")
    h = {}

    expectedHeadings = ['BOARD', 'DEALER', 'VULNERABLE', 'DEAL', 'OPTIMUM_SCORE', 'DOUBLE_DUMMY_TRICKS', 'OPTIMUM_RESULT_TABLE', 'SCORE_TABLE', 'SCORING']
    for item in dataAsList:
        try:
            '''search may return None and this is not an error, however, by the end of
               this loop all the fields should have been found.  That's why I check the headings
               against expected headings, in case some are missing
            '''
            if "SCORING" in h:
                appendToDf(h)
                h = {}
            search('BOARD')
            search('DEALER')
            search('VULNERABLE')
            search('DEAL')
            search('OPTIMUM_SCORE')
            search('DOUBLE_DUMMY_TRICKS')
            search('OPTIMUM_RESULT_TABLE')
            search('SCORE_TABLE')
            search('SCORING')
        except Exception as e:
            print(f"3: {fileName}: {e}")
            return None
    try:
        headings = list(df)
        if headings != expectedHeadings: raise Exception("Some data missing")
    except Exception as e:
        print(f"4: {fileName}: {e}")
        return None
    return df

def checkFilesForDoubleDummyInformation(pattern):
    def hasDoubleDummyAnalysis():
        # this checks the data has "double dummy" info available and not zeroed out
        data = getData(fileName)
        try:
            result = re.search(f'{DOUBLE_DUMMY_TRICKS}', ", ".join(data))
            if result:
                if result.group(1) == "00000000000000000000": 
                    print(f"*** error in file", end=", ")
                    return False
        except Exception as e:
            print(f"5: {e}")
        return bool(result)
    listOfFiles = glob.glob(pattern)
    listOfFiles.sort()
    for fileName in listOfFiles:
        if not hasDoubleDummyAnalysis():
            year = fileName[8:12]
            month_idx = int(fileName[12:14])
            month = calendar.month_name[month_idx]
            day = fileName[14:16]
            print(f"No double dummy analysis: {day} {month} {year} ")

def getDataframe(pattern):
    try:
        def rotateDeal(hands, dealer):
            i = "NESW".find(dealer)
            d = deque(hands)
            d.rotate(i)
            return list(d)
    
        def PTS(row):
            deal = row['DEAL']
            pts = []
            for hand in deal:
                pts.append(HCPs(hand))
            return pts
                  
        def HCPs(hand):
            pts = 0
            for suit in hand:
                if 'A' in suit: pts += 4
                if 'K' in suit: pts += 3
                if 'Q' in suit: pts += 2
                if 'J' in suit: pts += 1
            return pts
    
        def distribution(deal):
            handPatterns = []
            for hand in deal:
                suitLengths = []
                suits = hand.split(".")  
                for suit in suits:
                    suitLengths.append(len(suit))
                handPatterns.append(suitLengths)
            return handPatterns
        
        def rotateDealToMakeNorthFirst(row):
            def rotate(theList, dealer):
                i = "NESW".find(dealer)
                return theList[-i:] + theList[:-i]
            return rotate(row['DEAL'].split(), row['DEALER'])
    
        def doubleDummySuitLength(suitKey, distributionKey, row):
            suit = row[suitKey]
            if suit == 'NT':
                return "-"
            i = "SHDC".find(suit)
            return row[distributionKey][i]
    
        listOfFiles = glob.glob(pattern)
        listOfFiles.sort()
        df = None
                
        for fileName in listOfFiles:
            print(f"{fileName} : DONE")
            data = getData(fileName)
            if not data: continue
            
            df2 = extractData(df, data, fileName)
            if df2 is None: continue
            df = df2
        if df is None: raise Exception("Fileset has generated an empty dataframe")
    
        def suitFit(distributionKey, row):
            return max(row[distributionKey])
    
        def dealToArrays(row):
            result = []
            for hand in row['DEAL']:
                suits = hand.split(".")
                theSuits = []
                for suit in suits:
                    cards = [card for card in suit]
                    theSuits.append(cards)
                result.append(theSuits)
            return result
    
        def augmentScoreTable(row):                
            scoreTable = row['SCORE_TABLE'].strip()
            dealer = row['DEALER']
            vulnerable = row['VULNERABLE']
            table = scoreTable.split('\n')
            table.pop(0)   # remove headings
            scoreTable = []
            for entry in table:
                entry = entry.split()
                entry.pop(0)    # pop NS pair number
                entry.pop(0)    # pop EW pair number
                theScores = scores.getScores(entry, vulnerable)
                entry.extend(theScores)
                scoreTable.append(entry)
            return scoreTable
            
        df.dropna(axis=0, inplace=True)
        df['DEAL'] = df.apply(rotateDealToMakeNorthFirst, axis=1)
        df['DEAL2'] = df.apply(dealToArrays, axis=1)
        #df['DOUBLE_DUMMY_TRICKS'] = df.apply(lambda row:[int(c, 16) for c in row["DOUBLE_DUMMY_TRICKS"]], axis=1)
        #SUITS = ["NT","S","H","D","C"]
        #df['NS_DOUBLE_DUMMY'] = df.apply(lambda row: {key:(n+s)/2.0 for key,n,s in zip(SUITS, row["DOUBLE_DUMMY_TRICKS"][ 0: 5], row["DOUBLE_DUMMY_TRICKS"][ 5:10])}, axis=1)
        #df['EW_DOUBLE_DUMMY'] = df.apply(lambda row: {key:(e+w)/2.0 for key,e,w in zip(SUITS, row["DOUBLE_DUMMY_TRICKS"][10:15], row["DOUBLE_DUMMY_TRICKS"][15:20])}, axis=1)
        df[['N_PTS', 'E_PTS', 'S_PTS', 'W_PTS']] = df.apply(PTS, axis=1, result_type='expand')
        #df[['NS_PTS', 'EW_PTS']] = df.apply(PTS, axis=1, result_type='expand')
        df[['N_DISTRIBUTION','E_DISTRIBUTION','S_DISTRIBUTION','W_DISTRIBUTION']] = df.apply(lambda row: distribution(row['DEAL']), axis=1, result_type='expand')
        #df['NS_DISTRIBUTION'] = df.apply(lambda row: [n+s for n,s in zip(row['N_DISTRIBUTION'],row['S_DISTRIBUTION'])], axis=1)
        #df['EW_DISTRIBUTION'] = df.apply(lambda row: [e+w for e,w in zip(row['E_DISTRIBUTION'],row['W_DISTRIBUTION'])], axis=1)
        #df['NS_FIT_LENGTH'] = df.apply(partial(suitFit,'NS_DISTRIBUTION'), axis=1)
        #df['EW_FIT_LENGTH'] = df.apply(partial(suitFit,'EW_DISTRIBUTION'), axis=1)
#         df['NS_DOUBLE_DUMMY_SUIT'] = df.apply(lambda row: max(row['NS_DOUBLE_DUMMY'], key=row['NS_DOUBLE_DUMMY'].get), axis=1)
#         df['NS_DOUBLE_DUMMY_TRICKS'] = df.apply(lambda row: row['NS_DOUBLE_DUMMY'][row['NS_DOUBLE_DUMMY_SUIT']], axis=1)
#         df['EW_DOUBLE_DUMMY_SUIT'] = df.apply(lambda row: max(row['EW_DOUBLE_DUMMY'], key=row['EW_DOUBLE_DUMMY'].get), axis=1)
#         df['EW_DOUBLE_DUMMY_TRICKS'] = df.apply(lambda row: row['EW_DOUBLE_DUMMY'][row['EW_DOUBLE_DUMMY_SUIT']], axis=1)    
#         df['NS_DOUBLE_DUMMY_SUIT_LENGTH'] = df.apply(partial(doubleDummySuitLength,'NS_DOUBLE_DUMMY_SUIT','NS_DISTRIBUTION'), axis=1)
#         df['EW_DOUBLE_DUMMY_SUIT_LENGTH'] = df.apply(partial(doubleDummySuitLength,'EW_DOUBLE_DUMMY_SUIT','EW_DISTRIBUTION'), axis=1)
        df['SCORE_TABLE'] = df.apply(augmentScoreTable, axis=1)

    except Exception as e:
        print(f"6: rethrow")
        raise
    # remove any entries where scoring != MP
    df = df[ df['SCORING'] == 'MP']
    df = df.drop(columns=["DEAL", "OPTIMUM_SCORE", "DOUBLE_DUMMY_TRICKS", "OPTIMUM_RESULT_TABLE", 'SCORING'])
    df.rename(columns={'DEAL2':'DEAL'}, inplace=True)
    return df

def display(df, columns):
    # pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 100)
    pd.set_option('max_colwidth',80)
    pd.set_option('display.large_repr', 'info')
    df2 = df[columns] 
    print(df2.to_string(index=False, header=True))

if __name__ == "__main__":
    try:
        pattern = "laneend_*.pbn"
#        pattern = "reading_201012*_1.pbn"
#        pattern = "reading_20101230_1.pbn"
#        pattern = "*.pbn"
        df = getDataframe(pattern)
        df.to_msgpack('../bridge_results.msg')
        print(df)
    except Exception as e:
        print(f"7: {e}")
