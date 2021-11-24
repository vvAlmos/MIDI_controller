""" This module contains information about the content of the MIDI message """
""" More information: 
            https://wiki.cockos.com/wiki/index.php/MIDI_Specification
            https://anotherproducer.com/online-tools-for-musicians/midi-cc-list/ """


"""-------------------------------------------------------------------"""
""" MESSAGE TYPES """
"""-------------------------------------------------------------------"""

NOTE_OFF = 0x80
# Note Off. This message is sent when a note is stopped.

NOTE_ON = 0x90
# Note On. This message is sent when a note is started.

POLY_KEY_PRES = 0xA0
# Polyphonic Key Pressure (Aftertouch). This message is usually sent by
# pressing down on the key after it has been pressed.

CTRL_CHG = 0xB0
# Control Change. Sent when a controller value changes. Controllers include
# devices such as pedals and levers. Controller numbers 120-127 are reserved as
# "Channel Mode Messages".

PRG_CHG = 0xC0
# Program Change. Sent when a patch number changes.

CH_PRS_AFTT = 0xD0
# Channel Aftertouch. This message is usually sent by pressing down on the
# key after it has been pressed - but it is different from Polyphonic
# Key Pressure (Aftertouch) which is per note. This is per channel - use this
# message to send the single greatest pressure value (of all the currently depressed keys).


PITCH_BND = 0xE0
# Pitch Wheel. This message is sent to indicate a change in the pitch wheel.
# The pitch wheel is measured by a fourteen bit value. Center (no pitch change) is
# 0x2000. Sensitivity is a function of the transmitter

SYS_EX_START = 0xF0
# System Exclusive Start, with data1 being the manufacturer's ID and data2 the data itself.
# This message makes up for all that MIDI doesn't support. Data1 is usually a seven-bit
# Manufacturer's I.D. code. If a device recognizes the I.D. code as its own, it will listen
# to the rest of the message, otherwise it will be ignored. System Exclusive is used to send
# data in bulk, such as patch parameters and other non MIDI spec data. (Note: Only Real-Time
# messages may be interleaved with a System Exclusive.) This message also is used for
# extensions called Universal Exclusive Messages.

MTC = 0xF1
# MIDI Time Code, Quarter Frame

SC_SONG_PTR = 0xF2
# System Common, Song Pointer, with data1 and data2 being LSB and MSB respectively.
# This is an internal 14 bit register that holds the number of MIDI beats(1 beat=six MIDI clock
# messages) since the start of the song.

SC_SONG_SEL = 0xF3
# System Common, Song Select, with data1 being the Song Number, data2 unused

TUNE_REQ = 0xF6
# Tune Request. This is a request of all analog synthesizers to tune their oscillators

SYS_EX_END = 0xF7
# System Exclusive End, data1 and data2 unused

SRT_TM_CLK = 0xF8
# System Realtime, Timing Clock, Sent 24 times per quarter note when synchronization is required

SRT_MEAS_END = 0xF9
# System Realtime, Measure End

SRT_START = 0xFA
# System Realtime, Start the current sequence playing. (This message will be followed with Timing Clocks.)

SRT_CONTINUE = 0xFB
# System Realtime, Continue at the point the sequence was Stopped

SRT_STOP = 0xFC
# System Realtime, Stop the current sequence.

SRT_SENSE = 0xFE
# System Realtime, Active Sensing. Use of this message is optional. When initially sent,
# the receiver will expect to receive another Active Sensing message each 300ms(max), or it will
# be assume that the connection has been terminated. At termination, the receiver will turn off all
# voices and return to normal(non-active sensing) operation.

SRT_RESET = 0xFF
# System Realtime, Reset. Reset all receivers in the system to power-up status. This should be used
# sparingly, preferably under manual control. In particular, it should not be sent on power-up.

"""-------------------------------------------------------------------"""
""" NOTES """
"""-------------------------------------------------------------------"""

C = 0
CS = 1  # C#
D = 2
DS = 3  # D#
E = 4
F = 5
FS = 6  # F#
G = 7
GS = 8  # G#
A = 9
AS = 10  # A#
B = 11

"""-------------------------------------------------------------------"""
""" OCTAVES """
"""-------------------------------------------------------------------"""

