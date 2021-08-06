import os
import sys
import types
import random

sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'software_installation'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'joint_control'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'distributed_computing'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'introduction'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'kinematics'))
from os import listdir
import numpy as np
from kinematics.inverse_kinematics import InverseKinematicsAgent
import socket
import selectors
import time
import threading

CONNECT_FLAG = 1
REFUSE_ACCEPT_FLAG = 2
READY_FLAG = 3
PLAY_FLAG = 4
START_FLAG = 5
DONE_FLAG = 6
RESULT_FLAG = 7

'''
Server: Agent that listens
for an incoming connection to play rock-paper-scissors 
'''
class GameServer():
    HOST = '127.0.0.1'  # localhost
    PORT = 9000


    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.lobby_full = False
        self.lobby = []
        self.plays = []
        self.done = 0
        self.setup_listen_socket()
        return

    '''
    socket to receive messages on
    '''
    def setup_listen_socket(self, host=HOST, port=PORT):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print('listening on ' + str((host, port)))
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)   #register socket to be monitored with sel.select()

    def server_loop(self):
        while True:
            events = self.sel.select(timeout=None)  #returns (key, events) tuple list, each is one socket
            for key, mask in events:
                if key.data is None:    #if key==None, we need to accept() and create new I/O socket for connection
                    self.accept_connection(key.fileobj)
                else:                   #do something on socket
                    self.service_connection(key, mask)

    '''
    accept an incoming connection by creating a new socket for the communication
    '''
    def accept_connection(self, sock):
        conn, addr = sock.accept()
        print('Server: accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')  #object to hold data we want included along with socket
        events = selectors.EVENT_READ | selectors.EVENT_WRITE   #want to know when client is ready for reading and writing
        self.sel.register(conn,events, data=data)

        return
    
    def get_socket_from_id(self, id):
        for player in self.lobby:
            if player[0] == id:
                return player[1]
        return None

    '''
    Do stuff according to message type
    '''
    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1)
            '''
            if recv_data:
                data.outb += recv_data'''
            '''
            print('DEBUG msg: ' + repr(bin(ord(recv_data))))
            print('DEBUG shift: ' + repr(bin((recv_data[0] >> 4))))
            print('DEBUG and: ' + repr(bin((recv_data[0] >> 4) & DONE_FLAG)))
            print('DEBUG and: ' + repr(bin((recv_data[0] >> 4) & PLAY_FLAG)))
            '''
            if recv_data:
                if (recv_data[0] >> 4) == CONNECT_FLAG:
                    # accept players into the lobby and start the game if full
                    self.eval_connect_message(sock, recv_data)

                elif (recv_data[0] >> 4) == PLAY_FLAG:
                    # receive plays of the participants and tell them to start animation
                    self.eval_play_message(recv_data)

                elif (recv_data[0] >> 4) == DONE_FLAG:
                    # send results and close connections
                    self.eval_done_message()

                else:
                    print('Server: received unknown message: ' + str(recv_data[0]))

            else:  # client closed connection
                print('One participant disconnected, resetting...')
                self.reset_everything()

        '''if mask & selectors.EVENT_WRITE:
            if data.outb:
                #TODO
                print('echoing ', repr(data.outb), ' to ', data.addr)
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]'''

        return

    def eval_connect_message(self, sock, recv_data):
        print('Server: received Connect')
        if self.lobby_full:  # send refuse
            refuse_msg = 32  # 0010 0000
            print('Server: sending Refuse')
            sock.send(refuse_msg.to_bytes(1, 'big'))
        else:
            id = (recv_data[0] >> 2) & 3
            self.lobby += [(id, sock)]
            accept_msg = 40  # 0010 1000
            print('Server: sending accept to client with id' + str(id))
            sock.send(accept_msg.to_bytes(1, 'big'))
            # start game if we have 2 players
            if len(self.lobby) >= 2:
                self.lobby_full = True
                ready_msg = 48  # 0011 0000
                print('Server: sending ready to clients...')
                for player in self.lobby:
                    player[1].send(ready_msg.to_bytes(1, 'big'))

        return
                    
    def eval_play_message(self, recv_data):
        id = (recv_data[0] >> 2) & 3
        play_tmp = recv_data[0] & 3
        print('Server: received Play (' + str(id) + ', ' + str(play_tmp) + ')')
        self.plays += [(id, play_tmp)]
        # both players sent their plays for this turn
        if len(self.plays) >= 2:
            print('DEBUG plays')
            print(self.plays)
            start_message = 80
            print('Server: sending start to clients...')
            for player in self.lobby:
                player[1].send(start_message.to_bytes(1, 'big'))
        return

    def eval_done_message(self):
        print('Server: received Done, sending results...')
        self.done += 1
        # calculate result
        if self.done >= 2:
            result_message = 112
            # tie
            if self.plays[0][1] == self.plays[1][1]:
                result_message = result_message | 8
                for player in self.lobby:
                    player[1].send(result_message.to_bytes(1, 'big'))
            # first player wins
            elif (self.plays[0][1] > self.plays[1][1]) or (self.plays[0][1] == 0 and self.plays[1][1] == 2):
                id_player0 = self.plays[0][0]
                id_player1 = self.plays[1][1]
                socket_player0 = self.get_socket_from_id(id_player0)
                socket_player1 = self.get_socket_from_id(id_player1)

                if socket_player0 != None and socket_player1 != None:
                    win_message = result_message | 4
                    lose_message = result_message
                    socket_player0.send(win_message.to_bytes(1, 'big'))
                    socket_player1.send(lose_message.to_bytes(1, 'big'))
                else:
                    print('Server: Error sending result, sockets NULL')


            elif (self.plays[0][1] < self.plays[1][1]) or (self.plays[0][1] == 2 and self.plays[1][1] == 0):
                id_player0 = self.plays[0][0]
                id_player1 = self.plays[1][1]
                socket_player0 = self.get_socket_from_id(id_player0)
                socket_player1 = self.get_socket_from_id(id_player1)

                if socket_player0 != None and socket_player1 != None:
                    win_message = result_message | 4
                    lose_message = result_message
                    socket_player0.send(lose_message.to_bytes(1, 'big'))
                    socket_player1.send(win_message.to_bytes(1, 'big'))
                else:
                    print('Server: Error sending result, sockets NULL')

            else:
                print('Server: Calculating result went not as expected')

            # close connections and delete stuff from data structures
            self.reset_everything()

            return

    '''
    reset
    '''
    def reset_everything(self):
        for player in self.lobby:
            self.sel.unregister(player[1])
            player[1].close()

        self.lobby_full = False
        self.lobby = []
        self.plays = []
        self.done = 0





