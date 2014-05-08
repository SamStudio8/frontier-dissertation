frontier
========

## Overview of Contents

    .
    ├── Frontier
    │   ├── IO
    │   │   ├── AQCReader.py
    │   │   ├── AbstractReader.py
    │   │   ├── BamcheckReader.py
    │   │   └── __init__.py
    │   │
    │   ├── __init__.py
    │   └── frontier.py
    │
    ├── Goldilocks
    │   ├── __init__.py
    │   ├── goldilocks.log
    │   ├── goldilocks.py
    │   ├── goldilocks_regionplot.R
    │   ├── megabase_plot.pdf
    │   ├── megabase_plot.png
    │   ├── megabase_regions
    │   └── paths.g
    │
    ├── tests
    │   ├── data
    │   │   ├── goldilocks
    │   │   │   ├── group0_1.q
    │   │   │   ├── group0_2.q
    │   │   │   ├── group1_1.q
    │   │   │   └── paths.g
    │   │   │
    │   │   ├── example.aqc.txt
    │   │   ├── example.aqc.uniq.txt
    │   │   ├── example.bamcheck.baddups.txt
    │   │   ├── example.bamcheck.dups.txt
    │   │   └── example.bamcheck.txt
    │   │
    │   ├── __init__.py
    │   ├── aqcreader.py
    │   ├── bamcheckreader.py
    │   ├── frontier.py
    │   └── goldilocks.py
    │
    ├── .gitignore
    ├── README.md
    ├── front.py
    ├── msn_FinalReport_2014.pdf
    └── ratios.py



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
