## retrieveSPLSquery.py
#
# Retreive SPL text content from a list of setids written in a config
# file. Remove HTML tables so that they can be processed
# separately. Split files over a certain size (in terms of number of
# sentences) into smaller files to aid processing.

# Author: Richard D Boyce, Peter Randall, Yifan Ning
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
    drugName = None
    medicine = None
    adverseReactions = None
    boxedWarning = None
    clinicalPharmacology = None
    clinicalStudies = None
    contraindications = None
    description = None
    dosageAndAdministration = None 
    drugInteractions = None
    indicationsAndUsage = None
    patientInformation = None
    patientCounseling = None
    precautions = None
    specialPopulations = None 
    warningsAndPrecautions = None
    warnings = None
    setID = None

    def __init__(self, drugName = None, medicine = None, adverseReactions = None, boxedWarning = None, clinicalPharmacology = None, clinicalStudies = None, contraindications = None, description = None, dosageAndAdministration = None, drugInteractions = None, indicationsAndUsage = None, patientInformation = None, patientCounseling = None, precautions = None, specialPopulations = None, warningsAndPrecautions = None, warnings = None, setID = None):
        self.drugName = drugName
        self.medicine = medicine
        self.adverseReactions = adverseReactions
        self.boxedWarning = boxedWarning
        self.clinicalPharmacology = clinicalPharmacology
        self.clinicalStudies = clinicalStudies
        self.contraindications = contraindications
        self.description = description
        self.dosageAndAdministration = dosageAndAdministration
        self.drugInteractions = drugInteractions
        self.indicationsAndUsage = indicationsAndUsage
        self.patientInformation = patientInformation
        self.patientCounseling = patientCounseling
        self.precautions = precautions
        self.specialPopulations = specialPopulations
        self.warningsAndPrecautions = warningsAndPrecautions
        self.warnings = warnings
        self.setID = setID

    def __str__(self):
        return 'setID: ' + self.setID + '\ndrugName: ' + self.drugName + '\nmedicine: ' + self.medicine + '\nadverseReactions: ' + self.adverseReactions + '\nboxedWarning: ' + self.boxedWarning + '\nclinicalPharmacology: ' + self.clinicalPharmacology + '\nclinicalStudies: ' + self.clinicalStudies + '\ncontraindications: ' + self.contraindications + '\ndescription: ' + self.description + '\ndosageAndAdministration: ' + self.dosageAndAdministration + '\ndrugInteractions: ' + self.drugInteractions + '\nindicationAndUsage: ' + self.indicationsAndUsage + '\npatientInformation: ' +  self.patientInformation + '\npatientCounseling: ' + self.patientCounseling + '\nprecautions: ' + self.precautions + '\nspecialPopulations: ' + self.specialPopulations + '\nwarningsAndPrecautions: ' + self.warningsAndPrecautions + '\nwarnings: ' + self.warnings + '\n'


    def toDict(self):
        result = { "drugName": self.drugName, "medicine": self.medicine, "adverseReactions": self.adverseReactions, "boxedWarning": self.boxedWarning, "clinicalPharmacology": self.clinicalPharmacology, "clinicalStudies": self.clinicalStudies,"contraindications": self.contraindications, "description": self.description, "dosageAndAdministration": self.dosageAndAdministration,"drugInteractions": self.drugInteractions, "indicationsAndUsage":self.indicationsAndUsage, "patientInformation":self.patientInformation, "patientCounseling":self.patientCounseling, "precautions":self.precautions, "specialPopulations":self.specialPopulations, "warningsAndPrecautions":self.warningsAndPrecautions, "warnings":self.warnings }
        return result



def getAllSPLSectionsSparql(spl, sparql):
    sID = spl
    #print sID

## sample uri: http://bio2rdf.org/linkedspls:513a41d0-37d4-4355-8a6d-a2c643bce6fa
## Nardil

    splUri = "http://bio2rdf.org/linkedspls:" + spl
    qry = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX linkedspls_vocabulary: <http://bio2rdf.org/linkedspls_vocabulary:>
PREFIX loinc: <http://www.hipaaspace.com/Medical_Billing/Coding/Logical.Observation.Identifiers.Names.and.Codes/>

SELECT ?drugName ?medicine ?drugInteractions ?adverseReactions ?boxedWarning ?clinicalPharmacology ?clinicalStudies ?contraindications ?description ?dosageAndAdministration ?indicationAndUsage ?patientInformation ?patientCounseling  ?precautions ?specialPopulations ?warningsAndPrecautions ?warnings

