""" Python module for parsing GEDCOM geneaology files - user stories

    This file provides the user stories for the GEDCOM parsing project
"""

from datetime import datetime, timedelta

error_locations = []
anomaly_locations = []

def validation(individuals, families):
    """ Validation check to run all user stories """
    marriage_age(individuals, families)

    print "ERRORS/ANOMALIES".center(80, ' ')
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
    age_less_150(individuals)
    birth_before_marriage_of_parents(individuals, families)
    birth_before_death_of_parents(individuals, families)
    marriage_age(individuals, families)
    parents_not_too_old(individuals, families)
    no_bigamy(individuals, families)

    # Sprint 3
    no_sibling_marriage(individuals, families)
    no_marriage_to_decendants(individuals, families)


def report_error(etype, description, location):
    """ Reports an error to console """

    estr = 'ERROR {:5.5s}     {:55.55s} {}'\
        .format(etype, description, ','.join(location))
    for loc in location:
        error_locations.append(loc)
    print estr

def report_anomaly(atype, description, location):
    """ Reports an anomaly to console """

    astr = 'ANOMALY {:5.5s}     {:53.53s} {}'\
        .format(atype, description, ','.join(location))
    for loc in location:
        anomaly_locations.append(loc)
    print astr


### USER STORIES IN-ORDER BELOW ###