'''
Client: Agent that connects to the server to play a game of rock-paper-scissors
'''
class ParticipantAgent(InverseKinematicsAgent):
    REMOTEHOST = '127.0.0.1'  # localhost
    REMOTEPORT = 9000

    def __init__(self, id):
        self.id = id
        self.nextMove = 'undecided_move'
        return

    '''
    execute the Participant Agent
    '''
    def run(self):
        s = self.setup_socket()
        self.join_lobby(s, '127.0.0.1', 9000)
        self.decide(s)
        self.play(s)
        self.react(s)
        return

    def setup_socket(self):
        print("Client "+str(self.id)+" opening socket")
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    '''
    connect to the server's socket to play rock-paper-scissors
    '''
    def join_lobby(self, s, host=REMOTEHOST, port=REMOTEPORT):

        # connect to server
        s.connect((host, port))
        print("Client "+str(self.id)+" connected to host "+str(host)+" on port "+str(port))
        # send connection
        msg = composeMessage(CONNECT_FLAG, self.id)
        print("Client "+str(self.id)+" sending CONNECT with ID: " + str(self.id))
        s.send(msg)
        # wait for accept/refuse
        flag, bool = decomposeMessage(s.recv(1))

        print("Client "+str(self.id)+" received: " + flag_toString(flag) + " " + str(bool == 1))
        # TODO: Handle Refuse/No response
        if(bool != 1):
            print("Client "+str(self.id)+" REFUSED")
            print("Client "+str(self.id)+" terminating...")
            exit(-1)
        return

    '''
    decide whether to play 'rock', 'paper' or 'scissors'
    '''
    def decide(self, s):
        # blocking wait for servers call for move
        while True:
            flag = decomposeMessage(s.recv(1))
            print("Client " + str(self.id) + " received: " + flag_toString(flag))
            if (flag == READY_FLAG): break
            # TODO: Handle Abort/No response

        symbol = -1  # 'undecided_move'
        # TODO: Play Keyframe and send signals afterwards
        r = random.randrange(0.0, 1.0)
        if (r < 0.33):
            symbol = 0
            self.nextMove = 'rock'
        elif (r < 0.67):
            symbol = 1
            self.nextMove = 'paper'
        else:
            symbol = 2
            self.nextMove = 'scissors'

        msg = composeMessage(PLAY_FLAG, self.id, 0, symbol)
        print("Client " + str(self.id) + " sending PLAY with ID: " + str(self.id) + ", MOVE: " + symbol_toString(symbol))
        s.send(msg)

    '''
    play the predetermined move
    '''
    def play(self, s):
        # blocking wait for servers start gesture
        while True:
            flag = decomposeMessage(s.recv(1))
            print("Client " + str(self.id) + " received: " + flag_toString(flag))
            if(flag == START_FLAG): break
            # TODO: Handle No response

        if(self.nextMove == 'rock'):
            print("TODO: set rock-keyframes")
        elif(self.nextMove == 'paper'):
            print("TODO: set paper-keyframes")
        elif(self.nextMove == 'scissors'):
            print("TODO: set scissors-keyframes")
        time.sleep(5)

        msg = composeMessage(DONE_FLAG)
        print("Client " + str(self.id) + " sending DONE")
        #print(repr(bin(ord(msg))))
        s.send(msg)

    '''
    show happiness/sadness for a win/loss
    '''
    def react(self, s):
        flag, won = decomposeMessage(s.recv(1))
        print("Client " + str(self.id) + " received:" + flag_toString(flag) + " WON: " + str(won==1) + " TIE: " + str(won==2))

        # TODO: Play win/lose keyframes
        return