DBL_CONTRA_O = 0   # double-contra, starting with C-1
SUB_CONTRA_O = 12  # sub-contra, starting with C0
CONTRA_O = 24   # contra, starting with C1
GREAT_O = 36    # great, starting with C2
SMALL_O = 48    # small, starting with C3
LINE1_O = 60    # 1-line, starting with C4
LINE2_O = 72    # 2-line, starting with C5
LINE3_O = 84    # 3-line, starting with C6
LINE4_O = 96   # 4-line, starting with C7
LINE5_O = 108   # 5-line, starting with C8
LINE6_O = 120   # 6-line, starting with C9

"""-------------------------------------------------------------------"""
""" CHANNELS """
"""-------------------------------------------------------------------"""

CH1 = 0
CH2 = 1
CH3 = 2
CH4 = 3
CH5 = 4
CH6 = 5
CH7 = 6
CH8 = 7
CH9 = 8
CH10 = 9
CH11 = 10
CH12 = 11
CH13 = 12
CH14 = 13
CH15 = 14
CH16 = 15

"""-------------------------------------------------------------------"""
""" CONTROL MESSAGES """
"""-------------------------------------------------------------------"""

BANK = 0x00
# Bank Select (coarse). This is for MIDI devices which have more than 128 Programs.
# MIDI Program Change messages only support switching between 128 programs; Bank Select Controller
# (also called Bank Switch) can be used to allow switching between groups (Banks) of 128 programs.

MODULATION = 0x01
# Modulation Wheel (coarse). Sets the MOD Wheel to a particular value.

BREATH = 0x02
# Breath Controller (coarse). The musician can set this controller to affect what he or she chooses.
# Breath control is a wind player's version of Aftertouch.

FOOT_CTRL = 0x04
# Foot Contoller (coarse). The musician can set this controller to affect what he or she chooses.
# This foot pedal is a continuous controller.

PORTAMENTO_TM = 0x05
# Portamento Time (coarse). The rate at which the pitch slides between two notes.

DATA_ENTRY = 0x06
# Data Entry Slider (coarse). The value of some Registered or Non-Registered Parameter.
# Which parameter is affected depends upon a preceding RPN or NRPN message (which itself identifies the parameter's number).

VOLUME = 0x07
# Main Volume (coarse). The device's volume level.

BALANCE = 0x08
# Stereo Balance (coarse). Affects the device's stereo balance (assuming that the device has stereo audio outputs).

PAN = 0x0A
# Pan (coarse). The Pan (Left/Right) setting for a device. Pan is then used, along with Volume, and Balance controllers to
# internally mix all of the Parts to the device's stereo outputs.

EXPRESSION = 0x0B
# Expression (sub-Volume) (coarse). This is a percentage of the value set by Volume Controller). Expression divides the current
# volume into 16,384 steps (or 128 if 8-bit instead of 14-bit resolution is used). Volume Controller is used to set the overall volume
# of the entire musical part, while Expression is used for crescendos and diminuendos. This message makes it possible to adjust the
# overall volume of a part without having to adjust every single MIDI message comprising a crescendo or diminuendo. When Expression
# is at 100% the volume represents the true setting of Volume Controller. Lower values of Expression subtract from the setting of Volume Controller.
# When Expression is 0% then volume is off. When Expression is 50% then the volume is cut in half. All this is within the upper limit set by Volume Controller.

"""---------------------------------------------"""

BANK_LSB = 0x20
# Bank Select (fine), usually ignored

MODULATION_LSB = 0x21
# Modulation Wheel (fine)

BREATH_LSB = 0x22
# Breath Controller (fine)

FOOT_CTRL_LSB = 0x24
# Foot Contoller (fine)

PORTAMENTO_TM_LSB = 0x25
# Portamento Time (fine)

DATA_ENTRY_LSB = 0x26
# Data Entry Slider (fine)

VOLUME_LSB = 0x27
# Main Volume (fine)

BALANCE_LSB = 0x28
# Stereo Balance (fine)

PAN_LSB = 0x29
# Pan (fine)

EXPRESSION_LSB = 0x30
# Expression (sub-Volume) (fine)

"""---------------------------------------------"""

SUSTAIN = 0x40
# *** parameter: off<=63, on>=64
# Sustain Pedal

PORTAMENTO = 0x41
# *** parameter: off<=63, on>=64
# Portamento Switch

