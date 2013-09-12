# testmatch.py
#
# A simple test program to compare a tables from a list of files
# containing HTML tables for structure and categorize them into groups
#
# Authors: Stephanie Dofitas and Richard Boyce
# 09/12/2013
#
from bs4 import BeautifulSoup

fileL = ["TABLE-030dac01-d589-4c3e-94dc-a9088b6a1171-drugInteractions-0.txt","TABLE-030dac01-d589-4c3e-94dc-a9088b6a1171-drugInteractions-1.txt","TABLE-0392a32a-4546-4d58-834e-880b4db2d2f5-drugInteractions-0.txt","TABLE-0392a32a-4546-4d58-834e-880b4db2d2f5-drugInteractions-1.txt","TABLE-054dcdd1-4276-4137-b551-48edd8b7f218-drugInteractions-0.txt","TABLE-054dcdd1-4276-4137-b551-48edd8b7f218-drugInteractions-1.txt","TABLE-054dcdd1-4276-4137-b551-48edd8b7f218-drugInteractions-2.txt","TABLE-054dcdd1-4276-4137-b551-48edd8b7f218-drugInteractions-3.txt","TABLE-19a69a72-ac5d-45d5-a94d-a5aaecbe4730-drugInteractions-0.txt","TABLE-19a69a72-ac5d-45d5-a94d-a5aaecbe4730-drugInteractions-1.txt","TABLE-1f7e1308-e6f5-4380-8d85-e2a22bdec9db-drugInteractions-0.txt","TABLE-1f7e1308-e6f5-4380-8d85-e2a22bdec9db-drugInteractions-1.txt","TABLE-26e08f6a-4982-4c37-97de-3eb492148bd7-drugInteractions-0.txt","TABLE-26e08f6a-4982-4c37-97de-3eb492148bd7-drugInteractions-1.txt","TABLE-3018b992-64ca-41d0-aa43-6b97d4919ede-drugInteractions-0.txt","TABLE-3018b992-64ca-41d0-aa43-6b97d4919ede-drugInteractions-1.txt","TABLE-36a919ce-7a21-40c0-9af5-2299bf2b1f97-drugInteractions-0.txt","TABLE-36a919ce-7a21-40c0-9af5-2299bf2b1f97-drugInteractions-1.txt","TABLE-36a919ce-7a21-40c0-9af5-2299bf2b1f97-drugInteractions-2.txt","TABLE-36a919ce-7a21-40c0-9af5-2299bf2b1f97-drugInteractions-3.txt","TABLE-3ebcb71e-9a7e-4969-abb9-7c7d3e3aae3c-drugInteractions-0.txt","TABLE-3ebcb71e-9a7e-4969-abb9-7c7d3e3aae3c-drugInteractions-1.txt","TABLE-3fb2aa58-3a40-4255-a261-e2db5b9a5dde-drugInteractions-0.txt","TABLE-3fb2aa58-3a40-4255-a261-e2db5b9a5dde-drugInteractions-1.txt","TABLE-4445c26e-ec5c-40f4-956b-93c12fc73c1d-drugInteractions-0.txt","TABLE-4445c26e-ec5c-40f4-956b-93c12fc73c1d-drugInteractions-1.txt","TABLE-4bc9a57f-acb4-4f3f-aae4-c1215e0d5c30-drugInteractions-0.txt","TABLE-4bc9a57f-acb4-4f3f-aae4-c1215e0d5c30-drugInteractions-1.txt","TABLE-4e2045c4-4fee-4cc2-b014-6b04a7cea7a5-drugInteractions-0.txt","TABLE-4e2045c4-4fee-4cc2-b014-6b04a7cea7a5-drugInteractions-1.txt","TABLE-514bf988-9d2f-4727-a6ba-a99aa0fd61f6-drugInteractions-0.txt","TABLE-514bf988-9d2f-4727-a6ba-a99aa0fd61f6-drugInteractions-1.txt","TABLE-51c96814-18d9-4c5e-86d1-aced9499dfdf-drugInteractions-0.txt","TABLE-51c96814-18d9-4c5e-86d1-aced9499dfdf-drugInteractions-1.txt","TABLE-56381618-955b-4e4c-b6de-bde4e4abf42e-drugInteractions-0.txt","TABLE-56381618-955b-4e4c-b6de-bde4e4abf42e-drugInteractions-1.txt","TABLE-56df6dd1-d63a-4584-9196-5ba4799d1c45-drugInteractions-0.txt","TABLE-56df6dd1-d63a-4584-9196-5ba4799d1c45-drugInteractions-1.txt","TABLE-58728c03-948a-4940-b1be-5aeadab29c74-drugInteractions-0.txt","TABLE-58728c03-948a-4940-b1be-5aeadab29c74-drugInteractions-1.txt","TABLE-5907ef77-9c4d-4e3f-be7b-6157ebad2173-drugInteractions-0.txt","TABLE-5907ef77-9c4d-4e3f-be7b-6157ebad2173-drugInteractions-1.txt","TABLE-651d3aa8-97b1-4fb8-899e-d2448ab41432-drugInteractions-0.txt","TABLE-651d3aa8-97b1-4fb8-899e-d2448ab41432-drugInteractions-1.txt","TABLE-694e258d-86bd-440c-870b-a7d27fb1c467-drugInteractions-0.txt","TABLE-694e258d-86bd-440c-870b-a7d27fb1c467-drugInteractions-1.txt","TABLE-6a0068ba-19bd-4711-b894-868fd007a613-drugInteractions-0.txt","TABLE-6a0068ba-19bd-4711-b894-868fd007a613-drugInteractions-1.txt","TABLE-6b09bf23-ebdf-4422-b755-0d877a01ea38-drugInteractions-0.txt","TABLE-6b09bf23-ebdf-4422-b755-0d877a01ea38-drugInteractions-1.txt","TABLE-6c52f923-61a9-41b1-877a-363df6ca897e-drugInteractions-0.txt","TABLE-6c52f923-61a9-41b1-877a-363df6ca897e-drugInteractions-1.txt","TABLE-70741a88-5e0f-4171-89c8-425fb4e234e8-drugInteractions-0.txt","TABLE-70741a88-5e0f-4171-89c8-425fb4e234e8-drugInteractions-1.txt","TABLE-75f9abdf-52f2-48ee-b65b-9160c38564ec-drugInteractions-0.txt","TABLE-75f9abdf-52f2-48ee-b65b-9160c38564ec-drugInteractions-1.txt","TABLE-77f258d9-f380-4815-8140-0b2bfda3099c-drugInteractions-0.txt","TABLE-77f258d9-f380-4815-8140-0b2bfda3099c-drugInteractions-1.txt","TABLE-7999d658-ddb7-4470-87fe-202358ce4c17-drugInteractions-0.txt","TABLE-7999d658-ddb7-4470-87fe-202358ce4c17-drugInteractions-1.txt","TABLE-801e4da1-5459-47d2-b67b-009f0a3247cc-drugInteractions-0.txt","TABLE-801e4da1-5459-47d2-b67b-009f0a3247cc-drugInteractions-1.txt","TABLE-801e4da1-5459-47d2-b67b-009f0a3247cc-drugInteractions-2.txt","TABLE-801e4da1-5459-47d2-b67b-009f0a3247cc-drugInteractions-3.txt","TABLE-801e4da1-5459-47d2-b67b-009f0a3247cc-drugInteractions-4.txt","TABLE-801e4da1-5459-47d2-b67b-009f0a3247cc-drugInteractions-5.txt","TABLE-8547fd78-7483-4790-8c45-0da3c7e6b7b6-drugInteractions-0.txt","TABLE-8547fd78-7483-4790-8c45-0da3c7e6b7b6-drugInteractions-1.txt","TABLE-89b48f74-7188-4bf2-a99b-6e9b9bc8720f-drugInteractions-0.txt","TABLE-89b48f74-7188-4bf2-a99b-6e9b9bc8720f-drugInteractions-1.txt","TABLE-8ad881e0-ca41-42ad-9d7d-eb85b3a30af0-drugInteractions-0.txt","TABLE-8ad881e0-ca41-42ad-9d7d-eb85b3a30af0-drugInteractions-1.txt","TABLE-91fa852c-b43d-4a55-983b-74aa6827125d-drugInteractions-0.txt","TABLE-91fa852c-b43d-4a55-983b-74aa6827125d-drugInteractions-1.txt","TABLE-95e23715-f2bf-4998-aa51-3a7964e2cbb3-drugInteractions-0.txt","TABLE-95e23715-f2bf-4998-aa51-3a7964e2cbb3-drugInteractions-1.txt","TABLE-9802402a-00e5-4446-832c-cb01e0af7b3e-drugInteractions-0.txt","TABLE-9802402a-00e5-4446-832c-cb01e0af7b3e-drugInteractions-1.txt","TABLE-98ba5f6a-925e-4f98-a023-6cafa86ed74a-drugInteractions-0.txt","TABLE-98ba5f6a-925e-4f98-a023-6cafa86ed74a-drugInteractions-1.txt","TABLE-9c45edc1-5935-4685-9404-6ce7b7bb4056-drugInteractions-0.txt","TABLE-9c45edc1-5935-4685-9404-6ce7b7bb4056-drugInteractions-1.txt","TABLE-a0cfad4b-043e-451e-bfd6-1fe1ac1bd0d6-drugInteractions-0.txt","TABLE-a0cfad4b-043e-451e-bfd6-1fe1ac1bd0d6-drugInteractions-1.txt","TABLE-a0cfad4b-043e-451e-bfd6-1fe1ac1bd0d6-drugInteractions-2.txt","TABLE-a0cfad4b-043e-451e-bfd6-1fe1ac1bd0d6-drugInteractions-3.txt","TABLE-a0cfad4b-043e-451e-bfd6-1fe1ac1bd0d6-drugInteractions-4.txt","TABLE-a0cfad4b-043e-451e-bfd6-1fe1ac1bd0d6-drugInteractions-5.txt","TABLE-a1150d78-57cc-4216-beff-f7ea7364ab89-drugInteractions-0.txt","TABLE-a1150d78-57cc-4216-beff-f7ea7364ab89-drugInteractions-1.txt","TABLE-a1150d78-57cc-4216-beff-f7ea7364ab89-drugInteractions-2.txt","TABLE-a1150d78-57cc-4216-beff-f7ea7364ab89-drugInteractions-3.txt","TABLE-a1150d78-57cc-4216-beff-f7ea7364ab89-drugInteractions-4.txt","TABLE-a1150d78-57cc-4216-beff-f7ea7364ab89-drugInteractions-5.txt","TABLE-a9ca7308-059b-4d24-a0af-aa85adc108df-drugInteractions-0.txt","TABLE-a9ca7308-059b-4d24-a0af-aa85adc108df-drugInteractions-1.txt","TABLE-ab047628-67d0-4a64-8d77-36b054969b44-drugInteractions-0.txt","TABLE-ab047628-67d0-4a64-8d77-36b054969b44-drugInteractions-1.txt","TABLE-ab50f13c-7ec9-44b4-9a9f-ee3ddda6c8ea-drugInteractions-0.txt","TABLE-ab50f13c-7ec9-44b4-9a9f-ee3ddda6c8ea-drugInteractions-1.txt","TABLE-abfb23bd-54b5-4ec7-a067-814167f2060f-drugInteractions-0.txt","TABLE-abfb23bd-54b5-4ec7-a067-814167f2060f-drugInteractions-1.txt","TABLE-b1b766b1-0327-48cd-ab01-e85038cf365f-drugInteractions-0.txt","TABLE-b1b766b1-0327-48cd-ab01-e85038cf365f-drugInteractions-1.txt","TABLE-b6233f92-0d92-44d0-82cb-bacccb61d970-drugInteractions-0.txt","TABLE-b6233f92-0d92-44d0-82cb-bacccb61d970-drugInteractions-1.txt","TABLE-b6233f92-0d92-44d0-82cb-bacccb61d970-drugInteractions-2.txt","TABLE-b6233f92-0d92-44d0-82cb-bacccb61d970-drugInteractions-3.txt","TABLE-b6233f92-0d92-44d0-82cb-bacccb61d970-drugInteractions-4.txt","TABLE-b6233f92-0d92-44d0-82cb-bacccb61d970-drugInteractions-5.txt","TABLE-ba41b963-ec4a-4421-ac93-26654876a6be-drugInteractions-0.txt","TABLE-ba41b963-ec4a-4421-ac93-26654876a6be-drugInteractions-1.txt","TABLE-bc7ed493-67b3-476a-829f-6ccf48c874c1-drugInteractions-0.txt","TABLE-bc7ed493-67b3-476a-829f-6ccf48c874c1-drugInteractions-1.txt","TABLE-bd72a7c7-ff12-4b95-8d39-4426231bd5aa-drugInteractions-0.txt","TABLE-bd72a7c7-ff12-4b95-8d39-4426231bd5aa-drugInteractions-1.txt","TABLE-c01c31e0-9c1b-4bb6-ae6e-0b805264c4e6-drugInteractions-0.txt","TABLE-c01c31e0-9c1b-4bb6-ae6e-0b805264c4e6-drugInteractions-1.txt","TABLE-c0f238ff-2804-4150-9766-22a5111b4e74-drugInteractions-0.txt","TABLE-c0f238ff-2804-4150-9766-22a5111b4e74-drugInteractions-1.txt","TABLE-c437507c-d308-4aac-aa5e-a54972c7fa95-drugInteractions-0.txt","TABLE-c437507c-d308-4aac-aa5e-a54972c7fa95-drugInteractions-1.txt","TABLE-c437507c-d308-4aac-aa5e-a54972c7fa95-drugInteractions-2.txt","TABLE-c437507c-d308-4aac-aa5e-a54972c7fa95-drugInteractions-3.txt","TABLE-c437507c-d308-4aac-aa5e-a54972c7fa95-drugInteractions-4.txt","TABLE-c437507c-d308-4aac-aa5e-a54972c7fa95-drugInteractions-5.txt","TABLE-c90be37c-0ad0-4ccd-8fe7-b9a3427f0d80-drugInteractions-0.txt","TABLE-c90be37c-0ad0-4ccd-8fe7-b9a3427f0d80-drugInteractions-1.txt","TABLE-cd6d1b85-0ba2-4a10-a5b8-25496ae13fa3-drugInteractions-0.txt","TABLE-cd6d1b85-0ba2-4a10-a5b8-25496ae13fa3-drugInteractions-1.txt","TABLE-d52a68b4-86a8-40a4-9f74-a3ef5795db51-drugInteractions-0.txt","TABLE-d52a68b4-86a8-40a4-9f74-a3ef5795db51-drugInteractions-1.txt","TABLE-d655ff56-c17d-4331-8e9c-93e36f4ffeae-drugInteractions-0.txt","TABLE-d655ff56-c17d-4331-8e9c-93e36f4ffeae-drugInteractions-1.txt","TABLE-d91934a0-902e-c26c-23ca-d5accc4151b6-drugInteractions-0.txt","TABLE-d91934a0-902e-c26c-23ca-d5accc4151b6-drugInteractions-1.txt","TABLE-e6d0a19a-8d4e-4c58-a3e4-d90c88acd499-drugInteractions-0.txt","TABLE-e6d0a19a-8d4e-4c58-a3e4-d90c88acd499-drugInteractions-1.txt","TABLE-e9d8fb69-a4c7-48cb-a4a9-e5d18eb4fd63-drugInteractions-0.txt","TABLE-e9d8fb69-a4c7-48cb-a4a9-e5d18eb4fd63-drugInteractions-1.txt","TABLE-f11079c4-f085-4558-bee9-c159525b2497-drugInteractions-0.txt","TABLE-f11079c4-f085-4558-bee9-c159525b2497-drugInteractions-1.txt","TABLE-feaa5f6f-9753-4f37-ab81-04c9c6b45e6a-drugInteractions-0.txt","TABLE-feaa5f6f-9753-4f37-ab81-04c9c6b45e6a-drugInteractions-1.txt"]

