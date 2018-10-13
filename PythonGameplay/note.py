

pressed_fingers_to_notes_mapping = {
    '1111111': 'c1',
    '1111110': 'd1',
    '1111100': 'e1',
    '1111011': 'f1',
    '1110000': 'g1',
    '1100000': 'a1',
    '1000000': 'b1',
    '0100000': 'c2',
}


def note_for_recorder_press_combination(pressed_fingers):

    onehotBitstring = ''.join(map(str, pressed_fingers))

    if onehotBitstring in pressed_fingers_to_notes_mapping:
        return pressed_fingers_to_notes_mapping[onehotBitstring]
    else:
        return None

