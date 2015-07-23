# Goals for this .py file
#   1. List number of rows and columns for each table
#   2. Append all headings of each table into a list without duplication
#   3. Find the total number of tables [DONE]
#   4. Find the distribution of rows and columns between tables
#   5. Find how many times each heading is stated in HTML document
#   6. Find how many headers each group contains

import re
import os
from bs4 import BeautifulSoup
from collections import defaultdict

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def generate():
    dir = os.path.dirname(__file__)

    # [WORKING] Section fixes broken HTML before processing
    fileName = os.path.join(dir, "tables.html")
    file = open(fileName, "rb")
    html = file.read()

    ## TODO: fix the script that pulls tables from Linked SPLs so that
    ## encoding and "prettify" are done at the time of extraction.
    soupTemp = BeautifulSoup(html)

    output = open(os.path.join(dir, "output.txt"), "w")
    output.write(soupTemp.prettify().encode("utf-8"))
    output.close()

def organize():
    categories = {"SetID": [],
                  "Interacting Substance": [],
                  "Interacting Substance Properties": [],
                  "Interaction Properties": [],
                  "Drug Name or Drug Class": [],
                  "Drug Effect": [],
                  "Drug Dose Recommendation": [],
                  "Effect on Drug": [],
                  "Clinical Comment": [],
                  "Sample Size": [],
                  "Misc.": []}
    tableInfo = defaultdict(list)
    perTableCol = []
    perTableColLong = []
    headers = []
    headersRowsCols = []
    headersText = []
    tableStatsCols = []
    tableStatsRows = []
    tablePosInfo = []
    tempData = ""
    colNo = 0
    colsTot = 0
    colsTotTemp = 0
    rowsTot = 0
    newNum = 0
    dir = os.path.dirname(__file__)

    input = open(os.path.join(dir, "output.txt"), "r")
    htmlParse = input.read().decode("utf-8")

    # Section prepares each part for addition to tableInfo dictionary
    soup = BeautifulSoup(htmlParse)
    tables = soup.findChildren("table") # (ResultSet)

    tableIDs = [(n["value"]) for n in soup.findChildren("input")] # Creates a list of table names (List)

    for c in range(0, len(tableIDs) - 1): # Goes through all tables
        tableNo = tables[c].findChildren(["tr"]) # Finds all rows in a table (ResultSet)

        for line in tableNo:
            allTable = line.findChildren(["th", "td"])
            dataCellsCols = len(allTable) # The amount of cells per row (columns)
            colsTotTemp += dataCellsCols

            if (line.findChildren(["th", tableNo.index(line) == 0 and line.findChildren(["th"])])) or (tableNo.index(line) == 0 and line.findChildren(["td"])):
                headers.append(line.findChildren(["th", "td"]))

                tablePosInfo += chunks(list(len(line.findChildren(["th", "td"])) * (("Table: " + str(tableIDs[c])), "Row: " + str(1), "Column: " + str(colNo))), 3)
                perTableCol.append([len(line.findChildren(["th", "td"]))])

        colsTot += colsTotTemp/len(tableNo)
        colsTotTemp = 0

        dataCellsRows = len(tableNo)
        rowsTot += dataCellsRows

        tableStatsCols.append(dataCellsCols)
        tableStatsRows.append(len(tableNo))

    for n in range (0, len(headers)):
        for i in range (0, len(headers[n])):
            dataHTML = str(headers[n][i])
            soup = BeautifulSoup(dataHTML)
            tempData = (re.sub(' +',' ', soup.text.strip("\t\n\r").replace("\n", "").strip())).upper().encode("utf-8")

            headersText.append(tempData)

    for t in range (0, len(perTableCol)):
        for n in range (0, perTableCol[t][0]):
            newNum = perTableCol[t][0]
            if newNum > 0:
                newNum -= 1
                perTableCol[t].insert(0, newNum)
            elif newNum == 0:
                None

    for t in range (0, len(perTableCol)):
        for i in range (0, len(perTableCol[t])):
            if perTableCol[t][i] > 0:
                perTableColLong.append(perTableCol[t][i])

    for t in range (0, len(perTableColLong)):
        tablePosInfo[t][2] = "Column: " + str(perTableColLong[t])
        tablePosInfo[t] = tuple(tablePosInfo[t])

    for delvt, pin in zip(headersText, tablePosInfo):
        tableInfo[delvt].append(pin)

    headersFile = open(os.path.join(dir, "headers.txt"), "w")
    headersFile.write(str(tableInfo))

    print "List of parsed headers: " + str(len(headersText))
    print "Dictionary: " + str(len(tableInfo))
    print "List of tuples: " + str(len(tablePosInfo))
    print "List of unparsed headers: " + str(len(headers))

    print "Total Columns: " + str(colsTot)
    print "Minimum Columns: " + str(min(tableStatsCols))
    print "Maximum Columns: " + str(max(tableStatsCols))
    print "Average Columns: " + str(sum(tableStatsCols)/len(tableStatsCols)) + "\n\n"

    print "Total Rows: " + str(rowsTot)
    print "Minimum Rows: " + str(min(tableStatsRows))
    print "Maximum Rows: " + str(max(tableStatsRows))
    print "Average Rows: " + str(sum(tableStatsRows)/len(tableStatsRows)) + "\n\n"

def dbToDict():
    connect = {}
    dir = os.path.dirname(__file__)

    # [WORKING] Section takes txt database and categorizes everything into a dictionary
    db = os.path.join(dir, "Categories.txt") ## get the Categories.txt into the code repository and adjust like above to not care about local configuration (relative path)
    data = open(db, "rb")

    with data as txtData:
        for line in txtData:
            line = re.split(r"\t+", line.strip("\n"))

            if line[1] in connect:
                if line[0] not in connect.values():
                    connect[line[1]].append(line[0])

                else:
                    break

            else:
                connect.update({line[1]: [line[0]]})

    print connect

organize()