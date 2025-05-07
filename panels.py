import customtkinter as ctk
from settings import *


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.font_label = ctk.CTkFont(family = FONT, size = TEXT_FONT_SIZE)
        self.font_num = ctk.CTkFont(family = FONT, size = NUM_FONT_SIZE, weight = 'bold')
        self.pack(fill = 'x', pady = 5, padx = 7, ipady = 5)



class SegmentedPanel(Panel):
     def __init__(self, parent, text, data_var, options):
        super().__init__(parent = parent)

        ctk.CTkLabel(self, text = text, font=self.font_label).pack()
        ctk.CTkSegmentedButton(self,
                                 variable = data_var,
                                 values = options,
                                 font=self.font_num
        ).pack(expand = True, ipadx = 10, ipady = 5)
          


class EntryPanel(Panel):
    def __init__(self, parent, text, data_var):
        super().__init__(parent)

        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1), weight = 1)

        ctk.CTkLabel(self, text = text, font=self.font_label).grid(row = 0, column = 0, pady=10)

        self.entry = ctk.CTkEntry(self,
                     textvariable = data_var,
                     width = 50,
                     font = self.font_num,
        )
        self.entry.grid(row = 0, column = 1, pady = 10)

        self.data_empty()

    def data_empty(self):
        if self.entry.get() == '':
            self.entry.configure(textvariable = 1)



class SliderPanel(Panel):
    def __init__(self, parent, text, slide_param, min_val, max_val, step_num):
        super().__init__(parent = parent)

        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1), weight = 1)

        ctk.CTkLabel(self, text = text, font=self.font_label).grid(column = 0, row = 0, sticky = 'W', padx = 20)

        self.num_label = ctk.CTkLabel(self, text = slide_param.get(), font=self.font_num)
        self.num_label.grid(column = 1, row = 0, sticky = 'E', padx = 30)

        ctk.CTkSlider(self,
                      variable = slide_param,
                      from_ = min_val,
                      to = max_val,
                      number_of_steps= step_num,
                      command = self.update_text
                      ).grid(row = 1, column = 0, columnspan = 2, padx = 20, pady = 10)

    def update_text(self, value):
            self.num_label.configure(text = f'{round(value, 2)}')


class OutputPanel(Panel):
    def __init__(self, parent, text, data_var):
        super().__init__(parent = parent)

        self.rowconfigure(0, weight = 1, uniform= 'a')
        self.columnconfigure(0, weight = 2, uniform= 'a')
        self.columnconfigure(1, weight = 1, uniform= 'a')

        self.text_label = ctk.CTkLabel(self, text = text, font=self.font_label)
        self.text_label.grid(row = 0, column = 0, sticky='W', padx = 12, pady=3, )

        ctk.CTkEntry(self,
                     textvariable = data_var,
                     state = 'disabled',
                    #  width = 50,
                     font=self.font_num
        ).grid(row = 0, column = 1, sticky = 'NSEW', padx = 12, pady = 3)