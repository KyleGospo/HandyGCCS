#!/usr/bin/env python3
# This file is part of Handheld Game Console Controller System (HandyGCCS)
# Copyright 2022-2023 Derek J. Clark <derekjohn.clark@gmail.com>

from evdev import InputDevice, InputEvent, UInput, ecodes as e, list_devices, ff

handycon = None

def init_handheld(handheld_controller):
    global handycon
    handycon = handheld_controller
    handycon.BUTTON_DELAY = 0.10
    handycon.CAPTURE_CONTROLLER = True
    handycon.CAPTURE_KEYBOARD = True
    handycon.CAPTURE_POWER = True
    handycon.GAMEPAD_ADDRESS = 'usb-0000:04:00.3-4/input0'
    handycon.GAMEPAD_NAME = 'Microsoft X-Box 360 pad'
    handycon.KEYBOARD_ADDRESS = 'isa0060/serio0/input0'
    handycon.KEYBOARD_NAME = 'AT Translated Set 2 keyboard'


# Captures keyboard events and translates them to virtual device events.
async def process_event(seed_event, active_keys):
    global handycon

    # Button map shortcuts for easy reference.
    button1 = handycon.button_map["button1"]  # Default Screenshot
    button2 = handycon.button_map["button2"]  # Default QAM
    button3 = handycon.button_map["button3"]  # Default ESC
    button4 = handycon.button_map["button4"]  # Default OSK
    button5 = handycon.button_map["button5"]  # Default MODE
    button13 = handycon.button_map["button13"]

    ## Loop variables
    button_on = seed_event.value

    # Automatically pass default keycodes we dont intend to replace.
    if seed_event.code in [e.KEY_VOLUMEDOWN, e.KEY_VOLUMEUP]:
        handycon.emit_event(seed_event)

    # BUTTON 1 (Default: Screenshot/Launch Chiumera) LC Button
    # if active_keys == [87, 97, 125] and button_on == 1 and button1 not in handycon.event_queue:
    #     await handycon.handle_key_down(seed_event, button1)
    # elif active_keys == [] and seed_event.code in [87, 97, 125] and button_on == 0 and button1 in handycon.event_queue:
    #     await handycon.handle_key_up(seed_event, button1)

    action_button = button1
    if handycon.enable_special_suspend():
        action_button = button13
    if active_keys == [87, 97, 125] and button_on == 1 and action_button not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, action_button)
    elif active_keys == [] and seed_event.code in [87, 97, 125] and button_on == 0 and action_button in handycon.event_queue:
        await handycon.handle_key_up(seed_event, action_button)

    # BUTTON 2 (Default: QAM) Small Button
    if active_keys == [32, 125] and button_on == 1 and button2 not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, button2)
    elif active_keys == [] and seed_event.code in [32, 40, 125, 133] and button_on == 0 and button2 in handycon.event_queue:
        await handycon.handle_key_up(seed_event, button2)

    # BUTTON 4 (Default: OSK) RC Button
    if active_keys == [68, 97, 125] and button_on == 1 and button4 not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, button4)
    elif active_keys == [] and seed_event.code in [68, 97, 125] and button_on == 0 and button4 in handycon.event_queue:
        await handycon.handle_key_up(seed_event, button4)

    # BUTTON 5 (Default: MODE) Big button
    if active_keys == [88, 97, 125] and button_on == 1 and button5 not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, button5)
    elif active_keys == [] and seed_event.code in [88, 97, 125] and button_on == 0 and button5 in handycon.event_queue:
        await handycon.handle_key_up(seed_event, button5)

    # Handle L_META from power button
    elif active_keys == [] and seed_event.code == 125 and button_on == 0 and handycon.event_queue == [] and handycon.shutdown == True:
        handycon.shutdown = False

    if handycon.last_button:
        await handycon.handle_key_up(seed_event, handycon.last_button)
