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

class DirectQuestion(ctk.CTkFrame):
    def __init__(self, master, choices: tuple, name: str, answer_callback: callable, answers: tuple):
        super().__init__(master)

        self.name = name
        self.choices = choices
        self.callback = answer_callback
        self.answers = answers
        self.answer = None

        self.columnconfigure((0,3), weight = 1)
        
        self.choice_1 = ctk.CTkButton(master = self, text = self.choices[0])
        self.choice_1.grid_configure(row = 0, column = 1, padx = (10,0), pady = 10, sticky = 'nw')

        self.choice_2 = ctk.CTkButton(master = self, text = self.choices[1])
        self.choice_2.grid_configure(row = 0, column = 2, padx = 10, pady = 10, sticky = 'ne')

        self.choice_buttons = (self.choice_1, self.choice_2)

        for index, button in enumerate(self.choice_buttons):
            button.configure(command = lambda index = index: self.set_choice(index), hover = False)
            button.configure(fg_color = 'grey25')

    def reset(self) -> None:
        self.answer = None
        for button in self.choice_buttons:
            button.configure(fg_color = 'grey25')

    def set_choice(self, choice: int) -> None:
        self.answer = self.answers[choice]
        self.callback()
        
        not_chosen = (choice-1)**2

        self.choice_buttons[choice].configure(fg_color = '#00966b')
        self.choice_buttons[not_chosen].configure(fg_color = 'grey25')

    def get_answer(self) -> tuple:
        return (self.name, self.answer)
        

class RatingsView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.grid_rowconfigure((0,3), weight = 1)
        self.grid_columnconfigure((0,3), weight = 1)

        self.controller = controller

        self.direct_questions = []
        self.answers = {}

        self.done_playing = False
        self.done_answering = False

        self.copy_image = Image.open(path.join(ASSETS_FOLDER,'copy_to_clipboard.png'))
        self.copy_image_done = Image.open(path.join(ASSETS_FOLDER,'copy_to_clipboard_done.png'))

        self.text_variable = ctk.StringVar(value = '')
        self.copy_text_image = ctk.CTkImage(light_image = self.copy_image, dark_image = self.copy_image, size = (22, 28))

        self.timbre_rating = Rating(master = self, attribute_name = 'Timbre')
        self.timbre_rating.grid_configure(row = 1, column = 1, padx = (20,0), pady = (10,0), sticky = 'new')

        self.plausibility_rating = Rating(master = self, attribute_name = 'Plausibilité')
        self.plausibility_rating.grid_configure(row = 1, column = 2, padx = 20, pady = (10,0), sticky = 'new')

        self.angle_direct_question = DirectQuestion(master = self, choices = ('Frontal', 'Latéral'), name = 'angle', answers = ('Front', 'Side'), answer_callback = self.check_all_direct_questions_answered)
        self.angle_direct_question.grid_configure(row = 2, column = 0, columnspan = 4, padx = 0, pady = (20,0), sticky = 'new')
        self.direct_questions.append(self.angle_direct_question)

        self.movement_direct_question = DirectQuestion(master = self, choices = ('Statique', 'Dynamique'), name = 'movement', answers = (False, True), answer_callback = self.check_all_direct_questions_answered)
        self.movement_direct_question.grid_configure(row = 3, column = 0, columnspan = 4, padx = 0, pady = (20,0), sticky = 'new')
        self.direct_questions.append(self.movement_direct_question)

        self.validate_btn = ctk.CTkButton(master = self, width = 50, text = 'Valider', command = self.validate)
        self.validate_btn.grid_configure(row = 4, column = 0, columnspan = 4, padx = 0, pady = (20,0), sticky = 'new')

        self.progress_bar = ctk.CTkProgressBar(master = self)
        self.progress_bar.grid_configure(row = 5, column = 0, columnspan = 4, padx = 0, pady = (10,0), sticky = 'new')

        self.text_display = ctk.CTkButton(master = self, textvariable = self.text_variable, text_color = '#8d2929', fg_color = 'gray20', hover = False, image = self.copy_text_image, command = self.copy_text, width = 300)
        self.text_display.grid_configure(row = 6, column = 0, columnspan = 4, padx = 0, pady = (10,0), sticky = 'sew')

    def check_all_direct_questions_answered(self):
        for direct_question in self.direct_questions:
            answer = direct_question.get_answer()
            self.answers[answer[0]] = answer[1]

        if None in self.answers.values():
            return
        self.done_answering = True
        self.check_done_answering()

    def validate(self):
        if self.validate_btn.cget('state') == 'disabled':
            return
        
        self.controller.register_rating(ratings = tuple([slider.get_score() for slider in [self.timbre_rating, self.plausibility_rating]]), answers = self.answers)

    def reset(self, direct_question_names: list):
        self.answers = {}
        for slider in (self.timbre_rating, self.plausibility_rating):
            slider.reset()
        for name in direct_question_names:
            self.answers[name] = None
        for direct_question in self.direct_questions:
            direct_question.reset()

    def disable_validate_button(self, sound_duration_ms: int):
        self.validate_btn.configure(state = 'disabled')
        self.after(sound_duration_ms, self.end_sound_play)

    def end_sound_play(self):
        self.done_playing = True
        self.check_done_answering()

    def set_progress(self, progress: float):
        self.progress_bar.set(progress)

    def check_done_answering(self):
        if not self.done_playing:
            return
        if not self.done_answering:
            return
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