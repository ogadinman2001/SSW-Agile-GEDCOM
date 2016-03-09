""" Python module for parsing GEDCOM geneaology files - unit tests

    This file provides the unit tests for the GEDCOM parsing project
"""

import unittest
import os
from parser import parse_ged

# Add user stories after creation of test
from user_stories import dates_before_current, birth_before_marriage, \
    birth_before_death, marriage_before_divorce, marriage_before_death, \
    divorce_before_death, birth_before_death_of_parents, parents_not_too_old


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

    def test_birth_before_death_of_parents(self):
        """ Unit test for birth birth_before_death_of_parents"""

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
