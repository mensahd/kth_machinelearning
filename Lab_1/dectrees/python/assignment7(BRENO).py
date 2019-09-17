import monkdata as m
import dtree as d
import drawtree_qt5 as drawtree_qt5
import random
import matplotlib.pyplot as plt
import numpy as np


def partition(data, fraction):
    ldata = list(data)
    random.shuffle(ldata)
    break_point = int(len(ldata) * fraction)
    return ldata[:break_point], ldata[break_point:]


def pruning(tree, val_data):
    current_best = tree
    best_tree = None
    current_score = d.check(tree, val_data)
    best_score = 0
    while current_score >= best_score:
        best_score = current_score
        best_tree = current_best
        pruned_trees = d.allPruned(current_best)
        if len(pruned_trees) > 0:
            scores = [d.check(t, val_data) for t in pruned_trees]
            current_score = max(scores)
            current_best = pruned_trees[scores.index(current_score)]
        else:
            break
    return best_tree


def find_best_tree(data, attributes, fraction):
    train, val = partition(data, fraction)
    tree = d.buildTree(train, attributes)
    tree = pruning(tree, val)
    return tree


def plot_results(train, test):
    attributes = m.attributes
    fractions = [0.5]
    final_scores = np.zeros(len(fractions))
    for i in range(1):
        best_trees = [find_best_tree(train, attributes, 0.5)]
        scores = [d.check(t, test) for t in best_trees]
        final_scores = np.add(final_scores, scores)
        print(best_trees)
        print(final_scores)
    final_scores = final_scores / 1
    plt.clf()
    plt.plot(fractions, final_scores)
    plt.plot(fractions, final_scores, "rx")
    for a, b in zip(fractions, final_scores):
        plt.text(a, b, str(round(b, 3)))
    plt.xlabel("Proportion of the training set")
    plt.ylabel("val_accuracy")
    plt.show()

    # index_max = scores.index(max(scores))
    # drawtree_qt5.drawTree(best_trees[index_max])


plot_results(m.monk3, m.monk3test)
