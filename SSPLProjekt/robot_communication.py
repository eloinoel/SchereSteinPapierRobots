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
from new_keyframes import *

import PySimpleGUI as sg


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
        self.lobby = [] #(id, socket)
        self.plays = [] #id, play
        self.plays_submitted = False
        self.done = 0
        self.gui = None
        self.setup_listen_socket()
        return

    def set_gui(self, gui):
        self.gui = gui

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
            if recv_data:
                if (recv_data[0] >> 4) == CONNECT_FLAG:
                    # accept players into the lobby and start the game if full
                    self.eval_connect_message(sock, recv_data)

                elif (recv_data[0] >> 4) == PLAY_FLAG:
                    # receive plays of the participants and tell them to start animation
                    self.eval_play_message(sock, recv_data)

                elif (recv_data[0] >> 4) == DONE_FLAG:
                    # send results and close connections
                    self.eval_done_message()

                else:
                    print('Server: received unknown message: ' + str(recv_data[0]))

            else:  # client closed connection
                print(c.OKGREEN + 'One participant disconnected, resetting...' + c.ENDC)
                self.reset_everything()
        return

    def eval_connect_message(self, sock, recv_data):
        print(c.OKGREEN + 'Server: received Connect' + c.ENDC)
        if self.lobby_full:  # send refuse
            refuse_msg = 32  # 0010 0000
            print(c.OKGREEN + 'Server: sending Refuse' + c.ENDC)
            sock.send(refuse_msg.to_bytes(1, 'big'))
        else:
            id = (recv_data[0] >> 2) & 3
            self.lobby += [(id, sock)]
            accept_msg = 40  # 0010 1000
            print(c.OKGREEN + 'Server: sending accept to client with id: ' + str(id) + c.ENDC)
            sock.send(accept_msg.to_bytes(1, 'big'))

            #Players joined in GUI
            if self.gui != None:
                self.gui.set_agents_joined(len(self.lobby))

            # start game if we have 2 players
            if len(self.lobby) >= 2:
                self.lobby_full = True
                ready_msg = 48  # 0011 0000
                print(c.OKGREEN + 'Server: sending ready to clients...\n' + c.ENDC)
                for player in self.lobby:
                    player[1].send(ready_msg.to_bytes(1, 'big'))
        return
                    
    def eval_play_message(self, sock, recv_data):
        # block unwanted behavior
        if self.plays_submitted:
            refuse_msg = 32
            print(c.OKGREEN + 'Server sending Refuse' + c.ENDC)
            sock.send(refuse_msg.to_bytes(1, 'big'))
            return

        # evaluate message
        id = (recv_data[0] >> 2) & 3
        play_tmp = recv_data[0] & 3
        print(c.OKGREEN + 'Server: received Play (' + str(id) + ', ' + str(play_tmp) + ')' + c.ENDC)
        self.plays += [(id, play_tmp)]
        # both players sent their plays for this turn
        if len(self.plays) >= 2:
            self.plays_submitted = True
            start_message = 80
            print(c.OKGREEN + 'Server: sending start to clients...\n' + c.ENDC)
            for player in self.lobby:
                player[1].send(start_message.to_bytes(1, 'big'))
        return

    def eval_done_message(self):
        print(c.OKGREEN + 'Server: received Done' + c.ENDC)
        self.done += 1
        # calculate and send result when received done from both players (doesn't verify id's)
        if self.done >= 2:
            result_message = 112
            print(c.OKGREEN + 'Server: sending results...\n' + c.ENDC)

            #show result in GUI
            if self.gui != None:
                self.gui.set_pOne(self.numberToPlay(self.plays[0][1]))
                self.gui.set_pTwo(self.numberToPlay(self.plays[1][1]))

            # tie
            if self.plays[0][1] == self.plays[1][1]:
                result_message = result_message | 8
                for player in self.lobby:
                    player[1].send(result_message.to_bytes(1, 'big'))
            # first player wins
            elif (self.plays[0][1] > self.plays[1][1]) or (self.plays[0][1] == 0 and self.plays[1][1] == 2):
                id_player0 = self.plays[0][0]
                id_player1 = self.plays[1][0]
                socket_player0 = self.get_socket_from_id(id_player0)
                socket_player1 = self.get_socket_from_id(id_player1)

                if socket_player0 != None and socket_player1 != None:
                    win_message = result_message | 4
                    lose_message = result_message
                    '''print('Player 0 id:' + str(id_player0))
                    print(repr(bin(win_message)))
                    print(repr(bin(lose_message)))'''
                    socket_player0.send(win_message.to_bytes(1, 'big'))
                    socket_player1.send(lose_message.to_bytes(1, 'big'))
                else:
                    print('Server: Error sending result, sockets for id are NULL')
                    print(repr(id_player0) + " " + repr(id_player1))
                    print(self.lobby)


            elif (self.plays[0][1] < self.plays[1][1]) or (self.plays[0][1] == 2 and self.plays[1][1] == 0):
                id_player0 = self.plays[0][0]
                id_player1 = self.plays[1][0]
                socket_player0 = self.get_socket_from_id(id_player0)
                socket_player1 = self.get_socket_from_id(id_player1)

                if socket_player0 != None and socket_player1 != None:
                    win_message = result_message | 4
                    lose_message = result_message
                    '''print('Player 0 id:' + str(id_player0))
                    print(repr(bin(win_message)))
                    print(repr(bin(lose_message)))'''
                    socket_player0.send(lose_message.to_bytes(1, 'big'))
                    socket_player1.send(win_message.to_bytes(1, 'big'))
                else:
                    print('Server: Error sending result, sockets for id are NULL')
                    print(repr(id_player0) + " " + repr(id_player1))
                    print(self.lobby)

            else:
                print('Server: Calculating result went not as expected')

            # close connections and delete stuff from data structures
            time.sleep(0.5)

            self.reset_everything()
            #update gui
            if self.gui != None:
                self.gui.set_agents_joined(len(self.lobby))

            return

    '''
    reset the game server for a new round (reset button in GUI)
    '''
    def reset_everything(self):
        print(c.OKGREEN + 'Server: reset values' + c.ENDC)
        for player in self.lobby:
            self.sel.unregister(player[1])
            player[1].close()

        self.lobby_full = False
        self.lobby = []
        self.plays = []
        self.plays_submitted = False
        self.done = 0

    def numberToPlay(self, play):
        if(play == 0):
            return 'Rock'
        elif(play == 1):
            return 'Paper'
        elif(play == 2):
            return 'Scissors'
        else:
            return ' '





