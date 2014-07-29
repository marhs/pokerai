import xml.etree.ElementTree as ET
from random import choice, shuffle
from itertools import combinations
from poker import poker
LOOPS = 1000

def resolveAction(player, pocket, actions, state):


    indexActions = ['fold','check','call','bet','raise','allin']
    
    ## Guarda los datos del estado

    ## Empezamos guardando solo las cartas

    tableCards = []

    a = state.find('community')
    for card in a.findall('card'):
        tableCards.append(card.get('rank')+card.get('suit'))

    if len(tableCards) < 3:
        return doAction(2, actions) 
    else:
        odds = calculateOdds(pocket,tableCards, 3)
        if odds < 0.2:
            return doAction(1, actions)
        elif odds > 0.4:
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

def calculateOdds(hand, ntable, numPlayers):
    
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
    cards = hand + table
    hands = [list(x) for x in combinations(cards, 5)]
    return poker(hands)
