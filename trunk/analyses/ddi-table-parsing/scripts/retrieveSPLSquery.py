## retrieveSPLSquery.py
#
# Retreive SPL text content from a list of setids written in a config
# file. Remove HTML tables so that they can be processed
# separately. Split files over a certain size (in terms of number of
# sentences) into smaller files to aid processing.

# Author: Richard D Boyce and Peter Randall
#
# 
## This library is free software; you can redistribute it and/or
## modify it under the terms of the GNU Library General Public
## License as published by the Free Software Foundation; either
## version 2 of the License, or (at your option) any later version.

## This library is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## Library General Public License for more details.

## You should have received a copy of the GNU Library General Public
## License along with this library; if not, write to the
## Free Software Foundation, Inc., 59 Temple Place - Suite 330,
## Boston, MA 02111-1307, USA.


import re, string
import codecs
from SPARQLWrapper import SPARQLWrapper, JSON
import pickle
import sys, os
import fileinput
import glob

from bs4 import BeautifulSoup

class SPL:
	fullName = None
	genericMedicine = None
	adverseReactions = None
	boxedWarning = None
	clinicalPharmacology = None
	clinicalStudies = None
	contraindications = None
	description = None
	dosageAndAdministration = None 
	drugInteractions = None
	indicationsAndUsage = None
	patientMedicationInformation = None
	informationForPatients = None
	precautions = None
	useInSpecificPopulations = None 
	warningsAndPrecautions = None
	warnings = None
	setID = None

	def __init__(self, fullName = None, genericMedicine = None, adverseReactions = None, boxedWarning = None, clinicalPharmacology = None, clinicalStudies = None, contraindications = None, description = None, dosageAndAdministration = None, drugInteractions = None, indicationsAndUsage = None, patientMedicationInformation = None, informationForPatients = None, precautions = None, useInSpecificPopulations = None, warningsAndPrecautions = None, warnings = None, setID = None):
		self.fullName = fullName
		self.genericMedicine = genericMedicine
		self.adverseReactions = adverseReactions
		self.boxedWarning = boxedWarning
		self.clinicalPharmacology = clinicalPharmacology
		self.clinicalStudies = clinicalStudies
		self.contraindications = contraindications
		self.description = description
		self.dosageAndAdministration = dosageAndAdministration
		self.drugInteractions = drugInteractions
		self.indicationsAndUsage = indicationsAndUsage
		self.patientMedicationInformation = patientMedicationInformation
		self.informationForPatients = informationForPatients
		self.precautions = precautions
		self.useInSpecificPopulations = useInSpecificPopulations
		self.warningsAndPrecautions = warningsAndPrecautions
		self.warnings = warnings
		self.setID = setID

	def __str__(self):
		return 'setID: ' + self.setID + '\nfullName: ' + self.fullName + '\ngenericMedicine: ' + self.genericMedicine + '\nadverseReactions: ' + self.adverseReactions + '\nboxedWarning: ' + self.boxedWarning + '\nclinicalPharmacology: ' + self.clinicalPharmacology + '\nclinicalStudies: ' + self.clinicalStudies + '\ncontraindications: ' + self.contraindications + '\ndescription: ' + self.description + '\ndosageAndAdministration: ' + self.dosageAndAdministration + '\ndrugInteractions: ' + self.drugInteractions + '\nindicationAndUsage: ' + self.indicationsAndUsage + '\npatientMedicationInformation: ' +  self.patientMedicationInformation + '\ninformationForPatients: ' + self.informationForPatients + '\nprecautions: ' + self.precautions + '\nuseInSpecificPopulations: ' + self.useInSpecificPopulations + '\nwarningsAndPrecautions: ' + self.warningsAndPrecautions + '\nwarnings: ' + self.warnings + '\n'

	
	def toDict(self):
		result = { "fullName": self.fullName, "genericMedicine": self.genericMedicine, "adverseReactions": self.adverseReactions, "boxedWarning": self.boxedWarning, "clinicalPharmacology": self.clinicalPharmacology, "clinicalStudies": self.clinicalStudies,"contraindications": self.contraindications, "description": self.description, "dosageAndAdministration": self.dosageAndAdministration,"drugInteractions": self.drugInteractions, "indicationsAndUsage":self.indicationsAndUsage, "patientMedicationInformation":self.patientMedicationInformation, "informationForPatients":self.informationForPatients, "precautions":self.precautions, "useInSpecificPopulations":self.useInSpecificPopulations, "warningsAndPrecautions":self.warningsAndPrecautions, "warnings":self.warnings }
		return result
	
	
