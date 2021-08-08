# gui.py

import PySimpleGUI as sg
import os.path

image_schere = './ButtonGraphics/schere.png'
image_stein = './ButtonGraphics/stein.png'
image_papier = './ButtonGraphics/papier.png'
image_start = './ButtonGraphics/start.png'

TextElem = sg.Text('', size=(15, 3), font=("Helvetica", 14))


layout = [
    [
        sg.Button(
            # Todo Create Lobby
            button_color=sg.TRANSPARENT_BUTTON,
            image_filename=image_start,
            image_size=(50, 50),
            image_subsample=8,
            size = (7,7)
        ),
        # Todo reset Game button
    ],
    [
        sg.Text(
            "Autoplay:"
        ),
        sg.Button(
            'On',
            size=(3,1),
            button_color=('white', 'green'),
            key='_B_'
        )
    ],
    [
        sg.Text(
            text="Select Move"
        )
    ],
    [
        sg.Button(
            button_color=sg.TRANSPARENT_BUTTON,
            image_filename=image_schere,
            image_size=(50,50),
            image_subsample=12
        ),
        sg.Button(
            button_color=sg.TRANSPARENT_BUTTON,
            image_filename=image_stein,
            image_size=(50,50),
            image_subsample=12
        ),
        sg.Button(
            button_color=sg.TRANSPARENT_BUTTON,
            image_filename=image_papier,
            image_size=(50,50),
            image_subsample=12
        )
    ]
]










# create the window
window = sg.Window("Play-GUI", layout, margins=(100,50))

down = True

# create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or press the OK button
    if event in (None, 'Exit'):
        break
    elif event == '_B_':
        down = not down
        window.Element('_B_').Update(('Off', 'On')[down], button_color=(('white', ('red', 'green')[down])))

window.close()