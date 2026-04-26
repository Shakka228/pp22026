import pygame
import pygame
import sys
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Pro")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

# -------- SETTINGS --------
color = (0, 0, 0)
brush_size = 2
tool = "pencil"

drawing = False
start_pos = None
last_pos = None

# -------- TEXT --------
font = pygame.font.SysFont(None, 24)
text_input = ""
text_pos = (0, 0)
text_active = False

# -------- UNDO --------
history = []

# -------- COLORS --------
palette = [
    (0,0,0), (255,0,0), (0,255,0), (0,0,255),
    (255,255,0), (255,165,0), (255,192,203), (128,0,128)
]

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
    print("Saved:", filename)
    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
        print("CTRL+S detected")   # DEBUG
        save_canvas()

# -------- MAIN LOOP --------
while True:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 50))

    # -------- DRAW PALETTE --------
    for i, col in enumerate(palette):
        pygame.draw.rect(screen, col, (10 + i*40, 10, 30, 30))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------- KEYBOARD --------
        if event.type == pygame.KEYDOWN:

            # tools
            if event.key == pygame.K_p: tool = "pencil"
            if event.key == pygame.K_l: tool = "line"
            if event.key == pygame.K_r: tool = "rect"
            if event.key == pygame.K_c: tool = "circle"
            if event.key == pygame.K_f: tool = "fill"
            if event.key == pygame.K_t: tool = "text"

            # brush size
            if event.key == pygame.K_1: brush_size = 2
            if event.key == pygame.K_2: brush_size = 5
            if event.key == pygame.K_3: brush_size = 10

            # undo
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if history:
                    canvas.blit(history.pop(), (0,0))

            # clear
            if event.key == pygame.K_x:
                history.append(canvas.copy())
                canvas.fill((255,255,255))

            # save
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            # text
            if text_active:
                if event.key == pygame.K_RETURN:
                    canvas.blit(font.render(text_input, True, color), text_pos)
                    text_input = ""
                    text_active = False
                elif event.key == pygame.K_ESCAPE:
                    text_input = ""
                    text_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        # -------- MOUSE DOWN --------
        if event.type == pygame.MOUSEBUTTONDOWN:

            # palette click
            for i, col in enumerate(palette):
                if pygame.Rect(10 + i*40, 10, 30, 30).collidepoint(event.pos):
                    color = col

            drawing = True
            start_pos = (event.pos[0], event.pos[1] - 50)
            last_pos = start_pos

            history.append(canvas.copy())

            if tool == "fill":
                flood_fill(canvas, start_pos[0], start_pos[1], color)

            if tool == "text":
                text_active = True
                text_pos = start_pos
                text_input = ""

        # -------- MOUSE UP --------
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = (event.pos[0], event.pos[1] - 50)

            if tool == "line":
                pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

            if tool == "rect":
                rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                pygame.draw.rect(canvas, color, rect, brush_size)

            if tool == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, color, start_pos, radius, brush_size)

        # -------- MOUSE MOTION --------
        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pencil":
                current_pos = (event.pos[0], event.pos[1] - 50)
                pygame.draw.line(canvas, color, last_pos, current_pos, brush_size)
                last_pos = current_pos

    # -------- PREVIEW --------
    if drawing and tool in ["line", "rect", "circle"]:
        temp = canvas.copy()
        mx, my = pygame.mouse.get_pos()
        mx, my = mx, my - 50

        if tool == "line":
            pygame.draw.line(temp, color, start_pos, (mx, my), brush_size)

        if tool == "rect":
            rect = pygame.Rect(start_pos, (mx-start_pos[0], my-start_pos[1]))
            pygame.draw.rect(temp, color, rect, brush_size)

        if tool == "circle":
            radius = int(((mx-start_pos[0])**2 + (my-start_pos[1])**2)**0.5)
            pygame.draw.circle(temp, color, start_pos, radius, brush_size)

        screen.blit(temp, (0, 50))

    # -------- TEXT PREVIEW --------
    if text_active:
        screen.blit(font.render(text_input, True, color), (text_pos[0], text_pos[1]+50))

    pygame.display.flip()
    clock.tick(60)