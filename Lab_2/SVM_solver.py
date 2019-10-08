import numpy
import random
import matplotlib.pyplot as plt
from scipy.optimize import minimize

classA = numpy.concatenate(
    (numpy.random.randn(20, 2) * 0.2 + [1.5, 0.5],  # 10x2 vector of normal distribution around 1.5, 0.5,
     numpy.random.randn(20, 2) * 0.2 + [-1.5, 0.5]))  # standard deviation of 0.2
classB = numpy.random.randn(40, 2) * 0.2 + [0.0, -0.5]


def generating_test_data():
    inputs = numpy.concatenate((classA, classB))
    targets = numpy.concatenate(  # targets, either +1 or -1
        (numpy.ones(classA.shape[0]),
         -numpy.ones(classB.shape[0])))
    N = inputs.shape[0]  # number of samples
    permute = (list(range(N)))
    random.shuffle(permute)
    return inputs[permute, :], targets[permute]


datapoints, targets = generating_test_data()

N = datapoints.shape[0]
C = 0.5  # margin factor


def linear_kernel_function(x, y):
    return numpy.dot(x, y)


def kernel_function(datapoint_1, datapoint_2):  # defined new in every case
    return linear_kernel_function(datapoint_1, datapoint_2)


def init_matrix():
    matrix = numpy.zeros((N, N))
    for i in range(N):
        for j in range(N):
            matrix[i][j] = (targets[i] * targets[j] * kernel_function(datapoints[i], datapoints[j]))
    return matrix


P = init_matrix()


def objective(vector_a):
    return 0.5 * numpy.dot(vector_a, numpy.dot(vector_a, P)) - numpy.sum(vector_a)


def zerofun(a):
    return numpy.dot(a, targets)


def solve_min():
    boundaries = [(0, C) for b in range(N)]
    ret = minimize(objective, numpy.zeros(N), bounds=boundaries,
                   constraints={'type': 'eq', 'fun': zerofun})  # returns all the support vectors
    if not ret['success']:
        print("Not successful")
    alpha = ret['x']
    alpha_idx = numpy.where(alpha >= 10 ** (-5))
    perfect_list = list(zip(datapoints[alpha_idx], alpha[alpha_idx], numpy.array(targets)[alpha_idx]))
    return perfect_list


svm_alphas = solve_min()
print(svm_alphas)


def calculate_b():
    any_index = 0  # just pick the first one
    any_sv = svm_alphas[any_index]
    list_values = [numpy.dot(numpy.dot(x[1], x[2]), kernel_function(any_sv[0], x[0])) for x in svm_alphas]
    return numpy.sum(list_values) - any_sv[2]


bias = calculate_b()


def indicator_function(x, y ):
    s = [x,y]
    list_values = [numpy.dot(numpy.dot(x[1], x[2]), kernel_function(s, x[0])) for x in svm_alphas]
    return numpy.sum(list_values) - bias


def plot_data():
    plt.plot([p[0] for p in classA],
             [p[1] for p in classA],
             'b.')
    plt.plot([p[0] for p in classB],
             [p[1] for p in classB],
             'r.')

    plt.axis('equal')  # Force the same scale on both axes
    plt.savefig('svmplot.pdf')  # Save a copy in a file
    #plt.show()  # Show the plot on the screen

    xgrid = numpy.linspace(-5, 5)
    ygrid = numpy.linspace(-4, 4)
    grid = numpy.array([[indicator_function(x, y) for x in xgrid] for y in ygrid])

    plt.contour(xgrid, ygrid, grid, (-1.0, 0.0, 1.0), \
                colors=('red', 'black', 'blue'),
                linewidths=(1, 3, 1))

    plt.show()  # Show the plot on the screen


plot_data()
