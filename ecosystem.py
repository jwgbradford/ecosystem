import pygame, sys
from pygame.locals import *
from math import sin,cos,tan,asin,acos,atan,radians,sqrt,atan2, dist
from random import randint,choice

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
class Creature:
    def __init__(self,x,y,speed,size,eyesight,hunger):
        self.posx = x
        self.posy = y

        self.name = choice(prefixes) + choice(vowels) + choice(suffixes)

        self.speed = speed
        self.move_dir = radians(randint(1,360))
        self.move_loops = randint(50,120)

        self.action = randint(0,1)
        
        self.size = size
        self.surf = pygame.Surface((self.size,self.size))

        self.sight = eyesight

        self.hunger = hunger
        self.importants = [self.hunger] # WILL ADD MORE EVENTUALLY
    
    def wander(self):
        self.move_loops -= 1
        if self.move_loops <= 0:
            self.action = 0
            self.move_dir = radians(randint(1,360))
            self.move_loops = randint(20,80)
        self.posx += self.speed * cos(self.move_dir)
        self.posy -= self.speed * sin(self.move_dir)

    def pause(self):
        self.move_loops -= 1
        if self.move_loops <= 0:
            self.action = 1
            self.move_loops = randint(30,60)
            self.find_food()
    
    def find_food(self):
        pass # theres probably a better way to do this - i wanted it to look cleaner by just having pause in the superclass but the find_food will change between each subclass.. im not sure if theres a better way but there probably is
    
    def boundaries(self):
        if self.posx < 0:
            self.posx = 0
        elif self.posx > screen_width - self.size:
            self.posx = screen_width - self.size
        if self.posy < 0:
            self.posy = 0
        elif self.posy > screen_height - self.size:
            self.posy = screen_height - self.size

class Herbivore(Creature):
    def __init__(self,x,y,speed,size,sight,hunger):
        super().__init__(x,y,speed,size,sight,hunger)
        
        self.surf.fill("white")

    def find_food(self):
        dists = []
        for food in foods:
            dist = sqrt((abs(food.posx - self.posx) ** 2) + (abs(food.posy - self.posy) ** 2))
            dists.append(dist)
        if len(dists) > 0 and min(dists) < self.sight:
            self.action = 2
            self.nearest_food = foods[dists.index(min(dists))]
            self.target_x,self.target_y = self.nearest_food.posx,self.nearest_food.posy

            hyp = sqrt((self.posx - self.target_x) ** 2 + (self.posy - self.target_y) ** 2)
            self.move_loops = round(hyp / self.speed)
        else:
            self.action = 1
        
    def move_to_food(self):
        angle = atan2(self.target_y - self.posy, self.target_x - self.posx)

        try:
            foods[foods.index(self.nearest_food)]
            self.move_loops -= 1
            if self.move_loops <= 0:
                self.action = 0
                self.hunger += 0.5
                del foods[foods.index(self.nearest_food)]
                self.move_loops = randint(40,100)
            self.posx += self.speed * cos(angle)
            self.posy += self.speed * sin(angle)
        except ValueError:
            self.action = 0
            self.move_loops = randint(0,20)
    
    def vitals(self):
        if self.hunger > 1:
            self.hunger = 1
        self.hunger -= self.speed / self.size / 40
        if self.hunger <= 0:
            del herbivores[herbivores.index(self)]
    
    def update(self):
        if self.action == 0:
            self.pause()
        elif self.action == 1:
            self.wander()
        elif self.action == 2:
            self.move_to_food()
        self.boundaries()
        self.vitals()
        screen.blit(self.surf,(self.posx,self.posy))

# creatures CLEANING UP

