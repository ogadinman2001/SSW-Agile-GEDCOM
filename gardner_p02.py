# Bryan Gardner
# P02

DATA = "gedcom.ged"
VALID_TAGS = [
    "INDI",
    "NAME",
    "SEX",
    "BIRT",
    "DEAT",
    "FAMC",
    "FAMS",
    "FAM",
    "MARR",
    "HUSB",
    "WIFE",
    "CHIL",
    "DIV",
    "DATE",
    "HEAD",
    "TRLR",
    "NOTE"
]

gedcom = open(DATA, "r").read().split("\n")

for g in gedcom:
    print g
    line = g.strip().split(" ")

    if len(line) < 2:
        continue

    print line[0]
    if line[0] == "0":
        if line[1] in VALID_TAGS:
            print line[1]
        elif len(line) > 2 and line[2] in VALID_TAGS:
            print line[2]
        else:
            print "Invalid tag"
    elif line[1] in VALID_TAGS:
        print line[1]
    else:
        print "Invalid tag"
