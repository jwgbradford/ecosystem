from creature import Creature

class Herbivore(Creature): # prey/herbivore animal
    def __init__(self, x, y, speed, size, sight):
        super().__init__(x, y, speed, size, sight)
        self.surf.fill("white")
    
    