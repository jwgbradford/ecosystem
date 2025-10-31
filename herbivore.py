from creature import Creature

class Herbivore(Creature): # prey/herbivore animal
    def __init__(self, x, y, speed, size, sight):
        super().__init__(x, y, speed, size, sight)
        self.surf.fill("white")
    
    def update(self, screen):
        screen_width, screen_height = screen.get_size()
        #self.food(game.plants)
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

        screen.blit(self.surf, (self.posx,self.posy)) # might need to return screen