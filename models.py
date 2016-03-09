import re

VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
              'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR',
              'NOTE']

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
