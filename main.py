from FES_classes.stim_mid import  Stimulation_Mid_Lvl
from FES_classes.fes import FES


fes_device = FES("COM7")
stimulation = Stimulation_Mid_Lvl(amplitude_mA = 20, period_ms= 20, pulse_width_micros = 150, channel = 'red')
fes_device.mid_lvl_stimulate(stimulation, duration_s=1)