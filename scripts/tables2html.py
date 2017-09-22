import glob
import codecs

TABLE_DATA_PATH = "/home/rdb20/NER-pddi-table-parsing/data/spl-drug-interaction-section-tables-January-2017/"


#####


files = glob.glob(TABLE_DATA_PATH + "*.txt")

header = u"<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><style>table, th, td{border: 1px solid black;}</style><body>"
body = u""
footer = u"</body></html>"

for f in files:
    with codecs.open(f,"rb","utf-8") as table:    
        table_name = f
        body += u"Table name: <input type='set_id' size=80' onClick='this.select();' readonly='readonly' value='%s'/>" %f
        body += table.read()
        body += u"<hr><br>"
        
        

with codecs.open(TABLE_DATA_PATH + "tables.html","wb",'utf-8') as html:
    html.write(header+body+footer)
