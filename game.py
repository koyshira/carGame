import pygame
import sys
import random

pygame.init()

# Predefined some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

FPS = 60
FramePerSec = pygame.time.Clock()

# Load the images
background_image = pygame.image.load('assets/bg.png')
enemy_image = pygame.image.load('assets/Enemy.png')
player_image = pygame.image.load('assets/Player.png')

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")


class Background(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = background_image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (160, SCREEN_HEIGHT - 150)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
font = pygame.font.SysFont(None, 48)

def game_over():
    text = font.render('Game Over', True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    DISPLAYSURF.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()

P1 = Player()
E1 = Enemy()
BackGround = Background([0, 0])

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    P1.update()
    E1.move()

    if pygame.sprite.collide_rect(P1, E1):
        game_over()

    DISPLAYSURF.blit(background_image, [0, 0])
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)

    # Blit the score text
    score_text = font.render("Score: " + str(int(score)), True, (0, 0, 0))
    text_rect = score_text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    # Add a rectangle behind the score
    padding = 10
    rect_width = SCREEN_WIDTH
    rect_height = text_rect.height + padding * 2
    rect_pos = (0, SCREEN_HEIGHT - rect_height)
    score_rect = pygame.Rect(rect_pos, (rect_width, rect_height))
    pygame.draw.rect(DISPLAYSURF, WHITE, score_rect)

    # Blit the score text on top of the rectangle
    text_rect.center = score_rect.center
    DISPLAYSURF.blit(score_text, text_rect)

    # Update the display
    pygame.display.update()

    # Increment the score every second
    FramePerSec.tick(FPS)
    score += 0.02
