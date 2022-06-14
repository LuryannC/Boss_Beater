import pyasge

from game.gameobjects.Weaponry.weapon import Weapon
from game.gameobjects.Weaponry.weapon import DamageType


class Backhand(Weapon):

    def __init__(self):
        super().__init__()
        self.damage = 5
        self.range = 1
