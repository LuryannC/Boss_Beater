import pyasge
from enum import Enum
from abc import ABC, abstractmethod


class DamageType(Enum):
    MELEE = 1
    RANGED = 2


class Weapon(ABC):

    @abstractmethod
    def __init__(self):
        self.damage = 2
        self.sprite = pyasge.Sprite()
        self.attacks = []
        self.damage_type = DamageType.MELEE
        self.range = 1

        self.sprite.z_order = 52
