import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'software_installation'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'joint_control'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'distributed_computing'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'introduction'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'kinematics'))
from os import listdir
import numpy as np
from kinematics.inverse_kinematics import InverseKinematicsAgent
import socket
import time
import threading

'''
Server: Agent that listens for an incoming connection to play rock-paper-scissors with
'''
class GameInitiatorAgent(InverseKinematicsAgent):
    HOST = '127.0.0.1'  #localhost
    PORT = 9000

    def __init__(self):
        return

    '''
    start a game socket for game communication
    '''
    def open_lobby(self, host=HOST, port=PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print("Opened rock-paper-scissors lobby on " + host + ":" + str(port))
            conn, addr = s.accept() #blocks and waits for incoming connection
            with conn:
                print('Connected by', addr)
                while True: #receive data and do something with it

                    #TODO: evaluate incoming messages

                    data = conn.recv(512)
                    print('Server:Received data: ' + repr(data))
                    if not data:
                        break
                    conn.sendall(data)


        print('Closed rock-paper-scissors lobby')
        return

'''
Client: Agent that connects to the server to play a game of rock-paper-scissors
'''
class ParticipantAgent(InverseKinematicsAgent):
    def __init__(self):
        return

    '''
    connect to the server's socket to play rock-paper-scissors
    '''
    def join_lobby(self, host='127.0.0.1', port=9000):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(b'Hello I am a lobot beep bop!')
            data = s.recv(1024)

            #TODO: Interaction protocol

        print('Client:Received: ' + repr(data))
        return

'''
Call functions of the two players
Sync the network communication with simspark robot animations
Functions can be used in the UI
'''
class GameManager:


    def __init__(self):
        # initialize Agents
        self.bob = GameInitiatorAgent()
        self.alice = ParticipantAgent()
        return

    #start a game between bob and alice
    def start_game(self):
        #Call Agent methods for Handshake
        try:
            thread = threading.Thread(target=self.bob.open_lobby)
            thread.start()
        except KeyboardInterrupt:
            print('Interrupted server-lobby')
        time.sleep(0.01)
        self.alice.join_lobby()
        print("Game finished.")
        return

    '''
    play 'rock', 'paper' or 'scissors'
    '''
    def play(self, symbol):
        #TODO: Play Keyframe and send signals afterwards
        if symbol == 'rock':
            return
        elif symbol == 'paper':
            return
        elif symbol == 'scissors':
            return
        else:
            print('Unknown symbol: ' + str(symbol) + ", play either 'rock', 'paper' or 'scissors'")


if __name__ == '__main__':
    # agent.__dict__
    # dir(agent)
    game = GameManager()
    game.start_game()