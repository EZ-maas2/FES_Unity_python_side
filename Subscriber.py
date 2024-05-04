# This file is for communication between C# and python
# We will use a socket port approach with zero mq
# The python part is gonna act as a subscriber that awaits for the publisher to send a signal

import numpy
import zmq
import sounddevice as sd
from FES_classes.stim_mid import  Stimulation_Mid_Lvl
from FES_classes.fes import FES

def setupSUB(ip, port, topic = "FES"):
    cont = zmq.Context()
    socket = cont.socket(zmq.SUB)

    # IP of VR headset
    socket.connect(f"tcp://{ip}:{port}")
    #socket.connect(f"tcp://10.158.101.101:{port}") # lrz office ip adress
    #socket.connect(f"tcp://localhost:{port}")
    socket.subscribe("FES")
    return socket


def check_message(message, topic):
    message = message.decode('utf-8')

    if message == topic:
        return 0
    elif 'True' in message:
        return True
    else:
        return False


def check_message_stimulation(message, topic):
    if message == topic:
        return 0
    elif 'channel' in message: # message is of the format channel|red|
        stim_params_list = message.split('|')
        return create_stim(stim_params_list)
    else:
        return 0


def create_stim(stimulation_params):
    channel_ix = stimulation_params.index('channel')
    pwm_ix = stimulation_params.index('pwm_micros')
    amplitude_ix = stimulation_params.index('amplitude_mA')
    period_ix = stimulation_params.index('period_ms')

    channel = stimulation_params[channel_ix+1]
    pwm = int(stimulation_params[pwm_ix+1])
    amp = float(stimulation_params[amplitude_ix+1])
    period = float(stimulation_params[period_ix+1])

    stimulation = Stimulation_Mid_Lvl(amplitude_mA=amp, period_ms=period, pulse_width_micros=pwm, channel=channel)
    return stimulation


def setupFES(port):
    fes_device = FES(port)
    fes_device.mid_lvl_init()
    return fes_device


if __name__ == "__main__":
    #fes_device = setupFES(port='COM7')
    ip = '192.168.178.85'# home ip for vr
    topic = 'FES'
    port = 5556
    socket = setupSUB(ip, port) # let's try a different format

    i = 0
    message = ''
    while message != 'Stop':
        message = socket.recv() # Here im waiting for the type of stimulation FES device should deliver
        message = message.decode('utf-8')
        print(f'{i}: {message}')
        stimulation = check_message_stimulation(message, topic)
        if (stimulation != 0):
            print('stimulating!')
            #fes_device.mid_lvl_configure(stimulation)
            #fes_device.maintain(1) # duration is 1 second because this is the update frequency

        i = i+1
    print('Stopped!')
    #fes_device.close_port()
