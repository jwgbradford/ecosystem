from plant import Plant
from herbivore import Herbivore
from constants import BACKGROUND, FPS
from random import randint
from pygame import time, display, event, quit, QUIT

class Game():
    def __init__(self):
        self.clock = time.Clock()
        screen_width = 640
        screen_height = 360
        
        self.screen = display.set_mode((screen_width, screen_height))
        display.set_caption('ecosystem test')

        self.herbivores = []
        self.plants = []

        for i in range(5):
            self.herbivores.append(Herbivore(randint(0,600), randint(0,300), randint(15,25) / 10, randint(15,20), randint(20,30) * 10))
            self.plants.append(Plant(randint(0,600), randint(0,300), 10)) # food when added
        
        self.game_speed = 1 # when ui is added, should be able to be changed

    def update(self):
        self.screen.fill(BACKGROUND)

        for plant in self.plants:
            plant.update(self.screen)
        for herbivore in self.herbivores:
            herbivore.update(self.screen)

        display.update()
        self.clock.tick(FPS * self.game_speed)

    def run(self):
        running = True
        while running:
            for each_event in event.get():
                if each_event.type == QUIT:
                    quit()
            self.update()


if __name__ == "__main__":
    my_game = Game()
    my_game.run()

