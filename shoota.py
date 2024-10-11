import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

clock = pygame.time.Clock()

# Load images
background_img = pygame.image.load('resources/background.png').convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

player_img = pygame.image.load('resources/player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 38))

asteroid_imgs = []
asteroid_imgs.append(pygame.image.load('resources/asteroid1.png').convert_alpha())
asteroid_imgs.append(pygame.image.load('resources/asteroid2.png').convert_alpha())

mob_imgs = []
mob_imgs.append(pygame.image.load('resources/mob1.png').convert_alpha())
mob_imgs.append(pygame.image.load('resources/mob2.png').convert_alpha())

bullet_img = pygame.Surface((5, 15))
bullet_img.fill((255, 255, 0))

enemy_bullet_img = pygame.Surface((5, 15))
enemy_bullet_img.fill((255, 0, 0))

font = pygame.font.SysFont(None, 48)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_SPACE]:
            self.shoot()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.image_orig = random.choice(asteroid_imgs)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -100)
        self.speedy = random.randint(5, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-150, -100)
            self.speedy = random.randint(5, 8)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super(Mob, self).__init__()
        self.image_orig = random.choice(mob_imgs)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -100)
        self.speedy = random.randint(2, 4)
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-150, -100)
            self.speedy = random.randint(2, 4)
        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            enemy_bullets.add(bullet)
            all_sprites.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(EnemyBullet, self).__init__()
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 6

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

def show_main_menu():
    menu = True
    while menu:
        screen.blit(background_img, (0, 0))
        title_text = font.render("Alien Shooter", True, WHITE)
        play_text = font.render("Play", True, WHITE)
        exit_text = font.render("Exit", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    menu = False
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    menu = False
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def show_game_over_screen(score):
    game_over = True
    while game_over:
        screen.blit(background_img, (0, 0))
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        continue_text = font.render("Click to return to main menu", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game_over = False

while True:
    show_main_menu()
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    asteroids = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    for i in range(4):
        asteroid = Asteroid()
        asteroids.add(asteroid)
        all_sprites.add(asteroid)
    for i in range(4):
        mob = Mob()
        mobs.add(mob)
        all_sprites.add(mob)
    score = 0
    font_small = pygame.font.SysFont(None, 36)
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        all_sprites.update()
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            score += 10
            asteroid = Asteroid()
            asteroids.add(asteroid)
            all_sprites.add(asteroid)
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 20
            mob = Mob()
            mobs.add(mob)
            all_sprites.add(mob)
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            running = False
        hits = pygame.sprite.spritecollide(player, asteroids, False)
        if hits:
            running = False
        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            running = False
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
    show_game_over_screen(score)