SOSTENUTO = 0x42
# *** parameter: off<=63, on>=64
# Sostenuto Pedal

SOFT = 0x43
# *** parameter: off<=63, on>=64
# Soft Pedal

LEGATO = 0x44
# *** parameter: off<=63, on>=64
# Legato Foot Switch

HOLD2 = 0x45
# *** parameter: off<=63, on>=64
# Another way to “hold notes” (see MIDI CC 64 and MIDI CC 66). However notes fade out according to their release
# parameter rather than when the pedal is released

VARIATION = 0x46
# Sound Variation

HARMONICS = 0x47
# Allows shaping the Voltage Controlled Filter (VCF)

RELEASE_TM = 0x48
# Controls release time of the Voltage controlled Amplifier (VCA)

ATTACK_TM = 0x49
# Controls the “Attack’ of a sound. The attack is the amount of time it takes for the sound to reach maximum amplitude.

BRIGHTNESS = 0x4A
# Controls VCFs cutoff frequency of the filter.

PORTAMENTO_CTRL = 0x54
# Controls the amount of Portamento.

HIGH_RES_VELOCITY = 0x58
# Extends the range of possible velocity values

REVERB_DEPTH = 0x5B
# Controls the reverb ammount

TREMOLO_DEPTH = 0x5C
# Controls the tremolo ammount

CHORUS_DEPTH = 0x5D
# Controls the chorus ammount

CELESTE_DEPTH = 0x5E
# Controls the detune ammount

PHASER_DEPTH = 0x5F
# Controls the phaser ammount

"""---------------------------------------------"""

DATA_INCREMENT = 0x60
# Usually used to increment data for RPN and NRPN messages.

DATA_DECREMENT = 0x61
# Usually used to decrement data for RPN and NRPN messages.

NRPN_LSB = 0x62
# Non-Registered Parameter Number

NRPN_MSB = 0x63
# Non-Registered Parameter Number

RPN_LSB = 0x64
# Registered Parameter Number

RPN_MSB = 0x65
# Registered Parameter Number

"""---------------------------------------------"""

ALL_SOUND_OFF = 0x78
# *** parameter: 0
# Mutes all sounds

RESET_CTRL = 0x79
# *** parameter: 0
# It will reset all controllers to their default

LOCAL_CTRL = 0x7A
# *** parameter: 0/127
# Turns internal connection of a MIDI keyboard or workstation, etc. on or off.
# If you use a computer, you will most likely want local control off to avoid notes being played twice:
# once locally and twice when the note is sent back from the computer to your keyboard.

ALL_NOTES_OFF = 0x7B
# *** parameter: 0
# Mutes all sounding notes. Release time will still be maintained, and notes held by sustain will not turn off until sustain pedal is depressed.

OMNI_OFF = 0x7C
# *** parameter: 0
# Sets to “Omni Off” mode.

OMNI_ON = 0x7D
# *** parameter: 0
# Sets to “Omni On” mode.

MONO = 0x7E
# Sets device mode to Monophonic. The value equals the number of channels, or 0 if the number of channels equals the number of voices in the receiver.

POLY = 0x7F
# *** parameter: 0
# Sets device mode to Polyphonic.

"""-------------------------------------------------------------------"""
""" GENERAL CONTROLLERS """
"""-------------------------------------------------------------------"""

CONTINUOUS_CTRL = [0x03, 0x09, 0x0E, 0x0F, 0x14, 0x15,
                   0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1E, 0x1F]
# continuous controllers (coarse)

CONTINUOUS_CTRL_LSB = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36,
                       0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F]
# continuous controllers (fine)

EFFECT_CTRL = [0x0C, 0x0D]
# effect controllers

SLIDER = [0x10, 0x11, 0x12, 0x13]
# general purpose sliders

SOUND_CTRL = [0x4B, 0x4C, 0x4D, 0x4E, 0x4F]
# generic – some manufacturers may use to further shave their sounds

ON_OFF_SWC = [0x50, 0x51, 0x52, 0x53]
# *** parameter: off<=63, on>=64
# generic on/off switches

UNDEFINED = [0x23, 0x55, 0x57,  0x59, 0x5A, 0x66, 0x67, 0x68,
             0x69, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77]
# undefined
