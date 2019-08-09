'''
http://www.bridgeguys.com/Conventions/ScoreDuplicateBridge.html
'''

def getScores(entry, vulnerable):
    try:
        contract = entry[0]
        by = entry[1]
        tricks = int(entry[2])
    except Exception as e:
        # this will be because the hand was passed out
        print(f"scores(Passed out): entry={entry}")
        return ['', '']
        
    def parseBid(contract, vulnerable):
        if vulnerable == 'None': vulnerable = ''
        bid = {}
        try:
            bid['level'] = int(contract[0])
        except Exception as e:
            print(f"scores2: {e}")
        bid['suit'] = contract[1]
        bid['doubled'] = (not 'XX' in contract) and ('X' in contract)
        bid['redoubled'] = 'XX' in contract
        bid['vulnerable'] = by in vulnerable or vulnerable == 'All'
        bid['by'] = by
        bid['tricks'] = tricks
        bid['team'] = 'NS' if by in 'NS' else 'EW'
        return bid

    def isPartScore(bid):
        '''
        bid is a dict containing: level, suit, doubled, redoubled, vulnerable, by, tricks

        '''
        minor = False
        major = False
        if bid['suit'] == 'C': minor = True
        if bid['suit'] == 'D': minor = True
        if bid['suit'] == 'H': major = True
        if bid['suit'] == 'S': major = True
        if bid['redoubled']:
            if minor: 
                return bid['level'] == 1
            else:
                return False
        elif bid['doubled']:
            if minor: 
                return bid['level'] <= 2
            else:
                return bid['level'] == 1
        else:
            if minor:
                return bid['level'] < 5
            elif major:
                return bid['level'] < 4
            else:
                return bid['level'] < 3
    
    def isGame(bid):
        return not isPartScore(bid)
    
    def isSmallSlam(bid):
        return bid['level'] == 6
    
    def isGrandSlam(bid):
        return bid['level'] == 7
    
    def calculate():
        bid = parseBid(contract, vulnerable)
        if bid['level'] + 6 > tricks: 
            tricksDown = bid['level'] + 6 - tricks
            if bid['doubled']: 
                firstUnderTrick = 200 if bid['vulnerable'] else 100
                otherUnderTricks = 300 if bid['vulnerable'] else 200
                bonusFourOrMoreUnderTricks = 0 if bid['vulnerable'] else 100
            elif bid['redoubled']: 
                firstUnderTrick = 400 if bid['vulnerable'] else 200
                otherUnderTricks = 600 if bid['vulnerable'] else 400
                bonusFourOrMoreUnderTricks = 0 if bid['vulnerable'] else 200
            else:
                firstUnderTrick = 100 if bid['vulnerable'] else 50
                otherUnderTricks = 100 if bid['vulnerable'] else 50
                bonusFourOrMoreUnderTricks = 0
            if tricksDown == 1:
                score = firstUnderTrick
            elif tricksDown == 2 or tricksDown == 3:
                score = firstUnderTrick + (tricksDown - 1) * otherUnderTricks
            else:
                score = firstUnderTrick + (tricksDown - 1) * otherUnderTricks + (tricksDown - 3) * bonusFourOrMoreUnderTricks
            if bid['team'] == 'NS':
                return ['', score]
            else:
                return [score, '']
        suitValue = 20 if bid['suit'] == 'C' or bid['suit'] == 'D' else 30
        ntBonusValue = 10
        overtrickValue = suitValue
        bonus = 0
        
        if bid['doubled']: 
            suitValue = suitValue * 2
            ntBonusValue = ntBonusValue * 2
            bonus = 50
            overtrickValue = 200 if bid['vulnerable'] else 100
        if bid['redoubled']:
            suitValue = suitValue * 4
            ntBonusValue = ntBonusValue * 4
            bonus = 100
            overtrickValue = 400 if bid['vulnerable'] else 200

        tricksBidScore = bid['level'] * suitValue
        overtricksScore = (tricks - bid['level'] - 6) * overtrickValue
        ntBonusScore = ntBonusValue if bid['suit'] == 'N' else 0
        score = tricksBidScore + overtricksScore + ntBonusScore + bonus
        if isPartScore(bid):
            score += 50
        if isGame(bid):
            bonus = 500 if bid['vulnerable'] else 300
            score += bonus
        if isSmallSlam(bid):
            bonus = 750 if bid['vulnerable'] else 500
            score += bonus
        if isGrandSlam(bid):
            bonus = 1500 if bid['vulnerable'] else 1000
            score += bonus
        if bid['team'] == 'NS':
            return [score, '']
        else:
            return ['', score]
                
    score = calculate()
    return score

