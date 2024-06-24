import pygame
import soundfile as sf
import math

def get_sound_duration(path: str):
    with sf.SoundFile(path) as file:
        return math.ceil(1000 * file.frames / file.samplerate)
    
def play_sound(path: str):   
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()