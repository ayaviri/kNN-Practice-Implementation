from math import floor 

# represents a priority queue 
class PriorityQueue():
    def __init__(self, capacity) -> None:
        self.capacity = capacity # the number of elements in queue
        self.indices = {} # map from element id to index in values array
        self.reverseIndices = {} # map from index in values array to element id
        self.values = [] # an array of all the distances, represents heap data structure

    # determines whether the given key is contained in the priority queue
    def contains(self, elementKey):
        return elementKey in self.indices

    # inserts the value with the given key and given value at the correct position in the priority queue
    def insert(self, elementKey, elementValue):
        # ensuring that the elementKey is not already contained in the queue
        if self.contains(elementKey):
            raise Exception("This element is already contained in the priority queue")

        self.values += [elementValue]
        if len(self.values) > 1:
            self.__upheap(elementKey, len(self.values) - 1, elementValue)
        else:
            self.indices[elementKey] = 0
            self.reverseIndices[0] = elementKey
        return 0

    # a private helper to upheap a new value
    def __upheap(self, elementKey, currentElementIndex, elementValue):
        # we have ensured that there is at least two elements in the queue
        if currentElementIndex % 2 == 0:
            parentIndex = int((currentElementIndex / 2) - 1)
        else: 
            parentIndex = int(floor(currentElementIndex / 2))
        parentValue = self.values[parentIndex]
        parentKey = self.reverseIndices[parentIndex]

        while parentValue < elementValue:
            # we swap the two elements in the values array
            self.values[parentIndex], self.values[currentElementIndex] = self.values[currentElementIndex], self.values[parentIndex]

            # we fix the index the parentKey points to
            self.indices[parentKey] = currentElementIndex
            self.reverseIndices[currentElementIndex] = parentKey

            # calculating new indices
            currentElementIndex = parentIndex
            if currentElementIndex == 0:
                break

            if currentElementIndex % 2 == 0:
                parentIndex = int((currentElementIndex / 2) - 1)
            else: 
                parentIndex = int(floor(currentElementIndex / 2))
            parentValue = self.values[parentIndex]
            parentKey = self.reverseIndices[parentIndex]

        # assigning the index the elementKey now points to
        self.indices[elementKey] = currentElementIndex
        self.reverseIndices[currentElementIndex] = elementKey

    # peeks the value of the element at the front of the priority queue
    def peekRoot(self):
        return self.values[0]

    # returns and removes the value of the element at the front of the priority queue
    # and restores the heap invariant
    def extractRoot(self):
        # ensuring that the queue isn't empty
        if len(self.values) == 0:
            raise Exception("Cannot extract from an empty queue")
        
        # rootKey = self.reverseIndices[0]
        rootValue = self.values[0]
        self.indices.pop(self.reverseIndices.pop(0))
        if len(self.values) == 1:
            self.values.pop(0)
            return rootValue

        # grabbing the last node, severing connection, and placing the value at the front of the values array
        parentValue = self.values[len(self.values) - 1]
        parentKey = self.reverseIndices[len(self.values) - 1]
        self.reverseIndices.pop(self.indices.pop(parentKey))
        self.values[0] = self.values.pop()

        # calculating indices
        parentIndex = 0
        leftChildIndex = 1
        rightChildIndex = 2
        while ((rightChildIndex < len(self.values)) and (parentValue < min(self.values[leftChildIndex], self.values[rightChildIndex]))) or ((leftChildIndex < len(self.values)) and (parentValue < self.values[leftChildIndex])):
            if (rightChildIndex < len(self.values)) and (self.values[rightChildIndex] > self.values[leftChildIndex]):
                # parent must be swapped with right child
                self.values[parentIndex], self.values[rightChildIndex] = self.values[rightChildIndex], self.values[parentIndex]

                # fixing the mapping of the right child
                rightChildKey = self.reverseIndices[rightChildIndex]
                self.reverseIndices.pop(self.indices.pop(rightChildKey))
                self.indices[rightChildKey] = parentIndex
                self.reverseIndices[parentIndex] = rightChildKey

                parentIndex = rightChildIndex
            else: 
                # parent must be swapped with left child
                self.values[parentIndex], self.values[leftChildIndex] = self.values[leftChildIndex], self.values[parentIndex]

                # fixing the mapping of the left child
                leftChildKey = self.reverseIndices[leftChildIndex]
                self.reverseIndices.pop(self.indices.pop(leftChildKey))
                self.indices[leftChildKey] = parentIndex
                self.reverseIndices[parentIndex] = leftChildKey

                parentIndex = leftChildIndex
            
            # calculating new indices and values
            parentValue = self.values[parentIndex]
            leftChildIndex = (parentIndex * 2) + 1
            rightChildIndex = (parentIndex * 2) + 2
        
        # fixing the mapping of the original parent key
        self.indices[parentKey] = parentIndex
        self.reverseIndices[parentIndex] = parentKey
        return rootValue

    # returns a list of all the keys in the priority queue
    def getIndices(self):
        return self.indices.keys()