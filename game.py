import pygame, random, sys
from config import *
from db import *
from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.settings = load_settings()
        self.state = "menu"
        self.username = ""
        self.player_id = None
        self.best = 0

    def draw_text(self, text, y):
        t = self.font.render(text, True, (255,255,255))
        self.screen.blit(t, (50,y))

    def run(self):
        while True:
            self.screen.fill((0,0,0))

            if self.state == "menu": self.menu()
            elif self.state == "settings": self.settings_screen()
            elif self.state == "leaderboard": self.leaderboard()
            elif self.state == "game": self.play()
            elif self.state == "gameover": self.game_over()

            pygame.display.flip()

    def menu(self):
        self.draw_text("Enter username: " + self.username, 200)
        self.draw_text("ENTER - play | L - leaderboard | S - settings", 250)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and self.username:
                    self.player_id = get_or_create_player(self.username)
                    self.best = best_score(self.player_id)
                    self.state = "game"
                elif e.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif e.key == pygame.K_l:
                    self.state = "leaderboard"
                elif e.key == pygame.K_s:
                    self.state = "settings"
                else:
                    self.username += e.unicode

    def settings_screen(self):
        self.draw_text(f"Grid: {self.settings['grid']} (G)",150)
        self.draw_text(f"Sound: {self.settings['sound']} (M)",180)
        self.draw_text("R/B - color",210)
        self.draw_text("ESC - save",250)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_g: self.settings['grid'] = not self.settings['grid']
                if e.key == pygame.K_m: self.settings['sound'] = not self.settings['sound']
                if e.key == pygame.K_r: self.settings['snake_color']=[255,0,0]
                if e.key == pygame.K_b: self.settings['snake_color']=[0,0,255]
                if e.key == pygame.K_ESCAPE:
                    save_settings(self.settings)
                    self.state = "menu"

    def leaderboard(self):
        data = get_top()
        y=100
        for i,row in enumerate(data):
            self.draw_text(f"{i+1}. {row[0]} {row[1]}", y)
            y+=30

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                self.state="menu"

    def play(self):
        snake=[(100,100)]
        dx,dy=CELL,0
        food=(200,200)
        score=0
        level=1
        fps=BASE_FPS

        while True:
            self.screen.fill((0,0,0))

            for e in pygame.event.get():
                if e.type==pygame.QUIT: sys.exit()
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_UP: dx,dy=0,-CELL
                    if e.key==pygame.K_DOWN: dx,dy=0,CELL
                    if e.key==pygame.K_LEFT: dx,dy=-CELL,0
                    if e.key==pygame.K_RIGHT: dx,dy=CELL,0

            head=(snake[0][0]+dx, snake[0][1]+dy)

            if head in snake or not(0<=head[0]<WIDTH and 0<=head[1]<HEIGHT):
                save_score(self.player_id,score,level)
                self.state="gameover"
                return

            snake.insert(0,head)

            if head==food:
                score+=1
                food=(random.randrange(0,WIDTH,CELL),random.randrange(0,HEIGHT,CELL))
            else:
                snake.pop()

            for s in snake:
                pygame.draw.rect(self.screen, self.settings['snake_color'], (*s,CELL,CELL))

            pygame.draw.rect(self.screen,(255,0,0),(*food,CELL,CELL))

            self.draw_text(f"Score: {score}",10)
            self.draw_text(f"Best: {self.best}",40)

            pygame.display.flip()
            self.clock.tick(fps)

    def game_over(self):
        self.draw_text("GAME OVER",200)
        self.draw_text("ESC - menu",250)

        for e in pygame.event.get():
            if e.type==pygame.QUIT: sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                self.state="menu"
