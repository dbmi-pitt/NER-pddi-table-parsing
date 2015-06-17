------------

trivial edit

To get tables from a new drug:

1) With your browser, go to: http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/snorql/

2) clear out the query and copy in the following with <DRUG> replaced
by the drug you are interested in:

SELECT DISTINCT ?setid WHERE {
  ?s dailymed:activeMoiety "<DRUG>".
  ?s dailymed:setId ?setid.
}


3) Copy the results to scripts/setIDS.txt and remove any quotes

4) remove all text files from scripts/outfiles/

5) In the scripts folder, run retrieveSPLSquery.py

6) copy the tables (files in scripts/outfiles/ with the "TABLE-"
prefix) to a new folder in the data/ subfolder named with the drug
name
