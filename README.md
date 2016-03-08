[![Build Status](https://travis-ci.org/rickhousley/SSW-Agile-GEDCOM.svg?branch=master)](https://travis-ci.org/rickhousley/SSW-Agile-GEDCOM)

### Synopsis
This is a command-line program used to discover errors and anomalies in GEDCOM geanealogy files. This was developed for the Stevens Graduate Software Engineering course *Agile Methods for Software Development* (SSW 555) as an exercise in Extreme Programming and Scrum methods.

### Execution

To parse the default GEDCOM pass no arguments:
```
python ged_parser.py
```

To parse a specific GEDCOM pass a path argument:
```
python ged_parser.py ged_tests/bgardner_P02.ged
```

### Tests
To run feature tests:
```
python ged_parser.py test
```

### Current Features
| Story ID | Story Name                | Owner |
|----------|---------------------------|-------|
| US01     | Dates before current date | mm    |
| US02     | Birth before marriage     | mm    |
| US03     | Birth before death        | bg    |
| US04     | Marriage before divorce   | bg    |
| US05     | Marriage before death     | rh    |
| US06     | Divorce before death      | rh    |


### Contributors
+ Bryan Gardner
+ Rick Housley
+ Michael McCarthy
