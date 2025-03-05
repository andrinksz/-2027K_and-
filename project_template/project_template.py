import pygame
import random
import sys

# Initialisierung von Pygame
pygame.init()

# Bildschirmkonfiguration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flucht aus der Hölle")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Schriftart
font = pygame.font.SysFont(None, 48)

# Herz-Symbol laden
heart_image = pygame.image.load("res/images/herz/herz.png") 
heart_image = pygame.transform.scale(heart_image, (30, 30))

background_image = pygame.transform.scale(pygame.image.load("res/images/background/hintergrund.jpg"),
                                          (SCREEN_WIDTH, SCREEN_HEIGHT))

start_screen = pygame.transform.scale(pygame.image.load("res/images/startbild/startbild.jpg"),
                                      (SCREEN_WIDTH, SCREEN_HEIGHT))

end_screen = pygame.transform.scale(pygame.image.load("res/images/endbild/endbild.jpg"),
                                    (SCREEN_WIDTH, SCREEN_HEIGHT))

def show_start_screen():
    screen.blit(start_screen, (0, 0))
    text = font.render("Press ENTER to Start", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def show_end_screen(total_time):
    screen.blit(end_screen, (0, 0))
    text = font.render(f"Gesamtzeit: {int(total_time)}s", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
                pygame.quit()
                sys.exit()
                
                


# FPS und Zeit
clock = pygame.time.Clock()
FPS = 60

total_timer = 0
phase_timer = 30
in_hell = True

font = pygame.font.SysFont(None, 36)

def load_images(path,names,ending,number,xpix,ypix):
    file_names = [path+names+str(i)+ending for i in range(number)]
    return [pygame.transform.scale(pygame.image.load(file).convert(), (xpix, ypix)) for file in file_names]

def draw_timers():
    phase_time_text = font.render(f"{int(phase_timer)}s", True, WHITE)
    total_time_text = font.render(f"{int(total_timer)}s", True, WHITE)
    screen.blit(phase_time_text, (10, 10))
    screen.blit(total_time_text, (10, 50))


# Spielerklasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


#superdevil
class SuperDevil(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.is_super = True
        self.images = load_images("res/images/superteufel/", "superteufel", ".png", 1, 40, 40)
        self.image = self.images[0]  # Erstes Bild setzen
        self.rect = self.image.get_rect()  # Hier wird rect initialisiert
        self.speed = random.randint(4, 8)
        self.direction = direction

        if self.direction == "left_to_right":
            self.rect.x = 0
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif self.direction == "right_to_left":
            self.rect.x = SCREEN_WIDTH - self.rect.width
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif self.direction == "top_to_bottom":
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = 0
        elif self.direction == "bottom_to_top":
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def update(self):
        if self.direction == "left_to_right":
            self.rect.x += self.speed
        elif self.direction == "right_to_left":
            self.rect.x -= self.speed
        elif self.direction == "top_to_bottom":
            self.rect.y += self.speed
        elif self.direction == "bottom_to_top":
            self.rect.y -= self.speed
        
        if (
            self.rect.x > SCREEN_WIDTH or self.rect.x < -self.rect.width or
            self.rect.y > SCREEN_HEIGHT or self.rect.y < -self.rect.height
        ):
            self.kill()

    
# Teufelklasse
class Devil(pygame.sprite.Sprite):
    def __init__(self, direction, is_super=False):
        super().__init__()
        self.is_super = is_super
        self.images = load_images("res/images/teufel/", "teufel", ".png", 3, 40, 40)
        self.image = self.images[0]  # Erstes Bild setzen
        self.rect = self.image.get_rect()
        self.speed = random.randint(4, 8) if self.is_super else random.randint(3, 7)
        self.direction = direction

        if self.direction == "left_to_right":
            self.rect.x = 0
            self.rect.y = random.randint(0, SCREEN_HEIGHT)
        elif self.direction == "right_to_left":
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT)
        elif self.direction == "top_to_bottom":
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = 0
        elif self.direction == "bottom_to_top":
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = SCREEN_HEIGHT

    def update(self):
        if self.direction == "left_to_right":
            self.rect.x += self.speed
        elif self.direction == "right_to_left":
            self.rect.x -= self.speed
        elif self.direction == "top_to_bottom":
            self.rect.y += self.speed
        elif self.direction == "bottom_to_top":
            self.rect.y -= self.speed
        
        if (
            self.rect.x > SCREEN_WIDTH or self.rect.x < 0 or
            self.rect.y > SCREEN_HEIGHT or self.rect.y < 0
        ):
            self.kill()

# Engelklasse
class Angel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_images("res/images/engel/", "engel", ".png", 1, 40, 40)[0]
        self.rect = self.image.get_rect(
            center=(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
        )
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > 2000:
            self.kill()

# Spielvariablen
player = Player()
player_group = pygame.sprite.Group(player)

devils = pygame.sprite.Group()
angels = pygame.sprite.Group()

hit_count = 0
max_hits = 7
spawn_timer = 0
angel_spawn_timer = 0
collected_angels = 0
extra_lives = 0

devil_count = 0  # Zählt normale Teufel für Super-Teufel-Spawns


def draw_hearts():
    for i in range(max_hits - hit_count + extra_lives):
        screen.blit(heart_image, (SCREEN_WIDTH - (i + 1) * 35, 10))

        
def draw_game():
    screen.blit(self.background_images["img_game"], (0,0))
    self.all_sprites.draw(screen)
    

# Spiel starten
show_start_screen()


        
        
# Hauptspiel-Loop
running = True
while running:
    if in_hell:
        screen.blit(background_image, (0,0))
    else:
        screen.fill(LIGHT_BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player_group.update(keys)

    # Timer-Update
    total_timer += 1 / FPS
    phase_timer -= 1 / FPS
    
    # Wechsel zwischen Hölle (30s) und Himmel (10s)
    if phase_timer <= 0:
        in_hell = not in_hell
        phase_timer = 30 if in_hell else 10
        
        if in_hell:
            angels.empty()
        else:
            devils.empty()

        extra_lives += collected_angels
        collected_angels = 0  

    if in_hell:
        spawn_timer += 1
        if spawn_timer >= 30:
            devil_count += 1
            is_super = devil_count % 20 == 0  # Jeder 20. Teufel ist ein Super-Teufel
            direction = random.choice(["left_to_right", "right_to_left", "top_to_bottom", "bottom_to_top"])
            
            if is_super:
                devils.add(SuperDevil(direction))  # Super-Teufel spawn
            else:
                devils.add(Devil(direction))  # Normale Teufel spawn

            spawn_timer = 0
    else:
        angel_spawn_timer += 1
        if angel_spawn_timer >= FPS:
            angels.add(Angel())
            angel_spawn_timer = 0
    
    devils.update()
    angels.update()
    
    if in_hell:
        collided_devils = pygame.sprite.spritecollide(player, devils, True)
        for devil in collided_devils:
            if isinstance(devil, SuperDevil):  # Super-Teufel
                hit_count += 2  # Super-Teufel zieht 2 Leben ab
            else:
                hit_count += 1  # Normale Teufel ziehen 1 Leben ab
            
            if hit_count >= max_hits + extra_lives:
                running = False
    else:
        collided_angels = pygame.sprite.spritecollide(player, angels, True)
        collected_angels += len(collided_angels)
    

    draw_hearts()
    draw_timers()
    player_group.draw(screen)
    devils.draw(screen)
    angels.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

# Endbildschirm anzeigen
show_end_screen(total_timer)

pygame.quit()