# imports
import sys, time, random
import pygame
from pygame.locals import *
import pickle

### TOP SCORE ###

# Function to save top score to file
def save_top_score(score):
    with open('space_impact_top_score.pkl', 'wb') as f:
        pickle.dump(score, f)

# Function to load top score from file
def load_top_score():
    try:
        with open('space_impact_top_score.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return 0

ALL_TIME_TOP_SCORE = load_top_score()

### INITIATION AND DISPLAY ###

# initiation
pygame.init()

# FPS setting
FPS = 60
FramePerSec = pygame.time.Clock()

# colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SPEED = 3
asteroids_destroyed = 0

# screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption('Space Impact (Alibek\'s version)')
FONT = pygame.font.Font(None, 36)

### CLASSES AND SETTINGS ###

# class - Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        image = pygame.image.load(settings['image'])
        self.height = settings['height']
        self.width = settings['width']
        self.speed = settings['speed']
        self.health = settings['max_health']
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, random.randint(40, SCREEN_HEIGHT-40))

    def move(self):
        self.rect.move_ip(-self.speed, 0)
        if (self.rect.left < 0):
            self.kill()
        #     self.rect.left = SCREEN_WIDTH
        #     self.rect.center = (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            B = Bullets(self.rect.center)  
            bullets.add(B)
            all_sprites.add(B)
            global asteroids_destroyed
            asteroids_destroyed += 1
            self.kill()

    def draw_rect(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 1)

# class - Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        super().__init__() 
        image = pygame.image.load('images/player_rocket.png')
        self.image = pygame.transform.scale(image, (100, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT/2)
        self.attack = 1
        self.bullets = 100

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,7)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-7, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(7, 0)

    def shoot(self):
        if self.bullets > 0:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                projectile = Projectile(self.rect.center)
                all_sprites.add(projectile)
                projectiles.add(projectile)
                self.bullets -= 1

    def draw_rect(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 1)

# projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        image = pygame.image.load('images/projectile.png')
        self.image = pygame.transform.scale(image, (5, 3))
        self.rect = self.image.get_rect()
        self.rect.center = position
    def move(self):
        self.rect.move_ip(10, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# pickable bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        image = pygame.image.load('images/box.png')
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = position
    def move(self):
        self.rect.move_ip(-5, 0)
        if self.rect.left < 0:
            self.kill()

# enemy settings
asteroid_small_settings = {
    'image': 'images/asteroid01.png',
    'height': 60,
    'width': 60,
    'speed': 5,
    'max_health': 10
}

asteroid_large_settings = {
    'image': 'images/asteroid02.png',
    'height': 100,
    'width': 100,
    'speed': 3,
    'max_health': 20
}

# setting up sprites
P1 = Player()
E1 = Enemy(asteroid_small_settings)
E2 = Enemy(asteroid_large_settings)
# creating sprites groups
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)
projectiles = pygame.sprite.Group()
bullets = pygame.sprite.Group()

### FUNCTIONS ###

game_running = False

def reset_game(enemies, all_sprites):
    global asteroids_destroyed
    asteroids_destroyed = 0
    P1.rect.center = (100, SCREEN_HEIGHT/2)
    P1.bullets = 100
    E1 = Enemy(asteroid_small_settings)
    E2 = Enemy(asteroid_large_settings)
    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(E2)
    enemies.add(E1)
    enemies.add(E2)

def run_game():
    global game_running
    while game_running:
        
        ### MAIN GAME LOOP ###

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        DISPLAYSURF.fill(BLACK)

        # shows number of bullets
        bullets_text = FONT.render(f"Bullets: {P1.bullets}", True, (255, 255, 255))
        DISPLAYSURF.blit(bullets_text, (10, 1))
        # show number of destroyed asteroids
        asteroids_text = FONT.render(f"Asteroids destroyed: {asteroids_destroyed}", True, (255, 255, 255))
        DISPLAYSURF.blit(asteroids_text, (SCREEN_WIDTH-300, 1))
        # creates enemies
        if len(enemies) <= 5:
            E_new = Enemy(random.choice([asteroid_small_settings, asteroid_large_settings]))
            enemies.add(E_new)
            all_sprites.add(E_new)
        # moves and re-draws all sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
        # shoots and checks for damage
        P1.shoot()
        if len(projectiles) > 1:
            hits = pygame.sprite.groupcollide(projectiles, enemies, True, False)
            for projectile, enemies_list in hits.items():
                for enemy in enemies_list:
                    enemy.take_damage(P1.attack)
        # to be run if collision occurs between player and enemy
        if pygame.sprite.spritecollideany(P1, enemies):
            DISPLAYSURF.fill(RED)
            gameover_text = FONT.render('GAME OVER! YOU SUCK!!!', True, BLUE)
            gameover_text_rect = gameover_text.get_rect()
            gameover_text_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2.25)
            DISPLAYSURF.blit(gameover_text, gameover_text_rect)
            asteroids_text_rect = asteroids_text.get_rect()
            asteroids_text_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/1.75)
            DISPLAYSURF.blit(asteroids_text, asteroids_text_rect)
            pygame.display.update()
            for entity in all_sprites:
                entity.kill() 
            time.sleep(5)
            game_running = False

        # picks up bullets
        for bullet in bullets:
            if pygame.sprite.collide_rect(P1, bullet):
                P1.bullets += 30
                bullet.kill()
        # # draws a rectangle around enemies for debugging purposes
        # for enemy in enemies:
        #     enemy.draw_rect(DISPLAYSU
        # # draws a rectangle around player for debugging
        # P1.draw_rect(DISPLAYSURF)
        pygame.display.update()
        FramePerSec.tick(FPS)

def main_menu():
    global game_running
    while not game_running:
    
        ### MENU ###

        DISPLAYSURF.fill(BLUE)
        
        # "Start Flight" button
        start_button = pygame.Rect(250, 200, 200, 50)
        pygame.draw.rect(DISPLAYSURF, (0, 255, 0), start_button)
        start_text = FONT.render("Start Flight", True, (255, 255, 255))
        DISPLAYSURF.blit(start_text, (325, 215))

        # "Quit" button
        quit_button = pygame.Rect(250, 300, 200, 50)
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), quit_button)
        quit_text = FONT.render("Quit", True, (255, 255, 255))
        DISPLAYSURF.blit(quit_text, (325, 315))
            
        # shows top score
        score_text = FONT.render("Top Score: " + str(ALL_TIME_TOP_SCORE), True, (255, 255, 255))
        DISPLAYSURF.blit(score_text, (250, 100))
            
        pygame.display.flip()

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                # checks if mouse position is over the button
                if start_button.collidepoint(mouse_pos):
                    game_running = True
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        if game_running:
            print("game started")
            return

while True:
    # cycles through all events occuring
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if game_running:
            run_game()
        else:
            reset_game(enemies, all_sprites)
            main_menu()