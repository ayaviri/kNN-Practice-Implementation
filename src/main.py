from database import ExperimentResults
from datasets import glassClean, irisClean
from trainingData import TrainingData
from distanceMetrics import euclideanDistance, minkowskiDistance, manhattanDistance, cosineSimilarity
from experimenter import runTrial
from math import sqrt, floor
from database import SingleTrial, ExperimentResults
import sys

distanceMetrics = {0 : "euclideanDistance", 1 : "manhattanDistance", 2 : "cosineSimilarity"}
kValues = (lambda length : [1, 3, 5, 7, floor(sqrt(length))])

# allows the user to manually run a trial on a dataset with a fixed distance metric
# results of each trial print to console
def manual():
    # create a file in the datasets folder called cleanData, import it, and call it here
    cleanedData = glassClean.cleanData()
    trainingData = TrainingData(cleanedData)
    print()

    while True:
        print("please select a distance metric from the following (choose a number)")
        print("distance metrics: " + str(distanceMetrics))
        distanceMetric = __chooseDistanceMetric(int(input()))
        k = input("please select a value for k: ")
        j = input("please select the size for query set: ")
        labelsAsList = trainingData.getLabels()
        labels = {}
        for i in range(len(labelsAsList)):
            labels[i] = labelsAsList[i]
        print("please select a label from the following (choose a number)")
        print("valid labels: " + str(labels))
        label = labels[int(input())]
        trialOutput = runTrial(trainingData, int(k), int(j), label, distanceMetric)

        print()
        print("results of current trial: " + str(trialOutput))
        print()

# allows the user to run an automatic experiment in which distance metric, k value, and label
# are all altered
# results of the overall experiment print to a text file
def automatic():
    # create a file in the datasets folder called cleanData, import it, and call it here
    cleanedData = glassClean.cleanData()
    trainingData = TrainingData(cleanedData)
    maxTrainingSetSize = len(trainingData.getCurrentTrainingSet()) + len(trainingData.getCurrentQuerySet())
    currentKValues = kValues(maxTrainingSetSize)
    labels = trainingData.getLabels()

    experimentResults = ExperimentResults()
    for i in range(len(distanceMetrics)):
        distanceMetricName = distanceMetrics[i]
        distanceMetric = __chooseDistanceMetric(i)
        for j in range(len(currentKValues)):
            for k in range(len(labels)):
                # a dictionary containing the four statistical measures
                statisticalMeasures = runTrial(trainingData, currentKValues[j], floor(sqrt(maxTrainingSetSize)), labels[k], distanceMetric)
                trial = SingleTrial(distanceMetricName, currentKValues[j], labels[k], statisticalMeasures["accuracy"], statisticalMeasures["precision"], statisticalMeasures["recall"], statisticalMeasures["fScore"])
                experimentResults.addTrial(trial)

    # outputting experiment results to console
    print()
    print("results by distance metrics")
    print(str(experimentResults.byDistanceMetric("euclideanDistance")))
    print(str(experimentResults.byDistanceMetric("manhattanDistance")))
    print(str(experimentResults.byDistanceMetric("cosineSimilarity")))
    print()
    print("results by k value")
    for i in range(len(currentKValues)):
        print(str(experimentResults.byK(currentKValues[i])))
    print()
    print("results by label")
    for i in range(len(labels)):
        print(str(experimentResults.byLabel(labels[i])))

def __chooseDistanceMetric(choice):
    # distanceMetrics = {0 : "euclideanDistance", 1 : "manhattanDistance", 2 : "cosineSimilarity"}
    switcher = {
        0 : (lambda firstVector, secondVector : euclideanDistance(firstVector, secondVector)), 
        1 : (lambda firstVector, secondVector : manhattanDistance(firstVector, secondVector)), 
        2 : (lambda firstVector, secondVector : cosineSimilarity(firstVector, secondVector)), 
    }
    return switcher[choice]

def main():
    methodOfExperiment = sys.argv[1]
    if methodOfExperiment == "-manual":
        manual()
    elif methodOfExperiment == "-automatic":
        automatic()
    else: 
        print("Argument not recognized. Please use either \"-manual\" or \"-automatic\"")

main()