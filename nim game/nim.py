import copy
import sys


class Nim:
    def __init__(self, redCount, blueCount):
        self.redCount = redCount
        self.blueCount = blueCount
        self.alpha = -sys.maxsize-1
        self.beta = sys.maxsize
        self.points = 0
        self.choice = ""


def miniMax(nimState: Nim, depth: int, isHumanTurn: bool) -> Nim:
    # print(nimState.points)
    # Mini
    if isHumanTurn:
        # if the depth is reached return the best alternative for minimum
        if depth > depth_limit:
            nimState.points = nimState.beta
            return nimState

        # at the leaf node. Take the positive value (the computer tries to maximize in previous turn)
        if nimState.redCount == 0 or nimState.blueCount == 0:
            nimState.points = nimState.redCount*2 + nimState.blueCount*3
            return nimState

        # if intermediate state, the Human tries to minimize. The current node is mini

        # Take the blue ball and proceed further
        blueState = copy.deepcopy(nimState)
        blueState.blueCount -= 1
        newBlueState = miniMax(blueState, depth+1, False)

        # Set the points to +inf
        nimState.points = sys.maxsize

        # check if we get the minimum (it is minimum because nimState.points is +inf)
        nimState.choice = "blue"
        nimState.points = newBlueState.points
        nimState.beta = min(nimState.beta, nimState.points)

        # prune
        # If we cannot find the better alternative for maximum
        if nimState.alpha >= newBlueState.points:
            return nimState

        # Take the red ball and proceed further
        redState = copy.deepcopy(nimState)
        redState.redCount -= 1
        newRedState = miniMax(redState, depth+1, False)

        # check if we get the minimum
        if (newRedState.points < nimState.points):
            nimState.choice = "red"
            nimState.points = newRedState.points
            nimState.beta = min(nimState.beta, nimState.points)
    else:
        # if the depth is reached return the best alternative for maximum
        if depth > depth_limit:
            nimState.points = nimState.alpha
            return nimState

        # at the leaf node. Take negative values (the user tries to minimize in the preious turn)
        if nimState.blueCount == 0 or nimState.redCount == 0:
            nimState.points = -(nimState.blueCount*3+nimState.redCount*2)
            return nimState

        # If the intermediate state, the Computer tries to maximize. The Current node is Maxi

        # Take the blue and proceed
        blueState = copy.deepcopy(nimState)
        blueState.blueCount -= 1
        newBlueState = miniMax(blueState, depth+1, True)

        # Set the points to -inf
        nimState.points = -sys.maxsize-1

        # check if we get the maximum (it is maximum because nimState.points is -inf)
        nimState.choice = "blue"
        nimState.points = newBlueState.points
        nimState.alpha = max(nimState.alpha, nimState.points)

        # prune
        # if we cannot get the better alternative for minimum
        if nimState.beta <= newBlueState.points:
            return nimState

        # Take the red ball and proceed
        redState = copy.deepcopy(nimState)
        redState.redCount -= 1
        newRedState = miniMax(redState, depth+1, True)

        # check if we can get the maximum
        if (newRedState.points > nimState.points):
            nimState.choice = "red"
            nimState.points = newRedState.points
            nimState.alpha = max(nimState.alpha, nimState.points)
    return nimState


# Take Input from CLI
def humanTurn():
    human = input(
        "Enter the choice Red or blue (Enter only red or blue): ").lower()
    while human not in ["red", "blue"]:
        human = input(
            "Invalid Choice! Enter the correct choice (Either red or blue): ")
    return human


# Custom Eval method
name = locals()['miniMax']


def my_eval(arg1, arg2):
    return name(arg1, arg2, False)


# Start Game
blue = 20
red = 15
humanFirst = False
if len(sys.argv) < 3:
    print("Not enough arguments: ")
    print("Run the file this way: python nim.py <num-red> <num-blue> <first-player> <depth>")
    print("first-player and depth are optional arguments not required")
if len(sys.argv) >= 3:
    red = int(sys.argv[1])
    blue = int(sys.argv[2])
depth_limit = red+blue
if len(sys.argv) == 4:
    depth_limit = int(sys.argv[3])
if len(sys.argv) == 5:
    if "human" in sys.argv[3].lower():
        humanFirst = True
    depth_limit = int(sys.argv[4])


# 'i' is used to toggle between the turns (Humand and Computer)
# humanFirst is used to check if human starts the game or a computer
# For each computer turn the Computer performs the min max with alpha-beta pruning.
# depth_limit is used to limit the depth of the min max algorithm.
i = 0
if not humanFirst:
    i += 1
while (blue != 0 and red != 0):
    print("Remaining: ")
    print("   Blue: ", blue)
    print("   Red: ", red)
    choice = str
    if i % 2 == 0:
        choice = humanTurn()
    else:
        start = Nim(red, blue)
        choice = my_eval(start, 0).choice
        print("Computer Chooses: ", choice)
    if choice == "red":
        red -= 1
    else:
        blue -= 1
    i += 1

if i % 2 == 0:
    print("Computer Won: ", (red*2+blue*3), "points")
else:
    print("Human Won: ", (red*2+blue*3), "points")
