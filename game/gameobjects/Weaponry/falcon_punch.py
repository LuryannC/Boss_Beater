from game.gameobjects.Weaponry.weapon import Weapon
from game.gameobjects.Weaponry.weapon import DamageType


class FalconPunch(Weapon):

    def __init__(self):
        super().__init__()

        self.damage = 8
        self.damage_type = DamageType.MELEE
        self.range = 1
