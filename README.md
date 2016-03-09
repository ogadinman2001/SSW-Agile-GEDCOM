# SSW 555 - GEDCOM Error/Anomaly Detection
[![Build Status](https://travis-ci.org/rickhousley/SSW-Agile-GEDCOM.svg?branch=master)](https://travis-ci.org/rickhousley/SSW-Agile-GEDCOM)

## Synopsis
This is a command-line program used to discover errors and anomalies in GEDCOM geanealogy files. This was developed for the Stevens Graduate Software Engineering course *Agile Methods for Software Development* (SSW 555) as an exercise in Extreme Programming and Scrum methods.

Currently the program has the ability to
* Read a default_ged.ged from local directory
* Read a GEDCOM file passes as an argument
* Run test criteria
* Create a visualization with *error highlighting*

Current process:
Parse -> Summarize -> Validate -/-> Visualize
(Visualize will only occur if visualize flag is set)

## Installation
**This is only needed if you want to include the visualization feature!**

Install Python requirements:
```
pip install -r requirements.txt
```
Install GraphViz binary:
Fedora:
```
sudo dnf install graphviz
```
Ubuntu:
```
sudo apt-get install graphviz
```
Windows:

http://www.graphviz.org/pub/graphviz/stable/windows/graphviz-2.30.1.msi

## Execution

To parse the default GEDCOM pass no arguments:
```
python run.py
```

To parse a specific GEDCOM pass a path argument:
```
python run.py ged_tests/bgardner_P02.ged
```

## Tests
To run feature tests:
```
python run.py test
```
## Visualization Sample:
* Couples will have the same colors
* Anomalies will show up as orange octagons
* Errors will show up as red octagons

![Sample Visualization](/imgs/sample_tree.svg)


## Current Features
| Story ID | Story Name                | Owner |
|----------|---------------------------|-------|
| US01     | Dates before current date | mm    |
| US02     | Birth before marriage     | mm    |
| US03     | Birth before death        | bg    |
| US04     | Marriage before divorce   | bg    |
| US05     | Marriage before death     | rh    |
| US06     | Divorce before death      | rh    |


## Contributors
+ Bryan Gardner
+ Rick Housley
+ Michael McCarthy
