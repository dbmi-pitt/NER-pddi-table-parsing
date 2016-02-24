# -*- coding: utf-8 -*-

###############################################################
# Reads in the dictionary of table_structures.txt and parses  #
# it as a dictionary                                          #
###############################################################
# Author: Steven DeMarco                                      #
###############################################################

import ast


# Opens text file 'table_structures.txt'
with open('output/table_structures.txt', 'r') as f:
    dict = ast.literal_eval(f.read())

# Prints each table's unique structure along with each table name
with open('output/structure_setids.txt', 'w') as out:
    for key in dict:
        if key in dict.keys():
            splits = dict[key].split(' ')
            out.write('Table Header Structure: \n')
            out.write(key)
            out.write('Table Names: (' + str(len(splits)) + ' tables)\n')
            for s in splits:
                if '-' in s:
                    full_table_name = s.split('-')
                    # print full_table_name
                    # print str(len(full_table_name))
                    setID = full_table_name[1] + '-' + full_table_name[2] + '-' + full_table_name[3] + '-' + full_table_name[4] + '-' + full_table_name[5]
                    out.write(setID + '\n')
        out.write('\n')
