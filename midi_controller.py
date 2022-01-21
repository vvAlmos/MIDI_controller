import WF_SDK as wf     # https://github.com/Digilent/WaveForms-SDK-Getting-Started
import MIDI as midi     # import MIDI commands and messages
import FPGA as fpga
from MIDI.message import CTRL_CHG     # import FPGA commands

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
# different LED colors for different MIDI channels
LED_duty = [{"red": 100, "green": 0, "blue": 0}, {"red": 0, "green": 100, "blue": 0}, {"red": 0, "green": 0, "blue": 100},
            {"red": 100, "green": 100, "blue": 0}, {"red": 100, "green": 0, "blue": 100}, {"red": 0, "green": 100, "blue": 100},
            {"red": 50, "green": 100, "blue": 0}, {"red": 50, "green": 0, "blue": 100}, {"red": 100, "green": 50, "blue": 0},
            {"red": 0, "green": 50, "blue": 100}, {"red": 100, "green": 0, "blue": 50}, {"red": 0, "green": 100, "blue": 50},
            {"red": 100, "green": 25, "blue": 25}, {"red": 25, "green": 100, "blue": 25}, {"red": 25, "green": 25, "blue": 100},
            {"red": 100, "green": 100, "blue": 100}]

"""-----------------------------------------------------------------------"""

# global variables
class data:
    class switch:
        class play:
            value = 0
            change = False
            message = midi.ON_OFF_SWC[0]
        class record:
            value = 0
            change = False
            message = midi.ON_OFF_SWC[1]
    class potentiometer:
        class volume:
            value = 0
            change = False
            message = midi.VOLUME
        class filter:
            class high:
                value = 0
                change = False
                message = midi.CONTINUOUS_CTRL[0]
            class middle:
                value = 0
                change = False
                message = midi.CONTINUOUS_CTRL[1]
            class low:
                value = 0
                change = False
                message = midi.CONTINUOUS_CTRL[2]
        class effect:
            class a:
                value = 0
                change = False
                message = midi.EFFECT_CTRL[0]
            class b:
                value = 0
                change = False
                message = midi.EFFECT_CTRL[1]
            class c:
                value = 0
                change = False
                message = midi.SLIDER[0]
            class d:
                value = 0
                change = False
                message = midi.SLIDER[1]
            class e:
                value = 0
                change = False
                message = midi.SLIDER[2]
            class f:
                value = 0
                change = False
                message = midi.SLIDER[3]
    class encoder:
        class modulation:
            value = 0
            change = False
            message = midi.MODULATION
        class channel:
            value = 0
            change = False
        class octave:
            value = 0
            change = False
        class timing:
            class attack:
                value = 0
                change = False
                message = midi.ATTACK_TM
            class release:
                value = 0
                change = False
                message = midi.RELEASE_TM
    class key:
        class c:
            value = False
            change = False
            message = midi.C
        class cS:
            value = False
            change = False
            message = midi.CS
        class d:
            value = False
            change = False
            message = midi.D
        class dS:
            value = False
            change = False
            message = midi.DS
        class e:
            value = False
            change = False
            message = midi.E
        class f:
            value = False
            change = False
            message = midi.F
        class fS:
            value = False
            change = False
            message = midi.FS
        class g:
            value = False
            change = False
            message = midi.G
        class gS:
            value = False
            change = False
            message = midi.GS
        class a:
            value = False
            change = False
            message = midi.A
        class aS:
            value = False
            change = False
            message = midi.AS
        class b:
            value = False
            change = False
            message = midi.B
    class drumpad:
        class a:
            value = 0
            change = False
            message = midi.LINE1_O + midi.C
        class b:
            value = 0
            change = False
            message = midi.LINE1_O + midi.CS
        class c:
            value = 0
            change = False
            message = midi.LINE1_O + midi.D
        class d:
            value = 0
            change = False
            message = midi.LINE1_O + midi.DS
        class e:
            value = 0
            change = False
            message = midi.LINE1_O + midi.E
        class f:
            value = 0
            change = False
            message = midi.LINE1_O + midi.F
        class g:
            value = 0
            change = False
            message = midi.LINE1_O + midi.FS
        class h:
            value = 0
            change = False
            message = midi.LINE1_O + midi.G

"""-----------------------------------------------------------------------"""

# auxiliary function
def pwm_to_analog(device_handle, channel):
    # determine the duty cycle
    wf.logic.open(device_handle, sampling_frequency=(1000 * PWM_frequency), buffer_size=1000)
    buffer, _ = wf.logic.record(device_handle, channel, sampling_frequency=(1000 * PWM_frequency), buffer_size=1000)
    return round(sum(buffer) / 1000 * 127)

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
def change_object(object, value):
    # change controller data parameter
    if object.value != value:
        object.value = value
        object.change = True
    else:
        object.change = False
    return object

