import pygame, random
from config import *
from db import *
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        self.snake = [(100,100)]
        self.dx, self.dy = CELL, 0

        self.food = self.spawn()
        self.poison = self.spawn()
        self.power = self.spawn_power()

        self.score = 0
        self.level = 1
        self.fps = BASE_FPS

        self.obstacles = []
        self.shield = False

    # ---------------- SPAWN ----------------
    def spawn(self):
        return (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )

    def spawn_power(self):
        return {
            "type": random.choice(["speed","slow","shield"]),
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

    # ---------------- MENU ----------------
    def menu(self):
        self.screen.fill((0,0,0))
        self.text("Snake Game", 120)
        self.text("Enter name: " + self.username, 200)
        self.text("ENTER - Play | L - Leaderboard", 260)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and self.username:
                    self.player_id = get_or_create_player(self.username)
                    self.best = best_score(self.player_id)
                    self.state = "game"
                    self.reset()

                elif e.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif e.key == pygame.K_l:
                    self.state = "leaderboard"
                else:
                    self.username += e.unicode

    # ---------------- GAME ----------------
    def game(self):
        while True:
            self.screen.fill((0,0,0))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP: self.dx,self.dy=0,-CELL
                    if e.key == pygame.K_DOWN: self.dx,self.dy=0,CELL
                    if e.key == pygame.K_LEFT: self.dx,self.dy=-CELL,0
                    if e.key == pygame.K_RIGHT: self.dx,self.dy=CELL,0

            head = (self.snake[0][0]+self.dx, self.snake[0][1]+self.dy)

            # collision
            if head in self.snake or head in self.obstacles:
                if self.shield:
                    self.shield = False
                else:
                    save_score(self.player_id, self.score, self.level)
                    self.state = "menu"
                    return

            self.snake.insert(0, head)

            # food
            if head == self.food:
                self.score += 1
                self.food = self.spawn()
            else:
                self.snake.pop()

            # poison
            if head == self.poison:
                self.snake = self.snake[:-2] if len(self.snake)>2 else self.snake[:1]
                self.poison = self.spawn()

            # power
            if head == self.power["pos"]:
                t = self.power["type"]
                if t == "speed": self.fps += 2
                if t == "slow": self.fps = max(5,self.fps-2)
                if t == "shield": self.shield = True
                self.power = self.spawn_power()

            # level + obstacles
            self.level = self.score // 5 + 1
            if self.level >= 3 and not self.obstacles:
                self.obstacles = [self.spawn() for _ in range(10)]

            # draw snake
            for s in self.snake:
                pygame.draw.rect(self.screen, self.settings["snake_color"], (*s,CELL,CELL))

            pygame.draw.rect(self.screen,(255,0,0),(*self.food,CELL,CELL))
            pygame.draw.rect(self.screen,(139,0,0),(*self.poison,CELL,CELL))
            pygame.draw.rect(self.screen,(0,255,255),(*self.power["pos"],CELL,CELL))

            for o in self.obstacles:
                pygame.draw.rect(self.screen,(120,120,120),(*o,CELL,CELL))

            self.text(f"Score:{self.score}",10)
            self.text(f"Level:{self.level}",40)
            self.text(f"Best:{self.best}",70)

            pygame.display.flip()
            self.clock.tick(self.fps)

    # ---------------- LEADERBOARD ----------------
    def leaderboard(self):
        data = get_top()

        while True:
            self.screen.fill((0,0,0))
            self.text("TOP 10", 50)

            y = 120
            for i,row in enumerate(data):
                self.text(f"{i+1}. {row[0]} {row[1]}", y)
                y += 30

            self.text("ESC - back", 500)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    return

            pygame.display.flip()

    # ---------------- TEXT ----------------
    def text(self, txt, y):
        self.screen.blit(self.font.render(txt, True, (255,255,255)), (20,y))