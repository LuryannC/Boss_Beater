import pyasge

from game.gameobjects.Weaponry.weapon import Weapon


class BasicSword(Weapon):

    def __init__(self):
        super().__init__()

        self.damage = 6
        self.range = 1
