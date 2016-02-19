#!/usr/bin/env python
""" Python module for parsing GEDCOM geneaology files

    Currently reads in default_ged.ged from local directory, parses the file
    into Individual and Familiy classes, and then prints the found Individuals
    found in <ID Name> format followed by printing the families found in
    <ID Husband Wife> format. These are printed in order of their IDs

    Implemented User Stories:
    ---
    US05 - Marriage before death
    US06 - Divorce before death
"""

__author__ = "Rick Housley, Bryan Gardner Michael McCarthy"
__email__ = "rhousley@stevens.edu, bgardne2@stevens.edu, mmcart1@stevens.edu"

import operator, re, sys, os
from datetime import datetime
import unittest

FILENAME = 'default_ged.ged'

VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
              'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR',
              'NOTE']


## CLASSES (GEDLINE, FAMILY, INDIVIDUAL)
## ------------------------------------------------------------------

class Gedline:
    """Class for a single line of a GEDCOM file"""

    def __init__(self, line):
        self.level = None
        self.tag = None
        self.xref = None
        self.args = None

        # Do parsing into level, tag, args, xref
        line_listified = line.split(' ',)
        self.level = int(line_listified[0])

        # Default tag format if level > 0
        # <level-number> <tag> <args>
        if self.level > 0:
            self.tag = line_listified[1]
            self.args = line_listified[2:]

        # Check for non default formats
        if self.level == 0:
            # <level-number> <tag> <ignorable args>
            if line_listified[1] in VALID_TAGS:
                self.tag = line_listified[1]
                self.args = line_listified[2:]
                if self.args == []:
                    self.args = None
            # <level-number> <xref-id> <tag>
            else:
                self.xref = line_listified[1]
                self.tag = line_listified[2]

    def __str__(self):
        return self.tag

    def check_if_valid(self):
        """ Checks if the tag parsed is a valid tag"""
        if self.tag in VALID_TAGS:
            return True
        else:
            return False


class Individual:
    """ Class for an individual """

    def __init__(self, uid):
        self.uid = uid
        self.int_id = int(re.search(r'\d+', uid).group())
        self.name = None  # Name of individual
        self.sex = None  # Sex of individual (M or F)
        self.birthdate = None  # Birth date of individual
        self.death = None  # Date of death of individual
        self.famc = None  # Family where individual is a child
        self.fams = None  # Family where individual is spouse


class Family:
    """ Class for a family """

    def __init__(self, uid):
        self.uid = uid
        self.int_id = int(re.search(r'\d+', uid).group())
        self.marriage = None  # marriage event for family
        self.husband = None  # pointer for husband in family
        self.wife = None  # pointer for wife in family
        self.child = None  # pointer for child in family
        self.divorce = None  # divorce event in family

## MAIN FUNCTION GOES HERE
#-------------------------

def main():
    """ Main function for parsing of GEDCOM"""

    # Allow for arg to be passed for filename
    lines = []
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
            unittest.TextTestRunner(verbosity=1).run(suite)
            exit()
        else:
            path = sys.argv[1]
            if os.path.exists(path):
                individuals, families = parse_ged(path)
    else:
        individuals, families = parse_ged(FILENAME)

    # Printing of individuals and families
    individuals.sort(key=operator.attrgetter('int_id'))
    families.sort(key=operator.attrgetter('int_id'))

    print 'Individuals:\n'
    print '{:6s} {:20s}'.format('ID', 'Individual Name')
    print '-' * 26
    for indiv in individuals:
        print '{:6s} {:20s}'.format(indiv.uid, ' '.join(indiv.name))

    print '\n\nFamilies:\n'
    print '{:6s} {:20s} {:20s}'.format('ID', 'Husband', 'Wife')
    print '-' * 46
    for family in families:
        husband_name = None
        wife_name = None
        for indiv in individuals:
            if family.husband == indiv.uid:
                husband_name = indiv.name
            if family.wife == indiv.uid:
                wife_name = indiv.name
        print '{:6s} {:20s} {:20s}'.format(family.uid, ' '.join(husband_name),
                                           ' '.join(wife_name))



# USER STORIES / VALIDATION
#--------------------------------------------------

def birth_before_death(individuals):
    """ US03 - Birth should occur before death of an individual """
    # For each individual check if death occurs before death
    for individual in individuals:
        if (individual.death is not None):
            if (individual.death < individual.birthdate):
                print "Death occurs before death. ID: %s" % individual.uid
                return False
    return True

def marriage_before_death(individuals, families):
    """ US05 - Marriage should occur before death of either spouse """
    # For each family find spouses IDs
    for family in families:
        if family.marriage:
            # Search through individuals to get husband and wife
            husband = None
            wife = None
            for indiv in individuals:
                if indiv.uid == family.husband:
                    husband = indiv
                if indiv.uid == family.wife:
                    wife = indiv
            if (family.marriage is not None) and (wife.death is not None):
                if family.marriage > wife.death:
                    print "Marriage occurs after death (wife)"
                    return False
            if (family.marriage is not None) and (husband.death is not None):
                if family.marriage > husband.death:
                    print "Marriage occurs after death (husb)"
                    return False
    return True

