
class Stimulation_Mid_Lvl():

    channel0 = ['red', 'r', '0', 0]
    channel1 = ['blue', 'b', '1', 1]
    channel2 = ['black', 'k', '2', 2]
    channel3 = ['white', 'w', '3', 3]


    def __init__(self, amplitude_mA, period_ms, pulse_width_micros, channel):
        self.amplitude_mA = amplitude_mA
        self.period_ms = period_ms
        if period_ms != 0:
            self.freq = 1/(period_ms * 10**(-3))
        else:
            self.freq = 0
        self.pulse_width_micros = pulse_width_micros
        self.channel = self.get_channel(channel)

    def get_channel(self, channel):
        if channel in self.channel0:   return 0
        elif channel in self.channel1: return 1
        elif channel in self.channel2: return 2
        elif channel in self.channel3: return 3
        else: return None
