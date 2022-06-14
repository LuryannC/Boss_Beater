import math

import pyasge
from abc import ABC, abstractmethod
from enum import Enum
from enum import IntEnum


class Entity(ABC):
    WEAK = 1.25
    MEDIUM = 1
    HEAVY = 0.75
    SUPER_HEAVY = 0.5

    @abstractmethod
    def __init__(self):
        self.max_health = 0
        self.current_health = 0
        self.speed = 500
        self.weapons = []
        self.active_weapon = None
        self.defending = False
        self.armor = self.MEDIUM
        self.sprite = pyasge.Sprite()

        self.position = pyasge.Point2D(0, 0)
        self.midpoint = pyasge.Point2D(0, 0)
        self.destination = []
        self.direction = pyasge.Point2D(0, 0)
        self.tile = (0, 0)

        self.damage_dealt = 0
        self.damage_taken = 0
        self.enemies_killed = 0

        self.sprite.z_order = 10
        self.movement_points = 8
        self.action_points = 2
        self.your_turn = False

    @abstractmethod
    def init(self):
        pass

    def attack(self, tile: tuple[int, int], entities: list):
        for entity in entities:
            if entity == self:
                continue
            if entity.tile == tile:
                if not self.defending:
                    entity.current_health -= self.active_weapon.damage * entity.armor
                    # Stat tracking
                    self.damage_dealt += self.active_weapon.damage * entity.armor
                    entity.damage_taken += self.active_weapon.damage * entity.armor
                    print("attacked square")
                    print("Damage dealt: " + str(self.active_weapon.damage * entity.armor))
                    print("current health: " + str(entity.current_health))
                else:
                    entity.current_health -= self.active_weapon.damage / (entity.armor * 2)
                    # Stat tracking
                    self.damage_dealt += self.active_weapon.damage * entity.armor
                    entity.damage_taken += self.active_weapon.damage * entity.armor

                # Stat tracking
                if entity.current_health <= 0:
                    self.enemies_killed += 1

                self.action_points -= 1

    def move_entity(self, path: list[pyasge.Point2D]) -> None:
        """Updates the entities destination route"""
        self.destination = path

        for path in self.destination:
            path.x -= self.width * 0.5
            path.y -= self.height * 0.5

        self.rotate()

    def rotate(self) -> None:
        """Orientate the ship depending on its direction"""
        if len(self.destination):
            if self.destination[0] == self.position:
                return

            # direction becomes target - current position normalised
            self.direction.x = self.destination[0].x - self.x
            self.direction.y = self.destination[0].y - self.y
            normalise = math.sqrt(self.direction.x * self.direction.x + self.direction.y * self.direction.y)
            self.direction.x /= normalise
            self.direction.y /= normalise

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """The fixed-update function moves the player at a constant speed"""
        if len(self.destination):
            if abs(self.position.distance(self.destination[0])) < self.speed * 0.02:
                self.position = self.destination.pop(0)
                self.midpoint = pyasge.Point2D(self.position.x + (self.sprite.width / 2),
                                               self.position.y + (self.sprite.height / 2))
                self.rotate()
                return

            self.position += self.direction * self.speed * game_time.fixed_timestep
            self.midpoint += self.direction * self.speed * game_time.fixed_timestep

    @abstractmethod
    def update(self, game_time: pyasge.GameTime, data) -> None:
        pass

    def render(self, renderer: pyasge.Renderer) -> None:
        renderer.render(self.sprite)
        renderer.render(self.active_weapon.sprite)

    @property
    def midpoint(self) -> pyasge.Point2D:
        return self.middle
        # return pyasge.Point2D(self.middle.x, self.middle.y)

    @midpoint.setter
    def midpoint(self, value: pyasge.Point2D) -> None:
        self.middle = value

    @property
    def position(self) -> pyasge.Point2D:
        return pyasge.Point2D(self.sprite.x, self.sprite.y)

    @position.setter
    def position(self, value: pyasge.Point2D) -> None:
        self.sprite.x = value.x
        self.sprite.y = value.y

    @property
    def height(self) -> float:
        return self.sprite.height

    @height.setter
    def height(self, value: float) -> None:
        self.sprite.height = value

    @property
    def width(self) -> float:
        return self.sprite.width

    @width.setter
    def width(self, value: float) -> None:
        self.sprite.width = value

    @property
    def x(self) -> float:
        return self.sprite.x

    @x.setter
    def x(self, value) -> None:
        self.sprite.x = value

    @property
    def y(self) -> float:
        return self.sprite.y

    @y.setter
    def y(self, value) -> None:
        self.sprite.y = value

    @property
    def tile(self):
        return self.tile_pos

    @tile.setter
    def tile(self, value) -> None:
        self.tile_pos = value
