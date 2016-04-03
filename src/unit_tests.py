""" Python module for parsing GEDCOM geneaology files - unit tests

    This file provides the unit tests for the GEDCOM parsing project
"""

import unittest
import os
from parser import parse_ged

# Add user stories after creation of test
from user_stories import dates_before_current, birth_before_marriage, \
    birth_before_death, marriage_before_divorce, marriage_before_death, \
    divorce_before_death, birth_before_death_of_parents, marriage_age, \
    parents_not_too_old, no_bigamy, age_less_150, \
    birth_before_marriage_of_parents, multiple_births_less_5, \
    no_sibling_marriage, no_marriage_to_decendants, \
    fewer_than_fifteen_siblings, male_last_names, \
    sibling_spacing

FAIL_DIR = "acceptance_files/fail/"
PASS_DIR = "acceptance_files/pass/"


class TestParser(unittest.TestCase):
    """ Unit tests to verift unit stories"""

    def test_dates_before_current(self):
        """ Unit test for dates_before_current"""

        acceptf = "date_before_current.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(dates_before_current(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(dates_before_current(individuals, families))
        else:
            print "!!test_date_before_current acceptance file not found"

    def test_birth_before_marriage(self):
        """ Unit test for birth_before_marriage"""

        acceptf = "birth_before_marriage.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(birth_before_marriage(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(birth_before_marriage(individuals, families))
        else:
            print "!!test_marriage_before_death acceptance file not found"

    def test_marriage_before_death(self):
        """ Unit test for marriage_before_death """

        acceptf = "marriage_before_death.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(marriage_before_death(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(marriage_before_death(individuals, families))
        else:
            print "!!test_marriage_before_death acceptance file not found"

    def test_divorce_before_death(self):
        """ Unit test for divorce_before_death """

        acceptf = "divorce_before_death.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(divorce_before_death(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(divorce_before_death(individuals, families))
        else:
            print "!!test_divorce_before_death acceptance file not found"

    def test_birth_before_death(self):
        """ Unit test for birth_before_death """

        acceptf = "birth_before_death.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, _ = parse_ged(pass_file)
            self.assertTrue(birth_before_death(individuals))
            individuals, _ = parse_ged(fail_file)
            self.assertFalse(birth_before_death(individuals))
        else:
            print "!!test_birth_before_death acceptance file not found"

    def test_marriage_before_divorce(self):
        """ Unit test for marriage_before_divorce """

        fail_file = FAIL_DIR + "marriage_before_divorce.ged"
        pass_file = PASS_DIR + "marriage_before_divorce.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            _, families = parse_ged(pass_file)
            self.assertTrue(marriage_before_divorce(families))
            _, families = parse_ged(fail_file)
            self.assertFalse(marriage_before_divorce(families))
        else:
            print "!!marriage_before_divorce acceptance file not found"

    def test_age_less_150(self):
        """ Unit test for age_less_150 """

        acceptf = "age_less_150.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, _ = parse_ged(pass_file)
            self.assertTrue(age_less_150(individuals))
        else:
            print "!!age_less_150 acceptance file not found"

        if os.path.exists(fail_file):
            individuals, _ = parse_ged(fail_file)
            self.assertFalse(age_less_150(individuals))
        else:
            print "!!age_less_150 acceptance file not found"

    def test_birth_before_marriage_of_parents(self):
        """ Unit test for birth_before_marriage_of_parents """

        acceptf = "birth_before_marriage_of_parents.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(
                birth_before_marriage_of_parents(individuals, families))
        else:
            print "!!birth_before_marriage_of_parents " \
                + "acceptance file not found"

        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(
                birth_before_marriage_of_parents(individuals, families))
        else:
            print "!!birth_before_marriage_of_parents " \
                + "acceptance file not found"

    def test_birth_before_death_of_parents(self):
        """ Unit test for birth birth_before_death_of_parents"""

        fail_file_father = FAIL_DIR + "birth_before_death" \
            + "_of_parents_FATHER.ged"
        fail_file_mother = FAIL_DIR + "birth_before_death" \
            + "_of_parents_MOTHER.ged"
        pass_file = PASS_DIR + "birth_before_death_of_parents.ged"

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(
                birth_before_death_of_parents(individuals, families))
        else:
            print "!!birth_before_death_of_parents acceptance file not found"

        if os.path.exists(fail_file_father):
            individuals, families = parse_ged(fail_file_father)
            self.assertFalse(
                birth_before_death_of_parents(individuals, families))
        else:
            print "!!birth_before_death_of_parents acceptance file not found"

        if os.path.exists(fail_file_mother):
            individuals, families = parse_ged(fail_file_mother)
            self.assertFalse(
                birth_before_death_of_parents(individuals, families))
        else:
            print "!!birth_before_death_of_parents acceptance file not found"

    def test_parents_not_too_old(self):
        """ Unit test for test_parents_not_too_old """

        acceptf = "parents_not_too_old.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(parents_not_too_old(individuals, families))
        else:
            print "!!parents_not_too_old acceptance file not found"

        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(parents_not_too_old(individuals, families))
        else:
            print "!!parents_not_too_old acceptance file not found"

    def test_marriage_age(self):
        """ Unit test for marriage_age """

        acceptf = "marriage_age.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(marriage_age(individuals, families))
        else:
            print "!!marriage_age acceptance file not found"

        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(marriage_age(individuals, families))
        else:
            print "!!marriage_age acceptance file not found"

    def test_no_bigamy(self):
        """ Unit test for no_bigamy """

        acceptf = "no_bigamy.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(no_bigamy(individuals, families))
        else:
            print "!!no_bigamy acceptance file not found"

        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(no_bigamy(individuals, families))
        else:
            print "!!no_bigamy acceptance file not found"

    def test_multiple_births_less_5(self):
        """ Unit test for multiple_births_less_5"""

        acceptf = "multiple_births_less_5.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(multiple_births_less_5(individuals, families))
        else:
            print "!!multiple_births_less_5 acceptance file not found"
        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(multiple_births_less_5(
                individuals, families))
        else:
            print "!!multiple_births_less_5 acceptance file not found"

    def test_sibling_spacing(self):
        """ Unit test for sibling_spacing"""

        acceptf = "sibling_spacing.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(sibling_spacing(individuals, families))
        else:
            print "!!sibling_spacing acceptance file not found"
        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(sibling_spacing(individuals, families))
        else:
            print "!!sibling_spacing acceptance file not found"

    def test_fewer_than_fifteen_siblings(self):
        """ Unit test for fewer_than_fifteen_siblings"""

        acceptf = "fewer_than_fifteen_siblings.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(fewer_than_fifteen_siblings(individuals, families))
        else:
            print "!!fewer_than_fifteen_siblings acceptance file not found"
        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(fewer_than_fifteen_siblings(
                individuals, families))
        else:
            print "!!fewer_than_fifteen_siblings acceptance file not found"

    def test_male_last_names(self):
        """ Unit test for male_last_names """

        acceptf = "male_last_names.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(male_last_names(individuals, families))
        else:
            print "!!male_last_names acceptance file not found"

        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(male_last_names(individuals, families))
        else:
            print "!!male_last_names acceptance file not found"

    def test_no_sibling_marriage(self):
        """ Unit test for no_sibling_marriage """

        acceptf = "no_sibling_marriage.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(no_sibling_marriage(individuals, families))
        else:
            print "!!no_sibling_marriage acceptance file not found"
        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(no_sibling_marriage(individuals, families))
        else:
            print "!!no_sibling_marriage acceptance file not found"

    def test_no_marriage_to_decendants(self):
        """ Unit test for no_marriage_to_decendants """

        acceptf = "no_marriage_to_decendants.ged"
        fail_file = FAIL_DIR + acceptf
        pass_file = PASS_DIR + acceptf

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(no_marriage_to_decendants(individuals, families))
        else:
            print "!!no_marriage_to_decendants acceptance file not found"
        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(no_marriage_to_decendants(individuals, families))
        else:
            print "!!no_marriage_to_decendants file not found"