#*******************************************************************************************************************************************************
# Iterate through each file in the list and
# 1) store the content and structures (i.e., the string of the table) if its brand new
#*******************************************************************************************************************************************************

fileCount=len(fileL)
#Shows 144 files in the list



#initialize dictionary
#d={}


readFile= "../data/warfarin/"+fileL[0]
f = open(readFile)
soup=BeautifulSoup(f)
f.close()
# this is how you get the string for the table
tableStr = str(soup)

d={fileL[0]:tableStr}

i= 0
for i in range(1, fileCount-1):

    # this is how you get can process the HTML tags and content
    #f = open("../data/warfarin/" + , "r")
    #soup = BeautifulSoup(f)
    #f.close()
    readFile= "../data/warfarin/"+fileL[i]
    f = open(readFile)
    soup=BeautifulSoup(f)
    f.close()
    # this is how you get the string for the table
    tableStr = str(soup)


    for key in d:
        if key==fileL[i]:
            #mark somehow that they're identical
            i+=1
        else:
            d[fileL[i]]= tableStr
            #ERROR: dictionary size changed during interaction**********************************************
            i+=1

    print(d)
        


# (example starter code)

# Find all rows and then look for rows that have a comma-delimitted
# list. Print out the items in those lists.
table = soup.find('table')
rows = table.findAll('tr')
headers=table.findAll('content')


#*******************************************************************************************************************************************************
# 2) If the table matches another tables string content, then it is
# the same table. Somehow note that it is same table.
#*******************************************************************************************************************************************************



#*******************************************************************************************************************************************************
# 3) It the table does not match, then its not the same table, so,
# what is different about it? Is it the structure? Is it the content
# (e.g., additional drugs)?
#*******************************************************************************************************************************************************


#*******************************************************************************************************************************************************
# 4) Create a simple report that shows the different "types" of tables
#*******************************************************************************************************************************************************
    
