# -*- coding: utf-8 -*-

###############################################################
# Reads in the dictionary of table_structures.txt and parses  #
# it as a dictionary                                          #
###############################################################
# Author: Steven DeMarco                                      #
###############################################################

import ast


# Opens text file 'table_structures.txt'
with open('table_structures.txt', 'r') as f:
    dict = ast.literal_eval(f.read())

# Prints each table's unique structure along with each table name
for key in dict:
    if key in dict.keys():
        splits = dict[key].split(' ')
        print 'Table Header Structure: '
        print key
        print 'Table Names: (' + str(len(splits)) + ' tables)'
        for s in splits:
            print s
        print '\n'
