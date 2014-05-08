frontier
========

## Overview of Contents

    .
    ├── Frontier                                
    │   ├── IO                                  
    │   │   ├── AQCReader.py                    Class to read from AQC Matrix Files
    │   │   ├── AbstractReader.py               
    │   │   ├── BamcheckReader.py               Class to read from BAMcheckr'd Files
    │   │   └── __init__.py                     Package definition
    │   │
    │   ├── __init__.py                         Package definition
    │   └── frontier.py                         Frontier utilities and Statplexer class
    │
    ├── Goldilocks                              
    │   ├── __init__.py                         Package definition
    │   ├── goldilocks.log                      Latest log file from Goldilocks execution
    │   ├── goldilocks.py                       Goldilocks module
    │   ├── goldilocks_regionplot.R             R script for plotting Chapter 9 diagrams
    │   ├── megabase_plot.pdf                   PDF containing Chapter 9 diagram
    │   ├── megabase_plot.png                   PNG containing Chapter 9 diagram
    │   ├── megabase_regions                    Input data for regionplot.R
    │   └── paths.g                             Input data for goldilocks.py
    │
    ├── tests
    │   ├── data
    │   │   ├── goldilocks                      Paths and Variant Query Files for testing
    │   │   │   ├── group0_1.q
    │   │   │   ├── group0_2.q
    │   │   │   ├── group1_1.q
    │   │   │   └── paths.g
    │   │   │
    │   │   ├── example.aqc.txt                 AQC Matrix example with non varied intraclass labels
    │   │   ├── example.aqc.uniq.txt            AQC Matrix example with unique intraclass labels
    │   │   ├── example.bamcheck.baddups.txt    BAMcheckr'd example with non matching duplicate entries
    │   │   ├── example.bamcheck.dups.txt       BAMcheckr'd example with duplicate entries
    │   │   └── example.bamcheck.txt            BAMcheckr'd example
    │   │
    │   ├── __init__.py                         Package definition
    │   ├── aqcreader.py                        AQCReader testing suite
    │   ├── bamcheckreader.py                   BamcheckReader testing suite
    │   ├── frontier.py                         Frontier and Frontier utilities testing suite
    │   └── goldilocks.py                       Goldilocks testing suite
    │
    ├── .gitignore
    ├── README.md
    ├── front.py                                Script using Frontier and scikit-learn for analysis
    ├── msn_FinalReport_2014.pdf                The final version of the thesis write up
    └── ratios.py                               A proof of concept file showing bamcheckr function can be implemented by Frontier



## Installation

Frontier and the front.py script both require scikit-learn and numpy. Goldilocks requires numpy.

    pip install scikit-learn numpy

For plotting of trees with front.py you may need to install pydot and graphviz:

    yum install graphviz
    pip install pydot

The R scripts require the R programming language to be installed via an appropriate package manager.

front.py...
ratios.py...

##Housekeeping
### View documentation
    pydoc front

    pydoc Frontier/frontier.py
    pydoc Frontier/IO/AbstractReader.py
    pydoc Frontier/IO/AQCReader.py
    pydoc Frontier/IO/BamcheckReader.py

### Run tests
    python -m tests/bamcheckreader
    python -m tests/aqcreader
    python -m tests/frontier
    python -m tests/goldilocks
