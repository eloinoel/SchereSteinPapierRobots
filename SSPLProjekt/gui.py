# gui.py

import PySimpleGUI as sg
import os.path
import time
import threading

class GUI():
    def __init__(self, GameManager=None):
        pass
        #self.GameManager = GameManager

    def set_layout(self):
        image_schere = './ButtonGraphics/schere.png'
        image_stein = './ButtonGraphics/stein.png'
        image_papier = './ButtonGraphics/papier.png'
        #image_start = './ButtonGraphics/start.png'

        first_column = [
            #[sg.Button(button_color=sg.TRANSPARENT_BUTTON,image_filename=image_start,image_size=(70, 70),image_subsample=8,size = (7,7))],
            #[sg.Button(button_text="Create Lobby",)],


            [sg.Text("Autoplay:"),sg.Button('Off',size=(3,1),button_color=('white', 'red'),key='_B_')],
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
                self.window.Element('_B_').Update(('On', 'Off')[down], button_color=(('white', ('green', 'red')[down])))
                self.window["_scissor_"].Update(disabled=down)
                self.window["_rock_"].Update(disabled=down)
                self.window["_paper_"].Update(disabled=down)
                #self.GameManager.bob.setAutoplay(down)
            elif event == '_pGame_':
                print("Start Game")
                #self.GameManager.start_game()
                self.window["_scissor_"].Update(disabled=False)
                self.window["_paper_"].Update(disabled=False)
                self.window["_rock_"].Update(disabled=False)

            elif event == '_rock_':
                print("Rock")
                #self.GameManager.bob.setMove('Rock')
                self.window["_scissor_"].Update(disabled=True)
                self.window["_paper_"].Update(disabled=True)
            elif event == '_paper_':
                print("Paper")
                self.GameManager.bob.setMove('Paper')
                self.window["_scissor_"].Update(disabled=True)
                self.window["_rock_"].Update(disabled=True)
            elif event == '_scissor_':
                print("Scissors")
                #self.GameManager.bob.setMove('Scissors')
                self.window["_rock_"].Update(disabled=True)
                self.window["_paper_"].Update(disabled=True)

        self.window.close()

class GameManager:
    def __init__(self):
        self.gui = None

    def initGui(self):
        self.gui = Gui(self)
        self.gui.event_loop()

def doStart():
    game = GameManager()
    thread = threading.Thread(target=game.initGui)
    thread.start()
    return game



if __name__ == '__main__':
    game = doStart()

    time.sleep(5)
    game.gui.set_pTwo("Player 2 Won")