FROM <http://purl.org/net/nlprepository/spl-core>
WHERE {

<%s> linkedspls_vocabulary:fullName ?drugName;
     linkedspls_vocabulary:genericMedicine ?medicine.

OPTIONAL { <%s> loinc:34073-7 ?drugInteractions }
OPTIONAL { <%s> loinc:34084-4 ?adverseReactions }
OPTIONAL { <%s> loinc:34066-1 ?boxedWarning }
OPTIONAL { <%s> loinc:34090-1 ?clinicalPharmacology }
OPTIONAL { <%s> loinc:34092-7 ?clinicalStudies }
OPTIONAL { <%s> loinc:34070-3 ?contraindications }
OPTIONAL { <%s> loinc:34089-3 ?description }
OPTIONAL { <%s> loinc:34068-7 ?dosageAndAdministration }
OPTIONAL { <%s> loinc:34067-9 ?indicationAndUsage }
OPTIONAL { <%s> loinc:68498-5 ?patientInformation }
OPTIONAL { <%s> loinc:34076-0 ?patientCounseling  }
OPTIONAL { <%s> loinc:34072-9 ?precautions }
OPTIONAL { <%s> loinc:43684-0 ?specialPopulations }
OPTIONAL { <%s> loinc:43685-7 ?warningsAndPrecautions }
OPTIONAL { <%s> loinc:34071-1 ?warnings}
}

''' % (splUri, splUri, splUri, splUri, splUri, splUri, splUri, splUri, splUri, splUri,splUri, splUri, splUri, splUri, splUri, splUri)

    
    #print "QUERY: %s" % qry
    sparql.setQuery(qry)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results["results"]["bindings"]) == 0:
        print "ERROR: no results from query"
        return {}

    secD = {}

    sp = SPL()
    sp.setID = spl
    for res in results["results"]["bindings"]:
            
        #if res.has_key("drugName"):
        #    sp.drugName = unicode(res['drugName']["value"])
        #if res.has_key("medicine"):
        #    sp.medicine = unicode(res['medicine']["value"])
        
        # if res.has_key("boxedWarning"):
        #     sp.boxedWarning = unicode(res['boxedWarning']["value"])
        if res.has_key("clinicalPharmacology"):
            sp.clinicalPharmacology = unicode(res['clinicalPharmacology']["value"])                                    
        # if res.has_key("warnings"):
        #     sp.warnings = unicode(res['warnings']["value"])
        # if res.has_key("warningsAndPrecautions"):
        #     sp.warningsAndPrecautions = unicode(res['warningsAndPrecautions']["value"])
        # if res.has_key("precautions"):
        #     sp.precautions = unicode(res['precautions']["value"])
        # if res.has_key("contraindications"):
        #     sp.contraindications = unicode(res['contraindications']["value"])
        if res.has_key("drugInteractions"):
            sp.drugInteractions = unicode(res['drugInteractions']["value"])
            
        #if res.has_key("indicationAndUsage"):
        #    sp.indicationAndUsage = unicode(res['indicationAndUsage']["value"])
        #if res.has_key("adverseReactions"):
        #    sp.adverseReactions = unicode(res['adverseReactions']["value"])    
        #if res.has_key("clinicalStudies"):
        #    sp.clinicalStudies = unicode(res['clinicalStudies']["value"])
        #if res.has_key("specialPopulations"):
        #    sp.specialPopulations = unicode(res['specialPopulations']["value"])
        #if res.has_key("patientCounseling"):
        #    sp.patientCounseling = unicode(res['patientCounseling']["value"])
        #if res.has_key("patientInformation"):
        #    sp.patientInformation = unicode(res['patientInformation']["value"])
        #if res.has_key("dosageAndAdministration"):
        #    sp.dosageAndAdministration = unicode(res['dosageAndAdministration']["value"])
        #if res.has_key("description"):
        #    sp.description = unicode(res['description']["value"])
                        
    return sp





if __name__ == "__main__":
    ## the D2R server can be slower but is generally more
    ## up-to-date than the virtuoso server (next line)
    #sparql = SPARQLWrapper("http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/sparql")

    ## a higher performance but more static endpoint
    sparql = SPARQLWrapper("http://dbmi-icode-01.dbmi.pitt.edu/sparql")

    lspls = []
    for line in fileinput.input('setIDs-full.txt'):
        if not line or line == "":
            break

        #lspls.append(getDDISPLSectionsSparql(line.strip(), sparql))	
        lspls.append(getAllSPLSectionsSparql(line.strip(), sparql))	

    for sp in lspls:
        dic = sp.toDict()
        for key in dic:
            if (dic[key] is None):
                continue

            #print "[DEBUG] process " + sp.setID.strip() + " - " + key

            # extract HTML tables and split text into sub-files as necessary
            sectTxt = dic[key]

            if sectTxt == "None":
                print "WARNING: no section '%s' for setid %s, this SPL section will not be processed" % (key,sp.setID.strip())
                continue

            #print "[DEBUG] original Text: " + sectTxt 

            soup = BeautifulSoup(sectTxt, "html.parser")
            tables = soup.find_all('table')
            i = -1
            for tbl in tables:

                #print "[DEBUG] find table: " + str(tbl)
                
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






