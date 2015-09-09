## Forest Hughes

import numpy as np

class Node:
    def __init__(self, rule, left, right):
        self.rule = rule
        self.left = left
        self.right = right
        
class LeafNode:
    def __init__(self, label):
        self.label = label
        
class DTree:
    def __init__(self, depth, impurity, segmentor):
        self.depth = depth
        self.impurity = impurity
        self.segmentor = segmentor
        self.root = None
        
    def train(self, data, labels):
        self.root = self.train_helper(data, labels, 0)
       
    def train_helper(self, data, labels, depth):
        if (labels.count(0) == len(labels)):
            return LeafNode(0)
        elif (labels.count(1) == len(labels)):
            return LeafNode(1)
            
        if depth >= self.depth:
            if (labels.count(0) > labels.count(1)):
                return LeafNode(0)
            else:
                return LeafNode(1)
                
        rule = self.segmentor(data, labels, self.impurity)
        print rule, "\n"
        split = rule[0]
        threshold = rule[1]
        left = []
        right = []
        left_labels = []
        right_labels = []
        for i in range(len(data)): 
            if data[i][split] < threshold: 
                left.append(data[i]) #add the feature to the left data
                left_labels.append(labels[i])
            else:
                right.append(data[i])
                right_labels.append(labels[i])
        return Node(rule, self.train_helper(np.array(left), left_labels, depth+1), self.train_helper(np.array(right), right_labels, depth+1))
            
    def predict(self, data):
        predictions = []
        for i in range(len(data)):
            node = self.root
            predictions.append(self.predict_helper(node, data, i))
            print "\n"
        return predictions
            
    @staticmethod
    def predict_helper(node, data, i):
    
        while True:
            if isinstance(node, LeafNode):
                print node.label, "Label"
                return node.label
            rule = node.rule
            split = rule[0]
            threshold = rule[1]
            if data[i][split] < threshold:
                print "feature ", split, "(", features[split], ") : $ < $", threshold, "\\\\"
                node = node.left
            else: 
                print "feature ", split, "(", features[split], ") : $\geq$", threshold, "\\\\"
                node = node.right
                
            
        
def gini_impurity(left_label_hist, right_label_hist):
    if left_label_hist[0] == 0 and left_label_hist[1] == 0:
        f_0_left = 0
        f_1_left = 0
    else:
        f_0_left = left_label_hist[0]/float(left_label_hist[0] + left_label_hist[1])
        f_1_left = left_label_hist[1]/float(left_label_hist[0] + left_label_hist[1])
        
    if right_label_hist[0] == 0 and right_label_hist[1] == 0:
        f_0_right = 0
        f_1_right = 0
    else:
        f_0_right = right_label_hist[0]/float(right_label_hist[0] + right_label_hist[1])
        f_1_right =  right_label_hist[1]/float(right_label_hist[0] + right_label_hist[1])
    return 2 - f_0_left**2 - f_1_left**2 - f_0_right**2 - f_1_right**2
    
def segmentor(data, labels, impurity):
    splitting_index = 0 #which feature to split on.  
    impurity_measure = float("Inf")
    threshold = 0
    for i in range(len(data[0])):
        left_split = []
        left_labels =[]
        right_split = []
        right_labels = []
        cur_thresh = np.mean(data[:,i])
        for j in range(len(data)): # for every sample we want to count the number of 1's and 0's, the one with the biggest difference is the splitting index
            if data[j][i] < cur_thresh: #if the feature value is less than the threshold
                left_split.append(data[j]) #add the feature to the left data
                left_labels.append(labels[j]) #and append the corresponding label to the left labels
            else:
                right_split.append(data[j])
                right_labels.append(labels[j])
        left_hist = []
        right_hist = []
        left_hist.append(left_labels.count(0)) 
        left_hist.append(left_labels.count(1))
        right_hist.append(right_labels.count(0))
        right_hist.append(right_labels.count(1))
        
        pot_imp = impurity(left_hist, right_hist) 
        if pot_imp < impurity_measure:
            impurity_measure = pot_imp
            splitting_index = i
            threshold = cur_thresh
    
    return (splitting_index, threshold)