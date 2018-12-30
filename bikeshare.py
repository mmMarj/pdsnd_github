import pandas as pd
import statistics as st
import datetime as dt

from colorama import Fore, Style
# I found information about colorama on pypi.com .

# Creating a function for reverse search in dictionary.
# I found help for this function on thispointer.com .


def get_keys_by_value(dictionary, searched_value):
    list_of_keys = list()
    list_of_items = dictionary.items()
    for item in list_of_items:
        if item[1] == searched_value:
            list_of_keys.append(item[0])
    return list_of_keys;


# Creating a function for handling cases of several "most popular" values.


def multiple_mode(list_mult_mode):
    mode_dict = {}
    for x in list_mult_mode:
        if x not in mode_dict:
            mode_dict[x] = 1
        else:
            mode_dict[x] += 1
    modes = get_keys_by_value(mode_dict,max(mode_dict.values()))
    modes = ','.join(modes[:-1]) + ' and ' + modes[-1]
    return modes;


# Creating a function to display "most popular" statistics.


def most_pop(analyzed_column, name_for_output):
    try:
        print('The most popular {} was {}.'
          .format(name_for_output, st.mode(analyzed_column)))
    except st.StatisticsError:
        print('The most popular {}s were {}.'
          .format(name_for_output, multiple_mode(analyzed_column)))

# Asking for user input.

