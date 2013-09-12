from bs4 import BeautifulSoup

soup = BeautifulSoup(open("TABLE-1f7e1308-e6f5-4380-8d85-e2a22bdec9db-drugInteractions-0.txt"))

#print soup.prettify()
tablecols = len(soup.find('td'))
print(tablecols)

#tables1=soup.findChildren('tr')
#findChildrem method looks more effective
#print(tables1)

tables1=soup.find_all('tr')
print(tables1)
#****
table = soup.find('table')
 
rows = table.findAll('tr')
labels=table.findAll('content')
print(labels)

for tr in rows:
  cols = tr.findAll('td')
  for td in cols:
      text = ''.join(td.find(text=True))
      drugList= text.split(", ")

      drugList= '\n'.join(drugList)

      print("\n" + drugList)
      
      #print text+"\n ***line break**",



              

      #HOW TO MATCH????
