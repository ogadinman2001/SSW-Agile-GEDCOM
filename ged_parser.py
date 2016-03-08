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
import re
import operator
import os
from datetime import datetime, timedelta
import unittest

FILENAME = 'default_ged.ged'
PADDING = 80

VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
              'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR',
              'NOTE']

now = datetime.now()

## CLASSES (GEDLINE, FAMILY, INDIVIDUAL)
## ------------------------------------------------------------------

class Gedline(object):
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


class Individual(object):
    """ Class for an individual """

    def __init__(self, uid):
        self.uid = uid
        self.int_id = int(re.search(r'\d+', uid).group())
        self.name = None  # Name of individual
        self.sex = None  # Sex of individual (M or F)
        self.birthdate = None  # Birth date of individual
        self.death = None  # Date of death of individual
        self.famc = []  # Family where individual is a child
        self.fams = []  # Family where individual is spouse


class Family(object):
    """ Class for a family """

    def __init__(self, uid):
        self.uid = uid
        self.int_id = int(re.search(r'\d+', uid).group())
        self.marriage = None  # marriage event for family
        self.husband = None  # pointer for husband in family
        self.wife = None  # pointer for wife in family
        self.children = []  # pointer for child in family
        self.divorce = None  # divorce event in family

## MAIN FUNCTION GOES HERE
#-------------------------

def main():
    """ Main function for parsing of GEDCOM"""

    # Allow for arguments to be passed for filename
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

    summary(individuals, families)
    validation(individuals, families)
    print "\nDone!"

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


# USER STORIES / VALIDATION
#--------------------------------------------------
def validation(individuals, families):
    """ Validation check to run all user stories """

    print "ERRORS/ANOMALIES".center(80,' ')
    print "\nError/Anom:     Description:                                       "\
    "     Location"
    print '-' * 80

    # Sprint 1
    dates_before_current(individuals, families)
    birth_before_marriage(individuals, families)
    birth_before_death(individuals)
    marriage_before_divorce(families)
    marriage_before_death(individuals, families)
    divorce_before_death(individuals, families)

    # Sprint 2

def print_error(etype, description, location):
    estr = 'ERROR {:5.5s}     {:55.55s} {}'\
        .format(etype, description, ','.join(location))
    print estr

def print_anomaly(atype, description, location):
    astr = 'ANOMALY {:5.5s}     {:53.53s} {}'\
        .format(atype, description, ','.join(location))
    print astr


def dates_before_current(individuals, families):
    """ US01 All dates must be before the current date - ERROR"""

    return_flag = True
    error_type = "US01"
    # date of birth, death, marriage, or divorce must be before current date
    for family in families:
        if family.marriage and family.marriage > now:
            error_descrip = "Marriage occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            print_error(error_type, error_descrip, error_location)
            return_flag = False

        if family.divorce and family.divorce > now:
            error_descrip = "Divorce occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            print_error(error_type, error_descrip, error_location)
            return_flag = False

    for indiv in individuals:
        if indiv.birthdate and indiv.birthdate > now:
            error_descrip = "Birth occurs after current date"
            error_location = [indiv.uid]
            print_error(error_type, error_descrip, error_location)
            return_flag = False

        if indiv.death and indiv.death > now:
            error_descrip = "Death occurs after current date"
            error_location = [indiv.uid]
            print_error(error_type, error_descrip, error_location)
            return_flag = False

    return return_flag


