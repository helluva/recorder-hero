import simpleaudio
import threading

current_player = None
current_note = None

def play_note(note):
    global current_player, current_note

    if current_note is note:
        return

    if (current_player is not None) or (note is None):
        if current_player is not None:
            current_player.stop()
        current_player = None
        current_note = None

    if note is None:
        return


    def play_note_on_background_thread(note):
        global current_player, current_note
        wav = simpleaudio.WaveObject.from_wave_file("recorder sounds/" + note + "-full.wav")
        current_note = note
        current_player = wav.play()


    thread = threading.Thread(target=play_note_on_background_thread, args=(note,))
    thread.daemon = True
    thread.start()
