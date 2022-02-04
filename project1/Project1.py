#! /usr/bin/python3

import csv, math, sys
from State import *

"""
CAP 4640: Project 1 - Python Basics

Project1 is an executable program that reads states from a CSV file,
hard coded, storing them in a list. The program provides means to
sort the states, print all states, find and print a state, and prints a
Spearman's rho correlation matrix. This is a command line program.

Author: William L. Thomson Jr.
Version: 1/31/2022
Email: n01479416@unf.edu
"""

def main():
    """
    Main function invoked when the program is run. Reads a hardcoded
    States.csv file and presents the user with a menu of actions available
    """

    print("\nCAP4640 Project 1\nInstructor: Xudong Liu\n")
    filename = "States.csv"
    states = list()

    try:
        file = open(filename, "r")
    except IOError:
        print ("The file %s was not found, aborting." % filename)
        exit()

    lines = csv.reader(file)
    next(lines)
    for line in lines:
        states.append(State(line[0], line[1], line[2], int(line[3]),
                            int(line[4]), int(line[5]), int(line[6]),
                            float(line[7]), int(line[8]), float(line[9])))
    file.close()

    print("There were %d state records read from States.csv.\n" % len(states))

    mainMenu(states)


def mainMenu(states):
    """
    Displays a looping menu until user entry to quit
    :param states a list of states
    """

    nameSorted = False
    opt = 0
    while opt != "6":
        print("1. Print a States report")
        print("2. Sort by Name")
        print("3. Sort by Case Fatality Rate")
        print("4. Find and print a given State")
        print("5. Print Spearman's rho matrix")
        print("6. Quit")
        opt = input("Enter your choice: ")
        while True:
            if opt == "1":
                printStates(states)
                break
            elif opt == "2":
                nameSorted = True
                sortQuickRec(states, 0, len(states)-1)
                print("\nStates sorted by Name.\n")
                break
            elif opt == "3":
                nameSorted = False
                sortMerge(states)
                print("\nStates sorted by Case Fatality Rate.\n")
                break
            elif opt == "4":
                search(states, nameSorted)
                break
            elif opt == "5":
                printSpearmansRHOMatrix(states)
                break
            elif opt == "6":
                print("\nHave a good day!")
                break
            else:
                opt = input("Invalid choice enter 1-6: ")


def merge(states, workSpace, lowPtr, highPtr, upperBound):
    """
    Merge function, sorts list elements in temporary workspace and merges them
    back into original list
    :param states a list of states
    :param workSpace a list the size of states used for temporary storage
    :param lowPtr the low index pointer
    :param highPtr the high index pointer
    :param upperBound the upper bound index of the list
    """
    j = 0
    lowerBound = lowPtr
    mid = highPtr - 1
    n = upperBound - lowerBound + 1
    while lowPtr <= mid and highPtr <= upperBound:
        if states[lowPtr].getCFR() < states[highPtr].getCFR():
            workSpace[j] = states[lowPtr]
            lowPtr += 1
        else:
            workSpace[j] = states[highPtr]
            highPtr += 1
        j += 1

    while(lowPtr <= mid):
        workSpace[j] = states[lowPtr]
        j += 1
        lowPtr += 1

    while highPtr <= upperBound:
        workSpace[j] = states[highPtr]
        j += 1
        highPtr += 1

    for j in range (0,n):
        states[lowerBound+j] = workSpace[j]


def sortMerge(states):
    """
    Merge sort states list by case fatality rate
    :param states a list of states
    """
    elems = len(states)
    workSpace = [None] * elems
    sortMergeRec(states, workSpace, 0, elems-1)


def sortMergeRec(states, workSpace, lowerBound, upperBound):
    """
    Merge sort recursive function, splits up list recursively, sorts and merges
    :param states a list of states
    :param workSpace a list the size of states used for temporary storage
    :param lowerBound the lower bound index of the list
    :param upperBound the upper bound index of the list
    """
    if lowerBound == upperBound:
        return
    mid = (lowerBound+upperBound) // 2
    sortMergeRec(states, workSpace, lowerBound, mid)        # sort low half
    sortMergeRec(states, workSpace, mid+1, upperBound)      # sort high half
    merge(states, workSpace, lowerBound, mid+1, upperBound) # merge them

