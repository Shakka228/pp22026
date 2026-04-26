import pygame
import sys
import random
import json

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

# -------- BACKGROUND MUSIC --------
try:
    pygame.mixer.music.load("assets/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Missing background music")

# -------- SAFE LOADERS --------
def load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except:
        print("Missing image:", path)
        return None

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        print("Missing sound:", path)
        return None

# -------- ASSETS --------
player_img = load_image("assets/player.png", (40, 60))
enemy_img = load_image("assets/enemy.png", (40, 60))

crash_sound = load_sound("assets/crash.wav")
nitro_sound = load_sound("assets/nitro.wav")
pickup_sound = load_sound("assets/pickup.wav")

# -------- JSON --------
def load_json(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

settings = load_json("settings.json", {"difficulty": "medium"})
leaderboard = load_json("leaderboard.json", [])

# -------- PLAYER --------
player = pygame.Rect(WIDTH//2, HEIGHT-100, 40, 60)

vel_x = 0
vel_y = 0
acceleration = 0.5
friction = 0.9
max_speed = 6

ROAD_LEFT = 100
ROAD_RIGHT = 400

# -------- STATE --------
state = "menu"
username = ""
input_text = ""

obstacles = []
powerups = []

score = 0
score_saved = False

# -------- POWERUPS --------
shield = False
nitro_ready = False
nitro_active = False
nitro_start = 0
nitro_duration = 3000

# -------- BUTTON --------
class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 200, 50)

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = (120,120,120) if self.rect.collidepoint(mouse) else (70,70,70)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        txt = font.render(self.text, True, (255,255,255))
        screen.blit(txt, (self.rect.x + 40, self.rect.y + 10))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

play_btn = Button("Play", 150, 200)
leader_btn = Button("Leaderboard", 150, 270)
settings_btn = Button("Settings", 150, 340)

# -------- HELPERS --------
def draw_text(text, x, y):
    screen.blit(font.render(text, True, (255,255,255)), (x,y))

def spawn_obstacle():
    while True:
        x = random.randint(120, 360)
        rect = pygame.Rect(x, -60, 40, 60)
        if abs(rect.x - player.x) > 80:
            return rect

def spawn_powerup():
    return {
        "rect": pygame.Rect(random.randint(120,360), -40, 30, 30),
        "type": random.choice(["nitro", "shield", "repair"])
    }

# -------- LOOP --------
while True:
    screen.fill((20,20,20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.clicked(event.pos):
                    state = "input"
                    input_text = ""
                if leader_btn.clicked(event.pos):
                    state = "leaderboard"
                if settings_btn.clicked(event.pos):
                    state = "settings"

        elif state == "input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    username = input_text if input_text else "Player"
                    state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 12:
                        input_text += event.unicode

        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and nitro_ready:
                    nitro_active = True
                    nitro_ready = False
                    nitro_start = pygame.time.get_ticks()
                    if nitro_sound:
                        nitro_sound.play()

        elif state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    obstacles.clear()
                    powerups.clear()
                    score = 0
                    score_saved = False
                    state = "game"
                if event.key == pygame.K_m:
                    state = "menu"

    # -------- MENU --------
    if state == "menu":
        draw_text("TSIS3 RACER", 150, 100)
        play_btn.draw()
        leader_btn.draw()
        settings_btn.draw()

    # -------- INPUT --------
    elif state == "input":
        draw_text("Enter Name", 160, 200)
        box = pygame.Rect(120, 260, 260, 50)
        pygame.draw.rect(screen, (255,255,255), box, 2)
        txt = font.render(input_text, True, (255,255,255))
        screen.blit(txt, (box.x + 10, box.y + 10))
        draw_text("ENTER to start", 140, 330)

    # -------- SETTINGS --------
    elif state == "settings":
        draw_text("Settings", 180,150)
        draw_text(f"Difficulty: {settings['difficulty']}", 120,220)
        draw_text("Press D to change", 120,260)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if settings["difficulty"] == "easy":
                settings["difficulty"] = "medium"
            elif settings["difficulty"] == "medium":
                settings["difficulty"] = "hard"
            else:
                settings["difficulty"] = "easy"

            save_json("settings.json", settings)
            pygame.time.delay(200)

        if keys[pygame.K_ESCAPE]:
            state = "menu"

    # -------- GAME --------
    elif state == "game":

        difficulty = settings["difficulty"]
        if difficulty == "easy":
            speed, spawn_rate = 4, 0.02
        elif difficulty == "medium":
            speed, spawn_rate = 5, 0.03
        else:
            speed, spawn_rate = 7, 0.05

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: vel_x -= acceleration
        if keys[pygame.K_RIGHT]: vel_x += acceleration
        if keys[pygame.K_UP]: vel_y -= acceleration
        if keys[pygame.K_DOWN]: vel_y += acceleration

        vel_x *= friction
        vel_y *= friction

        player.x += int(vel_x)
        player.y += int(vel_y)

        player.left = max(player.left, ROAD_LEFT)
        player.right = min(player.right, ROAD_RIGHT)

        # spawn
        if random.random() < spawn_rate and len(obstacles) < 5:
            obstacles.append(spawn_obstacle())

        if random.random() < 0.01:
            powerups.append(spawn_powerup())

        # obstacles
        for obs in obstacles[:]:
            obs.y += speed
            if obs.top > HEIGHT:
                obstacles.remove(obs)
                continue

            if enemy_img:
                screen.blit(enemy_img, obs.topleft)
            else:
                pygame.draw.rect(screen, (255,0,0), obs)

            if player.colliderect(obs):
                if crash_sound:
                    crash_sound.play()

                if shield:
                    shield = False
                    obstacles.remove(obs)
                else:
                    state = "game_over"

        # powerups
        for p in powerups[:]:
            p["rect"].y += speed
            pygame.draw.rect(screen, (0,255,255), p["rect"])

            if player.colliderect(p["rect"]):
                if pickup_sound:
                    pickup_sound.play()

                if p["type"] == "nitro":
                    nitro_ready = True
                elif p["type"] == "shield":
                    shield = True
                elif p["type"] == "repair":
                    obstacles.clear()

                powerups.remove(p)

        # nitro
        if nitro_active:
            vel_y -= 0.3
            if pygame.time.get_ticks() - nitro_start > nitro_duration:
                nitro_active = False

        # player
        if player_img:
            screen.blit(player_img, player.topleft)
        else:
            pygame.draw.rect(screen, (255,255,0), player)

        score += 1
        draw_text(username, 10,10)
        draw_text(f"Score: {score}", 10,40)
        draw_text(f"Nitro: {nitro_ready}", 10,70)
        draw_text(f"Shield: {shield}", 10,100)

    # -------- GAME OVER --------
    elif state == "game_over":
        if not score_saved:
            leaderboard.append({"name": username, "score": score})
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
            save_json("leaderboard.json", leaderboard)
            score_saved = True

        draw_text("GAME OVER", 160,200)
        draw_text("R - Retry", 170,250)
        draw_text("M - Menu", 170,300)

    # -------- LEADERBOARD --------
    elif state == "leaderboard":
        draw_text("Leaderboard", 170,100)
        y = 150
        for i, e in enumerate(leaderboard):
            draw_text(f"{i+1}. {e['name']} - {e['score']}", 120, y)
            y += 30

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            state = "menu"

    pygame.display.flip()
    clock.tick(60)