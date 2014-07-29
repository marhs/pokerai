import xml.etree.ElementTree as ET
from random import choice, shuffle
from itertools import combinations
from poker import poker
LOOPS = 1000

def resolveAction(player, pocket, actions, state):


    ## Guarda los datos del estado

    ## Empezamos guardando solo las cartas

    tableCards = []

    a = state.find('community')
    for card in a.findall('card'):
        tableCards.append(card.get('rank')+card.get('suit'))

    if len(tableCards) < 3:
       return doAction(player, 'call', actions) 
    else:
        odds = calculateOdds(pocket,tableCards, 3)
        print(odds, len(tableCards))
        if odds < 0.2:
            return 'check'
        elif odds > 0.4:
            return doAction(player, 'bet', actions)
        else:
            return doAction(player, 'call', actions)

def doAction(player, action, actions):
    
    print(actions)
    if action == 'raise' or action == 'bet':
        if action in actions:
            action = action 
        elif 'raise' in actions:
            action = 'raise'
        elif 'bet' in actions:
            action = 'bet'
        elif 'call' in actions:
            action = 'call'
        else:
            action = 'check'
    elif action == 'call':
        if action in actions:
            action = 'call'
        else:
            action = 'check'
    else:
        action = 'check'
    print(player," is doing: ", action)
    return action

def calculateOdds(hand, ntable, numPlayers):
    
    score = 0
    table = [x for x in ntable]
    if len(table) < 3:
        return 0
    for n in range(LOOPS):

        deck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 
        # Remove the pockets cards of the deck
        deck.remove(hand[0])
        deck.remove(hand[1])
        # Remove the table cards of the deck
        shuffle(deck)
        for card in table:
            deck.remove(card)

        while(len(table)<5):
            table.append(deck.pop())
        # Repartir cartas
        players = [generateHands(hand, table)[0]]
        aux = []
        for n in range(numPlayers-1):
            aux.append(deck.pop())
            aux.append(deck.pop())
            players.append(generateHands(aux, table)[0])
            aux = []

        if players.index(poker(players)[0]) == 0:
            score += 1


    return score/LOOPS

def generateHands(hand, table):
    cards = hand + table
    hands = [list(x) for x in combinations(cards, 5)]
    return poker(hands)
