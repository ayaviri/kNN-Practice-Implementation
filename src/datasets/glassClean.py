import csv

# cleans the data in glassTrain.csv and returns the data in the following format for the 
# knn implementation: (list (vector, label))
def cleanData():
    outputTrainingData = []
    with open("datasets/glassTrain.csv") as csvFile:
        csvReader = csv.reader(csvFile)
        # we will skip the headers for now
        next(csvReader)
        for row in csvReader:
            label = row[len(row) - 1]
            vector = [float(x) for x in row[1:]]
            outputTrainingData += [(vector, label)]
    return outputTrainingData
