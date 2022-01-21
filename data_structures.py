import MIDI as midi

"""-----------------------------------------------------------------------"""

class data_object:
    # object template
    value = 0
    change = False
    message = None

    def __init__(self, message, change=False, value=0):
        self.value = value
        self.change = change
        self.message = message
        return

"""-----------------------------------------------------------------------"""

class controller_data:
    # MIDI controller data output
    class switch:
        play = data_object(midi.ON_OFF_SWC[0])
        record = data_object(midi.ON_OFF_SWC[1])
    class potentiometer:
        volume = data_object(midi.VOLUME)
        class filter:
            high = data_object(midi.CONTINUOUS_CTRL[0])
            middle = data_object(midi.CONTINUOUS_CTRL[1])
            low = data_object(midi.CONTINUOUS_CTRL[2])
        class effect:
            a = data_object(midi.EFFECT_CTRL[0])
            b = data_object(midi.EFFECT_CTRL[1])
            c = data_object(midi.SLIDER[0])
            d = data_object(midi.SLIDER[1])
            e = data_object(midi.SLIDER[2])
            f = data_object(midi.SLIDER[3])
    class encoder:
        modulation = data_object(midi.MODULATION)
        channel = data_object(None)
        octave = data_object(None)
        class timing:
            attack = data_object(midi.ATTACK_TM)
            release = data_object(midi.RELEASE_TM)
    class key:
        c = data_object(midi.C, value=False)
        cS = data_object(midi.CS, value=False)
        d = data_object(midi.D, value=False)
        dS = data_object(midi.DS, value=False)
        e = data_object(midi.E, value=False)
        f = data_object(midi.F, value=False)
        fS = data_object(midi.FS, value=False)
        g = data_object(midi.G, value=False)
        gS = data_object(midi.GS, value=False)
        a = data_object(midi.A, value=False)
        aS = data_object(midi.AS, value=False)
        b = data_object(midi.B, value=False)
    class drumpad:
        a = data_object(midi.LINE1_O + midi.C)
        b = data_object(midi.LINE1_O + midi.CS)
        c = data_object(midi.LINE1_O + midi.D)
        d = data_object(midi.LINE1_O + midi.DS)
        e = data_object(midi.LINE1_O + midi.E)
        f = data_object(midi.LINE1_O + midi.F)
        g = data_object(midi.LINE1_O + midi.FS)
        h = data_object(midi.LINE1_O + midi.G)
