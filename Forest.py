## Forest Hughes

import numpy as np
import math
import DTree
from DTree import * 
    
class RForest():
    def __init__(self, depth, impurity, segmentor, num):
        self.depth = depth
        self.impurity = impurity
        self.segmentor = segmentor
        self.num = num
        self.trees = []
            
    def train(self, data, labels):
        num_features = len(data[0])
        k = math.floor(len(labels)/float(self.num))
        p = math.ceil(np.sqrt(num_features))
        
        for i in range(self.num):
            indices_to_delete = np.random.permutation(num_features)[p:]
            tree = DTree(self.depth, self.impurity, self.segmentor)
            tree.train(np.delete(data[int(i*k):int((i+1)*k)], [], 1), labels[int(i*k):int((i+1)*k)])
            if not isinstance(tree.root, LeafNode):
                pass
            self.trees.append(tree)
            
        
    def predict(self, data):
        predictions = []
        votes = []
        for tree in self.trees:
            votes.append(tree.predict(data))
            
        for i in range(len(votes[0])):
            if np.sum(np.array(votes)[:,i]) > len(votes)/float(2):
                predictions.append(1)
            else:
                predictions.append(0)
        return predictions
