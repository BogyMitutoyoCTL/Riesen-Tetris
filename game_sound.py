import random
import pygame

_songs = ['./sound-files/lied.mp3', './sound-files/lied2.mp3']


def play_song(_song_file_name):
    pygame.mixer.music.load(_song_file_name)
    print('Song playing:' + _song_file_name)
    pygame.mixer.music.play(0)


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(pygame.QUIT)
    play_song(random.choice(_songs))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                next_song = random.choice(_songs)
                play_song(next_song)
            else:
                print(event)


if __name__ == '__main__':
    main()
