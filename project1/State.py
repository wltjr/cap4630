#! /usr/bin/python3

import sys

"""
State class represents one of the 50 states of the United States of
America with various attributes relating to the COVID-19 pandemic.

Author: William L. Thomson Jr.
Version: 1/22/2022
Email: n01479416@unf.edu
"""

class State:
    """
    State class represents one of the 50 states of the United States of
    America with various attributes relating to the COVID-19 pandemic.
    """

    def __init__(self, name, capitol, region, houseSeats, population,
                 covidCases, covidDeaths, fvr, mhi, vcr):
        """
        State class constructor to create new instances of State class/object

        :param name             the name of the state
        :param capitol          the name of the state's capitol
        :param region           the state's region
        :param houseSeats       the number of house seats for the state
        :param population       the population of the state
        :param covidCases       the number of COVID cases in the state
        :param covidDeaths      the number of COVID deaths in the state
        :param fvr              the full vaccination rates of the state
        :param mhi              the median household of the state
        :param vcr              the violent crime rate for the state
        """
        self.name = name
        self.capitol = capitol
        self.region = region
        self.houseSeats = houseSeats
        self.population = population
        self.covidCases = covidCases
        self.caseRate = (self.covidCases / self.population) * 100000
        self.covidDeaths = covidDeaths
        self.deathRate = (self.covidDeaths / self.population) * 100000
        self.cfr = self.deathRate / self.caseRate
        self.fvr = fvr / 100
        self.mhi = mhi
        self.vcr = vcr

    def __gt__(self, name):
        """
        Compares two State objects based on state names
        :param name the Name of a state to compare
        :return boolean if this state name is greater than compared state name 
        """
        return self.name > name

        
    def __str__(self):
        """
        Prints a state object's information as formatted columns
        """
        return "%s %s %s %d %d %d %d %.1f\n" % (
                             self.name, self.capitol, self.region,
                             self.population, self.covidCases, self.covidDeaths,
                             self.mhi, self.vcr)
        
    def printState(self):
        """
        Prints a state object's information as formatted column in rows
        """
        print("%-11s %s" % ("Name:", self.name))
        print("%-11s %d" % ("MHI:", self.mhi))
        print("%-11s %.1f" % ("VCR:", self.vcr))
        print("%-11s %.6f" % ("CFR:", self.cfr))
        print("%-11s %.2f" % ("Case Rate:", self.caseRate))
        print("%-11s %.2f" % ("Death Rate:", self.deathRate))
        print("%-11s %.3f" % ("FV Rate:", self.fvr))
        print("")

    def getCFR(self):
        """
        Get the case fatality rate of the state
        :return the case fatality rate of the state
        """
        return self.cfr

    def getCapitol(self):
        """
        Get the name of the state's capitol
        :return the name of the state's capitol
        """
        return self.capitol

    def getCaseRate(self):
        """
        Get the rate of cases in the state
        :return the rate of cases in the state
        """
        return self.caseRate

    def getCovidCases(self):
        """
        Get the number of COVID cases in the state
        :return the number of COVID cases in the state
        """
        return self.covidCases

    def getCovidDeaths(self):
        """
        Get the number of COVID deaths in the state
        :return the number of COVID deaths in the state
        """
        return self.covidDeaths

    def getDeathRate(self):
        """
        Get the rate of deaths in the state
        :return the rate of deaths in the state
        """
        return self.deathRate

    def getFVR(self):
        """
        Get the full vaccination rates of the state
        :return the full vaccination rates of the state
        """
        return self.fvr

    def getHouseSeats(self):
        """
        Get the number of seats the state has in the house of congress
        :return the number of house seats for the state
        """
        return self.houseSeats

    def getMHI(self):
        """
        Get the median household of the state
        :return the median household of the state
        """
        return self.mhi

    def getName(self):
        """
        Get the name of the state
        :return the name of the state
        """
        return self.name

    def getPopulation(self):
        """
        Get the population of the state
        :return the population of the state
        """
        return self.population

    def getRegion(self):
        """
        Get the state's region
        :return the state's region
        """
        return self.region

    def getVCR(self):
        """
        Get the violent crime rate for the state
        :return the violent crime rate for the state
        """
        return self.vcr

    def setCFR(self, cfr):
        """
        Set the case fatality rate of the state
        :param cfr the case fatality rate of the state
        """
        self.cfr = cfr

    def setCapitol(self, capitol):
        """
        Set the name of the state's capitol
        :param capitol the name of the state's capitol
        """
        self.capitol = capitol

    def setCaseRate(self, caseRate):
        """
        Set the rate of cases in the state
        :param caseRate the rate of cases in the state
        """
        self.caseRate = caseRate

    def setCovidCases(self, covidCases):
        """
        Set the number of COVID cases in the state
        :param covidCases the number of COVID cases in the state
        """
        self.covidCases = covidCases

    def setCovidDeaths(self, covidDeaths):
        """
        Set the number of COVID deaths in the state
        :param covidDeaths the number of COVID deaths in the state
        """
        self.covidDeaths = covidDeaths

    def setDeathRate(self, deathRate):
        """
        Set the rate of deaths in the state
        :param deathRate the rate of deaths in the state
        """
        self.deathRate = deathRate

    def setFVR(self, fvr):
        """
        Set the full vaccination rates of the state
        :param fvr the full vaccination rates of the state
        """
        self.fvr = fvr

    def setHouseSeats(self, houseSeats):
        """
        Set the number of seats the state has in the house of congress
        :param houseSeats the number of house seats for the state
        """
        self.houseSeats = houseSeats

    def setMHI(self, mhi):
        """
        Set the median household of the state
        :param mhi the median household of the state
        """
        self.mhi = mhi

    def setName(self, name):
        """
        Set the name of the state
        :param name the name of the state
        """
        self.name = name

    def setPopulation(self, population):
        """
        Set the population of the state
        :param population the population of the state
        """
        self.population = population

    def setRegion(self, region):
        """
        Set the state's region
        :param region the state's region
        """
        self.region = region

    def setVCR(self, vcr):
        """
        Set the violent crime rate for the state
        :param vcr the violent crime rate for the state
        """
        self.vcr = vcr

