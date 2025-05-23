import customtkinter as ctk
from panels import *
from settings import *


class Menu(ctk.CTkTabview):
    def __init__(self, parent, param_dict, output_dict):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'NSEW', padx = 10, pady=10)

        # ctk.CTkTabview.configure(font=ctk.CTkFont(family=FONT, size=TAB_FONT_SIZE, weight="bold"))
        # self.font = ctk.CTkFont(family = FONT, size = TAB_FONT_SIZE)

        # tabs
        self.add('Speed')
        self.add('DC Test')
        self.add('Field & Load')

        # WIDGETS
        SpeedFrame(self.tab('Speed'), param_dict)
        DCTFrame(self.tab('DC Test'), param_dict)
        FnLFrame(self.tab('Field & Load'), param_dict, output_dict)


class SpeedFrame(ctk.CTkFrame):
    def __init__(self, parent, param_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        SegmentedPanel(self, 'Frequency', param_dict['freq'],  OPTIONS_FREQ)
        SegmentedPanel(self, 'Poles', param_dict['poles'],  OPTIONS_POLES)


class DCTFrame(ctk.CTkFrame):
    def __init__(self, parent, param_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        EntryPanel(self, 'DC Voltage', param_dict['dct_volt'], 'V')
        EntryPanel(self, 'DC Current', param_dict['dct_curr'], 'A')


class FnLFrame(ctk.CTkFrame):
    def __init__(self, parent, param_dict, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        SliderPanel2(self, 'Field Resistance', param_dict['field_r'], 10, 150, 1000*(150-10), 'Ω')
        SliderPanel2(self, 'Load Amount', param_dict['load_s'], 0, 600, (600-0)*10, '')
        SliderPanel2(self, 'Load Type', param_dict['load_t'], -90, 90, (90+90)*10, '°')
        # SliderPanel2(self, 'Output Voltage', output_dict['phase_volt_mag'], 0, 5000, 5000, 'V')

