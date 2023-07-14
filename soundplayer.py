from pygame import mixer
import random


class SoundPlayer:
    def __init__(self):
        if not mixer.get_init():
            mixer.init()

        self.jump_sounds = []
        for i in range(1, 4):
            self.jump_sounds.append(SoundPlayer.load(f'.\\assets\\Sounds\\jump{i}.wav'))
            self.jump_sounds[-1].set_volume(0.15)

        self.death_sound = SoundPlayer.load('assets\\Sounds\\death.wav')
        self.death_sound.set_volume(0.15)

    @staticmethod
    def load(path):
        return mixer.Sound(path)

    def jump(self):
        random.choice(self.jump_sounds).play()

    def die(self):
        self.death_sound.play()