"""-----------------------------------------------------------------------"""

# auxiliary function
def read_data(device_handle, mux_address):
    if mux_address == 0:
        # MUX address = 0
        temp = 127 if wf.static.get_state(device_handle, MUX_0) else 0
        data.switch.play = change_object(data.switch.play, temp)    # play / pause
        temp = 127 if wf.static.get_state(device_handle, MUX_1) else 0
        data.switch.record = change_object(data.switch.record, temp)    # record / stop
        data.potentiometer.volume = change_object(data.potentiometer.volume, pwm_to_analog(device_handle, MUX_2))  # volume
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        data.encoder.channel = change_object(data.encoder.channel, binary_to_decimal(bits))  # channel
        data.key.c = change_object(data.key.c, wf.static.get_state(device_handle, MUX_7))    # piano key 1
        data.key.e = change_object(data.key.e, wf.static.get_state(device_handle, MUX_8))    # piano key 5
        data.key.gS = change_object(data.key.gS, wf.static.get_state(device_handle, MUX_9))  # piano key 9

    elif mux_address == 1:
        # MUX address = 1
        data.potentiometer.filter.high = change_object(data.potentiometer.filter.high, pwm_to_analog(device_handle, MUX_0))        # high filter
        data.potentiometer.filter.middle = change_object(data.potentiometer.filter.middle, pwm_to_analog(device_handle, MUX_1))    # middle filter
        data.potentiometer.filter.low = change_object(data.potentiometer.filter.low, pwm_to_analog(device_handle, MUX_2))          # low filter
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        data.encoder.modulation = change_object(data.encoder.modulation, round(binary_to_decimal(bits) / 15 * 127))  # modulation
        data.key.d = change_object(data.key.d, wf.static.get_state(device_handle, MUX_7))    # piano key 2
        data.key.fS = change_object(data.key.fS, wf.static.get_state(device_handle, MUX_8))  # piano key 6
        data.key.aS = change_object(data.key.aS, wf.static.get_state(device_handle, MUX_9))  # piano key 10

    elif mux_address == 2:
        # MUX address = 2
        data.potentiometer.effect.a = change_object(data.potentiometer.effect.a, pwm_to_analog(device_handle, MUX_0))  # effect 1
        data.potentiometer.effect.b = change_object(data.potentiometer.effect.b, pwm_to_analog(device_handle, MUX_1))  # effect 2
        data.potentiometer.effect.c = change_object(data.potentiometer.effect.c, pwm_to_analog(device_handle, MUX_2))  # effect 3
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        decimal_value = round(binary_to_decimal(bits) / 15 * 127)
        if wf.static.get_state(device_handle, MUX_10):
            data.encoder.timing.attack = change_object(data.encoder.timing.attack, decimal_value)   # attack time
        else:
            data.encoder.timing.release = change_object(data.encoder.timing.release, decimal_value) # release time
        data.key.cS = change_object(data.key.cS, wf.static.get_state(device_handle, MUX_7))  # piano key 3
        data.key.f = change_object(data.key.f, wf.static.get_state(device_handle, MUX_8))    # piano key 7
        data.key.a = change_object(data.key.a, wf.static.get_state(device_handle, MUX_9))    # piano key 11

    else:
        # MUX address = 3
        data.potentiometer.effect.d = change_object(data.potentiometer.effect.d, pwm_to_analog(device_handle, MUX_0))    # effect 4
        data.potentiometer.effect.e = change_object(data.potentiometer.effect.e, pwm_to_analog(device_handle, MUX_1))    # effect 5
        data.potentiometer.effect.f = change_object(data.potentiometer.effect.f, pwm_to_analog(device_handle, MUX_2))    # effect 6
        bits = [wf.static.get_state(device_handle, MUX_3), wf.static.get_state(device_handle, MUX_4),
                wf.static.get_state(device_handle, MUX_5), wf.static.get_state(device_handle, MUX_6)]
        data.encoder.octave = change_object(data.encoder.octave, binary_to_decimal(bits))    # modulation
        data.key.dS = change_object(data.key.dS, wf.static.get_state(device_handle, MUX_7))  # piano key 4
        data.key.g = change_object(data.key.g, wf.static.get_state(device_handle, MUX_8))    # piano key 8
        data.key.b = change_object(data.key.b, wf.static.get_state(device_handle, MUX_9))    # piano key 12

    return

"""-----------------------------------------------------------------------"""

