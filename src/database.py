# represents a single trial or row in an automated experiment
class SingleTrial:
    def __init__(self, distanceMetric, k, label, accuracy, precision, recall, fScore):
        self.distanceMetric = distanceMetric
        self.k = k
        self.label = label
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.fScore = fScore

    # returns as a string the distance metric used for this trial
    def getDistanceMetric(self):
        return self.distanceMetric
    
    # returns as a string the k value used for this trial
    def getK(self):
        return self.k

    # returns as a string the label used for this trial
    def getLabel(self):
        return self.label

    # returns the accuracy of this trial - may or may not be valid depending on the query set used
    def getAccuracy(self):
        return self.accuracy

    # returns the precision of this trial - may or may not be valid depending on the query set used
    def getPrecision(self):
        return self.precision

    # returns the recall of this trial - may or may not be valid depending on the query set used
    def getRecall(self):
        return self.recall

    # returns the f-score of this trial - may or may not be valid depending on the query set used
    def getFScore(self):
        return self.fScore

# represents a table of all the trials performed in an automated experimented
class ExperimentResults:
    def __init__(self):
        self.trials = []
        self.distanceMetrics = []
        self.kValues = []
        self.labels = []

    # adds a single trial to the experiment
    def addTrial(self, trial):
        self.trials += [trial]
        distanceMetric = trial.getDistanceMetric()
        k = trial.getK()
        label = trial.getLabel()

        # adding the distance metric, k value, and label to the list from which to query
        if distanceMetric not in self.distanceMetrics:
            self.distanceMetrics += [distanceMetric]
        if k not in self.kValues:
            self.kValues += [k]
        if label not in self.labels: 
            self.labels += [label]

    # returns an average across all trials of each of the four statistical measures calculated
    # by distance metric
    def byDistanceMetric(self, distanceMetric):
        if distanceMetric not in self.distanceMetrics:
            raise Exception("Distance metric not used in the experiment")

        outputTrials = [trial for trial in self.trials if trial.getDistanceMetric() == distanceMetric]
        results = self.__calculateStaticalMeasures(outputTrials)
        results["distanceMetric"] = distanceMetric
        return results

    # returns an average across all trials of each of the four statistical measures calculated
    # by k value
    def byK(self, kValue):
        if kValue not in self.kValues:
            raise Exception("K value not used in the experiment")
        
        outputTrials = [trial for trial in self.trials if trial.getK() == kValue]
        results = self.__calculateStaticalMeasures(outputTrials)
        results["kValue"] = kValue
        return results

    # returns an average across all trials of each of the four statistical measures calculated
    # by label
    def byLabel(self, label):
        if label not in self.labels:
            raise Exception("Label not contained in the training data")

        outputTrials = [trial for trial in self.trials if trial.getLabel() == label]
        results = self.__calculateStaticalMeasures(outputTrials)
        results["label"] = label
        return results

    # a private helper to calculate statistical measures of across all trials by category
    def __calculateStaticalMeasures(self, outputTrials):
        totalAccuracy = 0
        totalPrecision = 0
        totalRecall = 0
        totalFScore = 0
        validTrials = 0
        for i in range(len(outputTrials)):
            currentTrial = outputTrials[i]
            trialAccuracy = currentTrial.getAccuracy()
            trialPrecision = currentTrial.getPrecision()
            trialRecall = currentTrial.getRecall()
            trialFScore = currentTrial.getFScore()

            if (type(trialAccuracy) is float) and (type(trialPrecision) is float) and (type(trialRecall) is not str) and (type(trialFScore) is not str):
                totalAccuracy += trialAccuracy
                totalPrecision += trialPrecision
                totalRecall += trialRecall
                totalFScore += trialFScore
                validTrials += 1

        return {"validTrials" : validTrials, "averageAccuracy" : (totalAccuracy / validTrials), "averagePrecision" : (totalPrecision / validTrials), "averageRecall" : (totalRecall / validTrials), "averageFScore" : (totalFScore / validTrials)}