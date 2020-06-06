#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    put-text: given a language file created by get-text.py, and presumaby edited
    by a translator to add translations for the to language, use robot to create
    assertions which can be merged to the original ontology to add translations.
    
    For example:
    
    put-text.py fr translate-en-fr.tsv fr.owl
    
    will read the in-file, create assertions, and write them to the out-file

"""

import argparse

global verbose

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.1.0"


def ont_put(args):
    import os
    
    header = f'ID\tLabel\nID\tAL rdfs:label@{args.lang_to}'
    print(header, file=open('template.tsv', 'w'))
    input_file = open(args.input_filename)
    next(input_file)
    for line in input_file:
        columns = line[:-1].split('\t')
        if columns[2][1:-1] != "":
        	print(columns[0][1:-1], columns[2][1:-1], file=open('template.tsv', 'a'), sep='\t')
    input_file.close()
        
    robot_cmd = f'robot template --template template.tsv --output {args.output_filename}'
    
    os.system(robot_cmd)
    
    return None


def main():
    parser = argparse.ArgumentParser(description="get language text from an ontology")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("lang_to", help="the to language")
    parser.add_argument("input_filename", help="the name of TSV file containing the translations")
    parser.add_argument("output_filename", help="the name of the file to contain the assertions")
    args = parser.parse_args()
    if args.verbose > 0:
        print(args.lang_to)
        print(args.input_filename)
        print(args.output_filename)
    ont_put(args)
    return


if __name__ == "__main__":
    main()
