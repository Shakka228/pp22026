import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Player car
player = pygame.Rect(180, 500, 40, 60)

# Enemy car
enemy = pygame.Rect(random.randint(50, 310), -100, 40, 60)

# Coin
coin = pygame.Rect(random.randint(50, 310), -200, 20, 20)

coins = 0
speed = 5

running = True
while running:
    screen.fill((30, 30, 30))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.x < WIDTH - 40:
        player.x += 5

    # Enemy movement
    enemy.y += speed
    if enemy.y > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(50, 310)

    # Coin movement
    coin.y += speed
    if coin.y > HEIGHT:
        coin.y = -200
        coin.x = random.randint(50, 310)

    # Coin collision
    if player.colliderect(coin):
        coins += 1
        coin.y = -200
        coin.x = random.randint(50, 310)

    # Enemy collision
    if player.colliderect(enemy):
        print("Game Over")
        running = False

    # Draw objects
    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)
    pygame.draw.circle(screen, (255, 255, 0), coin.center, 10)

    # Show coins (top-right)
    text = font.render(f"Coins: {coins}", True, (255, 255, 255))
    screen.blit(text, (WIDTH - 120, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