def birth_before_marriage(individuals, families):
    """ US02 - Birth should occur before marriage of that individual - ERROR"""

    # For each individual check if birth occurs before marriage
    return_flag = True
    error_type = "US02"
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

            if wife.birthdate and wife.birthdate > family.marriage:
                # Found a case spouse marries before birthday
                error_descrip = "Birth of wife occurs after marriage"
                error_location = [wife.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False

            if husband.birthdate and husband.birthdate > family.marriage:
                error_descrip = "Birth of husband occurs after marraige"
                error_location = [husband.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False

    return return_flag

def birth_before_death(individuals):
    """ US03 - Birth should occur before death of an individual - ERROR"""
    # For each individual check if death occurs before death
    return_flag = True
    error_type = "US03"
    for individual in individuals:
        if individual.death and individual.birthdate:
            if individual.death < individual.birthdate:
                error_descrip = "Birth occurs before death."
                error_location = [individual.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

def marriage_before_divorce(families):
    """ US04 - Marriage should occur before divorce - ERROR"""

    # Search though the families
    return_flag = True
    error_type = "US04"
    for family in families:
        # Check if family has marriage and divorce dates
        if family.marriage and family.divorce:
            if family.marriage > family.divorce:
                error_descrip = "Marriage occurs after divorce"
                error_location = [family.uid, family.husband, family.wife]
                print_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

def marriage_before_death(individuals, families):
    """ US05 - Marriage should occur before death of either spouse - ERROR"""

    # For each family find spouses IDs
    error_type = "US05"
    return_flag = True
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
            if wife.death is not None and family.marriage > wife.death:
                error_descrip = "Marriage occurs after death of wife"
                error_location = [family.uid, wife.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False
            if husband.death is not None and family.marriage > husband.death:
                error_descrip = "Marriage occurs after death of husband"
                error_location = [family.uid, husband.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

def divorce_before_death(individuals, families):
    """ US06 - Divorce should occur before death of either spouse - ERROR"""

    return_flag = True
    error_type = "US06"
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

            # Found a case where spouse death before divorce
            if wife.death is not None and family.divorce > wife.death:
                error_descrip = "Divorce occurs after death of wife"
                error_location = [family.uid, wife.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False
            if husband.death is not None and family.divorce > husband.death:
                error_descrip = "Divorce occurs after death of husband"
                error_location = [family.uid, husband.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

def birth_before_death_of_parents(individuals, families):
    """ US09 - Birth should occur before the death of parents """
    return_flag = True
    error_type = "US09"
    anom_type = "US09"

    # Loop through individuals to compare their brithdate
    # with the death date of their parents
    for individual in individuals:

        # Some individuals do not have parents defined
        # if they are the oldest generation in the gedcom file,
        # so check if individual.famc has elements before proceeding
        if len(individual.famc) > 0:
            father = None
            father_id = None
            mother = None
            mother_id = None

            # Get the UID of parents for an individual
            for family in families:
                if family.uid == individual.famc[0]:
                    father_id = family.husband
                    mother_id = family.wife
                    break

            # Get reference to Father and Mother objects
            # based on their UID
            for ind in individuals:
                if ind.uid == father_id:
                    father = ind
                if ind.uid == mother_id:
                    mother = ind

            # Case when father dies more than 9 months before
            # birth of child. This is an error.
            if father.death is not None and \
                father.death < individual.birthdate - timedelta(days=266):
                error_description = "Child is born more than " +\
                    "9 months after death of father"
                error_location = [family.uid, individual.uid]
                print_error(error_type, error_description, error_location)
                return_flag = False

            # Case when father dies less than 9 months before
            # birth of child. This is an anomaly.
            elif father.death is not None and \
                father.death < individual.birthdate:
                anom_description = "Child is born after death of father " +\
                    "but within 9 months of father's death"
                anom_location = [family.uid, individual.uid]
                print_anomaly(anom_type, anom_description, anom_location)
                return_flag = False

            # Case when mother dies before birth of child.
            # This is impossible.
            if mother.death is not None and mother.death < individual.birthdate:
                error_descrip = "Child is born after death of mother"
                error_location = [family.uid, individual.uid]
                print_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

def no_bigamy(families, individuals):
    """ US11 - Marriage should not occur during marriage to another spouse -
        ANOMALY
    """
        #for each fams check for divorce or death prior to next fam
    anom_type = "US11"
    return_flag = True

    if (1):
        anom_description = "Married to more than one individual at a time"
        anom_location = "l"
        print_anomaly(anom_type, anom_description, anom_location)
        return_flag = False

    return return_flag

def parents_not_too_old(families, individuals):
    """ US12 - Mother should be less than 60 years older than her
    children and father should be less than 80 years older than his children -
    ANOMALY
    """

    pass


# GEDCOM PARSING
# ---------------------------

def parse_ged(filename):
    """ Parses a GEDCOM file. Returns list of individual instances and family
    instances."""
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
            indiv.famc.append(gedline.args[0])
        if gedline.tag == "FAMS":
            indiv.fams.append(gedline.args[0])

        # This assumes the following date tag corresponds to prev tag
        if gedline.tag == "DATE":
            if date_type == "BIRT":
                # Store birthdate as datetime object
                indiv.birthdate = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1], '%b').month, \
                    int(gedline.args[0]))
                date_type = None
            elif date_type == "DEAT":
                # Store death as datetime object
                indiv.death = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1], '%b').month, \
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
            family.children.append(gedline.args[0])

        # This assumes the following date tag corresponds to prev tag
        if gedline.tag == "DATE":
            if date_type == "MARR":
                # Store marriage date as datetime
                family.marriage = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1], '%b').month,\
                    int(gedline.args[0]))
                date_type = None

            elif date_type == "DIV":
                # Store divorce date as datetime
                family.divorce = datetime(
                    int(gedline.args[2]), \
                    datetime.strptime(gedline.args[1], '%b').month, \
                    int(gedline.args[0]))
                date_type = None
            else:
                print "ERROR"

    return family

