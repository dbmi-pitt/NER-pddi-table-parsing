
TableHeadingAnnotations - a folder with annotations on table headings
extracted from drug interaction sections of SPLs

The rest of the stuff here is for extract SPL tables from text/HTML
pulled from LinkedSPLs.

------------

To get tables from SPLs you first have to assemble a list of all setIds:

1) Log onto a server with the entire updated LinkedSPLs RDF graph

2) From the base of this repository, run the following from the command line:

$ isql-vt -H localhost -S 1111  -U <user name> -P <password> errors=stdout < ./scripts/querySPLSetIds.sparql > /tmp/test.out

3) Copy the results to scripts/setIDS.txt and remove any quotes

4) remove all text files from scripts/outfiles/
   If there is no folder outfiles, then create one for holding outputs

5) In the scripts folder, run retrieveSPLSquery.py if you want tables
from ALL SPLs, or retrieveSPLsForDDIQuery.py if you want tables only
from the DDI sections. 

6) copy the tables (files in scripts/outfiles/ with the "TABLE-"
prefix) to a new folder in the data/ subfolder named with the drug
name

7) Edit the TABLE_DATA_PATH in scripts/tables2html.py to point to the folder with table data and run the script

8) You should be able to view all tables by opening in your browser tables.html (written to TABLE_DATA_PATH)  

9) If you are planning to load data into TableAnnotator, you might
want the setIds of all SPLs with tables. You can get that from the
file listing of the folder that contains SPL tables using the
following command (just redirect to a file)


$ ls -1 data/spl-drug-interaction-section-tables-January-2017/*txt | sed 's/.*TABLE-//g' | sed 's/-drugInteractions.*//g' | sort | uniq

