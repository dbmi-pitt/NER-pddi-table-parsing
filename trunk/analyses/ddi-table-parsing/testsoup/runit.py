from bs4 import BeautifulSoup

#RUN PROGRAM

#open table
soup = BeautifulSoup(open("TABLENAME.TXT")) #Maybe do enter path?

tablecols = len(soup.find('td'))

if tablecols==3
    #use classProcess.method1

if tablecols==2
    #use classProcess.method2
