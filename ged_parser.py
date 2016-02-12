filename = 'rhousley_P02.ged'

valid_tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', \
    'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

def main():
    lines = [line.rstrip('\n\r') for line in open(filename)]

    for line in lines:
        line_listified = line.split(' ',)

        level = line_listified[0]
        tag = line_listified[1]
        args = line_listified[2:]

        # Do printing
        print line
        print level
        if (tag in valid_tags):
            print tag
        else:
            print "Invalid tag"


if __name__ == '__main__':
    main()
