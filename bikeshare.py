import time
import pandas as pd
import numpy as np

pd.set_option('precision', 1) # Set the precision of our dataframes to one decimal place.
pd.set_option('display.max_columns', 200) # set to display all columns of raw data to the user

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    month = 'all'
    day = 'all'

    while True:
        try:
            city = input('\nWhat city data would you like to see? Chicago, New York City, Washington\n').lower()
            assert city in ['chicago', 'new york city', 'washington']
            break
        except AssertionError:
            print('\nWrong Input!!!\nType one of the city names')
        except (EOFError, KeyboardInterrupt):
            print('\nTry Again, No input taken')
            city = 'no_input'
            break

    while True:
        try:
            filter = input('\nWould you like to filter the data by month or day? Type "all" for no time filter\n').lower()
            assert filter in ['month', 'day', 'all']
            break
        except AssertionError:
            print('\nWrong Input!!!\nType month or day or all')
        except (EOFError, KeyboardInterrupt):
            print('\nTry Again, No input taken')
            filter = 'no_input'
            break

    if filter == 'no_input':
        month = 'no_input'
        day = 'no_input'

    if filter == 'month':
        # get user input for month (all, january, february, ... , june)
        while True:
            try:
                month = input('\nWhich month? January, February, March, April, May, or June. Please type the full month name\n').lower()
                assert month in ['january', 'february', 'march', 'april', 'may', 'june']
                break
            except AssertionError:
                print('\nWrong Input!!!\nType the full month name')
            except (EOFError, KeyboardInterrupt):
                print('\nTry Again, No input taken')
                month = 'no_input'
                break

    if filter == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. Please type the day name\n').lower()
                assert day in ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                break
            except AssertionError:
                print('\nWrong Input!!!\nType the day name')
            except (EOFError, KeyboardInterrupt):
                print('\nTry Again, No input taken')
                day = 'no_input'
                break

    # tell users what the filter is: city,month,day
    print('-'*40)
    if filter == 'all':
        print('The data you selected is for "{}" city with no time filter'.format(city.title()))
        print()
    if filter == 'month':
        print('The data you selected is for "{}" city, filtered by month "{}"'.format(city.title(), month.title()))
        print()
    if filter == 'day':
        print('The data you selected is for "{}" city, filtered by day("{}")'.format(city.title(), day.title()))
        print()
    if city  == 'no_input' or filter  == 'no_input' or month  == 'no_input' or day == 'no_input':
        print("You didn't provide one of the neccessary inputs. Please restart the program")
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
    df['day_of_week'] = df['Start Time'].dt.day_name() # .dt.weekday_name returns AtrributeError on my Local Machine

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


def time_stats(df):
    """Displays statistics on the most frequent or popular times of travel."""

    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_num = df['month'].mode()[0]
    # convert month_number to month_name
    months = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June'}
    popular_month = months[month_num]
    print('Most Popular Month of Travel: {}\n'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Travel: {}\n'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Hour of Travel: {}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: {}\n'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: {}\n'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['station_combination'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['station_combination'].mode()[0]
    print('Most Popular Trip from "Start Station" to "End Station": {}\n'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    stat = df['Trip Duration'].describe()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time in seconds: {}\n'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = stat['mean']
    print('Average Travel Time in seconds: {}\n'.format(mean_travel_time))

    min_travel_time = stat['min']
    print('Shortest Travel Time in seconds: {}\n'.format(min_travel_time))

    max_travel_time = stat['max']
    print('Longest Travel Time in seconds: {}\n'.format(max_travel_time))

    trip_count = stat['count']
    print('Total Trips: {}\n'.format(int(trip_count)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of Each User Type\nSubscriber: {}\nCustomer: {}\n'.format(user_types[0], user_types[1]))

    if city == 'chicago' or city == 'new york city' :
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('Counts of Each Gender\nMale: {}\nFemale: {}\n'.format(gender_count[0], gender_count[1]))

        # descriptive statistics for user type column
        stat = df['Birth Year'].describe()
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = stat['min']
        print('Earliest Year of Birth: {}\n'.format(int(earliest_birth_year)))

        latest_birth_year = stat['max']
        print('Most Recent Year of Birth: {}\n'.format(int(latest_birth_year)))

        common_birth_year = df['Birth Year'].mode()
        print('Most Common Year of Birth: {}\n'.format(int(common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def chunker(iterable, size, start=0):
    """
    Yield successive chunks from iterable of length size.

    input:
        size - the length of the chunks to be returned
        start - the start index of the first chunk, default value is zero
    """
    for i in range(start, len(iterable), size):
        yield iterable[i:i + size]


def raw_data(city):
    """ Display the city raw data to the user in chunks of 5 rows. """

    print('\nWould you like to see the {} raw data'.format(city))

    while True:
        try:
            display_city = input('(Enter yes or no): ').lower()
            assert display_city in ['yes', 'no']
            break
        except AssertionError:
            print('\nWrong Input! Type yes or no')
        except (EOFError, KeyboardInterrupt):
            print('\nTry Again, No input taken')
            display_city = ''
            break

    if display_city == 'yes':
        # load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])
        print('\n', df.head())

        for chunk in chunker(df, 5,start=5):

            while True:
                try:
                    print('\nWould you like to see the next 5 lines of {} raw data'.format(city))
                    display_chunk = input('(Enter yes or no): ').lower()
                    assert display_chunk in ['yes', 'no']
                    break
                except AssertionError:
                    print('\nWrong Input! Type yes or no')
                except (EOFError, KeyboardInterrupt):
                    print('\nTry Again, No input taken')
                    display_chunk = ''
                    break

            if display_chunk == 'yes':
                print(chunk)
            else:
                break
        if display_chunk == 'yes':
            print('-'*40)
            print("\nThere is no more raw data to display")


def main():
    while True:
        city, month, day = get_filters()

        if city  != 'no_input'  and month  != 'no_input' and day != 'no_input':
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            raw_data(city)

        while True:
            try:
                restart = input('\nWould you like to restart the program? Pick another city or change the filter\n(Enter yes or no): ').lower()
                assert restart in ['yes', 'no']
                break
            except AssertionError:
                print('\nWrong Input!!!\nType yes or no')
            except (EOFError, KeyboardInterrupt):
                print('\nTry Again, No input taken')
                restart = ''
                break

        if restart.lower() != 'yes':
            break


#### alternative way to display chunks
def alt():
    # import tabulate library to use the code
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df_default.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i+=5


if __name__ == "__main__":
	main()
