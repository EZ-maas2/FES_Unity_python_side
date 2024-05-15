import datetime

from FES_classes.stim_mid import  Stimulation_Mid_Lvl
from FES_classes.fes import FES


fes_device = FES("COM7")
stimulation = Stimulation_Mid_Lvl(amplitude_mA = 17, period_ms= 30, pulse_width_micros = 150, channel = 'red')
#fes_device.mid_lvl_stimulate(stimulation, duration_s=1)
fes_device.mid_lvl_init()
fes_device.mid_lvl_configure(stimulation)
start = datetime.datetime.now()
print(f"started at {start}")
fes_device.maintain_new(0.1)
stop = datetime.datetime.now()
print(f"finished at {stop}, took {stop - start}")