def dates_before_current(individuals, families):
    """ US01 All dates must be before the current date - ERROR"""

    return_flag = True
    error_type = "US01"
    # date of birth, death, marriage, or divorce must be before current date
    for family in families:
        if family.marriage and family.marriage > datetime.now():
            error_descrip = "Marriage occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            report_error(error_type, error_descrip, error_location)
            return_flag = False

        if family.divorce and family.divorce > datetime.now():
            error_descrip = "Divorce occurs after current date"
            error_location = [family.uid, family.husband, family.wife]
            report_error(error_type, error_descrip, error_location)
            return_flag = False

    for indiv in individuals:
        if indiv.birthdate and indiv.birthdate > datetime.now():
            error_descrip = "Birth occurs after current date"
            error_location = [indiv.uid]
            report_error(error_type, error_descrip, error_location)
            return_flag = False

        if indiv.death and indiv.death > datetime.now():
            error_descrip = "Death occurs after current date"
            error_location = [indiv.uid]
            report_error(error_type, error_descrip, error_location)
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
                report_error(error_type, error_descrip, error_location)
                return_flag = False

            if husband.birthdate and husband.birthdate > family.marriage:
                error_descrip = "Birth of husband occurs after marraige"
                error_location = [husband.uid]
                report_error(error_type, error_descrip, error_location)
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
                report_error(error_type, error_descrip, error_location)
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
                report_error(error_type, error_descrip, error_location)
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
                report_error(error_type, error_descrip, error_location)
                return_flag = False
            if husband.death is not None and family.marriage > husband.death:
                error_descrip = "Marriage occurs after death of husband"
                error_location = [family.uid, husband.uid]
                report_error(error_type, error_descrip, error_location)
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
                report_error(error_type, error_descrip, error_location)
                return_flag = False
            if husband.death is not None and family.divorce > husband.death:
                error_descrip = "Divorce occurs after death of husband"
                error_location = [family.uid, husband.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag


def age_less_150(individuals):
    """  US07 - Age should be less than 150 years for deceased and alive"""
    return_flag = True
    error_type = "US07"
    # For each decesaded individual check age if age is over 150
    for individual in individuals:
        if individual.death and individual.birthdate:
            if (individual.birthdate + timedelta(days=54750) < individual.death):
                error_descrip = "Individual dies over 150 years of age"
                error_location = [individual.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False

    #For each living individual, check age
    for individual in individuals:
        if individual.death is None and individual.birthdate:
            if (individual.birthdate + timedelta(days=54750) < datetime.now()):
                error_descrip = "Living Individual over 150 years old"
                error_location = [individual.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

#Should this be done based off of date of conception or birth?
#user story from team report says birthdate
def birth_before_marriage_of_parents(individuals, families):
    """ US08 - Birth should occur after the marriage of parents """
    return_flag = True
    anom_type = "US08"

    # Loop through individuals to compare their brithdate
    # with the marriage/divorce dates of their parents
    for individual in individuals:

        # Some individuals do not have parents defined
        # if they are the oldest generation in the gedcom file,
        # so check if individual.famc has elements before proceeding
        if len(individual.famc) > 0:

            # locate family of individual
            for family in families:
                if family.uid == individual.famc[0]:
                    # Checks for a child born before marriage
                    if family.marriage:
                        if family.marriage > individual.birthdate :
                            anom_description = "Child is born before marriage "
                            anom_location = [individual.uid, family.uid]
                            report_anomaly(anom_type, anom_description, anom_location)
                            return_flag = False
                    # checks for child born after divorce
                    if family.marriage and family.divorce:
                        if family.divorce < individual.birthdate :
                            anom_description = "Child is born after divorce "
                            anom_location = [individual.uid, family.uid]
                            report_anomaly(anom_type, anom_description, anom_location)
                            return_flag = False

    return return_flag


def birth_before_death_of_parents(individuals, families):
    """ US09 - Birth should occur before the death of parents """
    return_flag = True
    error_type = "US09"

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
            fam = None

            # Get the UID of parents for an individual
            for family in families:
                if family.uid == individual.famc[0]:
                    father_id = family.husband
                    mother_id = family.wife
                    fam = family
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
                error_location = [fam.uid, individual.uid]
                report_error(error_type, error_description, error_location)
                return_flag = False

            # Case when mother dies before birth of child.
            # This is impossible.
            if mother.death is not None and mother.death < individual.birthdate:
                error_descrip = "Child is born after death of mother"
                error_location = [fam.uid, individual.uid]
                report_error(error_type, error_descrip, error_location)
                return_flag = False
    return return_flag

def marriage_age(individuals, families):
    """ US10 - Marriage should be atleast 14 years after the birth
        of both spouses - ANOMALY
    """

    anom_type = "US10"
    return_flag = True

    curr_date = datetime.today()
    min_birt = datetime(curr_date.year-14,
        curr_date.month, curr_date.day)

    for family in families:
        husband = None
        wife = None
        for individual in individuals:
            if individual.uid == family.husband:
                husband = individual
            if individual.uid == family.wife:
                wife = individual
            # We have found both the husband and wife individuals
            if husband is not None and wife is not None:
                break

        if husband.birthdate > min_birt:
            anom_description = "Husband is married before 14 years old"
            anom_location = [family.uid, husband.uid]
            report_anomaly(anom_type, anom_description, anom_location)
            return_flag = False

        if wife.birthdate > min_birt:
            anom_description = "Wife is married before 14 years old"
            anom_location = [family.uid, wife.uid]
            report_anomaly(anom_type, anom_description, anom_location)
            return_flag = False
    return return_flag

def no_bigamy(individuals, families):
    """ US11 - Marriage should not occur during marriage to another spouse -
        ANOMALY
    """
         #for each fams check for divorce or death prior to next fam
    anom_type = "US11"
    return_flag = True

    for family in families:
        #check if husband is in any other families
        husband_uid = family.husband
        wife_uid = family.wife

        for fam_compare in families:
            # Make sure not comparing against self
            if fam_compare is family:
                continue

            if fam_compare.husband == husband_uid:
                if fam_compare.marriage > family.marriage:
                    wife = next(x for x in individuals if x.uid == family.wife)

                    # Family divorce should occur after or wife should die first
                    if ((family.divorce < fam_compare.marriage) or \
                        ((wife.death) and (wife.death < fam_compare.marriage))):

                        anomaly_description="Marriage occured before divorce or death from/of wife"
                        a_loc = [family.wife, fam_compare.wife, family.husband]
                        report_anomaly(anom_type,anomaly_description,a_loc)
                        return_flag = False

            if fam_compare.wife == wife_uid:
                if fam_compare.marriage > family.marriage:
                    husb = next(x for x in individuals if x.uid == family.husband)

                    # Family divorce should occur after or wife should die first
                    if ((family.divorce > fam_compare.marriage) or ((husb.death) and (husb.death < family.marriage))):
                        anomaly_description=\
                        "Marriage occured before divorce or death from/of husband"
                        a_loc = [family.husband, fam_compare.husband, family.wife]
                        report_anomaly(anom_type,anomaly_description,a_loc)
                        return_flag = False
    return return_flag


def parents_not_too_old(individuals, families):
    """ US12 - Mother should be less than 60 years older than her
    children and father should be less than 80 years older than his children -
    ANOMALY
    """

    anom_type = "US12"
    return_flag = True
    DAYS_IN_60_YEARS = 21900
    DAYS_IN_80_YEARS = 29200

    # Find all families with children
    #   (create a list of all fams with non empty children)
    fams_with_children = [x for x in families if x.children is not []]

    for family in fams_with_children:

        mother = next((x for x in individuals if x.uid == family.wife), None)
        father = next((x for x in individuals if x.uid == family.husband), None)

        children_uids = family.children

        for child_uid in children_uids:
            child = next((x for x in individuals if x.uid == child_uid), None)

            if mother and child: #This may be repetitive
                if (child.birthdate - mother.birthdate) > \
                        timedelta(DAYS_IN_60_YEARS):
                    anom_description = "Mother is 60 years older than child"
                    anom_location = [mother.uid, child.uid]
                    report_anomaly(anom_type, anom_description, anom_location)
                    return_flag = False

            if father and child: #This may be repetitive
                if (child.birthdate - father.birthdate) > \
                        timedelta(days=DAYS_IN_80_YEARS):
                    anom_description = "Father is 80 years older than child"
                    anom_location = [father.uid, child.uid]
                    report_anomaly(anom_type, anom_description, anom_location)
                    return_flag = False

    return return_flag


def no_marriage_to_decendants(individuals, families):
    """ US17- Parents should not marry any of their descendants - ANOMALY """
    anom_type = "US17"
    return_flag = True

    for family in families:
        decendants = []

        decendants.extend(family.children)
        for decendant in decendants:
            temp_decs = return_children(decendant, families)
            if temp_decs is not None:
                decendants.extend(temp_decs)

        if family.husband and family.wife and family.wife in decendants:
            anom_descrip = "Wife is decendant of spouse"
            anom_location = [family.wife, family.husband]
            report_anomaly(anom_type,anom_descrip, anom_location)
            return_flag = False

        if family.husband and family.wife and family.wife in decendants:
            anom_descrip = "Husband is decendant of spouse"
            anom_location = [family.wife, family.husband]
            report_anomaly(anom_type,anom_descrip, anom_location)
            return_flag = False

    return return_flag

def return_children(uid, families):
    """ Helper function for no_marriage_to_decendants """
    #find family where uid is a Parents
    family = next((x for x in families if x.husband == uid), None)
    if family is None:
        family = next((x for x in families if x.wife==uid), None)

    if family is None: #Is never a parent
        return None
    else:
        return family.children

def no_sibling_marriage(individuals, families):
    """ US18 - Siblings should not marry one another - ANOMALY """
    anom_type = "US18"
    return_flag = True

    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)

        for sibling in siblings:
            sib_fam = next((x for x in families if x.husband == sibling.uid), None)

            if sib_fam and sib_fam.wife in sibling_uids:
                anom_descrip = "Sibling is married to another sibling"
                anom_location = [sibling.uid, sib_fam.wife]
                report_anomaly(anom_type, anom_descrip, anom_location)
                return_flag = False

    return return_flag
