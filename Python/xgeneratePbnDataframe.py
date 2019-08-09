import re, glob, os
import calendar
from collections import Counter
from collections import deque
import pandas as pd

os.chdir("results")

BOARD = r'[[]Board\s+["](\d+)["]'
DEAL = r'[[]Deal\s+["]([NESW]):(.*)["][]]'
DOUBLE_DUMMY_TRICKS = r'[[]DoubleDummyTricks\s+["](.*)["]'

pd.set_option('display.width', 1000)

def getData(fileName):
    allLines = []
    try:
        with open(fileName, "r") as f:
            allLines = f.readlines()
    except IOError as e:
        print(f"{fileName}: {e}")
    except UnicodeDecodeError as e:
        print(f"{fileName}: {e}")
    finally:
        return allLines
    
def extractData(data, fileName):
    # this strips out everything except "board", "deal" and "double dummy" info
    # deal has hands with dealer first; this routine rotates the list so North is first
    
    def rotateDeal(hands, dealer):
        i = "NESW".find(dealer)
        d = deque(hands)
        d.rotate(i)
        return list(d)

    results = []
    for d in data:
        try:
            result = re.search(f'{BOARD}', d)
            if result:
                h = {}
                h['board'] = result.group(1)
    
            result = re.search(f'{DEAL}', d)
            if result: 
                dealer = result.group(1)
                hands = result.group(2)
                hands = hands.split()
                hands = rotateDeal(hands, dealer)
                h['dealer'] = dealer
                h['deal'] = hands
            
            result = re.search(f'{DOUBLE_DUMMY_TRICKS}', d)
            if result: 
                tricks = result.group(1)
                if tricks == "00000000000000000000": raise Exception("double dummy information in error")
                h['tricks'] = tricks
                results.append(h)
        except Exception as e:
            print(f"{fileName}: {e}")
            return None
    return results

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
            print(e)
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
    def HCPs(hand):
        pts = 0
        for suit in hand:
            if 'A' in suit: pts += 4
            if 'K' in suit: pts += 3
            if 'Q' in suit: pts += 2
            if 'J' in suit: pts += 1
        return pts

    def distribution(hand):
        suitLengths = []
        for suit in hand:
            suitLengths.append(len(suit))
        return suitLengths

    def best(allSuits):
        level = 0
        bestSuit = {}
        for key in allSuits:
            if allSuits[key] > level: 
                level = allSuits[key]
                bestSuit = {key:allSuits[key]}
        suit = list(bestSuit.keys())[0]
        tricks = list(bestSuit.values())[0]
        return suit, tricks
        
    listOfFiles = glob.glob(pattern)
    listOfFiles.sort()
    columns = ['dealer','ns_pts','ns_tricks','ns_suit','ns_trumps','ew_pts','ew_tricks','ew_suit','ew_trumps']
    columns.extend(['n_pts', 'e-pts', 's_pts', 'w_pts'])
    df = pd.DataFrame(columns=columns)       
            
    for fileName in listOfFiles:
        data = getData(fileName)
        if not data: continue
        
        results = extractData(data, fileName)
        if not results: continue
        for result in results:
            dealer = result['dealer']

            tricks_NSHDC = [int(c, 16) for c in result['tricks']]
            hands = result['deal']
            suits_NESW = [distribution(hand.split(".")) for hand in hands]
            pts_for_NESW = [HCPs(hand.split(".")) for hand in hands]
            
            t = tricks_NSHDC
            NS_tricks = {key:(n+s)/2.0 for key,n,s in zip(["NT","S","H","D","C"], t[ 0: 5], t[ 5:10])}
            EW_tricks = {key:(e+w)/2.0 for key,e,w in zip(["NT","S","H","D","C"], t[10:15], t[15:20])}

            s = suits_NESW
            NS_trumps = {key:f"{N}-{S}" for key,N,S in zip(["S","H","D","C"],s[0], s[2])}
            EW_trumps = {key:f"{E}-{W}" for key,E,W in zip(["S","H","D","C"],s[1], s[3])}
            
            ns_suit, ns_tricks = best(NS_tricks)
            ew_suit, ew_tricks = best(EW_tricks)
            ns_trumps = "-" if ns_suit == "NT" else NS_trumps[ns_suit]
            ew_trumps = "-" if ew_suit == "NT" else EW_trumps[ew_suit]

            p = pts_for_NESW
            ns_pts = p[0] + p[2]
            ew_pts = p[1] + p[3]

            
            values = [dealer, ns_pts, ns_tricks, ns_suit, ns_trumps, ew_pts, ew_tricks, ew_suit, ew_trumps]
            values.extend(pts_for_NESW)
            row = {k:v for k,v in zip(columns, values)}
            df = df.append(row, ignore_index=True)
    return df

if __name__ == "__main__":
#    os.chdir("results")
    pattern = r"laneend*"
    pattern = "laneend_20181128_1.pbn"
#    pattern = r"laneend*"
#    getOptimumResults(pattern)
#    pattern = "reading_20150507_1.pbn"
#    checkFilesForDoubleDummyInformation(pattern)
    z = getDataframe(pattern)
    print(z)
#    showLAW(pattern)
