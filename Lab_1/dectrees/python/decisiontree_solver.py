import drawtree_qt5 as qt5
import dtree
import monkdata as m
import random


# import id3


def getMonkset(number, test=""):
    if test == "":
        monknumber = 'monk' + str(number)
    else:
        monknumber = 'monk' + str(number) + 'test'
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
        if (dtree.allPositive(currentSet) == True or dtree.allNegative(currentSet) == True):
            print("Subtree " + subtree + ": " + str(dtree.mostCommon(currentSet)))
        else:
            max_att = dtree.bestAttribute(currentSet, m.attributes)
            nextSets = [dtree.select(currentSet, max_att, x) for x in max_att.values]
            print("Split by " + str(max_att) + " in subtree " + subtree)
            for i, set in enumerate(nextSets):
                if len(set) > 0:
                    buildtree(set, level - 1, subtree + "-" + str(i + 1))
                else:
                    print("Subtree " + subtree + "-" + str(i + 1) + ": " + str(dtree.mostCommon(set)))
    else:
        print("Subtree " + subtree + ": " + str(dtree.mostCommon(currentSet)))


def assignment5_daniel():
    print("Assignment 5:")

    depth = 9
    for index in range(1, 2):
        mset = getMonkset(index)
        # buildtree(mset, depth)
        print("Comparison")
        tree = dtree.buildTree(mset, m.attributes)
        print("MONK-" + str(index) + ":")
        # print(tree)
        qt5.drawTree(tree)
        print("Correctness_Train: " + str(dtree.check(tree, mset)))
        print("Correctness_Test: " + str(dtree.check(tree, getMonkset(index, "test"))))
        # tree = id3.buildtree(mset,m.attributes)


def run_daniel():
    # assignment1_daniel()
    # assignment3_daniel()
    assignment5_daniel()


# Code BigLinguist
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
    depth = 9
    print("Tiefe: " + str(depth))
    for index in range(3, 4):#loop through all monk sets
        tree = dtree.buildTree(getMonkset(index), m.attributes, depth)
        print("MONK-" + str(index) + ":")
        print(tree)
        print("Error_Train: " + str(dtree.check(tree, getMonkset(index))))
        print("Error_Test: " + str(dtree.check(tree, getMonkset(index, "test"))))
        qt5.drawTree(tree)



def subtree(dataset):
    "Return the subtrees of a datatree for the best attribute"
    best_attribute = dtree.bestAttribute(dataset, m.attributes)
    subtree_dataset = [dtree.select(dataset, best_attribute, x) for x in best_attribute.values]
    return subtree_dataset


def find_best_attribute(dataset, attributes):
    "Find attribute with the highest information gain"
    gains = []
    for attribute in attributes:
        gains.append((dtree.averageGain(dataset, attribute),
                      attribute))  # creates a list of tupples with information gain + attribute
    return max(gains)[1]  # Glüch gehabt dass er das 1. Element im Tupel (Average Gain) miteinander vergleicht


def assignment6_linus():
    runs = 1000  # amount of runs
    monk = 3    #monkset
    monk_training = getMonkset(monk)
    monk_test = getMonkset(monk, "Test")
    fractions_all = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]#fractions for splitting training data

    for fraction in fractions_all:#loop through the different fraction
        scores_fraction = []
        for index in range(runs):#loop through several runs to take the average in the end
            monk_train, monk_val = partition(monk_training, fraction)
            tree = dtree.buildTree(monk_train, m.attributes)
            best_tree = pruning(tree, monk_val)#find the best tree by pruning
            scores_fraction.append(dtree.check(best_tree, monk_test))
        print("Fraction: " + str(fraction))
        for x in scores_fraction:#Ausgabe der scores für eine bestimmte Fraction als Liste -> Auswertung in Excel datei, Werte aus Console kopieren in .txt datei und in Excel einlesen
            print(x)


def pruning(tree, validation_data):
    "Find the best tree by pruning"
    best_tree = tree
    best_score = dtree.check(best_tree, validation_data)
    finished = False
    while not finished:
        "Loop as long pruning again shortens the tree and delivers a better result"
        pruned_list = dtree.allPruned(best_tree)
        found_next_best = False
        for pruned in pruned_list:#loop all prune possibilites
            current_score = dtree.check(pruned, validation_data)
            if current_score > best_score:#check if a pruned tree is better than the old one
                best_score = current_score
                best_tree = pruned
                found_next_best = True
        if not found_next_best:#falls in einer iteration kein neuer, besserer Tree gefunden wird, dann wurde der beste Baum gefunden
            finished = True
    return best_tree


def partition(data, fraction):
    ldata = list(data)
    random.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]


def run_linus():
    # assignment1_linus()
    # assignment3_linus()
    # assignment5_linus()
    assignment6_linus()


run_linus()
# run_daniel()
