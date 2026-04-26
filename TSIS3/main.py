import pygame, sys, random, json

# ---------- INITIALIZATION ----------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer - Power-Up Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# ---------- HELPERS ----------
def draw_text(text, x, y):
    screen.blit(font.render(text, True, (255, 255, 255)), (x, y))

def load_json(file, default):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except:
        print(f"Missing image: {path}")
        return None

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        print(f"Missing sound: {path}")
        return None

# ---------- SETTINGS ----------
def validate_settings(s):
    if s.get("difficulty") not in ["easy", "medium", "hard"]:
        s["difficulty"] = "medium"
    if not isinstance(s.get("sound"), bool):
        s["sound"] = True
    if s.get("car_color") not in ["yellow", "blue", "red", "green"]:
        s["car_color"] = "yellow"
    return s

settings = validate_settings(load_json("settings.json", {
    "difficulty": "medium",
    "sound": True,
    "car_color": "yellow"
}))
save_json("settings.json", settings)

leaderboard = load_json("leaderboard.json", [])

# ---------- ASSETS ----------
try:
    pygame.mixer.music.load("assets/music.mp3")
    pygame.mixer.music.set_volume(0.5 if settings["sound"] else 0)
    pygame.mixer.music.play(-1)
except:
    print("No music file found.")

crash_sound = load_sound("assets/crash.wav")
pickup_sound = load_sound("assets/pickup.wav")

enemy_img = load_image("assets/enemy.png", (40, 60))
nitro_img = load_image("assets/nitro.png", (30, 30))
shield_img = load_image("assets/shield.png", (30, 30))
repair_img = load_image("assets/repair.png", (30, 30))
coin_img = load_image("assets/coin.png", (30, 30))
oil_img = load_image("assets/oil.png", (40, 40))
boost_img = load_image("assets/boost.png", (40, 40))

# ---------- GAME OBJECTS ----------
player = pygame.Rect(250, 600, 40, 60)
vel_x = vel_y = 0
ROAD_LEFT, ROAD_RIGHT = 100, 400

color_map = {
    "yellow": (255, 255, 0),
    "blue": (0, 100, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0)
}

# ---------- STATE VARIABLES ----------
state = "menu"
username = ""
input_text = ""
score = 0
score_saved = False

obstacles = []
powerups = []
hazards = []

shield = False
nitro_ready = False
nitro_active = False
nitro_timer = 0
spin_timer = 0  # Timer for oil spin-out effect