def printSpearmansRHOMatrix(states):
    """
    Print Spearman's r correlation matrix
    :param states a list of states
    """
    length = len(states)
    caseRateFVR = 0
    caseRateMHI = 0
    caseRateVCR = 0
    deathRateFVR = 0
    deathRateMHI = 0
    deathRateVCR = 0
    divisor = length * (math.pow(length, 2) - 1)
    stateCases = states[:]
    stateDeaths = states[:]
    stateMHI = states[:]
    stateVCR = states[:]
    stateFVR = states[:]
    line = "-" * 50

    # bubble sort stateCases by case rate, stateDeaths by death rate,
    # state FVR by FVR, state MHI by MHI, and state VCR by VCR
    for i in range(0, length):
        for j in range(1, length):
            if stateCases[j - 1].getCaseRate() > stateCases[j].getCaseRate():
                swap(stateCases, j, j - 1)
            if stateDeaths[j - 1].getDeathRate() > stateDeaths[j].getDeathRate():
                swap(stateDeaths, j, j - 1)
            if stateFVR[j - 1].getFVR() > stateFVR[j].getFVR():
                swap(stateFVR, j, j - 1)
            elif stateFVR[j - 1].getFVR() == stateFVR[j].getFVR():
                if stateFVR[j - 1].__gt__(stateFVR[j].getName()):
                    swap(stateFVR, j - 1, j)
            if stateMHI[j - 1].getMHI() > stateMHI[j].getMHI():
                swap(stateMHI, j, j - 1)
            if stateVCR[j - 1].getVCR() > stateVCR[j].getVCR():
                swap(stateVCR, j, j - 1)

    # sum Ds for case rate and MHI, death rate and MHI, case rate and VCR,
    # and death rate and VCR
    for i in range(0, length):
        for j in range(0, length):
            if stateCases[i].getName() == stateFVR[j].getName():
                caseRateFVR += math.pow(i - j, 2)
            if stateDeaths[i].getName() == stateFVR[j].getName():
                deathRateFVR += math.pow(i - j, 2)
            if stateCases[i].getName() == stateMHI[j].getName():
                caseRateMHI += math.pow(i - j, 2)
            if stateDeaths[i].getName() == stateMHI[j].getName():
                deathRateMHI += math.pow(i - j, 2)
            if stateCases[i].getName() == stateVCR[j].getName():
                caseRateVCR += math.pow(i - j, 2)
            if stateDeaths[i].getName() == stateVCR[j].getName():
                deathRateVCR += math.pow(i - j, 2)

    caseRateFVR  = 1 - (6 * caseRateFVR)  / divisor
    deathRateFVR = 1 - (6 * deathRateFVR) / divisor
    caseRateMHI  = 1 - (6 * caseRateMHI)  / divisor
    deathRateMHI = 1 - (6 * deathRateMHI) / divisor
    caseRateVCR  = 1 - (6 * caseRateVCR)  / divisor
    deathRateVCR = 1 - (6 * deathRateVCR) / divisor

    print("\n%s" % line)
    print("|%10s  |%7s    |%7s    |%7s    |"
            % ("COVID-19", "MHI", "VCR", "FVR"))
    print(line)
    print("| Case Rate  |%9.4f  |%9.4f  |%9.4f  |"
            % (caseRateMHI, caseRateVCR, caseRateFVR))
    print(line)
    print("| Death Rate |%9.4f  |%9.4f  |%9.4f  |"
            % (deathRateMHI, deathRateVCR, deathRateFVR))
    print(line, "\n")


def printStates(states):
    """
    Print all states in the list in a table with column header
    :param states a list of states
    """
    print("\n%-14s %-11s %-12s %-13s %-13s %-13s %s" %
            ("Name", "MHI", "VCR", "CFR", "Case Rate", "Death Rate", "FVR"))
    print("-" * 89)
    for s in states:
        print("%-14s %-11d %-12.1f %-13f %-13.2f %6.2f %12.3f" %
              (s.getName(),
                s.getMHI(),
                s.getVCR(),
                s.getCFR(),
                s.getCaseRate(),
                s.getDeathRate(),
                s.getFVR()))
    print()


def search(states, nameSorted):
    """
    Search for a given state, if sorted by name used binary search,
    otherwise use sequential search, prints an error if state is not found
    :param states a list of states
    :param nameSorted boolean to represent if the states are sorted by name
    """
    name = input("\nEnter State name: ")
    if nameSorted:
        searchBinary(states, name)
    else:
        searchSequential(states, name)


def searchBinary(states, name):
    """
    Search for state by name by splitting the list each iteration, binary search
    Prints the state data in a single column key/value format, or
    prints an error if the state is not found
    :param states a list of states
    :param name the name of a state to search the list for
    """
    print("Binary search\n")
    cur = 0
    lower = 0
    upper = len(states) - 1
    while True:
        cur = (lower + upper) // 2
        if states[cur].getName() == name:
            states[cur].printState()
            return
        elif lower > upper:
            print("Error: %s not found\n" % name)
            return
        else:
            if states[cur].getName() < name :
                lower = cur + 1
            else:
                upper = cur - 1


def searchSequential(states, name):
    """
    Search for state by name using sequential list order, sequential search
    Prints the state data in a single column key/value format, or
    prints an error if the state is not found
    :param states a list of states
    :param name the name of a state to search the list for
    """
    print("Sequential search\n")
    for s in states:
        if s.getName() == name:
            s.printState()
            return
    print("Error: %s not found\n" % name)


def sortQuickRec(states, left, right):
    """
    Quicksort recursive function 
    :param states a list of states
    :param left the left position index
    :param right the right position index
    :param pivot a pivot value, a state name
    """
    if right-left <= 0:                                 # if size <= 1
        return                                          # it’s already sorted
    pivot = states[right].getName()                     # rightmost item
    # partition range
    partition = partitionIt(states, left, right, pivot)
    sortQuickRec(states, left, partition-1)             # sort left side
    sortQuickRec(states, partition+1, right)            # sort right side


def swap(states, a, b):
    """
    Swap positions in list
    :param states a list of states
    :param a the position index to swap with b
    :param b the position index to swap with a
    """
    states[a], states[b] = states[b], states[a]


def partitionIt(states, left, right, pivot):
    """
    Split the list into two partitions based on a pivot value
    :param states a list of states
    :param left the left position index
    :param right the right position index
    :param pivot a pivot value, a state name
    :return the left index pointer (left index value) 
    """
    leftPtr = left                                          # left    (after ++)
    rightPtr = right                                        # right-1 (after --)
    while True:
        while leftPtr < right and states[leftPtr].getName() < pivot:    # find bigger item
            leftPtr += 1
        while rightPtr > left and states[rightPtr].getName() > pivot:   # find smaller item  
            rightPtr -= 1
        if leftPtr >= rightPtr:                             # if pointers cross,
            break                                           # partition done
        else:                                               # not crossed, so
            swap(states, leftPtr, rightPtr)                 # swap elements
    return leftPtr


if __name__ == "__main__":
    main()
