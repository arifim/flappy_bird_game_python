import pygame
from pygame.constants import QUIT
import os
import random


pygame.init()
DEBUG = True

def debug(val_name, val):
    if DEBUG:
        print(val_name + ": ", val)


# Constant valiables
SCREEN_HEIGHT = 550
SCREEN_WIDTH = int(SCREEN_HEIGHT * 0.8)

GRAVITY = 9.81
GROUND = SCREEN_HEIGHT

# Color constants
BG = (255,255,255) 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # Create main window 
pygame.display.set_caption("Flappy Bird")

# Load collumn images
top_collumn_image = pygame.image.load(f"{os.getcwd()}/pygame/flappy_bird/images/top_collumn.png").convert_alpha()
bottom_collumn_image = pygame.image.load(f"{os.getcwd()}/pygame/flappy_bird/images/bottom_collumn.png").convert_alpha()

# Load cloud images
cloud1 = pygame.image.load(f"{os.getcwd()}/pygame/flappy_bird/images/cloud1.png").convert_alpha()
cloud2 = pygame.image.load(f"{os.getcwd()}/pygame/flappy_bird/images/cloud2.png").convert_alpha()
cloud1 = pygame.transform.scale(cloud1, (100, 60))
cloud2 = pygame.transform.scale(cloud2, (100, 60))

# Load 
background_image = pygame.transform.scale(
    pygame.image.load(f"{os.getcwd()}/pygame/flappy_bird/images/background.png"),
    (SCREEN_WIDTH+10, SCREEN_HEIGHT))


# Load sound effects
score_sound = pygame.mixer.Sound(os.getcwd() + "/pygame/flappy_bird/sounds/pass.wav")
hit_sound = pygame.mixer.Sound(os.getcwd() + "/pygame/flappy_bird/sounds/hit.wav")


class Bird(pygame.sprite.Sprite):
    
    def __init__(self, x, y, scale) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.animation_img_list = []
        self.scale = scale
        self.frame_index = 0
        self.animation_update_time = pygame.time.get_ticks()
        for i in range(4):
            img_path = f"{os.getcwd()}/pygame/flappy_bird/images/bird_{i}.png"
            img = pygame.transform.scale(pygame.image.load(img_path), (60,60)).convert_alpha()
            self.animation_img_list.append(img)
        self.image = self.animation_img_list[self.frame_index]
        self.rect = self.image.get_rect().inflate(-5,-5)
        debug("Bird rect", self.rect)
        self.rect.center = (x, y)
        self.speed = 4
        self.rotate_angle = 0
        self.a = 0.1
        self.direction = 1
        self.is_alive = True
    
    def update_animation(self, faling):        
        self.image = self.animation_img_list[self.frame_index]
        if faling:
            self.rotate_beak_down()
        else:
            self.wing_animation() 
            self.rotate_beak_up()


    def wing_animation(self):
        ANIMATION_COOLDOWN = 50
        self.image = self.animation_img_list[self.frame_index]
        if pygame.time.get_ticks() - self.animation_update_time > ANIMATION_COOLDOWN:
            self.frame_index = (self.frame_index + 1) % len(self.animation_img_list)
            self.animation_update_time = pygame.time.get_ticks()


    def rotate_beak_down(self):
        if self.rotate_angle <= 20:
            self.rotate_angle += 5
        self.image = pygame.transform.rotate(self.image, -self.rotate_angle)


    def rotate_beak_up(self):
        if self.rotate_angle > -30:
            self.rotate_angle -= 5
        self.image = pygame.transform.rotate(self.image, abs(self.rotate_angle))


    def fly_down(self):
        self.rect.y += GRAVITY * self.a
        self.a += 0.1


    def fly_up(self):
        if self.is_alive:
            self.rect.y -= self.speed+5


    def draw(self):
        screen.blit(self.image, self.rect)

    def dead(self):
        self.is_alive = False
        self.image = pygame.transform.flip(self.image, False, True)
        if self.rect.y > GROUND+60:
            self.fly_down()
            


class Collumn(pygame.sprite.Sprite):

    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.min_gap = 100
        self.top_collumn = top_collumn_image
        self.top_collumn_rect = self.top_collumn.get_rect().inflate(-5,-5)
        self.bottom_collumn = bottom_collumn_image
        self.collumn_height = self.top_collumn_rect.height
        self.y = 0 - self.collumn_height/2 + random.randint(50, 300)
        self.top_collumn_rect.center = (x, self.y)
        self.bottom_collumn_rect = self.bottom_collumn.get_rect().inflate(-5,-5)
        rm = random.randint(0, 100)
        self.bottom_collumn_rect.center = (x, self.y+(self.min_gap+rm) + self.collumn_height)
        debug("random gap in collumn", rm+self.min_gap)
        self.speed = 5


    def draw(self):
       screen.blit(self.top_collumn, self.top_collumn_rect)
       screen.blit(self.bottom_collumn, self.bottom_collumn_rect)


    def move(self):
        self.top_collumn_rect.x -= self.speed
        self.bottom_collumn_rect.x -= self.speed

class Cloud(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.clouds = [cloud1, cloud2]
        self.cloud_rects = []
        self.speed = 1
        for cloud in self.clouds:
            self.cloud_rects.append(cloud.get_rect())
        for cloud_rect in self.cloud_rects:
            cloud_rect.y = random.randint(50, 150)
            cloud_rect.x = SCREEN_WIDTH + random.randint(0, 300)

    def draw(self):
        for cloud, cloud_rect in zip(self.clouds, self.cloud_rects):
            screen.blit(cloud, cloud_rect)
    
    def move(self):
        for cloud in self.cloud_rects:
            cloud.x -= self.speed

pygame.display.update()
clock = pygame.time.Clock()

def draw_background(img, pos):
    screen.blit(img, pos)
    
bird = Bird(100, 200, 1)
collumn = Collumn(SCREEN_WIDTH+50, 0)
clouds = Cloud()

# Main event handler loop
done = False
game_started = False
game_over = False
faling = True
is_sound_playing = False

while not done:
    draw_background(background_image, pos=(0, 0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
            exit()
        if event.type == pygame.KEYDOWN:
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_SPACE]:
                if not game_over:
                    game_started = True
            if (key_input[pygame.K_UP]):
                if bird.is_alive:
                    faling = False
                    bird.a = 0.1
        else:
            faling = True
    clouds.draw()
    bird.draw()
    collumn.draw()
    if collumn.top_collumn_rect.x < -50:
        collumn = Collumn(SCREEN_WIDTH + random.randint(50, 150), 0)
    if game_started:
        if bird.is_alive:
            collumn.move()
            bird.update_animation(faling)
            clouds.move()
        if faling:
            bird.fly_down()
        else:
            bird.fly_up()

        # Cheking collisions
        if bird.rect.y > SCREEN_HEIGHT-60 or \
           bird.rect.colliderect(collumn.top_collumn_rect) or \
           bird.rect.colliderect(collumn.bottom_collumn_rect):
            bird.dead()
            if bird.rect.y >= GROUND-60:
                game_over = True
                game_started = False
        
        if bird.rect.x > collumn.top_collumn_rect.centerx and \
            bird.rect.x < collumn.top_collumn_rect.right:
            if not is_sound_playing:
                pygame.mixer.Sound.play(score_sound)
                is_sound_playing = True
        else:
            is_sound_playing = False
    pygame.display.flip()
    pygame.display.update()
    clock.tick(30)

pygame.quit()