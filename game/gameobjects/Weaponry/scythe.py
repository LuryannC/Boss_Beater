import pyasge

from game.gameobjects.Weaponry.weapon import Weapon
from game.gameobjects.Weaponry.weapon import DamageType


class Scythe(Weapon):

    def __init__(self):
        super().__init__()
        self.damage = 10
        self.range = 1
