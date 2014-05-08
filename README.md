frontier
========

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
