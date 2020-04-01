import datetime
from word2number import w2n


def get_date_from_interpretation(interpretation):
    number = None
    hierarchy_number = None
    time_measures = None
    for entity in interpretation['entities']:

        if entity["entity"] == "hierarchy_number":
            hierarchy_number = entity["value"]

        elif entity["entity"] == "time":
            time_measures = entity["value"]

        elif entity["entity"] == "number":
            number = entity["value"]

    if number is None and hierarchy_number is None and time_measures is None:
        returned_response = "Query not fully understood, returning last week data by default:"
        hierarchy_number = "last"
        time_measures = "week"

    # count the number of unit of time measures
    counter = 1
    # convert the unit of time measures as days
    time_measure_factor = 1

    if (time_measures[0:4] == "week"):
        time_measure_factor = 7
    elif (time_measures[0:5] == "month"):
        time_measure_factor = 30
    elif (time_measures[0:4] == "year"):
        time_measure_factor = 365

    # e.g. last week
    if (hierarchy_number == "last" and number is None):
        counter = 1    
    # e.g last 2 weeks
    elif (hierarchy_number == "last" and number is not None):
        try:
            counter = int(number)
        except:
            counter = w2n.word_to_num(number)
    elif (number is not None):
        try:
            counter = int(number)
        except:
            counter = w2n.word_to_num(number)
    # e.g one month ago (we then check the date one month ago and move 7 days ahead)
    if (hierarchy_number != "last"):

        d_up = datetime.date.today() - datetime.timedelta(days=counter*time_measure_factor) + datetime.timedelta(days = 7)

    else:

        d_up = datetime.date.today() # to switch for interval of time

    d_down = d_up - datetime.timedelta(days=counter*time_measure_factor)

    return d_down, d_up, counter*time_measure_factor