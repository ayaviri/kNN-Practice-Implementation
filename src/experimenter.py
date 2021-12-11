from distanceMetrics import euclideanDistance
from knn import knn

# runs a trial of knn on the trainingData object with the given k value, and the given query set size
# this query set will be randomly generated at the start of the trial
# the user can also choose which label to treat as the True value in Ground Truth
# optionally, the user can pass in a distance metric. euclidean distance is used by default
def runTrial(trainingData, k, j, label, distanceMetric = euclideanDistance):
    # ensuring that j is strictly greater than 0
    if j <= 0:
        raise Exception("The size of the query set must be strictly greater than zero")
        
    # ensuring that j is strictly less than the total number of samples available in the training data
    if j >= (len(trainingData.getCurrentTrainingSet()) + len(trainingData.getCurrentQuerySet())):
        raise Exception("The size of the query set must be strictly less than the total number of samples available in the training data")
       
    # randomly generating a new query set of size j and adjusting the training set accordingly 
    querySet = trainingData.generateNewQuery(j)
    trainingSet = trainingData.getCurrentTrainingSet()

    # ensuring that k is strictly greater than 0
    if k <= 0:
        raise Exception("K must be strictly greater than zero")
        
    # ensuring that k is strictly less than the size of the new training set
    if k >= len(trainingSet):
        raise Exception("K must be strictly less than the size of the training set")
        
    # setting the label to the one specified
    if label not in trainingData.getLabels():
        raise Exception("Label not contained in the training data's set of labels")
    elif label != trainingData.getCurrentLabel():
        trainingData.setCurrentLabel(label)
        
    # running a trial of knn and mapping to each vector in the query set, forgoing the label
    outputQuerySet = knn(trainingSet, k, [query[0] for query in trainingData.getCurrentQuerySet()], distanceMetric)

    truePositives = 0
    falsePositives = 0
    trueNegatives = 0
    falseNegatives = 0
    label = trainingData.getCurrentLabel()
    for i in range(len(outputQuerySet)):
        prediction = outputQuerySet[i][1]
        groundTruth = querySet[i][1]
        
        if prediction == label:
            if groundTruth == prediction:
                truePositives += 1
            else:
                falsePositives += 1
        else:
            if groundTruth == prediction:
                trueNegatives += 1
            else:
                falseNegatives += 1

    try:
        accuracy = (truePositives + trueNegatives) / (truePositives + trueNegatives + falsePositives + falseNegatives)
    except ZeroDivisionError:
        accuracy = "N/A - Zero Denominator"
    try:
        precision = truePositives / (truePositives + falsePositives)
    except ZeroDivisionError:
        precision = "N/A - Zero Denominator"
    try:
        recall = truePositives / (truePositives + falseNegatives)
    except ZeroDivisionError:
        recall = "N/A - Zero Denominator"
    try: 
        fScore = (2 * precision * recall) / (precision + recall)
    except ZeroDivisionError:
        fScore = "N/A - Zero Denominator"
    except TypeError:
        fScore = "N/A - Precision or Recall Unavailable"
    
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "fScore": fScore}