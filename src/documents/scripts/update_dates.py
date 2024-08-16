import random
from datetime import datetime, timedelta


def random_date_between(start_date):
    # Convert the start_date string to a datetime object
    start_date = datetime.strptime(start_date, "%Y-%m-%d ")

    # Get the current date and time
    end_date = datetime.now()

    # Calculate the time difference between the start and end dates
    time_difference = end_date - start_date

    # Generate a random number of seconds within the time difference
    random_seconds = random.randint(0, int(time_difference.total_seconds()))

    # Calculate the random date by adding the random seconds to the start date
    random_date = start_date + timedelta(seconds=random_seconds)

    return random_date

# Example usage


def run():
    start_date = "2021-01-01"
    print(random_date_between(start_date))
