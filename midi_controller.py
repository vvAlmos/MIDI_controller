import WF_SDK as wf     # https://github.com/Digilent/WaveForms-SDK-Getting-Started
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

# global variables
class controller_data:
    class switch:
        play = False
        record = False
    class potentiometer:
        volume = 0
        class filter:
            high = 0
            middle = 0
            low = 0
        class effect:
            a = 0
            b = 0
            c = 0
            d = 0
            e = 0
            f = 0
    class encoder:
        modulation = 0
        channel = 0
        octave = 0
        class timing:
            attack = 0
            release = 0
    class key:
        c = False
        cS = False
        d = False
        dS = False
        e = False
        f = False
        fS = False
        g = False
        gS = False
        a = False
        aS = False
        b = False
    class drumpad:
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        g = 0
        h = 0

"""-----------------------------------------------------------------------"""

# auxiliary function
def pwm_to_analog(device_handle, channel):
    # determine the duty cycle
    wf.logic.open(device_handle, sampling_frequency=(1000 * PWM_frequency), buffer_size=1000)
    buffer, _ = wf.logic.record(device_handle, channel, sampling_frequency=(1000 * PWM_frequency), buffer_size=1000)
    return (sum(buffer) / 1000 * 127)

"""-----------------------------------------------------------------------"""

def binary_to_decimal(bits):
    # convert boolean list to a number: LSB->MSB
    bits = bits[::-1]
    value = 0
    for bit in bits:
        value <<= 1
        if bit:
            value |= 1
    return value

"""-----------------------------------------------------------------------"""

# auxiliary function
def read_data(device_handle, mux_address):
    # create variable for data
    data = controller_data()

    if mux_address == 0:
        # MUX address = 0
        data.switch.play = wf.static.get_state(device_handle, MUX_0)    # play / pause
        data.switch.record = wf.static.get_state(device_handle, MUX_1)  # record / stop
        data.potentiometer.volume = pwm_to_analog(device_handle, MUX_2)    # volume
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        data.encoder.channel = binary_to_decimal(bits)  # channel
        data.key.c = wf.static.get_state(device_handle, MUX_7)  # piano key 1
        data.key.e = wf.static.get_state(device_handle, MUX_8)  # piano key 5
        data.key.gS = wf.static.get_state(device_handle, MUX_9) # piano key 9

    elif mux_address == 1:
        # MUX address = 1
        data.potentiometer.filter.high = pwm_to_analog(device_handle, MUX_0)      # high filter
        data.potentiometer.filter.middle = pwm_to_analog(device_handle, MUX_1)    # middle filter
        data.potentiometer.filter.low = pwm_to_analog(device_handle, MUX_2)       # low filter
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        data.encoder.modulation = binary_to_decimal(bits) / 15 * 127  # modulation
        data.key.d = wf.static.get_state(device_handle, MUX_7)   # piano key 2
        data.key.fS = wf.static.get_state(device_handle, MUX_8)  # piano key 6
        data.key.aS = wf.static.get_state(device_handle, MUX_9)  # piano key 10

    elif mux_address == 2:
        # MUX address = 2
        data.potentiometer.effect.a = pwm_to_analog(device_handle, MUX_0)    # effect 1
        data.potentiometer.effect.b = pwm_to_analog(device_handle, MUX_1)    # effect 2
        data.potentiometer.effect.c = pwm_to_analog(device_handle, MUX_2)    # effect 3
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        decimal_value = binary_to_decimal(bits) / 15 * 127
        if wf.static.get_state(device_handle, MUX_10):
            data.encoder.timing.attack = decimal_value  # attack time
        else:
            data.encoder.timing.release = decimal_value # release time
        data.key.cS = wf.static.get_state(device_handle, MUX_7)  # piano key 3
        data.key.f = wf.static.get_state(device_handle, MUX_8)   # piano key 7
        data.key.a = wf.static.get_state(device_handle, MUX_9)   # piano key 11

    else:
        # MUX address = 3
        data.potentiometer.effect.d = pwm_to_analog(device_handle, MUX_0)    # effect 4
        data.potentiometer.effect.f = pwm_to_analog(device_handle, MUX_1)    # effect 5
        data.potentiometer.effect.c = pwm_to_analog(device_handle, MUX_2)    # effect 6
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        data.encoder.octave = binary_to_decimal(bits)   # modulation
        data.key.dS = wf.static.get_state(device_handle, MUX_7)  # piano key 4
        data.key.g = wf.static.get_state(device_handle, MUX_8)   # piano key 8
        data.key.b = wf.static.get_state(device_handle, MUX_9)   # piano key 12

    return data

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
    iteration_cnt = -1

    # remember data from previous iteration
    old_data = controller_data()

    # main loop
    while True:
        # increment the iteration counter
        iteration_cnt += 1

        # set current MUX address
        mux_address = iteration_cnt % 4
        wf.static.set_state(device_handle, MUX_ADDR_0, mux_address & 1)
        wf.static.set_state(device_handle, MUX_ADDR_1, mux_address & 2)

        # get controller data
        new_data = read_data(device_handle, mux_address)

        # send out MIDI data
        

        # save current controller data
        old_data = new_data

        # set LED color
        wf.pattern.generate(device_handle, LED_R, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[new_data.encoder.channel]["red"])
        wf.pattern.generate(device_handle, LED_G, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[new_data.encoder.channel]["green"])
        wf.pattern.generate(device_handle, LED_B, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[new_data.encoder.channel]["blue"])

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
