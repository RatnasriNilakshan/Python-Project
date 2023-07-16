import datetime


def covert_datetime(timestamp):
    # Convert the Unix timestamp to a datetime object
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)

    # Format the datetime object as a string
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    # Print the formatted datetime
    return formatted_datetime
