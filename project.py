"""
Abhika Mishra
CSE 163 AC

This file contains functions which look at datasets on
paid and unpaid work based on gender to analyze the relevance
and difference in time use around the world between Men and Women
This file has functions which clean and merge the data
"""


def merge(male, female):
    """
    merge takes two data sets for the two genders and merges
    the data by Country name with an inner join and returns
    the merged data
    """
    # filters male and female to include useful columns
    male = male[['Country', 'Year Men', 'Unpaid Men',
                 'Paid Men', 'Youngest Age Men']]
    female = female[['Country', 'Year Women', 'Unpaid Women',
                     'Paid Women', 'Youngest Age Women']]
    # merges data sets
    merged = male.merge(female, left_on='Country', right_on='Country')
    return merged


def categorize_unpaid(data, gender):
    """
    adds a column representing unpaid hours for the given gender
    using the given data set. returns the data with new column
    """
    # filters data to include only unpaid hours
    unpaid = (data['Time use'] == 'Unpaid domestic, care and volunteer work')
    result = data.copy()
    # saves unpaid column to data2
    data2 = data[unpaid]
    # creates new column
    result['Unpaid ' + gender] = data2[gender]
    return result[unpaid]


def categorize_paid(data, gender):
    """
    adds a column representing paid hours for the given gender
    using the given data set. returns the data with new column
    """
    # filters data to include only unpaid hours
    paid = (data['Time use'] == 'Paid and subsistence work')
    # saves data2 to include paid column only
    data2 = data[paid]
    result = data.copy()
    # creates new column
    result['Paid ' + gender] = data2[gender]
    return result[paid]


def youngest_age(string):
    """
    used to find the youngest age in string with format
    "Age:(integer)-(integer)". returns int value of smallest
    number in string given, if string has unkown age, then
    returns 0.
    """
    number = ''
    i = 4
    # checks to see if Age is unknown
    if(string != 'Age:Unknown age'):
        # adds number starting at 4th index till it
        # finds a dash or plus
        while (string[i] != '+') and (string[i] != '-'):
            number += string[i]
            i += 1
        return int(number)
    else:
        return 0


def adding_youngest_age(data, gender):
    """
    adds a column representing the youngest working age in
    given dataset for given gender. returns data with new column
    """
    # creates new column and applies youngest_age function
    data['Youngest Age ' + gender] = data['Age'].apply(youngest_age)
    return data


def extract_year(string):
    """
    returns the year survey was taken. if survey year
    is in format "yyyy-yy" then it returns the first
    year amongst the two
    """
    string = string[0:4]
    num = int(string)
    return num


def cleaning_year(data, gender):
    """
    creates a new column representing the year the data was taken
    and the given gender using the given data
    """
    # creates column with applying extract_year
    data['Year ' + gender] = data['Year'].apply(extract_year)
    return data


def clean_data_paid(data, gender):
    """
    cleans the data by adding new columns for categorical data
    respective to gender. helps to merge data of two genders.
    returns the cleaned and usable data with respect to paid hours
    """
    # creates data p with columns for year, age, and paid hours
    p = categorize_paid(data, gender)
    p = cleaning_year(p, gender)
    p = adding_youngest_age(p, gender)
    # creates data u with column for unpaid hours
    u = categorize_unpaid(data, gender)
    # merges the paid and unpaid data
    data = p.merge(u, left_on='Country', right_on='Country', how='outer')
    # returns the data with useful columns
    return data[['Country', 'Youngest Age ' + gender,
                 'Unpaid ' + gender, 'Paid ' + gender, 'Year ' + gender]]


def clean_data_unpaid(data, gender):
    """
    cleans the data by adding new columns for categorical data
    respective to gender. helps to merge data of two genders.
    returns the cleaned and usable data with respect to unpaid hours
    """
    # creates data u with columns for year, age, and unpaid hours
    u = categorize_unpaid(data, gender)
    u = cleaning_year(u, gender)
    u = adding_youngest_age(u, gender)
    # creates data p with column for paid hours
    p = categorize_paid(data, gender)
    # merges the two data sets
    data2 = u.merge(p, left_on='Country', right_on='Country', how='outer')
    # returns data with useful columns
    return data2[['Country', 'Youngest Age ' + gender,
                  'Unpaid ' + gender, 'Paid ' + gender, 'Year ' + gender]]
