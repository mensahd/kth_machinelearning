import monkdata as m
import dtree


def getMonkset(number):
    monknumber = 'monk' + str(number)
    return getattr(m, monknumber, lambda: "Invalid MONK dataset")

#Code Daniel
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

#Code Linus
def assignment1_linus():
    entropy1 = dtree.entropy(m.monk1)
    entropy2 = dtree.entropy(m.monk2)
    entropy3 = dtree.entropy(m.monk3)
    print("Entropy of Monk1: " + str(entropy1))
    print("Entropy of Monk2: " + str(entropy2))
    print("Entropy of Monk2: " + str(entropy3))

def run_linus():
    assignment1_linus()

run_linus()
run_daniel()

