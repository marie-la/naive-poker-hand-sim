import random
import pickle

def draw(deck):
    card = random.choice(deck)
    deck.remove(card)
    return deck, card

def draw7(deck,num=7):
    hand = []
    for i in range(num):
        deck,card = draw(deck)
        hand.append(card)
    return deck,hand

#array implicitly representing deck
def pickCard(deck):
    r = random.randint(0,51)
    while deck[r] == True:
        r = random.randint(0,51)
    return r

def rankEqualScoreHands(h1,h2):
    for i in range(5):
        if h1[i][0] > h2[i][0]:
            return 1
        if h1[i][0] < h2[i][0]:
            return 0
    return .5

def makeBestHand(cards):
    #0 = high cards
    #1 = pair
    #2 = two pair
    #3 = three
    #4 = straight
    #5 = flush
    #6 = fullhouse
    #7 = four
    #8 = straight flush
    #9 = royal flush
    cards = sorted(cards, key=lambda c: c[1])
    flushHands = []
    samesuit = 1
    for i in range(6):
        if cards[i][1] == cards[i+1][1]:
            samesuit += 1
        else:
            samesuit = 1
        if samesuit >= 5:
            flushHands.append(cards[i-3:i+2])

    straightHands = []
    cards = sorted(cards, key=lambda c: c[0])
    connected = 1
    for i in range(6):
        if cards[i][0] == cards[i+1][0]-1:
            connected += 1
        else:
            connected = 1
        if connected >= 5:
            straightHands.append(cards[i-3:i+2])

    fourHands = []
    threeHands = []
    twoHands = []
    repeat = 1
    for i in range(6):
        if cards[i][0] == cards[i+1][0]:
            repeat += 1
        else:
            repeat = 1
        if repeat >= 2:
            twoHands.append((cards[i:i+2]))
        if repeat >= 3:
            threeHands.append(cards[i-1:i+2])
        if repeat == 4:
            fourHands.append(cards[i-2:i+2])
    '''
    print flushHands
    print straightHands
    print fourHands
    print threeHands
    print twoHands
    '''

    #straight/royal flush
    straightFlush = sum([set(h1)==set(h2) for h1 in straightHands for h2 in flushHands])
    if straightFlush > 0:
        for hand in [h1 for h1 in straightHands for h2 in flushHands if set(h1) == set(h2)]:
            if 14 in hand:
                #print "Royal flush"
                return 9,hand
            else:
                #print "Straight flush"
                return 8,hand

    #four of a kind
    if len(fourHands) > 0:
        hand = fourHands[0]
        x = -1
        while len(hand) < 5:
            if cards[x] not in hand:
                hand.append(cards[x])
            x -= 1

        #print "Four of a kind"
        return 7,hand

    #full house
    if len(threeHands) > 0 and len(twoHands) > 2:
        hand = threeHands[0]
        x = -1
        while len(hand) < 5:
            if twoHands[x][0][1] != hand[0][1]:
                hand+=twoHands[x]
            x -= 1
        #print "Full house"
        return 6,hand

    #flush
    if len(flushHands) > 0:
        hand = flushHands[-1]
        #print "Flush"
        return 5,hand

    #straight
    if len(straightHands) > 0:
        hand = straightHands[-1]
        #print "Straight"
        return 4,hand

    #three of a kind
    if len(threeHands) > 0:
        hand = threeHands[-1]
        x = -1
        while len(hand) < 5:
            if cards[x] not in hand:
                hand.append(cards[x])
            x -= 1
        #print "Three of a kind"
        return 3,hand

    #two pair
    if len(twoHands) > 1:
        twoHands = sorted(twoHands, key = lambda c: c[0])
        hand = twoHands[-1] + twoHands[-2]
        x = -1
        while len(hand) < 5:
            if cards[x][0] not in hand:
                hand.append(cards[x])
            x -= 1
        #print "Two Pair"
        return 2,hand

    #pair
    if len(twoHands) > 0:
        hand = twoHands[0]
        x = -1
        while len(hand) < 5:
            if cards[x] not in hand:
                hand.append(cards[x])
            x -= 1
        #print "Pair"
        return 1,hand

    #high card
    #print "High cards"
    return 0,cards[1:-1]


def simulatePlay(n):
    num_players = 2
    handRank = pickle.load(open('2handRankData.p', "rb"))

    for _ in range(n):
        deck = [(n,s) for n in nums for s in suits]

        deck,streets = draw7(deck,5)
        alldrawn = []
        scores = []
        besthands = []
        for _ in range(num_players):
            deck,deal = draw7(deck,2)
            alldrawn.append(deal)
            hand=deal+streets
            score,hand = makeBestHand(hand)
            scores.append(score)
            besthands.append(hand)

        hand = alldrawn[0]
        s = sum([1 for x in scores if x < scores[0]])
        if scores[0] == scores[1]:
            s += rankEqualScoreHands(besthands[0],besthands[1])
        key = str(hand)
        if key in handRank:
            newsum = handRank[key][0]+s
            newcount = handRank[key][1] + 1
            newavg = newsum*1.0/newcount
            handRank[key] = [newsum,newcount,newavg]
        else:
            handRank[key] = [s,1,s/1]

        key = str(alldrawn[1])
        s = sum([1 for x in scores if x < scores[1]])
        if scores[0] == scores[1]:
            s += rankEqualScoreHands(besthands[1],besthands[0])
        if key in handRank:
            newsum = handRank[key][0]+s
            newcount = handRank[key][1] + 1
            newavg = newsum*1.0/newcount
            handRank[key] = [newsum,newcount,newavg]
        else:
            handRank[key] = [s,1,s/1]
    pickle.dump(handRank, open("2handRankData.p", "wb"))

nums = [2,3,4,5,6,7,8,9,10,11,12,13,14]
suits = [1,2,3,4]
deck = [(n,s) for n in nums for s in suits]

simulatePlay(5000000)
'''



num = 100000
pair = 0
trip = 0
four = 0
fhouse = 0
flush = 0

for i in range(num):
    deck = [False] * 52
    ofakind = [0] * 13
    suit = [0] * 4
    for j in range(7):
        r = pickCard(deck)
        deck[r] = True
    for k in range(13):
        ofakind[k] = deck[k] + deck[k+13] + deck[k+2*13] + deck[k+3*13]
    for l in range(4):
        suit[l] = sum([deck[x] for x in range(l*13,(l+1)*13)])

    if max(suit) >= 5:
        flush += 1

    if 2 in ofakind:
        pair += 1
    if 3 in ofakind:
        trip += 1
    if 4 in ofakind:
        four += 1
    if 3 in ofakind and 2 in ofakind:
        fhouse += 1

print "p of pair: " + str(pair*1.0/num)
print "p of trip: " + str(trip*1.0/num)
print "p of four: " + str(four*1.0/num)
print "p of fhouse: " + str(fhouse*1.0/num)
print "p of flush: " + str(flush*1.0/num)


#p of pair that has something to do with your hand?
3.0/51+6.0/50+(6.0/49)*(44.0/40)

#increasing num of players, what is the prob that someone has a higher hand than you?
'''
