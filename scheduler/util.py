import datetime
import random
import string
from typing import Tuple

NUMBER_OF_MINUTES_IN_A_DAY = 1080  # (6am to 12am)


def get_random_alphanumeric_string():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits)
                          for i in range(10)))
    return result_str


def update_best_slots(participant_free_slots, best_slots):

    for i in range(participant_free_slots):
        if participant_free_slots[i] == 1:
            best_slots[i] = best_slots[i] + 1

    return best_slots


def get_slots(slot_size):
    tuples_list = list()
    start_time = datetime.datetime.strptime('6:00', '%H:%M')
    end_time = datetime.datetime.strptime('23:59', '%H:%M')

    while start_time <= end_time:
        tuples_list.append(
            (str(start_time.time()), str(start_time.time()) + " to " +
             str((start_time + datetime.timedelta(minutes=slot_size)).time()))
        )
        start_time += datetime.timedelta(minutes=slot_size)

    return tuples_list
