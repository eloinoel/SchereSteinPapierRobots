# Schere-Stein-Papier-Robots

Two robots stand in front of each other and play rounds of turn-based rock-paper-scissors. Each robot should be able to detect what the other robot plays and react with a win or lose animation, after the game has finished. You can either choose to play yourself against an AI or let 2 AI's battle each other. The AI will play the dominant strategy, meaning rock, paper or scissors with a probability of 1/3.

We used the code framework from the lecture and added our own code. The files from the project can be found in '/SSPLProjekt'. For the GUI to work you need to install the package PySimpleGUI 'pip install PySimpleGUI'.

- move_agents.ipynb: This notebook can be used to create keyframe data for the robot gestures. Execute all the cells in the right order while having Simspark running. A demo will be provided in the final presentation.
- /SSPLProjekt/new_keyframes: This folder contains all the newly generated keyframes. OpenPaper.py, Rock.py and Scissors.py are the game's gestures. Win.py and Sad.py are the reactions played after a round to show the result.
- gui.py: Contains the gui code. You don't need to execute this, as it is additionally integrated in robot_communication.py
- robot_communication.py: Contains the Client-Server-Implementation for the robots to communicate and play a game of rock-paper-scissors. While having Simspark open, execute the main function at the bottom to make it work.


Our Group: Christopher Dukart (358925), Bruno Lönne (402214), Eloi Sandt (401675)
