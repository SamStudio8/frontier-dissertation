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
    │   └── frontier.py                         Frontier module containing classification
    │                                             utilities and the Statplexer class
    │
    ├── Goldilocks                              
    │   ├── __init__.py                         Package definition
    │   ├── goldilocks.log                      Latest log file from Goldilocks execution
    │   ├── goldilocks.py                       Goldilocks module
    │   ├── goldilocks_regionplot.R             R script for plotting variant density vs.
    │   │                                         region location as displayed in Chap.9
    │   ├── megabase_plot.pdf                   PDF containing Figure 9.2
    │   ├── megabase_plot.png                   PNG containing Figure 9.2
    │   ├── megabase_regions                    Input data for regionplot.R script
    │   └── paths.g                             Paths File used for goldilocks.py
    │
    ├── tests
    │   ├── data
    │   │   ├── goldilocks                      
    │   │   │   ├── group0_1.q                  }
    │   │   │   ├── group0_2.q                  } Variant Query Files for testing Goldilocks
    │   │   │   ├── group1_1.q                  }
    │   │   │   └── paths.g                     Paths File locating VQF testing files
    │   │   │
    │   │   ├── example.aqc.txt                 AQC Matrix example with non-consistent
    │   │   │                                     intraclass target labels
    │   │   ├── example.aqc.uniq.txt            AQC Matrix example with consistent
    │   │   │                                     intraclass target labels
    │   │   ├── example.bamcheck.baddups.txt    BAMcheckr'd example containing non matching
    │   │   │                                     duplicate summary number entries
    │   │   ├── example.bamcheck.dups.txt       BAMcheckr'd example with consistent
    │   │   │                                     duplicated summary number entries
    │   │   └── example.bamcheck.txt            Valid BAMcheckr'd example
    │   │
    │   ├── __init__.py                         Package definition
    │   ├── aqcreader.py                        AQCReader testing suite
    │   ├── bamcheckreader.py                   BamcheckReader testing suite
    │   ├── frontier.py                         Frontier and Frontier utils testing suite
    │   └── goldilocks.py                       Goldilocks testing suite
    │
    ├── .gitignore
    ├── README.md
    ├── front.py                                Script using Frontier and scikit-learn for analysis
    │                                             of auto_qc data and targets for training, testing
    │                                             and documentation of decision tree classifiers.
    ├── msn_FinalReport_2014.pdf                The final version of the thesis write up
    └── ratios.py                               A proof of concept file showing bamcheckr
                                                  function can be implemented by Frontier



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
