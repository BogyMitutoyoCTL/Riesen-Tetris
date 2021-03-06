import random
import pygame

_songs = ['./sound-files/lied.mp3', './sound-files/lied2.mp3']


def play_song(_song_file_name):
    pygame.mixer.music.load(_song_file_name)
    pygame.mixer.music.set_volume(0.2)
    print('Song playing:' + _song_file_name)
    pygame.mixer.music.play(0)  # -1 plays song for ever


def stop_song():
    pygame.mixer.music.stop()


def play_sound(name: str = "bell"):
    file = "./sound-files/effects/" + name + ".wav"
    try:
        sound = pygame.mixer.Sound(file)
        sound.set_volume(1.0)
        pygame.mixer.Channel(1).play(sound)
        print('Sound playing:' + file)
    except:
        raise FileNotFoundError


def init_mixer():
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(pygame.QUIT)


def play_new_musik_if_music_is_over(songs_to_play: list):
    for event in pygame.event.get():  # plays new music if music is over
        if event.type == pygame.QUIT:
            print("New Music")
            pygame.time.wait(250)
            play_random_song(songs_to_play)


def play_random_song(songs_to_play: list):
    play_song(random.choice(songs_to_play))


if __name__ == '__main__':
    pygame.init()
    init_mixer()
    play_random_song(_songs)
