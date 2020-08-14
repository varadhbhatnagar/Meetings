import datetime
from random import randint
import numpy
from hashids import Hashids


def get_hash():
    r1 = randint(0, 5000)
    r2 = r1 * randint(0,10) + randint(0, 5000)
    hashids = Hashids(salt='meetings is cool', min_length=10)
    hash = hashids.encode(int(r2))
    return hash
    

def update_current_suitable_slots(queryset, best_slots):
    participant_free_slots = list(queryset)

    for i in participant_free_slots:
        if i.slot:
            best_slots[int(i.slot)]+=1

    return best_slots


def get_slot_choices(slot_size):
    tuples_list = list()
    start_time = datetime.datetime.strptime('8:00', '%H:%M')
    end_time = datetime.datetime.strptime('23:59', '%H:%M')

    i = 0
    while start_time + datetime.timedelta(minutes=slot_size) < end_time:
        tuples_list.append(
            (i, str(start_time.time()) + " to " +
             str((start_time + datetime.timedelta(minutes=slot_size)).time()))
        )
        start_time += datetime.timedelta(minutes=30)
        i = i + 1

    return tuples_list, i


def get_most_suitable_slots(slot_list, limit = 5):
    return numpy.argsort(-1* numpy.array(slot_list), kind='stable')[0:limit]


def flip_slots(slot_list, total_slots):
    flipped_slot_list = []
    for i in range(0, total_slots):
        if str(i) not in slot_list:
            flipped_slot_list.append(str(i))
    return flipped_slot_list