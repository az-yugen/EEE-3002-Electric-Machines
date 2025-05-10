import customtkinter as ctk
from panels import *
from settings import *

class Output(ctk.CTkTabview):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.grid(row = 0, column = 2, sticky = 'NSEW', padx = 10, pady=10)

        # TABS
        self.add('Speed & DC Test')
        self.add('OCC & SCC')
        self.add('Current & Voltage')
        self.add('Power & Losses')

        # WIDGETS
        FrameSpeednDC(self.tab('Speed & DC Test'), output_dict)
        FrameOCCnSCC(self.tab('OCC & SCC'), output_dict)
        FrameCurrnVolt(self.tab('Current & Voltage'), output_dict)
        FramePownLoss(self.tab('Power & Losses'), output_dict)



class FrameSpeednDC(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        self.output_dict = output_dict    # Store reference to param_dict

        OutputPanel(self, 'Synchronous Speed', output_dict['sync_speed'], 'rpm')
        OutputPanel(self, 'Synchronous Angular Speed', output_dict['sync_rad'], 'rad/s')
        OutputPanel(self, 'Armature Resistance', output_dict['arm_res'], 'Ω')
        OutputPanel(self, 'Applied Torque', output_dict['torque_app'], 'Nm')
        OutputPanel(self, 'induced Torque', output_dict['torque_ind'], 'Nm')



class FrameOCCnSCC(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        self.output_dict = output_dict    # Store reference to param_dict

        OutputPanel(self, 'Field Current', output_dict['field_curr'], 'A')
        OutputPanel(self, 'OCC Terminal Voltage', output_dict['occ_term_volt'], 'V')
        OutputPanel(self, 'SCC Armature Current', output_dict['scc_arm_curr'], 'A')
        OutputPanel(self, 'Internal Impedance', output_dict['int_imped_mag'], 'Ω')
        OutputPanel(self, 'Synchronous Reactance', output_dict['sync_react'], 'Ω')





class FrameCurrnVolt(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        self.output_dict = output_dict    # Store reference to param_dict

        OutputPanel(self, 'Line Current Magnitude', output_dict['line_curr'], 'A')
        OutputPanel(self, 'Armature Current Magnitude', output_dict['arm_curr'], 'A')
        OutputPanel(self, 'Load Angle', output_dict['arm_curr_ang'], '°')
        OutputPanel(self, 'Internal Angle', output_dict['int_ang'], '°')
        OutputPanel(self, 'Terminal Angle', output_dict['gamma_ang'], '°')
        OutputPanel(self, 'Internal Voltage', output_dict['int_volt_complex'], 'V')
        OutputPanel(self, 'Phase Voltage', output_dict['phase_volt_mag'], 'V')
        OutputPanel(self, 'Terminal Voltage', output_dict['term_volt'], 'V')
        OutputPanel(self, 'Voltage Regulation', output_dict['volt_reg'], '')



class FramePownLoss(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        self.output_dict = output_dict    # Store reference to param_dict

        OutputPanel(self, 'Input Power', output_dict['power_in'], 'W')
        OutputPanel(self, 'Output Power', output_dict['power_out'], 'W')
        OutputPanel(self, 'Reactive Power', output_dict['power_out_react'], 'VAR')
        OutputPanel(self, 'Converted Power', output_dict['power_conv'], 'W')
        # OutputPanel(self, 'Converted Power2', output_dict['power_conv2'])
        OutputPanel(self, 'Copper Loss', output_dict['power_loss_cu'], 'W')
        OutputPanel(self, 'Hysteresis Loss', output_dict['power_loss_he'], 'W')
        OutputPanel(self, 'Mechanical Loss', output_dict['power_loss_mech'], 'W')
        OutputPanel(self, 'Stray Loss', output_dict['power_loss_stray'], 'W')
        OutputPanel(self, 'Efficiency', output_dict['efficiency'], '%')



