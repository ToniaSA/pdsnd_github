import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

day_dict = {'m':'monday','tu':'tuesday','w':'wednesday','th':'thursday','f':'friday','sa':'saturday','su':'sunday'}
month_dict = {'jan':'january','feb':'february','mar':'march','apr':'april','may':'may','jun':'june'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = "all"
    day = "all"
    flag = 0
    day_flag = 0
    month_flag = 0
    filter_flag = 0


    print('Hello! Let\'s explore some US bikeshare data!')


   # Select a valid city
    while flag == 0:
        city = input("What city would you like to explore?  Chicago, New York City or Washington? ").lower()
        goodcity = city in CITY_DATA
        if goodcity == True:
            flag=1
        else:
            print("Oopsie! City entered is not valid.  Please try again.")

   # Select a time filter.
    while filter_flag == 0:
        time_filter = input("Would you like to filter by month, day or both or not at all?  Type 'none' for no filter. : ").lower()
        if time_filter in ('month', 'day', 'both', 'none'):
            filter_flag = 1
            print(time_filter)
        else:
            print("Oopsie! Filter {} is not valid.  Please try again.".format(time_filter))

    if time_filter != 'none':
         # user input for month (all, january, february, ... , june)
        if time_filter == "month" or time_filter == "both":
            while month_flag == 0:
                month = input("Please enter month (Jan, Feb, Mar, Apr, May or Jun):  ").lower()
                good_month = month in month_dict
                if good_month ==True:
                    month_flag=1
                else:
                    print("Oopsie! Month entered is not valid.  Please try again.")
            # user input for day
        if time_filter == "day" or time_filter == "both":
            while day_flag ==0:
                day = input("Please enter a day (M, Tu, W, TH, F, Sa, Su):  ").lower()
                good_day = day in day_dict
                if good_day == True:
                    day_flag=1
                else:
                    print("Oopsie! Day entered is not valid.  Please try again.")
        else:
            nofilterchosen = "Ok. No filter chosen."
            print(nofilterchosen)

    if day != 'all':
        day = (day_dict[day])

    if month != 'all':
        month = (month_dict[month])


    print("\nFilters: City: {}    Month: {}    Day: {}".format(city,month,day).title())


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

# filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
# filter by month to create the new dataframe
        df = df[df['month'] == month]
# filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df,city,month,day):
    """Displays statistics on the most frequent times of travel.

       Args:
            (df) df - dataframe containing filtered data
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
       Returns:
            nothing
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print("\nFilters: City: {}    Month: {}    Day: {}".format(city,month,day).title())

    # Display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('\nMost popular travel month is: ',months[popular_month-1].title())

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0].title()
    print('\nMost popular travel day is: {}'.format(popular_day))

    # Display the most common start hour
    df['Start Time'] = pd.to_datetime(df[('Start Time')])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,city,month,day):
    """Displays statistics on the most popular stations and trip.
         Args:
            (df) df - dataframe containing filtered data
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            nothing
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print("\nFilters: City: {}    Month: {}    Day: {}".format(city,month,day).title())

    # Display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', most_popular_start_station)

    # Display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('Most Frequent End Station:', most_popular_end_station)

    # Display most frequent combination of start station and end station trip
    print("\nMost popular start and end station combination...")
    print(df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).nlargest(n=1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,city,month,day):
    """Displays statistics on the total and average trip duration.
        Args:
            (df) df - dataframe containing filtered data
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
       Returns:
            nothing
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print("\nFilters: City: {}    Month: {}    Day: {}".format(city,month,day).title())

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    #total_travel_time = (total_travel_time/60)/60
    print('Total travel time for all riders is {} hours.'.format((total_travel_time/60)/60))


    # Display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average travel time is (in minutes)',avg_travel_time/60)

    # Display trip duration groups.
    less_than_five = len(df[df['Trip Duration'] <= 300])
    print('Number of trips with less than 5 minutes duration: ',less_than_five)

    between_five_and_sixty = len(df[df['Trip Duration'].between(301,3600)])
    print('Number of trips between 5 and 60 minutes: ',between_five_and_sixty)

    between_one_and_ten_hrs = len(df[df['Trip Duration'].between(3601,36000)])
    print('Number of trips between 1 and 10 hours: ',between_one_and_ten_hrs)

    greater_than_ten_hrs = len(df[df['Trip Duration']>36000])
    print('Number of trips greater than 10 hours: ',greater_than_ten_hrs)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city,month,day):
    """Displays statistics on bikeshare users.
        Args:
            (df) df - dataframe containing filtered data
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            nothing
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nFilters: City: {}    Month: {}    Day: {}".format(city,month,day).title())
    print(df.groupby(['User Type']).size().sort_values(ascending=False).nlargest())


    # Display gender counts

    try:
        gender_count = df['Gender'].value_counts()

        print("\nCount by Gender: ")
        print(gender_count)
    except:
        print("No gender data available.")


   # Display earliest, most recent, and most common year of birth

    try:
        most_common_birthyear = df['Birth Year'].mode()
        most_common_birthyear = int(most_common_birthyear)
        print("\nThe majority of riders were born in the year: {}".format(most_common_birthyear))

        earliest_birthyear = int(min(df["Birth Year"]))
        print("\nThe earliest birth year is: {}".format(earliest_birthyear))

        most_recent_birthyear = int(max(df["Birth Year"]))
        print("\nThe most recent birth year is: {}".format(most_recent_birthyear))
    except:
        print("No user data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df,city,month,day):
    """Displays raw data rows.
        Args:
            (df) df - dataframe containing filtered data
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            nothing
    """

    start = 0
    line_interval = 5

    print('\nDisplaying raw data...\n')
    start_time = time.time()

    print("\nFilters: City: {}    Month: {}    Day: {}".format(city,month,day).title())

    number_of_rows = df.shape[0]
    print("Total number of rows:  ",number_of_rows)

    display_data = input("Would you like to see lines of raw data? Yes or No (default) ").lower()
    print(display_data)

    if display_data == 'y':
        display_data = 'yes'
    elif display_data == 'n':
        display_data = 'no'
    #allow user to set the number of data rows to display
    try:
        if display_data == 'yes':
            line_interval = int(input("What line interval do you prefer? Default is 5.  "))
            print("Line Interval = ", line_interval)
    except ValueError:
            line_interval = 5
            print("Line Interval = ", line_interval)

    while True:
        if display_data == 'yes' and start < number_of_rows:
            print(df.iloc[start:start+line_interval])
            start +=line_interval
            if start > number_of_rows:
                print("\nNo more rows to display.")
            else:
                display_data = input("Would you like to continue?  Yes or No (default)").lower()
                if display_data == 'y':
                    display_data = 'yes'
                elif display_data == 'n':
                    display_data = 'no'
        else:
            break


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():

    while True:
        city, month, day = get_filters()
        #Debug: confirm city, month, day values are passed correctly
        #print(city, " ",month," ",day)
        df = load_data(city, month, day)
        #Debug: print first 5 rows to ensure data is available and as expected
        #print(df.head())


        time_stats(df,city,month,day)
        station_stats(df,city,month,day)
        trip_duration_stats(df,city,month,day)
        user_stats(df,city,month,day)
        display_raw_data(df,city,month,day)

        restart = input('\nWould you like to restart? Enter yes or no (default).\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
