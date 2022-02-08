"""
Abhika Mishra
CSE 163 AC

This file contains functions which look at datasets on
paid and unpaid work based on gender to analyze the relevance
and difference in time use around the world between Men and Women
"""
import pandas as pd
import matplotlib.pyplot as plt
from project import clean_data_paid, clean_data_unpaid
from project import merge


def breakdown_work_gender(data):
    """
    returns a data frame which shows the mean unpaid
    and paid hours of men and women using the given
    data set
    """
    # saves unpaid/paid hour means in variable
    unpaid_men = data['Unpaid Men'].mean()
    paid_men = data['Paid Men'].mean()
    unpaid_women = data['Unpaid Women'].mean()
    paid_women = data['Paid Women'].mean()
    # creates a dictionary with gender column and mean values
    data_dict = {'Gender': ['Male', 'Female'], 'Mean Unpaid Hours':
                 [unpaid_men, unpaid_women], 'Mean Paid Hours':
                 [paid_men, paid_women]}
    # transforms dictionary to dataframe
    result = pd.DataFrame(data_dict)
    return result


def difference_in_hours_country(data, country):
    """
    returns the difference in mean hours (female - male)
    for unpaid and paid work based on given country and
    dataset
    """
    # filters data to include data from given country
    in_country = data['Country'] == country
    result = data[in_country]
    # stores mean hours of paid and unpaid work in variable
    unpaid_women = result['Unpaid Women'].mean()
    unpaid_men = result['Unpaid Men'].mean()
    # computes difference of mean hours and stores in variable
    unpaid_difference = unpaid_women - unpaid_men
    paid_difference = result['Paid Women'].mean() - result['Paid Men'].mean()
    # creates dictionary with columns for country and difference
    data_dict = {'Country': [country],
                 'Mean Difference in Unpaid Hours (f-m)': [unpaid_difference],
                 'Mean Difference in Paid Hours (f-m)': [paid_difference]}
    # transforms dictionary to dataframe
    result = pd.DataFrame(data_dict)
    return result


def child_labor(data):
    """
    returns a series of countries with child labor (younger than 15)
    along with the youngest working age in that country using the
    given dataset
    """
    # filters data to inclue ages 0-15 (exclusive)
    f_15 = data['Youngest Age Women'] < 15
    f_0 = data['Youngest Age Women'] > 0
    child_female = f_15 & f_0
    m_15 = data['Youngest Age Men'] < 15
    m_0 = data['Youngest Age Men'] > 0
    child_male = m_15 & m_0
    result = data[child_female & child_male]
    # groups data by country with minimum age
    result_men = result.groupby('Country')['Youngest Age Men'].min()
    result_women = result.groupby('Country')['Youngest Age Women'].min()
    # combines the men and women series
    result = result_men.combine(result_women, min)
    return result


def plot_helper(data, use, gender, country):
    """
    helper method for plot_change_in_time. it returns
    a filtered dataset with columns for country, year, time
    use, and gender.
    """
    result = data.copy()
    # filters data to include relevant columns
    result = result[result['Country'] == country]
    result = result[['Country', 'Year ' + gender, use + ' ' + gender]]
    # removes missing data
    result = result.dropna()
    return result


def plot_change_in_time(paid, unpaid, gender, country):
    """
    shows a line plot of the change in paid and unpaid hours for
    given gender and country over time using the data with information
    on paid and unpaid hours. saves the plot in format:
    (country)(gender).png
    """
    # uses helper method to filter paid and unpaid data
    p_data = plot_helper(paid, 'Paid', gender, country)
    u_data = plot_helper(unpaid, 'Unpaid', gender, country)
    # groups data based on year and finds mean hours
    p = p_data.groupby('Year ' + gender)['Paid ' + gender].mean()
    u = u_data.groupby('Year ' + gender)['Unpaid ' + gender].mean()
    # sets up figure and axes
    fig, ax = plt.subplots(1)
    # plots paid and unpaid plot
    p.plot(x='Year '+gender, y='Paid '+gender, color='c', ax=ax)
    u.plot(x='Year '+gender, y='Unpaid '+gender, color='m', ax=ax)
    # sets up legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    # adds title and labels
    plt.title('Unpaid and Paid Over Time ' + country + ' ' + gender)
    plt.xlabel('Year')
    plt.ylabel('Hours spent')
    # saves figure
    fig.savefig(country+gender+'.png')


def main():
    """
    runs all functions in main.py to find how relevant
    the disparity in paid and unpaid hours is by gender.
    """
    female = pd.read_csv('women_data.csv')
    male = pd.read_csv('men_data.csv')
    # cleans and saves data depending on time use
    mp = clean_data_paid(male, 'Men')
    fp = clean_data_paid(female, 'Women')
    mu = clean_data_unpaid(male, 'Men')
    fu = clean_data_unpaid(female, 'Women')
    # merges data
    data = merge(mp, fp)
    # finds breakdown of work based on gender using
    # merged data
    print(breakdown_work_gender(data))
    # finds the difference hours (f-m) of time use
    # based on country (Belgium and USA)
    print(difference_in_hours_country(data, 'Belgium'))
    print(difference_in_hours_country(data, 'United States of America'))
    print(difference_in_hours_country(data, 'Cuba'))
    # returns a series indicating countries which have child labor
    # including the youngest working age
    print(child_labor(data))
    # plots change in hours of time use over the years based on
    # indicated gender and country
    plot_change_in_time(fp, fu, 'Women', 'Chile')
    plot_change_in_time(mp, mu, 'Men', 'Canada')
    plot_change_in_time(fp, fu, 'Women', 'United States of America')
    plot_change_in_time(mp, mu, 'Men', 'Finland')


if __name__ == '__main__':
    main()
