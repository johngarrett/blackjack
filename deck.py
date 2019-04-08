import random

class Card:
    kinds = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] #kinds to chose from
    suites = ['Hearts', 'Spades', 'Clubs', 'Diamonds'] #suites to chose from
    def __init__ (self, kind, value, suite):
        self.kind = kind    # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, or Ace
        self.value = value if kind != 'Ace' else [1, 11]
        self.suite = suite  # Clubs, Hearts, etc.

    def description(self): #return the information of a card (good for printing)
        if len(self.kind) > 1: #if it is a face card, tell them the value 
            return f'{self.kind} of {self.suite} with a value of {self.value}'
        else:
            return f'{self.kind} of {self.suite}'
    
    
class Deck:
    def generate_deck(self):
        for suite in Card.suites:
            for i, kind in enumerate(Card.kinds):
                self.cards.append(Card(kind, i + 1 if i < 10 else 10, suite))

    def __init__(self):
        self.cards = []
        self.generate_deck()

    def deal_card(self): #return a random card and remove it from the deck
        if len(self.cards) <= 0:
            return
        return self.cards.pop(random.randrange(len(self.cards)))

    def output_cards(self, card1, card2):
        return self.output_card(card1) + self.output_card(card2)
    
    def output_card(self, card):
        return f'\t> {card.description()} <\n'
