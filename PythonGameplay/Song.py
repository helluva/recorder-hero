import csv
import note
from enum import Enum

class Difficulty(Enum):
    EASY = 4.0
    MEDIUM = 2.0
    HARD = 1.0

class Song(Enum):
    Hot_Cross_Buns = 1
    Party_Rock_Anthem_by_LMFAO = 2


def timed_finger_positions_for_song(song, difficulty):
    with open('songs/' + song.name.replace("_", " ") + '.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    timed_finger_positions = []
    previous_time = 0.0
    delay_before_start = 5.0

    for line in data:
        note_type = line[0]
        note_length = float(line[1])

        note_time = (previous_time * difficulty.value) + delay_before_start
        previous_time += note_length

        if note_type == 'rest':
            continue
        else:
            finger_positions_for_note = note.press_combination_for_note(note_type)

            # the timing for the note is the last element in the position array
            finger_positions_for_note.append(note_time)
            timed_finger_positions.append(finger_positions_for_note)

    return timed_finger_positions



def rest_timings_for_song(song, difficulty):
    with open('songs/' + song.name.replace("_", " ") + '.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    rest_timings = []
    previous_time = 0.0
    delay_before_start = 5.0

    for line in data:
        note_type = line[0]
        note_length = float(line[1])

        note_time = (previous_time * difficulty.value) + delay_before_start
        previous_time += note_length

        if note_type == 'rest':
            rest_timings.append(note_time)
        else:
            continue

    return rest_timings


def cut_short_timings_for_song(song, difficulty):
    with open('songs/' + song.name.replace("_", " ") + '.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    cut_short_timings = []
    previous_time = 0.0
    delay_before_start = 5.0

    for line in data:
        note_type = line[0]
        note_length = float(line[1])

        note_time = (previous_time * difficulty.value) + delay_before_start
        previous_time += note_length

        if note_type == 'rest':
            continue
        elif len(line) > 2 and line[2] == 'short':
            cut_short_timings.append(note_time)

    return cut_short_timings