# Sample Board: (3x3)
#   0   1   2
#   3   4   5
#   6   7   8

# Sample Board: (4x3)
#   0   1   2   3
#   4   5   6   7
#   8   9   10  11

allMovesPossible = []
leaf = 0
# Draws the box in ASCII
def drawBoard(moves, width, height):
    for row in range(height):
        line = ""
        for col in range(width):
            index = row*width + col
            line += str(index) + "\t"
            if (index, index+1) in moves:
                line += "--"
            line += "\t"
        print line
        line = ""
        for col in range(width):
            index = row*width + col
            if (index, index+width) in moves:
                line += "|"
            line += "\t\t"
        print line


# returns a list of indexes adjacent to this dot index
def getAdjacent(dotIndex, width, height):
    # start with an empty list, we'll add adjcent indexes as we discover them
    adjacentIndexes = []
    
    # everything has a left, right, top, and left neighbor.
    # just not sure if its valid or not
    top = dotIndex - width
    bottom = dotIndex + width
    left = dotIndex - 1
    right = dotIndex + 1
    
    # now figure out if they're actually legal.
    # top row won't have a "top"
    if dotIndex >= width:
        adjacentIndexes.append(top)
        
    # left column (index evenly divisible by width) won't have a "left"
    if dotIndex % width != 0:
        adjacentIndexes.append(left)
    
    # right column (index+1 evenly divisible by width) won't have a "right"
    if (dotIndex + 1) % width != 0:
        adjacentIndexes.append(right)
    
    # bottom row won't have a "bottom"
    if dotIndex < (width * height) - width:
        adjacentIndexes.append(bottom)
    
    return adjacentIndexes

# Generate a list of all possible moves.
# In order to better get rid of duplicates, the first number will always be the smaller number
# (0,3) is the same move as (3,0) so only store (0,3).
def allMoves(width, height):
    listOfAllMoves = []     # We'll store the moves here
    
    for currentDot in range(width*height):  # Go through every dot in the grid
        # for each dot, get the pegs adjacent to it that have higher indexes
        # and store that tuple as a possible move 
        adjacentDots = getAdjacent(currentDot, width, height) # you could also write a special version of getAdjacent that only returns indexes greater than the currentDot... 
        
        
        for adjDot in adjacentDots:     # go through every dot that is adjacent to the current one (that we could draw a line to)
            if adjDot > currentDot:     # only include it if its greater than the current to avoid duplicates (0,3) vs (3,0)
                listOfAllMoves.append( (currentDot, adjDot) )   # add the move to the list of possibleMoves
    
    return listOfAllMoves

# Generate a list of possible moves left based on the ones already taken
# In order to better get rid of duplicates, the first number will always be the smaller number
# (0,3) is the same as (3,0) so only store (0,3).
def genMoves(listOfTakenMoves, width, height):
    global allMovesPossible
    if allMovesPossible == []:
        allMovesPossible = allMoves(width, height)
    remaining = [i for i in allMovesPossible if i not in listOfTakenMoves]
    if scoreAfterLastMove(listOfTakenMoves, width, height, (0,0)) == (0, 0) or len(remaining) == 0:
        return remaining
    else:
        return [(-999, -999)]

# Node getters/setters/accessors

def getMoveList(node):
    return node[0]

def setMoveList(node, moveList):
    node[0] = moveList

def addToMoveList(node, newMove):
    node[0].append(newMove)

def getWinState(node):
    return node[1]

def setWinState(node, winState):
    node[1] = winState

def getChildList(node):
    return node[2]

def setChildList(node, childList):
    node[2] = childList

def addChild(node, newChild):
    node[2].append(newChild)

def createNode(movesTaken, lastMove):
    moveListCopy = movesTaken[:]
    node = []
    if moveListCopy == []:
        node =  [ [lastMove], '?', [] ]
    else:
        moveListCopy.append(lastMove)
        node = [ moveListCopy , '?', [] ]
    return node


##############################################################
##                  Recursion - Beware                      ##
##############################################################

# Really, a lot of the times, you already know the score because you just 
# came from a position and knew the score from there already and you're 
# only interested in whether the last move finished a box or not
def scoreAfterLastMove(listOfMoves, width, height, previousScore):
    if len(listOfMoves) > 0 and listOfMoves[len(listOfMoves)-1] != (-999, -999):
        lastMove = listOfMoves[len(listOfMoves)-1]
        borderBox1 = []
        borderBox2 = []
        if lastMove[0] + 1 == lastMove[1]:  # horizontal 
            borderBox1.append((lastMove[0]-width, lastMove[0])) # top box
            borderBox1.append((lastMove[1]-width, lastMove[1]))
            borderBox1.append((lastMove[0]-width, lastMove[1]-width))
            borderBox2.append((lastMove[0], lastMove[0]+width)) # top box
            borderBox2.append((lastMove[1], lastMove[1]+width))
            borderBox2.append((lastMove[0]+width, lastMove[1]+width))
        else:   # vertical
            borderBox1.append((lastMove[0]-1, lastMove[0]))     # left box
            borderBox1.append((lastMove[1]-1, lastMove[1]))
            borderBox1.append((lastMove[0]-1, lastMove[1]-1))
            borderBox2.append((lastMove[0], lastMove[0]+1))     # right box
            borderBox2.append((lastMove[1], lastMove[1]+1))
            borderBox2.append((lastMove[0]+1, lastMove[1]+1))
        
        for move in listOfMoves:
            if move in borderBox1:
                borderBox1.remove(move)
            if move in borderBox2:
                borderBox2.remove(move)
        
        boxesCompleted = 0
        
        if len(borderBox1) == 0:
            boxesCompleted += 1
        if len(borderBox2) == 0:
            boxesCompleted += 1
    
        if len(listOfMoves) % 2 == 0:   # last move made by player 2
            #print "Player 2 completed " + str(boxesCompleted) + " boxes."  # testing
            #drawBoard(listOfMoves, width, height)                          # testing
            return (previousScore[0], previousScore[1] + boxesCompleted)
        else:
            #print "Player 1 completed " + str(boxesCompleted) + " boxes."  # testing
            #drawBoard(listOfMoves, width, height)                          # testing
            return (previousScore[0] + boxesCompleted, previousScore[1])
    else:
        #print "No boxes completed\n"
        return previousScore

