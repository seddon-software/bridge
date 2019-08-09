import re, glob, os
import calendar
from matplotlib import pyplot as plt
from collections import Counter

board = r'[[]Board\s+["](\d+)["]'
deal = r'[[]Deal\s+["][NESW]:(.*)["][]]'
doubleDummyTricks = r'[[]DoubleDummyTricks\s+["](.*)["]'

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

    
def main():
    os.chdir("results")
    listOfResults = glob.glob('reading*.pbn')
    listOfResults.sort()
    allDifferences = []
    
    for f in listOfResults:
        data = getData(f)
        results = extractData(data)
        totalTricks = computeTotalTricks(results)
        totalTrumps = computeTotalTrumps(results)        
        differences = [tricks-trumps for tricks, trumps in zip(totalTricks, totalTrumps)]

        for i, d in enumerate(differences):
            if (d < -2.5 and d > -10) or (d > 2.5): 
                year = f[8:12]
                month_idx = int(f[12:14])
                month = calendar.month_name[month_idx]
                day = f[14:16]
                print(f"Board {i+1:2} has LAW: {totalTricks[i]:4.1f}-{totalTrumps[i]:2}=" +
                      f"{totalTricks[i]-totalTrumps[i]:4.1f}, {day} {month} {year}") 
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

main()
