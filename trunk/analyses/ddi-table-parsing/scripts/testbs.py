# testbs.py
#
# A simple test program to list out all drugs presented in tables
# within SPLs
#
# Authors: Stephanie Dofitas and Richard Boyce
# 09/12/2013
#
from bs4 import BeautifulSoup

f = open("../data/warfarin/TABLE-1f7e1308-e6f5-4380-8d85-e2a22bdec9db-drugInteractions-0.txt", "r")
soup = BeautifulSoup(f)
f.close()

# Find all rows and then look for rows that have a comma-delimitted
# list. Print out the items in those lists.
table = soup.find('table')
rows = table.findAll('tr')
headers=table.findAll('content')

for tr in rows:
  cells = tr.findAll('td')
  i = -1 # to track header 
  for td in cells:
    i += 1
    print headers[i]
    text = ''.join(td.find(text=True))
    drugList = text.split(", ")
    drugList = '\n'.join(drugList)

    print("\n" + drugList)
