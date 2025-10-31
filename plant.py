from pygame import Surface

class Plant():
    def __init__(self, x, y, size):
        self.posx = x
        self.posy = y

        self.size = size
        self.surf = Surface((self.size,self.size))
        self.surf.fill("red")                                          # REMOVE THIS WHEN IT IS DONE IN THE FUTURE WAY
    
    def update(self, screen ):
        screen.blit(self.surf,(self.posx,self.posy))