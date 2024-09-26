import pygame
import json
import socket
from network import Network
pygame.font.init()


def send_game_state_to_ai(game_state):
    """Send the game state to the Java AI server and receive the AI's move."""
    host = 'localhost'
    port = 5065  # Port for the AI Bot
    print("I am inside the method" )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("socket erstellt and connected")
        #game_state_json = json.dumps(game_state) + '\n'
        game_state_json = game_state
        print("socket sent" + game_state_json )
        #sock.sendall((game_state_json).encode('utf-8'))
        sock.send((game_state_json + '\n').encode())
        print("socket sent" )
        move = sock.recv(1024).decode()
        print("socket received" ) # Receive the move from the AI
        return move

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    is_blue=True

    while run:
        clock.tick(60)
        try:
            #try to send get as a json to server over network, rest is error handling
            game = n.send(json.dumps("get"))
            if game is None:
                raise ValueError("Game data is None")
        except:
            run = False
            print("Couldn't get game")
            break

        #response is also a json, json.loads transforms into a python dictionary
        #dictionary consists of board string, a variable player1 which is true, when player 1 (or better 0),
        #variable player2 with the same concept and bothConnected, also a boolean
        game = json.loads(game)

        #allow input just when both players are in
        if game["bothConnected"]:


            if is_blue:
                # Swap the logic for player 1 and player 2
                if player == 0 and game["player1"]:
                    print("New Board: " + game["board"])
                    move = input("Enter your move: ")
                    n.send(json.dumps(move))
                elif player == 1 and game["player2"]:
                    print("New Board: " + game["board"])
                    print("Warning: Received empty game data")
                    move = send_game_state_to_ai(game["board"])
                    n.send(json.dumps(move))
                    print("AI move: " + move)
            else:
                if player == 0 and game["player1"]:
                    print("New Board: " + game["board"])
                    print("Warning: Received empty game data")
                    move = send_game_state_to_ai(game["board"])
                    print("AI move: " + move)
                    n.send(json.dumps(move))
                elif player == 1 and game["player2"]:
                    print("New Board: " + game["board"])
                    move = input("Enter your move: ")
                    n.send(json.dumps(move))

                #allow to only give input, when it is your turn
                # Player 0 (Me)


while True:
    main()
