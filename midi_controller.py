import WF_SDK as wf     # https://github.com/Digilent/WaveForms-SDK-Getting-Started
import MIDI as midi     # import MIDI commands and messages
import FPGA as fpga

from data_structures import controller_data
from functions import read_digital_data, read_analog_data, write_data
from parameters import *

"""-----------------------------------------------------------------------"""

# global variables
data = controller_data()

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
wf.logic.open(device_handle, sampling_frequency=(1000 * PWM_frequency), buffer_size=1000)

# turn on the power supply
class supplies_state:
    device_name = device_name
    master_state = True
    state = True
    voltage = 3.3
wf.supplies.switch(device_handle, supplies_state)

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
        data = read_digital_data(device_handle, data, mux_address)
        data = read_analog_data(device_handle, data)

        # send out MIDI data
        write_data(data)

        # set LED color
        if data.encoder.channel.change:
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
supplies_state.master_state = False
wf.supplies.switch(device_handle, supplies_state)
wf.supplies.close(device_handle)

# close raveloxmidi
midi.close()

# close the connection to the ADP
wf.device.close(device_handle)
