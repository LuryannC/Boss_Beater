import pyasge

from game.gameobjects.Weaponry.weapon import Weapon
from game.gameobjects.Weaponry.weapon import DamageType


class Bow(Weapon):

    def __init__(self):
        super().__init__()
        self.damage = 7
        self.damage_type = DamageType.RANGED
        self.range = 4
        self.init()

    def init(self):
        self.sprite.loadTexture("data/sprites/bow.png")
        self.sprite.scale = 0.3

