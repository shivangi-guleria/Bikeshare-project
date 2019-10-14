import time
import pandas as pd
import numpy as np

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
    #gets user input for city (chicago, new york city, washington).
    city=""
    while (True):
        city=input('\nEnter the city [Chicago / New York City / Washington] : ')
        city=city.lower()
        if ((city=='chicago') or (city=='new york city') or (city=='washington')):
            break
        else:
            print("Invalid input. Enter again\n")
    #gets user input for month 
    
    month=""
    months=["jan", "feb", "mar", "apr", "may","june"] 
    filtermonth=input("\nDo you want to filter by month? yes or no: " )
    if filtermonth.lower()== "yes":
        while month not in months:
            month=input('Enter month [jan, feb, mar, apr, may or june] : ')
            month=month.lower() 
            if month not in months:
                print("Invalid input\n")
    elif filtermonth.lower()== "no":
        month="all"
    else:
        print('I\'ll take it as a "no".\n')
        month="all"

    #gets user input for day of week 
    
    day=""
    days=["mon", "tue", "wed", "thu", "fri", "sat", "sun"] 
    filterday=input("\nDo you want to filter by day? yes or no: ")
    if filterday.lower()== "yes":
        while day not in days:
            day=input('Enter day [mon, tue, wed, thu, fri, sat or sun] : ')
            day=day.lower() 
            if day not in days:
                print("Invalid input\n")
    elif filterday.lower()== "no":
        day="all"
    else:
        print('I\'ll take it as a "no".\n')
        day="all"
    print("\n")          
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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extracts month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

   
    if month != 'all':
        # index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1

        # filters by month to create the new dataframe
        df = df[df['month'] == month]

    # filters by day of week
    if day != 'all':
        # filters by day of week to create the new dataframe
        days={"mon":"Monday", "tue" :"Tuesday", "wed":"Wednesday", "thu":"Thursday", "fri":"Friday","sat":"Saturday","sun":"Sunday"}
        df = df[df['day_of_week'] == days[day]]
    
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #displays the most common month
    months=["January", "February", "March", "April", "May", "June"]
    print("Most common month of travel: ",months[int(df['month'].mode())-1])
    
    #displays the most common day of week
    print("Most common day of travel: ", df['day_of_week'].mode()[0])

    #displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common start hour: ",df['hour'].mode()[0])

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #displays most commonly used start station
    print('Most popular start station is: ', df['Start Station'].mode()[0])

    #displays most commonly used end station
    print('Most popular end station is: ', df['End Station'].mode()[0])

    #displays most frequent combination of start station and end station trip
    df['journey'] = df['Start Station'].map(str) + " to " + df['End Station'].map(str)
    print('Most popular trip is: From ', df['journey'].mode()[0])

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n\nCalculating Trip Duration...\n')
    start_time = time.time()

    #displays total travel time
    minutes,seconds = divmod(int(df['Trip Duration'].sum()),60)
    hours,minutes=divmod(minutes,60)
    days,hours= divmod(hours,24)
    print("Total travel time is: {}days {}h {}m {}s ".format(days,hours,minutes,seconds))
    
    #display mean travel time
    minutes,seconds = divmod(int(df['Trip Duration'].mean()),60)
    print("Mean travel time is: {}m {}s ".format(minutes,seconds))
    
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n\nCalculating User Stats...\n')
    start_time = time.time()

    #Displays counts of user types
    
    print("\nBased on the user type:\n")
    print(df['User Type'].value_counts())
    print("Total:   ",df['User Type'].count())

    #Displays counts of gender
    
    print("\n\nBased on the users\' gender:\n")
    try:
        print(df['Gender'].value_counts())
    except:
        print("No gender data to share\n")
        
        
    # Displays earliest, most recent, and most common year of birth
    print("\n\nBased on the users\' birth year:\n")
    try:
        print("Most earliest year of birth: ", df['Birth Year'].min())
        print("Most recent year of birth: ", df['Birth Year'].max())
        print("Most common birth year: " , df['Birth Year'].mode()[0])
    except:
        print("No birth year to share.\n")

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df,i):
    print(df.iloc[i:i+5])    
    
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        s1=input("\nDisplay time stats? yes or no: ")
        if s1.lower()=="yes":    
            time_stats(df)
        s2=input("\nDisplay station stats? yes or no: ")
        if s2.lower()=="yes":    
            station_stats(df)
        s3=input("\nDisplay trip duration stats? yes or no: ")
        if s3.lower()=="yes":    
            trip_duration_stats(df)
        s4=input("\nDisplay user stats? yes or no: ")
        if s4.lower()=="yes":    
            user_stats(df)
        s5="yes"
        i=0
        while s5.lower()=="yes":     
            s5 = input("\nWould you like to display raw data of some users? yes or no: ")
            if s5.lower()=="yes":
                raw_data(df,i)
                i+=5
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
