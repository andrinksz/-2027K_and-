##########################################
# WB Pygames
# Autor: Lukas Zehnder
# Letzte Änderungen: 23.01.2024, 
##########################################

##########################################
# Externe Bibliotheken einbinden
##########################################
import pygame as py                                 # Pygames
import random                                # Zufallszahlen
import os                                           # Operating System für den relativen Pfad

##########################################
# Pygames initialisieren
##########################################
py.init()                                      # Pygames initialisieren
win_size = (800,800)                           # Fenstergrösse
screen = py.display.set_mode(win_size)         # Fenstergrösse setzen
py.display.set_caption("Male nicht den Teufel an die Wand")           # Titel des Fensters
clock = py.time.Clock() 					   # Eine Pygame-Uhr um die Framerate zu kontrollieren
my_font = py.font.SysFont('Comic Sans MS', 36)


#########################################################################
# Beginn Funktionen
#########################################################################

def load_images(path,names,ending,number,xpix,ypix):
    file_names = []                                                      # Liste der Namen der Bilder generieren
    for i in range(number):                                              # Alle Namen durchgehen
        file_names.append(path+names+str(i)+ending)                      # Alle vorhandenen Bildernamen generieren
    animation = []                                                       # Liste für die Bilder
    for i in range(number):                                              # Alle Bilder durchgehen
        img = py.image.load(file_names[i]).convert()                     # Bild laden
        animation.append(py.transform.scale(img, (xpix, ypix)))          # Bild vergrössern und in die Liste aufnehmen
    return animation

#########################################################################
# Beginn der Klassendefinitionen
#########################################################################


##########################################
# Die Klasse des Spielers
##########################################
class Player(py.sprite.Sprite):                                          # Wie sieht der Player aus?
    #######################################
    # Bauplan des Spielers
    #######################################
    def __init__(self, left, up, right, down):                           # Hier ist der Bauplan des Players
        super().__init__()                                               # Musst du nicht verstehen
        self.images = load_images  # kommt noch   # Bild laden
        self.image = py.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Spieler ist blau
        self.rect = self.image.get_rect()
        self.rect.x = win_size[0] // 2
        self.rect.y = win_size[1] // 2
        self.left = left
        self.up = up
        self.right = right
        self.down = down
        self.speed = random.randint(5, 10)
        self.costume = 0
        self.speed = 5
        self.points = 0
        
        
        
    def move(self):
        key = py.key.get_pressed()                                     # Alle gedrückten Tasten abrufen
        if key[self.left] == True and self.rect.x > 0:                 # Ist die linke Pfeiltaste gedrückt worden?
            self.rect.x = self.rect.x - self.speed
        if key[self.up] == True and self.rect.y > 0:                   # Ist die linke Pfeiltaste gedrückt worden?
            self.rect.y = self.rect.y - self.speed
        if key[self.right] == True and self.rect.x + self.rect.width < win_size[0]:
            self.rect.x = self.rect.x + self.speed
        if key[self.down] == True and self.rect.y + self.rect.height < win_size[1]:
            self.rect.y = self.rect.y + self.speed
            
    def change_costume(self):
        self.costume = self.costume + 1
        if self.costume == len(self.images):
            self.costume = 0
        self.image = self.images[self.costume]



##########################################
# Die Klasse des Spiels, welche alle Objekte beinhalten sollte
##########################################
class Game():
    def __init__(self):
        self.game_state = "intro"
        
        # create dictionary and save images in it
        self.background_images = {}
        self.background_images["img_intro"] = py.transform.scale(py.image.load("res/images/background/winter_intro.jpg"),
                                                                 (win_size[0], win_size[1]))
        self.background_images["img_game"] = py.transform.scale(py.image.load("res/images/background/winter_landscape.jpg"),
                                                                 (win_size[0], win_size[1]))
        self.background_images["img_end"] = py.transform.scale(py.image.load("res/images/background/winter_game_over.jpg"),
                                                                 (win_size[0], win_size[1]))   
            
        # Gruppen und Objekte
        self.player_1 = Player(py.K_LEFT, py.K_UP, py.K_RIGHT, py.K_DOWN)
        
        self.all_sprites = py.sprite.Group()                     # Gruppe aller Sprites
        
        self.all_sprites.add(self.player_1)
        self.game_clock = py.time.get_ticks()
        
##########################################
# Die Klasse der Teufel
##########################################
class Devil(py.sprite.Sprite):  
    def __init__(self):
        super().__init__()
        self.image = py.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Teufel sind rot (Bild kommt noch)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, win_size[0])
        self.rect.y = random.randint(0, win_size[1])
        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])  # Bewegung in x-Richtung
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])  # Bewegung in y-Richtung
        
        
        
##########################################
# Die Klasse der Spielfigur (Habe noch keinen Namen)
##########################################
class Game:
    def __init__(self):
        self.game_state = "intro"
        self.player_1 = Player(py.K_LEFT, py.K_UP, py.K_RIGHT, py.K_DOWN)
        self.all_sprites = py.sprite.Group()
        self.all_sprites.add(self.player_1)

        self.devils = py.sprite.Group()  # Gruppe der Teufel
        self.spawn_timer = 0

        self.lives = 7  # Maximal 7 Leben
        self.score = 0  # Punkte        
        
        
        
    def check_collisions(self):
        pass
        
    def draw_score(self):
        time_passed = py.time.get_ticks() - self.game_clock
        text = my_font.render("Time: " + str(int(time_passed/100)/10),True, (255,0,0)) 
        screen.blit(text,(50,20)) 
        
    def draw_intro(self):
        screen.blit(self.background_images["img_intro"], (0,0))
    
    def draw_game(self):
        screen.blit(self.background_images["img_game"], (0,0))
        self.all_sprites.draw(screen)
        self.draw_score()
        
    def draw_game_over(self):
        screen.blit(self.background_images["img_end"], (0,0))
                
    def run(self):
        ##########################################
        # Hauptschleife
        ##########################################
        while True:                              # Solange das Spiel läuft...
            
            ##########################################
            # Events abfragen
            ##########################################
            for event in py.event.get():                    # Gehe alle Events des Sysems durch
                if event.type == py.QUIT:                   # Ist das Spiel beendet worden?
                    py.quit()                               # Schliesse das Fenster und beende das Programm      
                
            
            keys = py.key.get_pressed()
            if self.game_state == "intro":
                self.draw_intro()
                if keys[py.K_SPACE]:
                    self.game_state = "game"
                    self.game_clock = py.time.get_ticks()
                
            if self.game_state == "game":
                self.player_1.move()                
                self.player_1.change_costume()
                self.check_collisions()
                self.draw_game()
               
                if py.time.get_ticks() > self.game_clock + 10000: # nach 10 Sekunden wechselt der Game State zu end
                    self.game_state = "end"
                
            if self.game_state == "end":
                self.draw_game_over()
                if keys[py.K_SPACE]:
                    self.game_state = "game"
                    self.game_clock = py.time.get_ticks()
                

            py.display.update()                             # Zeichne den Bildschirm neu
            clock.tick(24)                                  # Der Bildschirm soll alle 1/24 Sekunden aktualisiert werden
                



#########################################################################
# Beginn des Hauptprogramms
#########################################################################


game = Game()
game.run()


