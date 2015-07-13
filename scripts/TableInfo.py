import sys
from bs4 import BeautifulSoup

def init():
    rowNo = 0
    tdList = []

    fileName = "/Users/Josh/Documents/NER-pddi-table-parsing/data/all-DDI-section-tables-11142013/TABLE-ffa121b8-388f-4d7b-af48-d4aa8d9b5961-drugInteractions-0.txt"
    file = open(fileName, "rb")
    html = file.read()

    soup = BeautifulSoup(html)
    tables = soup.findChildren("table")

    firstTable = tables[0]
    row = firstTable.findChildren(["tr"])
    cell = firstTable.findChildren(["td", "th"])

    for line in row:
        lol = line.findChildren(["td"])
        print lol
        print "\n\n\n\n\n"

    print len(cell)

    for element in row:
        rowNo += 1

    print rowNo

init()