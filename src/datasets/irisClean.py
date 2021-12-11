import json

# cleans the data in irisTrain.json and returns the data in the following format for the 
# knn implementation: (list (vector, label))
def cleanData():
    outputTrainingData = []
    with open("datasets/irisTrain.json") as jsonFile:
        jsonData = json.load(jsonFile)
        for i in range(len(jsonData)):
            currentDataPoint = jsonData[i]
            currentVector = [currentDataPoint["sepalLength"], currentDataPoint["sepalWidth"], currentDataPoint["petalLength"], currentDataPoint["petalWidth"]]
            currentLabel = currentDataPoint["species"]
            outputTrainingData += [(currentVector, currentLabel)]
    return outputTrainingData

    