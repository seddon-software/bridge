import re, glob, os
import calendar
from matplotlib import pyplot as plt
from collections import Counter
import pandas as pd

board = r'[[]Board\s+["](\d+)["]'
deal = r'[[]Deal\s+["][NESW]:(.*)["][]]'
doubleDummyTricks = r'[[]DoubleDummyTricks\s+["](.*)["]'
pd.set_option('display.width', 1000)
#pd.set_option('display.max_rows', 500)

def getData(FILENAME):
    try:
        with open(FILENAME, "r") as f:
            allLines = f.readlines()
            return allLines
    except IOError as e:
        print(e)

def extractData(data):
    results = []
    for d in data:
        result = re.search(f'{board}', d)
        if result:
            h = {}
            h['board'] = result.group(1)

        result = re.search(f'{deal}', d)
        if result: 
            h['deal'] = result.group(1)
        
        result = re.search(f'{doubleDummyTricks}', d)
        if result: 
            h['tricks'] = result.group(1)
            results.append(h)
    return results

def hasDoubleDummyAnalysis(fileName):
    data = getData(fileName)
    try:
        result = re.search(f'{doubleDummyTricks}', ", ".join(data))
        if result:
            if result.group(1) == "00000000000000000000": 
                print(f"*** error in file", end=", ")
                return False
    except Exception as e:
        print(e)
    return bool(result)

def computeTotalTricks(results):
    TNTricks = []
    for result in results:
        tricks = [int(c, 16) for c in result['tricks']]
        NS = [(n+s)/2 for n, s in zip(tricks[0:5], tricks[5:10])]
        EW = [(e+w)/2 for e, w in zip(tricks[10:15], tricks[15:20])]
        TNTricks.append(max(NS) + max(EW))
    return TNTricks

def computeTotalTrumps(results):
    TNTrumps = []
    for result in results:
        hands = result['deal'].split()
        distributions = []
        for hand in hands:
            distributions.append([len(suit) for suit in hand.split('.')])
        NS = [n+s for n, s in zip(distributions[0], distributions[2])]
        EW = [e+w for e, w in zip(distributions[1], distributions[3])]
        TNTrumps.append(max(NS) + max(EW))
    return TNTrumps

    
def checkFilesForDoubleDummyInformation(pattern):
    listOfFiles = glob.glob(pattern)
    listOfFiles.sort()
    for fileName in listOfFiles:
        if not hasDoubleDummyAnalysis(fileName):
            year = fileName[8:12]
            month_idx = int(fileName[12:14])
            month = calendar.month_name[month_idx]
            day = fileName[14:16]
            print(f"No double dummy analysis: {day} {month} {year} ")

def examinePointsFor_4S(pattern):
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

    listOfFiles = glob.glob(pattern)
    listOfFiles.sort()
    columns = ['ns_pts','ns_tricks','ns_trumps','ew_pts','ew_tricks','ew_trumps']
    df = pd.DataFrame(columns=columns)
    def best(d):
        biggest = 0
        big_d = {}
        for key in d:
            if d[key] > biggest: 
                biggest = d[key]
                big_d = {key:d[key]}
        return big_d
            
    for fileName in listOfFiles:
        data = getData(fileName)
        results = extractData(data)
        for result in results:
            tricks = [int(c, 16) for c in result['tricks']]
            hands = result['deal'].split()
            N = HCPs(hands[0].split("."))
            E = HCPs(hands[1].split("."))
            S = HCPs(hands[2].split("."))
            W = HCPs(hands[3].split("."))
            NS_pts = N + S
            EW_pts = E + W
            tricks = [int(c, 16) for c in result['tricks']] # nt-S-H-D-C
            NS_tricks = {key:(n+s)/2.0 for key,n,s in zip(["NT","S","H","D","C"], tricks[0:5], tricks[5:10])}
            EW_tricks = {key:(e+w)/2.0 for key,e,w in zip(["NT","S","H","D","C"], tricks[10:15], tricks[15:20])}
            N = distribution(hands[0].split("."))
            E = distribution(hands[1].split("."))
            S = distribution(hands[2].split("."))
            W = distribution(hands[3].split("."))
            NS_trumps = {key:n+s for key,n,s in zip(["S","H","D","C"],N,S)}
            EW_trumps = {key:e+w for key,e,w in zip(["S","H","D","C"],E,W)}
            best_ns_tricks = best(NS_tricks)
            best_ew_tricks = best(EW_tricks)
            ns_tricks = list(best_ns_tricks.values())[0]
            ew_tricks = list(best_ew_tricks.values())[0]
            ns_suit = list(best_ns_tricks.keys())[0]
            ew_suit = list(best_ew_tricks.keys())[0]
#             print(f"NS: tricks={ns_tricks}, trumps={NS_trumps[ns_suit]}, HCPs={NS_pts}")
#             print(f"EW: tricks={ew_tricks}, trumps={EW_trumps[ew_suit]}, HCPs={EW_pts}")
            # columns = ['ns_pts','ns_tricks','ew_trumps','ew_pts','ew_tricks','ew_trumps']
            ns_trumps = 0 if ns_suit == "NT" else NS_trumps[ns_suit]
            ew_trumps = 0 if ew_suit == "NT" else EW_trumps[ew_suit]
            row = {k:v for k,v in zip(columns, [NS_pts, ns_tricks, ns_trumps, EW_pts, ew_tricks, ew_trumps])}
            df = df.append(row, ignore_index=True)

    return df

def showLAW(pattern):
    listOfFiles = glob.glob(pattern)
    listOfFiles.sort()
    allDifferences = []
    
    for fileName in listOfFiles:
        data = getData(fileName)
        results = extractData(data)
        totalTricks = computeTotalTricks(results)
        totalTrumps = computeTotalTrumps(results)        
        differences = [tricks-trumps for tricks, trumps in zip(totalTricks, totalTrumps)]

        for i, difference in enumerate(differences):
            # if difference <= -10 then the data has been uploaded incorrectly and should be ignored
            if (difference < -2.5 and difference > -10) or (difference > 2.5): 
                year = fileName[8:12]
                month_idx = int(fileName[12:14])
                month = calendar.month_name[month_idx]
                day = fileName[14:16]
                tricks = totalTricks[i]
                trumps = totalTrumps[i]
                mismatch = tricks - trumps
                print(f"Board {i+1:2} has LAW: {tricks:4.1f}-{trumps:2}={mismatch:4.1f}, {day} {month} {year}") 
        allDifferences.extend(differences)
    
    # remove data that has been posted incorrectly
    allDifferences = [d for d in allDifferences if d > -10]

    # determine frequencies
    allDifferences.sort()
    counts = Counter(allDifferences)
    numberOfHands = len(allDifferences)
    print(f"No of hands = {numberOfHands}")

    # print frequencies as percentages
    for key in counts:
        print("TNT mismatch: {:6.1f} {:6.1f}".format(key, counts[key]*100/numberOfHands))

    # plot results
    _, ax = plt.subplots()
    ax.bar(range(len(allDifferences)), allDifferences)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    os.chdir("results")
    pattern = r"laneend*"
    checkFilesForDoubleDummyInformation(pattern)
    z = examinePointsFor_4S(pattern)
    print(z)
#    showLAW(pattern)
