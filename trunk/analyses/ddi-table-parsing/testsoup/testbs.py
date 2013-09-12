from bs4 import BeautifulSoup

soup = BeautifulSoup(open("TABLE-1f7e1308-e6f5-4380-8d85-e2a22bdec9db-drugInteractions-0.txt"))

#print soup.prettify()
tablecols = len(soup.find('td'))
print(tablecols)

table = soup.find('table')
 
rows = table.findAll('tr')
for tr in rows:
  cols = tr.findAll('td')
  for td in cols:
      text = ''.join(td.find(text=True))
      drugList= text.split(", ")

      drugList= '\n'.join(drugList)

      print("\n" + drugList)
      #print text+"\n ***line break**",



              

      #HOW TO MATCH????
