# Description of MSD Dice Rolling Project
This was a project built with the Connected Dice Rolling team as part of the MSD program at RIT.
The goal of the project is to build a dice tray that users can roll die into. Once rolled
a sensor will detect the dice, trigger the camera, which sends the image to the users computer 
where a YOLO ensemble model will identify the dice type and what numbers were rolled on each die


## Usage
This is intended to be used in conjunction with the Connected Dice Rolling dice tray but 
### With dice tray
1. Plug Connected Dice Rolling dice tray into computer
2. Run Dice Rolling executable 
   1. If first time running will download python dependencies
3. After terminal pops up you are free to roll dice into tray, and it will output results to terminal

### Without dice tray
1. Obtain image of dice
2. Put image into ./demo
3. run main.py then output will be printed to terminal


## Files
### ensemble.py
This is the main file for program and runs the ensemble model to detect die type and roll

#### YOLO_training.py
This file is used to train the YOLO dice type and dice roll models 

#### arduino_communication.py
This file is used to communicate with arduino if you have the connected dice tray

### install_dependencies.py
This file is used to install all python dependencies needed in the project

## Installation (NEEDS TO BE UPDATED)
### Python
This program requires python 3.9 or greater. I would recommend using conda to create a virtual enviroment

[Link to a guide to install conda](https://developers.google.com/earth-engine/guides/python_install-conda)
1. conda create --name envName python=3.9
2. conda activate envName