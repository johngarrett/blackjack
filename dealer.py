from deck import Deck

class Dealer:
    players = {}
    def __init__(self):
        self.dealer_deck = Deck()
    
    #return only 1 card
    def deal_card(self):
        return self.dealer_deck.deal_card()
    
    #inital dealer cards (2)
    def inital_dcards(self):
        cards = self.get_two_cards()
        #set the card to 1 or 11 depending on the kind and other card's value
        cards[0].value = 1 if cards[0].kind == 'Ace' and cards[1].value != 10 else 11
        cards[1].value = 1 if cards[0].kind == 'Ace' and cards[0].value != 10 else 11
        
        self.hand_value = cards[0].value + cards[1].value
        return self.dealer_deck.output_cards(cards[0], cards[1])
    
    #inital player cards (2)
    def inital_pcards(self, player):
        cards = self.get_two_cards()
        player.cards = cards
        self.players[player] = player
        return cards
    
    def get_two_cards(self):
        card1 = self.deal_card()
        card2 = self.deal_card()
        return [card1, card2]

    def get_value(self, player):
        return self.players[player].hand_value
    
    #returns a string of the next move (card or draw)
    def next_dmove(self):
        update = ''
        if self.hand_value < 19: #still in the game
            n_card = self.deal_card()
            n_card.value = 1 if n_card.kind == 'Ace' and self.hand_value > 10 else 11
            self.hand_value += n_card.value
            update = self.dealer_deck.output_card(n_card)
            self.is_playing = True
        else:
            update = 'The dealer is done playing. They do not ask for another card'
        update += f'The dealer\'s hand now adds up to {self.hand_value}'
        return update
