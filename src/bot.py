import xml.etree.ElementTree as ET
from random import choice, shuffle
from itertools import combinations
from poker import poker

LOOPS = 1000        # Number of plays to simulate
LIMITS = (0.2,0.4)  # Checks under the first, raise over the second

# Define the parameters for the different bots
USERS = {'helmetk': (0.2,0.4),
         'marco':   (0.1,0.5)}

def resolveAction(player, pocket, actions, state):
    "Given the status of a game, returns the best action"
    # TODO Add a limit for the raise. Something like strenght*maxMoney
    tableCards, numPlayers = [], 0

    # Use the specific parameters if a bot is called. 
    if player in USERS:
        limits = USERS[player]
        print(player, 'is playing')
    else:
        limits = LIMITS

    a = state.find('community')
    for card in a.findall('card'):
        tableCards.append(card.get('rank')+card.get('suit'))
    a = state.find('table')
    for p in a.findall('player'):
        numPlayers += 1

    if len(tableCards) < 3:
        if preFlopStrenght(pocket):
            return doAction(4, actions)
        else:
            return doAction(2, actions) 
    else:
        odds = calculateOdds(pocket,tableCards, numPlayers)
        if odds < limits[0]:
            return doAction(1, actions)
        elif odds > limits[1]:
            return doAction(4, actions)
        else:
            return doAction(2, actions)

def doAction(maxAction, actions):
    "Try to do an action. If is not possible, try another least agressive"

    indexActions = ['fold','check','call','bet','raise','allin']
        
    for n in reversed(range(maxAction+1)):
        if indexActions[n] in actions:
            return indexActions[n]

    return 'fold'

def preFlopStrenght(hand):
    "Return if the strenght of the pocket cards is high"

    goodPairs = ['AA','AK','KA','KK','QQ','JJ']
    pair = [x[0] for x in hand]
     
    return ''.join(pair) in goodPairs

def calculateOdds(hand, ntable, numPlayers):
    "Given a hand and the community cards, returns the strenght of the hand" 
    score = 0
    table = [x for x in ntable] # Sort of deepcopy
    if len(table) < 3:
        return 0

    for n in range(LOOPS):
        deck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 
        # Remove the pockets cards of the deck
        deck.remove(hand[0])
        deck.remove(hand[1])
        # Remove the table cards of the deck
        for card in table:
            deck.remove(card)
        # Shuffle and fill the table with cards
        shuffle(deck)
        while(len(table)<5):
            table.append(deck.pop())
        # Generate hands
        players = [generateHands(hand, table)[0]]
        aux = []
        for n in range(numPlayers-1):
            aux.append(deck.pop())
            aux.append(deck.pop())
            players.append(generateHands(aux, table)[0])
            aux = []
        # Check if I have the winner hand
        if players.index(poker(players)[0]) == 0:
            score += 1

    return score/LOOPS

def generateHands(hand, table):
    "Return the winner combination of the avaiable cards"
    cards = hand + table
    hands = [list(x) for x in combinations(cards, 5)]
    return poker(hands)
