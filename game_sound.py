import time
import random
import pygame

_songs = ['./sound-files/lied.mp3', './sound-files/lied2.mp3']


def play_song(_song_file_name):
    pygame.mixer.music.load(_song_file_name)
    pygame.mixer.music.set_volume(0.2)
    print('Song playing:' + _song_file_name)
    pygame.mixer.music.play(0)      # -1 plays song for ever


def play_sound(file='./sound-files/effects/bell.wav'):
    sound = pygame.mixer.Sound(file)
    sound.set_volume(1.0)
    pygame.mixer.Channel(1).play(sound)
    print('Sound playing:' + file)


def init_pygame():
    pygame.init()


def init_mixer():
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(pygame.QUIT)


def play_random_song():
    play_sound()
    pygame.time.wait(500)
    play_song(random.choice(_songs))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                next_song = random.choice(_songs)
                play_song(next_song)
                play_sound()


# todo: Wire up sounds with events


if __name__ == '__main__':
    init_pygame()
    init_mixer()
    play_random_song()
