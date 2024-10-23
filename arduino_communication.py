import serial
import ensemble
# @TODO Make sure lines up with whats on arduino, also figure out way to detect arduino incase port is taken
arduino = serial.Serial(port='COM5',  baudrate=115200)


def read():
    data = arduino.readline()
    return  data

# Loop to check for
while True:
    # If value is read from arduino then it should have saved file to demo folder
    print("Reading Arduino")
    value = read()
    print(value)

    # @TODO if for some reason arduino cannot save image to needed file path we might be able to move it with a python
    # script given a consistent image name and folder path

    # With image in folder we can run ensemble model
    ensemble.run()
