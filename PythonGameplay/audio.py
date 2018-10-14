import simpleaudio
import threading
import time

current_player = None
current_note = None
Mistake_Note_Sentinel = 'mistake'

def play_note(note, cut_short=False):
    global current_player, current_note

    if current_note is note and not cut_short:
        return

    if (current_player is not None) or (note is None) or (current_note is note and cut_short):
        if current_player is not None:
            current_player.stop()
        current_player = None
        current_note = None

    if note is None:
        return

    current_note = note
    play_audio_file("recorder sounds/" + note + "-full.wav", cut_short=cut_short)


def play_mistake_audio():
    play_note(None)

    global current_note
    if current_note == Mistake_Note_Sentinel:
        return

    current_note = Mistake_Note_Sentinel
    play_audio_file("recorder sounds/mistake.wav")


def play_audio_file(file, cut_short=False):
    def play_audio_file_on_background_thread(wav_file, cut_short=False):
        global current_player, current_note
        wav = simpleaudio.WaveObject.from_wave_file(wav_file)
        current_player = wav.play()

        if cut_short:
            time.sleep(0.25)
            if current_player is not None:
                current_player.stop()
                current_player = None
                current_note = None

    thread = threading.Thread(target=play_audio_file_on_background_thread, args=(file,cut_short,))
    thread.daemon = True
    thread.start()
