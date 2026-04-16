import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

hand = pygame.image.load("images/mickey_hand.png")
hand = pygame.transform.scale(hand, (200, 10))

center = (WIDTH // 2, HEIGHT // 2)

running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    sec = now.second
    minute = now.minute

    sec_angle = -sec * 6
    min_angle = -minute * 6

    sec_hand = pygame.transform.rotate(hand, sec_angle)
    min_hand = pygame.transform.rotate(hand, min_angle)

    screen.blit(min_hand, min_hand.get_rect(center=center))
    screen.blit(sec_hand, sec_hand.get_rect(center=center))

    pygame.display.flip()
    clock.tick(1)

pygame.quit()