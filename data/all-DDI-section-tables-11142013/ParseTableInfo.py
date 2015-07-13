import sys
from bs4 import BeautifulSoup

def init():
    row = 0.0
    col = 0.0
    headers = []

    print("Enter file name")

    fileName = "/Users/Josh/Documents/NER-pddi-table-parsing/data/all-DDI-section-tables-11142013/" + raw_input()
    file = open(fileName, "rb")
    html = file.read()

    soup = BeautifulSoup(html)
    table = soup.find("table")
    tables = soup.findChildren("table")
    firstTable = tables[0]
    rows = firstTable.findChildren(["th", "tr"])
    cells = firstTable.findChildren(["td"])

    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        headers.append(dataset)

    print dataset

    for rowNo in rows:
        row += 1

    for colNo in cells:
        col += 1

    print "Rows: " + str(int(row))
    print "Columns: " + str(int(round(col/row)))

init()