# ---------- MAIN LOOP ----------
while True:
    screen.fill((30, 30, 30))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = "input"

        elif state == "input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    username = input_text or "Player"
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
                    nitro_timer = current_time

        elif state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    obstacles.clear(); powerups.clear(); hazards.clear()
                    score = 0; score_saved = False; shield = False; nitro_ready = False
                    state = "game"
                if event.key == pygame.K_m:
                    state = "menu"

    # ---------- MENU STATE ----------
    if state == "menu":
        draw_text("TSIS3 RACER", 170, 100)
        draw_text("Click to Play", 160, 200)
        draw_text("L - Leaderboard", 150, 260)
        draw_text("S - Settings", 170, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_l]: state = "leaderboard"
        if keys[pygame.K_s]: state = "settings"

    # ---------- SETTINGS STATE ----------
    elif state == "settings":
        draw_text(f"Difficulty: {settings['difficulty']}", 150, 200)
        draw_text(f"Sound: {settings['sound']}", 150, 240)
        draw_text(f"Color: {settings['car_color']}", 150, 280)
        draw_text("D (Diff) | S (Sound) | C (Color) | ESC", 80, 350)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            settings["difficulty"] = "medium" if settings["difficulty"] == "easy" else "hard" if settings["difficulty"] == "medium" else "easy"
            save_json("settings.json", settings)
            pygame.time.delay(200)
        if keys[pygame.K_s]:
            settings["sound"] = not settings["sound"]
            pygame.mixer.music.set_volume(0.5 if settings["sound"] else 0)
            save_json("settings.json", settings)
            pygame.time.delay(200)
        if keys[pygame.K_c]:
            colors = list(color_map.keys())
            i = colors.index(settings["car_color"])
            settings["car_color"] = colors[(i + 1) % len(colors)]
            save_json("settings.json", settings)
            pygame.time.delay(200)
        if keys[pygame.K_ESCAPE]:
            state = "menu"

    # ---------- GAMEPLAY STATE ----------
    elif state == "game":
        speed = {"easy": 4, "medium": 6, "hard": 9}[settings["difficulty"]]

        # Movement with Spin-out Logic
        keys = pygame.key.get_pressed()
        if current_time - spin_timer > 600:  # Allow control if not spinning
            if keys[pygame.K_LEFT]: vel_x -= 0.6
            if keys[pygame.K_RIGHT]: vel_x += 0.6
            if keys[pygame.K_UP]: vel_y -= 0.6
            if keys[pygame.K_DOWN]: vel_y += 0.6
        else:
            # Player is spinning; drift randomly
            player.x += random.randint(-2, 2)

        vel_x *= 0.9; vel_y *= 0.9
        player.x += int(vel_x); player.y += int(vel_y)
        player.clamp_ip(pygame.Rect(ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

        # Spawning Logic
        if random.random() < 0.03 and len(obstacles) < 5:
            obstacles.append(pygame.Rect(random.randint(ROAD_LEFT, ROAD_RIGHT - 40), -60, 40, 60))
        if random.random() < 0.015:
            hazards.append({"rect": pygame.Rect(random.randint(ROAD_LEFT, ROAD_RIGHT - 40), -40, 40, 40), "type": random.choice(["oil", "boost"])})
        if random.random() < 0.012:
            powerups.append({"rect": pygame.Rect(random.randint(ROAD_LEFT, ROAD_RIGHT - 30), -30, 30, 30), "type": random.choice(["nitro", "shield", "repair", "coin"])})

        # Process Hazards (Oil/Boost)
        for h in hazards[:]:
            h["rect"].y += speed
            img = oil_img if h["type"] == "oil" else boost_img
            if img: screen.blit(img, h["rect"].topleft)
            
            if player.colliderect(h["rect"]):
                if h["type"] == "oil":
                    spin_timer = current_time
                    vel_x = random.choice([-12, 12])
                else:
                    vel_y -= 10 # Speed boost
                hazards.remove(h)
            elif h["rect"].top > HEIGHT: hazards.remove(h)

        # Process Powerups (Nitro/Shield/Repair/Coin)
        for p in powerups[:]:
            p["rect"].y += speed
            img_map = {"nitro": nitro_img, "shield": shield_img, "repair": repair_img, "coin": coin_img}
            if img_map[p["type"]]: screen.blit(img_map[p["type"]], p["rect"].topleft)

            if player.colliderect(p["rect"]):
                if pickup_sound: pickup_sound.play()
                if p["type"] == "nitro": nitro_ready = True
                elif p["type"] == "shield": shield = True
                elif p["type"] == "repair": obstacles.clear()
                elif p["type"] == "coin": score += 500
                powerups.remove(p)
            elif p["rect"].top > HEIGHT: powerups.remove(p)

        # Process Obstacles (Enemies)
        for o in obstacles[:]:
            o.y += speed
            if enemy_img: screen.blit(enemy_img, o.topleft)
            else: pygame.draw.rect(screen, (255, 0, 0), o)

            if player.colliderect(o):
                if shield:
                    shield = False
                    obstacles.remove(o)
                    if crash_sound: crash_sound.play()
                else:
                    if crash_sound: crash_sound.play()
                    state = "game_over"
            elif o.top > HEIGHT: obstacles.remove(o)

        # Nitro Active Logic
        if nitro_active:
            vel_y -= 0.8
            if current_time - nitro_timer > 3000: nitro_active = False

        # Drawing Player & Shield Visual
        pygame.draw.rect(screen, color_map[settings["car_color"]], player)
        if shield:
            pygame.draw.circle(screen, (0, 180, 255), player.center, 45, 3)

        score += 1
        draw_text(f"{username} | Score: {score}", 10, 10)
        if nitro_ready: draw_text("NITRO READY (Space)", 10, 40)

    # ---------- REMAINING STATES ----------
    elif state == "input":
        draw_text("Enter Name:", 150, 200)
        draw_text(input_text, 150, 250)
        draw_text("Press ENTER", 150, 300)

    elif state == "game_over":
        if not score_saved:
            leaderboard.append({"name": username, "score": score})
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
            save_json("leaderboard.json", leaderboard)
            score_saved = True
        draw_text("GAME OVER", 170, 200)
        draw_text(f"Final Score: {score}", 160, 240)
        draw_text("R - Retry | M - Menu", 140, 300)

    elif state == "leaderboard":
        draw_text("TOP 10 RACERS", 160, 50)
        for i, e in enumerate(leaderboard):
            draw_text(f"{i+1}. {e['name']} - {e['score']}", 120, 100 + (i * 35))
        draw_text("Press ESC for Menu", 140, 600)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]: state = "menu"

    pygame.display.flip()
    clock.tick(60)