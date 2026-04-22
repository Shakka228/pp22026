import pygame

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

clock = pygame.time.Clock()

# Canvas (separate surface so drawings stay)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# Default settings
color = (0, 0, 0)
tool = "draw"
drawing = False
start_pos = None

# Colors palette
colors = [
    (0, 0, 0), (255, 0, 0),
    (0, 255, 0), (0, 0, 255),
    (255, 255, 0)
]

# Font
font = pygame.font.SysFont("Arial", 18)

running = True
while running:
    screen.blit(canvas, (0, 0))

    # Draw color palette
    for i, col in enumerate(colors):
        pygame.draw.rect(screen, col, (10 + i*40, 10, 30, 30))

    # Show current tool
    tool_text = font.render(f"Tool: {tool}", True, (0, 0, 0))
    screen.blit(tool_text, (10, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            # Check color selection
            for i, col in enumerate(colors):
                rect = pygame.Rect(10 + i*40, 10, 30, 30)
                if rect.collidepoint(event.pos):
                    color = col

        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            mx, my = pygame.mouse.get_pos()

            # Draw rectangle
            if tool == "rect" and start_pos:
                x, y = start_pos
                pygame.draw.rect(canvas, color, (x, y, mx-x, my-y), 2)

            # Draw circle
            if tool == "circle" and start_pos:
                x, y = start_pos
                radius = int(((mx-x)**2 + (my-y)**2)**0.5)
                pygame.draw.circle(canvas, color, (x, y), radius, 2)

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                tool = "draw"
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_e:
                tool = "eraser"

    # Drawing while holding mouse
    if drawing:
        mx, my = pygame.mouse.get_pos()

        if tool == "draw":
            pygame.draw.circle(canvas, color, (mx, my), 5)

        elif tool == "eraser":
            # Eraser = draw with white color
            pygame.draw.circle(canvas, (255, 255, 255), (mx, my), 12)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
