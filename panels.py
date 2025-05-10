import customtkinter as ctk
from settings import *


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.font_label = ctk.CTkFont(family = FONT, size = TEXT_FONT_SIZE)
        self.font_num = ctk.CTkFont(family = FONT, size = NUM_FONT_SIZE, weight = 'bold')
        self.pack(fill = 'both', pady = 5, padx = 7, ipady = 5)



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
    def __init__(self, parent, text, data_var, unit):
        super().__init__(parent)

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 4)
        self.columnconfigure(1, weight = 2)
        self.columnconfigure(2, weight = 1)

        ctk.CTkLabel(self, text = text, font=self.font_label).grid(row = 0, column = 0, pady=10)

        self.entry = ctk.CTkEntry(self,
                     textvariable = data_var,
                     width = 50,
                     font = self.font_num,
        )
        self.entry.grid(row = 0, column = 1, sticky = 'E', pady = 10)

        self.unit_label = ctk.CTkLabel(self, text = unit, font=self.font_num)
        self.unit_label.grid(column = 2, row = 0, sticky = 'W', padx = 10)

        self.data_empty()

    def data_empty(self):
        if self.entry.get() == '':
            self.entry.configure(textvariable = 1)



class SliderPanel(Panel):
    def __init__(self, parent, text, slide_param, min_val, max_val, step_num, unit):
        super().__init__(parent = parent)

        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure(0, weight = 4)
        self.columnconfigure(1, weight = 2)
        self.columnconfigure(2, weight = 1)

        ctk.CTkLabel(self, text = text, font=self.font_label).grid(column = 0, row = 0, sticky = 'W', padx = 20)

        self.slider = ctk.CTkSlider(self,
                      variable = slide_param,
                      from_ = min_val,
                      to = max_val,
                      number_of_steps= step_num,
                      command = self.update_text
                      )
        self.slider.grid(row = 1, column = 0, columnspan = 2, padx = 20, pady = 10)

        # self.num_label = ctk.CTkLabel(self, text = self.slider.get(), font=self.font_num)
        # self.num_label.grid(column = 1, row = 0, sticky = 'E')

        self.num_label = ctk.CTkEntry(self, textvariable = self.slider.get(), font=self.font_num)
        self.num_label.grid(column = 1, row = 0, sticky = 'E')

        self.unit_label = ctk.CTkLabel(self, text = unit, font=self.font_num)
        self.unit_label.grid(column = 2, row = 0, sticky = 'W',ipadx = 10)


    def update_text(self, value):
            self.num_label.configure(textvariable = f'{round(value, 2)}')






class SliderPanel2(Panel):
    def __init__(self, parent, text, slide_param, min_val, max_val, step_num, unit):
        super().__init__(parent = parent)

        self.rowconfigure((0,1), weight = 1, uniform= 'a')
        self.columnconfigure(0, weight = 4, uniform= 'a')
        self.columnconfigure(1, weight = 2, uniform= 'a')
        self.columnconfigure(2, weight = 1, uniform= 'a')

        self.slide_param = slide_param
        self.max_val = max_val
        self.min_val = min_val

        ctk.CTkLabel(self, text = text, font=self.font_label).grid(column = 0, row = 0, sticky = 'W', padx = 20)

        self.slider = ctk.CTkSlider(self,
                      variable = slide_param,
                      from_ = min_val,
                      to = max_val,
                      number_of_steps= step_num,
                      )
        self.slider.grid(row = 1, column = 0, columnspan = 2, padx = 20, pady = 10)

        # self.num_label = ctk.CTkLabel(self, text = self.slider.get(), font=self.font_num)
        # self.num_label.grid(column = 1, row = 0, sticky = 'E')

        abcd = ctk.StringVar()
        abcd.set(self.slider.get()) # Set the initial value of the entry to the value of the slider
        abcd.trace_add('write', lambda *args: self.slide(abcd)) # This sends an event to the slide function whenever you type something in the entry

        self.slider_entry = ctk.CTkEntry(self, textvariable=abcd, font=self.font_num, width=60)
        self.slider_entry.grid(column = 1, row = 0, sticky = 'E')

        self.unit_label = ctk.CTkLabel(self, text = unit, font=self.font_num)
        self.unit_label.grid(column = 2, row = 0, sticky = 'W',ipadx = 10)

        self.slider_entry.bind("<KeyRelease>", self.slide) # This sends an event to the slide function whenever you type something in the entry
        self.slider.bind("<B1-Motion>", self.on_change) # This sends an event to the on_change function whenever you change the value on the scale


    def slide(self,event):
        num = self.slider_entry.get() # Get whatever is entered in the entry
        if num.isdigit(): # Checks if it is an integer
        # if num in '-0123456789.': # Checks if it is an integer
            num = float(num)
            if num > self.max_val:
                num = self.max_val
            elif num < self.min_val:
                num = self.min_val
            self.slide_param.set(num)
            # self.on_change(event) # Call the on_change function to update the slider value

    def on_change(self,event): # Change the value of entry
        self.slider_entry.delete(0, 'end')
        self.slider_entry.insert(0, self.slide_param.get())



class OutputPanel(Panel):
    def __init__(self, parent, text, data_var, unit):
        super().__init__(parent = parent)

        self.rowconfigure(0, weight = 1, uniform= 'a')
        self.columnconfigure(0, weight = 4, uniform= 'a')
        self.columnconfigure(1, weight = 2, uniform= 'a')
        self.columnconfigure(2, weight = 1, uniform= 'a')

        self.text_label = ctk.CTkLabel(self, text = text, font=self.font_label)
        self.text_label.grid(row = 0, column = 0, sticky='W', padx = 10, pady=2, )

        ctk.CTkEntry(self,
                     textvariable = data_var,
                     state = 'disabled',
                     width = 75,
                     font=self.font_num
        ).grid(row = 0, column = 1, sticky = 'NSEW', pady = 3)

        self.unit_label = ctk.CTkLabel(self, text = unit, font=self.font_num)
        self.unit_label.grid(row = 0, column = 2, sticky='W', ipadx = 10, pady=3)