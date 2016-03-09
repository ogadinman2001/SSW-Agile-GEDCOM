#!/usr/bin/env python
""" Python module for parsing GEDCOM geneaology files

    This is a command-line program used to discover errors and anomalies in
    GEDCOM geanealogy files. This was developed for the Stevens Graduate
    Software Engineering course Agile Methods for Software Development (SSW 555)
    as an exercise in Extreme Programming and Scrum methods.

    Currently reads a) default_ged.ged from local directory, b) a passed GEDCOM
    file, or c) runs the tests on the acceptance tests. After reading in a file
    the GEDCOM is parsed and scanned for errors using our verification features.
"""

__author__ = "Rick Housley, Bryan Gardner, Michael McCarthy"
__email__ = "rhousley@stevens.edu, bgardne2@stevens.edu, mmccart1@stevens.edu"

import sys
import operator
import os
import unittest

# Project imports
from parser import parse_ged
from user_stories import validation, anomaly_locations, error_locations
from unit_tests import TestParser

FILENAME = 'default_ged.ged'

def main():
    """ Main function for parsing of GEDCOM"""

    # @TODO: Gardner implement argparse!
    graphing_flag = 0

    # Allow for arguments to be passed for filename
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
            if unittest.TextTestRunner(verbosity=1).run(suite).failures:
                exit(-1)
            else:
                exit()

        else:
            path = sys.argv[1]
            if os.path.exists(path):
                individuals, families = parse_ged(path)
    else:
        individuals, families = parse_ged(FILENAME)

    # Print Summary of results
    summary(individuals, families)

    # Run error & anomaly detection on parsed data
    validation(individuals, families)

    # Create Visualization
    if graphing_flag:
        try:
            # Do import here to prevent import error on new systems
            import ged_vis
            ged_vis.graph_family(families, individuals, \
                errors=error_locations, anomalies=anomaly_locations)

        except ImportError:
            print "GraphViz python import not installed!"

    print "\nDone!"
    exit()

def summary(individuals, families):
    """ Prints a summary of the GEDCOM file """

    individuals.sort(key=operator.attrgetter('int_id'))
    families.sort(key=operator.attrgetter('int_id'))

    print "\n"
    print 'INDIVIDUALS'.center(80,' ')
    print "\n"
    print '{:6s} {:20s} {:5s} {:10s}     {:10s}'\
        .format('ID', 'Individual Name', 'Sex', 'Birthdate', 'Deathdate')
    print '-' * 80
    for indiv in individuals:
        print '{:6s} {:20s} {:5s} {:.10s}     {:.10s}'\
        .format(indiv.uid, ' '.join(indiv.name), indiv.sex, \
        str(indiv.birthdate), str(indiv.death))

    print "\n\n"
    print 'FAMILIES'.center(80,' ')
    print "\n"
    print '{:6s} {:20s} {:20s} {:10.10s} {:10.10s} {}'\
        .format('ID', 'Husband', 'Wife', 'M-Date', 'D-Date',\
         '# Child')
    print '-' * 80
    for family in families:
        husband_name = None
        wife_name = None
        for indiv in individuals:
            if family.husband == indiv.uid:
                husband_name = indiv.name
            if family.wife == indiv.uid:
                wife_name = indiv.name
        print '{:6s} {:20s} {:20s} {:10.10s} {:10.10s} {}'\
        .format(family.uid, ' '.join(husband_name),' '.join(wife_name), \
        str(family.marriage), str(family.divorce), len(family.children))
    print "\n\n"

if __name__ == '__main__':
    main()
