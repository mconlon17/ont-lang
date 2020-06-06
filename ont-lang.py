#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    ont-map: read an ontology and determine paths from properties to entities

    No idea if this will work

    TODO: Everything

"""

import argparse

global verbose

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2020 Michael Conlon"
__license__ = "Apache-2"
__version__ = "0.1.0"


def ont_map(file_name):
    from rdflib import Graph, URIRef, Namespace, RDF, RDFS
    import sys
    global verbose

    owl = Namespace('http://www.w3.org/2002/07/owl#')

    # whatever is going to happen, is going to happen in here

    g = Graph()
    g = g.parse(file_name)

    # Tabulate the object properties

    q = g.query("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?vocab ?term ?s ?label ?domain ?range
        WHERE {
            ?s a owl:ObjectProperty .
            OPTIONAL {?s rdfs:label ?label . }
            FILTER (!STRSTARTS(str(?s), "http://aims"))
            
            BIND(IF(CONTAINS(str(?s), "#"), STRBEFORE(str(?s), "#"), REPLACE( str(?s) , '/[^/]*$', '' ))  AS ?vocab)
            BIND(SUBSTR(REPLACE(str(?s), ?vocab, ''),2) AS ?term)
            
            OPTIONAL { ?s rdfs:domain ?domain .}
            OPTIONAL { ?s rdfs:range ?range . }
        }
        """)
    out_file = open("object-properties.tsv", "w")
    print("Ontology\tTerm\tURI\tLabel\tDomain\tRange", file=out_file)
    for row in q:
        print("%s\t%s\t%s\t%s\t%s\t%s" % row, file=out_file)
    out_file.close()

    if verbose:
        print("Triples in ", file_name, "=", len(g))
        print("ObjectProperties", len(q))

    # Tabulate the Datatype Properties

    q = g.query("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?vocab ?term ?s ?label ?domain ?range
        WHERE {
            ?s a owl:DatatypeProperty .
            OPTIONAL {?s rdfs:label ?label . }
            FILTER (!STRSTARTS(str(?s), "http://aims"))

            BIND(IF(CONTAINS(str(?s), "#"), STRBEFORE(str(?s), "#"), REPLACE( str(?s) , '/[^/]*$', '' ))  AS ?vocab)
            BIND(SUBSTR(REPLACE(str(?s), ?vocab, ''),2) AS ?term)

            OPTIONAL { ?s rdfs:domain ?domain .}
            OPTIONAL { ?s rdfs:range ?range . }
        }
        """)
    out_file = open("datatype-properties.tsv", "w")
    print("Ontology\tTerm\tURI\tLabel\tDomain\tRange", file=out_file)
    for row in q:
        print("%s\t%s\t%s\t%s\t%s\t%s" % row, file=out_file)
    out_file.close()

    if verbose:
        print("DatatypeProperties", len(q))

    # Tabulate the Classes

    q = g.query("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        SELECT (MAX(?vocab) AS ?voc) (MAX(?term) AS ?t) ?s (MAX(?label) AS ?l) (MAX(?super) AS ?su) (MAX(?defn) AS ?d)
        WHERE {
            ?s a owl:Class .
            OPTIONAL {?s rdfs:label ?label . }
            FILTER (!STRSTARTS(str(?s), "http://aims"))
            FILTER (STRSTARTS(str(?s), "http"))

            BIND(IF(CONTAINS(str(?s), "#"), STRBEFORE(str(?s), "#"), REPLACE( str(?s) , '/[^/]*$', '' ))  AS ?vocab)
            BIND(SUBSTR(REPLACE(str(?s), ?vocab, ''),2) AS ?term)

            OPTIONAL { ?s rdfs:subClassOf ?super .}
            OPTIONAL { ?s obo:IAO_0000115 ?def . }
            BIND(REPLACE(str(?def), '\\n', '') AS ?defn)
        }
        GROUP BY ?s
        """)
    out_file = open("classes.tsv", "w")
    print("Ontology\tTerm\tURI\tLabel\tSuperClass\tDefinition", file=out_file)
    for row in q:
        print("%s\t%s\t%s\t%s\t%s\t%s" % row, file=out_file)
    out_file.close()

    if verbose:
        print("Classes", len(q))

    return None


def main():
    global verbose
    parser = argparse.ArgumentParser(description="Ontology entity lister")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="show work")
    parser.add_argument("--input", dest="input", required=True,
                        help="name of file containing ontology", metavar="INPUT",
                        type=str)
    args = parser.parse_args()
    verbose = args.verbose
    if verbose > 0:
        print("Input File name", args.input)
    ont_map(args.input)
    return


if __name__ == "__main__":
    main()
