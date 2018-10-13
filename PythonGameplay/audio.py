import simpleaudio

current_player = None
current_note = None

def play_note(note, is_initial=True):
    global current_player, current_note

    if current_note is note or note is None:
        return

    if current_player is not None:
        current_player.stop()
        current_player = None
        current_note = None

    if note is None:
        print("No note provided (note==Note)")
        return

    if is_initial:
        print("Playing", ("recorder sounds/" + note + "-full.wav"))
        wav = simpleaudio.WaveObject.from_wave_file("recorder sounds/" + note + "-full.wav")
    else:
        print("Playing", ("recorder sounds/" + note + "-partial.wav"))
        wav = simpleaudio.WaveObject.from_wave_file("recorder sounds/" + note + "-partial.wav")

    current_note = note
    current_player = wav.play()
