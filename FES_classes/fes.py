# Elizaveta Zavialova - API wrap for ScienceMode 4
# inspired by https://github.com/humancomputerintegration/rehamove-integration-lib/blob/master/builds/python/windows_amd64/rehamove.py
# API wrap from HCI lab in Chicago
from sciencemode import sciencemode
import time

class FES:

    def __init__(self, PORT):
        print("Initializing FES device...")
        self.device = sciencemode.ffi.new("Smpt_device*")
        self.port = sciencemode.ffi.new("char[]", bytes(PORT, 'utf-8'))
        ret = sciencemode.smpt_check_serial_port(self.port)
        print(f"Port check is {ret}")
        sciencemode.smpt_open_serial_port(self.device, self.port)


    def close_port(self):
        ret = sciencemode.smpt_close_serial_port(self.device)
        print(f"Closing serial port: {ret}")

    def mid_lvl_init(self):
        device = self.device
        ml_init = sciencemode.ffi.new("Smpt_ml_init*")
        ml_init.packet_number = sciencemode.smpt_packet_number_generator_next(device)
        ret = sciencemode.smpt_send_ml_init(device, ml_init)
        print(f"Sending mid level init...: {ret}")
        time.sleep(1) # TO DO: CHECK IF NEEDS REMOVING


    # Creates a bi-phasic pulse with specified
    def mid_lvl_channel_stim_pattern(self, ml_update, stimulation_obj):
        channel = stimulation_obj.channel
        period_ms = stimulation_obj.period_ms
        amplitude_mA = stimulation_obj.amplitude_mA
        pulse_width_micros = stimulation_obj.pulse_width_micros

        ml_update.enable_channel[channel] = True
        ml_update.channel_config[channel].period = period_ms
        ml_update.channel_config[channel].number_of_points = 3
        ml_update.channel_config[channel].points[0].time = pulse_width_micros
        ml_update.channel_config[channel].points[0].current = amplitude_mA
        ml_update.channel_config[channel].points[1].time = pulse_width_micros
        ml_update.channel_config[channel].points[1].current = 0
        ml_update.channel_config[channel].points[2].time = pulse_width_micros
        ml_update.channel_config[channel].points[2].current = -amplitude_mA
        return ml_update



    def mid_lvl_configure(self, stimulation_obj_list):
        device = self.device
        ml_update = sciencemode.ffi.new("Smpt_ml_update*")
        ml_update.packet_number = sciencemode.smpt_packet_number_generator_next(device)

        if type(stimulation_obj_list) != list:
            print('There is one or less stimulations, creating a list..')
            stimulation_obj_list = [stimulation_obj_list]

        for stimulation_obj in stimulation_obj_list:
            ml_update = self.mid_lvl_channel_stim_pattern(ml_update, stimulation_obj)

        ret = sciencemode.smpt_send_ml_update(device, ml_update)
        print(f"Sending mid level update... {ret}")
        return ml_update


    def maintain(self, duration_s):
        ml_get_current_data = sciencemode.ffi.new("Smpt_ml_get_current_data*")
        for i in range(duration_s):
            ml_get_current_data.data_selection = sciencemode.Smpt_Ml_Data_Channels
            ml_get_current_data.packet_number = sciencemode.smpt_packet_number_generator_next(self.device)
            ret = sciencemode.smpt_send_ml_get_current_data(self.device, ml_get_current_data)
            print(f"smpt_send_ml_get_current_data: {ret}")
            time.sleep(1)


    # takes in stimulation object
    # delivers sustained midlevel stimulation
    def mid_lvl_stimulate(self, stimulation, duration_s):
        self.mid_lvl_init()
        self.mid_lvl_configure(stimulation)
        self.maintain(duration_s)
       # self.close_port() RIGHT NOW WE NEED A SUSTAINED STIMULATION WITHOUT CLOSING THE PORT ALL THE TIME



    def low_lvl_init(self):
        ll_init = sciencemode.ffi.new("Smpt_ll_init*")
        ll_init.high_voltage_level = sciencemode.Smpt_High_Voltage_Default
        ll_init.packet_number = sciencemode.smpt_packet_number_generator_next(self.device)
        ret = sciencemode.smpt_send_ll_init(self.device, ll_init)
        print(f"Initiating low level signal: {ret}")
        time.sleep(1)


    def low_lvl_configure(self, stimulation_obj):
        ll_config = sciencemode.ffi.new("Smpt_ll_channel_config*")
        ll_config.enable_stimulation = True
        ll_config.channel = stimulation_obj.channel
        ll_config.connector = stimulation_obj.connector



    def low_lvl_stimulate(self, stimulation):
        self.low_lvl_init()
        self.low_lvl_configure(stimulation)


