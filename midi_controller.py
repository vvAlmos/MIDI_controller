import WF_SDK as wf     # import WF instruments
import MIDI as midi     # import MIDI commands and messages
import FPGA as fpga     # import FPGA commands

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
# different LED colors for different MIDI channels
LED_duty = [{"red": 100, "green": 0, "blue": 0}, {"red": 0, "green": 100, "blue": 0}, {"red": 0, "green": 0, "blue": 100},
            {"red": 100, "green": 100, "blue": 0}, {"red": 100, "green": 0, "blue": 100}, {"red": 0, "green": 100, "blue": 100},
            {"red": 50, "green": 100, "blue": 0}, {"red": 50, "green": 0, "blue": 100}, {"red": 100, "green": 50, "blue": 0},
            {"red": 0, "green": 50, "blue": 100}, {"red": 100, "green": 0, "blue": 50}, {"red": 0, "green": 100, "blue": 50},
            {"red": 100, "green": 25, "blue": 25}, {"red": 25, "green": 100, "blue": 25}, {"red": 25, "green": 25, "blue": 100},
            {"red": 100, "green": 100, "blue": 100}]

"""-----------------------------------------------------------------------"""

# connect to the device
device_handle, device_name = wf.device.open("Analog Discovery Pro 3X50")

# check for connection errors
wf.device.check_error(device_handle)

# open raveloxmidi
midi.open()

# configure the FPGA
fpga.configure(device_name="ArtyS7")

# initialize the static I/O
# set output pins
wf.static.set_mode(device_handle, MUX_ADDR_0, output=True)
wf.static.set_mode(device_handle, MUX_ADDR_1, output=True)
# set all static outputs to LOW
wf.static.set_state(device_handle, MUX_ADDR_0, False)
wf.static.set_state(device_handle, MUX_ADDR_1, False)

# initialize the oscilloscope
wf.scope.open(device_handle)

# initialize the logic analyzer
wf.logic.open(device_handle)

# turn on the power supply
wf.supplies.switch(device_handle, device_name, True, True, False, 3.3, 0)

# start generating the reference signals
# PWM reference
wf.wavegen.generate(device_handle, PWM_REF_CH, wf.wavegen.function.ramp_up, offset=1.65, amplitude=1.65, frequency=PWM_frequency, symmetry=100)
# -5V reference
wf.wavegen.generate(device_handle, NEG_REF_CH, wf.wavegen.function.dc, -5)

"""-----------------------------------"""

try:
    # initialize the iteration counter
    iteration_cnt = 0

    # main loop
    while True:
        # increment the iteration counter
        iteration_cnt += 1

        # set current MUX address
        mux_address = iteration_cnt % 4
        wf.static.set_state(device_handle, MUX_ADDR_0, mux_address & 1)
        wf.static.set_state(device_handle, MUX_ADDR_1, mux_address & 2)

        # get controller data

        # send out MIDI data

        # set LED color
        wf.pattern.generate(device_handle, LED_R, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[MIDI_channel]["red"])
        wf.pattern.generate(device_handle, LED_G, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[MIDI_channel]["green"])
        wf.pattern.generate(device_handle, LED_B, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[MIDI_channel]["blue"])

except:
    # exit on Ctrl+C
    pass

"""-----------------------------------"""

# turn off LEDs
wf.pattern.generate(device_handle, LED_R, wf.pattern.function.pulse, LED_frequency, duty_cycle=0)
wf.pattern.generate(device_handle, LED_G, wf.pattern.function.pulse, LED_frequency, duty_cycle=0)
wf.pattern.generate(device_handle, LED_B, wf.pattern.function.pulse, LED_frequency, duty_cycle=0)

# reset WF instruments
wf.wavegen.close(device_handle)
wf.pattern.close(device_handle)
wf.logic.close(device_handle)
wf.scope.close(device_handle)
wf.static.close(device_handle)
wf.supplies.switch(device_handle, device_name, False, False, False, 0, 0)
wf.supplies.close(device_handle)

# close raveloxmidi
midi.close()

# close the connection to the ADP
wf.device.close(device_handle)
