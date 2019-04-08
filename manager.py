from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from dealer import Dealer
import os

class GameManager:
    def attempt_start(self):
        while True:
            if len(self.players) < 2:
                self.broadcast('\nNot enough players yet.\nThe game cannot begin.\n')
                break
            for player in self.players:
                if player.state != True:
                    self.broadcast('Someone in the match is not ready')
                    return
            self.begin_game()
            return

    def begin_game(self):
        self.broadcast('clrscrn')
        self.broadcast('Lets begin.\n')
        self.broadcast(f'The dealer\'s first cards are:\n\n{self.dealer.inital_dcards()}')
        for player in self.players:
            inital_pcards = self.dealer.inital_pcards(player)
            self.send_message(player.socket, '\nYour first cards are:\n')
            for card in inital_pcards:
                self.send_message(player.socket, self.dealer.deck.output_card(card))
            self.ace_check(player)
            player.hand_value = inital_pcards[0].value + inital_pcards[1].value
        self.play()

    def play(self):
        for player in self.players:
            if not player.is_playing:
                return
            
            for other_player in self.players:
                if other_player != player:
                    self.send_message(other_player.socket, f'It\'s {player.name}\'s turn.')

            self.send_message(player.socket, f'Your hand adds up to {player.hand_value}\nWould you like a hit? (y/n):')
            response = self.get_response(player.socket)
            
            while response == 'Y' or response == 'y' and player.is_playing:
                for other_player in self.players:
                    if other_player != player:
                        self.send_message(other_player.socket, f'{player.name} asks for another card')

                additional_card = self.dealer.deal_card()
                self.send_message(player.socket, f'\nThe dealer gives you the following card:\n{self.dealer.deck.output_card(additional_card)}')
                player.cards.append(additional_card)
                self.ace_check(player)
                player.hand_value += additional_card.value
                self.dealer_move()
                self.send_message(player.socket, '\nWould you like a hit? (y/n):')
                response = self.get_response(player.socket)
            self.end_game_for(player)
        self.end_game()

    def dealer_move(self):
        if self.dealer_done:
            return
        next_move = self.dealer.next_dmove()
        if 'out' in next_move:
            self.dealer_done = True
        self.broadcast(next_move)

    def end_game(self):
        self.broadcast('clrscrn')
        self.broadcast_banner('⚑')
        end_game_msg = ''
        for player in self.players:
            end_game_msg += f'{player.name}\'s final score: {player.hand_value}\n'
        end_game_msg += f'The dealer\'s final score was {self.dealer.hand_value}'
        
        self.broadcast(end_game_msg)
        self.broadcast_banner('⚑')

    def end_game_for(self, player):
        player.is_playing = False
        self.send_message(player.socket, f'\nYou\'re out!\nYour final score was: {player.hand_value}')
    
    def ace_check(self, player):
        for index, card in enumerate(player.cards):
            if card.kind == 'Ace' and card.value == [1, 11]:
                self.send_message(player.socket, '\nYou were dealt an Ace\n\nYou must make a decision.\nWill the Ace\'s value be 1 or 11? (default = 11):')
                value = self.get_response(player.socket)
                player.cards[index].value = 1 if value == '1' else 11

    def send_message(self, socket, msg, prefix = ''):
        message = prefix + msg
        socket.send(bytes(message, 'utf8'))
    
    def broadcast(self, msg, prefix = ''):
        message = bytes(prefix, 'utf8') + bytes(msg, 'utf8')
        for sock in self.clients:
            sock.send(message)

    def broadcast_banner(self, char):
        message = '\n'
        for _ in range(10):
            message += f'{char}  '
        message += '\n'
        self.broadcast(message)
    
    def get_response(self, socket):
        message = socket.recv(1024).decode('utf8')
        return message

    
    def __init__(self):
        self.clients = {}
        self.players = []
        self.HOST = '127.0.0.1'
        self.PORT = 33000
        self.dealer_done = False
        self.ADDR = (self.HOST, self.PORT)
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)
        self.dealer = Dealer()
        _max = int(input('Max connections: ') or '5')
        self.SERVER.listen(_max)
        os.system('clear') #clear the screen (Linux)
        print('Waiting for connections...')
        ACCEPT_THREAD = Thread(target = self.accept_new_connection)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()
        self.attempt_start()
    def accept_new_connection(self):
        divider = '🂡  🂢  🂣  🂤  🂥  🂦  🂧  🂨  🂩  🂪  🂡  🂢  🂣  🂤'
        welcome = f'{divider}\n\n\tWELCOME TO BLACKJACK\n\n{divider}\n\n\nType ready when you\'re set to play\n\nPlease enter your name:'
        while True:
            socket, client_address = self.SERVER.accept()
            print('%s:%s has connected.' % client_address)
            player = Player(client_address, socket)
            self.send_message(socket, 'clrscrn')
            self.send_message(socket, welcome)
            Thread(target = handle_client, args = (self, player,)).start()

def handle_client(self, player):
        player.name = self.get_response(player.socket)
        self.clients[player.socket] = player.name #for tuple socket addresses
        self.players.append(player) #for the players
        index = len(self.players) - 1
        self.broadcast(f'{player.name} has joined the game -- type ready when you\'re set to play.')
        while self.get_response(player.socket) != 'ready':
            self.players[index].state = False
        self.players[index].state = True
        self.attempt_start()

class Player:
    state = False #ready to play? yes or no
    cards = {}
    is_playing = True
    
    hand_value = 0
    def __init__(self, address, socket):
        self.address = address
        self.socket = socket

if __name__ == '__main__':
    GameManager()
