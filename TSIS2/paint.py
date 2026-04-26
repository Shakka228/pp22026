import pygame
import sys
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
color = BLACK

# TOOLS
tool = "pencil"
brush_size = 2

# STATES
drawing = False
last_pos = None
start_pos = None

# TEXT TOOL
font = pygame.font.SysFont(None, 24)
text_input = ""
text_pos = None
text_active = False


# -------- FLOOD FILL --------
def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= WIDTH or py < 0 or py >= HEIGHT:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.extend([
            (px+1, py), (px-1, py),
            (px, py+1), (px, py-1)
        ])


# -------- SAVE --------
def save_canvas():
    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


# -------- MAIN LOOP --------
while True:
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # KEYBOARD
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2
            if event.key == pygame.K_2:
                brush_size = 5
            if event.key == pygame.K_3:
                brush_size = 10

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            # TEXT INPUT
            if text_active:
                if event.key == pygame.K_RETURN:
                    rendered = font.render(text_input, True, color)
                    canvas.blit(rendered, text_pos)
                    text_input = ""
                    text_active = False

                elif event.key == pygame.K_ESCAPE:
                    text_input = ""
                    text_active = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

        # MOUSE
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            if tool == "fill":
                flood_fill(canvas, *event.pos, color)

            if tool == "text":
                text_active = True
                text_pos = event.pos
                text_input = ""

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if tool == "line":
                pygame.draw.line(canvas, color, start_pos, event.pos, brush_size)

            if tool == "rect":
                rect = pygame.Rect(start_pos, (event.pos[0]-start_pos[0], event.pos[1]-start_pos[1]))
                pygame.draw.rect(canvas, color, rect, brush_size)

            if tool == "circle":
                radius = int(((event.pos[0]-start_pos[0])**2 + (event.pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, color, start_pos, radius, brush_size)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

    # -------- PREVIEW --------
    if drawing and tool in ["line", "rect", "circle"]:
        temp = canvas.copy()
        mouse_pos = pygame.mouse.get_pos()

        if tool == "line":
            pygame.draw.line(temp, color, start_pos, mouse_pos, brush_size)

        if tool == "rect":
            rect = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
            pygame.draw.rect(temp, color, rect, brush_size)

        if tool == "circle":
            radius = int(((mouse_pos[0]-start_pos[0])**2 + (mouse_pos[1]-start_pos[1])**2)**0.5)
            pygame.draw.circle(temp, color, start_pos, radius, brush_size)

        screen.blit(temp, (0, 0))

    # -------- TEXT PREVIEW --------
    if text_active:
        preview = font.render(text_input, True, color)
        screen.blit(preview, text_pos)

    pygame.display.flip()
    clock.tick(60)
