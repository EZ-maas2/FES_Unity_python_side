
import zmq
import datetime

def setupSUB(ip, port, topic = "FES"):
    cont = zmq.Context()
    socket = cont.socket(zmq.SUB)

    # IP of VR headset
    socket.connect(f"tcp://{ip}:{port}")
    socket.subscribe(topic)
    return socket



def data_registration_setup():
    print("Please provide  filename:")
    filename = input()
    return filename

if __name__ == "__main__":
    #ip = '192.168.178.85' # home ip for vr
    ip = '192.168.178.101' # home ip for desktop
    #ip = '10.158.101.242'  # lrz headset ip address
    topic = 'Timer'
    port = 5557
    socket = setupSUB(ip, port, topic) # let's try a different format
    experiment_id = data_registration_setup()

    i = 0
    message = ''
    while message != 'Stop':
        message = socket.recv()
        message = message.decode('utf-8')
        print(f'{i}: {message}')
        if message != topic:
            with open(f"Data/{experiment_id}", 'a') as file:
                file.write(f"{datetime.datetime.now()}: {experiment_id}_{i} : {message} s \n")
        i += 1
    print('Stopped!')
