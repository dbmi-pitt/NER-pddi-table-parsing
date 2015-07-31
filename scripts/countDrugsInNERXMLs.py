import xmltodict
from os import walk
import codecs

inputNERDir = 'NEROutputInXMLs/1059withTableIdx/'
filesPddi = []

for (dirpath, dirnames, filenames) in walk(inputNERDir):
    for fname in filenames:
        if fname.endswith("-PROCESSED.xml"):
            filesPddi.append(fname)
    break


for ner in filesPddi:
    with codecs.open(inputNERDir + ner, 'r', 'utf-8') as nerInputFile:

         contents = nerInputFile.read()
         numOfDrugs = contents.count('/name')
         print ner + "\t" + str(numOfDrugs)
