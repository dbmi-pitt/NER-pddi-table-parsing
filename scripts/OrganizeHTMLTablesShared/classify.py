# -*- coding: utf-8 -*-

###############################################################
# Generates unique table header structures and saves the      #
# result as a text file titled "table_structures.txt".        #
# Stored as key (table header structure) and                  #
# value (table-names). Can parse as dictionary.               #
###############################################################
# Author: Steven DeMarco                                      #
###############################################################

import re
import os
import string
from bs4 import BeautifulSoup

###############################################################
# Convenience function to convert the list into the final     #
# structure of key (structure) : value (table-name).          #
# Returns the final dictionary.                               #
###############################################################


def convertToStructureDict(structure):
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
# ** Removes all non-printable strings contained in header    #
# ** - helps with encoding/decoding issues that caused        #
# **   mismatched strings to occur.                           #
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
# Params: (TABLE-NAME , HEADERS-LIST , CATEGORIES-LIST)       #
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

    db = os.path.join(dir, "output/Categories.txt")  # relative path
    data = open(db, "rb")

    # Generate the dictionary headerClassification = { header : category }
    # Removes any non-printable strings and whitespaces
    with data as txtData:
        for line in txtData:
            line = line.translate(None, '[\n\r]')
            line = filter(lambda x: x in string.printable, line)
            line = re.split(r"\t+", line.strip("\n"))
            cat = line[1]
            header = re.sub(r'[\W_]+', '', line[0])
            if cat in headerClassification:
                if header not in headerClassification.values():
                    headerClassification[cat].append(header)
                else:
                    break
            else:
                headerClassification.update({header: cat})

    # Absolute path of the directory where the program resides
    dir = os.path.dirname(__file__)
    input = open(os.path.join(dir, "output/output.txt"), "r")
    htmlParse = input.read().decode("utf-8")

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
                soup = BeautifulSoup(str(line.findChildren(["th", "td"])))
                # Properly formats and encodes table headers
                tempData = (re.sub(' +', ' ', soup.text.strip("\t\n\r").replace("\n", "").strip())).upper().encode("utf-8")

                # Gathers table headers for classification and construction of categorical assignment string
                tableStructure.append(generateStructure(str(tableIDs[c]), generateList(str(tempData)), headerClassification))

    # Converts to final header-structure dictionary
    dict = convertToStructureDict(tableStructure)
    
    # Write the final dictionary to the file 'table_structures.txt'
    file = open(os.path.join(dir, "output/table_structures.txt"), "w")
    file.write(str(dict))
    file.close
    
    ###########################################################
    # Printing options for testing/review.                    #
    ###########################################################
    
    # Print number of unique table structures
    '''print "There are " + str(len(dict.keys())) + " unique table structures. \n"'''

    # Prints the number of tables within each unique table structure
    for key in dict:
        if key in dict.keys():
            splits = dict[key].split(' ')
            print 'Table Header Structure: '
            print key
            print str(len(splits)) + ' tables.'
            print '\n'
            # Prints each table name
            # for s in splits:
                # print s

    # Prints each table's structure (listForm) including all errors
    '''listForm = createList(tableStructure)
    for indvList in listForm:
        s = ''
        for item in indvList:
            s += item + ' '
        print s '''

    # Prints each table that does not contain a 'HEADER NOT FOUND' error
    '''for s in tableStructure:
        # if "ERR:HEADER NOT FOUND" not in s:
            print s'''

###############################################################
# Main code                                                   #
###############################################################

classify()
