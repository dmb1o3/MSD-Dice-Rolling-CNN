# Description of MSD Dice Rolling Project
This was a project built with the Connected Dice Rolling team as part of the MSD program at RIT.
The goal of the project is to build a dice tray that users can roll die into. Once rolled
a sensor will detect the dice, trigger the camera, which sends the image to the users computer 
where a YOLO ensemble model will identify the dice type and what numbers were rolled on each die


## Overview
### main.py
This is the main file for program and runs the ensemble model to detect die type and roll

#### YOLO_training.py
This file is used to train the YOLO dice type and dice roll models 

#### arduino_communication.py
NEED TO DO

### install_dependencies.py
NEED TO DO

## Installation (NEEDS TO BE UPDATED)
### Python
This program requires python 3.9 or greater. I would recommend using conda to create a virtual enviroment

[Link to a guide to install conda](https://developers.google.com/earth-engine/guides/python_install-conda)
1. conda create --name envName python=3.9
2. conda activate envName


### Requirements and Running Program(NEED TO UPDATE)
1. Download repository
2. Install requirements using "pip install -r requirements.txt" 
3. Run data_collector.py
4. Enter in desired seasons
5. After running can do whatever you would like with data but if you want to test the models go to models.py and change
   years_to_examine to contain years you have downloaded data for
6. Run models.py
