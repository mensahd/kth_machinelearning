from Lab_1.dectrees.python import monkdata as m
from Lab_1.dectrees.python import dtree



def getMonkset(number):
    monknumber = 'monk' + str(number)
    return getattr(m, monknumber, lambda: "Invalid MONK dataset")

def assignment1_daniel():
    print("Assignment 1:")
    for i in range(1, 4):
        print("MONK-" + str(i) + " entropy is:" + str(dtree.entropy(getMonkset(i))))

def assignment2_daniel():
    print("")

def assignment3_daniel():
    print("")

def assignment4_daniel():
    print("")

def assignment5_daniel():
    print("")

def run_daniel():
  assignment1_daniel()

run_daniel()