class newCreature:
    def __init__(self, x, y, speed, size, sight):
        self.posx,self.posy = x,y
        self.name = choice(prefixes) + choice(vowels) + choice(suffixes)

        self.action = 1
        self.action_loops = 0
        self.move_dir = radians(randint(1,360))

        self.speed = speed
        self.size = size
        self.sight = sight

        self.hunger = 1

    def pause(self):  # stands still for some time - ACTION 0
        if self.action_loops > 0:
            self.action_loops -= 1
        else:
            self.action = 1
            self.move_dir = radians(randint(1, 360))  # pick a new direction when done pausing
            self.action_loops = randint(50, 100)      # set how long to wander
    
    def wander(self): # moves randomly - ACTION 1
        self.action_loops -= 1
        if self.action_loops <= 0:
            self.action = 0
            self.move_dir = radians(randint(1,360))
            self.action_loops = randint(20,80)
        self.posx += self.speed * cos(self.move_dir)
        self.posy -= self.speed * sin(self.move_dir)

    def move_towards(self, target_pos): # moves towards a given point (most likely the above function) - ACTION 2
        angle = atan2(target_pos[1] - self.posy, target_pos[0] - self.posx)

        if sqrt((target_pos[0]-self.posx)**2 + (target_pos[1] - self.posy)**2) < self.size / 2:
            self.action = 0  # will eat after reaching food

        self.posx += self.speed * cos(angle)
        self.posy += self.speed * sin(angle)

        if self.action == 1:  # if wandering
            if self.action_loops > 0:
                self.action_loops -= 1
            else:
                self.move_dir = radians(randint(1, 360))
                self.action = 0
                self.action_loops = randint(50, 100)
    
    def screen_edge(self): # makes sure the creature doesn't leave the screen
        if self.posx < 0:
            self.posx = 0
        if self.posx > screen_width - self.size:
            self.posx = screen_width - self.size

        if self.posy < 0:
            self.posy = 0
        if self.posy > screen_height - self.size:
            self.posy = screen_height - self.size

class newHerbivore(newCreature):
    def __init__(self, x, y, speed, size, sight, food_type):
        super().__init__(x, y, speed, size, sight)

        self.surf = pygame.Surface((self.size,self.size))
        self.surf.fill("white")

        self.food_type = food_type
    
    def update(self):
        dists = []
        for food in foods: # finds the distance to every food
            dist = sqrt((abs(food.posx - self.posx) ** 2) + (abs(food.posy - self.posy) ** 2))
            dists.append(dist)
        if any(x < self.sight for x in dists): # if any are within the eyesight range, the creature moves towards it
            self.action = 2
            self.move_towards((foods[dists.index(min(dists))].posx,foods[dists.index(min(dists))].posy))
            if dist([self.posx,self.posy], [foods[dists.index(min(dists))].posx, foods[dists.index(min(dists))].posy]) < self.size:
                del herbivores[dists.index(foods[dists.index(min(dists))])]

        if self.action == 0: # wait
            self.pause()
        elif self.action == 1: # wander
            self.wander()
        
        self.screen_edge()
            
        screen.blit(self.surf, (self.posx,self.posy))


# plant
class Food:
    def __init__(self,x,y, size):
        self.posx = x
        self.posy = y

        self.size = size
        self.surf = pygame.Surface((self.size,self.size))
        self.surf.fill("red")                                          # REMOVE THIS WHEN IT IS DONE IN THE FUTURE WAY
    
    def update(self):
        screen.blit(self.surf,(self.posx,self.posy))

# LOOP

foods = []
for i in range(5):
    foods.append(Food(randint(0,600), randint(0,300), 10))
herbivores = []
for i in range(10):
    herbivores.append(Herbivore(randint(0,600), randint(0,300), randint(15,25)/10, randint(15,20), 200, 1))
    #herbivores.append(newHerbivore(randint(0,600), randint(0,300), randint(15,25)/10, randint(15,20), 200, foods))

running = True
while running:
    screen.fill("black")

    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()

    for food in foods:
        food.update()
    
    alive_herbivores = [] # update  all herbivores and collect survivors
    for herbivore in herbivores:
        herbivore.update()
        if herbivore.hunger > 0:
            alive_herbivores.append(herbivore)
    herbivores = alive_herbivores

    
    pygame.display.update()
    clock.tick(fps)