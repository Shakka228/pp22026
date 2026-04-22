import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

block = 20
snake = [(200, 200)]
dx, dy = block, 0

food = (100, 100)
score = 0
level = 1
speed = 8

def generate_food():
    while True:
        f = (random.randrange(0, WIDTH, block),
             random.randrange(0, HEIGHT, block))
        if f not in snake:
            return f

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        dx, dy = 0, -block
    if keys[pygame.K_DOWN]:
        dx, dy = 0, block
    if keys[pygame.K_LEFT]:
        dx, dy = -block, 0
    if keys[pygame.K_RIGHT]:
        dx, dy = block, 0

    # Move snake
    head = (snake[0][0] + dx, snake[0][1] + dy)

    # Border collision
    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT):
        print("Game Over")
        break

    # Self collision
    if head in snake:
        print("Game Over")
        break

    snake.insert(0, head)

    # Eat food
    if head == food:
        score += 1
        food = generate_food()

        # Level system
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Draw snake
    for part in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*part, block, block))

    # Draw food
    pygame.draw.rect(screen, (255, 0, 0), (*food, block, block))

    # UI
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10,30))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
