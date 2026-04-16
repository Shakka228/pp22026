import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500, 200))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)

music_folder = "music"
playlist = os.listdir(music_folder)
index = 0

def play_music():
    if playlist:
        pygame.mixer.music.load(os.path.join(music_folder, playlist[index]))
        pygame.mixer.music.play()

running = True

while running:
    screen.fill((0, 0, 0))

    if playlist:
        text = font.render(f"Track: {playlist[index]}", True, (255, 255, 255))
        screen.blit(text, (20, 80))
    else:
        text = font.render("No music files!", True, (255, 255, 255))
        screen.blit(text, (20, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_music()
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:
                index = (index + 1) % len(playlist)
                play_music()
            elif event.key == pygame.K_b:
                index = (index - 1) % len(playlist)
                play_music()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()