import os

# This script will create folder set up for storing data images of dice
# It will make folders following this schema
# d{diceNumber}/
#               {allPossibleRolls}/
# ex
# d4/
#    1/
#    2/
#    3/
#    4/
# To add a dice to the script add it to the array below
# Wait to implement d10s. Ours have 0 to represent 10 but seems like we are going to implement rule where d10s should
# have a 10 to represent 10 not 0
dice_to_add = [
    {
        "max_roll": 6,
        "step": 1,
    },
    {
        "max_roll": 8,
        "step": 1,
    },
    {
        "max_roll": 12,
        "step": 1,
    },
    {
        "max_roll": 20,
        "step": 1,
    },
]


def folder_check(directory):
    """
    Given a directory will check to see if it exists. If it does not exist, make the directory

    :param directory: String with a path for directory we want to check and possibly make
    :return: Does not return anything
    """
    if not os.path.isdir(directory):
        # Make directory if needed
        os.mkdir(directory)


def set_up_folders():
    # Make folder for all training images
    folder_check(os.getcwd() + "/Training-Images")
    for dice in dice_to_add:
        max_roll = dice["max_roll"]
        # Make directory for dice if not already there
        folder_check(os.getcwd() + "/Training-Images/d" + str(max_roll))
        # Make folders for possible rolls
        for roll in range(1, max_roll + 1, dice["step"]):
            folder_check(os.getcwd() + "/Training-Images/d" + str(max_roll) + "/" + str(roll))


if __name__ == '__main__':
    set_up_folders()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
