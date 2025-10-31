from random import choice, randint
from math import cos, sin, radians, sqrt, atan2, dist
from constants import PREFIXES, VOWELS, SUFFIXES
from pygame import Surface

class Creature: # parent class for all creatures
    def __init__(self, x, y, speed, size, sight):
        self.posx, self.posy = x, y
        self.name = choice(PREFIXES) + choice(VOWELS) + choice(SUFFIXES)

        self.speed = speed
        self.size = size
        self.sight = sight

        self.action = randint(0,1)
        self.action_loops = 0
        self.move_dir = radians(0)
        
        self.surf = Surface((size,size))

    
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
