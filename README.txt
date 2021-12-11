welcome to my implementation of the beginner classification algorithm, k-nearest neighbors!
in order to use this program, please read the following and the instruction in "USEME.txt"

SUMMARY OF IMPLEMENTATION + DESIGN OF CODE:
below is a brief summary of each file and its purpose in the "src" folder
- knn.py: this file stores the implementation of knn itself. the knn method takes in a training set, 
          which is the list of datapoints from which the algorithm will classify element in the 
          query set, a value of k which specifies how many neighbors are to be considered in the 
          voting, a query set, which is a subset of the training population, whose labels are 
          "unknown" to knn, and whose labels the algorithm is trying to figure out based on its
          closest neighbors, and, finally, a distance metric which is to be used when determining
          the distance or similarity between an element of the training set and an element of the 
          query set. the only thing to point out in this implementation is the use of a priority 
          queue or max heap in order to store the current set of the k closest neighbors. the
          elements in this queue are ordered by distance in descending order, with the farthest
          neighbor at the root of the queue. initally, k elements from the training set are chosen
          at random as the k closest neighbors. then, knn iterates through each element in the 
          training set, check to see if the current element is closer to the current query element
          than the farthest neighbor. if so, the root neighbor is extracted from the queue, and the
          current neighbor is then placed at the appropriate position in the queue. this decision, 
          in retrospect, was not entirely necessary, as k remains mostly constant with respect to
          the size of the training set. however, a subset of the trials done in the experiment use 
          the square root of n, where n is the size of the training set, as a value of k. as such, 
          the improvement from O(k) to O(log(k)) for each element in the training set is minor, 
          and not noticeable in practice. 
- priorityQueue.py: this file stores the representation of the priority queue used in the 
                    implemenation of knn. behind the scenes, there are three data structures being
                    used. there are two maps. the first which maps from the neighbor's index in the
                    training set (*) to its index in the array used to store the heap itself. the
                    second is a map in the reverse direction. this allows for quick access of 
                    elements by either key or value (**). finally, the heap itself is stored not in
                    a binary tree, but an array whose indices reveal the element's position in the
                    tree. this array contains the distance from each neighbor to the current query
                    element. otherwise, the implementation of this priority queue is pretty 
                    standard
- distanceMetric.py: this file stores all of the available distance metrics. the minkowski distance
                     metric is included here, but it is not used, as it requires an additional 
                     parameter. if you desire to add another distance metric, follow these steps
                     - write the distance metric as a function in this file
                     - NOTE: this distance metric must only take in the two vectors
                     - add the following import in "main.py": "from distanceMetrics import
                       nameOfFunction"
                     - add to the global dictionary "distanceMetrics" the entry 
                       "lengthOfDictionary : "nameOfFunction""
                     - in the private helper "__chooseDictionary", add the following entry to the 
                       "switcher" dictionary "lengthOfDictionary : (lambda firstVector, 
                       secondVector : nameOfFunction(firstVector, secondVector))"
- trainingData.py: this file stores all of the information needed to manipulate a dataset. an 
                   object of this class is constructed with just the output of the "cleanData" 
                   function of the corresponding dataset. upon construction, a query set whose size
                   is sqrt(n), is removed from the training set and maintained as the current
                   query set. in addition to this, a list of all the labels in the dataset is 
                   maintained, and one from this list is chosen as random as the current label (***).
                   a user can then perform a variety of operations, the most important being the
                   generation of a new random query set of a given length. this places all of the
                   elements in current query set back into the training set, and select a new
                   random subset of the desired size. 
- experimenter.py: this file stores function that acts as the middle man between "main.py" and 
                   "knn.py". this function runs a single trial of knn, taking in a TrainingData
                   object, k, the desired size of the new query set, and the desired distance 
                   metric. from here, this function creates the appropriate query and corresponding
                   training set from the TrainingData object, runs knn once, calculates the 
                   four statistical measures of the trial, and outputs them in a dictionary to
                   be used for display and analysis
- database.py: this file stores my solution for data storage. initially, i ran into the issue of 
               result storage. i wanted to display the results across all trials for each variable,
               and i couldn't figure out an easy solution for this. my next idea was to connect a
               SQLite database to the program corresponding with a given dataset, but, in order to
               avoid the nightmare that this is, i decided to create my own representation of a 
               data store or database in python that performs the operations i need. as such, there
               are two classes in this file. the first class, "SingleTrial" represents a row in a 
               database, with all of the information collected from a single trial. the second 
               class, "ExperimentResults" stores the entirety of an experiment as a list of 
               SingleTrial objects. given an object of the ExperimentResults class, one can obtain
               the average statistical measures across all trials for a single variable, which 
               greatly the readability of the results. this information is then used in the 
               "automatic" function of "main.py", where an experiment, with a trial for each 
               combination of settings described in the first section of "USEME.txt", is run until
               completion. 

(*) i understand there is no sense of order in a set, but the training set is being stored in an
    array, and the easiest way to identify it was to use its index in the array. for all other
    purposes, the training set can be thought of as a set
(**) i hope to implement a bidirectional map in the future as a slight optimization in favor of
     this approach
(***) a note on labels: the term "label" is used throughout this program. in order to force a 
binary labelling in multi-labelled datasets, one of the many labels is chosen as corresponding 
to True in Ground Truth. a classification of an element in the query set as any other label is
then treated as False. this forced binary simplifies the calculation of the four statistical 
measures used. the downside of this system is that these calculations only serve to analyse how
well the algorithm discriminates against the current label. in reality, the algorithm is capable 
of accurately classifying ALL labels. as such, some of the information captured by the algorithm
is lost. 