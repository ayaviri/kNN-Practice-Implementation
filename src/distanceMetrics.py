from math import sqrt, pow

# computes the euclidean distance between the two vectors
def euclideanDistance(firstVector, secondVector):
    # ensures that both vectors have the same number of dimensions
    if len(firstVector) != len(secondVector):
        raise Exception("Vectors must have the same dimension in order to compute distance")
        
    distanceSquared = 0
    for i in range(len(firstVector)):
        currentComponent = pow(firstVector[i] - secondVector[i], 2)
        distanceSquared += currentComponent
    distance = sqrt(distanceSquared)
    return distance

# computes the manhattan distance between two vectors
def manhattanDistance(firstVector, secondVector):
    # ensures that both vectors have the same number of dimensions
    if len(firstVector) != len(secondVector):
        raise Exception("Vectors must have the same dimension in order to compute distance")

    distance = 0
    for i in range(len(firstVector)):
        currentComponent = abs(firstVector[i] - secondVector[i])
        distance += currentComponent
    return distance

# computes the minkowski distance between two vectors with the given order of the norm
def minkowskiDistance(firstVector, secondVector, normOrder):
    # ensures that both vectors have the same number of dimensions
    if len(firstVector) != len(secondVector):
        raise Exception("Vectors must have the same dimension in order to compute distance")
    
    distancePow = 0
    for i in range(len(firstVector)):
        currentComponent = pow(abs(firstVector[i] - secondVector[i]), normOrder)
        distancePow += currentComponent
    distance = pow(distancePow, (1 / normOrder))
    return distance

# computes 1 - (cos(theta)) where theta is the angle between the two vectors. the smaller the value, the closer the angle between 
# the two vectors
def cosineSimilarity(firstVector, secondVector):
    # ensures that both vectors have the same number of dimensions
    if len(firstVector) != len(secondVector):
        raise Exception("Vectors must have the same dimension in order to compute distance")
    cosine = (dotProduct(firstVector, secondVector)) / (vectorMagnitude(firstVector) * vectorMagnitude(secondVector))
    return cosine

# computes the dot product between two vectors
def dotProduct(firstVector, secondVector):
    # ensures that the two vectors have the same number of dimensions
    if len(firstVector) != len(secondVector):
        raise Exception("Vectors must have the same dimension in order to compute distance")

    dotProduct = 0
    for i in range(len(firstVector)):
        currentComponent = firstVector[i] * secondVector[i]
        dotProduct += currentComponent
    return dotProduct

# computes the magnitude of a given vector
def vectorMagnitude(vector):
    magnitudeSquared = 0
    for i in range(len(vector)):
        currentComponent = vector[i]
        magnitudeSquared += pow(currentComponent, 2)
    magnitude = sqrt(magnitudeSquared)
    return magnitude