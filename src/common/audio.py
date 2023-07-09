from pygame.mixer import Channel
import pygame

def load_sound(file: str) -> pygame.mixer.Sound:
    return Sound(f"res/audio/{file}")

pygame.mixer.pre_init(buffer=32)
pygame.mixer.init(buffer=32)
pygame.mixer.set_num_channels(21)

class Sound(pygame.mixer.Sound):
    i = 0
    def play(self, loops: int = 0) -> None:
        pygame.mixer.Channel(self.i).play(self, loops=loops)
        self.__class__.i += 1
        self.__class__.i %= 20

pygame.mixer.music.load("res/audio/music.wav")
menu_music = load_sound("menu_music.wav")

disintegrate = load_sound("disintegrate.wav")
hurt = load_sound("hurt.wav")
end = load_sound("end.wav")
grow = load_sound("grow.wav")
footsteps = [load_sound("footsteps_1.wav"), load_sound("footsteps_2.wav"), load_sound("footsteps_3.wav")]
wind = load_sound("wind.wav")
chirp = [load_sound("chirp_1.wav"), load_sound("chirp_2.wav")]