def main():
    while True:

        # User input: city.
        city = str(input('Which city should we focus on? \n'
                         'Chicago, New York City or Washington? '))
        city = city.lower()
        # As requested in the review I improved the handling of input

        if city not in ('chicago', 'new york city', 'washington'):
            while city not in ('chicago', 'new york city', 'washington'):
                if city in ('new york', 'nyc'):
                    city = 'new york city'
                    break
                elif city in ('dc', 'washinton'):
                    city = 'Washington'
                    break
                else:
                    print(Fore.RED + '\nPlease make sure you are selecting one'
                          'of the available cities.' + Style.RESET_ALL)
                    city = str(input('Chicago, New York City or Washington? '))
                    continue
        city = city.title()

        # User input: month.
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July']
        month = str(input ('Which month do you want to analyze? \n'
                           'Type a month between January and June, or leave '
                           'blank: '))
        month = month.lower()
        month = month.title()

        if month not in months:
            while month not in months:
                print(Fore.RED + '\nSorry this is not a valid input. Please '
                      'make sure you are selecting a month between January and'
                      ' June.'+ Style.RESET_ALL)
                month = str(input('Type a month, or press enter to proceed '
                                  'without filtering: '))
                month = month.title()
                if month in months:
                    break
                else:
                    continue

        month = months.index(month)

        # User input: day.
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
        day = str(input('Which day of the week do you want to analyze? \n'
                        'Type a day or leave blank: '))
        day = day.lower()
        day = day.title()

        if day not in days and day != '':
             while day not in days:
                 print(Fore.RED + '\nSorry this is not a valid input.'
                       + Style.RESET_ALL)
                 day = str(input('Please type a day of the week, or press '
                                 'enter to proceed without filtering: '))
                 day = day.title()
                 if day in days or day == '':
                     break
                 else:
                     continue

        # Creating a filter variable to account for all cases.
        if month == 0 and day == '':
            filter_type = 1
            filter_text = ', not filtered by month or day'

        elif month == 0:
            filter_type = 2
            filter_text = ' on ' + day + 's, not filtered by month}'

        elif day == '':
            filter_type = 3
            filter_text = ' in ' + months[month] + ', not filtered by day'

        else:
            filter_type = 4
            filter_text = ' on ' + day + 's in ' + months[month]

        print(Fore.CYAN + '\nYou asked to see the data for {}{}.\n'
              .format(city, filter_text))

        # loading the required dataset.
        datasets = {'Chicago': 'chicago.csv',
                    'New York City': 'new_york_city.csv',
                    'Washington': 'washington.csv'}
        df = pd.read_csv(datasets[city])

        # Creating new columns required for all the statistics.
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['Start Month'] = df['Start Time'].dt.month
        df['Start Day of Week'] = df['Start Time'].dt.weekday_name

        # Applying the required filters
        if month != 0:
            df = df[df['Start Month'] == month]

        if day in days:
            df = df[df['Start Day of Week'] == day.title()]

        # Creating new columns for statistics.
        # This is placed after the filters so that it applies only
        # to selected rows.

        df['Start Month (Text)'] = pd.to_datetime(df['Start Month'],
           format='%m').dt.month_name()
        df['Start Hour'] = df['Start Time'].dt.hour
        df['Route'] = df['Start Station'] + ' to ' + df['End Station']

        # Compute and display statistics on time of rental.
        print(Fore.CYAN + Style.DIM + 'First, some information about the '
              'distribution of rentals:' + Style.RESET_ALL)

        # Most popular month.
        # This is not displayed if a month filter is selected.
        if filter_type == 1 or filter_type == 2:
            most_pop(df['Start Month (Text)'], 'month')

        # Most popular day of the week.
        # This is not displayed if a day filter is selected.

        if filter_type == 1 or filter_type == 3:
            most_pop(df['Start Day of Week'], 'day')

        # Most popular hour.
        most_pop(df['Start Hour'], 'hour')

        # Compute and display statistics on routes.
        print(Fore.CYAN + Style.DIM + '\nNow some information about the most '
              'popular routes:' + Style.RESET_ALL)

        # Most popular starting station.
        most_pop(df['Start Station'], 'start station')

        # Most popular ending station.
        most_pop(df['End Station'], 'end station')

        # Most popular route.
        most_pop(df['Route'], 'route')

        # Compute and display statistics on trip duration.
        print(Fore.CYAN + Style.DIM + '\nLet\'s see some statistics about '
              'travel time:' + Style.RESET_ALL)

        # Total travel time.
        sum_duration = df['Trip Duration'].sum()
        sum_duration_days = sum_duration / 86400
        print('The bikes were rented for a total of {} seconds. That\'s more '
              'than {:.0f} days!'.format(sum_duration, sum_duration_days))

        # Average travel time.
        avg_duration = df['Trip Duration'].mean()
        avg_duration_seconds = avg_duration % 60
        avg_duration_minutes = int((avg_duration - avg_duration_seconds) / 60)

        if avg_duration_seconds >= 59.5:
            print('On an average, bikes were rented for a period of {:.0f} '
                  'minutes.'.format(avg_duration_minutes+1))
        elif avg_duration_seconds == 0:
            print('On an average, bikes were rented for a period of {:.0f} '
                  'minutes.'.format(avg_duration_minutes))
        else:
            print('On an average, bikes were rented for a period of {:.0f} '
                  'minutes and {:.0f} seconds.'.format(avg_duration_minutes,
                   avg_duration_seconds))

        # Compute and display statistics on users.
        print(Fore.CYAN + Style.DIM + '\nFinally, some statistics about users:'
              + Style.RESET_ALL)

        # Distribution of user type.
        user_types = df['User Type'].value_counts()
        total_users = df['User Type'].count()
        print('We counted a total of {} users: {} subscribers ({:.2f}%) and {}'
              ' customers ({:.2f}%).'.format(total_users, user_types[0],
               user_types[0] / total_users * 100, user_types[1],
               user_types[1] / total_users * 100))

        # There is no data about gender and year of birth for Washington, so
        # if this city is selected there is no further statistics to present
        if city == 'Washington':
            print('Unfortunately we could not collect further data on users in'
                  ' Washington.')
        else:
        # Distribution of gender.
            user_gender = df['Gender'].value_counts()
            total_gender = df['Gender'].count()
            print('We collected gender information from {} users: {} were male'
                  '({:.2f}%) and {} female ({:.2f}%).'.format(total_gender,
                   user_gender[0], user_gender[0] / total_gender * 100,
                   user_gender[1], user_gender[1] / total_gender * 100))

        # Extremes and mode of year of birth.
            print('The oldest user was born in {:.0f}, the youngest in {:.0f}.'
                  .format(df['Birth Year'].min(), df['Birth Year'].max()))

            print('The most common year of birth among users is {:.0f}.'
                  .format(df['Birth Year'].mode()[0]))

        # Offering to see some raw data.

        raw = str(input('Do you want to see some examples of raw data ? '))
        raw = raw.lower()

        # Treating potential wrong inputs for the "raw data" question.
        if raw not in ('yes', 'y', 'no', 'n'):
             while raw not in ('yes', 'y', 'no', 'n'):
                 print(Fore.RED + '\nSorry this is not a valid input.'
                       + Style.RESET_ALL)
                 raw = str(input('Do you want to see some examples of raw '
                                 'data ? '))
                 raw = raw.lower()
                 if raw in ('yes', 'y', 'no', 'n'):
                     break
                 else:
                     continue

        if raw in ('yes', 'y'):
            # Using the filter variable to display an adequate introduction.
            if filter_type == 1:
                raw_text = ''

            elif filter_type == 2:
                raw_text = ' on {}s'.format(day)

            elif filter_type == 3:
                raw_text = ' in {}'.format(months[month])

            else:
                raw_text = ' in {} on {}s'.format(months[month], day)

            print(Fore.MAGENTA + '\nHere are five examples of rentals in {}{}:'
                  .format(city, raw_text))

            # Creating new columns for a nicer presentation of raw data.
            df['Start Minute'] = df['Start Time'].dt.minute
            df['End Hour'] = df['End Time'].dt.hour
            df['End Minute'] = df['End Time'].dt.minute
            df['Start Date'] = df['Start Time'].dt.day
            df['End Day of Week'] = df['End Time'].dt.weekday_name
            df['End Date'] = df['End Time'].dt.day
            df['End Month'] = df['End Time'].dt.month
            df['End Month (Text)'] = (pd.to_datetime(df['End Month'],
               format='%m').dt.month_name())
            df.fillna('',inplace=True)
            ex_index = 0
            ex_index_max = ex_index + 5

            # Displaying 5 examples of raw data.
            while ex_index < ex_index_max:
                try:
                    if city == 'Washington':
                        gender = ''
                    else:
                        gender = df.iloc[ex_index, 7]
                        gender = gender.lower()
                    user_type = df.iloc[ex_index, 6]
                    user_type = user_type.lower()

                    if (df.iloc[ex_index, -5] == df.iloc[ex_index, -3] and
                        df.iloc[ex_index, -13] == df.iloc[ex_index, -2]):
                            return_date = ('the same day')
                    else:
                        return_date = ('{} {} {}'.format(df.iloc[ex_index, -4],
                                       df.iloc[ex_index, -2], df.iloc[ex_index,
                                       -3]))
                # error message when all examples have been seen
                except IndexError or ValueError:
                    print(Fore.MAGENTA + '\nOups! You have already seen all '
                          'the available examples.' + Style.RESET_ALL)
                    break

                else:
                    print(Fore.MAGENTA + '\nExample {}:'.format(ex_index + 1)
                          + Style.RESET_ALL)
                    print('A {} {} rented a bike at {} on {} {} {:.0f} at '
                          '{:02d}:{:02.0f} and returned it at {} on {} at '
                          '{:02d}:{:02.0f}.'.format(gender, user_type,
                           df.iloc[ex_index, 4], df.iloc[ex_index,-12],
                           df.iloc[ex_index, -9], df.iloc[ex_index, -5],
                           df.iloc[ex_index, -10], df.iloc[ex_index, -8],
                           df.iloc[ex_index, 5], return_date,
                           df.iloc[ex_index, -7], df.iloc[ex_index, -6]))
                    ex_index += 1

                    if ex_index < ex_index_max:
                        continue

                    else:
                        # Offering to see 5 more examples.
                        more = str(input(Fore.MAGENTA + 'Would you like to'
                                         ' see more examples? '
                                         + Style.RESET_ALL))
                        more = more.lower()

                        # Handling incorrect input.
                        if more not in ('yes', 'y', 'no', 'n'):
                            while more not in ('yes', 'y', 'no', 'n'):
                                print(Fore.RED + '\nSorry this is not a valid '
                                      'input.' + Style.RESET_ALL)
                                more = str(input('Would you like to see more '
                                                 'examples? '))
                                more = more.lower()
                                if more in ('yes', 'y', 'no', 'n'):
                                    break

                                else:
                                    continue

                        if more in ('yes', 'y'):
                            print(Fore.MAGENTA + '\nHere are five more '
                                  'examples of rentals in {}{}:'.format(city,
                                                          raw_text))

                            ex_index_max = ex_index + 5
                            continue

        # Offering to restart
        restart = str(input('Do you want to see another set of data? '))
        restart = restart.lower()
        while restart not in ('yes', 'y', 'no', 'n'):
            print(Fore.RED + '\nSorry this is not a valid input.'
                  + Style.RESET_ALL)
            restart = str(input('Do you want to see another set of data? '))
            restart = restart.lower()
            if restart in ('yes', 'y', 'no', 'n'):
                 break
            else:
                continue

        if restart in ('no', 'n'):
            print(Fore.CYAN + '\nBye!' + Style.RESET_ALL)
            break;


if __name__ == "__main__":
    main()
