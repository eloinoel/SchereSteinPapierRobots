import os
import sys
from os import listdir
import numpy as np
from kinematics.inverse_kinematics import InverseKinematicsAgent
import socket

#server
class GameInitiatorAgent(InverseKinematicsAgent):
    HOST = '127.0.0.1'  #localhost
    PORT = 9000

    def __init__(self):
        return

    #open a port and server for an enemy player to connect to
    def open_lobby(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print("Opened rock-paper-scissors lobby on " + self.HOST + ":" + str(self.PORT))
            conn, addr = s.accept() #blocks and waits for incoming connection
            with conn:
                print('Connected by', addr)


        print('Closed rock-paper-scissors lobby')
        return

class ParticipantAgent(InverseKinematicsAgent):
    def __init__(self):
        return

    def join_lobby(self):
        return

class GameManager:
    '''
    Manages Rock-Paper-Scissors games between agents
    Functions can be used by buttons in UI
    '''
    def __init__(self):
        # initialize Agents
        return

    def start_game(self):
        #Call Agent methods for Handshake
        return

if __name__ == '__main__':
    # agent.__dict__
    game = GameManager()
    game.start_game()