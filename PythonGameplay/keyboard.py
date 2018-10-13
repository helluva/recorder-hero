from tkinter import *

pressed_keys_update_handler = None
pressed_fingers = [0, 0, 0, 0, 0, 0, 0]


def key_pressed(event):
    global pressed_keys_update_handler, pressed_fingers

    if event.char in ['1', '2', '3', '4', '5', '6', '7']:
        index = int(event.char) - 1
        pressed_fingers[index] = 1

    pressed_keys_update_handler(pressed_fingers)


def key_released(event):
    global pressed_keys_update_handler, pressed_fingers

    if event.char in ['1', '2', '3', '4', '5', '6', '7']:
        index = int(event.char) - 1
        pressed_fingers[index] = 0

    pressed_keys_update_handler(pressed_fingers)


def configure_keyboard_listener(tk, new_key_press_handler):
    global pressed_keys_update_handler
    pressed_keys_update_handler = new_key_press_handler

    tk.bind('<KeyPress>', key_pressed)
    tk.bind('<KeyRelease>', key_released)


