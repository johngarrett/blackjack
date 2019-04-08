## Instructions
1. run `manager.py`
2. run `client.py`

The manager acts as the server, `client.py` is what each user should run.

Hitting return on initial inputs for both files uses default values that should set everything automatically. 

## Info
#### Manager.py
This file manages both the game and the server.

 All clients are connected to the host’s IP address “127.0.0.1” through port 33000. The server is initialized and bound to that socket address and then connections are handled.

The exception function happens on another thread and is always listening for new connections. Once a client connects, they are greeted and added to the player array. Once they are added to the player array, attempt_start() is called to try and begin the game. 

Each player has a state (are they ready to play?), cards, and a socket address. 

Once attempt_start is called, each player in the player array is checked to see if they are ready. If they aren’t ready (which can occur when they are waiting for other players to join), a message is sent to all the clients saying the game cannot begin. 

If the game can begin, begin_game() is called. The screen is cleared on the client’s screens and the dealer begins to deal cards. The initial cards the dealer gives out is presented to the clients and the dealer’s cards are broadcasted to all. Once the game has begun, play() is called.

Once play() is called, the other players are told who is currently playing. The current player’s cards are dealt by the dealer and presented to them. They are then prompted if they want another card or not. Once the player declines another card, end_game_for_player() is called. When all players are done, end_game() is called. 

To send messages to users, there are two functions -- send_message(socket, msg, prefix) and broadcast(msg, prefix). Broadcast goes through all the players and sends the same message out to all of them. Send_message sends a private message to the one player specified in the parameter. 

get_response(socket) is a function that is called when the manager expects input from the users. Previously this was always listening but to reduce overhead, this is only called when we are promoting a client for input. The message is received from the client’s socket with a buffer size of 1024 and decoded as utf8 (this way, we can have Unicode cards, flags, etc). 

#### Client.py
Client.py is what each player runs. The host’s socket address is asked for (default values are provided) and then the client is connected to the server. On joined threads, send and receive is called. Sending takes any input from the user and sends them encoded as utf8 bytes to the server. The receive function is always running and decoding the messages from the server. If the message is invalid, the function returns. If the message is “clrscrn”, the client’s screen is cleared of all characters (this is good for formatting). If the previous conditions are false, the message is displayed on the client’s screen. 
