#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import random

# Define the server host and port
HOST = 'localhost'
PORT = 8000

# Create a TCP socket and bind it to the host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Define the card suits and values
card_suit = 'Spades'
card_values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

# Initialize the score card
score_card = {1: 0, 2: 0, 3: 0}

# Define the number of rounds
num_rounds = 13

# Define a list to keep track of the cards used by the server
used_cards = []


# Function to get a random card from the server's suit
def get_server_card():
    while True:
        card = (random.choice(card_values), card_suit)
        if card not in used_cards:
            used_cards.append(card)
            return card


# Function to determine the winner of a round and update the score card
def update_score_card(server_card, client_cards):
    card_numbers=[]
    for j in client_cards:
        card_numbers.append(j[0])
        
    winning_card = max(card_numbers)
    print(winning_card)
    if client_cards.count(winning_card) == 1:
        winner = client_cards.index(winning_card) + 1
        score_card[winner] += card_values.index(server_card[0]) + 1
        print(f"Winner of the round: Client {winner}")
    else:
        winners = [i + 1 for i, card in enumerate(card_numbers) if card == winning_card]
        points = card_values.index(server_card[0]) + 1
        for winner in winners:
            score_card[winner] += points
        print(f"Winners of the round: Clients {', '.join(map(str, winners))}")


def send_score_card(clients):
    for client_socket in clients:
        score_card_str = "\n".join([f"Client {i}: {score}" for i, score in score_card.items()])
        client_socket.sendall(f"\nScore card:\n{score_card_str}\n".encode())


# Accept three client connections
print('Waiting for clients to connect...')
clients = []
for i in range(3):
    client_socket, address = server_socket.accept()
    clients.append(client_socket)
    print(f'Client {i + 1} connected from {address}')

# Play the game for the specified number of rounds
for round_num in range(num_rounds):
    print(f'Round {round_num + 1}')

    # Get a card from the server's suit
    server_card = get_server_card()
    
    print(f'Server card: {server_card}')

    # wait for each client to send a card
    client_cards = []
    for i, client_socket in enumerate(clients):
        client_socket.sendall(f'Server card: {server_card}'.encode())
        while True:
            data = client_socket.recv(1024).decode()
            if data:
                card = tuple(data.split(","))
                print(card)
                if card not in client_cards:
                    client_cards.append(card)
                    break
                else:
                    client_socket.sendall(b"Invalid card, please send a new card\n")
            else:
                break
        print(f"Client {i + 1} card: {card}")

    # Determine the winner of the round and update the score card
    update_score_card(server_card, client_cards)
    send_score_card(clients)

# Determine the winner of the game
max_score = max(score_card.values())
#print(winners)

# determine the winner of the game and send it to all clients
game_winner = max(score_card, key=score_card.get)
for client_socket in clients:
    client_socket.sendall(f"\nGame winner: Client {game_winner}\n".encode())
    


# In[ ]:




