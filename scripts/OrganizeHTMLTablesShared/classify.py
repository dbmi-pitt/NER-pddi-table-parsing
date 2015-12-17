# -*- coding: utf-8 -*-

import re
import os
import string
from bs4 import BeautifulSoup


def converToStructureDict(structure):
    finaldict = {}
    for s in structure:
        splits = s.split("\t", 1)
        if splits[1] not in finaldict.keys():
            finaldict[splits[1]] = splits[0]
        elif splits[1] in finaldict.keys():
            hold = finaldict[splits[1]]
            hold += " " + splits[0]
            finaldict[splits[1]] = hold
    return finaldict


###############################################################
# Convenience function to clear header of all leading and     #
# trailing white spaces, commas or unneeded formatting.       #
# Returns a 'cleaned' string.                                 #
###############################################################


def cleanUp(s):
    s = s.translate(None, '[\t\n\r]')
    s = s.strip()
    s = s.lstrip(',')
    s = s.strip()
    s = s.rstrip(',')
    s = s.strip()
    return s

###############################################################
# Convenience function to generate a list of each table's     #
# headers. Returns a list of headers or None if empty.        #
# Removes all non-printable strings contained in header       #
# - this helps with encoding/decoding issues that caused      #
#   mismatched strings to occur.                              #
###############################################################


def generateList(x):
    holdHeaders = []
    x = filter(lambda y: y in string.printable, x)
    x = x.translate(None, '[')
    x = x.translate(None, ']')
    x = x.strip()
    if 'DRUGS WITH CLINICAL RECOMMENDATIONS REGARDING COADMINISTRATION' in x:
        holdHeaders.append('DRUGSWITHCLINICALRECOMMENDATIONSREGARDINGCOADMINISTRATIONSEEPRECAUTIONSDRUGINTERACTIONS')
        return holdHeaders
    elif 'DRUG INTERACTIONS ASSOCIATED WITH INCREASED RISK OF MYOPATHY' in x:
        holdHeaders.append('DRUGINTERACTIONSASSOCIATEDWITHINCREASEDRISKOFMYOPATHYRHABDOMYOLYSIS2245271727374123')
        return holdHeaders
    elif 'STRONG CYP3A4 (EG, KETOCONAZOLE) OR CYP2D6 (EG, FLUOXETINE) INHIBITORS WILL INCREASE ABILIFY DRUG CONCENTRATIONS' in x:
        holdHeaders.append('STRONGCYP3A4EGKETOCONAZOLEORCYP2D6EGFLUOXETINEINHIBITORSWILLINCREASEABILIFYDRUGCONCENTRATIONSREDUCEABILIFYDOSEBYONEHALFWHENUSEDCONCOMITANTLY2671EXCEPTWHENUSEDASADJUNCTIVETREATMENTWITHANTIDEPRESSANTS26CYP3A4INDUCERSEGCARBAMAZEPINEWILLDECREASEABILIFYDRUGCONCENTRATIONSDOUBLEABILIFYDOSEWHENUSEDCONCOMITANTLY2671')
        return holdHeaders
    elif 'INCREASED RISK OF MYOPATHY' in x:
        holdHeaders.append('INCREASEDRISKOFMYOPATHYRHABDOMYOLYSIS2517123')
        return holdHeaders
    elif x is not None:
        splits = x.split(" , ")
        for n in range(0, len(splits)):
            holdHeaders.append(str(re.sub(r'[\W_]+', '', splits[n])))

    return holdHeaders


###############################################################
# Convenience function to create a string that contains:      #
# Table's name and its corresponding categorical header       #
# structure (tab-separated); returns as a string.             #
###############################################################


def generateStructure(name, headers, c):
    s = name
    for header in headers:
        header = cleanUp(header)
        if header in c:
            s += '\t' + str(c[str(header)])
        elif header not in c:
            if header == ',':
                pass
            else:
                s += '\t' + 'ERR:HEADER NOT FOUND:' + str(header)
    return s


###############################################################
# Convenience function to transform the list of strings       #
# containing each table's categorical structure to a list of  #
# lists, containing each table name and categories.           #
###############################################################


def createList(structure):
    final = []
    for s in structure:
        hold = []
        splits = s.split('\t')
        hold.append(splits[0])
        for i in range(1, len(splits)-1):
            hold.append(splits[i])
        final.append(hold)
    return final


###############################################################
# Create a dict that stores each table header (key) with its  #
# corresponding category (value). Can write it to txt file.   #
# Also generates a list that contains strings of each table   #
# name and the categorical structure of the table's headers.  #
###############################################################


def classify():
    headerClassification = {}
    tableStructure = []

    dir = os.path.dirname(__file__)

    db = os.path.join(dir, "Categories.txt")  # relative path
    data = open(db, "rb")

    # Generate the dictionary headerClassification = { header : category }
    with data as txtData:
        for line in txtData:
            line = line.translate(None, '[\n\r]')
            line = filter(lambda x: x in string.printable, line)
            line = re.split(r"\t+", line.strip("\n"))
            zero = re.sub(r'[\W_]+', '', line[0])
            if line[1] in headerClassification:
                if zero not in headerClassification.values():
                    headerClassification[line[1]].append(zero)
                else:
                    break
            else:
                headerClassification.update({zero: line[1]})

    # print headerClassification

    # Testing purposes ######### Testing Purposes ######### Testing Purposes ################
    '''for key in headerClassification:
        print key + ' is the table header which is part of this category: ' + str(headerClassification[key])

    print 'The dict contains ', len(headerClassification.keys()), ' unique keys.'

    file = open(os.path.join(dir, "testingCreateDict.txt"), "w")
    file.write(str(headerClassification)) '''
    # Testing purposes ######### Testing Purposes ######### Testing Purposes ################

    # Absolute path of the directory where the program resides
    dir = os.path.dirname(__file__)
    input = open(os.path.join(dir, "output.txt"), "r")
    htmlParse = input.read().decode("utf-8")

    # Section prepares each part for addition to tableInfo dictionary
    soup = BeautifulSoup(htmlParse, "html.parser")
    tables = soup.findChildren("table")  # (ResultSet) - finds all the <table> tags in the HTML of output.txt

    # Creates a list of table names (List) -- using input tag to define table name which is stored in value attribute
    tableIDs = [(n["value"]) for n in soup.findChildren("input")]

    # Go through tables and print each tables' categorical structure.
    # Iterates through all of the tableIDs and gathers each table's content
    for c in range(0, len(tableIDs) - 1):  # Goes through all tables
        tableNo = tables[c].findChildren(["tr"])  # Finds all rows in a table (ResultSet)
        # Gathers the headers from each table's content
        for line in tableNo:
            if (line.findChildren(["th", tableNo.index(line) == 0 and line.findChildren(["th"])])) or \
                    (tableNo.index(line) == 0 and line.findChildren(["td"])):
                soup = BeautifulSoup(str(line.findChildren(["th", "td"])))  # -- ** try to remove str() - complete eval on this (turn string to list)
                # Properly formats and encodes **SOME** of the table headers
                tempData = (re.sub(' +', ' ', soup.text.strip("\t\n\r").replace("\n", "").strip())).upper().encode("utf-8")

                # Gathers table headers for classification and construction of categorical assignment string
                tableStructure.append(generateStructure(str(tableIDs[c]), generateList(str(tempData)), headerClassification))

    # Prints each table that does not contain a 'HEADER NOT FOUND' error
    '''for s in tableStructure:
        # if "ERR:HEADER NOT FOUND" not in s:
            print s'''

    dict = converToStructureDict(tableStructure)
    print "There are " + str(len(dict.keys())) + " unique table structures. \n"

    for key in dict:
        if key in dict.keys():
            splits = dict[key].split(' ')
            print 'Table Header Structure: '
            print key
            print str(len(splits)) + ' tables.'
            print '\n'
            # for s in splits:
                # print s



    # Prints each table's structure (listForm) including all errors
    '''listForm = createList(tableStructure)
    for indvList in listForm:
        s = ''
        for item in indvList:
            s += item + ' '
        print s '''


###############################################################
# Main code                                                   #
###############################################################


classify()
