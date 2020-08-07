import datetime
import random
import string
import itertools
import numpy


NUMBER_OF_MINUTES_IN_A_DAY = 1080  # (6am to 12am)


def get_random_alphanumeric_string():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits)
                          for i in range(10)))
    return result_str
    

def update_best_slots(queryset, best_slots):
    participant_free_slots = list(queryset)

    for i in participant_free_slots:
        if i.slot:
            best_slots[int(i.slot)]+=1

    return best_slots


def get_slots(slot_size):
    tuples_list = list()
    start_time = datetime.datetime.strptime('6:00', '%H:%M')
    end_time = datetime.datetime.strptime('23:59', '%H:%M')

    i = 0
    while start_time <= end_time:
        tuples_list.append(
            (i, str(start_time.time()) + " to " +
             str((start_time + datetime.timedelta(minutes=slot_size)).time()))
        )
        start_time += datetime.timedelta(minutes=slot_size)
        i = i + 1

    return tuples_list

def get_feasible_slots(slot_list, limit = 5):
    return numpy.argsort(-1* numpy.array(slot_list))[0:limit]


def flip_slots(slot_list, total_slots):
    flipped_slot_list = []
    for i in range(0, total_slots):
        if str(i) not in slot_list:
            flipped_slot_list.append(str(i))
    return flipped_slot_list