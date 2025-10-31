import pygame, sys
from pygame.locals import *

from math import atan2, cos, dist, radians, sin, sqrt
from random import choice, randint

# SETUP

BACKGROUND = (255, 255, 255)

fps = 30
clock = pygame.time.Clock()
screen_width = 640
screen_height = 360
 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ecosystem test')

# VARIABLES

# creature names (WILL HAVE USE LATER - SEE 'to_add.txt')
prefixes = ["Ap","Br","Cr","Dal","Egg","Forg","Grol","Hydr","Ib","Jol","Kr","L","My","N","Ox","Pr","Qu","R","Sap","Tyl","Ub","Val","W","Xyl","Y","Zy"]
vowels = ["a","ae","ai","ao","au","e","ea","ee","ei","eu","i","ie","ii","io","o","oa","oe","oi","ou","u","ui","y"]
suffixes = ["by","col","cry","dry","fy","gic","logy","ly","mic","mod","nod","pric","rac","ry","sal","si","sy","tal","ty","vic","xic","zy"]

# CLASSES

# creatures

class Creature: # parent class for all creatures
    def __init__(self, x, y, speed, size, sight):
        self.posx, self.posy = x, y
        self.name = choice(prefixes) + choice(vowels) + choice(suffixes)

        self.speed = speed
        self.size = size
        self.sight = sight

        self.action = randint(0,1)
        self.action_loops = 0
        self.move_dir = radians(0)
    
    def pause(self): # action 0
        if self.action_loops > 0:
            self.action_loops -= 1
        else:
            self.action = 1
            self.action_loops = randint(50,100)
            self.move_dir = radians(randint(1, 360))

    def wander(self): # action 1
        if self.action_loops > 0:
            self.action_loops -= 1
            self.posx += self.speed * cos(self.move_dir)
            self.posy -= self.speed * sin(self.move_dir)
        else:
            self.action = 0
            self.action_loops = randint(30,80)

    def food(self, food_type): # action 2
        dists = []
        for food in food_type: # finds the distance to every food
            tdist = sqrt((abs(food.posx - self.posx) ** 2) + (abs(food.posy - self.posy) ** 2))
            dists.append(tdist)
        if any(x < self.sight for x in dists): # if any are within the eyesight range, the creature moves towards it
            self.action = 2

            closest_index = dists.index(min(dists))
            target_posx = food_type[closest_index].posx
            target_posy = food_type[closest_index].posy

            angle = atan2(target_posy - self.posy, target_posx - self.posx)

            self.posx += self.speed * cos(angle)
            self.posy += self.speed * sin(angle)

            if dist((self.posx,self.posy), (food_type[closest_index].posx, food_type[closest_index].posy)) < self.speed:
                self.action = 0
                self.action_loops = randint(30,80)
                del food_type[closest_index]
        else:
            action = 1



class Herbivore(Creature): # prey/herbivore animal
    def __init__(self, x, y, speed, size, sight):
        super().__init__(x, y, speed, size, sight)

        self.surf = pygame.Surface((size,size))
        self.surf.fill("white")
    
    def update(self):
        self.food(game.plants)
        if self.action == 0:
            self.pause()
        elif self.action == 1:
            self.wander()
        
        if self.posx < 0:
            self.posx = 0
        if self.posx > screen_width - self.size:
            self.posx = screen_width - self.size

        if self.posy < 0:
            self.posy = 0
        if self.posy > screen_height - self.size:
            self.posy = screen_height - self.size

        screen.blit(self.surf, (self.posx,self.posy))

# plant

class Plant():
    def __init__(self, x, y, size):
        self.posx = x
        self.posy = y

        self.size = size
        self.surf = pygame.Surface((self.size,self.size))
        self.surf.fill("red")                                          # REMOVE THIS WHEN IT IS DONE IN THE FUTURE WAY
    
    def update(self):
        screen.blit(self.surf,(self.posx,self.posy))

# game

class Game():
    def __init__(self):
        self.herbivores = []
        self.plants = []

        for i in range(5):
            self.herbivores.append(Herbivore(randint(0,600), randint(0,300), randint(15,25) / 10, randint(15,20), randint(20,30) * 10))
            self.plants.append(Plant(randint(0,600), randint(0,300), 10)) # food when added
        
        self.game_speed = 1 # when ui is added, should be able to be changed

    def update(self):
        screen.fill("black")

        for plant in self.plants:
            plant.update()
        for herbivore in self.herbivores:
            herbivore.update()

        pygame.display.update()
        clock.tick(fps * self.game_speed)

# LOOP

game = Game()

running = True
while running:
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()

    game.update()