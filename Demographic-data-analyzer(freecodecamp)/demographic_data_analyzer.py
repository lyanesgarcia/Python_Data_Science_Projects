import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    df_Males = df[df['sex'] == 'Male']
    average_age_men = round(df_Males['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    people_Bachelor = df[df['education'] == 'Bachelors'].count()
    percentage_bachelors = round(people_Bachelor['education'] / df['education'].count() * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    people_Advanced = df[(df['education'] == 'Bachelors') | (df['education'] == 'Masters') | (df['education'] == 'Doctorate')]

    people_Advanced_more_50K = df[((df['education'] == 'Bachelors') | (df['education'] == 'Masters') | (df['education'] == 'Doctorate')) & (df['salary'] == '>50K')]

    people_Lower_more_50K = df[(df['education'] != 'Bachelors') & (df['education'] != 'Masters') & (df['education'] != 'Doctorate') & (df['salary'] == '>50K')]

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = people_Advanced['education'].count()
    lower_education = df['education'].count() - higher_education

    # percentage with salary >50K
    higher_education_rich = round((people_Advanced_more_50K['education'].count() / higher_education * 100) , 1)
    lower_education_rich = round((people_Lower_more_50K['education'].count() / lower_education * 100), 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    group_min_hours_more_50K = df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')]
    
    num_min_workers = df[df['hours-per-week'] == min_work_hours]

    rich_percentage = int(group_min_hours_more_50K['hours-per-week'].count() / num_min_workers['hours-per-week'].count() * 100)

    # What country has the highest percentage of people that earn >50K?
    country_more_50K = df.groupby('native-country')['salary'].apply((lambda x: (x=='>50K').sum())).reset_index(name='count')
    
    country_people = df.groupby('native-country', as_index=False).count()
    
    max_percentage = (country_more_50K['count'] / country_people['age']*100)
    country = pd.concat([country_more_50K, max_percentage], axis = 1)
 
    highest_earning_country = (country['native-country'][country[0] == max_percentage.max()].to_string(index=False)).strip()
     
    highest_earning_country_percentage = round(float(country[0][country[0] == max_percentage.max()].to_string(index=False)), 1)


    # Identify the most popular occupation for those who earn >50K in India.
    India_occupations = df['occupation'][(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    values_occupation = India_occupations.value_counts().keys()

    top_IN_occupation = values_occupation[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
