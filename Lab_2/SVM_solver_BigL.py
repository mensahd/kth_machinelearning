import numpy, random, math
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# numpy.zeros(N)

# ret = minimize(objective, start, bounds= B, constraints=XC)
# alpha = ret[’x’]


# stuff linus


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


inputs, targets = generating_test_data()
N = inputs.shape[0]

def kernel_linear(x, y):
    return numpy.dot(x, y)


P = numpy.zeros((N, N))  # zero matrix P
for i in range(N):  # implement matrix P
    for j in range(N):
        P[i][j] = targets[i] * targets[j] * kernel_linear(inputs[i], inputs[j])


def objective(a):
    # equation to minimalize in vector form
    return 0.5 * numpy.dot(a, numpy.dot(a, P)) - numpy.sum(a)


def zerofun(a):
    # checks the constraint
    return numpy.dot(a, targets)


def minimalize_alpha():
    C = None
    bound_B = [(0, C) for b in range(N)]
    # objective: function with a as argument
    # start: initial guess of a -> Zero vector
    # bounds: list of pairs with the lower and upper bounds
    # constraint: constraining alpha, constraint={'type':'eq', 'fun':zerofun}
    ret = minimize(objective, numpy.zeros(N), bounds=bound_B, constraints={'type': 'eq', 'fun': zerofun})
    alpha = ret['x']
    indices = numpy.where(alpha >= 10 ** (-5))
    indices = indices[0][:]                                             #da sonst indices als Matrix gesehen wird
    support_vector = [[alpha[i], targets[i], inputs[i]] for i in indices]
    return support_vector


support_vectors = minimalize_alpha()


def calculate_bias():
    any_sv = support_vectors[0][:]  # random support vector
    array = [[numpy.dot(numpy.dot(sv[0], sv[1]), kernel_linear(sv[2], any_sv[2]))] for sv in support_vectors]
    return numpy.sum(array) - any_sv[1]


b = calculate_bias()


def indicator_fct(x, y):
    s = [x, y]
    array = [[numpy.dot(numpy.dot(sv[0], sv[1]), kernel_linear(sv[2], s))] for sv in support_vectors]
    return numpy.sum(array) - b


def plot_data():
    plt.plot([p[0] for p in classA],
             [p[1] for p in classA],
             'b.')
    plt.plot([p[0] for p in classB],
             [p[1] for p in classB],
             'r.')
#    plt.plot([sv[2][0] for sv in support_vectors)],
 #            [sv[2][1] for sv in support_vectors)],
  #          'g+')
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
