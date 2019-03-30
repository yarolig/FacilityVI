
import pygame


class Sounds:
    def init(self):
        pygame.mixer.init()
        self.hit_hand = pygame.mixer.Sound('data/sound/hit_hand.wav')
        self.hit_umbrella = pygame.mixer.Sound('data/sound/hit_medium_ubrella.wav')
        self.hit_large = pygame.mixer.Sound('data/sound/hit_large.wav')
        self.miss = pygame.mixer.Sound('data/sound/miss.wav')
        self.miss2 = pygame.mixer.Sound('data/sound/miss2.wav')
        self.fall = pygame.mixer.Sound('data/sound/fall.wav')
        self.pickup = pygame.mixer.Sound('data/sound/pickup.wav')
        pygame.mixer.music.load('data/music/Parallel_Park_-_02_-_Base.ogg')
        pygame.mixer.music.play(loops=-1)
        self.music_enabled = True
        self.sound_enabled = True

    def play(self, name):
        if not self.sound_enabled:
            return
        if name == 'hand':
            self.hit_hand.play()
        if name == 'umbrella':
            self.hit_umbrella.play()
        if name == 'large':
            self.hit_large.play()
        if name == 'miss':
            self.miss.play()
        if name == 'pickup':
            self.pickup.play()
        if name == 'fall':
            self.fall.play()

    def play_music(self):
        pygame.mixer.music.play(loops=-1)
    def stop_music(self):
        pygame.mixer.music.stop()
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled


sounds = Sounds()

def init_sound():
    sounds.init()

def play_sound(name):
    sounds.play(name)