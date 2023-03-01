from ursina import color, raycast
from math import *

from block import *

class Grass(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "textures/grass_block.png"
        

