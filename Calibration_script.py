import numpy as np

from FES_classes.stim_mid import  Stimulation_Mid_Lvl
from FES_classes.fes import FES



def MakeSeq():
    experiments = ["Orange:FESFast", "Red:ControlSlow", "Black:ControlFast", "Green:FESSlow"]
    np.random.shuffle(experiments)
    return str(experiments)

if __name__ == "__main__":
    MAX_AMPLITUDE = 50 # mA
    INITIAL_AMP = 0
    STEP_SIZE = 5
    STIMULATION_DURATION = 1
    FES_DEVICE = FES("COM7")
    PERIOD = 28 # 35Hz
    PWM = 150
    # I assume we are going to adjust the stimulation just based on the stimulus
    amp_list = []
    amp_list.append(INITIAL_AMP)
    CalibrationFinished = False
    amp_list_ix = 0

    skip_next = False
    # 28 ms is 35Hz
    while not CalibrationFinished:
        stim = Stimulation_Mid_Lvl(amplitude_mA = amp_list[amp_list_ix], period_ms= PERIOD, pulse_width_micros = PWM, channel = 'red')
        if not skip_next:
            #FES_DEVICE.mid_lvl_stimulate(stim, duration_s= STIMULATION_DURATION)
            print("bzz")
        skip_next = False

        print(f'current amplitude is {amp_list[amp_list_ix]} mA')
        print(f"type 'up' to increase the amplitude by {STEP_SIZE}mA, 'down' to go back to a previous stimulation,"
           f" and 'exit' to confirm your choice")
        decision = input()

        if decision == "up":
            print("pressed up")
            print(f"{amp_list=}, {amp_list_ix=} before")

            # if the researcher inputs up sign, the calibration continues,
            # amplitude is increased, the whole process is repeated
            if (amp_list[amp_list_ix] + STEP_SIZE) > MAX_AMPLITUDE:
                print("reached maximum amplitude, force quitting the calibration")
                CalibrationFinished = True
                final_amp = amp_list[amp_list_ix]

            else:
                new_amp = amp_list[amp_list_ix] + STEP_SIZE
                if new_amp not in amp_list:
                    amp_list.append(new_amp)
                amp_list_ix += 1
                print(f"{amp_list=}, {amp_list_ix=} after")

        elif decision == "down":
            print("pressed down")
            print(f"{amp_list=}, {amp_list_ix=} before")
            # if we want to go down to a previous intensity, we just reduce the amplitude_index
            if amp_list_ix != 0:
                 amp_list.pop()

            amp_list_ix = max(0, amp_list_ix - 1)  # we cant go beyond the first
            print(f"{amp_list=}, {amp_list_ix=} after")

        elif ("step_size =" in decision.lower() or "step size =" in decision.lower()):
            dec = decision.split('=')
            STEP_SIZE = int(dec[-1])
            print(f"new step size is {STEP_SIZE}")
            skip_next = True

        elif decision == "exit":
            print('pressed exit')
            CalibrationFinished = True
            final_amp = amp_list[amp_list_ix]

        elif decision == "repeat":
            pass

        else:
            print("not a valid command")


    print("please provide participants name:")
    name = input()
    with open(f"Calibrations/calibrated_{name}", 'w') as f:
        f.write(f"amplitude = {final_amp}, period  = {PERIOD}, pwm = {PWM}\n")
        f.write(MakeSeq())
