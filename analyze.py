import pickle
import ast
import sys

handRank = pickle.load(open('2handRankData.p', "rb"))

#p with highest a single ace    (and p if suited)
#p with highest a single king   (and p if suited)
#p with highest .. etc          (and p if suited)

#p all pocket pairs             (and p if suited)

#p all connectors

def allThatMatch(c1, c2=None):
    sAll = 0
    nAll = 1
    st = 0
    nt = 1
    for k in handRank.keys():
        s,n,avg = handRank[k]
        parsedKey = ast.literal_eval(k)
        if c2 == None:
            if parsedKey[0] in c1 or parsedKey[1] in c1:
                sAll += s
                nAll += n
        else:
            if parsedKey[0] in c1 or parsedKey[1] in c1 and parsedKey[0] in c2 or parsedKey[1] in c2:
                sAll += s
                nAll += n
    print "ranked above in " + str(sAll*1.0/nAll) + " of hands"

allThatMatch([(14,1),(14,2),(14,3),(14,4)])
allThatMatch([(13,1),(13,2),(13,3),(13,4)])
allThatMatch([(12,1),(12,2),(12,3),(12,4)])
allThatMatch([(11,1),(11,2),(11,3),(11,4)])
allThatMatch([(10,1),(10,2),(10,3),(10,4)])
allThatMatch([(9,1),(9,2),(9,3),(9,4)])
allThatMatch([(8,1),(8,2),(8,3),(8,4)])

print "Pair"
print handRank['[(14, 1), (14, 2)]']
print handRank['[(13, 1), (13, 2)]']
print handRank['[(12, 1), (12, 2)]']
print handRank['[(11, 1), (11, 2)]']
print handRank['[(10, 1), (10, 2)]']
print handRank['[(9, 1), (9, 2)]']
print handRank['[(8, 1), (8, 2)]']
print handRank['[(7, 1), (7, 2)]']
print handRank['[(6, 1), (6, 2)]']
print handRank['[(5, 1), (5, 2)]']
print handRank['[(4, 1), (4, 2)]']
print handRank['[(3, 1), (3, 2)]']
print handRank['[(2, 1), (2, 2)]']

print "AK"
allThatMatch([(14,1),(14,2),(14,3),(14,4)],[(13,1),(13,2),(13,3),(13,4)])
print "KQ"
allThatMatch([(13,1),(13,2),(13,3),(13,4)],[(12,1),(12,2),(12,3),(12,4)])
print "AQ"
allThatMatch([(14,1),(14,2),(14,3),(14,4)],[(12,1),(12,2),(12,3),(12,4)])
print "AJ"
allThatMatch([(14,1),(14,2),(14,3),(14,4)],[(11,1),(11,2),(11,3),(11,4)])

if len(sys.argv) > 1:
    print sys.argv[1]
    print handRank[sys.argv[1]]
