from random import choice, randrange
from math import sqrt, floor

# represents a store for homogeneous training data
class TrainingData:
    def __init__(self, trainingSet):
        # ensuring that the training set is not null
        if trainingSet is None: 
            raise Exception("Training set must not be null")
        
        self.trainingSet = trainingSet

        # populating the query set
        querySize = floor(sqrt(len(trainingSet)))
        print("new training data object has been created")
        print("query size has been initialized to: " + str(querySize))
        self.querySet = []
        for i in range(querySize):
            currentQuery = self.trainingSet.pop(randrange(len(self.trainingSet)))
            self.querySet += [currentQuery]
        
        self.labels = []
        for i in range (len(trainingSet)):
            currentLabel = trainingSet[i][1] # each element in trainingSet is (vector, label)
            if currentLabel not in self.labels:
                self.labels += [currentLabel]
        self.multilabelled = len(self.labels) > 2
        
        # choosing a random label to set as the current label
        self.currentLabel = choice(self.labels)
        
    # determines whether or not this set contains more than two labels
    def isMultiLabelled(self):
        return self.multilabelled
        
    # returns the set of labels in this training data
    def getLabels(self):
        return self.labels
    
    # returns the current label of the training set
    # if an element of the query set is labelled as the current label, this corresponds to True 
    # as ground truth, False otherwise
    def getCurrentLabel(self):
        return self.currentLabel
        
    # generates a new label from the available selection at random and returns it to the user
    def generateNewRandomLabel(self):
        self.currentLabel = choice(self.labels)
        return self.currentLabel
        
    # sets the current label to the given one, raises an exception if the label is not contained
    # in the list of valid labels
    def setCurrentLabel(self, newLabel):
        if newLabel not in self.labels:
            raise Exception("Label is not contained in list of existing labels")
        
        self.currentLabel = newLabel
        
    # generates a new query of the given size and returns it to the user. raises
    # an exception if the given size is greater than or equal to the total number
    # of available training samples
    def generateNewQuery(self, querySize):
        if querySize >= (len(self.querySet) + len(self.trainingSet)):
            raise Exception("Size of the query must be strictly less than the length of the training set")
        
        # emptying all the contents of the current query back into the training set
        self.trainingSet.extend(self.querySet)
        self.querySet.clear()
        
        for i in range(querySize):
            currentQuery = self.trainingSet.pop(randrange(len(self.trainingSet)))
            self.querySet += [currentQuery]
            
        return self.querySet
        
    # returns the current query set to the user
    def getCurrentQuerySet(self):
        return self.querySet
    
    # returns the current training set to the user
    def getCurrentTrainingSet(self):
        return self.trainingSet