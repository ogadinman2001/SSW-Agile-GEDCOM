FILENAME = 'default_ged.ged'

VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', \
    'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

class Gedline:
    """Class for line of gedcom"""

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
        if (self.level > 0):
            self.tag = line_listified[1]
            self.args = line_listified[2:]

        # Check for non default formats
        if (self.level == 0):
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
        if (self.tag in VALID_TAGS):
            return True
        else:
            return False

class Individual:
    """Class for individual"""

    def __init__(self, id):
        self.id = id
        self.name = None  # Name of individual
        self.sex = None # Sex of individual (M or F)
        self.birthdate = None # Birth date of individual
        self.death = None # Date of death of individual
        self.famc = None # Family where individual is a child
        self.fams = None # Family where individual is spouse

    # def __init__(self, id):
    #     self.fam = id
    #     self.marriage = None  # marriage event for family
    #     self.husband = None # pointer for husband in family
    #     self.wife = None # pointer for wife in family
    #     self.children = None # pointer for child in family
    #     self.divorce = None # divorce event in family

class Family:
    """Class for family"""

    def __init__(self):
        pass

def main():
    gedlist = []
    individuals = []
    families = []

    lines = [line.rstrip('\n\r') for line in open(FILENAME)]

    for l in lines:
        #print l
        current_ged = Gedline(l)
        gedlist.append(current_ged)

    # Do invidual parsing
    temp = None
    for i, g in enumerate(gedlist):
        if (g.tag == 'INDI'):
            individuals.append(fill_individual(gedlist, i, g.xref))
        if (g.tag == 'FAM'):
            pass

    for indiv in individuals:
        print indiv.name, indiv.id

def fill_individual(gedlist, index, xref):
    indiv = Individual(xref)
    endNotFound = True
    date_type = None
    for i, g in enumerate(gedlist[index+1:]):
        if (g.level == 0):
            break
        if (g.tag == "NAME"):
            indiv.name = g.args
        if (g.tag == "SEX"):
            indiv.sex = g.args[0]
        if (g.tag == "BIRT"):
            date_type = "BIRT"
        if (g.tag == "DEAT"):
            date_type = "DEAT"
        if (g.tag == "FAMC"):
            indiv.famc = g.args[0]
        if (g.tag == "FAMS"):
            indiv.fams = g.args[0]

        # This assumes the following date tag corresponds to prev tag
        if (g.tag == "DATE"):
            if (date_type=="BIRT"):
                indiv.birthdate = g.args
                date_type = None
            elif (date_type=="DEAT"):
                indiv.death = g.args
                date_type = None
            else:
                print "ERROR"

    return indiv

# def fill_family(gedlist, index, xref):
#     family = Individual(xref)
#     endNotFound = True
#     date_type = None
#     for i, g in enumerate(gedlist[index+1:]):
#         if (g.level == 0):
#             break
#         if (g.tag == "NAME"):
#             indiv.name = g.args
#         if (g.tag == "SEX"):
#             indiv.sex = g.args[0]
#         if (g.tag == "BIRT"):
#             date_type = "BIRT"
#         if (g.tag == "DEAT"):
#             date_type = "DEAT"
#         if (g.tag == "FAMC"):
#             indiv.famc = g.args[0]
#         if (g.tag == "FAMS"):
#             indiv.fams = g.args[0]
#
#         # This assumes the following date tag corresponds to prev tag
#         if (g.tag == "DATE"):
#             if (date_type=="BIRT"):
#                 indiv.birthdate = g.args
#                 date_type = None
#             elif (date_type=="DEAT"):
#                 indiv.death = g.args
#                 date_type = None
#             else:
#                 print "ERROR"
#
#     return indiv


if __name__ == '__main__':
    main()
