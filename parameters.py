"""
Edit the script parameters in this file
"""

import MIDI as midi

"""-----------------------------------------------------------------------"""

# define connections
# DIO
LED_B = 15
LED_G = 14
LED_R = 13
MUX_ADDR_1 = 12
MUX_ADDR_0 = 11
MUX_10 = 10     # empty, empty, attack/release time, empty
MUX_9 = 9       # G#, A, A#, B
MUX_8 = 8       # E, F, F#, G
MUX_7 = 7       # C, C#, D, D#
MUX_6 = 6       # channel 4, modulation 4, timing 4, octave 4 (MSB)
MUX_5 = 5       # channel 3, modulation 3, timing 3, octave 3
MUX_4 = 4       # channel 2, modulation 2, timing 2, octave 2
MUX_3 = 3       # channel 1, modulation 1, timing 1, octave 1 (LSB)
MUX_2 = 2       # volume, filter: low, effect 3, effect 6
MUX_1 = 1       # record, filter: middle, effect 2, effect 5
MUX_0 = 0       # play, filter: high, effect 1, effect 4

# scope
DRUM_15 = 1
DRUM_26 = 2
DRUM_37 = 3
DRUM_48 = 4

# wavegen
PWM_REF_CH = 1
NEG_REF_CH = 2

"""-----------------------------------------------------------------------"""

# other parameters
LED_frequency = 1e03    # in Hz
PWM_frequency = 100e03  # in Hz
note_velocity = 127     # between 0 and 127
drum_channel = midi.CH10

class analog_tresholds:
    low = -0.2  # in V
    high = 0.2  # in V
    clamp = 4.7 # in V
    
# different LED colors for different MIDI channels
LED_duty = [{"red": 100, "green": 0, "blue": 0}, {"red": 0, "green": 100, "blue": 0}, {"red": 0, "green": 0, "blue": 100},
            {"red": 100, "green": 100, "blue": 0}, {"red": 100, "green": 0, "blue": 100}, {"red": 0, "green": 100, "blue": 100},
            {"red": 50, "green": 100, "blue": 0}, {"red": 50, "green": 0, "blue": 100}, {"red": 100, "green": 50, "blue": 0},
            {"red": 0, "green": 50, "blue": 100}, {"red": 100, "green": 0, "blue": 50}, {"red": 0, "green": 100, "blue": 50},
            {"red": 100, "green": 25, "blue": 25}, {"red": 25, "green": 100, "blue": 25}, {"red": 25, "green": 25, "blue": 100},
            {"red": 100, "green": 100, "blue": 100}]
