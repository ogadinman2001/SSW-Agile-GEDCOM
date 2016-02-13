#!/usr/bin/env python
""" Python module for parsing GEDCOM geneaology files

    Currently reads in default_ged.ged from local directory, parses the file
    into Individual and Familiy classes, and then prints the found Individuals
    found in <ID Name> format followed by printing the families found in
    <ID Husband Wife> format. These are printed in order of their IDs
"""

__author__ = "Rick Housley, Bryan Gardner Michael McCarthy"
__email__ = "rhousley@stevens.edu, bgardne2@stevens.edu, mmcart1@stevens.edu"

import operator, re, sys, os

FILENAME = 'default_ged.ged'

VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
              'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR',
              'NOTE']


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


def main():
    """ Main function for parsing of GEDCOM"""

    gedlist = []
    individuals = []
    families = []

    # Allow for arg to be passed for filename
    if len(sys.argv)>1:
        path = sys.argv[1]
        if os.path.exists(path):
            lines = [line.rstrip('\n\r') for line in open(path)]
    else:
        lines = [line.rstrip('\n\r') for line in open(FILENAME)]

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
                indiv.birthdate = gedline.args
                date_type = None
            elif date_type == "DEAT":
                indiv.death = gedline.args
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
                family.marriage = gedline.args
                date_type = None
            elif date_type == "DIV":
                family.divorce = gedline.args
                date_type = None
            else:
                print "ERROR"

    return family


if __name__ == '__main__':
    main()
