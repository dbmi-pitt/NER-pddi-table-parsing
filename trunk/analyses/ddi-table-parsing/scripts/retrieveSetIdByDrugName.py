## retrieveSetIdByDrugName.py

## Retrieve set id by drug name or medicine name on graph core linkedSPLs
# Author: Yifan Ning

## hard coded drug list and mappings of drug name and dailyemed label
## prior to query setId by drug name, by dailymed label first
## return setid of latest product label 

import re, string
import codecs
from SPARQLWrapper import SPARQLWrapper, JSON
import pickle
import sys, os
import fileinput
import glob

drugL = ["Isocarboxazid", "Phenelzine" ,"Tranylcypromine" ,"Selegiline" ,"Citalopram" ,"Escitalopram" ,"Fluoxetine" ,"Fluvoxamine" ,"Paroxetine" ,"Sertraline" ,"Vilazodone (5HT1a receptor antagonist)" ,"Desvenlafaxine" ,"Duloxetine" ,"Levomilnacipran" ,"Minacipran" ,"Venlafaxine" ,"Tetracyclic" ,"Maprotiline" ,"Mirtazapine" ,"Amitriptyline" ,"Amoxapine" ,"Clomipramine" ,"Desipramine" ,"Doxepin" ,"Imipramine" ,"Nortriptyline" ,"Protriptyline" ,"Trimipramine" ,"Bupropion" ,"Nefazodone" ,"Vortioxetine" ,"Iloperidone" ,"Paliparidone" ,"Risperidon" ,"Ziprasidone" ,"Lurasidone" ,"Asenapine" ,"Clozapine" ,"Loxapine" ,"Olanzapine" ,"Quetiapine" ,"Chlorpromazine" ,"Fluphenazine" ,"Perphenazine" ,"Prochlorperazine" ,"Thioridazine" ,"Trifluoperazine" ,"Haloperidol" ,"Aripiprazole" ,"Thiothixene" ,"Eszopiclone" ,"Zaleplon" ,"Zolpidem" ,"Estazolam" ,"Flurazepam" ,"Quazepam" ,"Temazepam" ,"Triazolam" ,"Atorvastatin" ,"Fluvastatin" ,"Lovastatin" ,"Pitavastatin" ,"Pravastatin" ,"Rosuvastatin" ,"Simvastatin" ,"warfarin" ,"dabigatran" ,"apixaban" ,"rivaroxaban"]

dailymedLabelD = {"Isocarboxazid":"Marplan", "Phenelzine":"Nardil", "Tranylcypromine":"Parnate", "Selegiline":"EMSAM", "Citalopram":"Celexa", "Escitalopram":"Lexapro", "Fluoxetine":"Prozac", "Maprotiline":"Mylan", "Clomipramine":"Sandoz", "Fluvastatin":"Teva", "Olanzapine":"Zyprexa", "Clozapine":"Clozaril", "Aripiprazole":"Abilify", "Eszopiclone":"Lunesta", "Zaleplon":"Pfizer", "Zolpidem":"Ambien", "Triazolam":"Halcion", "Atorvastatin":"Lipitor", "Lovastatin":"Mevacor", "Pitavastatin":"Livalo", "Rosuvastatin":"Crestor", "Simvastatin":"Zocor", "dabigatran":"Pradaxa", "Mirtazapine":"Remeron", "Desipramine":"Norpramin", "Imipramine":"Tofranil", "Nortriptyline":"Pamelor", "Trimipramine":"Surmontil", "Bupropion":"Wellbutrin"}



def getRecentlySetIdByDrug(drugName):

    sparql = SPARQLWrapper("http://dbmi-icode-01.dbmi.pitt.edu/sparql")

    qry = '''

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX linkedspls_vocabulary: <http://bio2rdf.org/linkedspls_vocabulary:>
PREFIX loinc: <http://www.hipaaspace.com/Medical_Billing/Coding/Logical.Observation.Identifiers.Names.and.Codes/>

SELECT ?spl ?setId ?medicine ?effectiveTime ?versionNumber ?drugInteractions ?adverseReactions
FROM <http://purl.org/net/nlprepository/spl-core>
WHERE {

?spl linkedspls_vocabulary:fullName ?fullName;
     linkedspls_vocabulary:genericMedicine ?medicine.
     FILTER (regex(str(?fullName),"%s","i") || regex(str(?medicine),"%s","i"))
     
?spl linkedspls_vocabulary:setId ?setId;
     linkedspls_vocabulary:effectiveTime ?effectiveTime;
     linkedspls_vocabulary:versionNumber ?versionNumber.

OPTIONAL { ?spl loinc:34073-7 ?drugInteractions }
OPTIONAL { ?spl loinc:34084-4 ?adverseReactions}

}
ORDER BY DESC(?effectiveTime)
LIMIT 10  ''' % (drugName, drugName)
    sparql.setQuery(qry)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if len(results["results"]["bindings"]) == 0:
        #print "ERROR: no results from query"
        return {}
    else:
        return results["results"]["bindings"][0]['setId']['value']

################ MAIN ################

for drug in drugL:
    if dailymedLabelD.has_key(drug):
        dailymedL = dailymedLabelD[drug]
        setId = getRecentlySetIdByDrug(dailymedL)
        if setId:
            print "find setId by dailymedL: %s for drug: %s, setId: %s" % (dailymedL, drug, setId)
        else:
            print "setId not found for drugName-dailymedLabel: %s-%s" % (drug, dailymedL)
    else:
        setId = getRecentlySetIdByDrug(drug)
        if setId:
            print "find setId by drugName: %s, setId: %s" % (drug, setId)
        else:
            print "setId not found for drug: %s" % (drug)


