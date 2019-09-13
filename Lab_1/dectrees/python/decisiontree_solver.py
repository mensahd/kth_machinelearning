import monkdata as m
import dtree

#Code Linus
def assignment1_linus():
    entropy1 = dtree.entropy(m.monk1)
    entropy2 = dtree.entropy(m.monk2)
    entropy3 = dtree.entropy(m.monk3)
    print("Entropy of Monk1: " + str(entropy1))
    print("Entropy of Monk2: " + str(entropy2))
    print("Entropy of Monk2: " + str(entropy3))

def run_linus():


run_linus()