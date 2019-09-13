import drawtree_qt5 as qt5
import dtree
import monkdata as m
import id3


def getMonkset(number):
    monknumber = 'monk' + str(number)
    return getattr(m, monknumber, lambda: "Invalid MONK dataset")

def tabHelper(text, min_field=25):
    tabs_to_append = min_field - len(text)
    return_string = (text if (tabs_to_append <= 0) else text + " " * tabs_to_append)
    return return_string

# Code Daniel
def assignment1_daniel():
    print("Assignment 1:")
    for i in range(1, 4):
        print("MONK-" + str(i) + " entropy is: " + str(dtree.entropy(getMonkset(i))))


def assignment3_daniel():
    print("Assignment 3:")

    print(tabHelper("MONK-X |", min_field=10) + tabHelper("A1") + tabHelper("A2") + tabHelper("A3") + tabHelper(
        "A4") + tabHelper("A5") + tabHelper("A6"))
    print(6 * 25 * "-")
    for i in range(1, 4):
        mset = getMonkset(i)
        print(tabHelper("MONK-" + str(i) + str(" |"), min_field=10), end=" ")
        for att in m.attributes:
            print(tabHelper(str(dtree.averageGain(mset, att) * 1000)), end="")
        print()


def buildtree(currentSet, level=5, subtree="X"):
    if (level > 0):
        '''
        max_att = None;
        max_gain = -1;
        for att in m.attributes:
            gain = dtree.averageGain(currentSet, att)
            if gain > max_gain:
                max_att, max_gain = att, gain
        '''
        max_att = dtree.bestAttribute(currentSet, m.attributes)
        nextSets = [dtree.select(currentSet, max_att, x) for x in max_att.values]
        print("Split by " + str(max_att) + " in subtree " + subtree)
        for i, set in enumerate(nextSets):
            if len(set) > 0:
                buildtree(set, level - 1, subtree + "-" + str(i+1))
    else:
        print("Subtree " + subtree + ": " + str(dtree.mostCommon(currentSet)))


def assignment5_daniel():
    print("Assignment 5:")
    mset = getMonkset(1)
    buildtree(mset, 2)

    print("Comparison")
    tree = id3.buildtree(mset, m.attributes)
    qt5.drawtree(tree)



def run_daniel():
    assignment1_daniel()
    assignment3_daniel()
    assignment5_daniel()


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
run_daniel()

