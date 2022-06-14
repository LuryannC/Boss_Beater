from game.gameobjects.Weaponry.weapon import Weapon
from game.gameobjects.Weaponry.weapon import DamageType


class EnragedWeapon(Weapon):

    def __init__(self):
        super().__init__()

        self.damage = 12
        self.damage_type = DamageType.MELEE
        self.range = 1
