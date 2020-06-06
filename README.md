# Ont-lang

Hacking around to provide a simple means for adding text in languages to ontologies.

## Command line process
Perhaps there are three steps:

1. Extract the existing assertions from an existing ontology.  For each class and property, extract the assertions that contain text.  Provide the assertions in two languages, the reference langiage (often english) and the target language (any other language).  The result is a CSV file
1. Edit the CSV file to add/correct text in the target language.
1. Update the ontology with the assertions regarding the target language.

### Tools used 

python, SPARQL, robot.

## On-line process

An on-line process would need to *stop* at creating the assertions, and possibly open a pull request against the ontology for review.  Seems unlikley that an on-line process would be authorized to make changes to an ontology.

### Tools used

Javascript, SPARQL, robot, Google Docs API
