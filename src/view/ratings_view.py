import customtkinter as ctk
from os import path
import pyperclip
from PIL import Image
from src import ASSETS_FOLDER

class Rating(ctk.CTkFrame):
    def __init__(self, master, attribute_name):
        super().__init__(master)

        self.attribute_name = attribute_name

        self.grid_columnconfigure((0,2), weight = 1)

        self.slider = ctk.CTkSlider(master = self, orientation = 'vertical', from_ = 0., to = 1., height = 500)
        self.slider.grid_configure(row = 0, column = 1, padx = 0, pady = 0, sticky = 'n')

        self.label = ctk.CTkLabel(master = self, text = self.attribute_name, width = 100)
        self.label.grid_configure(row = 1, column = 0, columnspan = 3, padx = 10, pady = (10,0), sticky = 'new')

    def get_score(self) -> float:
        return self.slider.get()
    
    def reset(self):
        self.slider.set(.5)
        

class RatingsView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.grid_rowconfigure((0,3), weight = 1)

        self.controller = controller

        self.copy_image = Image.open(path.join(ASSETS_FOLDER,'copy_to_clipboard.png'))
        self.copy_image_done = Image.open(path.join(ASSETS_FOLDER,'copy_to_clipboard_done.png'))

        self.text_variable = ctk.StringVar(value = '')
        self.copy_text_image = ctk.CTkImage(light_image = self.copy_image, dark_image = self.copy_image, size = (22, 28))

        self.timbre_rating = Rating(master = self, attribute_name = 'Timbre')
        self.timbre_rating.grid_configure(row = 1, column = 0, padx = (20,0), pady = (10,0), sticky = 'new')

        self.source_width_rating = Rating(master = self, attribute_name = 'Largeur de Source')
        self.source_width_rating.grid_configure(row = 1, column = 1, padx = (20,0), pady = (10,0), sticky = 'new')

        self.plausibility_rating = Rating(master = self, attribute_name = 'Plausibilité')
        self.plausibility_rating.grid_configure(row = 1, column = 2, padx = 20, pady = (10,0), sticky = 'new')

        self.validate_btn = ctk.CTkButton(master = self, width = 50, text = 'Valider', command = self.validate)
        self.validate_btn.grid_configure(row = 2, column = 0, columnspan = 3, padx = 0, pady = (20,0), sticky = 'new')

        self.progress_bar = ctk.CTkProgressBar(master = self)
        self.progress_bar.grid_configure(row = 3, column = 0, columnspan = 3, padx = 0, pady = (10,0), sticky = 'new')

        self.text_display = ctk.CTkButton(master = self, textvariable = self.text_variable, text_color = '#8d2929', fg_color = 'gray20', hover = False, image = self.copy_text_image, command = self.copy_text, width = 300)
        self.text_display.grid_configure(row = 4, column = 0, columnspan = 3, padx = 0, pady = (10,0), sticky = 'sew')

    def validate(self):
        if self.validate_btn.cget('state') == 'disabled':
            return
        self.controller.register_rating(ratings = tuple([slider.get_score() for slider in [self.timbre_rating, self.source_width_rating, self.plausibility_rating]]))

    def reset_sliders(self):
        for slider in (self.timbre_rating, self.source_width_rating, self.plausibility_rating):
            slider.reset()

    def disable_validate_button(self, sound_duration_ms: int):
        self.validate_btn.configure(state = 'disabled')
        self.after(sound_duration_ms, self.allow_rating)

    def set_progress(self, progress: float):
        self.progress_bar.set(progress)

    def allow_rating(self):
        self.validate_btn.configure(state = 'normal')

    def display_soundfile_error(self, soundfile: str):
        self.validate_btn.configure(state = 'disabled')
        self.text_variable.set(f'Impossible d\'ouvrir {soundfile}')
        self.text_display.configure(text_color = '#8d2929')

    def display_soundfile_name(self, soundfile: str):
        self.text_variable.set(soundfile)
        self.text_display.configure(text_color = 'gray10')
        self.copy_text_image.configure(light_image = self.copy_image, dark_image = self.copy_image)

    def copy_text(self):
        pyperclip.copy(self.text_variable.get())
        self.text_display.configure(text_color = 'gray10')
        self.copy_text_image.configure(light_image = self.copy_image_done, dark_image = self.copy_image_done)