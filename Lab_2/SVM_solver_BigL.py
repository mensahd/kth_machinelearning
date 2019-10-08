import numpy, random, math
from scipy.optimize import minimize
import matplotlib.pyplot as plt

"parameters for dataclasses A and B"
c_A_1 = [1.5, 0.5]
c_A_2 = [-1.5, 0.5]
c_A_3 = [0, -2]
c_B_1 = [0.0, -0.5]
c_B_2 = [-3.0, -0.5]
c_B_3 = [0, 4]
points_A = 20
points_B = 20
variance_A = 0.35
variance_B = 0.35
kernel = 2  # 0: linear, 1: polynomial, 2: RBF

#generate the classes
classA = numpy.concatenate(
    (numpy.random.randn(points_A, 2) * variance_A + c_A_1,  # 10x2 vector of normal distribution around 1.5, 0.5,
     numpy.random.randn(points_A, 2) * variance_A + c_A_2,
     numpy.random.randn(points_A, 2) * variance_A + c_A_3))  # standard deviation of 0.2
classB = numpy.concatenate(
    (numpy.random.randn(points_B, 2) * variance_B + c_B_1,  # 10x2 vector of normal distribution around 1.5, 0.5,
     numpy.random.randn(points_B, 2) * variance_B + c_B_2,
     numpy.random.randn(points_B, 2) * variance_B + c_B_3))


def generating_test_data():
    inputs = numpy.concatenate((classA, classB))
    targets = numpy.concatenate(                # targets, either +1 or -1 corresponding to class
        (numpy.ones(classA.shape[0]),
         -numpy.ones(classB.shape[0])))
    N = inputs.shape[0]                         # number of samples
    permute = (list(range(N)))
    random.shuffle(permute)
    return inputs[permute, :], targets[permute]


inputs, targets = generating_test_data()
N = inputs.shape[0]


def kernel_function(x, y):
    "Different kernel funcitons"
    p = 10      # parameter polynomial kernel
    sigma = 2   # parameter RBF kernel
    if kernel == 1:
        return (numpy.dot(x, y) + 1) ** p   #polynomial
    elif kernel == 2:
        return numpy.exp(-(numpy.linalg.norm(x - y) ** 2) / (2 * (sigma ** 2))) # RBF
    else:
        return numpy.dot(x, y)              # linear


P = numpy.zeros((N, N))  # zero matrix P
for i in range(N):  # implement matrix P
    for j in range(N):
        P[i][j] = targets[i] * targets[j] * kernel_function(inputs[i], inputs[j])


def objective(a):
    # equation to minimalize in vector form
    return 0.5 * numpy.dot(a, numpy.dot(a, P)) - numpy.sum(a)


def zerofun(a):
    # checks the constraint
    return numpy.dot(a, targets)


def minimalize_alpha():

    bound_B = [(0, 10) for b in range(N)]
    # objective: function with a as argument
    # start: initial guess of a -> Zero vector
    # bounds: list of pairs with the lower and upper bounds
    # constraint: constraining alpha, constraint={'type':'eq', 'fun':zerofun}
    ret = minimize(objective, numpy.zeros(N), bounds=bound_B, constraints={'type': 'eq', 'fun': zerofun})
    if ret['success']:
        solution_found = True
        print("solution found")
    else:
        solution_found = False
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nNO SOLUTION FOUND\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    alpha = ret['x']
    indices = numpy.where(alpha >= 10 ** (-5))
    indices = indices[0][:]  # da sonst indices als Matrix gesehen wird
    support_vector = [[alpha[i], targets[i], inputs[i]] for i in indices]
    return support_vector, solution_found


support_vectors, solution_found = minimalize_alpha()


def calculate_bias():
    any_sv = support_vectors[0][:]  # random support vector
    array = [[numpy.dot(numpy.dot(sv[0], sv[1]), kernel_function(sv[2], any_sv[2]))] for sv in support_vectors]
    return numpy.sum(array) - any_sv[1]


b = calculate_bias()


def indicator_fct(x, y):
    "Indicator function which determines class"
    s = [x, y]
    array = [[numpy.dot(numpy.dot(sv[0], sv[1]), kernel_function(sv[2], s))] for sv in support_vectors]
    return numpy.sum(array) - b


def plot_data():
    plt.plot([p[0] for p in classA],
             [p[1] for p in classA],
             'b.')
    plt.plot([p[0] for p in classB],
             [p[1] for p in classB],
             'r.')
    if solution_found:
        plt.plot([sv[2][0] for sv in support_vectors],
             [sv[2][1] for sv in support_vectors],
             'yo')

    plt.axis('equal')
    plt.savefig('svmplot.pdf')
    plt.show()

    xgrid = numpy.linspace(-5, 5)
    ygrid = numpy.linspace(-4, 4)
    grid = numpy.array([[indicator_fct(x, y) for x in xgrid] for y in ygrid])
    plt.contour(xgrid, ygrid, grid,
                (-1.0, 0.0, 1.0),
                colors=('red', 'black', 'blue'),
                linewidths=(1, 3, 1))


plot_data()
