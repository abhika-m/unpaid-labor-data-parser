"""
Abhika Mishra
CSE 163 AC

This file contains tests for functions in project.py which
looks at the disparity of time use in paid/unpaid work
based on gender and country. This file does not contain
a test for plot_change_in_time()
"""
from cse163_utils import assert_equals
import pandas as pd
from main import breakdown_work_gender, difference_in_hours_country
from main import child_labor
from project import merge, clean_data_paid


def test():
    """
    sets up and tests functions from project.py using
    assert_equals and print functions
    """
    # setting up data
    female = pd.read_csv('test_women.csv')
    male = pd.read_csv('test_men.csv')
    # cleans and saves data depending on time use
    mp = clean_data_paid(male, 'Men')
    fp = clean_data_paid(female, 'Women')
    # merges data
    data = merge(mp, fp)
    # set up for breakdown_work_gender
    bwg = {'Gender': ['Male', 'Female'],
           'Mean Unpaid Hours': [2, 4.8],
           'Mean Paid Hours': [5, 2.4]}
    manualbwg = pd.DataFrame(bwg)
    testingbwg = breakdown_work_gender(data)
    # set up for difference_in_hours_country
    dhc = {'Country': ['Country1'],
           'Mean Difference in Unpaid Hours (f-m)': [2.5],
           'Mean Difference in Paid Hours (f-m)': [-4.0]}
    manualdhc = pd.DataFrame(dhc)
    testingdhc = difference_in_hours_country(data, 'Country1')
    # testing breakdown_work_gender
    assert_equals(True, manualbwg.equals(testingbwg))
    # testing difference_in_hours_country
    assert_equals(True, manualdhc.equals(testingdhc))
    # testing child labor manually
    # should print 'Country3' and 'Country5'
    # with ages 5 and 10 respectively
    print(child_labor(data))


def main():
    """
    runs the test functions
    """
    test()


if __name__ == '__main__':
    main()':
    main()
