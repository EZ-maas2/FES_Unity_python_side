class Stimulation_Low_Lvl:

    channel0 = ['red', 'r', '0', 0]
    channel1 = ['blue', 'b', '1', 1]
    channel2 = ['black', 'k', '2', 2]
    channel3 = ['white', 'w', '3', 3]

    connector0 = ['yellow', 'y', 0, '1']
    connector1 = ['green', 'g', 1, '1']


    def __init__(self, channel, connector):
        self.connector = self.get_conector(connector)
        self.channel = self.get_channel(channel)

    def get_channel(self, channel):
        if channel in self.channel0:   return 0
        elif channel in self.channel1: return 1
        elif channel in self.channel2: return 2
        elif channel in self.channel3: return 3
        else: return None

    def get_connector(self, connector):
        if connector in self.connector0: return 0
        elif connector in self.connector1: return 1
        else: return None