# Unit testing happens HERE
#--------------------------

class TestParser(unittest.TestCase):
    """ Unit tests to verift unit stories"""

    def test_dates_before_current(self):
        # First load acceptance file
        fail_file = "acceptance_files/fail/date_before_current.ged"
        pass_file = "acceptance_files/pass/date_before_current.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertFalse(dates_before_current(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(dates_before_current(individuals, families))
        else:
            print "!!test_date_before_current acceptance file not found\n\n"

    def test_birth_before_marriage(self):
        # First load acceptance file
        fail_file = "acceptance_files/fail/birth_before_marriage.ged"
        pass_file = "acceptance_files/pass/birth_before_marriage.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(birth_before_marriage(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(birth_before_marriage(individuals, families))
        else:
            print "!!test_marriage_before_death acceptance file not found\n\n"

    def test_marriage_before_death(self):
        # First load acceptance file
        fail_file = "acceptance_files/fail/marriage_before_death.ged"
        pass_file = "acceptance_files/pass/marriage_before_death.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(marriage_before_death(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(marriage_before_death(individuals, families))
        else:
            print "!!test_marriage_before_death acceptance file not found\n\n"

    def test_divorce_before_death(self):
        # First load acceptance file
        fail_file = "acceptance_files/fail/divorce_before_death.ged"
        pass_file = "acceptance_files/pass/divorce_before_death.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(divorce_before_death(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(divorce_before_death(individuals, families))
        else:
            print "!!test_divorce_before_death acceptance file not found\n\n"

    def test_birth_before_death(self):
        #First load acceptance file
        fail_file = "acceptance_files/fail/birth_before_death.ged"
        pass_file = "acceptance_files/pass/birth_before_death.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, _ = parse_ged(pass_file)
            self.assertTrue(birth_before_death(individuals))
            individuals, _ = parse_ged(fail_file)
            self.assertFalse(birth_before_death(individuals))
        else:
            print "!!test_birth_before_death acceptance file not found\n\n"

    def test_marriage_before_divorce(self):
        #First load acceptance file
        fail_file = "acceptance_files/fail/marriage_before_divorce.ged"
        pass_file = "acceptance_files/pass/marriage_before_divorce.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            _, families = parse_ged(pass_file)
            self.assertTrue(marriage_before_divorce(families))
            _, families = parse_ged(fail_file)
            self.assertFalse(marriage_before_divorce(families))
        else:
            print "!!marriage_before_divorce acceptance file not found\n\n"

    def test_birth_before_death_of_parents(self):
        # First load acceptance file
        fail_file_father_anomaly = "acceptance_files/fail/birth_before_death" \
            + "_of_parents_FATHER_anomaly.ged"
        fail_file_father_error = "acceptance_files/fail/birth_before_death" \
            + "_of_parents_FATHER_error.ged"
        fail_file_mother = "acceptance_files/fail/birth_before_death" \
            +"_of_parents_MOTHER.ged"
        pass_file = "acceptance_files/pass/birth_before_death_of_parents.ged"

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(birth_before_death_of_parents(individuals, families))
            individuals, families = parse_ged(fail_file_father_anomaly)
            self.assertFalse(birth_before_death_of_parents(individuals, families))
            individuals, families = parse_ged(fail_file_father_error)
            self.assertFalse(birth_before_death_of_parents(individuals, families))
            individuals, families = parse_ged(fail_file_mother)
            self.assertFalse(birth_before_death_of_parents(individuals, families))
        else:
            print "!!birth_before_death_of_parents acceptance file not found\n\n"

if __name__ == '__main__':
    main()
