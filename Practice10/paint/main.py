import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

color = (0, 0, 0)
tool = "draw"

colors = [(255,0,0), (0,255,0), (0,0,255), (0,0,0)]

drawing = False
start_pos = None

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

running = True
while running:
    screen.blit(canvas, (0, 0))

    # Draw color palette
    for i, col in enumerate(colors):
        pygame.draw.rect(screen, col, (10 + i*40, 10, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            # Color selection
            for i, col in enumerate(colors):
                rect = pygame.Rect(10 + i*40, 10, 30, 30)
                if rect.collidepoint(event.pos):
                    color = col

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if tool == "rect" and start_pos:
                x, y = start_pos
                mx, my = pygame.mouse.get_pos()
                pygame.draw.rect(canvas, color, (x, y, mx-x, my-y), 2)

            if tool == "circle" and start_pos:
                x, y = start_pos
                mx, my = pygame.mouse.get_pos()
                radius = int(((mx-x)**2 + (my-y)**2)**0.5)
                pygame.draw.circle(canvas, color, (x, y), radius, 2)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_e:
                tool = "eraser"
            if event.key == pygame.K_d:
                tool = "draw"

    if drawing:
        mx, my = pygame.mouse.get_pos()

        if tool == "draw":
            pygame.draw.circle(canvas, color, (mx, my), 5)

        elif tool == "eraser":
            pygame.draw.circle(canvas, (255,255,255), (mx, my), 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