# This method is recursive.
def countBoxesToDepth(listOfMoves, width, height, depth, score):
    if depth > len(listOfMoves):
        return score
    else:
        return countBoxesToDepth(listOfMoves, width, height, depth + 1, scoreAfterLastMove(listOfMoves[:depth], width, height, score))


# Play through the game based on this list of moves and determine how many 
# boxes each player has. Returns a tuple (boxesForPlayer1, boxesForPlayer2)
# Test with:
#   scoreGame([ (0, 1), (1, 3), (0, 2), (2, 3) ], 2, 2)
#   scoreGame([ (0, 1), (2, 3), (1, 2), (5, 6), (4, 5), (5, 9), (6, 7), (2, 6), (1, 5), (-999, -999), (0, 4), (-999, -999), (9, 10), (6, 10), (-999, -999), (3, 7), (-999, -999), (4, 8), (8, 9), (-999, -999), (7, 11), (10, 11)  ], 4, 3)
def scoreGame(listOfMoves, width, height):
    return countBoxesToDepth(listOfMoves, width, height, 0, (0, 0))


def relativeScore(score):
    return score[0] - score[1]


def winLoseDraw(relativeScore):
    if relativeScore == 0:
        return 'D'
    elif relativeScore < 0:
        return 'L'
    elif relativeScore > 0:
        return 'W'
    else:
        return '?'  # this should never happen.

def evaluateTree(node, width, height):
    if getWinState(node) != '?':        # we already figured out if this wins loses or draws
        return
    else:
        if True:
            movesFromHere = genMoves(getMoveList(node), width, height)
            if len(movesFromHere) == 0:     # no more children. score and mark as win lose or draw
                mult = 1
                if len(getMoveList(node)) % 2 == 1:
                    mult = -1
                gameScore = mult * relativeScore(scoreGame(getMoveList(node), width, height))
                setWinState(node, winLoseDraw(gameScore))
                global leaf
                leaf += 1
                if leaf % 10000 == 0:
                    print leaf
                return
            else:       # go get children and figure out if they win lose or draw
                #earlyBreak = False
                for move in movesFromHere:
                    newNode = createNode(getMoveList(node), move)
                    evaluateTree(newNode, width, height)
                    if (len(getMoveList(node))%2 == 0 and getWinState(newNode) == 'L') :
                       setChildList(node, [newNode])
                       break
                    #elif not (len(getMoveList(node))%2 == 0 and getWinState(newNode) == 'W') :
                    #   addChild(node, newNode)
                    else:
                        addChild(node, newNode)
                # count wins loses and draws to figure out if i won or not
                #if earlyBreak:
                #   print "break early"
                wins = 0
                draws = 0
                loses = 0
                for child in getChildList(node):
                    if getWinState(child) == 'W':
                        wins += 1
                    elif getWinState(child) == 'L':
                        loses += 1
                    elif getWinState(child) == 'D':
                        draws += 1
                    else:
                        print "Screwed up somewhere. This should never happen"
                
                if loses > 0:
                    setWinState(node, 'W')
                    if len(getMoveList(node))%2 == 1:
                        setChildList(node, [])
                elif draws > 0:
                    setWinState(node, 'D')
                else:
                    setWinState(node, 'L')
                    if len(getMoveList(node))%2 == 0:
                        setChildList(node, [])
                    #setChildList(node, [])
                #print "Position: " + str(getMoveList(node)) + "\t W: " + str(wins) + "\t D: " + str(draws) + "\t L: " + str(loses) + ". This is a " + str(getWinState(node))

def getBestPath(node):
    if getChildList(node) == []:
        print getMoveList(node)
    else:
        winNode = []
        drawNode = []
        loseNode = []
        for child in getChildList(node):
            if getWinState(child) == 'L':
                winNode = child
                break
            elif getWinState(child) == 'D':
                drawNode = child
            elif getWinState(child) == 'W':
                loseNode = child
        if winNode != []:
            #print "There is a win"
            getBestPath(winNode)
        elif drawNode != []:
            #print "There is a draw"
            getBestPath(drawNode)
        elif loseNode != []:
            #print "There is a loss"
            getBestPath(loseNode)

#root = [ [(0, 1), (7, 8), (1, 2), (6, 7), (0, 3), (5, 8), (3, 4), (1,4), (-999, -999), (4, 5), (4, 7), (-999,-999)] , '?', [] ]
root = [ [] , '?', [] ]
evaluateTree(root, 2, 4)
print "Tested " + str(leaf) + " strategies."
print "The root position is a " + str( getWinState(root))
print "Best Path is: " 
getBestPath(root)
