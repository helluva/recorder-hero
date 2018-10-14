

pressed_fingers_to_notes_mapping = {
    #'1111111': 'c1',   # we can't actually use these notes,
    '1111010': 'd1',   # because iPhone multitouch only supports 5 taps at a time
    '1111100': 'e1',
    '1111000': 'f1',
    '1110000': 'g1',
    '1100000': 'a1',
    '1000000': 'b1',
    '0100000': 'c2',
    '0010000': 'd2',
    '0111110': 'e2',
    '0111101': 'f2',
    '0111000': 'g2',
    '0110000': 'a2',
    '0110110': 'b2',
    '0100110': 'c3'
}


def note_for_recorder_press_combination(pressed_fingers):
    onehotBitstring = ''.join(map(str, pressed_fingers))

    if onehotBitstring in pressed_fingers_to_notes_mapping:
        return pressed_fingers_to_notes_mapping[onehotBitstring]
    else:
        return None

def press_combination_for_note(note):
    for (key, value) in pressed_fingers_to_notes_mapping.items():
        if value == note:
            return list(map(int, list(key)))

    # otherwise
    exit("Error: can't use note " + note)