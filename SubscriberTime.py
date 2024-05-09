
import zmq
from FES_classes.stim_mid import  Stimulation_Mid_Lvl
from FES_classes.fes import FES
import  datetime

def setupSUB(ip, port, topic = "FES"):
    cont = zmq.Context()
    socket = cont.socket(zmq.SUB)

    # IP of VR headset
    socket.connect(f"tcp://{ip}:{port}")
    socket.subscribe(topic)
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


def data_registration_setup():
    print("Please provide participant name:")
    name = input()
    name = name.split()
    full_name = ''
    for part in name:
        full_name += part

    print("Please provide the experiment mode (FES or Control):")
    mode = input()
    print("Please provide the speed of the box: ")
    speed = input()
    return full_name+mode+speed

if __name__ == "__main__":
    #fes_device = setupFES(port='COM7')
    ip = '192.168.178.85' # home ip for vr
    ip = '192.168.178.101' # home ip for desktop
    topic = 'Timer'
    port = 5556
    socket = setupSUB(ip, port, topic) # let's try a different format
    experiment_id = data_registration_setup()

    i = 0
    message = ''
    while message != 'Stop':
        message = socket.recv()
        message = message.decode('utf-8')
        print(f'{i}: {message}')
        with open(f"{experiment_id}", 'w') as file:
            file.write(f"{experiment_id}_i : {message} s")
        i += 1
    print('Stopped!')
