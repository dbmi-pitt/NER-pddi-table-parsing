from bs4 import BeautifulSoup

class tableRead:
    def method1(self)
        table = soup.find('table')
 
        rows = table.findAll('tr')
        for tr in rows:
          cols = tr.findAll('td')
          text1=tr.renderContents().strip('\n')
          #print(text1)

          for td in cols:
              text = ''.join(td.find(text=True))
              drugList= text.split(", ")

              drugList= '\n'.join(drugList)

              print("\n" + drugList)
              #print text+"\n ***line break**",



              
             #HOW TO MATCH????
      

