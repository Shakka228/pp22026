import pygame, random
from config import *
from db import *
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake")

        self.font = pygame.font.SysFont(None, 28)
        self.clock = pygame.time.Clock()

        self.settings = load_settings()

        self.state = "menu"
        self.username = ""
        self.player_id = None
        self.best = 0

        self.reset()

    # ---------------- RESET ----------------
    def reset(self):
        self.snake = [(100, 100)]
        self.dx, self.dy = CELL, 0

        self.score = 0
        self.level = 1

        self.obstacles = []

        self.food = self.spawn()
        self.poison = self.spawn()

        self.power = None
        self.power_spawn_time = 0
        self.active_power = None
        self.power_start_time = 0

        self.fps = BASE_FPS

    # ---------------- SAFE SPAWN ----------------
    def spawn(self):
        while True:
            pos = (
                random.randrange(0, WIDTH, CELL),
                random.randrange(0, HEIGHT, CELL)
            )
            if pos not in self.snake and pos not in self.obstacles:
                return pos

    def spawn_power(self):
        return {
            "type": random.choice(["speed", "slow", "shield"]),
            "pos": self.spawn()
        }

    # ---------------- RUN ----------------
    def run(self):
        while True:
            if self.state == "menu":
                self.menu()
            elif self.state == "game":
                self.game()
            elif self.state == "leaderboard":
                self.leaderboard()
            elif self.state == "game_over":
                self.game_over()

    # ---------------- MENU ----------------
    def menu(self):
        while True:
            self.screen.fill((0, 0, 0))

            self.text("SNAKE GAME", 120)
            self.text("Enter username:", 180)
            self.text(self.username, 220)
            self.text("ENTER - Play | L - Leaderboard", 300)

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN and self.username:
                        self.player_id = get_or_create_player(self.username)
                        self.best = best_score(self.player_id)
                        self.reset()
                        self.state = "game"
                        return

                    elif e.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]

                    elif e.key == pygame.K_l:
                        self.state = "leaderboard"
                        return

                    else:
                        if len(self.username) < 15:
                            self.username += e.unicode

    # ---------------- GAME ----------------
    def game(self):
        while True:
            self.screen.fill((0, 0, 0))
            now = pygame.time.get_ticks()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP and self.dy == 0:
                        self.dx, self.dy = 0, -CELL
                    if e.key == pygame.K_DOWN and self.dy == 0:
                        self.dx, self.dy = 0, CELL
                    if e.key == pygame.K_LEFT and self.dx == 0:
                        self.dx, self.dy = -CELL, 0
                    if e.key == pygame.K_RIGHT and self.dx == 0:
                        self.dx, self.dy = CELL, 0

            head = (self.snake[0][0] + self.dx, self.snake[0][1] + self.dy)

            # ---- BORDER ----
            if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
                if self.active_power == "shield":
                    self.active_power = None
                else:
                    save_score(self.player_id, self.score, self.level)
                    self.best = max(self.best, self.score)
                    self.state = "game_over"
                    return

            # ---- SELF / OBSTACLE ----
            if head in self.snake or head in self.obstacles:
                if self.active_power == "shield":
                    self.active_power = None
                else:
                    save_score(self.player_id, self.score, self.level)
                    self.best = max(self.best, self.score)
                    self.state = "game_over"
                    return

            self.snake.insert(0, head)

            # ---- FOOD ----
            if head == self.food:
                self.score += 1
                self.food = self.spawn()
            else:
                self.snake.pop()

            # ---- POISON ----
            if head == self.poison:
                self.snake = self.snake[:-2]

                if len(self.snake) <= 1:
                    save_score(self.player_id, self.score, self.level)
                    self.best = max(self.best, self.score)
                    self.state = "game_over"
                    return

                self.poison = self.spawn()

            # ---- POWER SPAWN ----
            if self.power is None:
                self.power = self.spawn_power()
                self.power_spawn_time = now
            elif now - self.power_spawn_time > 8000:
                self.power = None

            # ---- POWER PICKUP ----
            if self.power and head == self.power["pos"]:
                self.active_power = self.power["type"]
                self.power_start_time = now
                self.power = None

            # ---- LEVEL ----
            self.level = self.score // 5 + 1

            # ---- SPEED SYSTEM (FIXED) ----
            base_speed = BASE_FPS + self.level

            if self.active_power == "speed":
                self.fps = base_speed + 4
            elif self.active_power == "slow":
                self.fps = max(3, base_speed - 3)
            else:
                self.fps = base_speed

            # ---- POWER EXPIRE ----
            if self.active_power and now - self.power_start_time > 5000:
                self.active_power = None

            # ---- OBSTACLES ----
            if self.level >= 3 and not self.obstacles:
                for _ in range(10):
                    self.obstacles.append(self.spawn())

            # ---- DRAW ----
            for s in self.snake:
                pygame.draw.rect(self.screen, self.settings["snake_color"], (*s, CELL, CELL))

            pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, CELL, CELL))
            pygame.draw.rect(self.screen, (139, 0, 0), (*self.poison, CELL, CELL))

            if self.power:
                pygame.draw.rect(self.screen, (0, 255, 255), (*self.power["pos"], CELL, CELL))

            for o in self.obstacles:
                pygame.draw.rect(self.screen, (120, 120, 120), (*o, CELL, CELL))

            self.text(f"Score: {self.score}", 10)
            self.text(f"Level: {self.level}", 40)
            self.text(f"Best: {self.best}", 70)

            pygame.display.flip()
            self.clock.tick(self.fps)

    # ---------------- GAME OVER ----------------
    def game_over(self):
        while True:
            self.screen.fill((0, 0, 0))

            self.text("GAME OVER", 150)
            self.text(f"Score: {self.score}", 220)
            self.text(f"Level: {self.level}", 260)
            self.text(f"Best: {self.best}", 300)
            self.text("R - Retry | ESC - Menu", 360)

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        self.reset()
                        self.state = "game"
                        return
                    if e.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        return

    # ---------------- LEADERBOARD ----------------
    def leaderboard(self):
        data = get_top()

        while True:
            self.screen.fill((0, 0, 0))
            self.text("TOP 10", 50)

            y = 120
            for i, row in enumerate(data):
                username, score, level, date = row
                date_str = date.strftime("%Y-%m-%d")
                self.text(f"{i+1}. {username} | {score} | L{level} | {date_str}", y)
                y += 30

            self.text("ESC - back", 520)

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    return

    # ---------------- TEXT ----------------
    def text(self, txt, y):
        img = self.font.render(txt, True, (255, 255, 255))
        self.screen.blit(img, (20, y))