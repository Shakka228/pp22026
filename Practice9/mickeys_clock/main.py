import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

# Load ORIGINAL image once (important!)
original_hand = pygame.image.load("images/mickey_hand.png").convert_alpha()

# Scale only once (not every frame)
original_hand = pygame.transform.scale(original_hand, (200, 10))

center = (WIDTH // 2, HEIGHT // 2)

running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen every frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    sec = now.second
    minute = now.minute

    # Calculate angles
    sec_angle = -sec * 6
    min_angle = -(minute * 6 + sec * 0.1)  # smoother minute hand

    # Always rotate from ORIGINAL image
    sec_hand = pygame.transform.rotate(original_hand, sec_angle)
    min_hand = pygame.transform.rotate(original_hand, min_angle)

    # Get centered rectangles AFTER rotation
    sec_rect = sec_hand.get_rect(center=center)
    min_rect = min_hand.get_rect(center=center)

    # Draw hands
    screen.blit(min_hand, min_rect)
    screen.blit(sec_hand, sec_rect)

    pygame.display.flip()

    # Higher FPS = smoother rendering
    clock.tick(60)

pygame.quit()