'''
Client: Agent that connects to the server to play a game of rock-paper-scissors
'''
class ParticipantAgent(InverseKinematicsAgent):
    REMOTEHOST = '127.0.0.1'  # localhost
    REMOTEPORT = 9000

    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(InverseKinematicsAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.id = player_id
        self.nextMove = 'undecided_move'
        self.move_GUI = 'undecided_move'
        self.autoPlay = True
        self.gui = None
        return

    def setGui(self, gui):
        self.gui = gui

    '''
    execute the Participant Agent
    '''
    def run_client(self):
        s = self.setup_socket()

        self.join_lobby(s, '127.0.0.1', 9000)
        self.decide(s)
        self.play(s)
        self.react(s)
        self.leave_lobby(s)
        return

    def setup_socket(self):
        print(c.OKBLUE + "Client "+str(self.id)+" opening socket" + c.ENDC)
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    '''
    connect to the server's socket to play rock-paper-scissors
    '''
    def join_lobby(self, s, host=REMOTEHOST, port=REMOTEPORT):

        # connect to server
        s.connect((host, port))
        print(c.OKBLUE + "Client "+str(self.id)+" connected to host "+str(host)+" on port "+str(port) + c.ENDC)
        # send connection
        msg = composeMessage(CONNECT_FLAG, self.id)
        print(c.OKBLUE + "Client "+str(self.id)+" sending CONNECT with ID: " + str(self.id) + c.ENDC)
        s.send(msg)
        # wait for accept/refuse
        flag, bool = decomposeMessage(s.recv(1))

        print(c.OKBLUE + "Client "+str(self.id)+" received: " + flag_toString(flag) + " " + str(bool == 1) + c.ENDC)
        # TODO: Handle Refuse/No response
        if(bool != 1):
            print(c.WARNING + "Client "+str(self.id)+" REFUSED" + c.ENDC)
            print(c.WARNING + "Client "+str(self.id)+" terminating..." + c.ENDC)
            exit(-1)
        return

    '''
    decide whether to play 'rock', 'paper' or 'scissors'
    '''
    def decide(self, s):
        # blocking wait for servers call for move
        while True:
            flag = decomposeMessage(s.recv(1))
            print(c.OKBLUE + "Client " + str(self.id) + " received: " + flag_toString(flag) + c.ENDC)
            if (flag == READY_FLAG): break
            # TODO: Handle Abort/No response

        if(self.autoPlay):
            symbol = -1  # 'undecided_move'
            # TODO: Play Keyframe and send signals afterwards
            r = random.random()
            if (r < 0.33):
                self.nextMove = "Rock"
            elif (r < 0.67):
                self.nextMove = "Paper"
            else:
                self.nextMove = "Scissors"
        # take input from GUI
        else:
            # Wait until self.move_GUI is set
            while True:
                if (self.move_GUI != 'undecided_move'):
                    break
            self.nextMove = self.move_GUI
            # TODO: reset self.move_GUI for each new round of rock, paper, scissors


        symbol = string_toSymbol(self.nextMove)
        msg = composeMessage(PLAY_FLAG, self.id, 0, symbol)
        print(c.OKBLUE + "Client " + str(self.id) + " sending PLAY with ID: " + str(self.id) + ", MOVE: " + symbol_toString(symbol) + c.ENDC)
        s.send(msg)

    '''
    play the predetermined move
    '''
    def play(self, s):
        # blocking wait for servers start gesture
        while True:
            flag = decomposeMessage(s.recv(1))
            print(c.OKBLUE + "Client " + str(self.id) + " received: " + flag_toString(flag) + c.ENDC)
            if(flag == START_FLAG): break
            # TODO: Handle No response

        # Set keyframes
        self.setKeyframe(self.nextMove)

        msg = composeMessage(DONE_FLAG)
        print(c.OKBLUE + "Client " + str(self.id) + " sending DONE" + c.ENDC)
        #print(repr(bin(ord(msg))))
        s.send(msg)

    '''
    show happiness/sadness for a win/loss
    '''
    def react(self, s):
        while True:
            flag, won = decomposeMessage(s.recv(1))
            #print("Client " + str(self.id) + " received: " + flag_toString(flag))
            if(flag == RESULT_FLAG): break
        print(c.OKBLUE + "Client " + str(self.id) + " received:" + flag_toString(flag) + " WON: " + str(won==1) + " TIE: " + str(won==2) + c.ENDC)

        #Play win/lose keyframes
        if(won == 2 or won != 1):
            # Loser
            self.setKeyframe('Lose')
        elif(won == 1):
            # Winner
            self.setKeyframe('Win')
        else:
            print("Client Error: didn't know which animation to play")
        return

    def leave_lobby(self, s):
        print(c.OKBLUE + "Client " + str(self.id) + " closing socket" + c.ENDC)
        s.close()
        self.nextMove = 'undecided_move'
        return

    '''
    User clicks on a move to play in the GUI
    '''
    def setMove(self, move):
        self.move_GUI = move
        return

    '''
    Whether a move is selected randomly or by the player in the GUI
    '''
    def setAutoPlay(self, boolean):
        self.autoPlay = boolean
        return

    def setKeyframe(self, keyframe):
        #TODO: reset time of keyframes
        while(self.keyframes != ([], [], [])):
            time.sleep(0.1)

        self.start_time = self.perception.time

        if (keyframe == "Rock"):
            print(c.OKBLUE + '** Robot ' + str(self.id) + ' plays rock**' + c.ENDC)
            self.keyframes = Rock()
            #time.sleep(5.2)
            #self.keyframes = ([], [], [])
        elif (keyframe == "Paper"):
            print(c.OKBLUE + '** Robot ' + str(self.id) + ' plays paper**' + c.ENDC)
            self.keyframes = OpenPaper()
            #time.sleep(5.2)
            #self.keyframes = ([], [], [])
        elif (keyframe == "Scissors"):
            print(c.OKBLUE + '** Robot ' + str(self.id) + ' plays scissors**' + c.ENDC)
            self.keyframes = Scissors()
            #time.sleep(5.2)
            #self.keyframes = ([], [], [])
        elif (keyframe == "Win"):
            print(c.OKBLUE + '** Robot ' + str(self.id) + ' won!**' + c.ENDC)
            self.keyframes = Win()
            #time.sleep(3.2)
            #self.keyframes = ([], [], [])
        elif (keyframe == "Lose"):
            print(c.OKBLUE + '** Robot ' + str(self.id) + ' is sad :(**' + c.ENDC)
            self.keyframes = Sad()
            #time.sleep(3.2)
            #self.keyframes = ([], [], [])
        else:
            print(c.OKBLUE + '** Robot ' + str(self.id) + 'is doing nothing**' + c.ENDC)
            self.keyframes = default_pose()

'''
GUI for graphical interaction with the server and clients
'''
class GUI():
    def __init__(self, gameManager):
        self.GameManager = gameManager

    def set_layout(self):
        image_schere = './ButtonGraphics/schere.png'
        image_stein = './ButtonGraphics/stein.png'
        image_papier = './ButtonGraphics/papier.png'
        #image_start = './ButtonGraphics/start.png'

        first_column = [
            #[sg.Button(button_color=sg.TRANSPARENT_BUTTON,image_filename=image_start,image_size=(70, 70),image_subsample=8,size = (7,7))],
            #[sg.Button(button_text="Create Lobby",)],


            [sg.Text("Autoplay:"),sg.Button('On',size=(3,1),button_color=('white', 'green'),key='_B_')],
            [sg.Text(text="Select Move"),],
            [
                sg.Button(
                    button_color=sg.TRANSPARENT_BUTTON,image_filename=image_schere,
                    image_size=(50,50),image_subsample=12,disabled=True,key="_scissor_"),
                sg.Button(button_color=sg.TRANSPARENT_BUTTON,image_filename=image_stein,
                          image_size=(50,50),image_subsample=12,disabled=True,key="_rock_"),
                sg.Button(button_color=sg.TRANSPARENT_BUTTON,image_filename=image_papier,
                          image_size=(50,50),image_subsample=12,disabled=True,key="_paper_")
            ]
        ]

        secound_column = [
            [sg.Text(text="Agents joined:")],
            [sg.Text(size=(3,1),key="_jAgents_")],
            [sg.Button(button_text="Play Game",key="_pGame_")],
            [sg.Text(text="Game Result:")],
            [
                sg.Text(text="Player 1:\t"),
                sg.Text(key="_pOne_",size=(10,1)),
                sg.Text(text="Player 2:\t"),
                sg.Text(key="_pTwo_",size=(10,1))
            ]
        ]
        layout = [
            [
                sg.Column(first_column),
                sg.VSeparator(),
                sg.Column(secound_column),
            ]
        ]
        return layout

    def set_window(self):
        # create the window
        window = sg.Window("Play-GUI", self.layout, size=(600, 200), finalize=True)
        return window

    def set_agents_joined(self,agents_joined):
        self.window["_jAgents_"].Update(value=agents_joined)

    def set_pOne(self, value):
        self.window["_pOne_"].Update(value=value)

    def set_pTwo(self, value):
        self.window["_pTwo_"].Update(value=value)

    def event_loop(self):
        down = True
        self.layout = self.set_layout()
        self.window = self.set_window()
        while True:
            event, values = self.window.read()
            # End program if user closes window or press the OK button
            if event in (None, 'Exit'):
                break
            elif event == sg.WIN_CLOSED:
                break
            elif event == '_B_':
                down = not down
                self.window.Element('_B_').Update(('Off', 'On')[down], button_color=(('white', ('red', 'green')[down])))
                self.window["_scissor_"].Update(disabled=down)
                self.window["_rock_"].Update(disabled=down)
                self.window["_paper_"].Update(disabled=down)
                self.GameManager.bob.setAutoPlay(down)
            elif event == '_pGame_':
                print("Start Game")
                self.GameManager.start_game()
                if not down:
                    self.window["_scissor_"].Update(disabled=False)
                    self.window["_paper_"].Update(disabled=False)
                    self.window["_rock_"].Update(disabled=False)

            elif event == '_rock_':
                print("Rock")
                self.GameManager.bob.setMove('Rock')
                self.window["_scissor_"].Update(disabled=True)
                self.window["_paper_"].Update(disabled=True)
            elif event == '_paper_':
                print("Paper")
                self.GameManager.bob.setMove('Paper')
                self.window["_scissor_"].Update(disabled=True)
                self.window["_rock_"].Update(disabled=True)
            elif event == '_scissor_':
                print("Scissors")
                self.GameManager.bob.setMove('Scissors')
                self.window["_rock_"].Update(disabled=True)
                self.window["_paper_"].Update(disabled=True)

        self.window.close()


'''
Call functions of the two players
Sync the network communication with simspark robot animations
Functions can be used in the UI
'''
class GameManager:

    def __init__(self):
        # initialize Agents
        self.server = GameServer()
        self.gui = GUI(self)
        self.server.set_gui(self.gui)


        self.bob = ParticipantAgent(player_id=1)
        self.bob.start()
        self.bob.setGui(self.gui)

        self.alice = ParticipantAgent(player_id=2)
        self.alice.start()
        self.alice.setGui(self.gui)

        #start server
        try:
            thread = threading.Thread(target=self.server.server_loop)
            thread.start()
        except KeyboardInterrupt:
            print('Interrupted server-lobby')
        time.sleep(0.01)

        #TODO: position and rotation in front of each other
        return

    def start_gui(self):
        try:
            thread_gui = threading.Thread(target=self.gui.event_loop)
            thread_gui.start()
            time.sleep(1)
        except KeyboardInterrupt:
            print('Interrupted gui start')
        self.gui.set_agents_joined(0)

    #start a game between bob and alice
    def start_game(self):
        #Call Agent methods for Handshake

        try:
            thread4 = threading.Thread(target=self.bob.run_client)
            thread4.start()
        except KeyboardInterrupt:
            print('Interrupted Client')


        try:
            thread5 = threading.Thread(target=self.alice.run_client)
            thread5.start()
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
    #print(repr(bin(msg)))
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

def string_toSymbol(string):
    if(string == "Rock"):
        return 0
    elif(string == "Paper"):
        return 1
    elif(string == "Scissors"):
        return 2
    else:
        return "NOTFOUND"

class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BACKGROUND = '\033[94;43m'

if __name__ == '__main__':
    # agent.__dict__
    # dir(agent)
    game = GameManager()
    game.start_gui()
    #game.start_game()

