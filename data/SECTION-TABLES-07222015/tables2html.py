import glob

files = glob.glob("*.txt")

header = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><style>table, th, td{border: 1px solid black;}</style><body>"
body = ""
footer = "</body></html>"

for f in files:
    with open(f,"rb") as table:    
        table_name = f
        body += "Table name: <input type='set_id' size=80' onClick='this.select();' readonly='readonly' value='%s'/>" %f
        body += table.read()
        body += "<hr><br>"
        
        

with open("tables.html","wb") as html:
    html.write(header+body+footer)