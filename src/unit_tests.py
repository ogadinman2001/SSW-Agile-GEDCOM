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
    birth_before_marriage_of_parents, no_sibling_marriage, \
    no_marriage_to_decendants


class TestParser(unittest.TestCase):
    """ Unit tests to verift unit stories"""

    def test_dates_before_current(self):
        """ Unit test for dates_before_current"""

        fail_file = "acceptance_files/fail/date_before_current.ged"
        pass_file = "acceptance_files/pass/date_before_current.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(dates_before_current(individuals, families))
            individuals, families = parse_ged(fail_file)
            self.assertFalse(dates_before_current(individuals, families))
        else:
            print "!!test_date_before_current acceptance file not found\n\n"

    def test_birth_before_marriage(self):
        """ Unit test for birth_before_marriage"""

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
        """ Unit test for marriage_before_death """

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
        """ Unit test for divorce_before_death """

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
        """ Unit test for birth_before_death """

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
        """ Unit test for marriage_before_divorce """

        fail_file = "acceptance_files/fail/marriage_before_divorce.ged"
        pass_file = "acceptance_files/pass/marriage_before_divorce.ged"

        if os.path.exists(fail_file) and os.path.exists(pass_file):
            _, families = parse_ged(pass_file)
            self.assertTrue(marriage_before_divorce(families))
            _, families = parse_ged(fail_file)
            self.assertFalse(marriage_before_divorce(families))
        else:
            print "!!marriage_before_divorce acceptance file not found\n\n"

    def test_age_less_150(self):
        """ Unit test for age_less_150 """
        fail_file = "acceptance_files/fail/age_less_150.ged"
        pass_file = "acceptance_files/pass/age_less_150.ged"

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(age_less_150(individuals))
        else:
            print "!!age_less_150 acceptance file not found"

        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(age_less_150(individuals))
        else:
            print "!!age_less_150 acceptance file not found"

    def test_birth_before_marriage_of_parents(self):
        """ Unit test for birth_before_marriage_of_parents """
        fail_file = "acceptance_files/fail/birth_before_marriage_of_parents.ged"
        pass_file = "acceptance_files/pass/birth_before_marriage_of_parents.ged"

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(birth_before_marriage_of_parents(individuals, families))
        else:
            print "!! birth_before_marriage_of_parents acceptance file not found"

        if os.path.exists(fail_file):
            individuals, families = parse_ged(fail_file)
            self.assertFalse(birth_before_marriage_of_parents(individuals, families))
        else:
            print "!! birth_before_marriage_of_parents acceptance file not found"

    def test_birth_before_death_of_parents(self):
        """ Unit test for birth birth_before_death_of_parents"""

        # fail_file_father_anomaly = "acceptance_files/fail/birth_before_death" \
        #     + "_of_parents_FATHER_anomaly.ged"
        fail_file_father = "acceptance_files/fail/birth_before_death" \
            + "_of_parents_FATHER.ged"
        fail_file_mother = "acceptance_files/fail/birth_before_death" \
            +"_of_parents_MOTHER.ged"
        pass_file = "acceptance_files/pass/birth_before_death_of_parents.ged"

        if os.path.exists(pass_file):
            individuals, families = parse_ged(pass_file)
            self.assertTrue(birth_before_death_of_parents(individuals, families))
        else:
            print "!!birth_before_death_of_parents acceptance file not found\n\n"

        if os.path.exists(fail_file_father):
            individuals, families = parse_ged(fail_file_father)
            self.assertFalse(birth_before_death_of_parents(individuals, families))
        else:
            print "!!birth_before_death_of_parents acceptance file not found\n\n"

        if os.path.exists(fail_file_mother):
            individuals, families = parse_ged(fail_file_mother)
            self.assertFalse(birth_before_death_of_parents(individuals, families))
        else:
            print "!!birth_before_death_of_parents acceptance file not found\n\n"

    def test_parents_not_too_old(self):
        """ Unit test for test_parents_not_too_old """

        fail_file = "acceptance_files/fail/parents_not_too_old.ged"
        pass_file = "acceptance_files/pass/parents_not_too_old.ged"

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
        fail_file = "acceptance_files/fail/marriage_age.ged"
        pass_file = "acceptance_files/pass/marriage_age.ged"

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

        fail_file = "acceptance_files/fail/no_bigamy.ged"
        pass_file = "acceptance_files/pass/no_bigamy.ged"

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

    def test_no_sibling_marriage(self):
        """ Unit test for no_sibling_marriage """

        fail_file = "acceptance_files/fail/no_sibling_marriage.ged"
        pass_file = "acceptance_files/pass/no_sibling_marriage.ged"

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

        fail_file = "acceptance_files/fail/no_marriage_to_decendants.ged"
        pass_file = "acceptance_files/pass/no_marriage_to_decendants.ged"

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
