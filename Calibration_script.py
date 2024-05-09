
from FES_classes.stim_mid import  Stimulation_Mid_Lvl
from FES_classes.fes import FES

if __name__ == "__main__":
    MAX_AMPLITUDE = 300 # mA
    INITIAL_AMP = 20
    STEP_SIZE = 50
    STIMULATION_DURATION = 1
    # I assume we are going to adjust the stimulation just based on the stimulus
    amp_list = []
    amp_list.append(INITIAL_AMP)
    CalibrationFinished = False
    amp_list_ix = 0

    while not CalibrationFinished:
        stim = Stimulation_Mid_Lvl(amplitude_mA = amp_list[amp_list_ix], period_ms= 20, pulse_width_micros = 150, channel = 'red')
        #FES.mid_lvl_stimulate(stim, duration_s= STIMULATION_DURATION)
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

        elif decision == "exit":
            print('pressed exit')
            CalibrationFinished = True
            final_amp = amp_list[amp_list_ix]

        else:
            print("not a valid command")



    with open("calibrated", 'w') as f:
        f.write(f"amplitude = {final_amp}, period  = 20, pwm = 150")
