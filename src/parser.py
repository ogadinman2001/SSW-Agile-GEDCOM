""" Python module for parsing GEDCOM geneaology files - parser

    This file provides the parsing utility for the GEDCOM parsing project
"""
from models import Gedline, Individual, Family
from datetime import datetime


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
            individuals.append(parse_single_individual(gedlist, index,
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
    for gedline in gedlist[index + 1:]:
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
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None
            elif date_type == "DEAT":
                # Store death as datetime object
                indiv.death = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
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
    for gedline in gedlist[index + 1:]:
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
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None

            elif date_type == "DIV":
                # Store divorce date as datetime
                family.divorce = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None
            else:
                print "ERROR"

    return family