def getAllSPLSectionsSparql(spl, sparql):
	sID = spl
	#print sID
	splUri = "http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/resource/structuredProductLabelMetadata/" + spl
	qry = '''
PREFIX dailymed: <http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/>

SELECT 
?fullName ?genericMedicine ?adverseReactions ?boxedWarning ?clinicalPharmacology ?clinicalStudies ?contraindications ?description ?dosageAndAdministration ?drugInteractions ?indicationsAndUsage ?patientMedicationInformation ?informationForPatients ?precautions ?useInSpecificPopulations ?warningsAndPrecautions ?warnings

WHERE { 
    OPTIONAL { <%s> dailymed:fullName   ?fullName}
    OPTIONAL { <%s> dailymed:genericName   ?genericMedicine}
    OPTIONAL { <%s> dailymed:adverseReactions   ?adverseReactions }
    OPTIONAL { <%s> dailymed:boxedWarning   ?boxedWarning }
    OPTIONAL { <%s> dailymed:clinicalPharmacology   ?clinicalPharmacology }
    OPTIONAL { <%s> dailymed:clinicalStudies   ?clinicalStudies }
    OPTIONAL { <%s> dailymed:contraindications   ?contraindications }
    OPTIONAL { <%s> dailymed:description   ?description }
    OPTIONAL { <%s> dailymed:dosageAndAdministration   ?dosageAndAdministration }
    OPTIONAL { <%s> dailymed:drugInteractions   ?drugInteractions }
    OPTIONAL { <%s> dailymed:indicationsAndUsage   ?indicationsAndUsage }
    OPTIONAL { <%s> dailymed:patientMedicationInformation   ?patientMedicationInformation }
    OPTIONAL { <%s> dailymed:informationForPatients   ?informationForPatients }
    OPTIONAL { <%s> dailymed:precautions   ?precautions }
    OPTIONAL { <%s> dailymed:useInSpecificPopulations   ?useInSpecificPopulations }
    OPTIONAL { <%s> dailymed:warningsAndPrecautions   ?warningsAndPrecautions }
    OPTIONAL { <%s> dailymed:warnings   ?warnings }
}
''' % (splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri,splUri)

	#print "QUERY: %s" % qry
	sparql.setQuery(qry)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()


	if len(results["results"]["bindings"]) == 0:
		print "ERROR: no results from query"
		return {}

	secD = {
        "fullName": 'None',
        "genericMedicine": 'None',
        "adverseReactions": 'None',
        "boxedWarning": 'None',
        "clinicalPharmacology": 'None',
        "clinicalStudies": 'None',
        "contraindications": 'None',
        "description": 'None',
        "dosageAndAdministration":'None',
        "drugInteractions":'None',
        "indicationsAndUsage":'None',
        "patientMedicationInformation":'None',
        "informationForPatients":'None',
        "precautions":'None',
        "useInSpecificPopulations":'None',
        "warningsAndPrecautions":'None',
        "warnings":'None'
        }

	for k in secD.keys():
		if results["results"]["bindings"][0].has_key(k):
			secD[k] = unicode(results["results"]["bindings"][0][k]["value"])
	sp = SPL(secD['fullName'].strip(), secD['genericMedicine'].strip(), secD['adverseReactions'].strip(), secD['boxedWarning'].strip(), secD['clinicalPharmacology'].strip(), secD['clinicalStudies'].strip(), secD['contraindications'].strip(),secD['description'].strip(), secD['dosageAndAdministration'].strip(), secD['drugInteractions'].strip(), secD['indicationsAndUsage'].strip(), secD['patientMedicationInformation'].strip(), secD['informationForPatients'].strip(), secD['precautions'].strip(), secD['useInSpecificPopulations'].strip(), secD['warningsAndPrecautions'].strip(), secD['warnings'].strip(), spl)
	return sp


def getDDISPLSectionsSparql(spl, sparql):
	sID = spl
	#print sID
	splUri = "http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/resource/structuredProductLabelMetadata/" + spl
	qry = '''
PREFIX dailymed: <http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/>

SELECT 
?drugInteractions

WHERE { 
    OPTIONAL { <%s> dailymed:drugInteractions   ?drugInteractions }
}
''' % (splUri)

	#print "QUERY: %s" % qry
	sparql.setQuery(qry)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()


	if len(results["results"]["bindings"]) == 0:
		print "ERROR: no results from query"
		return {}

	secD = {
        "drugInteractions":'None',
        }

	for k in secD.keys():
		if results["results"]["bindings"][0].has_key(k):
			secD[k] = unicode(results["results"]["bindings"][0][k]["value"])
	sp = SPL()
	sp.drugInteractions = secD['drugInteractions'].strip()
	sp.setID = spl

	return sp
		

if __name__ == "__main__":
	## the D2R server can be slower but is generally more
	## up-to-date than the virtuoso server (next line)
	#sparql = SPARQLWrapper("http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/sparql")

	## a higher performance but more static endpoint
	sparql = SPARQLWrapper("http://dbmi-icode-01.dbmi.pitt.edu:8080/sparql")

	lspls = []
	for line in fileinput.input('setIDs.txt'):
		if not line or line == "":
			break
		#print line.strip()

		## uncomment this line and comment the next to get all
		## sections
		#lspls.append(getAllSPLSectionsSparql(line.strip(), sparql))	

		## uncomment this line and comment the previous to get
		## only the DDI sections
		lspls.append(getDDISPLSectionsSparql(line.strip(), sparql))	

	for sp in lspls:
		dic = sp.toDict()
		for key in dic:
			if (dic[key] is None):
				continue
			
			# extract HTML tables and split text into sub-files as necessary
			sectTxt = dic[key]
			
			if sectTxt == "None":
				print "WARNING: no section '%s' for setid %s, this SPL section will not be processed" % (key,sp.setID.strip())
				continue

			soup = BeautifulSoup(sectTxt)
			tables = soup.findAll('table')
			i = -1
			for tbl in tables:
				i += 1
				tbl.replaceWith("")
				f = codecs.open("outfiles/TABLE-%s-%s-%d.txt" % (sp.setID.strip(), key, i) ,encoding = 'utf-8', mode ='w+') 
				f.write(unicode(tbl))
				f.close()

			# put whats left over into unicode files for further processing
			newStr = ""
			for st in soup.strings:
				newStr += st
			f = codecs.open("outfiles/%s-%s.txt" % (sp.setID.strip(), key) ,encoding = 'utf-8', mode ='w+') 
			f.write(unicode(newStr))
			f.close()
	

		
		
	

