from game.gameobjects.Weaponry.weapon import Weapon
from game.gameobjects.Weaponry.weapon import DamageType
import math


class GodSword(Weapon):

    def __init__(self):
        super().__init__()

        self.damage = 12
        self.damage_type = DamageType.MELEE
        self.range = 1
        self.init()

    def init(self):
        self.sprite.loadTexture("data/sprites/god_sword.png")
        self.sprite.scale = 0.1
        self.sprite.rotation = 90 * (math.pi / 180)