# auxiliary function
def write_data():
    # define channel and octave
    channel = data.encoder.channel.value
    octave = midi.octaves[channel]

    # send switch states
    if data.switch.play.change:
        midi.send(midi.CTRL_CHG, channel, [data.switch.play.message, data.switch.play.value])
    if data.switch.record.change:
        midi.send(midi.CTRL_CHG, channel, [data.switch.record.message, data.switch.record.value])

    # send potentiometer states
    if data.potentiometer.volume.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.volume.message, data.potentiometer.volume.value])
    if data.potentiometer.filter.high.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.filter.high.message, data.potentiometer.filter.high.value])
    if data.potentiometer.filter.middle.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.filter.middle.message, data.potentiometer.filter.middle.value])
    if data.potentiometer.filter.low.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.filter.low.message, data.potentiometer.filter.low.value])
    if data.potentiometer.effect.a.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.effect.a.message, data.potentiometer.effect.a.value])
    if data.potentiometer.effect.b.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.effect.b.message, data.potentiometer.effect.b.value])
    if data.potentiometer.effect.c.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.effect.c.message, data.potentiometer.effect.c.value])
    if data.potentiometer.effect.d.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.effect.d.message, data.potentiometer.effect.d.value])
    if data.potentiometer.effect.e.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.effect.e.message, data.potentiometer.effect.e.value])
    if data.potentiometer.effect.f.change:
        midi.send(midi.CTRL_CHG, channel, [data.potentiometer.effect.f.message, data.potentiometer.effect.f.value])
    
    # send rotary encoder states
    if data.encoder.modulation.change:
        midi.send(midi.CTRL_CHG, channel, [data.encoder.modulation.message, data.encoder.modulation.value])
    if data.encoder.timing.attack.change:
        midi.send(midi.CTRL_CHG, channel, [data.encoder.timing.attack.message, data.encoder.timing.attack.value])
    if data.encoder.timing.release.change:
        midi.send(midi.CTRL_CHG, channel, [data.encoder.timing.release.message, data.encoder.timing.release.value])

    # send the piano keys
    if data.key.c.change:
        if data.key.c.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.c.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.c.message, note_velocity])
    if data.key.cS.change:
        if data.key.cS.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.cS.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.cS.message, note_velocity])
    if data.key.d.change:
        if data.key.d.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.d.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.d.message, note_velocity])
    if data.key.dS.change:
        if data.key.dS.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.dS.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.dS.message, note_velocity])
    if data.key.e.change:
        if data.key.e.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.e.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.e.message, note_velocity])
    if data.key.f.change:
        if data.key.f.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.f.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.f.message, note_velocity])
    if data.key.fS.change:
        if data.key.fS.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.fS.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.fS.message, note_velocity])
    if data.key.g.change:
        if data.key.g.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.g.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.g.message, note_velocity])
    if data.key.gS.change:
        if data.key.gS.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.gS.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.gS.message, note_velocity])
    if data.key.a.change:
        if data.key.a.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.a.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.a.message, note_velocity])
    if data.key.aS.change:
        if data.key.aS.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.aS.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.aS.message, note_velocity])
    if data.key.b.change:
        if data.key.b.value:
            midi.send(midi.NOTE_ON, channel, [octave + data.key.b.message, note_velocity])
        else:
            midi.send(midi.NOTE_OFF, channel, [octave + data.key.b.message, note_velocity])
    
    # send drumpad values
    if data.drumpad.a.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.a.message, data.drumpad.a.value])
    if data.drumpad.b.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.b.message, data.drumpad.b.value])
    if data.drumpad.c.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.c.message, data.drumpad.c.value])
    if data.drumpad.d.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.d.message, data.drumpad.d.value])
    if data.drumpad.e.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.e.message, data.drumpad.e.value])
    if data.drumpad.f.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.f.message, data.drumpad.f.value])
    if data.drumpad.g.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.g.message, data.drumpad.g.value])
    if data.drumpad.h.change:
        midi.send(midi.NOTE_ON, drum_channel, [data.drumpad.h.message, data.drumpad.h.value])

    return

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

    # main loop
    while True:
        # increment the iteration counter
        iteration_cnt += 1

        # set current MUX address
        mux_address = iteration_cnt % 4
        wf.static.set_state(device_handle, MUX_ADDR_0, mux_address & 1)
        wf.static.set_state(device_handle, MUX_ADDR_1, mux_address & 2)

        # get controller data
        read_data(device_handle, mux_address)

        # send out MIDI data
        write_data()

        # set LED color
        wf.pattern.generate(device_handle, LED_R, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[data.encoder.channel.value]["red"])
        wf.pattern.generate(device_handle, LED_G, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[data.encoder.channel.value]["green"])
        wf.pattern.generate(device_handle, LED_B, wf.pattern.function.pulse, LED_frequency, duty_cycle=LED_duty[data.encoder.channel.value]["blue"])

except:
    # exit on Ctrl+C
    pass

"""-----------------------------------"""

# finish all notes
for channel in range(0, 16):
    midi.send(midi.CTRL_CHG, channel, [midi.ALL_SOUND_OFF])

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
