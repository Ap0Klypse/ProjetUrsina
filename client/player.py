from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_sensitivity = (155, 155)

class PlayerRepresentation(Entity):
    def __init__(self, position = (5,5,5)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'folder/MANNO.obj',
            texture = 'folder/MANNO.mtl',
            double_sided=True,
            origin_y = -1,
            scale = 0.5
        )
        print("HELLO !")