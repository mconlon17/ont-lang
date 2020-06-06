#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    get-text: given two languages and an ontology, extract the text for the two
    languages and write a TSV file for a translater to provide additional text
    in the second language.
    
    For example:
    
    get-text.py en de lang.owl
    
    will extract the english and german text from lang.owl to a TSV file

"""

import argparse

global verbose

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.1.0"


def ont_get(args):
    import os
    
        
    robot_cmd = f'robot query --format TSV --input {args.filename} --query get-text.sparql translate-{args.lang_from}-{args.lang_to}.tsv'

    q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?s (MAX(?slang1) AS ?lang1) (MAX(?slang2) AS ?lang2)
    WHERE {
        { ?s a owl:Class } UNION 
        { ?s a owl:ObjectProperty } UNION 
        { ?s a owl:DatatypeProperty } UNION 
        { ?s a owl:AnnotationProperty }
        
        OPTIONAL {  
            ?s rdfs:label ?label . 
            BIND(lang(?label) AS ?lang)       
            BIND(IF(?lang="<lang_from>", str(?label), "") AS ?slang1)
            BIND(IF(?lang="<lang_to>", str(?label), "") AS ?slang2)
        }
    }
    GROUP BY ?s
    ORDER BY ?s
    """
    q = q.replace('<lang_from>', args.lang_from)
    q = q.replace('<lang_to>', args.lang_to)

    print(q, file=open('get-text.sparql', 'w'))
    
    os.system(robot_cmd)
    
    return None


def main():
    parser = argparse.ArgumentParser(description="get language text from an ontology")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("lang_from", help="the from language")
    parser.add_argument("lang_to", help="the to language")
    parser.add_argument("filename", help="the ontology filename")
    args = parser.parse_args()
    if args.verbose > 0:
        print(args.lang_from)
        print(args.lang_to)
        print(args.filename)
    ont_get(args)
    return


if __name__ == "__main__":
    main()
