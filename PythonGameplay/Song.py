import csv
import note
from enum import Enum

class Difficulty(Enum):
    EASY = 4.0
    MEDIUM = 2.0
    HARD = 1.0


def timed_finger_positions_for_song(song, difficulty):
    with open('songs/' + song + '.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    timed_finger_positions = []
    previous_time = 0.0
    delay_before_start = 0.5

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