frontier
========

## Overview of Contents

    .
    ├── Frontier
    │   ├── IO
    │   │   ├── AQCReader.py                    Class to read from AQC Matrix Files
    │   │   ├── AbstractReader.py               Abstract class to inherit generic file reading
    │   │   │                                     methods for users to implement custom readers
    │   │   ├── BamcheckReader.py               Class to read from BAMcheckr'd Files
    │   │   └── __init__.py                     Package definition
    │   │
    │   ├── __init__.py                         Package definition
    │   └── frontier.py                         Frontier module containing classification
    │                                             utilities and the Statplexer class
    │
    ├── Goldilocks
    │   ├── __init__.py                         Package definition
    │   ├── goldilocks.py                       Goldilocks module
    │   └── paths.g                             Paths File used for goldilocks.py
    │
    │
    ├── R
    │   ├── goldilocks_regionplot.R             R script for plotting variant density vs.
    │   │                                         region location as displayed in Chap.9
    │   ├── lanemap.r                           R script to investigate potential correlation
    │   │                                         between samples, lanes and lanelets
    │   └── megabase_regions                    Input data for goldilocks_regionplot.R script
    │
    │
    ├── results
    │   ├── front
    │   │   ├── log
    │   │   │   └── *                           Log files generated by Front for each experiment,
    │   │   │                                     named in the format yyyy-mm-dd_hhmm__dset_pset_score.txt
    │   │   │
    │   │   └── pdf
    │   │       └── *                           Directories of PDF files generated by Front each
    │   │                                         containing 10 trees drawn by graphviz, one for each
    │   │                                         training and testing fold.
    │   │                                         Named in the format yyyy-mm-dd_hhmm__dset_pset_/
    │   │
    │   └── goldilocks
    │       ├── goldilocks.log                  Latest log file from Goldilocks execution
    │       ├── megabase_plot.pdf               PDF containing Figure 9.2
    │       └── megabase_plot.png               PNG containing Figure 9.2
    │
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
    │
    ├── .gitignore
    ├── README.md
    ├── front.py                                Script using Frontier and scikit-learn for analysis
    │                                             of auto_qc data and targets for training, testing
    │                                             and documentation of decision tree classifiers.
    ├── msn_FinalReport_2014.pdf                The final version of the thesis write up
    └── ratios.py                               A proof of concept file showing bamcheckr
                                                  function can be implemented by Frontier


## Other Contributions

Please see the following for examples of contributions to external projects made as a result of this project:

### samtools
[samtools #200](https://github.com/samtools/samtools/pull/200): **Fix arbitrary memory leaks in merge and split test harnesses**  
[samtools #188](https://github.com/samtools/samtools/pull/188): **Add -b option to samtools merge manpage**

### bamcheckr
[seq_autoqc #2](https://github.com/wtsi-hgi/seq_autoqc/pull/2): **Fix quality_dropoff.r**

## Installation

Both the `Frontier` and `Goldilocks` packages require `numpy` for its efficient data containers.
Additionally the `front.py` script requires the `scikit-learn` machine learning framework.

You can install these packages via `pip`:

    pip install scikit-learn numpy

Although included with some distributions, for the plotting of decision trees as PDF files you may need to install `graphviz` and `pydot` via your distribution's package manager and `pip`, respectively.

    yum install graphviz
    pip install pydot

The R scripts require the `R` data analysis language to be installed via an appropriate package manager.

    yum install R

Once installed, use the `R` environment to download and install the packages:

    install.packages("ggplot2")
    install.packages("reshape")
    install.packages("plyr")
    install.packages("pheatmap")

##Housekeeping

### View documentation using pydoc (from this directory)

    # Front AQC Module
    pydoc front

    # Frontier Package
    pydoc Frontier
    pydoc Frontier.frontier

    # Frontier IO Subpackage
    pydoc Frontier.IO
    pydoc Frontier.IO.AbstractReader
    pydoc Frontier.IO.AQCReader
    pydoc Frontier.IO.BamcheckReader

    # Goldilocks
    pydoc Goldilocks
    pydoc Goldilocks.goldilocks

### Run tests

    # Frontier
    python -m tests/frontier
    python -m tests/aqcreader
    python -m tests/bamcheckreader

    # Goldilocks
    python -m tests/goldilocks
