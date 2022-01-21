import WF_SDK as wf
import MIDI as midi
from parameters import *

"""-----------------------------------------------------------------------"""

# auxiliary function
def pwm_to_analog(device_handle, channel):
    # determine the duty cycle
    buffer, _ = wf.logic.record(device_handle, channel, sampling_frequency=(1000 * PWM_frequency), buffer_size=1000)
    return round(sum(buffer) / 1000 * 127)

"""-----------------------------------------------------------------------"""

# auxiliary function
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

# main function
def read_digital_data(device_handle, data, mux_address):
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

    return data

"""-----------------------------------------------------------------------"""

# main function
def read_analog_data(device_handle, data):
    # create and get buffers
    buffers = [[], [], [], []]
    buffers[0] = wf.scope.record(device_handle, DRUM_15)
    buffers[1] = wf.scope.record(device_handle, DRUM_26)
    buffers[2] = wf.scope.record(device_handle, DRUM_37)
    buffers[3] = wf.scope.record(device_handle, DRUM_48)

    # find negative and positive peaks
    peaks = [0, 0, 0, 0, 0, 0, 0, 0]
    index = -1
    for buffer in buffers:
        index += 1

        highest = analog_tresholds.low
        lowest = analog_tresholds.high
        for element in buffer:
            if element > analog_tresholds.high and element > highest:
                highest = element
            elif element < analog_tresholds.low and element < lowest:
                lowest = element
        
        # save peaks
        if highest > analog_tresholds.high:
            peaks[index] = highest
        if lowest < analog_tresholds.low:
            peaks[index + 4] = (-1) * lowest

    # convert and round values
    for peak in peaks:
        peak = round(peak / analog_tresholds.clamp * 127)

    # change data
    data.drumpad.a = change_object(data.drumpad.a, peaks[0])
    data.drumpad.b = change_object(data.drumpad.b, peaks[1])
    data.drumpad.c = change_object(data.drumpad.c, peaks[2])
    data.drumpad.d = change_object(data.drumpad.d, peaks[3])
    data.drumpad.e = change_object(data.drumpad.e, peaks[4])
    data.drumpad.f = change_object(data.drumpad.f, peaks[5])
    data.drumpad.g = change_object(data.drumpad.g, peaks[6])
    data.drumpad.h = change_object(data.drumpad.h, peaks[7])
    
    return data

"""-----------------------------------------------------------------------"""

# main function
def write_data(data):
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
