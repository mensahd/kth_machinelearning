import monkdata as m
import dtree


def getMonkset(number):
    monknumber = 'monk' + str(number)
    return getattr(m, monknumber, lambda: "Invalid MONK dataset")


# Code Daniel
def assignment1_daniel():
    print("Assignment 1:")
    for i in range(1, 4):
        print("MONK-" + str(i) + " entropy is: " + str(dtree.entropy(getMonkset(i))))


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


# Code Linus
def assignment1_linus():
    entropy1 = dtree.entropy(m.monk1)
    entropy2 = dtree.entropy(m.monk2)
    entropy3 = dtree.entropy(m.monk3)
    print("Entropy of Monk1: " + str(entropy1))
    print("Entropy of Monk2: " + str(entropy2))
    print("Entropy of Monk2: " + str(entropy3))


def assignment3_linus():
    for index in range(1, 4):  # for-loop for the monk-datasets
        print("MONK-" + str(index))
        for attribute in m.attributes:
            gain = dtree.averageGain(getMonkset(index), attribute)
            print(str(attribute) + ": " + str(gain))

def assignment5_linus():
    dataset = m.monk1
    print(find_best_attribute(dataset, m.attributes))

def find_best_attribute(dataset, attributes):
    "Find attribute with the highest information gain"
    gains = []
    for attribute in attributes:
        gains.append((dtree.averageGain(dataset, attribute), attribute))#creates a list of tupples with information gain + attribute
    return max(gains)[1]#Glüch gehabt dass er das 1. Element im Tupel (Average Gain) miteinander vergleicht

def run_linus():
    # assignment1_linus()
    #assignment3_linus()
    assignment5_linus()

run_linus()
# run_daniel()
