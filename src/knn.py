from random import sample
from statistics import mode
from priorityQueue import PriorityQueue

def knn(trainingSet, k, querySet, distanceMetric):
    # ensuring that the training set has more points than the value of k
    if k >= len(trainingSet):
        raise Exception("K must be strictly less than the length of the training set")
        
    # ensuring that k is strictly positive
    if k <= 0: 
        raise Exception("K must be strictly greater than zero")
        
    outputQuerySet = []
    # calculating the label for each element of the query set
    for i in range(len(querySet)):
        currentQuery = querySet[i] 
        # choosing the k nearest neighbors from the training set and 
        # constructing the priority queue, where each neighbor will be identified
        # by their index in the training set
        indices = sample(range(len(trainingSet)), k)
        priorityQueue = PriorityQueue(k)
        for j in range(k):
            currentNeighborIndex = indices[j] # the neighbor's id
            currentNeighbor = trainingSet[currentNeighborIndex] # (vector, label)
            currentNeighborDistance = distanceMetric(currentQuery, currentNeighbor[0])
            priorityQueue.insert(currentNeighborIndex, currentNeighborDistance)
            
        # iterating through all of the elements in the training set to calculate k 
        # nearest neighbors
        for j in range(len(trainingSet)):
            # if the queue already contains the current data point, skip it
            if priorityQueue.contains(j):
                continue
            
            currentDataPoint = trainingSet[j] # (vector, label)
            currentDistance = distanceMetric(currentQuery, currentDataPoint[0])
            if currentDistance < priorityQueue.peekRoot():
                priorityQueue.extractRoot()
                priorityQueue.insert(j, currentDistance)
                
        # obtaining the k nearest neighbors 
        closestNeighborIndices = priorityQueue.getIndices()
        # maps from each index to its corresponding label in the training set
        closestLabels = [trainingSet[index][1] for index in closestNeighborIndices]
        queryLabel = mode(closestLabels)
        outputQuerySet += [(currentQuery, queryLabel)]
    return outputQuerySet