def divorce_before_death(individuals, families):
    """ US06 - Divorce should occur before death of either spouse """
    # For each family find spouses IDs
    for family in families:
        if family.divorce:
            # Search through individuals to get husband and wife
            husband = None
            wife = None
            for indiv in individuals:
                if indiv.uid == family.husband:
                    husband = indiv
                if indiv.uid == family.wife:
                    wife = indiv
            if (family.divorce is not None) and (wife.death is not None):
                if (family.divorce > wife.death):
                    print "Marriage occurs after death (wife)"
                    return False
            if (family.divorce is not None ) and (husband.death is not None):
                if (family.divorce > husband.death):
                    # Found a case where spouse death before divorce
                    print "Marriage occurs after death (husb)"
                    return False
    return True

# GEDCOM PARSING
# ---------------------------

def parse_ged(filename):
    individuals = []
    families = []
    gedlist = []

    lines = [line.rstrip('\n\r') for line in open(filename)]

    # Parse into gedline class
    for line in lines:
        current_ged = Gedline(line)
        gedlist.append(current_ged)

    # Parsing of 0 level tags
    for index, gedline in enumerate(gedlist):
        if gedline.tag == 'INDI':
            individuals.append(parse_single_individual(gedlist, index, \
            gedline.xref))
        if gedline.tag == 'FAM':
            families.append(parse_single_family(gedlist, index, gedline.xref))

    return (individuals, families)

def parse_single_individual(gedlist, index, xref):
    """
    Parses a single individual from a GEDCOM giving the starting index of an
    'INDI' tag. Returns an Individual class
    """
    indiv = Individual(xref)

    date_type = None
    for gedline in gedlist[index+1:]:
        if gedline.level == 0:
            break
        if gedline.tag == "NAME":
            indiv.name = gedline.args
        if gedline.tag == "SEX":
            indiv.sex = gedline.args[0]
        if gedline.tag == "BIRT":
            date_type = "BIRT"
        if gedline.tag == "DEAT":
            date_type = "DEAT"
        if gedline.tag == "FAMC":
            indiv.famc = gedline.args[0]
        if gedline.tag == "FAMS":
            indiv.fams = gedline.args[0]

        # This assumes the following date tag corresponds to prev tag
        if gedline.tag == "DATE":
            if date_type == "BIRT":
                # Store birthdate as datetime object
                indiv.birthdate = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1],'%b').month , \
                    int(gedline.args[0]))
                date_type = None
            elif date_type == "DEAT":
                # Store death as datetime object
                indiv.death = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1],'%b').month , \
                    int(gedline.args[0]))
                date_type = None
            else:
                print "ERROR"

    return indiv


def parse_single_family(gedlist, index, xref):
    """
    Parses a single family from a GEDCOM giving the starting index of a
    'FAM' tag. Returns an Family class
    """
    family = Family(xref)

    date_type = None
    for gedline in gedlist[index+1:]:
        if gedline.level == 0:
            break
        if gedline.tag == "MARR":
            date_type = "MARR"
        if gedline.tag == "DIV":
            date_type = "DIV"

        if gedline.tag == "HUSB":
            family.husband = gedline.args[0]
        if gedline.tag == "WIFE":
            family.wife = gedline.args[0]
        if gedline.tag == "CHIL":
            family.child = gedline.args[0]

        # This assumes the following date tag corresponds to prev tag
        if gedline.tag == "DATE":
            if date_type == "MARR":
                # Store marriage date as datetime
                family.marriage = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1],'%b').month , \
                    int(gedline.args[0]))
                date_type = None

            elif date_type == "DIV":
                # Store divorce date as datetime
                family.divorce = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1],'%b').month , \
                    int(gedline.args[0]))
                date_type = None
            else:
                print "ERROR"

    return family

# Unit testing happens HERE
#--------------------------

class TestParser(unittest.TestCase):

    def test_marriage_before_death(self):
        # First load acceptance file
        fail_file = "acceptance_files/fail/marriage_before_death.ged"
        pass_file = "acceptance_files/pass/marriage_before_death.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(marriage_before_death(individuals,families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(marriage_before_death(individuals,families))
        else:
            print "!!test_marriage_before_death acceptance file not found\n\n"

    def test_divorce_before_death(self):
        # First load acceptance file
        fail_file = "acceptance_files/fail/divorce_before_death.ged"
        pass_file = "acceptance_files/pass/divorce_before_death.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(divorce_before_death(individuals,families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(divorce_before_death(individuals,families))
        else:
            print "!!test_divorce_before_death acceptance file not found\n\n"

    def test_birth_before_death(self):
        #First load acceptance file
        fail_file = "acceptance_files/fail/birth_before_death.ged"
        pass_file = "acceptance_files/pass/birth_before_death.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(birth_before_death(individuals))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(birth_before_death(individuals))
        else:
            print "!!test_birth_before_death acceptance file not found\n\n"

if __name__ == '__main__':
    main()
