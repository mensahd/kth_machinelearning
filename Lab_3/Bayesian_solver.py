import numpy as np
# Dimensions of Matrices

def sample_matrix(): #notused
    rows = 7
    cols = 4
    depth = 5
    # Creating matrices
    A = np.zeros((rows,cols)) # 2D Matrix of zeros
    print(A.shape)

    A = np.zeros((depth,rows,cols)) # 3D Matrix of zeros
    A = np.ones((rows,cols)) # 2D Matrix of ones
    A = np.array([(1,2,3),(4,5,6),(7,8,9)]) # 2D 3x3 matrix with values
    # Turn it into a square diagonal matrix with zeros of-diagonal
    d = np.diag(A) # Get diagonal as a row vector
    d = np.diag(d) # Turn a row vector into a diagonal matrix

def logical_indexing():
    X,y = getData()
    classes = np.unique(y) # Get the unique examples
    # Iterate over both index and value
    for jdx,class in enumerate(classes):
    idx = y==class # Returns a true or false with the length of y
    # Or more compactly extract the indices for which y==class is true,
    # analogous to MATLAB’s find
    idx = np.where(y==class)[0]
    xlc = X[idx,:] # Get the x for the class labels. Vectors are rows.