'''
Call functions of the two players
Sync the network communication with simspark robot animations
Functions can be used in the UI
'''
class GameManager:


    def __init__(self):
        # initialize Agents
        self.server = GameServer()
        self.bob = ParticipantAgent(1)
        self.alice = ParticipantAgent(2)
        #TODO: position and rotation in front of each other
        return

    #start a game between bob and alice
    def start_game(self):
        #Call Agent methods for Handshake
        try:
            thread = threading.Thread(target=self.server.server_loop)
            thread.start()
        except KeyboardInterrupt:
            print('Interrupted server-lobby')
        time.sleep(0.01)

        try:
            thread2 = threading.Thread(target=self.bob.run)
            thread2.start()
        except KeyboardInterrupt:
            print('Interrupted Client')

        try:
            thread3 = threading.Thread(target=self.alice.run)
            thread3.start()
        except KeyboardInterrupt:
            print('Interrupted Client')

        return

def composeMessage(flag, id=0, bool=0, move=0):
    # set flag field
    msg = flag << 4

    # set id field
    if(flag == CONNECT_FLAG or flag == PLAY_FLAG):
        msg = msg | (id << 2)

    # set true/false field
    if(flag == REFUSE_ACCEPT_FLAG):
        msg = msg | (bool << 3)

    # set true/false field
    if(flag == RESULT_FLAG):
        msg = msg | (bool << 2)

    # set move field
    if(flag == PLAY_FLAG):
        msg = msg | move

    return msg.to_bytes(1, 'big')

def decomposeMessage(msg):
    msg = int.from_bytes(msg, 'big')
    flag = (msg & 240) >> 4
    if(flag == CONNECT_FLAG):
        id = (msg & 12) >> 2
        return flag, id

    if(flag == REFUSE_ACCEPT_FLAG):
        bool = (msg & 8) >> 3
        return flag, bool

    if(flag == RESULT_FLAG):
        bool = (msg & 12) >> 2
        return flag, bool

    if(flag == PLAY_FLAG):
        id = (msg & 12) >> 2
        move = (msg & 3)
        return flag, id, move

    return flag

def flag_toString(flag):
    if(flag == CONNECT_FLAG):
        return "CONNECT"
    elif(flag == REFUSE_ACCEPT_FLAG):
        return "REFUSE_ACCEPT"
    elif (flag == READY_FLAG):
        return "READY"
    elif (flag == PLAY_FLAG):
        return "PLAY"
    elif (flag == START_FLAG):
        return "START"
    elif (flag == DONE_FLAG):
        return "DONE"
    elif (flag == RESULT_FLAG):
        return "RESULT"
    else:
        return "FLAGNOTFOUND"

def symbol_toString(symbol):
    if(symbol == 0):
        return "Rock"
    elif(symbol == 1):
        return "Paper"
    elif(symbol == 2):
        return "Scissors"
    else:
        return "NOTFOUND"    

if __name__ == '__main__':
    # agent.__dict__
    # dir(agent)
    game = GameManager()
    game.start_game()