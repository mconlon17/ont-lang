# Ont-lang

Provide a simple means for adding text in various languages to ontologies.

## Four step process

1. Extract the existing assertions from an existing ontology.  For each class and 
property, 
extract the assertions that contain text.  Provide the assertions in two languages, 
the reference langiage (often english) and the target language (any other language).  
The result is a TSV file
1. Edit the TSV file to add/correct text in the target language.
1. Create a set of assertions that can be merged into the existing ontology

## Tools used 

python, SPARQL, robot

## Usage Example

In the steps below we add text for french to the language ontology

### Step 1 -- extract english and french from the language ontology

    python3 get-text.py en fr lang.owl
    
`get-text.py` produces a TSV file `translate-en-fr.tsv`

### Step 2 -- provide additional language text

A translator edits `translate-en-fr.tsv` to provide additional language text for french.
The translator can add as many or as few translations as they wish, or improve
existing translations.

### Step 3 -- create language assertions

    python3 put-text.py translate-en-fr.tsv fr.owl
    
The file edited by the translator is used as input to `put-text.py`  

### Step 4 -- merge the new assertions into the ontology

The resulting  file `fr.owl` can be merged to the language ontology.  This can be 
accomplished using robot as shown below:

    robot merge --input lang.owl --input fr.owl --output new-lang.owl
    
The resulting ontology file `new-lang.owl` contains the translations provided by the
translator.
