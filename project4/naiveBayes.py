# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in list(datum.keys()) ]));

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        # dictionary for pixel counters
        pixelCounts = {}

        # initialize counters for every pixel
        for f in self.features:
            pixelCounts[f] = util.Counter()

        # counter for label totals
        labelTotals = util.Counter()
 
        # for each picture in the training data
        for i, pixels in enumerate(trainingData):
            # total times each label has been seen
            labelTotals[trainingLabels[i]] += 1
            # for each pixel
            for f, pixel in pixels.items():
                # if the pixel is off
                if pixel == 0:
                    # increment the count, number of times pixel seen off
                    pixelCounts[f][trainingLabels[i]] += 1

        # copy label totals and normalize label probabilities
        labelProbabilities = labelTotals.copy()
        labelProbabilities.normalize()

        # make global for use in other methods
        self.labelProbabilities = labelProbabilities

        # store best guess
        bestGuess = -1

        # for each k value
        for k in kgrid:
            # create a dictionary of conditional probabilities counters
            condtionalProbabilities = {}

            # loop through each pixel
            for f in self.features:
                # initialize pixel conditional probabilities counter
                condtionalProbabilities[f] = util.Counter()
                
                # perform laplace smoothing using equation
                for label in self.legalLabels:
                    # smoothing pixel at label
                    condtionalProbabilities[f][label] = (pixelCounts[f][label] + k) / (labelTotals[label] + k * 2)

            # make global for use in other methods
            self.condtionalProbabilities = condtionalProbabilities

            # get list of best guesses
            guesses = self.classify(validationData)
            # store the count of correct guesses
            correctCount = 0
            # for every picture in the validation data
            for i in range(len(validationData)):
                # if the guess is the same increment the correct count
                if guesses[i] == validationLabels[i]:
                    correctCount += 1

            # compare the best guess to the current count of guesses
            if bestGuess < correctCount:
                # store current best guess, k, and conditional probabilities
                bestGuess = correctCount
                bestCondtionalProbabilities = condtionalProbabilities
                self.k = k

        # make global for use in other methods
        self.condtionalProbabilities = bestCondtionalProbabilities

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()

        for label in self.legalLabels:
            # log probability for each label
            logJoint[label] = math.log(self.labelProbabilities[label])
            for conditional in self.condtionalProbabilities:
                # probability of label at pixel
                probability = self.condtionalProbabilities[conditional][label]
                # check if pixel is on
                if datum[conditional] == 1:
                    # subtract from 1 since only tracking off pixels
                    probability = 1 - probability
                # add to the log join the log of the pixel probability
                logJoint[label] += math.log(probability)

        return logJoint

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        featuresOdds = []

        # loop through each pixel, only care about odd, so only off
        for f in self.features:
            # get probability of label1 at pixel, 1 - for odd probability
            probability1 = 1 - self.condtionalProbabilities[f][label1]
            # get probability of label2 at pixel, 1 - for odd probability
            probability2 = 1 - self.condtionalProbabilities[f][label2]
            # get the ratio of label 1 probability / label 2 probability
            oddsRatio = probability1 / probability2
            # add the ratio at pixel to the list
            featuresOdds.append((oddsRatio, f))

        # sort the odd pixels
        featuresOdds = sorted(featuresOdds)

        # store the 100 best odd pixels
        featuresOdds = [f for r, f in featuresOdds[-100:]]

        return featuresOdds
