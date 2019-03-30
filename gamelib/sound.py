
import pygame


class Sounds:
    def init(self):
        pygame.mixer.init()
        self.hit_hand = pygame.mixer.Sound('data/sound/hit_hand.wav')
        self.hit_umbrella = pygame.mixer.Sound('data/sound/hit_medium_ubrella.wav')
        self.hit_large = pygame.mixer.Sound('data/sound/hit_large.wav')
        self.miss = pygame.mixer.Sound('data/sound/miss2.wav')
        self.fall = pygame.mixer.Sound('data/sound/fall.wav')

    def play(self, name):
        if name == 'hand':
            self.hit_hand.play()
        if name == 'umbrella':
            self.hit_umbrella.play()
        if name == 'large':
            self.hit_large.play()
        if name == 'miss':
            self.miss.play()
        if name == 'fall':
            self.fall.play()

sounds = Sounds()

def init_sound():
    sounds.init()

def play_sound(name):
    sounds.play(name)