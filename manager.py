from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from dealer import Dealer
import os

class GameManager:
    def attempt_start(self):
        while True:
            if len(self.players) < 2:
                self.broadcast('\nNot enough players yet\nEncourage your opponents to ready up.\n')
                break
            for player in self.players:
                if player.state != True:
                    self.broadcast('Someone in the match is not ready')
                    return
            self.begin_game()

    def begin_game(self):
        self.broadcast('Welcome to blackjack. Lets begin.')
        self.broadcast(self.dealer.inital_dcards())
        for player in self.players:
            self.send_message(player.socket, self.dealer.inital_pcards(player), 'Your cards are:\n')
            self.ace_check(player)
            player.hand_value = self.dealer.get_value(player)
        self.play()

    def play(self):
        for player in self.players:
            self.send_message(player.socket, 'Your hand adds up to {}\nWould you like a hit? (y/n)'.format(player.hand_value))
            response = self.get_response(player.socket)
            while response == 'Y' or response == 'y':
                additional_card = self.dealer.deal_card()
                self.send_message(player.socket, f'\nThe dealer gives you the following card:\n\t{additional_card.description()}\n')
                self.ace_check(player)
                player.cards.append(additional_card)
                self.send_message(player.socket, 'Would you like a hit? (y/n)')
                response = self.get_response(player.socket)
        while True:
            next_move = self.dealer.next_dmove()
            if 'done' in next_move:
                break
            self.broadcast(next_move)
        self.end_game()

    def end_game(self):
        for player in self.players:
            self.broadcast(f'\n{player.name}\'s final score:\n{player.hand_value}')
        self.broadcast(f'The dealer\'s final score was {self.dealer.hand_value}')

    def ace_check(self, player):
        for index, card in enumerate(player.cards):
            if card.kind == 'Ace':
                self.send_message(player.socket, '\n{}You were dealt an Ace\n\nYou must make a decision.\nWill the Ace\'s value be 1 or 11? (default = 11)')
                value = self.get_response(player.socket)
                player.cards[index].value = 1 if value == '1' else 11

    def send_message(self, socket, msg, prefix = ''):
        message = prefix + msg
        socket.send(bytes(message, 'utf8'))
    
    def broadcast(self, msg, prefix = ''):
        message = bytes(prefix, 'utf8') + bytes(msg, 'utf8')
        for sock in self.clients:
            sock.send(message)
    
    def get_response(self, socket):
        message = socket.recv(1024).decode("utf8")
        return message

    
    def __init__(self):
        os.system('clear') #clear the screen (Linux)
        self.clients = {}
        self.players = []
        self.HOST = '127.0.0.1'
        self.PORT = 33000
        self.ADDR = (self.HOST, self.PORT)
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)
        self.dealer = Dealer()
        _max = int(input('Max connections: ') or '5')
        self.SERVER.listen(_max)
        print('Waiting for connections...')
        ACCEPT_THREAD = Thread(target = self.accept_new_connection)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()
        self.attempt_start()

    def accept_new_connection(self):
        divider = '🂡  🂢  🂣  🂤  🂥  🂦  🂧  🂨  🂩  🂪  🂡  🂢  🂣  🂤'
        welcome = f'{divider}\n\n\tWELCOME TO BLACKJACK\n\n{divider}\n\n\nPlease enter your name:'
        while True:
            socket, client_address = self.SERVER.accept()
            print("%s:%s has connected." % client_address)
            player = Player(client_address, socket)
            self.send_message(socket, 'clrscrn')
            self.send_message(socket, welcome)
            Thread(target = handle_client, args = (self, player,)).start()

def handle_client(self, player):
        player.name = self.get_response(player.socket)
        self.clients[player.socket] = player.name #for tuple socket addresses
        self.players.append(player) #for the players
        index = len(self.players) - 1
        self.broadcast(f'{player.name} has joined the game!')
        self.send_message(player.socket, 'Type ready when ready.')
        while self.get_response(player.socket) != 'ready':
            self.players[index].state = False
        self.players[index].state = True
        self.attempt_start()

class Player:
    state = False #ready? yes or no
    cards = {}
    
    hand_value = 0
    def __init__(self, address, socket):
        self.address = address
        self.socket = socket

if __name__ == '__main__':
    GameManager()
